"""pick_worker_model.py 단위 검사. 네트워크 없이 고정 models.dev 조각으로 돈다.
실행: 스킬 폴더에서 python3 -I tests/test_pick_worker_model.py
"""

import importlib.util
import unittest
from unittest.mock import patch
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "pick_worker_model.py"
spec = importlib.util.spec_from_file_location("pwm", SCRIPT)
pwm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pwm)


def model(
    cost_in,
    cost_out,
    family=None,
    ctx=1_000_000,
    tool_call=True,
    status=None,
    mtype=None,
    mid="m",
    released="2026-10-01",
):
    m = {
        "id": mid,
        "cost": {"input": cost_in, "output": cost_out},
        "limit": {"context": ctx},
        "tool_call": tool_call,
        "release_date": released,
    }
    if family:
        m["family"] = family
    if status:
        m["status"] = status
    if mtype:
        m["type"] = mtype
    return m


FIXTURE = {
    # reseller listed first on purpose: canonical provider must still win
    "some-reseller": {
        "models": {"claude-small-9": model(5, 25, "claude-small", mid="claude-small-9")}
    },
    "anthropic": {
        "models": {
            "claude-small-9": model(
                0.1, 0.5, "claude-small", mid="claude-small-9", released="2026-10-01"
            ),
            # older and *cheaper* than small-9: must still lose, same-generation rule
            "claude-small-8": model(
                0.05,
                0.2,
                "claude-small",
                ctx=200_000,
                mid="claude-small-8",
                released="2025-10-01",
            ),
            "claude-big-9": model(5, 25, "claude-big", mid="claude-big-9"),
            "claude-old-1": model(
                0.01,
                0.01,
                "claude-old",
                status="deprecated",
                mid="claude-old-1",
                released="2026-09-01",
            ),
            # last-generation tiny tier: newest of its family but 400 days behind
            "claude-tiny-3": model(
                0.01, 0.05, "claude-tiny", mid="claude-tiny-3", released="2025-08-01"
            ),
            "claude-embed": model(
                0.02, 0, "claude-embed", mtype="embedding", mid="claude-embed"
            ),
        }
    },
    "openai": {
        "models": {
            "gpt-x-tiny": model(0.1, 0.5, "gpt-tiny", mid="gpt-x-tiny"),
            "gpt-x-free": model(0, 0, "gpt-free", mid="gpt-x-free"),
            "gpt-x-notool": model(
                0.01, 0.01, "gpt-notool", tool_call=False, mid="gpt-x-notool"
            ),
        }
    },
    "indie-lab": {"models": {"indie-1": model(0.001, 0.001, mid="indie-1")}},
}


