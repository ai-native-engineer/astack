#!/usr/bin/env python3
"""Regression checks for bounded lists and structurally safe redacted JSON."""

from __future__ import annotations

import io
import json
import sys
import unittest
from contextlib import redirect_stdout
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import session_history as history  # noqa: E402
from common import hits_from_messages  # noqa: E402
from session_history import (  # noqa: E402
    format_list_summary,
    redact_sensitive_text,
    redact_shapes_only,
    summarize_sessions,
)


class TestSafeListOutput(unittest.TestCase):
    def test_redacts_common_secret_shapes(self):
        jwt = ".".join(("eyJ" + "a" * 12, "b" * 14, "c" * 14))
        api_key = "sk-" + "d" * 24
        text = redact_sensitive_text(f"token={jwt} Bearer {api_key}")
        self.assertNotIn(jwt, text)
        self.assertNotIn(api_key, text)
        self.assertIn("[REDACTED]", text)

    def test_shape_only_redaction_covers_keyless_formats(self):
        """이름 없이 값만 있는 키도 디스크 치환에서 잡혀야 한다."""
        cases = [
            "AIza" + "B" * 35,
            "0e85f3a1-2b4c-4d6e-8f01-234567890abc:" + "d" * 32,
            "sk_" + "a" * 48,
        ]
        for secret in cases:
            with self.subTest(secret=secret[:6]):
                self.assertNotIn(secret, redact_shapes_only(f"value {secret} end"))

    def test_shape_only_redaction_leaves_ordinary_records_intact(self):
        """디스크 치환은 이름 기반 휴리스틱을 쓰지 않는다 - 멀쩡한 기록을
        덮어쓰면 되돌릴 수 없다."""
        for benign in ('"input_tokens": 4096', "token=3", "api_key=None"):
            with self.subTest(benign=benign):
                self.assertEqual(redact_shapes_only(benign), benign)
        # 화면 출력은 반대로 이 휴리스틱을 그대로 쓴다
        self.assertIn("[REDACTED]", redact_sensitive_text("api_key=None"))

    def test_summary_has_no_prompt_content_and_caps_projects(self):
        sessions = {
            str(index): {
                "tool": "codex",
                "project": f"/tmp/project-{index}",
                "messages": [{"text": "private prompt"}],
            }
            for index in range(12)
        }
        summary = summarize_sessions(sessions, "test")
        rendered = format_list_summary(sessions, "test")
        self.assertEqual(summary["total"], 12)
        self.assertEqual(len(summary["projects"]), 10)
        self.assertNotIn("private prompt", rendered)


