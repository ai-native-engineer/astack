"""Codex transcript coverage must survive format changes and missing rollout tails."""

from __future__ import annotations

import argparse
import contextlib
import datetime
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import session_history as cli
from adapters import codex
from common import Matcher, refresh_indexes

SID = "20000000-0000-4000-8000-000000000021"
SEGMENT = "20000000-0000-4000-8000-000000000022"
STAMP = "2026-08-18T00:00:00Z"


def message(text, *, role="user", ident="m1", ordinal=1, second=1):
    return {
        "type": "response_item",
        "ordinal": ordinal,
        "timestamp": f"2026-08-18T00:00:{second:02d}Z",
        "payload": {
            "type": "message",
            "id": ident,
            "role": role,
            "content": [{"type": "input_text", "text": text}],
        },
    }


class CodexRecoveryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.sessions = self.root / "sessions"
        self.sessions.mkdir()
        self.history = self.root / "history.jsonl"
        for key, value in {
            "CODEX_SESSIONS_DIR": self.sessions,
            "CODEX_ARCHIVED_SESSIONS_DIR": self.root / "archived",
            "CODEX_HISTORY": self.history,
            "CODEX_STATE_DB": self.root / "missing.sqlite",
        }.items():
            patcher = mock.patch.object(codex, key, value)
            patcher.start()
            self.addCleanup(patcher.stop)
        refresh_indexes()
        self.addCleanup(refresh_indexes)

    def rollout(self, records, *, suffix="", base=None):
        path = self.sessions / f"rollout-{SID}{suffix}.jsonl"
        meta = {
            "id": SID,
            "cwd": str(self.root),
            "timestamp": STAMP,
            "history_mode": "paginated",
        }
        if base:
            meta["timestamp"] = "2026-08-18T00:00:02Z"
            meta["history_base"] = base
        path.write_text(
            "".join(
                json.dumps(row) + "\n"
                for row in [
                    {"type": "session_meta", "ordinal": 0, "payload": meta},
                    *records,
                ]
            ),
            encoding="utf-8",
        )
        refresh_indexes()
        return path

    def prompts(self, *texts):
        ts = int(
            datetime.datetime.fromisoformat(STAMP.replace("Z", "+00:00")).timestamp()
        )
        self.history.write_text(
            "".join(
                json.dumps(
                    {
                        "session_id": SID,
                        "ts": ts + second,
                        "text": text,
                    }
                )
                + "\n"
                for second, text in texts
            ),
            encoding="utf-8",
        )
        refresh_indexes()

    def test_modern_messages_skip_injected_context_and_deduplicate_event_mirror(self):
        self.rollout(
            [
                message(
                    "# AGENTS.md instructions\n<INSTRUCTIONS>injected</INSTRUCTIONS>"
                ),
                message("first request", ident="msg_u1", ordinal=2, second=2),
                {
                    "type": "event_msg",
                    "ordinal": 3,
                    "timestamp": "2026-08-18T00:00:02Z",
                    "payload": {
                        "type": "item_completed",
                        "item": {
                            "type": "userMessage",
                            "id": "u1",
                            "content": [{"type": "text", "text": "first request"}],
                        },
                    },
                },
                message(
                    "assistant reply", role="assistant", ident="a1", ordinal=4, second=3
                ),
                message("first request", ident="u2", ordinal=5, second=4),
            ]
        )
        rows, _ = codex.read_conversation(SID)
        self.assertEqual(
            [r["text"] for r in rows],
            ["first request", "assistant reply", "first request"],
        )

    def test_custom_calls_and_list_outputs_are_searchable_without_early_clipping(self):
        long_text = "x" * 900 + " recovery needle"
        self.rollout(
            [
                {
                    "type": "response_item",
                    "payload": {
                        "type": "custom_tool_call",
                        "name": "exec",
                        "call_id": "call1",
                        "input": "x" * 400 + " call needle",
                    },
                },
                {
                    "type": "response_item",
                    "payload": {
                        "type": "custom_tool_call_output",
                        "call_id": "call1",
                        "output": [{"type": "input_text", "text": long_text}],
                    },
                },
            ]
        )
        rows, _ = codex.read_conversation(SID, True)
        self.assertEqual([r["role"] for r in rows], ["tool_call", "tool_result"])
        self.assertIn(long_text, rows[1]["text"])
        self.assertEqual(
            len(
                codex.grep_session(codex.find_session_file(SID), "recovery needle", SID)
            ),
            1,
        )

    def test_different_message_ids_are_not_deduplicated_by_close_timestamps(self):
        self.rollout(
            [
                message("repeat", ident="first", second=1),
                {
                    "type": "event_msg",
                    "timestamp": "2026-08-18T00:00:02Z",
                    "payload": {
                        "type": "item_completed",
                        "item": {
                            "type": "userMessage",
                            "id": "second",
                            "content": [{"type": "text", "text": "repeat"}],
                        },
                    },
                },
            ]
        )
        rows, _ = codex.read_conversation(SID)
        self.assertEqual(len(rows), 2)

    def test_child_cutoff_propagates_to_earlier_ancestor(self):
        parent = self.rollout(
            [
                message("keep", ordinal=1),
                message("exclude ancestor", ident="drop", ordinal=3, second=3),
            ]
        )
        middle = self.rollout(
            [message("middle", ident="middle", ordinal=5, second=5)],
            suffix="_" + SEGMENT,
            base={
                "thread_id": SID,
                "end_ordinal_exclusive": 5,
                "end_byte_offset": parent.stat().st_size,
            },
        )
        last_id = "20000000-0000-4000-8000-000000000023"
        self.rollout(
            [message("current", ident="current", ordinal=2, second=8)],
            suffix="_" + last_id,
            base={
                "thread_id": SEGMENT,
                "end_ordinal_exclusive": 2,
                "end_byte_offset": middle.stat().st_size,
            },
        )
        rows, _ = codex.read_conversation(SID)
        self.assertEqual([r["text"] for r in rows], ["keep", "current"])

    def test_history_does_not_reinsert_known_excluded_branch_request(self):
        parent = self.rollout(
            [
                message("keep", ordinal=1),
                message("abandoned request", ident="drop", ordinal=3, second=3),
            ]
        )
        self.rollout(
            [message("current", ident="current", ordinal=2, second=4)],
            suffix="_" + SEGMENT,
            base={
                "thread_id": SID,
                "end_ordinal_exclusive": 2,
                "end_byte_offset": parent.stat().st_size,
            },
        )
        self.prompts((1, "keep"), (3, "abandoned request"), (4, "current"))
        rows, _ = codex.read_conversation(SID)
        self.assertEqual([r["text"] for r in rows], ["keep", "current"])
        self.assertEqual(codex.conversation_status(SID)["excluded_history_count"], 1)

    def test_old_rollout_cannot_consume_later_identical_history_request(self):
        self.rollout([message("repeat", second=1)])
        self.prompts((30, "repeat"))
        rows, _ = codex.read_conversation(SID)
        self.assertEqual([r["source"] for r in rows], ["rollout", "history"])

    def test_excluded_mirrors_do_not_consume_a_new_repeated_request(self):
        parent = self.rollout(
            [
                message("keep", ordinal=1),
                message("repeat", ident="drop", ordinal=3, second=3),
                {
                    "type": "event_msg",
                    "ordinal": 4,
                    "timestamp": "2026-08-18T00:00:03Z",
                    "payload": {"type": "user_message", "message": "repeat"},
                },
            ]
        )
        self.rollout(
            [message("new branch", ident="current", ordinal=2, second=10)],
            suffix="_" + SEGMENT,
            base={
                "thread_id": SID,
                "end_ordinal_exclusive": 2,
                "end_byte_offset": parent.stat().st_size,
            },
        )
        self.prompts((1, "keep"), (3, "repeat"), (10, "new branch"), (30, "repeat"))
        rows, _ = codex.read_conversation(SID)
        self.assertEqual([r["text"] for r in rows], ["keep", "new branch", "repeat"])
        self.assertEqual(rows[-1]["source"], "history")
        self.assertEqual(codex.conversation_status(SID)["excluded_history_count"], 1)

    def test_lineage_includes_parent_prefix_but_not_superseded_tail(self):
        parent = self.rollout(
            [
                message("parent retained"),
                message("superseded tail", ordinal=3, second=3),
            ]
        )
        latest = self.rollout(
            [message("latest branch", ident="latest", ordinal=2, second=4)],
            suffix="_" + SEGMENT,
            base={
                "thread_id": SID,
                "end_ordinal_exclusive": 2,
                "end_byte_offset": parent.stat().st_size + 100,
            },
        )
        rows, chosen = codex.read_conversation(SID)
        self.assertEqual(chosen, latest)
        self.assertEqual(
            [r["text"] for r in rows], ["parent retained", "latest branch"]
        )
        self.assertTrue(codex.conversation_status(SID)["warnings"])

    def test_history_recovers_latest_prompt_and_labels_missing_response(self):
        self.rollout(
            [
                message("known request"),
                message("old reply", role="assistant", ident="a", second=2),
            ]
        )
        self.prompts((1, "known request"), (20, "latest request after lost tail"))
        rows, _ = codex.read_conversation(SID)
        self.assertEqual(
            [r["text"] for r in rows],
            ["known request", "old reply", "latest request after lost tail"],
        )
        self.assertEqual(rows[-1]["source"], "history")
        self.assertEqual(codex.conversation_status(SID)["history_only_count"], 1)
        self.assertEqual([r["role"] for r in rows].count("assistant"), 1)

    def test_history_matching_preserves_repeated_user_submissions(self):
        self.rollout([message("repeat")])
        self.prompts((1, "repeat"), (20, "repeat"))
        rows, _ = codex.read_conversation(SID)
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[-1]["source"], "history")

    def test_history_image_marker_matches_rollout_attachment_wrapper(self):
        self.rollout(
            [
                message(
                    '<image name="ref" path="/example/ref.png"></image>\n[Image #1]\n\nuse this'
                )
            ]
        )
        self.prompts((1, "[Image #1]\n\nuse this"))
        rows, _ = codex.read_conversation(SID)
        self.assertEqual(len(rows), 1)

    def test_repeated_prompt_matches_saved_latest_occurrence(self):
        self.rollout([message("repeat", second=20)])
        self.prompts((1, "repeat"), (20, "repeat"))
        rows, _ = codex.read_conversation(SID)
        self.assertEqual([row["source"] for row in rows], ["history", "rollout"])
        self.assertEqual(codex.conversation_status(SID)["history_only_count"], 1)

    def test_missing_parent_is_reported_without_losing_readable_child(self):
        self.rollout(
            [message("readable child")],
            suffix="_" + SEGMENT,
            base={
                "thread_id": "missing-parent",
                "end_ordinal_exclusive": 2,
                "end_byte_offset": 200,
            },
        )
        rows, _ = codex.read_conversation(SID)
        self.assertEqual(rows[0]["text"], "readable child")
        self.assertTrue(codex.conversation_status(SID)["warnings"])

    def test_rg_and_show_agree_on_history_only_prompt(self):
        path = self.rollout([message("old text")])
        self.prompts((20, "only in input history"))
        with mock.patch.object(cli, "prefilter_paths", return_value=set()):
            candidates = cli.grep_candidates(
                {SID: {"tool": "codex", "first_ts_ms": 1}},
                Matcher("only in input history"),
            )
        self.assertEqual(len(candidates), 1)
        hits = codex.grep_session(path, "only in input history", SID)
        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0]["source"], "history")

    def test_show_json_warns_and_marks_recovered_prompt(self):
        self.rollout([message("known")])
        self.prompts((20, "missing tail"))
        args = argparse.Namespace(
            last=False,
            session=SID,
            tool="codex",
            grep=None,
            regex=False,
            full=False,
            files=False,
            context=0,
            offset=0,
            limit=None,
            format="json",
            raw=False,
        )
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            cli.cmd_show(args)
        self.assertEqual(json.loads(out.getvalue())[-1]["source"], "history")
        self.assertIn("history.jsonl", err.getvalue())

    def test_changed_files_follow_lineage(self):
        parent = self.rollout(
            [
                {
                    "type": "response_item",
                    "ordinal": 1,
                    "payload": {
                        "type": "custom_tool_call",
                        "name": "apply_patch",
                        "input": "*** Add File: before.py\n+ok",
                    },
                }
            ]
        )
        self.rollout(
            [message("new branch", ordinal=2)],
            suffix="_" + SEGMENT,
            base={
                "thread_id": SID,
                "end_ordinal_exclusive": 2,
                "end_byte_offset": parent.stat().st_size,
            },
        )
        changes, _ = codex.extract_changed_files(SID)
        self.assertEqual([c["file"] for c in changes], ["before.py"])

    def test_redact_apply_refuses_paginated_rollout_rewrite(self):
        path = self.rollout([message("key " + "sk-" + "A" * 40)])
        original = path.read_bytes()
        args = argparse.Namespace(
            tool="codex",
            path=[str(path)],
            exclude=[],
            apply=True,
            backup=str(self.root / "backup.tar.gz"),
        )
        with (
            mock.patch.object(cli, "collect_sources", return_value=[]),
            contextlib.redirect_stdout(io.StringIO()),
            contextlib.redirect_stderr(io.StringIO()),
            self.assertRaises(SystemExit),
        ):
            cli.cmd_redact(args)
        self.assertEqual(path.read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
