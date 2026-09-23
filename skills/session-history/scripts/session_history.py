#!/usr/bin/env python3
"""로컬 AI agent 통합 세션 히스토리.

Subcommands:
    list      세션 목록 조회 (기본)
    show      특정 세션의 전체 대화 내역 보기
    timeline  오늘 작업 시간순 타임라인 (데일리 노트용)
    rg        세션 전문 검색 (preview 아닌 실제 대화·도구 기록)
    sources   감지된 로컬 로그 소스와 세션 수
    redact    로그 파일에 남은 시크릿을 실제로 지움

Usage:
    python3 session_history.py                              # 오늘 세션 목록
    python3 session_history.py list --cwd                   # 현재 디렉토리 프로젝트만
    python3 session_history.py list --tool grok             # Grok 세션만
    python3 session_history.py list --search pytest         # 키워드 검색
    python3 session_history.py timeline                     # 오늘 타임라인
    python3 session_history.py rg "gcloud"                  # 대화·도구 기록 검색
    python3 session_history.py show --last                  # 가장 최근 세션
    python3 session_history.py show abc123 --full           # 도구 호출 포함
    python3 session_history.py show abc123 --limit 20       # 앞 20개만
    python3 session_history.py sources                      # 감지된 로그 소스
"""

from __future__ import annotations

import argparse
import datetime
import json
import re
import sys
import tarfile
from collections import defaultdict
from pathlib import Path

# Allow `python3 scripts/session_history.py` without package install.
_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from adapters import ADAPTERS, ORDER, iter_adapters  # noqa: E402
from common import (  # noqa: E402
    date_range,
    set_include_subagents,
    shorten_home,
    ts_to_hm,
    ts_to_hms,
)


def collect_history(
    tool_filter: str, start_ms, end_ms, project_filter=None, cwd_filter=None
):
    sessions = {}
    for adapter in iter_adapters(tool_filter):
        sessions.update(
            adapter.extract_history(start_ms, end_ms, project_filter, cwd_filter)
        )
    return sessions


def adapter_session_path(adapter, session_id: str):
    try:
        return adapter.find_session_file(session_id)
    except (OSError, KeyError):
        return None


def collect_sources(tool_filter: str = "all"):
    sources = []
    for adapter in iter_adapters(tool_filter):
        try:
            count = len(adapter.session_index())
            error = ""
        except OSError as exc:
            count = 0
            error = str(exc)
        roots = []
        for path in getattr(adapter, "SOURCE_PATHS", ()):
            path = Path(path)
            roots.append(
                {
                    "path": str(path),
                    "exists": path.exists(),
                }
            )
        notes_fn = getattr(adapter, "source_notes", None)
        try:
            notes = list(notes_fn()) if notes_fn else []
        except OSError:
            notes = []
        sources.append(
            {
                "tool": adapter.TOOL,
                "display": adapter.DISPLAY,
                "sessions": count,
                "available": any(root["exists"] for root in roots),
                "roots": roots,
                "notes": notes,
                "error": error,
            }
        )
    return sources


def format_sources_text(sources):
    lines = ["# 로컬 AI 세션 소스", ""]
    for source in sources:
        status = "감지됨" if source["available"] else "없음"
        lines.append(f"## {source['display']} - {source['sessions']}개 세션 ({status})")
        for root in source["roots"]:
            marker = "[ok]" if root["exists"] else "[-]"
            lines.append(f"  {marker} {shorten_home(root['path'])}")
        for note in source.get("notes") or []:
            lines.append(f"  · {note}")
        if source["error"]:
            lines.append(f"  오류: {source['error']}")
        lines.append("")
    lines.append(
        "`list`, `timeline`, `rg`, `show`의 기본 `--tool all`은 위 소스를 함께 조회합니다."
    )
    return "\n".join(lines)