class TestJsonOutput(unittest.TestCase):
    def render(self, value, raw=False):
        output = io.StringIO()
        with redirect_stdout(output):
            history.emit_json(value, SimpleNamespace(raw=raw))
        return output.getvalue()

    def test_nested_values_are_redacted_without_changing_keys_or_input(self):
        secret = "sk-" + "a" * 24
        payload = {
            "token": 3,
            "password": None,
            "secret": True,
            "api_key": False,
            "numbers": [0, -7, 2.5, 9007199254740993],
            "nested": [
                {secret: secret, "token=label": "password=fixture-value"},
                ("Bearer " + "b" * 24, None),
            ],
            17: {"text": '한글 "quoted" \\ path\nnext'},
        }
        original = deepcopy(payload)
        expected = {
            "token": 3,
            "password": None,
            "secret": True,
            "api_key": False,
            "numbers": [0, -7, 2.5, 9007199254740993],
            "nested": [
                {secret: "[REDACTED_API_KEY]", "token=label": "password=[REDACTED]"},
                ["Bearer [REDACTED]", None],
            ],
            17: {"text": '한글 "quoted" \\ path\nnext'},
        }
        masked = history.redact_json_values(payload)
        self.assertEqual(masked, expected)
        self.assertIn(17, masked)
        self.assertEqual(payload, original)

        # JSON itself stringifies numeric object keys; the redactor must not.
        expected["17"] = expected.pop(17)
        result = json.loads(self.render(payload))
        self.assertEqual(result, expected)
        self.assertIs(type(result["token"]), int)
        self.assertIs(result["secret"], True)
        self.assertIs(result["api_key"], False)
        self.assertIsNone(result["password"])
        self.assertEqual(payload, original)

    def test_secrets_at_end_of_excerpt_leave_json_delimiters_intact(self):
        cases = [
            ("password=fixture-value", "password=[REDACTED]"),
            ('api_key="fixture value"', "api_key=[REDACTED]"),
            ("Bearer " + "b" * 24, "Bearer [REDACTED]"),
            ("sk-" + "a" * 24, "[REDACTED_API_KEY]"),
        ]
        prefix = '한글 "quoted" \\ path\n'
        for secret, masked in cases:
            with self.subTest(secret=secret):
                payload = {"hits": [{"excerpt": prefix + secret}], "token": 4}
                result = json.loads(self.render(payload))
                self.assertEqual(
                    result, {"hits": [{"excerpt": prefix + masked}], "token": 4}
                )

    def test_serialized_text_is_not_masked_again(self):
        with patch.object(
            history, "redact_sensitive_text", wraps=history.redact_sensitive_text
        ) as redact:
            result = json.loads(
                self.render({"token": 3, "token=key": 0, "text": "api_key=None"})
            )
        redact.assert_called_once_with("api_key=None")
        self.assertEqual(
            result, {"token": 3, "token=key": 0, "text": "api_key=[REDACTED]"}
        )

    def test_raw_preserves_values_without_running_redaction(self):
        payload = {
            "nested": [{"text": 'token="fixture value"', "secret": "sk-" + "a" * 24}],
            "token": 3,
            "password": None,
            "enabled": False,
        }
        with patch.object(
            history, "redact_json_values", side_effect=AssertionError("raw redaction")
        ):
            self.assertEqual(json.loads(self.render(payload, raw=True)), payload)

    def test_strings_are_values_not_guessed_json_documents(self):
        for text in ('{"text": "ordinary"}', '{"text":', "not JSON"):
            with self.subTest(text=text):
                self.assertEqual(json.loads(self.render(text)), text)

    def test_invalid_json_values_raise_without_partial_output(self):
        cases = [
            ({"nested": [object()]}, TypeError),
            ({"nested": [float("nan")]}, ValueError),
            ({"nested": [float("inf")]}, ValueError),
        ]
        for raw in (False, True):
            for value, error in cases:
                with self.subTest(raw=raw, error=error, value=value):
                    output = io.StringIO()
                    with redirect_stdout(output), self.assertRaises(error):
                        history.emit_json(value, SimpleNamespace(raw=raw))
                    self.assertEqual(output.getvalue(), "")

    def test_text_emit_keeps_plain_text_and_raw_behavior(self):
        for raw in (False, True):
            with self.subTest(raw=raw):
                output = io.StringIO()
                with redirect_stdout(output):
                    history.emit("token=fixture-value", SimpleNamespace(raw=raw))
                expected = "token=fixture-value" if raw else "token=[REDACTED]"
                self.assertEqual(output.getvalue(), expected + "\n")


