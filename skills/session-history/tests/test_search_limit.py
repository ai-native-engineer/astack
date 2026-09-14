"""Bounded search keeps full-search ordering without reading discarded sessions."""

import json
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import session_history as history


class TestSearchLimit(unittest.TestCase):
    def test_limit_preserves_results_and_bounds_adapter_reads(self):
        # Unsorted input, equal timestamps across adapters, and nonmatching records.
        sessions = {
            "late": {"tool": "codex", "first_ts_ms": 30, "project": "p"},
            "tie-first": {"tool": "grok", "first_ts_ms": 20, "project": "p"},
            "no-hit": {"tool": "claude", "first_ts_ms": 1, "project": "p"},
            "missing": {"tool": "claude", "first_ts_ms": 2, "project": "p"},
            "unreadable": {"tool": "claude", "first_ts_ms": 3, "project": "p"},
            "tie-second": {"tool": "claude", "first_ts_ms": 20, "project": "p"},
            "early": {"tool": "codex", "project": "p"},
        }
        ordered_hits = ["early", "tie-first", "tie-second", "late"]

        def grep(path, keyword, session_id):
            if session_id == "unreadable":
                raise OSError("fixture unreadable")
            if session_id == "no-hit":
                return []
            return [{"role": "tool", "ts": "", "excerpt": session_id}] * 2

        for limit, reads in [(None, 6), (0, 0), (1, 1), (2, 4), (10, 6), (-1, 6)]:
            with self.subTest(limit=limit):
                search = Mock(side_effect=grep)
                adapters = {
                    tool: SimpleNamespace(grep_session=search)
                    for tool in ("claude", "codex", "grok")
                }
                args = SimpleNamespace(keyword="needle", tool="all", format="json", limit=limit)
                with (
                    patch.object(history, "date_range", return_value=(0, 100, "fixture")),
                    patch.object(history, "collect_history", return_value=sessions),
                    patch.object(history, "ADAPTERS", adapters),
                    patch.object(history, "adapter_session_path", side_effect=lambda adapter, sid: None if sid == "missing" else Path(__file__)),
                    patch.object(history, "emit") as emit,
                ):
                    history.cmd_grep(args)
                result = json.loads(emit.call_args.args[0])
                self.assertEqual([row["sid"] for row in result], ordered_hits[:limit])
                self.assertTrue(all(len(row["hits"]) == 2 for row in result))
                self.assertEqual(search.call_count, reads)


if __name__ == "__main__":
    unittest.main()
