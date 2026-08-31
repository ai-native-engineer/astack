#!/usr/bin/env python3
"""Regression checks for bounded, redacted session list output."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

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


if __name__ == "__main__":
    unittest.main()
