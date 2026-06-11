#!/usr/bin/env python3
"""Claude Code + Codex token usage parser.

Aggregation notes:
- Claude Code: sum assistant message usage, deduplicated by requestId.
- Codex: sum event_msg.token_count.info.last_token_usage.
- The primary "effective" total excludes cache-read/cached-input tokens because
  those can make local context throughput look much larger than uncached usage.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import shutil
import sys
import unicodedata
from collections import defaultdict
from pathlib import Path


HOME = Path.home()
CLAUDE_PROJECTS_DIR = HOME / ".claude" / "projects"
CODEX_SESSIONS_DIR = HOME / ".codex" / "sessions"
LOCAL_TZ = dt.datetime.now().astimezone().tzinfo or dt.timezone.utc


def parse_ts(value):
    if value is None:
        return None
    try:
        if isinstance(value, (int, float)):
            seconds = value / 1000 if value > 10**12 else value
            return dt.datetime.fromtimestamp(seconds, tz=LOCAL_TZ)
        if isinstance(value, str):
            if value.endswith("Z"):
                parsed = dt.datetime.fromisoformat(value[:-1] + "+00:00")
            else:
                parsed = dt.datetime.fromisoformat(value)
            if parsed.tzinfo is None:
                parsed = parsed.replace(tzinfo=LOCAL_TZ)
            return parsed.astimezone(LOCAL_TZ)
    except (OSError, ValueError, TypeError):
        return None
    return None


def date_range(args):
    if args.all_time:
        return None, None, "전체 기간"
    if args.date:
        start = dt.datetime.strptime(args.date, "%Y-%m-%d").replace(tzinfo=LOCAL_TZ)
        end = start + dt.timedelta(days=1)
        label = args.date
    else:
        now = dt.datetime.now(tz=LOCAL_TZ)
        today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        start = today - dt.timedelta(days=args.days - 1)
        end = now
        label = start.strftime("%Y-%m-%d") if args.days == 1 else f"{start:%Y-%m-%d} ~ {now:%Y-%m-%d}"
    return start, end, label


def in_range(timestamp, start, end):
    if timestamp is None:
        return False
    if start is None and end is None:
        return True
    return start <= timestamp < end


def path_matches(project: str, filter_path: str) -> bool:
    if not project or not filter_path:
        return False
    project = project.rstrip("/")
    filter_path = filter_path.rstrip("/")
    if project == str(HOME):
        return False
    return project.startswith(filter_path) or filter_path.startswith(project)


def shorten_home(path: str) -> str:
    return path.replace(str(HOME), "~") if path else "(unknown)"


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


def add_claude_usage(totals, usage):
    input_tokens = int(usage.get("input_tokens") or 0)
    output_tokens = int(usage.get("output_tokens") or 0)
    cache_create = int(usage.get("cache_creation_input_tokens") or 0)
    cache_read = int(usage.get("cache_read_input_tokens") or 0)
    totals["input_tokens"] += input_tokens
    totals["output_tokens"] += output_tokens
    totals["cache_creation_input_tokens"] += cache_create
    totals["cache_read_input_tokens"] += cache_read
    totals["total_tokens"] += input_tokens + output_tokens + cache_create + cache_read
    totals["effective_tokens"] += input_tokens + output_tokens + cache_create
    totals["cache_tokens"] += cache_read
    totals["calls"] += 1


def add_codex_usage(totals, usage):
    input_tokens = int(usage.get("input_tokens") or 0)
    cached_input = int(usage.get("cached_input_tokens") or 0)
    output_tokens = int(usage.get("output_tokens") or 0)
    reasoning_output = int(usage.get("reasoning_output_tokens") or 0)
    total_tokens = int(usage.get("total_tokens") or (input_tokens + output_tokens))
    totals["input_tokens"] += input_tokens
    totals["cached_input_tokens"] += cached_input
    totals["output_tokens"] += output_tokens
    totals["reasoning_output_tokens"] += reasoning_output
    totals["total_tokens"] += total_tokens
    totals["effective_tokens"] += max(0, input_tokens - cached_input) + output_tokens
    totals["cache_tokens"] += cached_input
    totals["calls"] += 1


def is_subagent_path(path: Path) -> bool:
    return "/subagents/" in str(path)


def collect_claude_rows(start, end, args):
    rows_by_request = {}
    if not CLAUDE_PROJECTS_DIR.exists():
        return []

    for path in CLAUDE_PROJECTS_DIR.rglob("*.jsonl"):
        if args.main_only and is_subagent_path(path):
            continue
        try:
            fh = path.open(encoding="utf-8")
        except OSError:
            continue
        with fh:
            for line_no, line in enumerate(fh, 1):
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if entry.get("type") != "assistant":
                    continue
                message = entry.get("message") or {}
                usage = message.get("usage") or {}
                if not usage:
                    continue
                timestamp = parse_ts(entry.get("timestamp"))
                if not in_range(timestamp, start, end):
                    continue
                cwd = entry.get("cwd") or ""
                if args.cwd and not path_matches(cwd, str(Path.cwd())):
                    continue
                if args.project and args.project not in cwd:
                    continue

                request_id = entry.get("requestId") or message.get("id") or f"{path}:{line_no}"
                row = {
                    "tool": "claude",
                    "timestamp": timestamp.isoformat(),
                    "session_id": entry.get("sessionId") or path.stem,
                    "cwd": cwd,
                    "path": str(path),
                    "model": message.get("model") or "",
                    "subagent": is_subagent_path(path) or bool(entry.get("isSidechain")) or bool(entry.get("attributionAgent")),
                    "input_tokens": int(usage.get("input_tokens") or 0),
                    "output_tokens": int(usage.get("output_tokens") or 0),
                    "cache_creation_input_tokens": int(usage.get("cache_creation_input_tokens") or 0),
                    "cache_read_input_tokens": int(usage.get("cache_read_input_tokens") or 0),
                }
                row["total_tokens"] = (
                    row["input_tokens"]
                    + row["output_tokens"]
                    + row["cache_creation_input_tokens"]
                    + row["cache_read_input_tokens"]
                )
                old = rows_by_request.get(request_id)
                if old is None or row["total_tokens"] > old["total_tokens"]:
                    rows_by_request[request_id] = row

    return list(rows_by_request.values())


def read_codex_meta(path: Path):
    try:
        with path.open(encoding="utf-8") as fh:
            for line in fh:
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if entry.get("type") == "session_meta":
                    return entry.get("payload") or {}
    except OSError:
        return {}
    return {}


def collect_codex_rows(start, end, args):
    rows = []
    if not CODEX_SESSIONS_DIR.exists():
        return rows

    for path in CODEX_SESSIONS_DIR.rglob("rollout-*.jsonl"):
        meta = read_codex_meta(path)
        cwd = meta.get("cwd") or ""
        source = meta.get("source")
        subagent = (
            meta.get("originator") == "codex_exec"
            or source == "exec"
            or (isinstance(source, dict) and "subagent" in source)
        )
        if args.main_only and subagent:
            continue
        if args.cwd and not path_matches(cwd, str(Path.cwd())):
            continue
        if args.project and args.project not in cwd:
            continue

        try:
            fh = path.open(encoding="utf-8")
        except OSError:
            continue
        with fh:
            for line in fh:
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if entry.get("type") != "event_msg":
                    continue
                payload = entry.get("payload") or {}
                if payload.get("type") != "token_count":
                    continue
                timestamp = parse_ts(entry.get("timestamp"))
                if not in_range(timestamp, start, end):
                    continue
                info = payload.get("info") or {}
                usage = info.get("last_token_usage") or {}
                if not usage:
                    continue
                row = {
                    "tool": "codex",
                    "timestamp": timestamp.isoformat(),
                    "session_id": meta.get("id") or path.stem,
                    "cwd": cwd,
                    "path": str(path),
                    "model": meta.get("model_provider") or "",
                    "subagent": subagent,
                    "input_tokens": int(usage.get("input_tokens") or 0),
                    "cached_input_tokens": int(usage.get("cached_input_tokens") or 0),
                    "output_tokens": int(usage.get("output_tokens") or 0),
                    "reasoning_output_tokens": int(usage.get("reasoning_output_tokens") or 0),
                    "total_tokens": int(usage.get("total_tokens") or 0),
                }
                if not row["total_tokens"]:
                    row["total_tokens"] = row["input_tokens"] + row["output_tokens"]
                rows.append(row)

    return rows


def summarize(rows):
    by_tool = defaultdict(empty_totals)
    by_cwd = defaultdict(empty_totals)
    by_session = defaultdict(empty_totals)
    session_meta = {}

    for row in rows:
        tool = row["tool"]
        if tool == "claude":
            add_claude_usage(by_tool[tool], row)
            add_claude_usage(by_cwd[(tool, row["cwd"])], row)
            add_claude_usage(by_session[(tool, row["session_id"])], row)
        else:
            add_codex_usage(by_tool[tool], row)
            add_codex_usage(by_cwd[(tool, row["cwd"])], row)
            add_codex_usage(by_session[(tool, row["session_id"])], row)
        session_meta[(tool, row["session_id"])] = {
            "cwd": row["cwd"],
            "path": row["path"],
            "subagent": row["subagent"],
        }

    total = sum(t["total_tokens"] for t in by_tool.values())
    effective_total = sum(t["effective_tokens"] for t in by_tool.values())
    return {
        "total_tokens": total,
        "effective_tokens": effective_total,
        "by_tool": {tool: dict(values) for tool, values in by_tool.items()},
        "by_cwd": {f"{tool}\t{cwd}": dict(values) for (tool, cwd), values in by_cwd.items()},
        "by_session": {f"{tool}\t{sid}": dict(values) for (tool, sid), values in by_session.items()},
        "session_meta": {f"{tool}\t{sid}": meta for (tool, sid), meta in session_meta.items()},
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


def format_text(summary, rows, label, args):
    terminal_width = shutil.get_terminal_size((120, 20)).columns
    total_tokens = summary["total_tokens"]
    effective_total = summary.get("effective_tokens", total_tokens)
    first_seen, last_seen = observed_period(rows)
    lines = []
    filters = []
    if args.cwd:
        filters.append(f"cwd={Path.cwd()}")
    if args.project:
        filters.append(f"project~={args.project}")
    if args.main_only:
        filters.append("main-only")

    panel_lines = [
        f"합계  {fmt_int(effective_total)} tokens  ({fmt_compact_tokens(effective_total)}, 캐시 제외)",
        f"시작  {first_seen.strftime('%Y-%m-%d') if first_seen else '-'}",
        f"최근  {last_seen.strftime('%Y-%m-%d %H:%M') if last_seen else '-'}",
        f"로그  {fmt_int(len(rows))} events",
    ]
    if filters:
        panel_lines.append("필터  " + ", ".join(filters))
    lines.append(make_panel(f"토큰 사용량 · {label}", panel_lines))
    lines.append("")

    tool_rows = []
    for tool in ("claude", "codex"):
        values = summary["by_tool"].get(tool, {})
        if not values:
            continue
        tokens = values.get("effective_tokens", values.get("total_tokens", 0))
        share = f"{(tokens / effective_total * 100):.1f}%" if effective_total else "0.0%"
        if tool == "claude":
            detail = (
                f"in {fmt_compact_tokens(values.get('input_tokens', 0))}, "
                f"out {fmt_compact_tokens(values.get('output_tokens', 0))}, "
                f"cache_create {fmt_compact_tokens(values.get('cache_creation_input_tokens', 0))}"
            )
        else:
            detail = (
                f"uncached_in {fmt_compact_tokens(max(0, values.get('input_tokens', 0) - values.get('cached_input_tokens', 0)))}, "
                f"out {fmt_compact_tokens(values.get('output_tokens', 0))}"
            )
        tool_rows.append([
            "Claude Code" if tool == "claude" else "Codex",
            f"{fmt_int(tokens)} ({fmt_compact_tokens(tokens)})",
            token_bar(tokens, effective_total),
            share,
            fmt_int(values.get("calls", 0)),
            detail,
        ])
    if tool_rows:
        lines.append(style("도구별", "1;37"))
        lines.append(make_table(
            ["도구", "토큰", "비중", "%", "호출", "구성"],
            tool_rows,
            ["left", "right", "left", "right", "right", "left"],
        ))

    lines.append("")
    lines.append(style("프로젝트별 상위", "1;37"))
    by_cwd = []
    for key, values in summary["by_cwd"].items():
        tool, cwd = key.split("\t", 1)
        by_cwd.append((values.get("effective_tokens", values.get("total_tokens", 0)), tool, cwd, values))
    project_rows = []
    fixed_width = 5 + 8 + 21 + 20 + 8 + 15
    project_width = max(28, min(70, terminal_width - fixed_width))
    for rank, (total, tool, cwd, values) in enumerate(sorted(by_cwd, reverse=True)[: args.limit], 1):
        label_name = "Claude" if tool == "claude" else "Codex"
        share = f"{(total / effective_total * 100):.1f}%" if effective_total else "0.0%"
        project_rows.append([
            str(rank),
            label_name,
            f"{fmt_compact_tokens(total)}",
            token_bar(total, effective_total, width=14),
            share,
            fmt_int(values.get("calls", 0)),
            trim_to_width(shorten_home(cwd), project_width),
        ])
    lines.append(make_table(
        ["#", "도구", "토큰", "비중", "%", "호출", "프로젝트"],
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
            by_session.append((values.get("effective_tokens", values.get("total_tokens", 0)), tool, sid, values, meta))
        session_rows = []
        session_project_width = max(24, min(56, terminal_width - fixed_width))
        for rank, (total, tool, sid, values, meta) in enumerate(sorted(by_session, reverse=True)[: args.limit], 1):
            label_name = "Claude" if tool == "claude" else "Codex"
            session_id = sid[:12] + ("*" if meta.get("subagent") else "")
            share = f"{(total / effective_total * 100):.1f}%" if effective_total else "0.0%"
            session_rows.append([
                str(rank),
                label_name,
                session_id,
                f"{fmt_compact_tokens(total)}",
                token_bar(total, effective_total, width=14),
                share,
                fmt_int(values.get("calls", 0)),
                trim_to_width(shorten_home(meta.get("cwd", "")), session_project_width),
            ])
        lines.append(make_table(
            ["#", "도구", "세션", "토큰", "비중", "%", "호출", "프로젝트"],
            session_rows,
            ["right", "left", "left", "right", "left", "right", "right", "left"],
        ))
        if any(meta.get("subagent") for meta in summary["session_meta"].values()):
            lines.append("* 세션 ID 뒤의 * 표시는 subagent/sidechain입니다.")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Parse Claude Code + Codex token usage from local JSONL logs.")
    parser.add_argument("--date", help="조회할 날짜 (YYYY-MM-DD)")
    parser.add_argument("--days", type=int, default=1, help="최근 N일 (기본: 1)")
    parser.add_argument("--all-time", action="store_true", help="날짜 필터 없이 로컬에 남은 전체 로그 집계")
    parser.add_argument("--tool", choices=["all", "claude", "codex"], default="all")
    parser.add_argument("--cwd", action="store_true", help="현재 작업 디렉토리 기준 프로젝트 필터")
    parser.add_argument("--project", help="프로젝트 경로 문자열 필터")
    parser.add_argument("--main-only", action="store_true", help="Claude/Codex subagent 세션 제외")
    parser.add_argument("--by-session", action="store_true", help="세션별 상위 사용량 표시")
    parser.add_argument("--limit", type=int, default=10, help="표시할 상위 항목 수 (기본: 10)")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args()

    start, end, label = date_range(args)
    rows = []
    if args.tool in ("all", "claude"):
        rows.extend(collect_claude_rows(start, end, args))
    if args.tool in ("all", "codex"):
        rows.extend(collect_codex_rows(start, end, args))

    summary = summarize(rows)
    if args.format == "json":
        out = {
            "range": {
                "start": start.isoformat() if start else None,
                "end": end.isoformat() if end else None,
                "label": label,
            },
            "summary": summary,
            "rows": rows,
        }
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print(format_text(summary, rows, label, args))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(130)
