#!/usr/bin/env python3
"""Claude Code + Codex + Grok token usage parser.

Aggregation notes:
- Claude Code: sum assistant message usage, deduplicated by requestId.
- Codex: sum event_msg.token_count.info.last_token_usage.
- Grok: sum updates.jsonl turn_completed usage (per user turn).
- The primary "pure" total excludes cache read, cached input, and Claude/Grok
  cache creation tokens. "effective" is kept as a secondary metric for cache-read
  excluded usage that still includes cache creation.
- --cost: API-equivalent USD (rate card, or Grok costUsdTicks when present).
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path

_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from adapters import ADAPTERS, ORDER, iter_adapters  # noqa: E402
from common import (  # noqa: E402
    date_range_dt,
    parse_ts,
    shorten_home,
)
from pricing import (  # noqa: E402
    PricingTable,
    apply_cost_result,
    empty_cost_summary,
    estimate_row_cost,
    is_non_model_id,
    load_pricing_overrides,
    resolve_model_key,
)


def fmt_int(value: int) -> str:
    return f"{value:,}"


def fmt_compact_tokens(value: int) -> str:
    if value >= 100_000_000:
        return f"{value / 100_000_000:.1f}억"
    if value >= 1_000_000:
        return f"{value / 1_000_000:.1f}M"
    if value >= 1_000:
        return f"{value / 1_000:.1f}K"
    return str(value)


def fmt_usd(value: float) -> str:
    if value >= 1000:
        return f"${value:,.0f}"
    if value >= 10:
        return f"${value:,.2f}"
    if value >= 0.01:
        return f"${value:,.3f}"
    if value > 0:
        return f"${value:,.4f}"
    return "$0"


def display_width(text) -> int:
    width = 0
    for char in str(text):
        if unicodedata.combining(char):
            continue
        width += 2 if unicodedata.east_asian_width(char) in ("F", "W") else 1
    return width


def trim_to_width(text, max_width: int) -> str:
    text = str(text)
    if display_width(text) <= max_width:
        return text
    if max_width <= 1:
        return "…"[:max_width]
    out = []
    width = 0
    for char in text:
        char_width = 2 if unicodedata.east_asian_width(char) in ("F", "W") else 1
        if width + char_width > max_width - 1:
            break
        out.append(char)
        width += char_width
    return "".join(out) + "…"


def pad_cell(text, width: int, align: str = "left") -> str:
    text = trim_to_width(text, width)
    gap = width - display_width(text)
    if align == "right":
        return " " * gap + text
    if align == "center":
        left = gap // 2
        return " " * left + text + " " * (gap - left)
    return text + " " * gap


def supports_color() -> bool:
    return sys.stdout.isatty() and os.environ.get("NO_COLOR") is None and os.environ.get("TERM") != "dumb"


COLOR_ENABLED = supports_color()


def style(text: str, code: str) -> str:
    if not COLOR_ENABLED:
        return text
    return f"\033[{code}m{text}\033[0m"


def token_bar(value: int, total: int, width: int = 18) -> str:
    if total <= 0:
        filled = 0
    else:
        filled = round((value / total) * width)
    filled = max(0, min(width, filled))
    return style("█" * filled, "36") + style("░" * (width - filled), "90")


def make_table(headers, rows, aligns=None):
    if not rows:
        return "(없음)"
    aligns = aligns or ["left"] * len(headers)
    widths = [display_width(header) for header in headers]
    for row in rows:
        for idx, cell in enumerate(row):
            widths[idx] = max(widths[idx], display_width(cell))

    top = "┌" + "┬".join("─" * (width + 2) for width in widths) + "┐"
    sep = "├" + "┼".join("─" * (width + 2) for width in widths) + "┤"
    bottom = "└" + "┴".join("─" * (width + 2) for width in widths) + "┘"
    header = "│ " + " │ ".join(pad_cell(h, widths[i], "center") for i, h in enumerate(headers)) + " │"
    body = [
        "│ " + " │ ".join(pad_cell(cell, widths[i], aligns[i]) for i, cell in enumerate(row)) + " │"
        for row in rows
    ]
    return "\n".join([top, header, sep, *body, bottom])


def make_panel(title: str, lines):
    content_width = max([display_width(title), *(display_width(line) for line in lines)], default=0)
    content_width = min(max(content_width, 42), max(42, shutil.get_terminal_size((120, 20)).columns - 4))
    title_text = f" {title} "
    top = "╭" + title_text + "─" * max(0, content_width + 2 - display_width(title_text)) + "╮"
    body = ["│ " + pad_cell(line, content_width, "left") + " │" for line in lines]
    bottom = "╰" + "─" * (content_width + 2) + "╯"
    return "\n".join([top, *body, bottom])


def empty_totals():
    return defaultdict(int)


def collect_rows(tool_filter: str, start, end, args):
    rows = []
    for adapter in iter_adapters(tool_filter):
        rows.extend(adapter.collect_token_rows(start, end, args))
    return rows


def model_display(tool: str, model_raw: str) -> tuple[str, str, str]:
    """Return (display_label, canonical_key, resolve_source)."""
    model_key, src = resolve_model_key(model_raw, tool)
    if is_non_model_id(model_raw):
        if src == "default":
            return f"(default:{model_key})", model_key, src
        return "(unknown)", model_key, src
    if src == "unknown":
        return f"{model_raw} (unpriced)", model_key, src
    if model_raw:
        return model_raw, model_key, src
    return f"(default:{model_key})", model_key, src


def summarize(rows, pricing_table: PricingTable | None = None):
    """One pass over rows: token rollups + optional cost summary."""
    by_tool = defaultdict(empty_totals)
    by_cwd = defaultdict(empty_totals)
    by_session = defaultdict(empty_totals)
    by_model = defaultdict(empty_totals)
    cost_by_model_display: dict[str, float] = defaultdict(float)
    unpriced_by_model_display: dict[str, int] = defaultdict(int)
    session_meta = {}
    cost_summary = empty_cost_summary() if pricing_table is not None else None

    for row in rows:
        tool = row["tool"]
        adapter = ADAPTERS.get(tool)
        if not adapter:
            continue
        adder = adapter.add_token_usage
        adder(by_tool[tool], row)
        adder(by_cwd[(tool, row["cwd"])], row)
        adder(by_session[(tool, row["session_id"])], row)
        model_raw = row.get("model") or ""
        display_model, model_key, _src = model_display(tool, model_raw)
        adder(by_model[(tool, display_model, model_key)], row)
        if pricing_table is not None and cost_summary is not None:
            result = estimate_row_cost(row, pricing_table)
            apply_cost_result(cost_summary, row, result)
            display_key = f"{tool}\t{display_model}"
            if result.missing:
                unpriced_by_model_display[display_key] += 1
            else:
                cost_by_model_display[display_key] += result.usd
        session_meta[(tool, row["session_id"])] = {
            "cwd": row["cwd"],
            "path": row["path"],
            "subagent": row["subagent"],
            "model": model_raw,
        }

    total = sum(t["total_tokens"] for t in by_tool.values())
    effective_total = sum(t["effective_tokens"] for t in by_tool.values())
    pure_total = sum(t["pure_tokens"] for t in by_tool.values())
    return {
        "total_tokens": total,
        "effective_tokens": effective_total,
        "pure_tokens": pure_total,
        "by_tool": {tool: dict(values) for tool, values in by_tool.items()},
        "by_cwd": {f"{tool}\t{cwd}": dict(values) for (tool, cwd), values in by_cwd.items()},
        "by_session": {f"{tool}\t{sid}": dict(values) for (tool, sid), values in by_session.items()},
        "by_model": {
            f"{tool}\t{display}\t{key}": dict(values)
            for (tool, display, key), values in by_model.items()
        },
        "cost_by_model_display": dict(cost_by_model_display),
        "unpriced_by_model_display": dict(unpriced_by_model_display),
        "session_meta": {f"{tool}\t{sid}": meta for (tool, sid), meta in session_meta.items()},
        "cost": cost_summary,
    }


def observed_period(rows):
    timestamps = []
    for row in rows:
        timestamp = parse_ts(row.get("timestamp"))
        if timestamp:
            timestamps.append(timestamp)
    if not timestamps:
        return None, None
    return min(timestamps), max(timestamps)


def tool_detail(tool: str, values) -> str:
    if tool == "claude":
        c5 = values.get("cache_creation_5m_tokens", 0)
        c1 = values.get("cache_creation_1h_tokens", 0)
        split = ""
        if c5 or c1:
            split = f", 5m {fmt_compact_tokens(c5)}/1h {fmt_compact_tokens(c1)}"
        return (
            f"in {fmt_compact_tokens(values.get('input_tokens', 0))}, "
            f"out {fmt_compact_tokens(values.get('output_tokens', 0))}, "
            f"cache_create {fmt_compact_tokens(values.get('cache_creation_input_tokens', 0))}"
            f"{split}"
        )
    if tool == "grok":
        cost = values.get("cost_usd")
        cost_s = f", ~{fmt_usd(float(cost))}" if cost else ""
        return (
            f"uncached_in {fmt_compact_tokens(max(0, values.get('input_tokens', 0) - values.get('cached_read_tokens', 0)))}, "
            f"out {fmt_compact_tokens(values.get('output_tokens', 0))}, "
            f"reason {fmt_compact_tokens(values.get('reasoning_tokens', 0))}"
            f"{cost_s}"
        )
    return (
        f"uncached_in {fmt_compact_tokens(max(0, values.get('input_tokens', 0) - values.get('cached_input_tokens', 0)))}, "
        f"out {fmt_compact_tokens(values.get('output_tokens', 0))}"
    )


def format_quota_section(quotas) -> str:
    lines = [style("구독 한도 (live)", "1;37")]
    rows = []
    for q in quotas:
        tool = q.get("tool", "?")
        short = getattr(ADAPTERS.get(tool), "SHORT", tool)
        if not q.get("ok"):
            rows.append([short, "—", q.get("error") or "error", ""])
            continue
        plan = q.get("plan") or ""
        windows = q.get("windows") or []
        if not windows:
            rows.append([short, plan or "—", "(window 없음)", ""])
            continue
        for i, w in enumerate(windows):
            label = w.get("label") or "?"
            pct = w.get("used_percent")
            pct_s = f"{pct:.1f}%" if isinstance(pct, (int, float)) else "—"
            reset = w.get("resets_at")
            if isinstance(reset, (int, float)) and reset > 1_000_000_000_000:
                # ms
                ts = parse_ts(reset)
                reset_s = ts.strftime("%m-%d %H:%M") if ts else ""
            elif isinstance(reset, (int, float)) and reset > 1_000_000_000:
                ts = parse_ts(reset)  # seconds handled in parse_ts
                reset_s = ts.strftime("%m-%d %H:%M") if ts else ""
            elif isinstance(reset, str):
                ts = parse_ts(reset)
                reset_s = ts.strftime("%m-%d %H:%M") if ts else reset[:16]
            else:
                reset_s = ""
            rows.append([
                short if i == 0 else "",
                plan if i == 0 else "",
                f"{label} {pct_s}",
                reset_s,
            ])
    lines.append(make_table(
        ["도구", "플랜", "사용률", "리셋"],
        rows,
        ["left", "left", "left", "left"],
    ))
    return "\n".join(lines)


def format_text(summary, rows, label, args, cost_summary=None, quotas=None):
    terminal_width = shutil.get_terminal_size((120, 20)).columns
    total_tokens = summary["total_tokens"]
    effective_total = summary.get("effective_tokens", total_tokens)
    pure_total = summary.get("pure_tokens", effective_total)
    first_seen, last_seen = observed_period(rows)
    lines = []
    filters = []
    if args.cwd:
        filters.append(f"cwd={Path.cwd()}")
    if args.project:
        filters.append(f"project~={args.project}")
    if args.main_only:
        filters.append("main-only")
    if getattr(args, "month", None):
        filters.append(f"month={args.month if args.month not in (True, 'current', '') else label}")

    panel_lines = [
        f"실사용  {fmt_int(pure_total)} tokens  ({fmt_compact_tokens(pure_total)}, 캐시 읽기/생성 제외)",
        f"캐시생성포함  {fmt_int(effective_total)} tokens  ({fmt_compact_tokens(effective_total)}, 캐시 읽기 제외)",
        f"전체처리량  {fmt_int(total_tokens)} tokens  ({fmt_compact_tokens(total_tokens)}, 캐시 포함)",
        f"시작  {first_seen.strftime('%Y-%m-%d') if first_seen else '-'}",
        f"최근  {last_seen.strftime('%Y-%m-%d %H:%M') if last_seen else '-'}",
        f"로그  {fmt_int(len(rows))} events",
    ]
    if cost_summary is not None:
        panel_lines.insert(
            0,
            f"API환산  {fmt_usd(cost_summary['total_usd'])}  "
            f"(priced {fmt_int(cost_summary['priced_rows'])} / missing {fmt_int(cost_summary['missing_rows'])})",
        )
        sources = cost_summary.get("by_source") or {}
        if sources:
            src = ", ".join(f"{k} {fmt_usd(v)}" for k, v in sorted(sources.items(), key=lambda x: -x[1]))
            panel_lines.insert(1, f"비용출처  {src}")
    if filters:
        panel_lines.append("필터  " + ", ".join(filters))
    lines.append(make_panel(f"토큰 사용량 · {label}", panel_lines))
    lines.append("")

    if quotas is not None:
        lines.append(format_quota_section(quotas))
        lines.append("")

    tool_rows = []
    for tool in ORDER:
        values = summary["by_tool"].get(tool, {})
        if not values:
            continue
        adapter = ADAPTERS[tool]
        tokens = values.get("pure_tokens", values.get("effective_tokens", values.get("total_tokens", 0)))
        share = f"{(tokens / pure_total * 100):.1f}%" if pure_total else "0.0%"
        cost_cell = ""
        if cost_summary is not None:
            cost_cell = fmt_usd(cost_summary.get("by_tool", {}).get(tool, 0.0))
        row = [
            adapter.DISPLAY,
            f"{fmt_int(tokens)} ({fmt_compact_tokens(tokens)})",
            token_bar(tokens, pure_total),
            share,
            fmt_int(values.get("calls", 0)),
            tool_detail(tool, values),
        ]
        headers = ["도구", "실사용", "비중", "%", "호출", "구성"]
        aligns = ["left", "right", "left", "right", "right", "left"]
        if cost_summary is not None:
            row.insert(2, cost_cell)
            headers.insert(2, "API$")
            aligns.insert(2, "right")
        tool_rows.append(row)
    if tool_rows:
        lines.append(style("도구별", "1;37"))
        # rebuild with consistent headers from first branch
        if cost_summary is not None:
            headers = ["도구", "실사용", "API$", "비중", "%", "호출", "구성"]
            aligns = ["left", "right", "right", "left", "right", "right", "left"]
        else:
            headers = ["도구", "실사용", "비중", "%", "호출", "구성"]
            aligns = ["left", "right", "left", "right", "right", "left"]
        lines.append(make_table(headers, tool_rows, aligns))

    if args.by_model or (cost_summary is not None and args.cost):
        lines.append("")
        lines.append(style("모델별 상위", "1;37"))
        model_items = []
        cost_by_display = summary.get("cost_by_model_display") or {}
        unpriced_by_display = summary.get("unpriced_by_model_display") or {}
        for key, values in summary.get("by_model", {}).items():
            parts = key.split("\t")
            tool = parts[0] if parts else ""
            display = parts[1] if len(parts) > 1 else ""
            model_key = parts[2] if len(parts) > 2 else display
            tokens = values.get("pure_tokens", values.get("effective_tokens", values.get("total_tokens", 0)))
            display_key = f"{tool}\t{display}"
            unpriced_n = int(unpriced_by_display.get(display_key, 0) or 0)
            usd = float(cost_by_display.get(display_key, 0.0)) if cost_summary is not None else 0.0
            model_items.append((tokens, usd, unpriced_n, tool, display, model_key, values))
        model_items.sort(
            key=lambda x: (x[1] if cost_summary is not None else x[0]),
            reverse=True,
        )
        model_rows = []
        for rank, (tokens, usd, unpriced_n, tool, display, model_key, values) in enumerate(
            model_items[: args.limit], 1
        ):
            short = getattr(ADAPTERS.get(tool), "SHORT", tool)
            share = f"{(tokens / pure_total * 100):.1f}%" if pure_total else "0.0%"
            row = [
                str(rank),
                short,
                trim_to_width(display or model_key, 32),
                fmt_compact_tokens(tokens),
                share,
                fmt_int(values.get("calls", 0)),
            ]
            if cost_summary is not None:
                if unpriced_n and usd <= 0:
                    cost_cell = "unpriced"
                else:
                    cost_cell = fmt_usd(usd)
                row.insert(4, cost_cell)
            model_rows.append(row)
        if cost_summary is not None:
            lines.append(make_table(
                ["#", "도구", "모델", "실사용", "API$", "%", "호출"],
                model_rows,
                ["right", "left", "left", "right", "right", "right", "right"],
            ))
        else:
            lines.append(make_table(
                ["#", "도구", "모델", "실사용", "%", "호출"],
                model_rows,
                ["right", "left", "left", "right", "right", "right"],
            ))
        if cost_summary and cost_summary.get("missing_rows"):
            missing = cost_summary.get("missing_models") or {}
            top_missing = sorted(
                missing.items(),
                key=lambda kv: int((kv[1] or {}).get("events") or 0),
                reverse=True,
            )[:5]
            names = ", ".join(
                f"{name}×{int((info or {}).get('events') or 0)}" for name, info in top_missing
            )
            detail = f": {names}" if names else ""
            lines.append(
                f"※ 단가 미매칭 {fmt_int(cost_summary['missing_rows'])} events"
                f"{detail}. 합계에 미포함. --pricing-file 로 보강 가능."
            )

    lines.append("")
    lines.append(style("프로젝트별 상위", "1;37"))
    by_cwd = []
    for key, values in summary["by_cwd"].items():
        tool, cwd = key.split("\t", 1)
        by_cwd.append((
            values.get("pure_tokens", values.get("effective_tokens", values.get("total_tokens", 0))),
            tool,
            cwd,
            values,
        ))
    project_rows = []
    fixed_width = 5 + 8 + 21 + 20 + 8 + 15
    project_width = max(28, min(70, terminal_width - fixed_width))
    for rank, (total, tool, cwd, values) in enumerate(sorted(by_cwd, reverse=True)[: args.limit], 1):
        short = getattr(ADAPTERS.get(tool), "SHORT", tool)
        share = f"{(total / pure_total * 100):.1f}%" if pure_total else "0.0%"
        project_rows.append([
            str(rank),
            short,
            f"{fmt_compact_tokens(total)}",
            token_bar(total, pure_total, width=14),
            share,
            fmt_int(values.get("calls", 0)),
            trim_to_width(shorten_home(cwd), project_width),
        ])
    lines.append(make_table(
        ["#", "도구", "실사용", "비중", "%", "호출", "프로젝트"],
        project_rows,
        ["right", "left", "right", "left", "right", "right", "left"],
    ))

    if args.by_session:
        lines.append("")
        lines.append(style("세션별 상위", "1;37"))
        by_session = []
        for key, values in summary["by_session"].items():
            tool, sid = key.split("\t", 1)
            meta = summary["session_meta"].get(key, {})
            by_session.append((
                values.get("pure_tokens", values.get("effective_tokens", values.get("total_tokens", 0))),
                tool,
                sid,
                values,
                meta,
            ))
        session_rows = []
        session_project_width = max(24, min(56, terminal_width - fixed_width))
        for rank, (total, tool, sid, values, meta) in enumerate(sorted(by_session, reverse=True)[: args.limit], 1):
            short = getattr(ADAPTERS.get(tool), "SHORT", tool)
            session_id = sid[:12] + ("*" if meta.get("subagent") else "")
            share = f"{(total / pure_total * 100):.1f}%" if pure_total else "0.0%"
            session_rows.append([
                str(rank),
                short,
                session_id,
                f"{fmt_compact_tokens(total)}",
                token_bar(total, pure_total, width=14),
                share,
                fmt_int(values.get("calls", 0)),
                trim_to_width(shorten_home(meta.get("cwd", "")), session_project_width),
            ])
        lines.append(make_table(
            ["#", "도구", "세션", "실사용", "비중", "%", "호출", "프로젝트"],
            session_rows,
            ["right", "left", "left", "right", "left", "right", "right", "left"],
        ))
        if any(meta.get("subagent") for meta in summary["session_meta"].values()):
            lines.append("* 세션 ID 뒤의 * 표시는 subagent/sidechain입니다.")

    if cost_summary is not None:
        lines.append("")
        lines.append(
            "API 환산은 구독 청구서가 아니라 같은 토큰을 list API 단가로 환산한 대체비용입니다. "
            "Grok은 costUsdTicks가 있으면 공급자 집계를 우선합니다."
        )

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Parse Claude Code + Codex + Grok token usage from local logs.")
    parser.add_argument("--date", help="조회할 날짜 (YYYY-MM-DD)")
    parser.add_argument("--days", type=int, default=1, help="최근 N일 (기본: 1)")
    parser.add_argument(
        "--month",
        nargs="?",
        const="current",
        help="달력 월 집계 (YYYY-MM, 생략 시 이번 달). --days/--date 대신 사용",
    )
    parser.add_argument("--all-time", action="store_true", help="날짜 필터 없이 로컬에 남은 전체 로그 집계")
    parser.add_argument("--tool", choices=["all", "claude", "codex", "grok"], default="all")
    parser.add_argument("--cwd", action="store_true", help="현재 작업 디렉토리 기준 프로젝트 필터")
    parser.add_argument("--project", help="프로젝트 경로 문자열 필터")
    parser.add_argument("--main-only", action="store_true", help="Claude/Codex subagent 세션 제외")
    parser.add_argument("--by-session", action="store_true", help="세션별 상위 사용량 표시")
    parser.add_argument("--by-model", action="store_true", help="모델별 상위 사용량 표시")
    parser.add_argument(
        "--cost",
        action="store_true",
        help="API 환산 비용($) 표시. Grok costUsdTicks 우선, 그 외 단가표",
    )
    parser.add_argument(
        "--quota",
        action="store_true",
        help="구독 한도 live 조회 (Claude OAuth usage + Codex wham)",
    )
    parser.add_argument(
        "--pricing-file",
        help="단가 오버라이드 JSON (또는 env SESSION_HISTORY_PRICING)",
    )
    parser.add_argument("--limit", type=int, default=10, help="표시할 상위 항목 수 (기본: 10)")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args()

    start, end, label = date_range_dt(args)
    rows = collect_rows(args.tool, start, end, args)

    pricing_table = None
    if args.cost:
        overrides = load_pricing_overrides(args.pricing_file)
        pricing_table = PricingTable(overrides)

    # Single pass: token rollups + cost (when --cost).
    summary = summarize(rows, pricing_table=pricing_table)
    cost_summary = summary.get("cost") if args.cost else None

    quotas = None
    if args.quota:
        from quota import fetch_quotas

        quotas = fetch_quotas(args.tool)

    if args.format == "json":
        out_summary = {k: v for k, v in summary.items() if k != "cost"}
        out = {
            "range": {
                "start": start.isoformat() if start else None,
                "end": end.isoformat() if end else None,
                "label": label,
            },
            "summary": out_summary,
            "rows": rows,
        }
        if args.cost:
            out["cost"] = cost_summary
        if args.quota:
            out["quota"] = quotas
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print(format_text(summary, rows, label, args, cost_summary=cost_summary, quotas=quotas))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(130)
