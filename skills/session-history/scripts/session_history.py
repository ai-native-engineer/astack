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
    python3 session_history.py rg 정지 이의신청 --sort relevance  # 여러 키워드 OR, 관련도 순
    python3 session_history.py show --last                  # 가장 최근 세션
    python3 session_history.py show abc123 --full           # 도구 호출 포함
    python3 session_history.py show abc123 --grep 정지      # 일치한 곳과 앞뒤만
    python3 session_history.py show abc123 --limit 20       # 앞 20개만
    python3 session_history.py sources                      # 감지된 로그 소스
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
from collections import Counter, defaultdict
from pathlib import Path

# Allow `python3 scripts/session_history.py` without package install.
_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from adapters import ADAPTERS, ORDER, iter_adapters  # noqa: E402
from common import (  # noqa: E402
    Matcher,
    date_range,
    local_time,
    set_include_subagents,
    shorten_home,
    ts_to_hm,
)

# 하네스가 도구 호출 환경에 넣어 주는 현재 세션 ID. 검색하는 세션은 자기 검색 명령
# 때문에 항상 걸리므로 기본 결과에서 뺀다
CURRENT_SESSION_ENV = ("CLAUDE_CODE_SESSION_ID", "CODEX_THREAD_ID", "GJC_SESSION_ID")

# 경로를 명령 인자로 넘기므로 ARG_MAX(macOS 1MB)에 닿지 않게 나눠 부른다.
# 세션 파일 경로는 200자 안팎이라 400개면 100KB 수준이다
PREFILTER_CHUNK = 400

# show가 도구 출력을 보여 주는 폭. 텍스트는 훑기용, JSON은 다른 도구가 읽을 몫이다
TOOL_TEXT_WIDTH = 300
TOOL_JSON_WIDTH = 500
TOOL_ROLES = ("tool", "tool_call", "tool_result")
TALK_ROLES = ("user", "assistant")


def current_session_ids() -> set[str]:
    return {os.environ[name] for name in CURRENT_SESSION_ENV if os.environ.get(name)}


def prefilter_paths(paths, matcher):
    """키워드가 원문에 없는 로그를 JSON 파싱 전에 ripgrep으로 거른다.

    반환값은 키워드가 있는 경로 집합이다. 거를 수 없으면(rg 없음, 정규식, 오류) None을
    돌려 모든 파일을 파싱하게 한다. 거르다 놓치는 것보다 느린 편이 낫다.
    """
    forms = matcher.raw_forms()
    rg = shutil.which("rg")
    if not forms or not rg or not paths:
        return None
    patterns = [arg for form in forms for arg in ("-e", form)]
    found = set()
    for i in range(0, len(paths), PREFILTER_CHUNK):
        chunk = paths[i : i + PREFILTER_CHUNK]
        command = [rg, "--no-config", "-l", "-i", "-F", "-a", "--no-messages"]
        try:
            proc = subprocess.run(
                [*command, *patterns, "--", *chunk],
                capture_output=True,
                text=True,
                check=False,
            )
        except OSError:
            return None
        # 0은 찾음, 1은 없음. 그 밖의 종료 코드는 결과를 믿을 수 없다
        if proc.returncode not in (0, 1):
            return None
        found.update(proc.stdout.splitlines())
    return found


def build_matcher(terms, regex: bool, skip_echo: bool = True) -> Matcher:
    try:
        return Matcher(terms, regex=regex, skip_echo=skip_echo)
    except re.error as exc:
        print(
            f"정규식 오류: {exc}. -E를 빼면 키워드를 글자 그대로 찾습니다.",
            file=sys.stderr,
        )
        sys.exit(2)


def literal_pipe_note(terms, regex: bool) -> str:
    """`a|b`를 OR로 기대하고 넘긴 경우를 짚어 준다. 결과가 비어도 원인을 알 수 있게."""
    piped = [term for term in terms if "|" in term]
    if regex or not piped:
        return ""
    return (
        f'참고: "{piped[0]}"의 |는 글자 그대로 찾습니다. '
        "여러 키워드는 rg A B처럼 나눠 넘기면 OR로 찾고, 정규식은 -E를 붙입니다."
    )


