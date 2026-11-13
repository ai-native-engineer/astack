#!/usr/bin/env python3
"""Runnable checks for the goal_log.py ledger commands (converted from the old `selftest` subcommand)."""

from __future__ import annotations

import io
import sys
import tempfile
import unittest
from argparse import Namespace
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import goal_log  # noqa: E402


class LedgerCommandTests(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.file = str(Path(self._tmp.name) / "progress.tsv")

    def expect(self, code: int, func, **ns) -> None:
        stdout, stderr = io.StringIO(), io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            rc = func(Namespace(file=self.file, **ns))
        self.assertEqual(rc, code, (func.__name__, ns, stdout.getvalue(), stderr.getvalue()))

    def rows(self) -> list[dict[str, str]]:
        return goal_log.read_rows(Path(self.file))[1]

    def row(self, row_id: str) -> dict[str, str]:
        found = goal_log.find_row(self.rows(), row_id)
        self.assertIsNotNone(found)
        return found

    def test_add_start_done_and_the_done_enum_checks(self) -> None:
        self.expect(0, goal_log.cmd_add, task="first\twith tab", done_when="x", next="n", notes="")
        self.expect(0, goal_log.cmd_add, task="second", issue="#7", done_when="", next="", notes="")
        self.expect(2, goal_log.cmd_add, task="third", issue="soon", done_when="", next="", notes="")
        self.assertEqual([r["id"] for r in self.rows()], ["1", "2"])
        self.assertEqual(self.row("2")["task"], "#7 second")
        self.assertNotIn("\t", self.row("1")["task"])
        self.assertIn("with tab", self.row("1")["task"])
        self.expect(0, goal_log.cmd_start, id="1")
        self.assertEqual(self.row("1")["status"], "doing")
        self.expect(0, goal_log.cmd_done, id="1", decision="keep", artifact="proof", notes=None)
        done = self.row("1")
        self.assertEqual((done["status"], done["decision"], done["artifact"]), ("done", "keep", "proof"))
        self.expect(2, goal_log.cmd_done, id="99", decision="keep", artifact="proof", notes=None)  # unknown id
        self.expect(2, goal_log.cmd_done, id="2", decision="bogus", artifact="proof", notes=None)  # bad enum
        self.expect(2, goal_log.cmd_done, id="2", decision="n/a", artifact="proof", notes=None)  # open-only
        self.expect(2, goal_log.cmd_done, id="2", decision="keep", artifact=None, notes=None)  # no proof
        self.expect(2, goal_log.cmd_done, id="2", decision="keep", artifact="-", notes=None)  # placeholder

    def test_drop_and_set_refusals(self) -> None:
        self.expect(0, goal_log.cmd_add, task="first", done_when="", next="", notes="")
        self.expect(0, goal_log.cmd_add, task="second", done_when="", next="", notes="")
        self.expect(0, goal_log.cmd_done, id="1", decision="keep", artifact="proof", notes=None)
        self.expect(2, goal_log.cmd_drop, id="2", decision="n/a", notes=None)  # open-only decision
        self.expect(2, goal_log.cmd_drop, id="2", decision="keep", notes=None)  # done-only decision
        self.expect(2, goal_log.cmd_drop, id="2", decision="discard", notes=None)  # missing reason
        self.expect(2, goal_log.cmd_set, id="2", col="status", value="done")
        self.expect(2, goal_log.cmd_set, id="2", col="decision", value="keep")
        self.expect(2, goal_log.cmd_set, id="1", col="artifact", value="-")
        self.expect(2, goal_log.cmd_set, id="1", col="decision", value="n/a")
        self.expect(2, goal_log.cmd_set, id="1", col="status", value="blocked")
        self.expect(2, goal_log.cmd_block, id="1", notes="reopen")
        self.expect(2, goal_log.cmd_set, id="2", col="status", value="nope")

    def test_assign_defer_resume_drop(self) -> None:
        self.expect(0, goal_log.cmd_add, task="second", issue="#7", done_when="", next="", notes="")
        self.expect(0, goal_log.cmd_assign, id="1", worker="w1", branch="feat/7-second",
                    worktree="/tmp/w1", depends_on="-")
        self.assertEqual(self.row("1")["worker"], "w1")
        self.expect(0, goal_log.cmd_defer, id="1", reason="awaiting approval", resume_when="user approves")
        self.assertEqual(self.row("1")["status"], "deferred")
        self.expect(0, goal_log.cmd_resume, id="1", next="retry")
        self.assertEqual(self.row("1")["status"], "todo")
        self.expect(0, goal_log.cmd_drop, id="1", decision="discard", notes="not needed")
        self.assertEqual(self.row("1")["status"], "dropped")


if __name__ == "__main__":
    unittest.main()
