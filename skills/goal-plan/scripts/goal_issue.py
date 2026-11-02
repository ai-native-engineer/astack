#!/usr/bin/env python3
"""Sub-issues for a goal's tracking issue, through `gh`.

Each progress row that deserves its own page gets a sub-issue under the goal's
tracking issue, so the parent issue shows the steps and their state, commits
with `#N` land on the step's timeline, and the PR links back to every step.
Run from the target checkout; pass `--repo owner/name` on a fork.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys


def gh(*args: str, repo: str | None = None, check: bool = True) -> subprocess.CompletedProcess[str]:
    cmd = ["gh", *args]
    if repo:
        cmd += ["--repo", repo] if args[0] != "api" else []
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if check and result.returncode != 0:
        detail = (result.stderr or result.stdout).strip() or f"exit {result.returncode}"
        raise RuntimeError(f"gh {' '.join(args)}: {detail}")
    return result


def repo_name(repo: str | None) -> str:
    if repo:
        return repo
    out = gh("repo", "view", "--json", "nameWithOwner", "--jq", ".nameWithOwner").stdout.strip()
    if not out:
        raise RuntimeError("could not determine the repository; pass --repo owner/name")
    return out


def issue_id(repo: str, number: str) -> int:
    """GitHub's database id for an issue number; the sub-issue API wants the id."""
    out = gh("api", f"repos/{repo}/issues/{number}", "--jq", ".id").stdout.strip()
    if not out.isdigit():
        raise RuntimeError(f"issue #{number} has no numeric id in {repo}")
    return int(out)


def number_from_url(url: str) -> str:
    match = re.search(r"/issues/(\d+)\s*$", url.strip())
    if not match:
        raise RuntimeError(f"gh issue create returned no issue URL: {url!r}")
    return match.group(1)


def attach(repo: str, parent: str, child: str) -> None:
    gh("api", "-X", "POST", f"repos/{repo}/issues/{parent}/sub_issues",
       "-F", f"sub_issue_id={issue_id(repo, child)}")


def cmd_open(args) -> int:
    repo = repo_name(args.repo)
    if args.existing:
        number = args.existing.lstrip("#")
    else:
        body = args.body or f"Step of #{args.parent}."
        created = gh("issue", "create", "--title", args.title, "--body", body,
                     *(["--label", args.label] if args.label else []), repo=repo)
        number = number_from_url(created.stdout)
    attach(repo, args.parent, number)
    print(number)
    return 0


def cmd_close(args) -> int:
    repo = repo_name(args.repo)
    reason = "completed" if args.reason == "completed" else "not planned"
    gh("issue", "close", args.number.lstrip("#"), "--reason", reason,
       *(["--comment", args.comment] if args.comment else []), repo=repo)
    return 0


def cmd_list(args) -> int:
    repo = repo_name(args.repo)
    out = gh("api", f"repos/{repo}/issues/{args.parent}/sub_issues", "--paginate").stdout
    items = json.loads(out or "[]")
    if isinstance(items, dict):
        items = [items]
    for item in items:
        print(f"#{item.get('number')}\t{item.get('state')}\t{item.get('title')}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=None, help="owner/name; required on a fork, else detected")
    sub = parser.add_subparsers(dest="cmd", required=True)

    op = sub.add_parser("open", help="create a sub-issue under the tracking issue and print its number")
    op.add_argument("--parent", required=True, help="tracking issue number")
    op.add_argument("--title", default=None, help="sub-issue title, usually the row task")
    op.add_argument("--body", default=None, help="sub-issue body (default: 'Step of #parent.')")
    op.add_argument("--label", default=None)
    op.add_argument("--existing", default=None, metavar="N",
                    help="attach an existing issue as the sub-issue instead of creating one")
    op.set_defaults(func=cmd_open)

    cl = sub.add_parser("close", help="close a sub-issue with the row's outcome")
    cl.add_argument("number")
    cl.add_argument("--reason", choices=["completed", "not-planned"], default="completed",
                    help="completed for keep, not-planned for discard, crash, or drop")
    cl.add_argument("--comment", default=None, help="artifact or drop reason, pasted as the closing comment")
    cl.set_defaults(func=cmd_close)

    ls = sub.add_parser("list", help="print the sub-issues of the tracking issue")
    ls.add_argument("--parent", required=True)
    ls.set_defaults(func=cmd_list)

    args = parser.parse_args(argv)
    if args.cmd == "open":
        args.parent = args.parent.lstrip("#")
        if not args.parent.isdigit():
            print("error: --parent must be an issue number", file=sys.stderr)
            return 2
        if not args.existing and not args.title:
            print("error: --title is required unless --existing is given", file=sys.stderr)
            return 2
    try:
        return args.func(args)
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