# 값의 모양만으로 시크릿이라고 단정할 수 있는 패턴. 화면과 디스크 양쪽에 쓴다
_SHAPE_PATTERNS = (
    (re.compile(r"\bsk-ant-[A-Za-z0-9_-]{10,}\b"), "[REDACTED_ANTHROPIC_KEY]"),
    (re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"), "[REDACTED_API_KEY]"),
    (
        re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{20,}\b"),
        "[REDACTED_GITHUB_TOKEN]",
    ),
    (re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b"), "[REDACTED_GITHUB_TOKEN]"),
    (re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b"), "[REDACTED_AWS_ACCESS_KEY]"),
    (re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b"), "[REDACTED_SLACK_TOKEN]"),
    (re.compile(r"\bntn_[A-Za-z0-9_]{20,}\b"), "[REDACTED_NOTION_TOKEN]"),
    (re.compile(r"\bAIza[A-Za-z0-9_-]{35}\b"), "[REDACTED_GOOGLE_API_KEY]"),
    # `<uuid>:<32 hex>` 한 덩어리. fal이 이 모양을 쓰고, 앞뒤로 키 이름이 없어
    # key=value 패턴에도 안 걸린다
    (
        re.compile(
            r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}:[0-9a-f]{32}\b"
        ),
        "[REDACTED_FAL_KEY]",
    ),
    # 밑줄형 `sk_`. 하이픈을 쓰는 위의 `sk-`와 서로 안 걸친다
    (re.compile(r"\bsk_[0-9a-f]{32,}\b"), "[REDACTED_API_KEY]"),
    (
        re.compile(
            r"\beyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b"
        ),
        "[REDACTED_JWT]",
    ),
    (
        re.compile(r"\b(Bearer\s+)[A-Za-z0-9._~+/-]{32,}", re.IGNORECASE),
        r"\1[REDACTED]",
    ),
)

# 값이 아니라 옆에 붙은 이름을 보고 찍는 휴리스틱. `token=3`이나 `api_key=None`
# 같은 코드 예시까지 걸려 화면 출력에만 쓴다 - 가려서 손해가 없는 쪽이다
_CONTEXT_PATTERNS = (
    (
        re.compile(
            r"([\"']?(?:password|passwd|pwd|api[_-]?key|token|secret|client[_-]?secret)[\"']?\s*[:=]\s*)(?:\"[^\"]*\"|'[^']*'|[^\s,;)\]]+)",
            re.IGNORECASE,
        ),
        r"\1[REDACTED]",
    ),
    (
        re.compile(r"\b(Bearer\s+)[A-Za-z0-9._~+/-]{12,}", re.IGNORECASE),
        r"\1[REDACTED]",
    ),
)

_SECRET_PATTERNS = _SHAPE_PATTERNS + _CONTEXT_PATTERNS


def redact_sensitive_text(text: str) -> str:
    """화면에 찍기 전에 쓴다. 넓게 잡는다 - 과하게 가려도 손해가 없다."""
    for pattern, replacement in _SECRET_PATTERNS:
        text = pattern.sub(replacement, text)
    return text


def redact_shapes_only(text: str) -> str:
    """파일을 되돌릴 수 없게 고치기 전에 쓴다. 모양이 확실한 것만 지운다.

    화면용 휴리스틱을 그대로 쓰면 `token=3` 같은 멀쩡한 기록까지 덮어써
    로그를 훼손한다. 지우는 쪽에서는 놓치는 것보다 부수는 것이 더 비싸다.
    """
    for pattern, replacement in _SHAPE_PATTERNS:
        text = pattern.sub(replacement, text)
    return text


def emit(text: str, args=None) -> None:
    """출력 직전에 한 번 가리고 찍는다. `--raw`면 원문 그대로 간다.

    필드마다 가리면 출력 경로를 하나 늘릴 때마다 빠뜨리는 자리가 생긴다.
    여기 한 곳을 지나게 해야 어느 서브커맨드로 나가든 같은 기준이 걸린다.
    JSON도 이 게이트를 지난다 - 치환값에 따옴표와 역슬래시가 없어 구조가 깨지지 않는다.
    """
    if not getattr(args, "raw", False):
        text = redact_sensitive_text(text)
    print(text)


def short_id_width(session_ids, minimum: int = 12) -> int:
    """목록 안에서 서로 구분되는 최소 ID 길이. opencode의 `ses_` 접두사처럼
    공통 머리가 길면 12자리로는 다른 세션이 같아 보인다."""
    ids = list(session_ids)
    width = minimum
    longest = max((len(sid) for sid in ids), default=minimum)
    while width < longest:
        if len({sid[:width] for sid in ids}) == len(set(ids)):
            break
        width += 1
    return width


def summarize_sessions(sessions, date_label):
    counts = {tool: 0 for tool in ORDER}
    projects = defaultdict(int)
    for info in sessions.values():
        tool = info.get("tool")
        counts[tool] = counts.get(tool, 0) + 1
        project = shorten_home(info.get("project", ""))
        projects[project] += 1

    top_projects = sorted(projects.items(), key=lambda item: (-item[1], item[0]))[:10]
    return {
        "range": date_label,
        "total": len(sessions),
        "tools": {tool: counts[tool] for tool in ORDER},
        "projects": [
            {"project": project, "sessions": count} for project, count in top_projects
        ],
    }


def format_list_summary(sessions, date_label):
    summary = summarize_sessions(sessions, date_label)
    lines = [
        f"# 세션 히스토리 요약 ({date_label})",
        "",
        f"총 {summary['total']}개 세션",
    ]
    for tool in ORDER:
        lines.append(f"- {ADAPTERS[tool].DISPLAY}: {summary['tools'][tool]}")
    if summary["projects"]:
        lines.extend(["", "## 상위 프로젝트"])
        lines.extend(
            f"- {item['project']}: {item['sessions']}" for item in summary["projects"]
        )
    lines.extend(["", "세부 목록: python3 session_history.py list --days <N>"])
    return "\n".join(lines)


def format_list_text(sessions, date_label):
    lines = [f"# 세션 히스토리 ({date_label})", ""]
    if not sessions:
        lines.append("세션 기록 없음.")
        return "\n".join(lines)

    counts = {}
    for tool in ORDER:
        adapter = ADAPTERS[tool]
        tool_sessions = {k: v for k, v in sessions.items() if v.get("tool") == tool}
        counts[tool] = len(tool_sessions)
        if not tool_sessions:
            continue
        lines.append(f"## {adapter.DISPLAY} ({len(tool_sessions)}개 세션)")
        lines.append("")
        sorted_items = sorted(
            tool_sessions.items(), key=lambda kv: kv[1].get("first_ts_ms", 0)
        )
        width = short_id_width(tool_sessions)
        for sid, info in sorted_items:
            proj = shorten_home(info["project"])
            label = info.get("name") or (info.get("provider") and f"provider={info['provider']}") or ""
            msg_count = len(info["messages"])
            if not info["messages"]:
                lines.append(f"  {sid[:width]}  {proj}  {label}  (메시지 없음)")
            else:
                first = info["messages"][0]["time"]
                last = info["messages"][-1]["time"]
                first_msg = info["messages"][0]["text"].replace("\n", " ")[:80]
                lines.append(
                    f"  {sid[:width]}  {proj}  {label}  {first}~{last}  ({msg_count}건)  {first_msg}"
                )
            fpath = adapter_session_path(adapter, sid)
            if fpath:
                lines.append(f"    └ {fpath}")
        lines.append("")

    count_text = ", ".join(
        f"{ADAPTERS[tool].DISPLAY}: {counts.get(tool, 0)}" for tool in ORDER
    )
    lines.append(f"총 {len(sessions)}개 세션 ({count_text})")
    lines.append("")
    lines.append("대화 보기: python3 session_history.py show <세션ID 앞 12자리 이상>")
    lines.append("최근 세션: python3 session_history.py show --last")
    return "\n".join(lines)


def cmd_list(args):
    start_ms, end_ms, label = date_range(args)
    cwd_filter = str(Path.cwd()) if getattr(args, "cwd", False) else None
    sessions = collect_history(args.tool, start_ms, end_ms, args.project, cwd_filter)

    if getattr(args, "search", None):
        keyword = args.search.lower()
        sessions = {
            sid: info
            for sid, info in sessions.items()
            if keyword in info.get("name", "").lower()
            or keyword in info.get("provider", "").lower()
            or any(keyword in m["text"].lower() for m in info["messages"])
        }

    if getattr(args, "summary", False):
        summary = summarize_sessions(sessions, label)
        emit(
            json.dumps(summary, ensure_ascii=False, indent=2)
            if args.format == "json"
            else format_list_summary(sessions, label),
            args,
        )
    elif args.format == "json":
        emit(json.dumps(sessions, ensure_ascii=False, indent=2), args)
    else:
        emit(format_list_text(sessions, label), args)


def cmd_sources(args):
    sources = collect_sources(args.tool)
    if args.format == "json":
        emit(json.dumps(sources, ensure_ascii=False, indent=2), args)
    else:
        emit(format_sources_text(sources), args)


def cmd_timeline(args):
    start_ms, end_ms, label = date_range(args)
    cwd_filter = str(Path.cwd()) if getattr(args, "cwd", False) else None
    sessions = collect_history(args.tool, start_ms, end_ms, cwd_filter=cwd_filter)

    if not sessions:
        emit(f"세션 없음 ({label})", args)
        return

    sorted_sessions = sorted(
        sessions.items(), key=lambda kv: kv[1].get("first_ts_ms", 0)
    )

    if args.format == "json":
        tl_width = short_id_width(sessions)
        out = [
            {
                "sid": sid[:tl_width],
                "tool": info["tool"],
                "project": info["project"],
                "time": ts_to_hm(info["first_ts_ms"]) if info["first_ts_ms"] else "",
                "first_msg": info["messages"][0]["text"] if info["messages"] else "",
                "msg_count": len(info["messages"]),
            }
            for sid, info in sorted_sessions
        ]
        emit(json.dumps(out, ensure_ascii=False, indent=2), args)
        return

    lines = [f"# 작업 타임라인 ({label})", ""]
    by_date = defaultdict(list)
    for sid, info in sorted_sessions:
        if info["first_ts_ms"]:
            day = datetime.datetime.fromtimestamp(info["first_ts_ms"] / 1000).strftime(
                "%Y-%m-%d"
            )
        else:
            day = "unknown"
        by_date[day].append((sid, info))

    for day in sorted(by_date.keys()):
        if len(by_date) > 1:
            lines.append(f"## {day}")
            lines.append("")
        for sid, info in by_date[day]:
            time_str = ts_to_hm(info["first_ts_ms"]) if info["first_ts_ms"] else "??"
            proj = info["project"].split("/")[-1] if info["project"] else "(root)"
            tool_tag = ADAPTERS[info["tool"]].TAG if info["tool"] in ADAPTERS else "[?]"
            msg_count = len(info["messages"])
            first_msg = (
                info["messages"][0]["text"].replace("\n", " ")[:100]
                if info["messages"]
                else "(메시지 없음)"
            )
            lines.append(
                f"{time_str}  {tool_tag} [{proj}]  {first_msg}  ({msg_count}건)"
            )
            if msg_count >= 5 and not getattr(args, "compact", False):
                mid = info["messages"][msg_count // 2]
                mid_text = mid["text"].replace("\n", " ")[:80]
                lines.append(f"       ↳ {mid['time']}  {mid_text}")
        lines.append("")

    lines.append(f"총 {len(sorted_sessions)}개 세션")
    lines.append(
        "  ".join(f"{ADAPTERS[tool].TAG}={ADAPTERS[tool].DISPLAY}" for tool in ORDER)
    )
    emit("\n".join(lines), args)


def cmd_grep(args):
    keyword = args.keyword
    start_ms, end_ms, label = date_range(args)
    cwd_filter = str(Path.cwd()) if getattr(args, "cwd", False) else None
    sessions = collect_history(args.tool, start_ms, end_ms, cwd_filter=cwd_filter)

    results = []
    ordered_sessions = sorted(
        sessions.items(), key=lambda item: item[1].get("first_ts_ms", 0)
    )
    result_limit = getattr(args, "limit", None)
    for sid, info in ordered_sessions:
        if result_limit is not None and 0 <= result_limit <= len(results):
            break
        tool = info["tool"]
        adapter = ADAPTERS.get(tool)
        if not adapter:
            continue
        fpath = adapter_session_path(adapter, sid)
        if not fpath or not Path(fpath).exists():
            continue
        try:
            hits = adapter.grep_session(fpath, keyword, session_id=sid)
        except OSError:
            continue
        if hits:
            results.append(
                {
                    "sid": sid,
                    "tool": tool,
                    "project": info["project"],
                    "first_ts_ms": info.get("first_ts_ms", 0),
                    "hits": hits,
                    "fpath": fpath,
                }
            )
    if result_limit is not None:
        results = results[:result_limit]

    if args.format == "json":
        out = [{**r, "fpath": str(r["fpath"]), "sid": r["sid"]} for r in results]
        emit(json.dumps(out, ensure_ascii=False, indent=2), args)
        return

    command_label = "rg" if getattr(args, "command", "") == "rg" else "grep"
    lines = [f'# {command_label}: "{keyword}" ({label})', ""]
    if not results:
        lines.append("매칭 없음.")
        emit("\n".join(lines), args)
        return

    lines.append(f"{len(results)}개 세션에서 발견")
    lines.append("─" * 60)

    hit_width = short_id_width(r["sid"] for r in results)
    for r in results:
        proj = shorten_home(r["project"])
        time_str = ts_to_hm(r["first_ts_ms"]) if r["first_ts_ms"] else "??"
        tool_tag = (
            f"[{ADAPTERS[r['tool']].DISPLAY}]"
            if r["tool"] in ADAPTERS
            else f"[{r['tool']}]"
        )
        lines.append(f"\n{tool_tag} {r['sid'][:hit_width]}  {proj}  {time_str}")
        lines.append(f"  파일: {r['fpath']}")
        for hit in r["hits"][:3]:
            role_icon = {"user": "👤", "assistant": "🤖"}.get(hit["role"], "🔧")
            try:
                if isinstance(hit["ts"], str) and hit["ts"]:
                    dt = datetime.datetime.fromisoformat(
                        hit["ts"].replace("Z", "+00:00")
                    )
                    t = dt.strftime("%H:%M:%S")
                elif hit["ts"]:
                    t = ts_to_hms(hit["ts"])
                else:
                    t = ""
            except Exception:
                t = ""
            lines.append(f"  {role_icon} {t}  {hit['excerpt']}")
        if len(r["hits"]) > 3:
            lines.append(f"  ... 외 {len(r['hits']) - 3}건 더")

    lines.append("")
    lines.append("─" * 60)
    lines.append(f"총 {sum(len(r['hits']) for r in results)}건 ({len(results)}개 세션)")
    lines.append("전체 보기: python3 session_history.py show <세션ID>")
    emit("\n".join(lines), args)


def find_session(session_prefix: str, tool_filter: str = "all"):
    results = []
    for adapter in iter_adapters(tool_filter):
        for sid in adapter.session_index():
            if sid.startswith(session_prefix):
                results.append((adapter.TOOL, sid))
    return results


def find_latest_session(tool_filter: str = "all"):
    for days in (1, 7):
        ns = argparse.Namespace(date=None, days=days)
        start_ms, end_ms, _ = date_range(ns)
        sessions = collect_history(tool_filter, start_ms, end_ms)
        if sessions:
            sid = max(sessions.items(), key=lambda kv: kv[1].get("first_ts_ms", 0))[0]
            return sessions[sid]["tool"], sid
    return None, None


def format_conversation(messages, tool_name, session_id, full, fpath=None, limit=None):
    role_labels = {
        "user": "👤 USER",
        "assistant": "🤖 ASSISTANT",
        "tool": "🔧 TOOL RESULT",
        "tool_call": "🔧 TOOL CALL",
        "tool_result": "🔧 TOOL OUTPUT",
    }

    lines = [f"# {tool_name} 세션 대화 ({session_id[:12]}...)", ""]
    if fpath:
        lines.append(f"파일: {fpath}")
        lines.append("")

    if not messages:
        lines.append("(대화 내역 없음)")
        return "\n".join(lines)

    total = len(messages)
    if limit and limit < total:
        messages = messages[:limit]
        truncated = True
    else:
        truncated = False

    mode_label = "전체 (도구 호출 포함)" if full else "대화만"
    count_label = (
        f"{len(messages)}/{total}건 (--limit {limit})" if truncated else f"{total}건"
    )
    lines.append(f"모드: {mode_label} | 메시지 {count_label}")
    lines.append("─" * 60)

    for msg in messages:
        role = msg.get("role", "")
        label = role_labels.get(role, role.upper())
        ts = msg.get("ts", "")

        time_str = ""
        if ts:
            try:
                if isinstance(ts, str):
                    dt = datetime.datetime.fromisoformat(ts.replace("Z", "+00:00"))
                    time_str = dt.strftime("%H:%M:%S")
                else:
                    time_str = datetime.datetime.fromtimestamp(ts / 1000).strftime(
                        "%H:%M:%S"
                    )
            except (ValueError, OSError):
                time_str = str(ts)[:8]

        phase = msg.get("phase", "")
        phase_str = f" ({phase})" if phase else ""
        model = msg.get("model", "")
        model_str = f" [{model}]" if model else ""

        lines.append(f"\n{label}{phase_str}{model_str}  {time_str}")

        text = msg.get("text", "")
        if role in ("tool", "tool_result") and len(text) > 300:
            text = text[:300] + f"\n... ({len(msg.get('text', ''))}자 중 300자 표시)"
        lines.append(text)

    lines.append("")
    lines.append("─" * 60)
    lines.append(f"총 {total}건")
    return "\n".join(lines)


def format_changed_files(changes, bash_hints, tool_name, session_id, fpath=None):
    lines = [f"# {tool_name} 세션 변경 파일 ({session_id[:12]}...)", ""]
    if fpath:
        lines.append(f"파일: {fpath}")
        lines.append("")
    changes = changes or []
    bash_hints = bash_hints or []

    if not changes and not bash_hints:
        lines.append("(변경된 파일 없음)")
        return "\n".join(lines)

    if changes:
        stats = defaultdict(lambda: {"count": 0, "tools": set()})
        for c in changes:
            s = stats[c["file"]]
            s["count"] += 1
            s["tools"].add(c["tool"])
        lines.append(f"## 구조화된 파일 변경 ({len(changes)}건 · 고유 {len(stats)}개)")
        lines.append("─" * 60)
        for path, s in sorted(stats.items(), key=lambda kv: (-kv[1]["count"], kv[0])):
            tools = ",".join(sorted(s["tools"]))
            lines.append(f"  [{tools}] x{s['count']}  {shorten_home(path)}")

    if bash_hints:
        if changes:
            lines.append("")
        lines.append(f"## Bash/shell 변경 의심 ({len(bash_hints)}건)")
        lines.append("─" * 60)
        for h in bash_hints[:20]:
            cmd = h["cmd"].replace("\n", " ⏎ ")
            if len(cmd) > 160:
                cmd = cmd[:160] + "…"
            lines.append(f"  {cmd}")
        if len(bash_hints) > 20:
            lines.append(f"  ... {len(bash_hints) - 20}건 생략")

    return "\n".join(lines)


def cmd_show(args):
    use_last = getattr(args, "last", False)
    session_prefix = getattr(args, "session", None)

    if use_last:
        tool, session_id = find_latest_session(args.tool)
        if not tool:
            print("최근 세션을 찾을 수 없습니다.")
            sys.exit(1)
        matches = [(tool, session_id)]
    else:
        if not session_prefix:
            print("세션 ID 또는 --last 옵션이 필요합니다.")
            sys.exit(1)
        matches = find_session(session_prefix, args.tool)

    if not matches:
        print(f"'{session_prefix}'로 시작하는 세션을 찾을 수 없습니다.")
        sys.exit(1)

    if len(matches) > 1:
        print(f"'{session_prefix}'에 매칭되는 세션이 {len(matches)}개입니다:")
        for tool, sid in matches:
            print(f"  [{tool}] {sid}")
        print("\n더 긴 ID를 입력하거나 --tool 옵션을 사용해 주세요.")
        sys.exit(1)

    tool, session_id = matches[0]
    adapter = ADAPTERS[tool]
    full = args.full
    limit = getattr(args, "limit", None)

    if getattr(args, "files", False):
        changes, bash_hints = adapter.extract_changed_files(session_id)
        fpath = adapter.find_session_file(session_id)
        if changes is None:
            print(f"세션 파일을 찾을 수 없습니다: {session_id}")
            sys.exit(1)
        if args.format == "json":
            emit(
                json.dumps(
                    {"changes": changes, "bash_hints": bash_hints},
                    ensure_ascii=False,
                    indent=2,
                ),
                args,
            )
        else:
            emit(
                format_changed_files(
                    changes, bash_hints, adapter.DISPLAY, session_id, fpath=fpath
                ),
                args,
            )
        return

    messages, fpath = adapter.read_conversation(session_id, full)
    if messages is None:
        print(f"세션 파일을 찾을 수 없습니다: {session_id}")
        sys.exit(1)

    if args.format == "json":
        emit(json.dumps(messages, ensure_ascii=False, indent=2), args)
    else:
        emit(
            format_conversation(
                messages, adapter.DISPLAY, session_id, full, fpath=fpath, limit=limit
            ),
            args,
        )


# 텍스트로 안전하게 다시 쓸 수 있는 로그만 고친다. sqlite 같은 바이너리 저장소를
# 문자열 치환하면 길이가 달라져 파일이 깨진다
_REDACT_SUFFIXES = (".jsonl", ".json", ".txt", ".md", ".log")


def iter_redact_targets(roots):
    for root in roots:
        if root.is_file():
            yield root
        elif root.is_dir():
            for path in root.rglob("*"):
                if path.is_file() and path.suffix in _REDACT_SUFFIXES:
                    yield path


def cmd_redact(args):
    """로그 파일에 남은 시크릿을 실제로 지운다.

    조회 마스킹은 화면만 가리고 디스크에는 원문이 남는다. 키가 실제로 노출돼
    회수해야 할 때 쓴다. 기본은 세기만 하고, `--apply`가 있어야 백업 후 고친다.
    """
    roots = []
    for source in collect_sources(args.tool):
        roots += [Path(r["path"]) for r in source.get("roots") or [] if r.get("exists")]
    roots += [Path(p).expanduser() for p in (args.path or [])]

    exclude = tuple(args.exclude or ())
    targets = list(iter_redact_targets(roots))
    # 로그 저장소는 수만 개까지 간다. 규모를 먼저 알려야 멈춘 것으로 안 보인다
    print(f"대상 {len(targets):,}개 검사 중...", file=sys.stderr)

    scanned = 0
    changed = []
    for path in targets:
        if any(token in str(path) for token in exclude):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        scanned += 1
        masked = redact_shapes_only(text)
        if masked != text:
            changed.append((path, masked))

    print(f"검사 {scanned:,}개 · 시크릿이 남은 파일 {len(changed)}개")
    if not changed:
        return

    if not args.apply:
        for path, _ in changed[:20]:
            print(f"  {path}")
        if len(changed) > 20:
            print(f"  ... 외 {len(changed) - 20}개")
        print("\n실제로 지우려면 --apply를 붙인다. 붙이면 먼저 백업한다")
        return

    stamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = Path(
        args.backup
        or Path.home() / ".local/state/session-history" / f"redact-{stamp}.tar.gz"
    ).expanduser()
    backup.parent.mkdir(parents=True, exist_ok=True)
    with tarfile.open(backup, "w:gz") as tar:
        for path, _ in changed:
            tar.add(path, arcname=str(path).lstrip("/"))

    for path, masked in changed:
        tmp = path.with_suffix(path.suffix + ".tmp")
        tmp.write_text(masked, encoding="utf-8")
        tmp.replace(path)

    print(f"백업: {backup}")
    print(f"치환: {len(changed)}개 파일")
    print(f"되돌리기: tar -xzf {backup} -C /")


def main():
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--tool", choices=["all", *ORDER], default="all")
    common.add_argument("--format", choices=["text", "json"], default="text")
    common.add_argument(
        "--include-subagents",
        action="store_true",
        help="subagent 세션도 포함 (기본: 제외)",
    )
    common.add_argument(
        "--raw",
        action="store_true",
        help="시크릿 마스킹 없이 원문 출력 (기본: 마스킹)",
    )

    parser = argparse.ArgumentParser(
        description="로컬 AI agent 통합 세션 히스토리",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=[common],
        epilog="""
예시:
  %(prog)s                                 오늘 세션 목록
  %(prog)s list --cwd                      현재 디렉토리 프로젝트만
  %(prog)s list --tool grok                Grok 세션만
  %(prog)s list --tool cursor              Cursor 세션만
  %(prog)s list --days 30 --summary        30일 세션 수와 상위 프로젝트 요약
  %(prog)s list --search pytest            키워드 검색 (preview)
  %(prog)s timeline                        오늘 타임라인 (데일리 노트용)
  %(prog)s timeline --days 3 --cwd         현재 프로젝트 3일 타임라인
  %(prog)s rg "gcloud"                     대화·도구 기록 검색
  %(prog)s rg "gcloud" --days 14           14일간 대화·도구 기록 검색
  %(prog)s show --last                     가장 최근 세션
  %(prog)s show abc12345 --files           수정된 파일 목록
  %(prog)s show abc12345 --limit 20        앞 20개 메시지만
  %(prog)s show --last --raw               마스킹 없이 원문 (기본은 마스킹)
  %(prog)s sources                         감지된 로컬 로그 소스와 세션 수
  %(prog)s redact                          로그에 남은 시크릿 세기
  %(prog)s redact --apply                  백업 후 실제로 지우기
""",
    )

    subparsers = parser.add_subparsers(dest="command")

    list_parser = subparsers.add_parser("list", help="세션 목록 조회", parents=[common])
    list_parser.add_argument("--date", help="조회할 날짜 (YYYY-MM-DD)")
    list_parser.add_argument("--days", type=int, default=1, help="최근 N일 (기본: 1)")
    list_parser.add_argument("--project", help="특정 프로젝트 경로 필터")
    list_parser.add_argument(
        "--cwd", action="store_true", help="현재 작업 디렉토리 기준으로 프로젝트 필터"
    )
    list_parser.add_argument(
        "--search", help="메시지 텍스트 키워드 필터 (preview 기준)"
    )
    list_parser.add_argument(
        "--summary",
        action="store_true",
        help="메시지 미리보기 없이 도구별 수와 상위 프로젝트만 출력",
    )

    tl_parser = subparsers.add_parser(
        "timeline", help="오늘 작업 시간순 타임라인", parents=[common]
    )
    tl_parser.add_argument("--date", help="조회할 날짜 (YYYY-MM-DD)")
    tl_parser.add_argument("--days", type=int, default=1, help="최근 N일 (기본: 1)")
    tl_parser.add_argument(
        "--cwd", action="store_true", help="현재 디렉토리 프로젝트만"
    )
    tl_parser.add_argument("--compact", action="store_true", help="중간 스냅샷 생략")

    grep_parser = subparsers.add_parser(
        "grep", aliases=["rg"], help="세션 전문 검색 (대화·도구 기록)", parents=[common]
    )
    grep_parser.add_argument("keyword", help="검색할 키워드")
    grep_parser.add_argument("--days", type=int, default=7, help="최근 N일 (기본: 7)")
    grep_parser.add_argument("--date", help="조회할 날짜 (YYYY-MM-DD)")
    grep_parser.add_argument(
        "--cwd", action="store_true", help="현재 디렉토리 프로젝트만"
    )
    grep_parser.add_argument(
        "--limit", type=int, default=None, help="결과 세션 최대 N개"
    )

    show_parser = subparsers.add_parser(
        "show", help="특정 세션 대화 보기", parents=[common]
    )
    show_parser.add_argument(
        "session", nargs="?", default=None, help="세션 ID (앞 12자리 이상 권장)"
    )
    show_parser.add_argument("--last", action="store_true", help="가장 최근 세션 보기")
    show_parser.add_argument("--full", action="store_true", help="도구 호출/결과 포함")
    show_parser.add_argument("--files", action="store_true", help="수정된 파일 목록만")
    show_parser.add_argument("--limit", type=int, default=None, help="앞 N개 메시지만")

    subparsers.add_parser(
        "sources", help="감지된 로컬 로그 소스 조회", parents=[common]
    )

    redact_parser = subparsers.add_parser(
        "redact", help="로그 파일에 남은 시크릿을 실제로 지움", parents=[common]
    )
    redact_parser.add_argument(
        "--apply", action="store_true", help="실제로 치환 (기본: 세기만)"
    )
    redact_parser.add_argument(
        "--path", action="append", help="로그 소스 밖의 추가 대상 경로 (반복 가능)"
    )
    redact_parser.add_argument(
        "--exclude",
        action="append",
        help="경로에 이 문자열이 있으면 건너뜀 (반복 가능)",
    )
    redact_parser.add_argument(
        "--backup", default=None, help="백업 tar.gz 경로 (기본: ~/.local/state)"
    )

    args = parser.parse_args()
    set_include_subagents(getattr(args, "include_subagents", False))

    if args.command is None or args.command == "list":
        if not hasattr(args, "date"):
            args.date = None
        if not hasattr(args, "days"):
            args.days = 1
        if not hasattr(args, "project"):
            args.project = None
        if not hasattr(args, "cwd"):
            args.cwd = False
        if not hasattr(args, "search"):
            args.search = None
        if not hasattr(args, "summary"):
            args.summary = False
        cmd_list(args)
    elif args.command == "timeline":
        cmd_timeline(args)
    elif args.command in ("grep", "rg"):
        cmd_grep(args)
    elif args.command == "show":
        cmd_show(args)
    elif args.command == "sources":
        cmd_sources(args)
    elif args.command == "redact":
        cmd_redact(args)


if __name__ == "__main__":
    main()
