#!/usr/bin/env python3
"""Runnable checks for goal_issue.py against a recorded `gh` stand-in (no network)."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parent.parent
GOAL_ISSUE = SKILL_ROOT / "scripts" / "goal_issue.py"

# A `gh` that logs every call and answers the few queries goal_issue.py makes.
FAKE_GH = r'''#!/bin/sh
printf '%s\n' "$*" >> "$GH_LOG"
case "$*" in
  "repo view --json nameWithOwner --jq .nameWithOwner") echo "octo/demo" ;;
  "issue create --title "*) echo "https://github.com/octo/demo/issues/12" ;;
  "api repos/octo/demo/issues/12 --jq .id") echo "900012" ;;
  "api repos/octo/demo/issues/5 --jq .id") echo "900005" ;;
  "api -X POST repos/octo/demo/issues/7/sub_issues -F sub_issue_id="*) echo '{"number": 7}' ;;
  "api repos/octo/demo/issues/7/sub_issues --paginate")
    echo '[{"number": 12, "state": "open", "title": "build e2e lane"}, {"number": 5, "state": "closed", "title": "old"}]' ;;
  "issue close "*) ;;
  *) echo "unexpected gh call: $*" >&2; exit 9 ;;
esac
'''


class GoalIssueTests(unittest.TestCase):
    def run_tool(self, tmp: Path, *args: str) -> tuple[subprocess.CompletedProcess[str], list[str]]:
        bin_dir = tmp / "bin"
        bin_dir.mkdir(exist_ok=True)
        fake = bin_dir / "gh"
        fake.write_text(FAKE_GH, encoding="utf-8")
        fake.chmod(0o755)
        log = tmp / "gh.log"
        log.write_text("", encoding="utf-8")
        env = {**os.environ, "PATH": f"{bin_dir}:{os.environ.get('PATH', '')}", "GH_LOG": str(log)}
        result = subprocess.run([sys.executable, str(GOAL_ISSUE), *args],
                                capture_output=True, text=True, env=env, cwd=tmp)
        return result, log.read_text(encoding="utf-8").splitlines()

    def test_open_creates_issue_and_attaches_it_by_id(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result, calls = self.run_tool(Path(tmp), "open", "--parent", "#7", "--title", "build e2e lane")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout.strip(), "12")
            self.assertIn("issue create --title build e2e lane --body Step of #7. --repo octo/demo", calls)
            self.assertIn("api -X POST repos/octo/demo/issues/7/sub_issues -F sub_issue_id=900012", calls)

    def test_open_attaches_existing_issue_without_creating(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result, calls = self.run_tool(Path(tmp), "--repo", "octo/demo", "open", "--parent", "7", "--existing", "#5")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout.strip(), "5")
            self.assertFalse(any(call.startswith("issue create") for call in calls))
            self.assertFalse(any(call.startswith("repo view") for call in calls))
            self.assertIn("api -X POST repos/octo/demo/issues/7/sub_issues -F sub_issue_id=900005", calls)

    def test_close_maps_reason_and_passes_comment(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result, calls = self.run_tool(Path(tmp), "close", "#12", "--reason", "not-planned",
                                          "--comment", "discard: slower than baseline")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("issue close 12 --reason not planned --comment discard: slower than baseline --repo octo/demo",
                          calls)

    def test_list_prints_number_state_title(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result, _ = self.run_tool(Path(tmp), "list", "--parent", "7")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout.splitlines(), ["#12\topen\tbuild e2e lane", "#5\tclosed\told"])

    def test_rejects_bad_parent_and_missing_title(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            bad_parent, calls = self.run_tool(Path(tmp), "open", "--parent", "soon", "--title", "x")
            self.assertEqual(bad_parent.returncode, 2)
            self.assertIn("--parent must be an issue number", bad_parent.stderr)
            self.assertEqual(calls, [])
            no_title, calls = self.run_tool(Path(tmp), "open", "--parent", "7")
            self.assertEqual(no_title.returncode, 2)
            self.assertIn("--title is required", no_title.stderr)
            self.assertEqual(calls, [])


if __name__ == "__main__":
    unittest.main()
