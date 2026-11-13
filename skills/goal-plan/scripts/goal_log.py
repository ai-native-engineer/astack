#!/usr/bin/env python3
"""CRUD helper for a goal-plan progress.tsv so rows are never hand-edited.

Every change goes through this tool: it auto-fills id/checkpoint, escapes
tabs/newlines, and validates the status/decision enums. Run `<cmd> --help`
for flags, `condition` for readiness or a Codex-compatible /goal line.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

CONDITION_LIMIT = 4000  # Claude Code caps a /goal condition at 4,000 characters

COLUMNS = ["id", "status", "decision", "task", "done_when",
           "checkpoint", "artifact", "next", "notes", "worker", "branch",
           "worktree", "depends_on"]
STATUSES = {"todo", "doing", "deferred", "blocked", "done", "dropped"}
DECISIONS = {"n/a", "keep", "discard", "crash"}
OPEN_STATUSES = {"todo", "doing", "deferred", "blocked"}
DONE_DECISIONS = {"keep", "discard", "crash"}
DROP_DECISIONS = {"discard", "crash"}
EDITABLE = [c for c in COLUMNS if c != "id"]


def _clean(value: str) -> str:
    return (value or "").replace("\t", " ").replace("\r", " ").replace("\n", " ").strip()


def _git_short_hash() -> str:
    """Current commit hash, or '-' when not in a git repo (read-only)."""
    try:
        out = subprocess.run(["git", "rev-parse", "--short", "HEAD"],
                             capture_output=True, text=True, check=True)
        return out.stdout.strip() or "-"
    except (subprocess.CalledProcessError, FileNotFoundError):
        return "-"


def read_rows(path: Path):
    if not path.exists():
        return list(COLUMNS), []
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines:
        return list(COLUMNS), []
    header = lines[0].split("\t")
    rows = []
    for ln in lines[1:]:
        if not ln.strip():
            continue
        cells = ln.split("\t")
        cells += [""] * (len(header) - len(cells))  # tolerate short rows
        rows.append(dict(zip(header, cells)))
    return header, rows


def write_rows(path: Path, header, rows):
    header = list(header)
    for column in COLUMNS:
        if column not in header:
            header.append(column)
    out = ["\t".join(header)]
    out += ["\t".join(_clean(r.get(c, "")) for c in header) for r in rows]
    path.write_text("\n".join(out) + "\n", encoding="utf-8")


def next_id(rows):
    mx = 0
    for r in rows:
        try:
            mx = max(mx, int(r.get("id", "0")))
        except ValueError:
            pass
    return str(mx + 1)


def find_row(rows, rid):
    return next((r for r in rows if r.get("id") == str(rid)), None)


def _has_evidence(*values: str) -> bool:
    return any(_clean(v) not in {"", "-"} for v in values)


def _validate_row(row) -> int:
    status = row.get("status", "")
    decision = row.get("decision", "")
    if status in OPEN_STATUSES and decision != "n/a":
        print("error: open rows need decision n/a", file=sys.stderr)
        return 2
    if status == "done":
        if decision not in DONE_DECISIONS:
            print(f"error: done decision must be one of {sorted(DONE_DECISIONS)}", file=sys.stderr)
            return 2
        if not _has_evidence(row.get("artifact", ""), row.get("notes", "")):
            print("error: done rows need proof in artifact or notes", file=sys.stderr)
            return 2
    if status == "dropped" and decision not in DROP_DECISIONS:
        print(f"error: dropped decision must be one of {sorted(DROP_DECISIONS)}", file=sys.stderr)
        return 2
    if status == "dropped" and not _has_evidence(row.get("notes", "")):
        print("error: dropped rows need a reason in notes", file=sys.stderr)
        return 2
    return 0


def _update(args, **fields):
    path = Path(args.file)
    header, rows = read_rows(path)
    r = find_row(rows, args.id)
    if r is None:
        ids = ", ".join(x.get("id", "") for x in rows) or "(none)"
        print(f"error: no row id={args.id}. existing ids: {ids}", file=sys.stderr)
        return 2
    for k, v in fields.items():
        if v is not None:
            r[k] = _clean(v)
    invalid = _validate_row(r)
    if invalid:
        return invalid
    write_rows(path, header, rows)
    return 0


def cmd_add(args):
    path = Path(args.file)
    header, rows = read_rows(path)
    rid = next_id(rows)
    task = _clean(args.task)
    issue = getattr(args, "issue", None)
    if issue:
        number = str(issue).strip().lstrip("#")
        if not number.isdigit():
            print(f"error: --issue must be an issue number, got {issue!r}", file=sys.stderr)
            return 2
        task = f"#{number} {task}"
    rows.append({"id": rid, "status": "todo", "decision": "n/a",
                 "task": task, "done_when": _clean(args.done_when),
                 "checkpoint": "-", "artifact": "-",
                 "next": _clean(args.next), "notes": _clean(args.notes),
                 "worker": "-", "branch": "-", "worktree": "-",
                 "depends_on": _clean(getattr(args, "depends_on", "")) or "-"})
    write_rows(path, header, rows)
    print(rid)
    return 0


def cmd_start(args):
    return _update(args, status="doing")


def cmd_done(args):
    dec = args.decision or "keep"
    if dec not in DONE_DECISIONS:
        print(f"error: decision must be one of {sorted(DONE_DECISIONS)}", file=sys.stderr)
        return 2
    if not _has_evidence(args.artifact, args.notes):
        print("error: done rows need proof in --artifact or --notes", file=sys.stderr)
        return 2
    return _update(args, status="done", decision=dec,
                   checkpoint=_git_short_hash(), artifact=args.artifact, notes=args.notes)


def cmd_block(args):
    return _update(args, status="blocked", notes=args.notes)


def cmd_defer(args):
    if not _has_evidence(args.reason):
        print("error: deferred rows need a reason in --reason", file=sys.stderr)
        return 2
    return _update(args, status="deferred", notes=args.reason, next=args.resume_when)


def cmd_resume(args):
    return _update(args, status="todo", decision="n/a", next=args.next)


def cmd_assign(args):
    fields = {"worker": args.worker, "branch": args.branch,
              "worktree": args.worktree, "depends_on": args.depends_on}
    return _update(args, **fields)


def cmd_drop(args):
    dec = args.decision or "discard"
    if dec not in DROP_DECISIONS:
        print(f"error: decision must be one of {sorted(DROP_DECISIONS)}", file=sys.stderr)
        return 2
    if not _has_evidence(args.notes):
        print("error: dropped rows need a reason in --notes", file=sys.stderr)
        return 2
    return _update(args, status="dropped", decision=dec, notes=args.notes)


def cmd_set(args):
    if args.col not in EDITABLE:
        print(f"error: col must be one of {EDITABLE}", file=sys.stderr)
        return 2
    if args.col == "status" and args.value not in STATUSES:
        print(f"error: status must be one of {sorted(STATUSES)}", file=sys.stderr)
        return 2
    if args.col == "status" and args.value in {"done", "dropped"}:
        cmd = "done" if args.value == "done" else "drop"
        print(f"error: use `{cmd}` instead of setting status={args.value}", file=sys.stderr)
        return 2
    if args.col == "decision" and args.value not in DECISIONS:
        print(f"error: decision must be one of {sorted(DECISIONS)}", file=sys.stderr)
        return 2
    return _update(args, **{args.col: args.value})


def cmd_show(args):
    header, rows = read_rows(Path(args.file))
    if args.status:
        rows = [r for r in rows if r.get("status") == args.status]
    limit = 10 ** 9 if args.full else 40

    def cell(r, c):
        v = r.get(c, "")
        return v if len(v) <= limit else v[:limit - 3] + "..."

    widths = {c: len(c) for c in header}
    for r in rows:
        for c in header:
            widths[c] = max(widths[c], len(cell(r, c)))
    print("  ".join(c.ljust(widths[c]) for c in header))
    for r in rows:
        print("  ".join(cell(r, c).ljust(widths[c]) for c in header))
    return 0


def _section(text: str, name: str) -> str:
    match = re.search(rf"^## {re.escape(name)}\s*\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    return match.group(1).strip() if match else ""


def readiness_problems(text: str) -> list[str]:
    """What still blocks the unattended loop from starting on this GOAL.md.

    Only emptiness is checked, never content: a `TBD` left anywhere, a Decisions
    section with no recorded answer, or an acceptance criterion without its own
    Proof. "none", "n/a", and "Covered by Proof." are complete answers.
    """
    problems: list[str] = []
    section = "(top)"
    for number, line in enumerate(text.splitlines(), 1):
        if line.startswith("## "):
            section = line[3:].strip()
        if re.search(r"\bTBD\b", line):
            problems.append(f"line {number} in ## {section} still says TBD")
    decisions = [ln for ln in _section(text, "Decisions").splitlines() if ln.startswith("- ")]
    if not decisions or all(ln.startswith("- <") for ln in decisions):
        problems.append("## Decisions has no recorded interview answer")
    criteria = _section(text, "Acceptance Criteria")
    items = [ln for ln in criteria.splitlines() if re.match(r"- AC-\d+", ln)]
    if not items and "Covered by Proof" not in criteria:
        problems.append("## Acceptance Criteria needs AC-n items or the words 'Covered by Proof.'")
    for ln in items:
        if "Proof:" not in ln:
            problems.append(f"{ln.split(':', 1)[0]} has no 'Proof:'")
    return problems


def cmd_condition(args):
    """Validate a filled GOAL.md and print a Codex-compatible /goal line.

    Claude Code uses `/goal @GOAL.md` so the fresh loop reads the saved
    contract directly. This command remains useful as a readiness check and
    for runtimes that require the goal and proof in the condition text.
    """
    path = Path(args.goal_file)
    if not path.is_file():
        print(f"error: no goal file at {path}", file=sys.stderr)
        return 2
    text = path.read_text(encoding="utf-8")
    goal = " ".join(_section(text, "Goal").split())
    proof = _section(text, "Proof")
    if not goal or goal.startswith("TBD") or not proof or proof.startswith("TBD"):
        print("error: fill ## Goal and ## Proof before asking for the condition", file=sys.stderr)
        return 2
    problems = readiness_problems(text)
    if problems:
        print(f"error: {path.name} is not ready for an unattended loop:", file=sys.stderr)
        for problem in problems:
            print(f"  - {problem}", file=sys.stderr)
        print("finish the interview, replace every TBD with an answer (\"none\" counts), then retry",
              file=sys.stderr)
        return 2
    commands = [ln.strip() for ln in proof.splitlines() if ln.startswith("    ") and ln.strip()]
    if commands:
        proof_part = "Proof: run `" + " && ".join(commands) + "` and show its output."
    else:
        proof_part = f"Proof: the check in {path.name} Proof, with its output shown in the reply."
    bounds = " ".join(_section(text, "Bounds").split())
    no_bound = not bounds or bounds.startswith("TBD") or bounds.lower().rstrip(".") in {"none", "n/a", "-"}
    bounds_part = "" if no_bound else f" Bounds: {bounds}"
    condition = (f"{goal.rstrip('.')}. {proof_part} Follow {path.name} end to end "
                 f"(Loop Protocol, Environment, Verification Layers, GitHub Flow) and finish with "
                 f"the result PR URL.{bounds_part}")
    if len(condition) > CONDITION_LIMIT:
        print(f"error: condition is {len(condition)} characters; shorten ## Goal or ## Bounds "
              f"below {CONDITION_LIMIT}", file=sys.stderr)
        return 2
    print(f"/goal {condition}")
    return 0


def main(argv=None):
    parent = argparse.ArgumentParser(add_help=False)
    parent.add_argument("--file", default="progress.tsv", help="progress TSV path")

    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("add", parents=[parent], help="append a new todo row")
    a.add_argument("--task", required=True)
    a.add_argument("--issue", default=None, metavar="N",
                   help="existing GitHub issue this row resolves; prefixes the task with #N")
    a.add_argument("--done-when", dest="done_when", default="")
    a.add_argument("--next", default="")
    a.add_argument("--notes", default="")
    a.add_argument("--depends-on", default="", help="comma-separated row ids that must be done")
    a.set_defaults(func=cmd_add)

    s = sub.add_parser("start", parents=[parent], help="mark row doing")
    s.add_argument("id")
    s.set_defaults(func=cmd_start)

    dn = sub.add_parser("done", parents=[parent], help="close row with proof")
    dn.add_argument("id")
    dn.add_argument("--decision", default=None, help="keep|discard|crash (default keep)")
    dn.add_argument("--artifact", default=None, help="proof text or log path; required unless --notes contains proof")
    dn.add_argument("--notes", default=None)
    dn.set_defaults(func=cmd_done)

    b = sub.add_parser("block", parents=[parent], help="mark row blocked by a technical dependency")
    b.add_argument("id")
    b.add_argument("--notes", default=None)
    b.set_defaults(func=cmd_block)

    df = sub.add_parser("defer", parents=[parent], help="record an approval or external-condition hold")
    df.add_argument("id")
    df.add_argument("--reason", required=True)
    df.add_argument("--resume-when", default="", help="condition or next action for resuming")
    df.set_defaults(func=cmd_defer)

    rs = sub.add_parser("resume", parents=[parent], help="return a deferred row to the todo queue")
    rs.add_argument("id")
    rs.add_argument("--next", default=None)
    rs.set_defaults(func=cmd_resume)

    aa = sub.add_parser("assign", parents=[parent], help="record the worker allocation for a row")
    aa.add_argument("id")
    aa.add_argument("--worker", required=True)
    aa.add_argument("--branch", required=True)
    aa.add_argument("--worktree", required=True)
    aa.add_argument("--depends-on", default="-", help="comma-separated row ids")
    aa.set_defaults(func=cmd_assign)

    dr = sub.add_parser("drop", parents=[parent], help="mark row dropped")
    dr.add_argument("id")
    dr.add_argument("--decision", default=None, help="discard|crash (default discard)")
    dr.add_argument("--notes", default=None, help="reason for dropping; required")
    dr.set_defaults(func=cmd_drop)

    st = sub.add_parser("set", parents=[parent], help="set any field on a row")
    st.add_argument("id")
    st.add_argument("--col", required=True)
    st.add_argument("--value", required=True)
    st.set_defaults(func=cmd_set)

    sh = sub.add_parser("show", parents=[parent], help="print the table")
    sh.add_argument("--status", default=None)
    sh.add_argument("--full", action="store_true")
    sh.set_defaults(func=cmd_show)

    cd = sub.add_parser("condition", help="print the /goal line from GOAL.md")
    cd.add_argument("--goal-file", default="GOAL.md", help="goal file path")
    cd.set_defaults(func=cmd_condition)

    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
