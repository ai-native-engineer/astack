#!/usr/bin/env python3
"""Create a minimal AGENTS.md + progress.tsv goal plan.

Plans can live in a target repo worktree or in a dedicated repo under
~/.agents/goals.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
import sys


DEFAULT_GOAL = "TBD: one measurable end state for this goal"
DEFAULT_DEDICATED_ROOT = Path("~/.agents/goals")
SKILL_ROOT = Path(__file__).resolve().parent.parent
AGENTS_TEMPLATE = SKILL_ROOT / "templates" / "AGENTS.md.tmpl"
GOAL_START = "<!-- goal-plan:start -->"
GOAL_END = "<!-- goal-plan:end -->"


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


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "goal"


def timestamped_goal_path(root: Path, name: str) -> Path:
    stamp = datetime.now().strftime("%y%m%d-%H%M%S")
    return root.expanduser().resolve() / f"{stamp}-{slugify(name)}"


def add_worktree(root: Path, tag: str, worktree_root: Path) -> Path:
    """Create a timestamped external goal/<tag> worktree."""
    wt = timestamped_goal_path(worktree_root, tag)
    wt.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "-C", str(root), "worktree", "add", "-b", f"goal/{tag}", str(wt)],
                   check=True, capture_output=True, text=True)
    return wt


def goal_instructions(goal: str, progress_file: str, goal_log: str) -> str:
    clean_goal = tsv_cell(goal).strip() or DEFAULT_GOAL
    try:
        template = AGENTS_TEMPLATE.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"missing goal template: {AGENTS_TEMPLATE}") from exc
    missing = [
        marker for marker in ["{{GOAL}}", "{{PROGRESS_FILE}}", "{{GOAL_LOG}}"]
        if marker not in template
    ]
    if missing:
        raise ValueError(f"goal template missing placeholders: {', '.join(missing)}")

    return (
        template
        .replace("{{GOAL}}", clean_goal)
        .replace("{{PROGRESS_FILE}}", progress_file)
        .replace("{{GOAL_LOG}}", goal_log)
    )


def goal_block(goal: str, progress_file: str, goal_log: str) -> str:
    body = goal_instructions(goal, progress_file, goal_log).strip()
    return f"{GOAL_START}\n{body}\n{GOAL_END}\n"


def merge_agents(existing: str, block: str) -> str:
    has_start = GOAL_START in existing
    has_end = GOAL_END in existing
    if has_start != has_end:
        raise ValueError("AGENTS.md has partial goal-plan markers")
    if has_start:
        before, rest = existing.split(GOAL_START, 1)
        _, after = rest.split(GOAL_END, 1)
        return f"{before.rstrip()}\n\n{block.rstrip()}\n\n{after.lstrip()}".rstrip() + "\n"
    prefix = existing.rstrip()
    return f"{prefix}\n\n{block}" if prefix else block


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


def backup_existing(path: Path) -> str | None:
    if not path.exists():
        return None
    backup = path.with_name(path.name + ".bak")
    shutil.copy2(path, backup)
    return f"backed up {path} to {backup}"


def write_agents(path: Path, block: str) -> list[str]:
    messages = []
    backup = backup_existing(path)
    if backup:
        messages.append(backup)
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    path.write_text(merge_agents(existing, block), encoding="utf-8")
    messages.append(f"wrote {path}")
    return messages


def write_claude(path: Path) -> list[str]:
    messages = []
    content = "@AGENTS.md\n"
    if path.exists() and path.read_text(encoding="utf-8") == content:
        return [f"kept existing {path}"]
    backup = backup_existing(path)
    if backup:
        messages.append(backup)
    path.write_text(content, encoding="utf-8")
    messages.append(f"wrote {path}")
    return messages


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", default=".", help="Target repo (worktree mode) or workspace directory")
    parser.add_argument("--goal", default=DEFAULT_GOAL, help="Measurable completion condition")
    parser.add_argument("--worktree", metavar="TAG", default=None,
                        help="Create the plan in a timestamped external goal/<TAG> git worktree")
    parser.add_argument("--worktree-root", default=str(DEFAULT_DEDICATED_ROOT),
                        help="Root for --worktree worktrees (default: ~/.agents/goals)")
    parser.add_argument("--dedicated", metavar="NAME", default=None,
                        help="Create a dedicated goal repo at ~/.agents/goals/YYMMDD-HHMMSS-<NAME>")
    parser.add_argument("--dedicated-root", default=str(DEFAULT_DEDICATED_ROOT),
                        help="Root for --dedicated repos (default: ~/.agents/goals)")
    parser.add_argument("--progress-file", default="progress.tsv", help="Progress TSV file name")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files")
    args = parser.parse_args(argv)

    if args.worktree and args.dedicated:
        print("error: choose either --worktree or --dedicated, not both", file=sys.stderr)
        return 2
    if args.dedicated and args.path != ".":
        print("error: --dedicated creates its own path; use --dedicated-root to change the root",
              file=sys.stderr)
        return 2

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
            target = add_worktree(root, args.worktree, Path(args.worktree_root))
        except subprocess.CalledProcessError as exc:
            detail = (exc.stderr or "").strip() or f"exit {exc.returncode}"
            print(f"error: git worktree add failed: {detail} "
                  f"(branch goal/{args.worktree} or its worktree may already exist)", file=sys.stderr)
            return 2

    if args.dedicated:
        target = timestamped_goal_path(Path(args.dedicated_root), args.dedicated)

    target.mkdir(parents=True, exist_ok=True)
    if args.dedicated and not (target / ".git").exists():
        try:
            subprocess.run(["git", "-C", str(target), "init"],
                           check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as exc:
            detail = (exc.stderr or "").strip() or f"exit {exc.returncode}"
            print(f"error: git init failed: {detail}", file=sys.stderr)
            return 2

    progress_file = args.progress_file
    goal_log = str(Path(__file__).resolve().parent / "goal_log.py")

    messages = []
    try:
        messages.extend(write_agents(target / "AGENTS.md",
                                     goal_block(args.goal, progress_file, goal_log)))
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    messages.extend(write_claude(target / "CLAUDE.md"))
    messages.append(write_file(target / progress_file, progress_tsv(args.goal), args.force))
    if args.worktree:
        messages.append(f"worktree ready at {target} (branch goal/{args.worktree})")
    if args.dedicated:
        messages.append(f"dedicated goal repo ready at {target}")
    if not args.worktree and not args.dedicated:
        messages.append(f"goal workspace ready at {target}")
    messages.extend([
        "next: fill every TBD, add initial progress rows, commit the plan, then stop",
        "handoff overview: summarize goal, acceptance criteria, proof, progress rows, workspace, branch, and plan commit",
        f"run: !cd {target}",
        "run: /goal @AGENTS.md",
    ])
    print("\n".join(messages))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