class TestSafeJsonCommands(unittest.TestCase):
    def setUp(self):
        self.sid = "synthetic-session"
        self.project = "/synthetic/" + "sk-" + "a" * 24
        self.masked_project = "/synthetic/[REDACTED_API_KEY]"
        self.text = 'café "quoted" \\ token=fixture-value'
        self.masked_text = 'café "quoted" \\ token=[REDACTED]'
        self.message = {"role": "user", "text": self.text, "ts": 1234, "time": "00:00"}
        self.sessions = {
            self.sid: {
                "tool": "codex",
                "project": self.project,
                "first_ts_ms": 1234,
                "messages": [self.message],
                "metadata": {"token": 3, "secret": False, "password": None},
            }
        }

    def run_cli(self, *arguments, raw=False):
        output = io.StringIO()
        argv = ["session_history.py", *arguments, "--format", "json"]
        if raw:
            argv.append("--raw")
        with (
            patch.object(sys, "argv", argv),
            patch.object(history, "set_include_subagents"),
            patch.object(history, "date_range", return_value=(0, 10000, "fixture")),
            patch.object(
                history,
                "collect_history",
                side_effect=lambda *args, **kwargs: deepcopy(self.sessions),
            ),
            redirect_stdout(output),
        ):
            history.main()
        return json.loads(output.getvalue())

    def test_list_json_preserves_metadata_and_masks_nested_messages(self):
        for raw in (False, True):
            with self.subTest(raw=raw):
                expected = deepcopy(self.sessions)
                if not raw:
                    expected[self.sid]["project"] = self.masked_project
                    expected[self.sid]["messages"][0]["text"] = self.masked_text
                self.assertEqual(self.run_cli("list", raw=raw), expected)

    def test_list_summary_json_masks_projects_and_keeps_counts(self):
        for raw in (False, True):
            with self.subTest(raw=raw):
                result = self.run_cli("list", "--summary", raw=raw)
                self.assertEqual(result["total"], 1)
                self.assertEqual(result["tools"]["codex"], 1)
                self.assertEqual(
                    result["projects"],
                    [{"project": self.project if raw else self.masked_project, "sessions": 1}],
                )

    def test_sources_json_masks_nested_strings_and_keeps_types(self):
        sources = [
            {
                "tool": "codex",
                "sessions": 3,
                "available": False,
                "roots": [{"path": self.project, "exists": False}],
                "notes": ["api_key=None"],
                "error": None,
            }
        ]
        for raw in (False, True):
            with self.subTest(raw=raw):
                expected = deepcopy(sources)
                if not raw:
                    expected[0]["roots"][0]["path"] = self.masked_project
                    expected[0]["notes"] = ["api_key=[REDACTED]"]
                with patch.object(history, "collect_sources", return_value=sources):
                    self.assertEqual(self.run_cli("sources", raw=raw), expected)

    def test_timeline_json_masks_messages_and_keeps_counts(self):
        for raw in (False, True):
            with self.subTest(raw=raw):
                result = self.run_cli("timeline", raw=raw)
                self.assertEqual(len(result), 1)
                self.assertEqual(result[0]["msg_count"], 1)
                self.assertEqual(
                    result[0]["project"], self.project if raw else self.masked_project
                )
                self.assertEqual(
                    result[0]["first_msg"], self.text if raw else self.masked_text
                )

    def test_empty_timeline_json_is_an_empty_array(self):
        self.sessions = {}
        for raw in (False, True):
            with self.subTest(raw=raw):
                self.assertEqual(self.run_cli("timeline", raw=raw), [])

    def test_rg_json_preserves_token_term_counts_and_excerpt_boundaries(self):
        adapter = SimpleNamespace(
            grep_session=lambda path, matcher, session_id: hits_from_messages(
                [self.message], matcher
            )
        )
        candidates = [
            (self.sid, self.sessions[self.sid], adapter, Path("synthetic.jsonl"))
        ]
        for raw in (False, True):
            with self.subTest(raw=raw), patch.object(
                history, "grep_candidates", return_value=candidates
            ), patch.object(history, "current_session_ids", return_value=set()):
                result = self.run_cli("rg", "token", raw=raw)
                self.assertEqual(len(result), 1)
                self.assertEqual(result[0]["terms"], {"token": 1})
                self.assertEqual(result[0]["hit_count"], 1)
                self.assertEqual(result[0]["talk_count"], 1)
                self.assertEqual(result[0]["first_ts_ms"], 1234)
                self.assertEqual(
                    result[0]["hits"][0]["excerpt"],
                    self.text if raw else self.masked_text,
                )

    def test_show_json_masks_conversation_values(self):
        adapter = SimpleNamespace(
            read_conversation=Mock(return_value=([self.message], "synthetic.jsonl"))
        )
        for raw in (False, True):
            with (
                self.subTest(raw=raw),
                patch.object(history, "find_session", return_value=[("codex", self.sid)]),
                patch.dict(history.ADAPTERS, {"codex": adapter}),
            ):
                result = self.run_cli("show", self.sid, raw=raw)
                expected = {**self.message, "index": 0}
                if not raw:
                    expected["text"] = self.masked_text
                self.assertEqual(result, [expected])

    def test_show_files_json_masks_changes_and_shell_hints(self):
        changes = [{"file": self.project, "tool": "write", "token": 3}]
        hints = [{"cmd": "echo token=fixture-value"}]
        adapter = SimpleNamespace(
            extract_changed_files=Mock(return_value=(changes, hints)),
            find_session_file=Mock(return_value="synthetic.jsonl"),
        )
        for raw in (False, True):
            with (
                self.subTest(raw=raw),
                patch.object(history, "find_session", return_value=[("codex", self.sid)]),
                patch.dict(history.ADAPTERS, {"codex": adapter}),
            ):
                result = self.run_cli("show", self.sid, "--files", raw=raw)
                expected = deepcopy({"changes": changes, "bash_hints": hints})
                if not raw:
                    expected["changes"][0]["file"] = self.masked_project
                    expected["bash_hints"][0]["cmd"] = "echo token=[REDACTED]"
                self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
