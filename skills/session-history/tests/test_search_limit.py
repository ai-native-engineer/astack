"""Bounded search keeps full-search ordering without reading discarded sessions."""

import json
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import session_history as history


def grep_args(**overrides):
    values = {
        "keywords": ["needle"],
        "regex": False,
        "include_self": False,
        "sort": "recent",
        "tool": "all",
        "format": "json",
        "limit": None,
    }
    values.update(overrides)
    return SimpleNamespace(**values)


# Unsorted input, equal timestamps across adapters, and nonmatching records.
SESSIONS = {
    "late": {"tool": "codex", "first_ts_ms": 30, "project": "p"},
    "tie-first": {"tool": "grok", "first_ts_ms": 20, "project": "p"},
    "no-hit": {"tool": "claude", "first_ts_ms": 1, "project": "p"},
    "missing": {"tool": "claude", "first_ts_ms": 2, "project": "p"},
    "unreadable": {"tool": "claude", "first_ts_ms": 3, "project": "p"},
    "tie-second": {"tool": "claude", "first_ts_ms": 20, "project": "p"},
    "early": {"tool": "codex", "project": "p"},
}


class TestSearchLimit(unittest.TestCase):
    def _run(self, args, hit_counts=None, current=frozenset(), hits_by_sid=None):
        hit_counts = hit_counts or {}
        hits_by_sid = hits_by_sid or {}

        def grep(path, matcher, session_id):
            if session_id == "unreadable":
                raise OSError("fixture unreadable")
            if session_id == "no-hit":
                return []
            if session_id in hits_by_sid:
                return hits_by_sid[session_id]
            count = hit_counts.get(session_id, 2)
            return [{"role": "tool", "ts": "", "excerpt": session_id}] * count

        search = Mock(side_effect=grep)
        adapters = {
            tool: SimpleNamespace(grep_session=search)
            for tool in ("claude", "codex", "grok")
        }
        with (
            patch.object(history, "current_session_ids", return_value=set(current)),
            patch.object(history, "date_range", return_value=(0, 100, "fixture")),
            patch.object(history, "collect_history", return_value=dict(SESSIONS)),
            patch.object(history, "ADAPTERS", adapters),
            patch.object(
                history,
                "adapter_session_path",
                side_effect=lambda adapter, sid: (
                    None if sid == "missing" else Path(__file__)
                ),
            ),
            patch.object(history, "emit") as emit,
        ):
            history.cmd_grep(args)
        return json.loads(emit.call_args.args[0]), search

    def test_recent_limit_keeps_newest_and_bounds_adapter_reads(self):
        ordered_hits = ["late", "tie-first", "tie-second", "early"]
        # 최근 순은 limit을 채우면 멈추므로 뒤쪽 세션은 읽지 않는다
        for limit, reads in [
            (None, 6),
            (0, 0),
            (1, 1),
            (2, 2),
            (3, 3),
            (4, 6),
            (10, 6),
        ]:
            with self.subTest(limit=limit):
                result, search = self._run(grep_args(limit=limit))
                expected = ordered_hits if limit is None else ordered_hits[:limit]
                self.assertEqual([row["sid"] for row in result], expected)
                self.assertTrue(all(row["hit_count"] == 2 for row in result))
                self.assertEqual(search.call_count, reads)

    def test_relevance_reads_all_then_falls_back_to_hit_count(self):
        result, search = self._run(
            grep_args(sort="relevance", limit=2),
            hit_counts={"early": 9, "tie-second": 5},
        )
        self.assertEqual([row["sid"] for row in result], ["early", "tie-second"])
        self.assertEqual(search.call_count, 6)

    def test_relevance_ranks_keyword_coverage_before_raw_hits(self):
        def hit(role, term):
            return {"role": role, "ts": "", "term": term, "excerpt": term}

        result, _ = self._run(
            grep_args(keywords=["common", "rare"], sort="relevance"),
            hits_by_sid={
                # 흔한 키워드가 든 파일을 여러 번 읽은 세션
                "late": [hit("tool_result", "common")] * 9,
                # 두 키워드를 모두 다룬 세션
                "tie-first": [hit("tool_call", "rare"), hit("tool_result", "common")],
                # 같은 범위면 대화 hit가 이긴다
                "tie-second": [hit("user", "rare"), hit("assistant", "common")],
            },
        )
        self.assertEqual(
            [row["sid"] for row in result][:3], ["tie-second", "tie-first", "late"]
        )

    def test_current_session_ids_come_from_harness_env(self):
        env = {name: "" for name in history.CURRENT_SESSION_ENV}
        env["CODEX_THREAD_ID"] = "codex-thread"
        with patch.dict("os.environ", env):
            self.assertEqual(history.current_session_ids(), {"codex-thread"})

    def test_current_session_is_excluded_unless_include_self(self):
        result, _ = self._run(grep_args(), current={"late"})
        self.assertNotIn("late", [row["sid"] for row in result])
        result, _ = self._run(grep_args(include_self=True), current={"late"})
        self.assertIn("late", [row["sid"] for row in result])


if __name__ == "__main__":
    unittest.main()
