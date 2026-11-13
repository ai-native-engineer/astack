#!/usr/bin/env python3
"""Pick the cheapest usable worker model for a harness. Effort is not chosen
here; leave it at the harness default.

Run it; do not read it for the algorithm. `--help` is the interface.

Availability comes from the harness itself (what it can actually spawn today),
price comes from models.dev (the public model DB opencode uses). Nothing here
hard-codes a model name, so a new model release changes the answer without a
code change.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

MODELS_DEV_URL = "https://models.dev/api.json"
CACHE_DIR = (
    Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache")) / "agent-team"
)
CACHE_FILE = CACHE_DIR / "models-dev.json"
# models.dev updates a few times a week; prices change far less often. One day
# keeps the hook path offline-fast without serving a stale price for long.
CACHE_TTL_SEC = 24 * 3600
# A research worker reads far more than it writes. 4:1 input:output matches the
# token_usage ratios seen in this user's delegated research sessions.
OUTPUT_WEIGHT = 0.25
# A reader needs room for several files plus search results; 200k is the
# smallest window the current frontier harnesses ship, so anything below it
# is a legacy model, not a bargain.
DEFAULT_MIN_CONTEXT = 200_000
# "Cheapest" means cheapest of the current generation, never a two-generation-old
# small model. Labs ship a generation's tiers within about half a year of each
# other, so a family whose newest release trails the provider's newest by more
# than this is treated as last generation.
DEFAULT_GENERATION_DAYS = 180
HARNESSES = ("claude", "codex", "opencode", "agy", "omp")


def load_models_dev(refresh: bool) -> tuple[dict, str]:
    """Return (data, source). Falls back to any cache when offline."""
    fresh = (
        CACHE_FILE.exists()
        and (time.time() - CACHE_FILE.stat().st_mtime) < CACHE_TTL_SEC
    )
    if fresh and not refresh:
        return json.loads(CACHE_FILE.read_text()), f"cache {CACHE_FILE}"
    try:
        with urllib.request.urlopen(MODELS_DEV_URL, timeout=60) as resp:
            raw = resp.read()
        data = json.loads(raw)
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        tmp = CACHE_FILE.with_suffix(".tmp")
        tmp.write_bytes(raw)
        tmp.replace(CACHE_FILE)
        return data, MODELS_DEV_URL
    except Exception as exc:
        if CACHE_FILE.exists():
            return json.loads(
                CACHE_FILE.read_text()
            ), f"stale cache {CACHE_FILE} ({exc})"
        raise SystemExit(f"models.dev를 받지 못했고 캐시도 없다: {exc}") from exc


# First-party providers price their own models; resellers (bedrock, copilot,
# openrouter) relist them, sometimes at different prices. Index these first so a
# bare model id resolves to the vendor's own price.
CANONICAL_PROVIDERS = ("anthropic", "openai", "google", "xai", "deepseek", "moonshotai")


def price_index(data: dict) -> dict[str, dict]:
    """model id -> record, merged across providers (canonical provider wins)."""
    idx: dict[str, dict] = {}
    order = [p for p in CANONICAL_PROVIDERS if p in data] + [
        p for p in data if p not in CANONICAL_PROVIDERS
    ]
    for provider in order:
        pdata = data[provider]
        for mid, m in (pdata.get("models") or {}).items():
            cost = m.get("cost") or {}
            if cost.get("input") is None or cost.get("output") is None:
                continue
            if (m.get("type") or "chat") not in ("chat", None):
                continue
            rec = dict(m)
            rec["provider"] = provider
            idx.setdefault(mid, rec)
            idx.setdefault(f"{provider}/{mid}", rec)
    return idx


def score(rec: dict) -> float:
    cost = rec["cost"]
    return float(cost["input"]) + OUTPUT_WEIGHT * float(cost["output"])


def usable(
    rec: dict, min_context: int, allow_free: bool = False, any_lab: bool = False
) -> str | None:
    """Return a reason the model is unusable for a research worker, else None."""
    if rec.get("status") == "deprecated":
        return "deprecated"
    # Cheapest is not cost-effective when the worker cannot follow a research
    # brief. Price alone cannot judge quality, so the floor is "made by a
    # frontier lab" (the record's own vendor, whatever reseller route lists it).
    if not any_lab and rec["provider"] not in CANONICAL_PROVIDERS:
        return f"{rec['provider']} 모델, --any-lab로만 허용"
    # $0 in models.dev means a free tier or a bundled/proxy listing, not a
    # priced model; free tiers are rate-limited and unreliable for batch workers.
    if (
        not allow_free
        and float(rec["cost"]["input"]) == 0
        and float(rec["cost"]["output"]) == 0
    ):
        return "free tier ($0), --allow-free로만 허용"
    if rec.get("tool_call") is False:
        return "no tool calls"
    ctx = (rec.get("limit") or {}).get("context") or 0
    if ctx < min_context:
        return f"context {ctx} < {min_context}"
    return None


def run(cmd: list[str]) -> str:
    exe = shutil.which(cmd[0])
    if not exe:
        raise SystemExit(
            f"`{cmd[0]}`를 PATH에서 찾지 못했다. 그 하네스가 설치된 셸에서 실행하거나 --available로 목록을 넘긴다."
        )
    return subprocess.run(
        [exe, *cmd[1:]], capture_output=True, text=True, timeout=30, check=False
    ).stdout


# --- availability per harness -------------------------------------------------


def available_claude(idx: dict) -> list[tuple[str, dict]]:
    """Claude Code's Agent tool takes family aliases (haiku/sonnet/opus/...), not
    IDs. An alias resolves to the family's newest model, so the candidate set is
    each anthropic family's newest release and the alias is the family name
    without the `claude-` prefix."""
    best: dict[str, dict] = {}
    for mid, rec in idx.items():
        if "/" in mid or rec["provider"] != "anthropic":
            continue
        fam = rec.get("family") or ""
        if not fam.startswith("claude-"):
            continue
        if fam not in best or (rec.get("release_date") or "") > (
            best[fam].get("release_date") or ""
        ):
            best[fam] = rec
    return [(fam.removeprefix("claude-"), rec) for fam, rec in best.items()]


def resolve_alias(harness: str, value: str, idx: dict) -> dict | None:
    """`--available haiku` style aliases: map a Claude family alias to its
    cheapest current model."""
    if harness == "claude":
        for alias, rec in available_claude(idx):
            if alias == value:
                return rec
    return None


def available_codex(idx: dict) -> list[tuple[str, dict]]:
    """Codex's catalog for the logged-in account is `~/.codex/models_cache.json`.
    A proxy profile (codex-proxy) launches with `-c model_catalog_json=<file>`
    of the same shape; export that path as CODEX_MODEL_CATALOG_JSON so the pick
    matches what that session can actually spawn. Inside such a session the
    `spawn_agent` tool description lists the overrides: pass them via
    `--available` when the env var is not set."""
    override = os.environ.get("CODEX_MODEL_CATALOG_JSON")
    home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
    cache = Path(override) if override else home / "models_cache.json"
    if not cache.exists():
        raise SystemExit(
            f"{cache} 가 없다. Codex를 한 번 실행해 모델 목록을 받게 하거나, "
            "spawn_agent 설명의 모델 목록을 --available로 넘긴다."
        )
    out = []
    for m in json.loads(cache.read_text()).get("models", []):
        if m.get("visibility") != "list":
            continue
        slug = m["slug"]
        out.append((slug, idx.get(slug) or idx.get(f"openai/{slug}")))
    return out


def opencode_providers() -> set[str] | None:
    """Providers with stored credentials; None when unknown (no filter)."""
    auth = (
        Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local/share"))
        / "opencode"
        / "auth.json"
    )
    if not auth.exists():
        return None
    return set(json.loads(auth.read_text()).keys())


def available_opencode(idx: dict) -> list[tuple[str, dict]]:
    """`opencode models` lists every known provider/model; keep only providers
    opencode holds credentials for, otherwise the pick cannot actually run."""
    allowed = opencode_providers()
    out = []
    for line in run(["opencode", "models"]).splitlines():
        line = line.strip()
        if not line or "/" not in line:
            continue
        provider, mid = line.split("/", 1)
        if allowed is not None and provider not in allowed:
            continue
        out.append((line, idx.get(line) or idx.get(mid)))
    return out


def available_agy(idx: dict) -> list[tuple[str, dict]]:
    """`agy models` prints `<model>-<effort>\\t<label>`; strip the effort suffix
    to find the price, keep the full ID as the value to pass."""
    out = []
    for line in run(["agy", "models"]).splitlines():
        if not line.strip():
            continue
        mid = line.split("\t", 1)[0].strip()
        base = re.sub(r"-(low|medium|high|xhigh|max)$", "", mid)
        out.append((mid, idx.get(base)))
    return out


def available_omp(idx: dict) -> list[tuple[str, dict]]:
    """Read the native catalog only; require an explicit provider route."""
    provider = os.environ.get("OMP_WORKER_PROVIDER")
    if not provider or not re.fullmatch(r"[A-Za-z0-9_.-]+", provider):
        raise SystemExit("OMP_WORKER_PROVIDER must name the existing configured CLIProxyAPI provider.")
    try:
        data = json.loads(run(["omp", "models", provider, "--json", "--no-extensions"]))
    except (ValueError, TypeError):
        raise SystemExit("OMP model catalog is not valid JSON; no route was selected.") from None
    if not isinstance(data, dict) or not isinstance(data.get("models"), list):
        raise SystemExit("OMP model catalog has no models array; no route was selected.")
    result = []
    for model in data["models"]:
        if not isinstance(model, dict) or model.get("provider") != provider:
            continue
        mid, selector = model.get("id"), model.get("selector")
        if not isinstance(mid, str) or selector != f"{provider}/{mid}":
            continue
        result.append((selector, idx.get(selector) or idx.get(mid)))
    return result


AVAILABILITY = {
    "claude": available_claude,
    "codex": available_codex,
    "opencode": available_opencode,
    "agy": available_agy,
    "omp": available_omp,
}


def detect_harness() -> str | None:
    if os.environ.get("CLAUDE_CODE_ENTRYPOINT") or os.environ.get("CLAUDECODE"):
        return "claude"
    if os.environ.get("CODEX_THREAD_ID") or os.environ.get("CODEX_SANDBOX"):
        return "codex"
    return None


# Effort stays at the harness default; this script only picks the model. agy is
# the exception because effort is baked into its model IDs, so a price tie among
# `<model>-<effort>` variants goes to medium (the neutral middle: not lowered,
# not extra spend), then high, then low.
EFFORT_RANK = {"medium": 0, "high": 1, "low": 2, "xhigh": 3, "max": 4, "ultra": 5}


def effort_rank(value: str) -> int:
    m = re.search(r"-(low|medium|high|xhigh|max|ultra)$", value)
    return EFFORT_RANK[m.group(1)] if m else 0


def days_between(newer: str, older: str) -> int:
    from datetime import date

    y1, m1, d1 = (int(x) for x in newer.split("-"))
    y2, m2, d2 = (int(x) for x in older.split("-"))
    return (date(y1, m1, d1) - date(y2, m2, d2)).days


def same_generation(
    cands: list[tuple[str, dict]], generation_days: int
) -> tuple[list[tuple[str, dict]], list[dict]]:
    """Keep each (provider, family)'s newest release, then drop families that
    trail their provider's newest release by more than `generation_days`."""
    newest_in_family: dict[tuple[str, str], str] = {}
    newest_in_provider: dict[str, str] = {}
    for _, rec in cands:
        if not rec or not rec.get("release_date"):
            continue
        key = (rec["provider"], rec.get("family") or rec.get("id"))
        rd = rec["release_date"]
        newest_in_family[key] = max(newest_in_family.get(key, ""), rd)
        newest_in_provider[rec["provider"]] = max(
            newest_in_provider.get(rec["provider"], ""), rd
        )
    kept, skipped = [], []
    for value, rec in cands:
        if not rec or not rec.get("release_date"):
            kept.append((value, rec))
            continue
        key = (rec["provider"], rec.get("family") or rec.get("id"))
        rd = rec["release_date"]
        if rd < newest_in_family[key]:
            skipped.append(
                {
                    "model": value,
                    "reason": f"같은 계열에 더 새 모델 있음 ({newest_in_family[key]})",
                }
            )
            continue
        lag = days_between(newest_in_provider[rec["provider"]], rd)
        if lag > generation_days:
            skipped.append(
                {"model": value, "reason": f"이전 세대: 공급자 최신보다 {lag}일 오래됨"}
            )
            continue
        kept.append((value, rec))
    return kept, skipped


