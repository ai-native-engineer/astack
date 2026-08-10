#!/usr/bin/env python3
"""Unit tests for session-history pricing and cost estimation."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from pricing import (  # noqa: E402
    GROK_TICKS_PER_USD,
    PricingTable,
    estimate_row_cost,
    is_non_model_id,
    normalize_model_id,
    resolve_model_key,
    summarize_costs,
    ticks_to_usd,
)


class TestNormalize(unittest.TestCase):
    def test_sol_alias(self):
        key, src = resolve_model_key("gpt-5.6-sol", "codex")
        self.assertEqual(key, "gpt-5.6-sol")
        self.assertIn(src, ("match", "alias", "prefix"))

    def test_opus_alias(self):
        key, src = resolve_model_key("claude-opus-5-20260301", "claude")
        self.assertEqual(key, "claude-opus-5")

    def test_grok_build(self):
        key, _ = resolve_model_key("grok-4.5-build", "grok")
        self.assertEqual(key, "grok-4.5")

    def test_default_when_empty(self):
        key, src = resolve_model_key("", "codex")
        self.assertEqual(key, "gpt-5.6-sol")
        self.assertEqual(src, "default")

    def test_non_model_placeholders_default(self):
        for placeholder in ("openai", "codex", "<synthetic>", "synthetic"):
            self.assertTrue(is_non_model_id(placeholder), placeholder)
            key, src = resolve_model_key(placeholder, "codex")
            self.assertEqual(key, "gpt-5.6-sol", placeholder)
            self.assertEqual(src, "default", placeholder)

    def test_unmatched_real_model_is_unknown_not_default(self):
        key, src = resolve_model_key("totally-unknown-xyz", "claude")
        self.assertEqual(key, "totally-unknown-xyz")
        self.assertEqual(src, "unknown")
        result = estimate_row_cost(
            {
                "tool": "claude",
                "model": "totally-unknown-xyz",
                "input_tokens": 1_000_000,
                "output_tokens": 0,
            }
        )
        self.assertTrue(result.missing)
        self.assertEqual(result.usd, 0.0)
        self.assertEqual(result.source, "unknown")

    def test_openai_not_prefix_matched_to_o3(self):
        # "o3" is a substring of "openai"; must not resolve via loose prefix.
        key, src = resolve_model_key("openai", "codex")
        self.assertEqual(src, "default")
        self.assertEqual(key, "gpt-5.6-sol")

    def test_fable_rates(self):
        key, src = resolve_model_key("fable", "claude")
        self.assertEqual(key, "claude-fable-5")
        self.assertIn(src, ("match", "alias"))
        key2, _ = resolve_model_key("claude-fable-5", "claude")
        self.assertEqual(key2, "claude-fable-5")
        result = estimate_row_cost(
            {
                "tool": "claude",
                "model": "fable",
                "input_tokens": 1_000_000,
                "output_tokens": 0,
                "cache_read_input_tokens": 0,
                "cache_creation_input_tokens": 0,
            }
        )
        self.assertFalse(result.missing)
        self.assertAlmostEqual(result.usd, 10.0, places=4)
        self.assertEqual(result.model_key, "claude-fable-5")

    def test_normalize_strips_date(self):
        self.assertNotIn("20260301", normalize_model_id("claude-opus-5-20260301") or "x")


class TestCostEstimate(unittest.TestCase):
    def test_grok_ticks_priority(self):
        row = {
            "tool": "grok",
            "model": "grok-4.5-build",
            "input_tokens": 1000,
            "output_tokens": 100,
            "cached_read_tokens": 0,
            "cost_usd_ticks": GROK_TICKS_PER_USD,  # $1
        }
        result = estimate_row_cost(row)
        self.assertAlmostEqual(result.usd, 1.0, places=6)
        self.assertEqual(result.source, "provider_ticks")

    def test_ticks_to_usd(self):
        self.assertAlmostEqual(ticks_to_usd(6_016_812_000) or 0, 0.6016812, places=6)

    def test_claude_cache_split(self):
        # 1M input @ $5, 1M out @ $25, 1M cache read @ $0.50, 1M 1h write @ $10
        row = {
            "tool": "claude",
            "model": "claude-opus-5",
            "input_tokens": 1_000_000,
            "output_tokens": 1_000_000,
            "cache_read_input_tokens": 1_000_000,
            "cache_creation_input_tokens": 1_000_000,
            "cache_creation_5m_tokens": 0,
            "cache_creation_1h_tokens": 1_000_000,
        }
        result = estimate_row_cost(row)
        self.assertAlmostEqual(result.usd, 5 + 25 + 0.50 + 10, places=4)
        self.assertEqual(result.source, "rate_card")

    def test_claude_cache_fallback_to_5m(self):
        row = {
            "tool": "claude",
            "model": "claude-opus-5",
            "input_tokens": 0,
            "output_tokens": 0,
            "cache_read_input_tokens": 0,
            "cache_creation_input_tokens": 1_000_000,
            "cache_creation_5m_tokens": 0,
            "cache_creation_1h_tokens": 0,
        }
        result = estimate_row_cost(row)
        # 5m write $6.25
        self.assertAlmostEqual(result.usd, 6.25, places=4)

    def test_codex_sol(self):
        # 1M uncached @ $5, 1M cached @ $0.50, 1M out @ $30
        row = {
            "tool": "codex",
            "model": "gpt-5.6-sol",
            "input_tokens": 2_000_000,
            "cached_input_tokens": 1_000_000,
            "output_tokens": 1_000_000,
        }
        result = estimate_row_cost(row)
        self.assertAlmostEqual(result.usd, 5 + 0.50 + 30, places=4)

    def test_summarize_costs_tracks_missing_models(self):
        rows = [
            {
                "tool": "codex",
                "model": "gpt-5.6-sol",
                "input_tokens": 1_000_000,
                "cached_input_tokens": 0,
                "output_tokens": 0,
            },
            {
                "tool": "grok",
                "model": "grok-4.5",
                "input_tokens": 0,
                "output_tokens": 0,
                "cost_usd_ticks": GROK_TICKS_PER_USD // 2,
            },
            {
                "tool": "claude",
                "model": "brand-new-unlisted",
                "input_tokens": 1000,
                "output_tokens": 0,
            },
        ]
        summary = summarize_costs(rows, PricingTable())
        self.assertAlmostEqual(summary["total_usd"], 5.0 + 0.5, places=4)
        self.assertEqual(summary["priced_rows"], 2)
        self.assertEqual(summary["missing_rows"], 1)
        self.assertIn("gpt-5.6-sol", summary["by_model"])
        self.assertIn("grok-4.5", summary["by_model"])
        self.assertIn("brand-new-unlisted", summary["missing_models"])
        self.assertEqual(summary["missing_models"]["brand-new-unlisted"]["events"], 1)


if __name__ == "__main__":
    unittest.main()