def clip_around(text: str, width: int, matcher=None) -> str:
    """긴 도구 출력을 width로 줄인다. 일치한 곳이 있으면 그 주변을 남긴다."""
    if len(text) <= width:
        return text
    found = matcher.first(text) if matcher else None
    lo = 0
    if found:
        lo = max(0, min(found[1] - width // 3, len(text) - width))
    hi = lo + width
    return ("..." if lo else "") + text[lo:hi] + ("..." if hi < len(text) else "")


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
            label = (
                info.get("name")
                or (info.get("provider") and f"provider={info['provider']}")
                or ""
            )
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


def grep_candidates(sessions, matcher):
    """검색할 (sid, info, adapter, fpath) 목록. 최근 세션이 앞에 온다."""
    candidates = []
    for sid, info in sessions.items():
        adapter = ADAPTERS.get(info.get("tool"))
        if not adapter:
            continue
        fpath = adapter_session_path(adapter, sid)
        if not fpath or not Path(fpath).exists():
            continue
        candidates.append((sid, info, adapter, fpath))

    single_file = [
        str(fpath)
        for _, _, adapter, fpath in candidates
        if getattr(adapter, "GREP_READS_SESSION_FILE", False)
    ]
    found = prefilter_paths(single_file, matcher)
    if found is not None:
        candidates = [
            row
            for row in candidates
            if not getattr(row[2], "GREP_READS_SESSION_FILE", False)
            or str(row[3]) in found
        ]
    # sorted는 안정 정렬이라 같은 시각은 수집 순서를 유지한다
    return sorted(
        candidates, key=lambda row: row[1].get("first_ts_ms") or 0, reverse=True
    )


def grep_result(sid, info, fpath, hits):
    first_ts_ms = info.get("first_ts_ms") or 0
    return {
        "sid": sid,
        "tool": info["tool"],
        "project": info.get("project", ""),
        "first_ts_ms": first_ts_ms,
        "start": local_time(first_ts_ms, "%Y-%m-%d %H:%M") if first_ts_ms else "",
        "hit_count": len(hits),
        "talk_count": sum(1 for h in hits if h.get("role") in TALK_ROLES),
        "terms": dict(Counter(h["term"] for h in hits if h.get("term"))),
        "fpath": str(fpath),
        "hits": [
            {**hit, "time": local_time(hit.get("ts"), "%Y-%m-%d %H:%M:%S")}
            for hit in hits
        ],
    }


def cmd_grep(args):
    terms = args.keywords
    matcher = build_matcher(terms, args.regex, skip_echo=not args.include_self)
    note = literal_pipe_note(terms, args.regex)
    start_ms, end_ms, label = date_range(args)
    cwd_filter = str(Path.cwd()) if getattr(args, "cwd", False) else None
    sessions = collect_history(args.tool, start_ms, end_ms, cwd_filter=cwd_filter)
    if not args.include_self:
        for sid in current_session_ids():
            sessions.pop(sid, None)

    limit = args.limit
    # 최근 순이면 앞에서 limit개를 채우는 즉시 멈춘다. hit 순은 전부 세어야 순위가 나온다
    stop_early = limit is not None and args.sort == "recent"
    results = []
    for sid, info, adapter, fpath in grep_candidates(sessions, matcher):
        if stop_early and len(results) >= limit:
            break
        try:
            hits = adapter.grep_session(fpath, matcher, session_id=sid)
        except OSError:
            continue
        if hits:
            result = grep_result(sid, info, fpath, hits)
            status = getattr(adapter, "conversation_status", lambda _: {})(sid)
            if status.get("warnings"):
                result["warnings"] = status["warnings"]
            results.append(result)
    if args.sort == "relevance":
        # 흔한 키워드 하나는 그 말이 든 파일을 여러 번 읽은 세션에서 도구 출력 hit로 쌓인다.
        # 주제를 실제로 다룬 세션은 동의어를 여러 종류 맞히고 대화에서 말한다
        results.sort(
            key=lambda row: (len(row["terms"]), row["talk_count"], row["hit_count"]),
            reverse=True,
        )
    if limit is not None:
        results = results[:limit]

    if args.format == "json":
        if note:
            print(note, file=sys.stderr)
        emit(json.dumps(results, ensure_ascii=False, indent=2), args)
        return

    command_label = "rg" if getattr(args, "command", "") == "rg" else "grep"
    quoted = ", ".join(f'"{term}"' for term in terms)
    lines = [f"# {command_label}: {quoted} ({label})", ""]
    if note:
        lines.extend([note, ""])
    if not results:
        lines.append("매칭 없음.")
        emit("\n".join(lines), args)
        return

    order_label = (
        "관련도 순 (맞힌 키워드 종류, 대화 hit, 전체 hit)"
        if args.sort == "relevance"
        else "최근 순"
    )
    lines.append(f"{len(results)}개 세션에서 발견, {order_label}")
    lines.append("─" * 60)

    hit_width = short_id_width(r["sid"] for r in results)
    for r in results:
        proj = shorten_home(r["project"])
        start = local_time(r["first_ts_ms"]) if r["first_ts_ms"] else "??"
        tool_tag = (
            f"[{ADAPTERS[r['tool']].DISPLAY}]"
            if r["tool"] in ADAPTERS
            else f"[{r['tool']}]"
        )
        count = f"hit {r['hit_count']}, 대화 {r['talk_count']}"
        if len(terms) > 1 and r["terms"]:
            count += f", 키워드 {len(r['terms'])}/{len(terms)}"
            count += " (" + ", ".join(f"{t} {n}" for t, n in r["terms"].items()) + ")"
        lines.append(f"\n{tool_tag} {r['sid'][:hit_width]}  {proj}  {start}  {count}")
        lines.append(f"  파일: {r['fpath']}")
        for warning in r.get("warnings", []):
            lines.append(f"  주의: {warning}")
        for hit in r["hits"][:3]:
            role_icon = {"user": "👤", "assistant": "🤖"}.get(hit["role"], "🔧")
            source_label = (
                " [입력 기록만 복원]" if hit.get("source") == "history" else ""
            )
            lines.append(
                f"  {role_icon} {local_time(hit['ts'])}{source_label}  {hit['excerpt']}"
            )
        if len(r["hits"]) > 3:
            lines.append(f"  ... 외 {len(r['hits']) - 3}건 더")

    lines.append("")
    lines.append("─" * 60)
    lines.append(f"총 {sum(r['hit_count'] for r in results)}건 ({len(results)}개 세션)")
    lines.append("👤 사용자  🤖 어시스턴트  🔧 도구 호출과 결과. 대화 = 👤와 🤖 hit 수")
    lines.append(
        "일치한 곳 읽기: python3 session_history.py show <세션ID> --grep <키워드>"
    )
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


def select_messages(messages, matcher=None, context=0, offset=0, limit=None):
    """show에 낼 (번호, 메시지, 일치 여부) 목록. 번호는 세션 안 위치라 --offset에 그대로 쓴다."""
    matched = set()
    if matcher:
        for index, message in enumerate(messages):
            if matcher.first(message.get("text") or ""):
                matched.add(index)
        keep = set()
        for index in matched:
            keep.update(range(index - context, index + context + 1))
        view = [(i, m) for i, m in enumerate(messages) if i in keep]
    else:
        view = list(enumerate(messages))
    view = view[offset or 0 :]
    if limit:
        view = view[:limit]
    return [(i, m, i in matched) for i, m in view]


def format_conversation(
    view,
    total,
    tool_name,
    session_id,
    mode_label,
    fpath=None,
    matcher=None,
    next_hint="",
):
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

    if not total:
        lines.append("(대화 내역 없음)")
        return "\n".join(lines)
    if not view:
        if matcher:
            lines.append("(일치하는 메시지 없음. 다른 세션은 rg로 찾습니다)")
        else:
            lines.append(f"(표시할 메시지 없음. 전체 {total}건)")
        return "\n".join(lines)

    lines.append(f"모드: {mode_label} | 메시지 {len(view)}/{total}건")
    lines.append("─" * 60)

    previous = None
    for index, msg, is_match in view:
        if previous is not None and index > previous + 1:
            skipped = (
                f"#{previous + 1}"
                if index == previous + 2
                else f"#{previous + 1}~#{index - 1}"
            )
            lines.append(f"\n... {skipped} 생략")
        previous = index

        role = msg.get("role", "")
        label = role_labels.get(role, role.upper())
        time_str = local_time(msg.get("ts"), "%m-%d %H:%M:%S")
        phase = msg.get("phase", "")
        phase_str = f" ({phase})" if phase else ""
        if msg.get("source") == "history":
            phase_str += " (입력 기록만 복원, 응답/실행 미확인)"
        model = msg.get("model", "")
        model_str = f" [{model}]" if model else ""
        match_str = "  일치" if is_match else ""

        lines.append(f"\n#{index} {label}{phase_str}{model_str}  {time_str}{match_str}")

        text = msg.get("text", "")
        if role in TOOL_ROLES and len(text) > TOOL_TEXT_WIDTH:
            text = (
                clip_around(text, TOOL_TEXT_WIDTH, matcher)
                + f"\n... ({len(text)}자 중 {TOOL_TEXT_WIDTH}자 표시)"
            )
        lines.append(text)

    lines.append("")
    lines.append("─" * 60)
    lines.append(f"총 {total}건")
    if next_hint:
        lines.append(next_hint)
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
    grep_terms = getattr(args, "grep", None)
    # 세션 하나를 고른 뒤라 지난 검색 명령도 그 세션의 맥락이다. 메아리를 거르지 않는다
    matcher = (
        build_matcher(grep_terms, args.regex, skip_echo=False) if grep_terms else None
    )
    # rg는 도구 기록까지 찾으므로, 그 hit를 따라 들어온 show --grep도 도구 기록을 읽는다
    full = args.full or matcher is not None

    if getattr(args, "files", False):
        changes, bash_hints = adapter.extract_changed_files(session_id)
        if hasattr(adapter, "conversation_status"):
            # 입력만 남은 구간에는 변경 파일도 없다고 단정할 수 없다.
            adapter.read_conversation(session_id)
        _print_conversation_warnings(adapter, session_id)
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
    _print_conversation_warnings(adapter, session_id)
    if messages is None:
        print(f"세션 파일을 찾을 수 없습니다: {session_id}")
        sys.exit(1)

    view = select_messages(messages, matcher, args.context, args.offset, args.limit)

    if args.format == "json":
        out = []
        for index, msg, is_match in view:
            row = {**msg, "index": index}
            row.pop("call_id", None)
            text = row.get("text") or ""
            if row.get("role") in TOOL_ROLES and len(text) > TOOL_JSON_WIDTH:
                row["text"] = clip_around(text, TOOL_JSON_WIDTH, matcher)
                row["chars"] = len(text)
            if matcher:
                row["match"] = is_match
            out.append(row)
        emit(json.dumps(out, ensure_ascii=False, indent=2), args)
        return

    # #번호는 모드마다 기준이 다르다(대화만 / 도구 기록 포함). 이어 읽기 명령에 기준을 박아 둔다
    base = f"python3 session_history.py show {session_id[:12]}"
    next_hint = ""
    if matcher:
        matched = sum(1 for _, _, is_match in view if is_match)
        mode_label = (
            f"--grep 일치 {matched}건과 앞뒤 {args.context}건 "
            "(도구 기록 포함, #번호는 --full 기준)"
        )
        first = next((index for index, _, is_match in view if is_match), None)
        if first is not None:
            start = max(first - args.context, 0)
            next_hint = f"주변 이어 읽기: {base} --full --offset {start} --limit 20"
    else:
        mode_label = (
            "전체 (도구 호출 포함, #번호는 --full 기준)"
            if full
            else "대화만 (#번호는 대화 기준이라 --full과 다름)"
        )
        consumed = (args.offset or 0) + len(view)
        if args.limit and view and consumed < len(messages):
            flag = " --full" if full else ""
            next_hint = (
                f"이어 보기: {base}{flag} --offset {consumed} --limit {args.limit}"
            )
    emit(
        format_conversation(
            view,
            len(messages),
            adapter.DISPLAY,
            session_id,
            mode_label,
            fpath=fpath,
            matcher=matcher,
            next_hint=next_hint,
        ),
        args,
    )


# 텍스트로 안전하게 다시 쓸 수 있는 로그만 고친다. sqlite 같은 바이너리 저장소를
# 문자열 치환하면 길이가 달라져 파일이 깨진다
_REDACT_SUFFIXES = (".jsonl", ".json", ".txt", ".md", ".log")


def _print_conversation_warnings(adapter, session_id):
    status = getattr(adapter, "conversation_status", lambda _: {})(session_id)
    for warning in status.get("warnings", []):
        print(f"주의: {redact_sensitive_text(warning)}", file=sys.stderr)


def _is_paginated_rollout(path):
    try:
        with path.open(encoding="utf-8") as stream:
            first = json.loads(stream.readline())
        meta = first.get("payload") or {}
        return first.get("type") == "session_meta" and (
            meta.get("history_mode") == "paginated" or bool(meta.get("history_base"))
        )
    except (OSError, ValueError, AttributeError):
        return False


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

    protected = [path for path, _ in changed if _is_paginated_rollout(path)]
    if protected:
        print(
            "Codex paginated rollout은 byte offset으로 연결됩니다. 원본 치환을 중단합니다. 조회 마스킹을 사용하세요.",
            file=sys.stderr,
        )
        for path in protected:
            print(f"  {path}", file=sys.stderr)
        raise SystemExit(1)

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


def date_arg(value: str) -> str:
    try:
        return datetime.date.fromisoformat(value).isoformat()
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            f"YYYY-MM-DD 형식이어야 합니다 (받은 값: {value})"
        ) from exc


def count_arg(value: str) -> int:
    try:
        number = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"정수여야 합니다 (받은 값: {value})") from exc
    if number < 0:
        raise argparse.ArgumentTypeError(f"0 이상이어야 합니다 (받은 값: {value})")
    return number


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
  %(prog)s rg "gcloud"                     대화·도구 기록 검색 (최근 7일)
  %(prog)s rg 정지 이의신청 --since 2026-08-01 --sort relevance
                                           여러 키워드 OR, 날짜 이후, 관련도 순
  %(prog)s rg -E "account.*suspend"        정규식 (사전 필터를 못 써 느림)
  %(prog)s show --last                     가장 최근 세션
  %(prog)s show abc12345 --files           수정된 파일 목록
  %(prog)s show abc12345 --grep 정지       일치한 메시지와 앞뒤 2건 (도구 기록 포함)
  %(prog)s show abc12345 --limit 20        앞 20개 메시지만
  %(prog)s show abc12345 --offset 20 --limit 20
                                           이어서 20개
  %(prog)s show --last --raw               마스킹 없이 원문 (기본은 마스킹)
  %(prog)s sources                         감지된 로컬 로그 소스와 세션 수
  %(prog)s redact                          로그에 남은 시크릿 세기
  %(prog)s redact --apply                  백업 후 실제로 지우기
