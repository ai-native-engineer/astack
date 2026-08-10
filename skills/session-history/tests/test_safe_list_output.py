#!/usr/bin/env python3
"""Regression checks for bounded, redacted session list output."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from session_history import format_list_summary, redact_sensitive_text, summarize_sessions  # noqa: E402


class TestSafeListOutput(unittest.TestCase):
    def test_redacts_common_secret_shapes(self):
        jwt = ".".join(("eyJ" + "a" * 12, "b" * 14, "c" * 14))
        api_key = "sk-" + "d" * 24
        text = redact_sensitive_text(f"token={jwt} Bearer {api_key}")
        self.assertNotIn(jwt, text)
        self.assertNotIn(api_key, text)
        self.assertIn("[REDACTED]", text)

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
