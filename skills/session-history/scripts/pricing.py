"""API-equivalent cost estimation for session-history token rows.

Rates are USD per million tokens (MTok), snapshot-style defaults for CLI models.
Grok rows with cost_usd_ticks use provider ticks (10_000_000_000 ticks = $1)
instead of rate-card math when present.

Override path (optional JSON map model_id -> rates):
  --pricing-file /path/to/pricing.json
  or SESSION_HISTORY_PRICING=/path/to/pricing.json

Resolution policy:
  - empty model or known non-model placeholder (provider labels, <synthetic>)
    → tool default rates, source=default
  - known model (exact / alias / safe prefix) → rate card, source=match|alias|prefix
  - non-empty unmatched model → unpriced (usd=0, missing=True), never silent flagship fallback
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

# Provider-reported Grok cost scale (observed in updates.jsonl costUsdTicks).
GROK_TICKS_PER_USD = 10_000_000_000

# Tool defaults when model is empty/placeholder only (never for unmatched real ids).
TOOL_DEFAULT_MODELS = {
    "claude": "claude-opus-5",
    "codex": "gpt-5.6-sol",
    "grok": "grok-4.5",
}

# Provider/tool labels that appear in model fields but are not billable model ids.
# (Claude Code / Codex / Grok only — no local proxy names.)
NON_MODEL_IDS = frozenset(
    {
        "openai",
        "codex",
        "anthropic",
        "xai",
        "claude",
        "grok",
        "<synthetic>",
        "synthetic",
        "unknown",
        "default",
        "none",
        "null",
        "n/a",
        "na",
    }
)


@dataclass(frozen=True)
class ModelRates:
    """USD per 1M tokens."""

    input: float
    output: float
    # OpenAI/xAI style: price for the cached portion of input
    cached_input: float = 0.0
    # Anthropic prompt-cache writes
    cache_write_5m: float | None = None
    cache_write_1h: float | None = None
    # Anthropic cache hits (also used if cached_input is 0 and cache_read set)
    cache_read: float | None = None
    style: str = "generic"  # anthropic | openai | xai | generic
    note: str = ""

    def resolved_cache_read(self) -> float:
        if self.cache_read is not None:
            return self.cache_read
        return self.cached_input


# Snapshot rates (2026-08 official list prices used for API-equivalent math).
# Sources (human-maintained): Anthropic/OpenAI/xAI public pricing pages;
# Fable 5 = Anthropic list $10/$50 (2x Opus 4.8 family cache multipliers).
# Keys are normalized ids (see normalize_model_id).
DEFAULT_RATES: dict[str, ModelRates] = {
    # OpenAI Codex CLI families
    "gpt-5.6-sol": ModelRates(5.0, 30.0, cached_input=0.50, style="openai"),
    "gpt-5.6-terra": ModelRates(2.0, 12.0, cached_input=0.20, style="openai"),
    "gpt-5.6-luna": ModelRates(0.20, 1.20, cached_input=0.02, style="openai"),
    "gpt-5.5": ModelRates(1.75, 14.0, cached_input=0.175, style="openai"),
    "gpt-5.4": ModelRates(1.75, 14.0, cached_input=0.175, style="openai", note="approx"),
    "gpt-5": ModelRates(1.25, 10.0, cached_input=0.125, style="openai", note="approx"),
    "o3": ModelRates(2.0, 8.0, cached_input=0.50, style="openai", note="approx"),
    "o4-mini": ModelRates(1.10, 4.40, cached_input=0.275, style="openai", note="approx"),
    # Anthropic Claude Code
    "claude-opus-5": ModelRates(
        5.0, 25.0, cache_write_5m=6.25, cache_write_1h=10.0, cache_read=0.50, style="anthropic"
    ),
    "claude-opus-4.8": ModelRates(
        5.0, 25.0, cache_write_5m=6.25, cache_write_1h=10.0, cache_read=0.50, style="anthropic"
    ),
    "claude-opus-4.7": ModelRates(
        5.0, 25.0, cache_write_5m=6.25, cache_write_1h=10.0, cache_read=0.50, style="anthropic"
    ),
    "claude-opus-4.6": ModelRates(
        5.0, 25.0, cache_write_5m=6.25, cache_write_1h=10.0, cache_read=0.50, style="anthropic"
    ),
    "claude-opus-4.5": ModelRates(
        5.0, 25.0, cache_write_5m=6.25, cache_write_1h=10.0, cache_read=0.50, style="anthropic"
    ),
    "claude-opus-4.1": ModelRates(
        15.0, 75.0, cache_write_5m=18.75, cache_write_1h=30.0, cache_read=1.50, style="anthropic"
    ),
    "claude-opus-4": ModelRates(
        15.0, 75.0, cache_write_5m=18.75, cache_write_1h=30.0, cache_read=1.50, style="anthropic"
    ),
    # Sonnet 5 intro through 2026-08-31; table uses intro rates (document in note).
    "claude-sonnet-5": ModelRates(
        2.0,
        10.0,
        cache_write_5m=2.50,
        cache_write_1h=4.0,
        cache_read=0.20,
        style="anthropic",
        note="intro $2/$10 through 2026-08-31; then $3/$15",
    ),
    "claude-sonnet-4.6": ModelRates(
        3.0, 15.0, cache_write_5m=3.75, cache_write_1h=6.0, cache_read=0.30, style="anthropic"
    ),
    "claude-sonnet-4.5": ModelRates(
        3.0, 15.0, cache_write_5m=3.75, cache_write_1h=6.0, cache_read=0.30, style="anthropic"
    ),
    "claude-sonnet-4": ModelRates(
        3.0, 15.0, cache_write_5m=3.75, cache_write_1h=6.0, cache_read=0.30, style="anthropic"
    ),
    "claude-haiku-4.5": ModelRates(
        1.0, 5.0, cache_write_5m=1.25, cache_write_1h=2.0, cache_read=0.10, style="anthropic"
    ),
    "claude-haiku-4": ModelRates(
        1.0, 5.0, cache_write_5m=1.25, cache_write_1h=2.0, cache_read=0.10, style="anthropic"
    ),
    "claude-haiku-3.5": ModelRates(
        0.80, 4.0, cache_write_5m=1.0, cache_write_1h=1.6, cache_read=0.08, style="anthropic"
    ),
    # Claude Fable 5 (list $10/$50; cache 1.25x / 2x / 0.1x input)
    "claude-fable-5": ModelRates(
        10.0,
        50.0,
        cache_write_5m=12.5,
        cache_write_1h=20.0,
        cache_read=1.0,
        style="anthropic",
        note="list $10/$50",
    ),
    # xAI Grok Build
    "grok-4.5": ModelRates(2.0, 6.0, cached_input=0.30, style="xai"),
    "grok-4": ModelRates(3.0, 15.0, cached_input=0.75, style="xai", note="approx"),
    "grok-3": ModelRates(3.0, 15.0, cached_input=0.75, style="xai", note="approx"),
}

# Alias fragments -> canonical key (first match wins after normalize).
_ALIAS_RULES: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"gpt-5\.6-sol|gpt-5-6-sol|5\.6-sol"), "gpt-5.6-sol"),
    (re.compile(r"gpt-5\.6-terra|gpt-5-6-terra|5\.6-terra"), "gpt-5.6-terra"),
    (re.compile(r"gpt-5\.6-luna|gpt-5-6-luna|5\.6-luna"), "gpt-5.6-luna"),
    (re.compile(r"gpt-5\.5"), "gpt-5.5"),
    (re.compile(r"gpt-5\.4"), "gpt-5.4"),
    (re.compile(r"\bo3\b"), "o3"),
    (re.compile(r"o4-mini"), "o4-mini"),
    (re.compile(r"claude-fable-5|fable-5|\bfable\b"), "claude-fable-5"),
    (re.compile(r"claude-opus-5|opus-5|opus\[1m\]|opus-1m"), "claude-opus-5"),
    (re.compile(r"claude-opus-4[.-]?8|opus-4\.8"), "claude-opus-4.8"),
    (re.compile(r"claude-opus-4[.-]?7|opus-4\.7"), "claude-opus-4.7"),
    (re.compile(r"claude-opus-4[.-]?6|opus-4\.6"), "claude-opus-4.6"),
    (re.compile(r"claude-opus-4[.-]?5|opus-4\.5"), "claude-opus-4.5"),
    (re.compile(r"claude-opus-4[.-]?1|opus-4\.1"), "claude-opus-4.1"),
    (re.compile(r"claude-opus-4(?![.\-\d])|opus-4\b"), "claude-opus-4"),
    (re.compile(r"claude-sonnet-5|sonnet-5"), "claude-sonnet-5"),
    (re.compile(r"claude-sonnet-4[.-]?6|sonnet-4\.6"), "claude-sonnet-4.6"),
    (re.compile(r"claude-sonnet-4[.-]?5|sonnet-4\.5"), "claude-sonnet-4.5"),
    (re.compile(r"claude-sonnet-4|sonnet-4\b"), "claude-sonnet-4"),
    (re.compile(r"claude-haiku-4[.-]?5|haiku-4\.5"), "claude-haiku-4.5"),
    (re.compile(r"claude-haiku-4|haiku-4\b"), "claude-haiku-4"),
    (re.compile(r"claude-haiku-3\.5|haiku-3\.5"), "claude-haiku-3.5"),
    (re.compile(r"grok-4\.5|grok-4-5"), "grok-4.5"),
    (re.compile(r"grok-4\b"), "grok-4"),
    (re.compile(r"grok-3\b"), "grok-3"),
]


def normalize_model_id(model: str | None) -> str:
    if not model:
        return ""
    text = str(model).strip().lower()
    text = text.replace("@", "-")
    # drop common date/build suffixes after first useful segment
    text = re.sub(r"(\d{8}).*$", r"\1", text)  # keep date if present then trim later
    text = re.sub(r"-\d{8}.*$", "", text)
    text = re.sub(r"-build(?:-.*)?$", "", text)
    text = re.sub(r"\s+", "", text)
    return text


def is_non_model_id(model: str | None) -> bool:
    """True for empty or known provider/proxy/synthetic labels, not billable models."""
    raw = normalize_model_id(model)
    if not raw:
        return True
    if raw in NON_MODEL_IDS:
        return True
    # angle-bracket synthetic markers: <synthetic>, <system>, ...
    if raw.startswith("<") and raw.endswith(">"):
        return True
    return False


def resolve_model_key(model: str | None, tool: str | None = None) -> tuple[str, str]:
    """Return (canonical_key, source).

    source: match | alias | prefix | default | unknown
    default only when model empty/placeholder; unmatched real ids → unknown.
    """
    if is_non_model_id(model):
        if tool and tool in TOOL_DEFAULT_MODELS:
            return TOOL_DEFAULT_MODELS[tool], "default"
        return "unknown", "unknown"

    raw = normalize_model_id(model)
    if raw in DEFAULT_RATES:
        return raw, "match"
    for pattern, key in _ALIAS_RULES:
        if pattern.search(raw):
            return key, "alias"
    # Safe prefix only: model id starts with a known key (avoids "o3" in "openai").
    for key in sorted(DEFAULT_RATES.keys(), key=len, reverse=True):
        if raw.startswith(key):
            return key, "prefix"
    # Unmatched real model id — do not silent-fallback to flagship pricing.
    return raw or "unknown", "unknown"


def _rates_from_dict(data: dict[str, Any]) -> ModelRates:
    return ModelRates(
        input=float(data.get("input") or data.get("input_per_mtok") or 0),
        output=float(data.get("output") or data.get("output_per_mtok") or 0),
        cached_input=float(data.get("cached_input") or data.get("cached_input_per_mtok") or 0),
        cache_write_5m=_opt_float(data.get("cache_write_5m")),
        cache_write_1h=_opt_float(data.get("cache_write_1h")),
        cache_read=_opt_float(data.get("cache_read")),
        style=str(data.get("style") or "generic"),
        note=str(data.get("note") or ""),
    )


def _opt_float(value) -> float | None:
    if value is None or value == "":
        return None
    return float(value)


def load_pricing_overrides(path: str | Path | None = None) -> dict[str, ModelRates]:
    path = path or os.environ.get("SESSION_HISTORY_PRICING")
    if not path:
        return {}
    p = Path(path).expanduser()
    if not p.exists():
        return {}
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    models = data.get("models") if isinstance(data, dict) and "models" in data else data
    if not isinstance(models, dict):
        return {}
    out: dict[str, ModelRates] = {}
    for key, value in models.items():
        if isinstance(value, dict):
            out[normalize_model_id(key)] = _rates_from_dict(value)
    return out


class PricingTable:
    def __init__(self, overrides: dict[str, ModelRates] | None = None):
        self.rates = dict(DEFAULT_RATES)
        if overrides:
            self.rates.update(overrides)

    def lookup(self, model: str | None, tool: str | None = None) -> tuple[ModelRates | None, str, str]:
        key, source = resolve_model_key(model, tool)
        rates = self.rates.get(key)
        if rates is None:
            return None, key, "unknown"
        return rates, key, source


@dataclass
class CostResult:
    usd: float
    model_key: str
    source: str  # provider_ticks | rate_card | default | unknown
    components: dict[str, float]
    missing: bool = False
    raw_model: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def ticks_to_usd(ticks: int | float | None) -> float | None:
    if ticks is None:
        return None
    return float(ticks) / GROK_TICKS_PER_USD


def _mtok(tokens: int | float, rate: float) -> float:
    if not tokens or not rate:
        return 0.0
    return (float(tokens) / 1_000_000.0) * float(rate)


def estimate_row_cost(row: dict[str, Any], table: PricingTable | None = None) -> CostResult:
    """Estimate API-equivalent USD for one token_usage row."""
    table = table or PricingTable()
    tool = row.get("tool") or ""
    model = row.get("model") or ""
    raw_model = str(model)

    # Prefer provider-reported Grok ticks when present.
    ticks = row.get("cost_usd_ticks")
    if ticks is None and row.get("cost_usd") is not None and tool == "grok":
        key, _ = resolve_model_key(model, tool)
        return CostResult(
            usd=float(row["cost_usd"]),
            model_key=key if key != "unknown" else (normalize_model_id(model) or "grok-4.5"),
            source="provider_ticks",
            components={"provider_ticks_usd": float(row["cost_usd"])},
            raw_model=raw_model,
        )
    if ticks is not None:
        usd = ticks_to_usd(ticks) or 0.0
        key, _ = resolve_model_key(model, tool)
        return CostResult(
            usd=usd,
            model_key=key if key != "unknown" else (normalize_model_id(model) or "grok-4.5"),
            source="provider_ticks",
            components={"provider_ticks_usd": usd, "cost_usd_ticks": float(ticks)},
            raw_model=raw_model,
        )

    rates, model_key, source = table.lookup(model, tool)
    if rates is None or source == "unknown":
        return CostResult(
            usd=0.0,
            model_key=model_key,
            source="unknown",
            components={},
            missing=True,
            raw_model=raw_model,
        )

    components: dict[str, float] = {}
    if tool == "claude" or rates.style == "anthropic":
        input_tokens = int(row.get("input_tokens") or 0)
        output_tokens = int(row.get("output_tokens") or 0)
        cache_read = int(row.get("cache_read_input_tokens") or 0)
        cache_5m = int(row.get("cache_creation_5m_tokens") or 0)
        cache_1h = int(row.get("cache_creation_1h_tokens") or 0)
        cache_create_total = int(row.get("cache_creation_input_tokens") or 0)
        if cache_5m == 0 and cache_1h == 0 and cache_create_total:
            # No 5m/1h split: bill whole write at 5m rate (underestimates 1h).
            cache_5m = cache_create_total
        write_5m_rate = rates.cache_write_5m if rates.cache_write_5m is not None else rates.input * 1.25
        write_1h_rate = rates.cache_write_1h if rates.cache_write_1h is not None else rates.input * 2.0
        read_rate = rates.resolved_cache_read()
        components["input"] = _mtok(input_tokens, rates.input)
        components["output"] = _mtok(output_tokens, rates.output)
        components["cache_read"] = _mtok(cache_read, read_rate)
        components["cache_write_5m"] = _mtok(cache_5m, write_5m_rate)
        components["cache_write_1h"] = _mtok(cache_1h, write_1h_rate)
    else:
        # OpenAI / xAI / generic: input includes cached; bill uncached + cached + output.
        input_tokens = int(row.get("input_tokens") or 0)
        cached = int(
            row.get("cached_input_tokens")
            or row.get("cached_read_tokens")
            or 0
        )
        output_tokens = int(row.get("output_tokens") or 0)
        # reasoning is usually already in output_tokens; do not double-count.
        uncached = max(0, input_tokens - cached)
        read_rate = rates.resolved_cache_read()
        components["uncached_input"] = _mtok(uncached, rates.input)
        components["cached_input"] = _mtok(cached, read_rate)
        components["output"] = _mtok(output_tokens, rates.output)

    usd = sum(components.values())
    cost_source = "default" if source == "default" else "rate_card"
    return CostResult(
        usd=usd,
        model_key=model_key,
        source=cost_source,
        components=components,
        missing=False,
        raw_model=raw_model,
    )


def empty_cost_summary() -> dict[str, Any]:
    return {
        "total_usd": 0.0,
        "priced_rows": 0,
        "missing_rows": 0,
        "by_tool": {},
        "by_model": {},
        "by_source": {},
        "components": {},
        "missing_models": {},
    }


def apply_cost_result(
    summary: dict[str, Any],
    row: dict[str, Any],
    result: CostResult,
) -> None:
    """Mutate a cost summary with one estimate_row_cost result (single-pass helper)."""
    if result.missing:
        summary["missing_rows"] = int(summary.get("missing_rows") or 0) + 1
        label = result.raw_model or result.model_key or "unknown"
        missing = summary.setdefault("missing_models", {})
        entry = missing.setdefault(label, {"events": 0, "model_key": result.model_key})
        entry["events"] = int(entry.get("events") or 0) + 1
        return
    summary["priced_rows"] = int(summary.get("priced_rows") or 0) + 1
    summary["total_usd"] = float(summary.get("total_usd") or 0.0) + result.usd
    tool = row.get("tool") or "unknown"
    by_tool = summary.setdefault("by_tool", {})
    by_tool[tool] = float(by_tool.get(tool) or 0.0) + result.usd
    by_model = summary.setdefault("by_model", {})
    by_model[result.model_key] = float(by_model.get(result.model_key) or 0.0) + result.usd
    by_source = summary.setdefault("by_source", {})
    by_source[result.source] = float(by_source.get(result.source) or 0.0) + result.usd
    components_total = summary.setdefault("components", {})
    for key, value in result.components.items():
        if key == "cost_usd_ticks":
            continue
        components_total[key] = float(components_total.get(key) or 0.0) + value


def summarize_costs(rows: list[dict[str, Any]], table: PricingTable | None = None) -> dict[str, Any]:
    table = table or PricingTable()
    summary = empty_cost_summary()
    for row in rows:
        apply_cost_result(summary, row, estimate_row_cost(row, table))
    return summary


def rates_catalog() -> dict[str, dict[str, Any]]:
    return {key: asdict(value) for key, value in DEFAULT_RATES.items()}
