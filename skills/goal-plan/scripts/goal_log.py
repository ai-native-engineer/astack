#!/usr/bin/env python3
"""CRUD helper for a goal-plan progress.tsv so rows are never hand-edited.

Every change goes through this tool: it auto-fills id/checkpoint, escapes
tabs/newlines, and validates the status/decision enums. Run `<cmd> --help`
for flags, or `selftest` to verify the tool itself.
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
from pathlib import Path

COLUMNS = ["id", "status", "decision", "task", "done_when",
           "checkpoint", "artifact", "next", "notes"]
STATUSES = {"todo", "doing", "done", "blocked", "dropped"}
DECISIONS = {"n/a", "keep", "discard", "crash"}
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
    write_rows(path, header, rows)
    return 0


def cmd_add(args):
    path = Path(args.file)
    header, rows = read_rows(path)
    rid = next_id(rows)
    rows.append({"id": rid, "status": "todo", "decision": "n/a",
                 "task": _clean(args.task), "done_when": _clean(args.done_when),
                 "checkpoint": "-", "artifact": "-",
                 "next": _clean(args.next), "notes": _clean(args.notes)})
    write_rows(path, header, rows)
    print(rid)
    return 0


def cmd_start(args):
    return _update(args, status="doing")


def cmd_done(args):
    dec = args.decision or "keep"
    if dec not in DECISIONS:
        print(f"error: decision must be one of {sorted(DECISIONS)}", file=sys.stderr)
        return 2
    if not _clean(args.artifact) and not _clean(args.notes):
        print("error: done rows need proof in --artifact or --notes", file=sys.stderr)
        return 2
    return _update(args, status="done", decision=dec,
                   checkpoint=_git_short_hash(), artifact=args.artifact, notes=args.notes)


def cmd_block(args):
    return _update(args, status="blocked", notes=args.notes)


def cmd_drop(args):
    dec = args.decision or "discard"
    if dec not in DECISIONS:
        print(f"error: decision must be one of {sorted(DECISIONS)}", file=sys.stderr)
        return 2
    return _update(args, status="dropped", decision=dec, notes=args.notes)


def cmd_set(args):
    if args.col not in EDITABLE:
        print(f"error: col must be one of {EDITABLE}", file=sys.stderr)
        return 2
    if args.col == "status" and args.value not in STATUSES:
        print(f"error: status must be one of {sorted(STATUSES)}", file=sys.stderr)
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


def cmd_selftest(args):
    from argparse import Namespace
    with tempfile.TemporaryDirectory() as d:
        f = str(Path(d) / "progress.tsv")
        assert cmd_add(Namespace(file=f, task="first\twith tab",
                                 done_when="x", next="n", notes="")) == 0
        assert cmd_add(Namespace(file=f, task="second",
                                 done_when="", next="", notes="")) == 0
        _, rows = read_rows(Path(f))
        assert [r["id"] for r in rows] == ["1", "2"], rows
        assert "\t" not in rows[0]["task"] and "with tab" in rows[0]["task"]
        assert cmd_start(Namespace(file=f, id="1")) == 0
        _, rows = read_rows(Path(f))
        assert find_row(rows, "1")["status"] == "doing"
        assert cmd_done(Namespace(file=f, id="1", decision="keep",
                                  artifact="proof", notes=None)) == 0
        _, rows = read_rows(Path(f))
        r = find_row(rows, "1")
        assert r["status"] == "done" and r["decision"] == "keep" and r["artifact"] == "proof"
        assert cmd_done(Namespace(file=f, id="99", decision="keep",
                                  artifact="proof", notes=None)) == 2  # unknown id
        assert cmd_done(Namespace(file=f, id="2", decision="bogus",
                                  artifact="proof", notes=None)) == 2   # bad enum
        assert cmd_done(Namespace(file=f, id="2", decision="keep",
                                  artifact=None, notes=None)) == 2      # missing proof
        assert cmd_set(Namespace(file=f, id="2", col="status", value="blocked")) == 0
        _, rows = read_rows(Path(f))
        assert find_row(rows, "2")["status"] == "blocked"
        assert cmd_set(Namespace(file=f, id="2", col="status", value="nope")) == 2
    print("selftest OK")
    return 0


def main(argv=None):
    parent = argparse.ArgumentParser(add_help=False)
    parent.add_argument("--file", default="progress.tsv", help="progress TSV path")

    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("add", parents=[parent], help="append a new todo row")
    a.add_argument("--task", required=True)
    a.add_argument("--done-when", dest="done_when", default="")
    a.add_argument("--next", default="")
    a.add_argument("--notes", default="")
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

    b = sub.add_parser("block", parents=[parent], help="mark row blocked")
    b.add_argument("id")
    b.add_argument("--notes", default=None)
    b.set_defaults(func=cmd_block)

    dr = sub.add_parser("drop", parents=[parent], help="mark row dropped")
    dr.add_argument("id")
    dr.add_argument("--decision", default=None, help="discard|crash (default discard)")
    dr.add_argument("--notes", default=None)
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

    sub.add_parser("selftest", parents=[parent],
                   help="run internal checks").set_defaults(func=cmd_selftest)

    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
