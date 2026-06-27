#!/usr/bin/env python3
"""Create a minimal GOAL.md + progress.tsv goal plan, optionally in a git worktree."""

from __future__ import annotations

import argparse
import subprocess
from datetime import datetime, timezone
from pathlib import Path
import sys
from textwrap import dedent


DEFAULT_GOAL = "TBD: one measurable end state for this goal"


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def tsv_cell(value: str) -> str:
    return value.replace("\t", " ").replace("\r", " ").replace("\n", " ")


def repo_root(path: Path) -> Path | None:
    """Top level of the git repo containing path, or None when path is not in one."""
    probe = path if path.is_dir() else path.parent
    try:
        out = subprocess.run(["git", "-C", str(probe), "rev-parse", "--show-toplevel"],
                             capture_output=True, text=True, check=True)
        return Path(out.stdout.strip())
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def add_worktree(root: Path, tag: str) -> Path:
    """Create (or reuse) a goal/<tag> worktree under <root>/.claude/worktrees."""
    wt = root / ".claude" / "worktrees" / f"goal-{tag}"
    if wt.exists():
        return wt
    wt.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "-C", str(root), "worktree", "add", "-b", f"goal/{tag}", str(wt)],
                   check=True, capture_output=True, text=True)
    return wt


def goal_md(goal: str, progress_file: str, goal_log: str) -> str:
    clean_goal = tsv_cell(goal).strip() or DEFAULT_GOAL
    return dedent(
        f"""\
        # Goal Plan Instructions

        Long-running agent work that continues until a verifiable condition holds.
        Start the loop with `/goal @GOAL.md`.

        ## Goal

        {clean_goal}

        ## Proof

        TBD: the exact command or check that proves the Goal (propose it from the repo, then confirm). Make it deterministic and repeatable -- test exit code, build status, count, artifact exists -- not a "looks good" judgment, because on an unattended run the agent is the only verifier.

        ## Context

        TBD: background, repo layout, and the docs/decisions to read before working. Repo-local context is the system of record; if it is not reachable from here, it does not exist for this goal.

        ## Scope

        TBD: what this goal includes.

        ## Out of Scope

        TBD: what is explicitly excluded or deferred.

        ## Constraints

        TBD: what must not change, required tools, paths git may touch, and -- for unattended running -- which irreversible actions (deleting files, network calls, sending or publishing, payments) are pre-approved versus must pause for the user. For destructive actions use `git revert`, never `git reset --hard` or force-push, and delete files only inside a staged commit.

        ## Bounds

        TBD: turn or time limit for unattended running (e.g. "stop after 30 turns", "8 hours", or "none" with supervision). If one step blows its time budget, record it as a failure and move on.

        ## How Progress Is Tracked

        - `{progress_file}` is the plan and progress table; the task breakdown lives in its rows. Edit it ONLY through the helper so rows never break on tab matching:
          `python3 {goal_log} <add|start|done|block|drop|set|show> ...` (flags: `<cmd> --help`).
        - This plan lives on its own `goal/<tag>` branch (a worktree, or a dedicated goal repo). Each loop step ends in a commit, so the commit history is the durable record. `goal_log.py done` stamps the current `HEAD` as the row checkpoint; the commit you make immediately after records the row update. The checkpoint plus git history is your resume point: on resume, recover state with `pwd`, `goal_log.py show`, `git log`, then re-run the Proof.
        - On a long run, watch the context window and compact old turns when it fills, keeping the Proof output and `{progress_file}` intact (in Claude Code, `/context` to check and `/compact` to summarize); repeated compaction lets the loop run for many more hours.

        ## Loop Protocol

        Run as an autonomous loop until the Goal holds.

        1. `goal_log.py show` to see where you are.
        2. Take the next row (or `goal_log.py add --task ...`), then `goal_log.py start <id>`. Pick the row most likely to advance the Goal or unblock the rest, not just the next in line.
        3. Do the work within Scope and Constraints, then run the Proof.
        4. `goal_log.py done <id> --decision keep|discard|crash --artifact "<proof>"` (keep if it advanced the goal; discard if it did not but did no harm; crash if it caused a regression). Be skeptical of your own success -- if the Proof passed quietly, rerun it before marking done. Every done row needs artifact or notes evidence; for discard/crash, put WHY it failed and what to try instead in notes so a later session does not repeat the dead end.
        5. Commit the changed files plus `{progress_file}`: `git add <files> {progress_file} && git commit -m "<keep|discard>: <what you did>"`.
        6. Surface the Proof in your reply as evidence, not a claim: paste the actual command output (pass/fail, line numbers, exact errors), then name the checkpoint, what you verified this step, what remains, and whether you are blocked. The `/goal` evaluator reads the conversation, not the files.
        7. To undo a change that made things worse, revert with git, sparingly. Do not `git reset` away failed attempts you have already committed -- the commit log is the full record, including discards.

        Do not ask "should I continue?" once the loop starts. Stop only when the Goal holds, when you hit a Bound, or when blocked by missing access, destructive risk, or an explicit user choice -- when blocked, report what specific input or access would unblock you. Budget or turn exhaustion is not completion.

        ## Completion

        Complete only when the Goal holds and is shown with the Proof output in the conversation or logs, and required rows in `{progress_file}` are `done` or intentionally `dropped`.
        """
    )