class PickTests(unittest.TestCase):
    def setUp(self):
        self.idx = pwm.price_index(FIXTURE)

    def test_canonical_provider_wins_over_reseller(self):
        self.assertEqual(self.idx["claude-small-9"]["provider"], "anthropic")
        self.assertEqual(self.idx["claude-small-9"]["cost"]["input"], 0.1)
        self.assertEqual(self.idx["some-reseller/claude-small-9"]["cost"]["input"], 5)

    def test_embeddings_are_not_candidates(self):
        self.assertNotIn("claude-embed", self.idx)

    def test_claude_aliases_are_family_names_with_cheapest_current_model(self):
        got = dict(pwm.available_claude(self.idx))
        self.assertEqual(set(got), {"small", "big", "old", "tiny"})
        self.assertEqual(got["small"]["id"], "claude-small-9")

    def test_pick_claude_skips_deprecated_and_returns_alias(self):
        rows, skipped = pwm.pick("claude", self.idx, 200_000, None)
        self.assertEqual(rows[0]["model"], "small")
        self.assertIn(
            ("old", "deprecated"), [(s["model"], s["reason"]) for s in skipped]
        )

    def test_last_generation_family_is_dropped_even_if_cheapest(self):
        rows, skipped = pwm.pick("claude", self.idx, 200_000, None)
        self.assertNotIn("tiny", [r["model"] for r in rows])
        self.assertTrue(
            any(s["model"] == "tiny" and "이전 세대" in s["reason"] for s in skipped)
        )
        rows, _ = pwm.pick("claude", self.idx, 200_000, None, generation_days=10_000)
        self.assertEqual(rows[0]["model"], "tiny")

    def test_older_model_in_same_family_is_dropped_even_if_cheaper(self):
        rows, skipped = pwm.pick(
            "codex", self.idx, 200_000, ["claude-small-8", "claude-small-9"]
        )
        self.assertEqual([r["model"] for r in rows], ["claude-small-9"])
        self.assertIn("더 새 모델", skipped[0]["reason"])

    def test_available_override_resolves_alias_and_ids(self):
        rows, skipped = pwm.pick("claude", self.idx, 200_000, ["big", "small", "nope"])
        self.assertEqual([r["model"] for r in rows], ["small", "big"])
        self.assertEqual(skipped[0]["model"], "nope")

    def test_free_and_toolless_and_indie_excluded_by_default(self):
        rows, skipped = pwm.pick(
            "codex",
            self.idx,
            200_000,
            ["gpt-x-tiny", "gpt-x-free", "gpt-x-notool", "indie-1"],
        )
        self.assertEqual([r["model"] for r in rows], ["gpt-x-tiny"])
        reasons = {s["model"]: s["reason"] for s in skipped}
        self.assertIn("free", reasons["gpt-x-free"])
        self.assertIn("tool", reasons["gpt-x-notool"])
        self.assertIn("indie-lab", reasons["indie-1"])

    def test_flags_lift_floors(self):
        rows, _ = pwm.pick(
            "codex",
            self.idx,
            200_000,
            ["gpt-x-tiny", "gpt-x-free", "indie-1"],
            allow_free=True,
            any_lab=True,
        )
        self.assertEqual(
            [r["model"] for r in rows], ["gpt-x-free", "indie-1", "gpt-x-tiny"]
        )

    def test_min_context_filters(self):
        rows, skipped = pwm.pick("codex", self.idx, 1_500_000, ["claude-small-9"])
        self.assertEqual(rows, [])
        self.assertIn("context", skipped[0]["reason"])

    def test_score_weights_input_heavier(self):
        self.assertAlmostEqual(pwm.score(model(1, 4)), 2.0)

    def test_effort_suffix_breaks_ties_toward_medium(self):
        self.assertEqual(
            sorted(["x-high", "x-low", "x-medium"], key=pwm.effort_rank),
            ["x-medium", "x-high", "x-low"],
        )

    def test_codex_catalog_env_overrides_account_cache(self):
        import json
        import os

        cat = Path(__file__).parent / "_fixture_codex_catalog.json"
        cat.write_text(
            json.dumps(
                {
                    "models": [
                        {"slug": "gpt-x-tiny", "visibility": "list"},
                        {"slug": "gpt-hidden", "visibility": "hide"},
                    ]
                }
            )
        )
        os.environ["CODEX_MODEL_CATALOG_JSON"] = str(cat)
        try:
            got = pwm.available_codex(self.idx)
            self.assertEqual([v for v, _ in got], ["gpt-x-tiny"])
        finally:
            del os.environ["CODEX_MODEL_CATALOG_JSON"]
            cat.unlink()


    def test_main_json_output_for_available(self):
        import contextlib
        import io
        import json

        pwm.CACHE_FILE = Path(__file__).parent / "_fixture_models_dev.json"
        pwm.CACHE_FILE.write_text(json.dumps(FIXTURE))
        try:
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                rc = pwm.main(
                    [
                        "--harness",
                        "claude",
                        "--available",
                        "big,small",
                        "--format",
                        "json",
                    ]
                )
            self.assertEqual(rc, 0)
            self.assertEqual(json.loads(buf.getvalue())["model"], "small")
        finally:
            pwm.CACHE_FILE.unlink()


class OmpCatalogTests(unittest.TestCase):
    def test_provider_route_is_required_before_catalog_query(self):
        with patch.dict(pwm.os.environ, {}, clear=True), patch.object(pwm, "run") as run:
            with self.assertRaises(SystemExit):
                pwm.available_omp({})
            run.assert_not_called()

    def test_catalog_shape_preserves_only_the_explicit_provider_selector(self):
        catalog = {"models": [
            {"provider": "proxy", "id": "model-1", "selector": "proxy/model-1"},
            {"provider": "other", "id": "model-1", "selector": "other/model-1"},
            {"provider": "proxy", "id": "model-1", "selector": "other/model-1"},
        ]}
        with patch.dict(pwm.os.environ, {"OMP_WORKER_PROVIDER": "proxy"}), patch.object(pwm, "run", return_value=pwm.json.dumps(catalog)) as run:
            self.assertEqual(pwm.available_omp({"model-1": {"id": "model-1"}}), [("proxy/model-1", {"id": "model-1"})])
        run.assert_called_once_with(["omp", "models", "proxy", "--json", "--no-extensions"])


if __name__ == "__main__":
    unittest.main(verbosity=1)
