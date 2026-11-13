#!/usr/bin/env python3
"""Worker branches for a goal: start one, integrate its PR.

`start` creates the worker branch and worktree for a row and records the
assignment. `integrate` merges the worker's reviewed PR into the goal branch as
one commit that also carries the row's ledger update, pushes, closes the row's
issue, and removes the worker branch and worktree. Run from the goal workspace.
The orchestrator reviews the PR diff and the row's proof before `integrate`.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from argparse import Namespace
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import goal_issue  # noqa: E402
import goal_log  # noqa: E402
import goal_pr  # noqa: E402

TYPES = ("feat", "fix", "docs", "style", "refactor", "test", "chore")
DESC_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
OPEN_ROWS = {"todo", "doing"}
CONFIRM_ATTEMPTS = 5
SHA_RE = re.compile(r"^[0-9a-f]{40}$")


class Refused(Exception):
    """A precondition failed; nothing was changed."""


def git(*args: str, cwd: Path | None = None, check: bool = True) -> str:
    result = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, check=False)
    if check and result.returncode != 0:
        detail = (result.stderr or result.stdout).strip() or f"exit {result.returncode}"
        raise RuntimeError(f"git {' '.join(args)}: {detail}")
    return result.stdout.strip()


def dirty_paths(cwd: Path, untracked: bool) -> list[str]:
    """Paths `git status --porcelain` reports (not stripped, so the XY columns stay aligned)."""
    flag = "--untracked-files=all" if untracked else "--untracked-files=no"
    out = subprocess.run(["git", "status", "--porcelain", flag], cwd=cwd, capture_output=True, text=True).stdout
    return [line[3:] for line in out.splitlines()]


def worktree_registered(root: Path, path: str, branch: str) -> bool:
    """True when `git worktree list` has this path registered with this branch checked out."""
    listing = git("worktree", "list", "--porcelain", cwd=root)
    for block in listing.split("\n\n"):
        lines = block.splitlines()
        if (f"branch refs/heads/{branch}" in lines and any(
                line.startswith("worktree ") and Path(line[len("worktree "):]).resolve() == Path(path).resolve()
                for line in lines)):
            return True
    return False


def gh(*args: str, repo: str | None) -> str:
    cmd = ["gh", *args] + (["--repo", repo] if repo else [])
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        detail = (result.stderr or result.stdout).strip() or f"exit {result.returncode}"
        raise RuntimeError(f"gh {' '.join(args)}: {detail}")
    return result.stdout.strip()


def row_issue(row: dict) -> str | None:
    match = re.match(r"#(\d+)\b", row.get("task", ""))
    return match.group(1) if match else None


def tracking_issue(root: Path) -> str | None:
    goal = root / "GOAL.md"
    if not goal.is_file():
        return None
    match = re.search(r"tracking issue:\s*#(\d+)", goal.read_text(encoding="utf-8"))
    return match.group(1) if match else None


def load_row(path: Path, row_id: str) -> dict:
    _, rows = goal_log.read_rows(path)
    row = goal_log.find_row(rows, row_id)
    if row is None:
        ids = ", ".join(r.get("id", "") for r in rows) or "(none)"
        raise Refused(f"no row id={row_id}. existing ids: {ids}")
    return row


def has_value(value: str) -> bool:
    return value.strip() not in {"", "-"}


def cmd_start(args: argparse.Namespace, root: Path, goal_branch: str, progress: Path) -> int:
    if args.type not in TYPES:
        raise Refused(f"--type must be one of {', '.join(TYPES)}")
    if not DESC_RE.match(args.desc):
        raise Refused("--desc must be lowercase kebab-case")
    row = load_row(progress, args.row)
    if row["status"] != "todo":
        raise Refused(f"row {args.row} is {row['status']}; only a todo row can start a worker")
    issue = row_issue(row) or tracking_issue(root)
    if issue is None:
        print("warning: no issue number for this row or GOAL.md; branch has no issue prefix", file=sys.stderr)
    branch = f"{args.type}/{issue}-{args.desc}" if issue else f"{args.type}/{args.desc}"
    worktree = Path(args.worktree).expanduser().resolve() if args.worktree \
        else root.parent / branch.replace("/", "-")
    if worktree.exists():
        raise Refused(f"worktree path exists: {worktree}")
    if git("branch", "--list", branch, cwd=root):
        raise Refused(f"branch {branch} already exists")

    fetch = subprocess.run(["git", "fetch", "-q", args.remote], cwd=root, capture_output=True, text=True)
    if fetch.returncode != 0:
        print(f"warning: git fetch {args.remote} failed: {fetch.stderr.strip()}", file=sys.stderr)
    ahead = git("rev-list", "--count", f"{args.remote}/{goal_branch}..{goal_branch}", cwd=root, check=False)
    if ahead not in {"", "0"}:
        print(f"warning: {goal_branch} has {ahead} commit(s) not on {args.remote}; push before the worker "
              "opens its PR", file=sys.stderr)
    git("worktree", "add", "--no-track", "-b", branch, str(worktree), goal_branch, cwd=root)
    ns = Namespace(file=str(progress), id=args.row, worker=args.worker, branch=branch,
                   worktree=str(worktree), depends_on=None)
    if goal_log.cmd_assign(ns) or goal_log.cmd_start(Namespace(file=str(progress), id=args.row)):
        raise RuntimeError(f"worktree {worktree} was created but the ledger update failed")
    print(f"branch: {branch}")
    print(f"worktree: {worktree}")
    return 0


def check_integrable(args: argparse.Namespace, root: Path, goal_branch: str, progress: Path,
                     row: dict) -> tuple[dict, str]:
    """Return (PR data, remote head oid) or raise Refused listing every failed check."""
    problems: list[str] = []
    branch = row.get("branch", "")
    if row["status"] not in OPEN_ROWS:
        problems.append(f"row {args.row} is {row['status']}; only doing or todo rows integrate")
    if not has_value(branch):
        raise Refused(f"row {args.row} has no branch; run `start` first")
    default = goal_pr.default_base(root, args.remote, args.repo)
    if not goal_pr.BRANCH_RE.match(branch) or branch.split("/", 1)[1] in goal_pr.PROTECTED:
        raise Refused(f"row branch {branch} is not a plain work branch (<type>/<description>, not protected)")
    if branch in {goal_branch, default}:
        raise Refused(f"row branch {branch} is the goal branch or the repository default branch")

    pr = json.loads(gh("pr", "view", str(args.pr), "--json", "state,baseRefName,headRefName,headRefOid,title",
                       repo=args.repo))
    if pr.get("state") != "OPEN":
        problems.append(f"PR #{args.pr} is {pr.get('state')}, not OPEN")
    if pr.get("baseRefName") != goal_branch:
        problems.append(f"PR #{args.pr} targets {pr.get('baseRefName')}, not the goal branch {goal_branch}")
    if pr.get("headRefName") != branch:
        problems.append(f"PR #{args.pr} head is {pr.get('headRefName')}, not the row branch {branch}")

    remote_oid = git("ls-remote", "--heads", args.remote, f"refs/heads/{branch}", cwd=root,
                     check=False).split("\t")[0]
    if not SHA_RE.match(args.head):
        problems.append("--head must be the full 40-character sha of the reviewed commit")
    if not remote_oid:
        problems.append(f"{branch} is not on {args.remote}")
    elif remote_oid != pr.get("headRefOid"):
        problems.append(f"PR head {pr.get('headRefOid')} differs from {args.remote}/{branch} {remote_oid}")
    elif remote_oid != args.head:
        problems.append(f"--head {args.head} is not the PR head and {args.remote}/{branch} tip {remote_oid}; "
                        "review the new commits and pass the new sha")
    else:
        git("fetch", "-q", args.remote, cwd=root)
        owned = subprocess.run(["git", "diff", "--name-only", f"{goal_branch}...{args.head}"], cwd=root,
                               capture_output=True, text=True)
        if owned.returncode != 0:
            problems.append(f"cannot diff {args.head} against {goal_branch}: {owned.stderr.strip()}")
        touched = sorted(set(owned.stdout.split()) & set(goal_pr.SCAFFOLD_FILES))
        if touched:
            problems.append("the worker diff touches orchestrator-owned files: " + ", ".join(touched))
        if git("rev-parse", "-q", "--verify", f"refs/heads/{branch}", cwd=root, check=False):
            local = git("rev-parse", f"refs/heads/{branch}", cwd=root)
            if subprocess.run(["git", "merge-base", "--is-ancestor", local, remote_oid], cwd=root).returncode != 0:
                problems.append(f"local {branch} has commits not on {args.remote}")

    worktree = row.get("worktree", "")
    if has_value(worktree) and Path(worktree).is_dir() and dirty_paths(Path(worktree), True):
        problems.append(f"worker worktree {worktree} is not clean")

    dirty = [path for path in dirty_paths(root, False) if path != progress.name]
    if dirty:
        problems.append("goal workspace has changes besides " + progress.name + ": " + ", ".join(dirty))
    if problems:
        raise Refused("\n".join(problems))
    return pr, remote_oid


def confirm_merged(pr_number: str, repo: str | None) -> bool:
    delay = float(os.environ.get("GOAL_WORKER_CONFIRM_DELAY", "2"))
    for attempt in range(CONFIRM_ATTEMPTS):
        if gh("pr", "view", pr_number, "--json", "state", "--jq", ".state", repo=repo) == "MERGED":
            return True
        if attempt + 1 < CONFIRM_ATTEMPTS:
            time.sleep(delay)
    return False


def cmd_integrate(args: argparse.Namespace, root: Path, goal_branch: str, progress: Path) -> int:
    row = load_row(progress, args.row)
    pr, _ = check_integrable(args, root, goal_branch, progress, row)
    branch, worktree = row["branch"], row.get("worktree", "")

    merge = subprocess.run(["git", "merge", "--no-ff", "--no-commit", args.head], cwd=root,
                           capture_output=True, text=True)
    merging = subprocess.run(["git", "rev-parse", "-q", "--verify", "MERGE_HEAD"], cwd=root,
                             capture_output=True).returncode == 0
    if merge.returncode != 0 or not merging:
        git("merge", "--abort", cwd=root, check=False)
        print((merge.stdout + merge.stderr).strip() or f"nothing to merge from {branch}", file=sys.stderr)
        print(f"error: merging {branch} failed; merge aborted, nothing else changed", file=sys.stderr)
        return 1

    snapshot = progress.read_bytes()

    def undo(reason: str, detail: str = "") -> int:
        """Leave the workspace as it was before the merge, other rows' uncommitted ledger entries included."""
        git("merge", "--abort", cwd=root, check=False)
        progress.write_bytes(snapshot)
        if detail:
            print(detail, file=sys.stderr)
        print(f"error: {reason}; merge aborted, workspace restored, nothing else changed", file=sys.stderr)
        return 1

    done = Namespace(file=str(progress), id=args.row, decision="keep", artifact=args.artifact, notes=None)
    if goal_log.cmd_done(done):
        return undo("ledger update failed")
    title = pr["title"]
    if not re.search(r"#\d+", title):
        print(f"warning: PR title has no issue number (#N): {title}", file=sys.stderr)
    staged = subprocess.run(["git", "add", "--", str(progress)], cwd=root, capture_output=True, text=True)
    committed = staged if staged.returncode != 0 else subprocess.run(
        ["git", "commit", "-q", "-m", title, "-m", f"Worker PR #{args.pr}, branch {branch}"],
        cwd=root, capture_output=True, text=True)
    if committed.returncode != 0:
        return undo("commit failed", (committed.stdout + committed.stderr).strip())
    print(f"merged {branch} into {goal_branch}: {git('rev-parse', '--short', 'HEAD', cwd=root)}")

    push = subprocess.run(["git", "push", "-q", args.remote, goal_branch], cwd=root,
                          capture_output=True, text=True)
    if push.returncode != 0:
        print(f"error: push rejected: {push.stderr.strip()}", file=sys.stderr)
        print(f"The merge commit is local on {goal_branch}; the worker branch and worktree are untouched.\n"
              f"Recover: git fetch {args.remote}, merge or rebase {args.remote}/{goal_branch} "
              f"(never force-push), push, then remove the worker branch and worktree by hand.",
              file=sys.stderr)
        return 1

    if not confirm_merged(str(args.pr), args.repo):
        print(f"error: PR #{args.pr} is not MERGED after the push; nothing deleted. "
              f"Check the PR on GitHub, then remove {branch} and its worktree by hand.", file=sys.stderr)
        return 1

    left: list[str] = []
    issue = row_issue(row)
    if args.keep_issue or issue is None:
        print("issue: left open" + ("" if args.keep_issue else " (row has no issue)"))
    else:
        comment = f"{args.artifact} (PR #{args.pr})"
        issue_args = (["--repo", args.repo] if args.repo else []) + ["close", issue, "--reason", "completed",
                                                                      "--comment", comment]
        if goal_issue.main(issue_args) != 0:
            left.append(f"issue #{issue} still open")
    if has_value(worktree) and Path(worktree).exists() and not worktree_registered(root, worktree, branch):
        left.append(f"worktree {worktree}: not registered with branch {branch} in `git worktree list`; kept")
    elif has_value(worktree) and Path(worktree).exists():
        removed = subprocess.run(["git", "worktree", "remove", worktree], cwd=root, capture_output=True, text=True)
        if removed.returncode != 0:
            left.append(f"worktree {worktree}: {removed.stderr.strip()}")
    deleted = subprocess.run(["git", "branch", "-d", branch], cwd=root, capture_output=True, text=True)
    if deleted.returncode != 0:
        left.append(f"local branch {branch}: {deleted.stderr.strip()}")
    remote = subprocess.run(["git", "push", "-q", f"--force-with-lease=refs/heads/{branch}:{args.head}",
                             "--delete", args.remote, branch], cwd=root, capture_output=True, text=True)
    if remote.returncode != 0:
        left.append(f"remote branch {args.remote}/{branch}: {remote.stderr.strip()}")
    if left:
        print("error: merged, but cleanup left behind:\n  " + "\n  ".join(left), file=sys.stderr)
        return 1
    print(f"removed {branch}, its worktree" + ("" if args.keep_issue or issue is None else f", closed #{issue}"))
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--file", default="progress.tsv", help="progress TSV in the goal workspace")
    parser.add_argument("--remote", default="origin")
    parser.add_argument("--repo", default=None, help="owner/name for gh; required on a fork")
    sub = parser.add_subparsers(dest="cmd", required=True)

    st = sub.add_parser("start", help="create the worker branch and worktree for a row, record and start it")
    st.add_argument("row")
    st.add_argument("--worker", required=True)
    st.add_argument("--type", required=True, help=", ".join(TYPES))
    st.add_argument("--desc", required=True, help="lowercase kebab-case description")
    st.add_argument("--worktree", default=None, help="worktree path (default: sibling of the goal worktree)")
    st.set_defaults(func=cmd_start)

    it = sub.add_parser("integrate", help="merge a reviewed worker PR into the goal branch and clean up")
    it.add_argument("row")
    it.add_argument("--pr", required=True, type=int)
    it.add_argument("--head", required=True, help="full sha of the reviewed worker commit; the merge is bound to it")
    it.add_argument("--artifact", required=True, help="the row's proof, recorded in the ledger and issue")
    it.add_argument("--keep-issue", action="store_true", help="leave the issue open (several rows share it)")
    it.set_defaults(func=cmd_integrate)

    args = parser.parse_args(argv)
    try:
        root = Path(git("rev-parse", "--show-toplevel"))
        os.chdir(root)
        goal_branch = git("branch", "--show-current", cwd=root)
        if not goal_branch:
            raise Refused("detached HEAD; check out the goal branch first")
        return args.func(args, root, goal_branch, Path(args.file).resolve())
    except Refused as exc:
        print(f"refused, nothing changed:\n{exc}", file=sys.stderr)
        return 2
    except (RuntimeError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