def progress_tsv(goal: str) -> str:
    timestamp = now_iso()
    clean_goal = tsv_cell(goal).strip() or DEFAULT_GOAL
    header = "id\tstatus\tdecision\ttask\tdone_when\tcheckpoint\tartifact\tnext\tnotes"
    row = "\t".join([
        "0",
        "todo",
        "n/a",
        "Record baseline/current state",
        clean_goal,
        "-",
        "-",
        "goal_log.py add --task ... to queue the first implementation row",
        f"Initialized goal plan at {timestamp}",
    ])
    return f"{header}\n{row}\n"


def write_file(path: Path, content: str, force: bool) -> str:
    if path.exists() and not force:
        return f"skipped existing {path}"
    path.write_text(content, encoding="utf-8")
    return f"wrote {path}"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", default=".", help="Target repo (worktree mode) or workspace directory")
    parser.add_argument("--goal", default=DEFAULT_GOAL, help="Measurable completion condition")
    parser.add_argument("--worktree", metavar="TAG", default=None,
                        help="Create the plan in a new goal/<TAG> git worktree under <repo>/.claude/worktrees")
    parser.add_argument("--progress-file", default="progress.tsv", help="Progress TSV file name")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files")
    args = parser.parse_args(argv)

    target = Path(args.path).expanduser().resolve()
    if target.exists() and not target.is_dir():
        print(f"error: target is not a directory: {target}", file=sys.stderr)
        return 2

    if args.worktree:
        root = repo_root(target)
        if root is None:
            print(f"error: --worktree needs a git repo at {target}. Either `git init` it, "
                  f"or drop --worktree and pass a dedicated goal repo directory instead.",
                  file=sys.stderr)
            return 2
        try:
            target = add_worktree(root, args.worktree)
        except subprocess.CalledProcessError as exc:
            detail = (exc.stderr or "").strip() or f"exit {exc.returncode}"
            print(f"error: git worktree add failed: {detail} "
                  f"(branch goal/{args.worktree} or its worktree may already exist)", file=sys.stderr)
            return 2

    target.mkdir(parents=True, exist_ok=True)
    progress_file = args.progress_file
    goal_log = str(Path(__file__).resolve().parent / "goal_log.py")

    messages = [
        write_file(target / "GOAL.md", goal_md(args.goal, progress_file, goal_log), args.force),
        write_file(target / progress_file, progress_tsv(args.goal), args.force),
    ]
    if args.worktree:
        messages.append(f"worktree ready at {target} (branch goal/{args.worktree}); "
                        f"start the loop there with `/goal @GOAL.md`")
    print("\n".join(messages))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
