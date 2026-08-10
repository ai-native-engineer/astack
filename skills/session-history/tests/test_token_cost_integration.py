#!/usr/bin/env python3
"""Adapter field + common month-range integration tests (no full log scan)."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path
from types import SimpleNamespace

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from common import date_range_dt  # noqa: E402
from pricing import estimate_row_cost  # noqa: E402


class TestMonthRange(unittest.TestCase):
    def test_month_parse(self):
        args = SimpleNamespace(all_time=False, month="2026-07", date=None, days=1)
        start, end, label = date_range_dt(args)
        self.assertEqual(label, "2026-07")
        self.assertEqual(start.year, 2026)
        self.assertEqual(start.month, 7)
        self.assertEqual(start.day, 1)
        self.assertEqual(end.month, 8)
        self.assertEqual(end.day, 1)

    def test_month_current_const(self):
        args = SimpleNamespace(all_time=False, month="current", date=None, days=1)
        start, end, label = date_range_dt(args)
        self.assertRegex(label, r"^\d{4}-\d{2}$")
        self.assertIsNotNone(start)
        self.assertIsNotNone(end)

    def test_bad_month(self):
        args = SimpleNamespace(all_time=False, month="2026-13", date=None, days=1)
        with self.assertRaises(SystemExit):
            date_range_dt(args)


class TestCodexModelExtract(unittest.TestCase):
    def test_thread_settings_helper(self):
        from adapters.codex import _extract_thread_model

        payload = {
            "type": "thread_settings_applied",
            "thread_settings": {"model": "gpt-5.6-sol"},
        }
        self.assertEqual(_extract_thread_model(payload), "gpt-5.6-sol")

    def test_provider_label_not_used_as_model(self):
        # model_provider-style labels (openai/codex) are not billable model ids
        row = {
            "tool": "codex",
            "model": "openai",
            "input_tokens": 1_000_000,
            "cached_input_tokens": 0,
            "output_tokens": 0,
        }
        result = estimate_row_cost(row)
        self.assertFalse(result.missing)
        self.assertEqual(result.model_key, "gpt-5.6-sol")
        self.assertEqual(result.source, "default")
        self.assertAlmostEqual(result.usd, 5.0, places=4)

    def test_empty_model_uses_tool_default(self):
        row = {
            "tool": "codex",
            "model": "",
            "input_tokens": 1_000_000,
            "cached_input_tokens": 0,
            "output_tokens": 0,
        }
        result = estimate_row_cost(row)
        self.assertFalse(result.missing)
        self.assertEqual(result.model_key, "gpt-5.6-sol")
        self.assertEqual(result.source, "default")

    def test_unmatched_model_not_priced_as_flagship(self):
        row = {
            "tool": "claude",
            "model": "some-future-model-99",
            "input_tokens": 1_000_000,
            "output_tokens": 0,
            "cache_read_input_tokens": 0,
            "cache_creation_input_tokens": 0,
        }
        result = estimate_row_cost(row)
        self.assertTrue(result.missing)
        self.assertEqual(result.usd, 0.0)
        self.assertEqual(result.source, "unknown")


class TestClaudeCacheRowShape(unittest.TestCase):
    def test_estimate_with_adapter_fields(self):
        row = {
            "tool": "claude",
            "model": "claude-opus-5",
            "input_tokens": 2,
            "output_tokens": 155,
            "cache_creation_input_tokens": 40813,
            "cache_creation_5m_tokens": 0,
            "cache_creation_1h_tokens": 40813,
            "cache_read_input_tokens": 22700,
        }
        result = estimate_row_cost(row)
        self.assertGreater(result.usd, 0)
        self.assertIn("cache_write_1h", result.components)
        self.assertGreater(result.components["cache_write_1h"], 0)


if __name__ == "__main__":
    unittest.main()