""",
    )

    subparsers = parser.add_subparsers(dest="command")

    since_help = "이 날짜(YYYY-MM-DD)부터 오늘까지. --days보다 우선, --date보다 후순위"

    list_parser = subparsers.add_parser("list", help="세션 목록 조회", parents=[common])
    list_parser.add_argument("--date", type=date_arg, help="조회할 날짜 (YYYY-MM-DD)")
    list_parser.add_argument("--since", type=date_arg, help=since_help)
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
    tl_parser.add_argument("--date", type=date_arg, help="조회할 날짜 (YYYY-MM-DD)")
    tl_parser.add_argument("--since", type=date_arg, help=since_help)
    tl_parser.add_argument("--days", type=int, default=1, help="최근 N일 (기본: 1)")
    tl_parser.add_argument(
        "--cwd", action="store_true", help="현재 디렉토리 프로젝트만"
    )
    tl_parser.add_argument("--compact", action="store_true", help="중간 스냅샷 생략")

    grep_parser = subparsers.add_parser(
        "grep", aliases=["rg"], help="세션 전문 검색 (대화·도구 기록)", parents=[common]
    )
    grep_parser.add_argument(
        "keywords",
        nargs="+",
        metavar="keyword",
        help="검색할 키워드. 여러 개면 OR. 대소문자 무시, 기본은 글자 그대로",
    )
    grep_parser.add_argument(
        "-E", "--regex", action="store_true", help="키워드를 정규식으로 해석 (느림)"
    )
    grep_parser.add_argument("--days", type=int, default=7, help="최근 N일 (기본: 7)")
    grep_parser.add_argument("--since", type=date_arg, help=since_help)
    grep_parser.add_argument("--date", type=date_arg, help="조회할 날짜 (YYYY-MM-DD)")
    grep_parser.add_argument(
        "--cwd", action="store_true", help="현재 디렉토리 프로젝트만"
    )
    grep_parser.add_argument(
        "--sort",
        choices=["recent", "relevance"],
        default="recent",
        help=(
            "결과 순서. recent=세션 시작이 최근인 순(기본), "
            "relevance=맞힌 키워드 종류, 대화 hit, 전체 hit 순"
        ),
    )
    grep_parser.add_argument(
        "--limit", type=count_arg, default=None, help="--sort 순서로 앞 N개 세션만"
    )
    grep_parser.add_argument(
        "--include-self",
        action="store_true",
        help="현재 세션과 지난 session_history 검색 기록도 포함 (기본: 제외)",
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
    show_parser.add_argument(
        "--grep",
        nargs="+",
        metavar="keyword",
        help="일치한 메시지와 앞뒤만 (OR, 도구 기록 포함). 세션 ID 뒤에 쓴다",
    )
    show_parser.add_argument(
        "-E", "--regex", action="store_true", help="--grep 키워드를 정규식으로 해석"
    )
    show_parser.add_argument(
        "--context",
        type=count_arg,
        default=2,
        help="--grep 일치 앞뒤로 볼 메시지 수 (기본: 2)",
    )
    show_parser.add_argument(
        "--offset",
        type=count_arg,
        default=0,
        help="앞 N개를 건너뜀 (--limit와 함께 페이지 넘김)",
    )
    show_parser.add_argument(
        "--limit", type=count_arg, default=None, help="N개 메시지만"
    )

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