def pick(
    harness: str,
    idx: dict,
    min_context: int,
    available_override: list[str] | None,
    allow_free: bool = False,
    any_lab: bool = False,
    generation_days: int = DEFAULT_GENERATION_DAYS,
):
    if available_override:
        cands = [
            (a, idx.get(a) or resolve_alias(harness, a, idx))
            for a in available_override
        ]
    else:
        cands = AVAILABILITY[harness](idx)
    cands, skipped = same_generation(cands, generation_days)
    rows = []
    for value, rec in cands:
        if rec is None:
            skipped.append({"model": value, "reason": "models.dev에 가격 없음"})
            continue
        why = usable(rec, min_context, allow_free, any_lab)
        if why:
            skipped.append({"model": value, "reason": why})
            continue
        row = {
            "model": value,
            "id": rec.get("id"),
            "provider": rec["provider"],
            "input_per_m": rec["cost"]["input"],
            "output_per_m": rec["cost"]["output"],
            "score": round(score(rec), 4),
            "context": (rec.get("limit") or {}).get("context"),
            "release_date": rec.get("release_date"),
        }
        rows.append(row)
    rows.sort(key=lambda r: (r["score"], effort_rank(r["model"]), -(r["context"] or 0)))
    return rows, skipped


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description="하네스가 지금 띄울 수 있는 모델 중 읽기 전용 worker에 가장 싼 모델을 고른다.",
        epilog="score = 입력 $/M + 0.25 × 출력 $/M. 같은 세대만 비교한다: 계열마다 최신 출시만 남기고, 공급자 최신보다 --generation-days 이상 오래된 계열은 뺀다. deprecated, tool call 불가, 컨텍스트 부족, $0 무료 티어, 인증 없는 공급자, 프론티어 랩 밖 모델도 기본으로 뺀다.",
    )
    p.add_argument("--harness", choices=HARNESSES, help="생략하면 환경변수로 감지한다")
    p.add_argument(
        "--available",
        help="하네스 조회 대신 쓸 후보 목록(쉼표 구분). 도구 스키마의 enum을 그대로 넘길 때 쓴다",
    )
    p.add_argument("--min-context", type=int, default=DEFAULT_MIN_CONTEXT)
    p.add_argument(
        "--generation-days",
        type=int,
        default=DEFAULT_GENERATION_DAYS,
        help="공급자 최신 출시보다 이만큼 오래된 계열은 이전 세대로 본다",
    )
    p.add_argument(
        "--allow-free", action="store_true", help="$0(무료 티어) 모델도 후보에 넣는다"
    )
    p.add_argument(
        "--any-lab",
        action="store_true",
        help="프론티어 랩(anthropic, openai, google, xai, deepseek, moonshotai) 밖 모델도 후보에 넣는다",
    )
    p.add_argument(
        "--refresh", action="store_true", help="models.dev를 지금 다시 받는다"
    )
    p.add_argument("--format", choices=("text", "json"), default="text")
    p.add_argument("--all", action="store_true", help="후보 전체와 제외 사유까지 출력")
    a = p.parse_args(argv)

    harness = a.harness or detect_harness()
    if not harness:
        p.error("--harness를 알 수 없다. 환경변수에서 감지되지 않으니 직접 넘긴다.")
    data, source = load_models_dev(a.refresh)
    idx = price_index(data)
    rows, skipped = pick(
        harness,
        idx,
        a.min_context,
        a.available.split(",") if a.available else None,
        a.allow_free,
        a.any_lab,
        a.generation_days,
    )
    if not rows:
        print(
            json.dumps(
                {
                    "harness": harness,
                    "error": "쓸 수 있는 후보가 없다",
                    "skipped": skipped,
                },
                ensure_ascii=False,
            ),
            file=sys.stderr,
        )
        return 1
    best = rows[0]
    result = {
        "harness": harness,
        "model": best["model"],
        "price_source": source,
        "best": best,
    }
    if a.all:
        result["candidates"] = rows
        result["skipped"] = skipped
    if a.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=1))
        return 0
    print(
        f"{harness}: {best['model']}  (${best['input_per_m']}/M in, ${best['output_per_m']}/M out, ctx {best['context']}; {source})"
    )
    if a.all:
        for r in rows[1:]:
            print(
                f"  next: {r['model']}  ${r['input_per_m']}/{r['output_per_m']}  score {r['score']}"
            )
        for s in skipped:
            print(f"  skip: {s['model']}  {s['reason']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
