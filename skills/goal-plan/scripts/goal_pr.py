#!/usr/bin/env python3
"""Open the result PR for a goal.

Branches from the current goal branch, removes the goal scaffold files in one
commit so the PR carries only the work, pushes the branch, and opens the PR
with `gh`. Run from the goal workspace after the Proof passes.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import tempfile
from pathlib import Path


SCAFFOLD_FILES = ["GOAL.md", "progress.tsv", ".claude/settings.json", ".codex/hooks.json"]
BRANCH_RE = re.compile(r"^(feat|fix|docs|style|refactor|test|chore)/[A-Za-z0-9][A-Za-z0-9._/-]*$")
PROTECTED = {"main", "master", "develop"}


def git(*args: str, cwd: Path | None = None, check: bool = True) -> str:
    result = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, check=False)
    if check and result.returncode != 0:
        detail = (result.stderr or result.stdout).strip() or f"exit {result.returncode}"
        raise RuntimeError(f"git {' '.join(args)}: {detail}")
    return result.stdout.strip()


def default_base(root: Path, remote: str) -> str:
    try:
        ref = git("symbolic-ref", "--short", f"refs/remotes/{remote}/HEAD", cwd=root)
        return ref.split("/", 1)[1]
    except RuntimeError:
        pass
    probe = subprocess.run(["gh", "repo", "view", "--json", "defaultBranchRef",
                            "--jq", ".defaultBranchRef.name"],
                           cwd=root, capture_output=True, text=True, check=False)
    name = probe.stdout.strip()
    return name if probe.returncode == 0 and name else "main"


def branch_exists(root: Path, branch: str, remote: str) -> str | None:
    if git("branch", "--list", branch, cwd=root):
        return "locally"
    if git("ls-remote", "--heads", remote, branch, cwd=root, check=False):
        return f"on {remote}"
    return None


def tracking_issue(root: Path) -> str | None:
    """Tracking issue number from GOAL.md GitHub Flow, or None when not recorded."""
    goal = root / "GOAL.md"
    if not goal.is_file():
        return None
    match = re.search(r"tracking issue:\s*#(\d+)", goal.read_text(encoding="utf-8"))
    return match.group(1) if match else None


def unlinked_commits(work: Path, base_ref: str, branch: str, skip_subject: str) -> list[str]:
    """Commits on the result branch whose subject names no issue (#N).

    A warning, not a failure: the PR still closes its issues, but a commit without a
    number does not appear on any issue timeline.
    """
    log = git("log", "--format=%h %s", f"{base_ref}..{branch}", cwd=work, check=False)
    return [line for line in log.splitlines()
            if not re.search(r"#\d+", line) and not line.endswith(skip_subject)]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--branch", required=True, help="Result branch name, <type>/<description>")
    parser.add_argument("--base", default=None, help="PR base branch (default: the remote default branch)")
    parser.add_argument("--remote", default="origin")
    parser.add_argument("--title", default=None, help="PR title, <type>(<scope>): <subject>")
    parser.add_argument("--body-file", default=None, help="Markdown file with the PR body")
    parser.add_argument("--include", action="append", default=[],
                        help="Scaffold file to keep in the result (repeatable)")
    parser.add_argument("--exclude", action="append", default=[],
                        help="Extra path to drop from the result (repeatable)")
    parser.add_argument("--draft", action="store_true", help="Open the PR as a draft")
    parser.add_argument("--dry-run", action="store_true", help="Build the result branch, do not push")
    parser.add_argument("--no-pr", action="store_true", help="Push the branch, do not open a PR")
    args = parser.parse_args(argv)

    if not BRANCH_RE.match(args.branch) or args.branch.split("/", 1)[1] in PROTECTED:
        print("error: --branch must be <type>/<description> and not a protected branch", file=sys.stderr)
        return 2
    opens_pr = not args.dry_run and not args.no_pr
    if opens_pr and (not args.title or not args.body_file):
        print("error: --title and --body-file are required to open the PR", file=sys.stderr)
        return 2
    if args.body_file and not Path(args.body_file).is_file():
        print(f"error: body file not found: {args.body_file}", file=sys.stderr)
        return 2

    try:
        root = Path(git("rev-parse", "--show-toplevel"))
        goal_branch = git("branch", "--show-current", cwd=root)
        if not goal_branch:
            print("error: detached HEAD; check out the goal branch first", file=sys.stderr)
            return 2
        if git("status", "--porcelain", "--untracked-files=no", cwd=root):
            print("error: uncommitted changes; commit or revert them first", file=sys.stderr)
            return 2
        base = args.base or default_base(root, args.remote)
        if args.branch in {base, goal_branch}:
            print("error: --branch must differ from the base and goal branches", file=sys.stderr)
            return 2
        where = branch_exists(root, args.branch, args.remote)
        if where:
            print(f"error: branch {args.branch} already exists {where}", file=sys.stderr)
            return 2

        drop = [p for p in SCAFFOLD_FILES if p not in args.include] + args.exclude
        tracked = [p for p in drop if git("ls-files", "--", p, cwd=root)]
        issue = tracking_issue(root)
        scaffold_subject = "chore(goal): remove goal scaffold from result branch"
        if issue:
            scaffold_subject += f" (#{issue})"

        tmp = Path(tempfile.mkdtemp(prefix="goal-pr-"))
        work = tmp / "result"
        git("worktree", "add", "-b", args.branch, str(work), goal_branch, cwd=root)
        try:
            if tracked:
                git("rm", "-q", "-r", "--", *tracked, cwd=work)
                git("commit", "-q", "-m", scaffold_subject, cwd=work)
            fetch = subprocess.run(["git", "fetch", "-q", args.remote, base], cwd=work,
                                   capture_output=True, text=True, check=False)
            if fetch.returncode == 0:
                base_ref = f"{args.remote}/{base}"
                changed = git("diff", "--name-only", f"{base_ref}...{args.branch}", cwd=work)
                for line in unlinked_commits(work, base_ref, args.branch, scaffold_subject):
                    print(f"warning: commit without an issue number (#N): {line}", file=sys.stderr)
            else:
                changed = "(could not fetch base; diff against base unknown)"
            print(f"result branch {args.branch} from {goal_branch}, base {base}")
            print("dropped: " + (", ".join(tracked) or "(none tracked)"))
            print("files vs base:\n" + (changed or "(none)"))
            if args.dry_run:
                print("dry run: branch built, nothing pushed")
                return 0
            git("push", "-q", "-u", args.remote, args.branch, cwd=work)
            print(f"pushed {args.remote}/{args.branch}")
            if args.no_pr:
                return 0
            cmd = ["gh", "pr", "create", "--base", base, "--head", args.branch,
                   "--title", args.title, "--body-file", args.body_file]
            if args.draft:
                cmd.append("--draft")
            created = subprocess.run(cmd, cwd=work, capture_output=True, text=True, check=False)
            if created.returncode != 0:
                print(f"error: gh pr create failed: {(created.stderr or created.stdout).strip()}",
                      file=sys.stderr)
                return 1
            print(created.stdout.strip())
            return 0
        finally:
            git("worktree", "remove", "--force", str(work), cwd=root, check=False)
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
