#!/usr/bin/env python3
"""Claude Code + Codex 통합 세션 히스토리.

Subcommands:
    list      세션 목록 조회 (기본)
    show      특정 세션의 전체 대화 내역 보기
    timeline  오늘 작업 시간순 타임라인 (데일리 노트용)
    rg        세션 전문 검색 (preview 아닌 실제 대화·도구 기록)

Usage:
    python3 session_history.py                              # 오늘 세션 목록
    python3 session_history.py list --cwd                   # 현재 디렉토리 프로젝트만
    python3 session_history.py list --search pytest         # 키워드 검색
    python3 session_history.py timeline                     # 오늘 타임라인
    python3 session_history.py rg "gcloud"                  # 대화·도구 기록 검색
    python3 session_history.py show --last                  # 가장 최근 세션
    python3 session_history.py show abc123 --full           # 도구 호출 포함
    python3 session_history.py show abc123 --limit 20       # 앞 20개만
"""

import json
import re
import datetime
import argparse
import functools
import sys
from collections import defaultdict
from pathlib import Path

CLAUDE_EDIT_TOOLS = {"Edit", "Write", "MultiEdit", "NotebookEdit"}
APPLY_PATCH_HEADER_RE = re.compile(
    r"^\*\*\*\s+(Update|Add|Delete|Move)\s+(?:File|to):\s+(.+?)\s*$", re.MULTILINE
)
BASH_MUTATION_RE = re.compile(
    r"(?:(?:^|[;&|\s])(?:rm|mv|cp|mkdir|rmdir|touch|ln|chmod|chown|sed\s+-i|tee|apply_patch)\b)|(?:\s>>?\s*[^\s;&|])",
)

_INCLUDE_SUBAGENTS = False


def set_include_subagents(value: bool):
    global _INCLUDE_SUBAGENTS
    if _INCLUDE_SUBAGENTS == bool(value):
        return
    _INCLUDE_SUBAGENTS = bool(value)
    claude_conversation_index.cache_clear()
    codex_session_index.cache_clear()


def refresh_indexes():
    claude_conversation_index.cache_clear()
    codex_session_index.cache_clear()

HOME = Path.home()
CLAUDE_HISTORY = HOME / ".claude" / "history.jsonl"
CLAUDE_SESSIONS_DIR = HOME / ".claude" / "sessions"
CLAUDE_PROJECTS_DIR = HOME / ".claude" / "projects"
CODEX_HISTORY = HOME / ".codex" / "history.jsonl"
CODEX_SESSIONS_DIR = HOME / ".codex" / "sessions"


# ─── Helpers ───────────────────────────────────────────────────

def shorten_home(path: str) -> str:
    home = str(HOME)
    return path.replace(home, "~") if path else "(unknown)"


def ts_to_hm(ts_ms: int) -> str:
    return datetime.datetime.fromtimestamp(ts_ms / 1000).strftime("%H:%M")


def ts_to_hms(ts_ms: int) -> str:
    return datetime.datetime.fromtimestamp(ts_ms / 1000).strftime("%H:%M:%S")


def date_range(args):
    if args.date:
        target = datetime.datetime.strptime(args.date, "%Y-%m-%d")
        start = target
        end = target + datetime.timedelta(days=1)
        label = args.date
    else:
        now = datetime.datetime.now()
        start = now.replace(hour=0, minute=0, second=0, microsecond=0) - datetime.timedelta(days=args.days - 1)
        end = now + datetime.timedelta(days=1)
        label = (
            start.strftime("%Y-%m-%d")
            if args.days == 1
            else f"{start.strftime('%Y-%m-%d')} ~ {now.strftime('%Y-%m-%d')}"
        )
    return int(start.timestamp() * 1000), int(end.timestamp() * 1000), label


def path_matches(project: str, filter_path: str) -> bool:
    """cwd 기준 프로젝트 매칭.

    - project가 cwd 하위 경로 → 매칭 (서브프로젝트)
    - cwd가 project 하위 경로 → 매칭 (하위 폴더에서 작업 중)
      단, project가 홈 디렉토리와 동일하면 제외 (너무 광범위)
    """
    if not project or not filter_path:
        return False
    p = project.rstrip("/")
    f = filter_path.rstrip("/")
    home = str(HOME)
    if p == home:
        return False
    return p.startswith(f) or f.startswith(p)


# ─── 단일-빌드 인덱스 ──────────────────────────────────────────

@functools.lru_cache(maxsize=1)
def claude_conversation_index():
    """session_id (stem) → conversation jsonl Path."""
    idx = {}
    if not CLAUDE_PROJECTS_DIR.exists():
        return idx
    for f in CLAUDE_PROJECTS_DIR.rglob("*.jsonl"):
        if not _INCLUDE_SUBAGENTS and "/subagents/" in str(f):
            continue
        idx[f.stem] = f
    return idx


@functools.lru_cache(maxsize=1)
def codex_session_index():
    """session_meta.payload.id → {"path", "cwd", "ts"}."""
    idx = {}
    if not CODEX_SESSIONS_DIR.exists():
        return idx
    for f in CODEX_SESSIONS_DIR.rglob("rollout-*.jsonl"):
        try:
            with open(f, encoding="utf-8") as fh:
                first = fh.readline().strip()
                if not first:
                    continue
                d = json.loads(first)
        except (json.JSONDecodeError, OSError):
            continue
        if d.get("type") != "session_meta":
            continue
        payload = d.get("payload", {}) or {}
        sid = payload.get("id", "")
        if not sid:
            continue
        if not _INCLUDE_SUBAGENTS:
            src = payload.get("source", "")
            originator = payload.get("originator", "")
            if originator == "codex_exec" or src == "exec":
                continue
            if isinstance(src, dict) and "subagent" in src:
                continue
        idx[sid] = {
            "path": f,
            "cwd": payload.get("cwd", ""),
            "ts": payload.get("timestamp", ""),
        }
    return idx


# ─── Claude Code session IO ────────────────────────────────────

def find_claude_conversation_file(session_id: str) -> Path | None:
    idx = claude_conversation_index()
    if session_id in idx:
        return idx[session_id]
    for sid, path in idx.items():
        if sid.startswith(session_id):
            return path
    return None


def read_claude_conversation(session_id: str, full: bool = False):
    """(messages, fpath) 반환."""
    fpath = find_claude_conversation_file(session_id)
    if not fpath:
        return None, None

    messages = []
    with open(fpath, encoding="utf-8") as f:
        for line in f:
            try:
                d = json.loads(line.strip())
            except json.JSONDecodeError:
                continue

            entry_type = d.get("type", "")
            ts = d.get("timestamp", "")

            if entry_type == "user":
                msg = d.get("message", {})
                content = msg.get("content", "")
                if isinstance(content, list):
                    parts = []
                    for c in content:
                        if isinstance(c, dict) and c.get("type") == "text":
                            parts.append(c["text"])
                        elif isinstance(c, str):
                            parts.append(c)
                    content = "\n".join(parts)
                if content.strip():
                    messages.append({"role": "user", "text": content.strip(), "ts": ts})

            elif entry_type == "assistant":
                msg = d.get("message", {})
                content_parts = msg.get("content", [])
                texts = []
                tool_calls = []
                for part in content_parts:
                    if not isinstance(part, dict):
                        continue
                    if part.get("type") == "text":
                        texts.append(part["text"])
                    elif part.get("type") == "tool_use" and full:
                        tool_calls.append(f"[tool: {part.get('name', '')}]")

                text = "\n".join(texts)
                if full and tool_calls:
                    text += "\n" + "\n".join(tool_calls)
                if text.strip():
                    messages.append({
                        "role": "assistant",
                        "text": text.strip(),
                        "ts": ts,
                        "model": msg.get("model", ""),
                    })

            elif entry_type == "tool_result" and full:
                msg = d.get("message", {})
                content = msg.get("content", [])
                for part in content:
                    if isinstance(part, dict) and part.get("type") == "tool_result":
                        result_text = part.get("content", "")
                        if isinstance(result_text, str) and result_text.strip():
                            messages.append({"role": "tool", "text": result_text[:500], "ts": ts})

    return messages, fpath


def extract_claude_changed_files(session_id: str):
    fpath = find_claude_conversation_file(session_id)
    if not fpath:
        return None, None

    changes = []
    bash_hints = []
    with open(fpath, encoding="utf-8") as f:
        for line in f:
            try:
                d = json.loads(line.strip())
            except json.JSONDecodeError:
                continue
            if d.get("type") != "assistant":
                continue
            ts = d.get("timestamp", "")
            for part in d.get("message", {}).get("content", []) or []:
                if not isinstance(part, dict) or part.get("type") != "tool_use":
                    continue
                name = part.get("name", "")
                inp = part.get("input", {}) or {}
                if name in CLAUDE_EDIT_TOOLS:
                    path = inp.get("file_path") or inp.get("notebook_path") or ""
                    if path:
                        changes.append({"file": path, "tool": name, "ts": ts})
                elif name == "Bash":
                    cmd = inp.get("command", "")
                    if cmd and BASH_MUTATION_RE.search(cmd):
                        bash_hints.append({"cmd": cmd, "ts": ts})
    return changes, bash_hints


# ─── Codex session IO ──────────────────────────────────────────

def find_codex_session_file(session_id: str) -> Path | None:
    idx = codex_session_index()
    if session_id in idx:
        return idx[session_id]["path"]
    for sid, info in idx.items():
        if sid.startswith(session_id):
            return info["path"]
    return None


def read_codex_conversation(session_id: str, full: bool = False):
    """(messages, fpath) 반환."""
    fpath = find_codex_session_file(session_id)
    if not fpath:
        return None, None

    messages = []
    with open(fpath, encoding="utf-8") as f:
        for line in f:
            try:
                d = json.loads(line.strip())
            except json.JSONDecodeError:
                continue

            entry_type = d.get("type", "")
            ts = d.get("timestamp", "")
            payload = d.get("payload", {})

            if entry_type == "event_msg":
                msg_type = payload.get("type", "")
                if msg_type == "user_message":
                    text = payload.get("message", "")
                    if text.strip():
                        messages.append({"role": "user", "text": text.strip(), "ts": ts})
                elif msg_type == "agent_message":
                    phase = payload.get("phase", "")
                    text = payload.get("message", "")
                    if text.strip():
                        messages.append({"role": "assistant", "text": text.strip(), "ts": ts, "phase": phase})

            elif entry_type == "response_item" and full:
                rtype = payload.get("type", "")
                if rtype == "function_call":
                    name = payload.get("name", "")
                    args_str = payload.get("arguments", "")
                    try:
                        args_obj = json.loads(args_str)
                        cmd = args_obj.get("command", args_obj.get("cmd", ""))[:200]
                    except (json.JSONDecodeError, TypeError):
                        cmd = args_str[:200]
                    messages.append({"role": "tool_call", "text": f"[{name}] {cmd}", "ts": ts})
                elif rtype == "function_call_output":
                    output = payload.get("output", "")[:500]
                    if output.strip():
                        messages.append({"role": "tool_result", "text": output.strip(), "ts": ts})

    return messages, fpath


def extract_codex_changed_files(session_id: str):
    fpath = find_codex_session_file(session_id)
    if not fpath:
        return None, None

    changes = []
    bash_hints = []
    seen_patches = set()

    def _add_patch(file_path, op, ts_iso, tool_label):
        op_key = (op or "").lower()
        ts_key = ts_iso[:19] if isinstance(ts_iso, str) else str(ts_iso)
        key = (file_path, op_key, ts_key)
        if key in seen_patches:
            return
        seen_patches.add(key)
        changes.append({"file": file_path, "tool": tool_label, "ts": ts_iso})

    with open(fpath, encoding="utf-8") as f:
        for line in f:
            try:
                d = json.loads(line.strip())
            except json.JSONDecodeError:
                continue

            entry_type = d.get("type", "")
            payload = d.get("payload", {}) or {}
            ts = d.get("timestamp", "")

            if entry_type == "event_msg" and payload.get("type") == "patch_apply_begin":
                changes_dict = payload.get("changes", {}) or {}
                for path, info in changes_dict.items():
                    op = info.get("type") if isinstance(info, dict) else str(info)
                    _add_patch(path, op, ts, f"patch/{op}")
                continue

            if entry_type != "response_item":
                continue
            ptype = payload.get("type", "")
            if ptype not in ("custom_tool_call", "function_call"):
                continue

            name = payload.get("name", "")

            if name == "apply_patch":
                raw = payload.get("input", "")
                if not raw:
                    args_str = payload.get("arguments", "")
                    try:
                        args_obj = json.loads(args_str) if args_str else {}
                        raw = args_obj.get("input", "") if isinstance(args_obj, dict) else ""
                    except (json.JSONDecodeError, TypeError):
                        raw = ""
                if not raw:
                    continue
                for op, path in APPLY_PATCH_HEADER_RE.findall(raw):
                    _add_patch(path.strip(), op, ts, f"apply_patch/{op}")
                continue

            if name == "shell":
                args_str = payload.get("arguments", "")
                try:
                    args_obj = json.loads(args_str) if args_str else {}
                except (json.JSONDecodeError, TypeError):
                    args_obj = {}
                cmd_field = args_obj.get("command", "") if isinstance(args_obj, dict) else ""
                cmd = " ".join(cmd_field) if isinstance(cmd_field, list) else str(cmd_field)
                if cmd and BASH_MUTATION_RE.search(cmd):
                    bash_hints.append({"cmd": cmd, "ts": ts})

    return changes, bash_hints


# ─── History extraction ────────────────────────────────────────

def extract_claude_history(start_ms, end_ms, project_filter=None, cwd_filter=None):
    sessions = defaultdict(lambda: {
        "project": "", "messages": [], "tool": "claude", "first_ts_ms": 0,
    })
    if not CLAUDE_HISTORY.exists():
        return {}
    with open(CLAUDE_HISTORY, encoding="utf-8") as f:
        for line in f:
            try:
                d = json.loads(line.strip())
            except json.JSONDecodeError:
                continue
            ts = int(d.get("timestamp", 0))
            if not (start_ms <= ts < end_ms):
                continue
            sid = d.get("sessionId", "")
            project = d.get("project", "")
            display = d.get("display", "").strip()
            if project_filter and project_filter not in project:
                continue
            if cwd_filter and not path_matches(project, cwd_filter):
                continue
            if not sessions[sid]["project"] and project:
                sessions[sid]["project"] = project
            if not sessions[sid]["first_ts_ms"]:
                sessions[sid]["first_ts_ms"] = ts
            else:
                sessions[sid]["first_ts_ms"] = min(sessions[sid]["first_ts_ms"], ts)
            if display:
                sessions[sid]["messages"].append({"time": ts_to_hm(ts), "text": display[:300]})
    return dict(sessions)


def codex_first_user_message(fpath, max_lines=500):
    try:
        with open(fpath, encoding="utf-8") as f:
            for i, line in enumerate(f):
                if i >= max_lines:
                    break
                try:
                    d = json.loads(line.strip())
                except json.JSONDecodeError:
                    continue
                if d.get("type") != "event_msg":
                    continue
                p = d.get("payload", {}) or {}
                if p.get("type") == "user_message":
                    return (p.get("message", "") or "").strip()
    except OSError:
        pass
    return ""


def extract_codex_history(start_ms, end_ms, project_filter=None, cwd_filter=None):
    sessions = defaultdict(lambda: {
        "project": "", "messages": [], "tool": "codex", "first_ts_ms": 0,
    })
    index = codex_session_index()
    cwd_map = {sid: info["cwd"] for sid, info in index.items() if info["cwd"]}

    if CODEX_HISTORY.exists():
        with open(CODEX_HISTORY, encoding="utf-8") as f:
            for line in f:
                try:
                    d = json.loads(line.strip())
                except json.JSONDecodeError:
                    continue
                ts_sec = int(d.get("ts", 0))
                ts_ms = ts_sec * 1000
                if not (start_ms <= ts_ms < end_ms):
                    continue
                sid = d.get("session_id", "")
                if sid not in index:
                    continue
                text = d.get("text", "").strip()
                project = cwd_map.get(sid, "")
                if project_filter and project_filter not in project:
                    continue
                if cwd_filter and not path_matches(project, cwd_filter):
                    continue
                if not sessions[sid]["project"] and project:
                    sessions[sid]["project"] = project
                if not sessions[sid]["first_ts_ms"]:
                    sessions[sid]["first_ts_ms"] = ts_ms
                else:
                    sessions[sid]["first_ts_ms"] = min(sessions[sid]["first_ts_ms"], ts_ms)
                if text:
                    sessions[sid]["messages"].append({"time": ts_to_hm(ts_ms), "text": text[:300]})

    for sid, info in index.items():
        ts_str = info.get("ts", "")
        if not ts_str:
            continue
        try:
            dt = datetime.datetime.fromisoformat(ts_str.replace("Z", "+00:00"))
        except ValueError:
            continue
        ts_ms = int(dt.timestamp() * 1000)
        if not (start_ms <= ts_ms < end_ms):
            continue
        project = info.get("cwd", "")
        if project_filter and project_filter not in project:
            continue
        if cwd_filter and not path_matches(project, cwd_filter):
            continue
        if sid in sessions:
            if not sessions[sid]["project"] and project:
                sessions[sid]["project"] = project
            continue
        entry = sessions[sid]
        entry["project"] = project
        entry["first_ts_ms"] = ts_ms
        first_msg = codex_first_user_message(info["path"])
        if first_msg:
            entry["messages"].append({"time": ts_to_hm(ts_ms), "text": first_msg[:300]})

    return dict(sessions)


# ─── list 서브커맨드 ──────────────────────────────────────────

def format_list_text(sessions, date_label):
    lines = [f"# 세션 히스토리 ({date_label})", ""]
    if not sessions:
        lines.append("세션 기록 없음.")
        return "\n".join(lines)

    claude_sessions = {k: v for k, v in sessions.items() if v.get("tool") == "claude"}
    codex_sessions = {k: v for k, v in sessions.items() if v.get("tool") == "codex"}
    claude_idx = claude_conversation_index()
    codex_idx = codex_session_index()

    for tool_name, tool_sessions, idx in [
        ("Claude Code", claude_sessions, claude_idx),
        ("Codex", codex_sessions, codex_idx),
    ]:
        if not tool_sessions:
            continue
        lines.append(f"## {tool_name} ({len(tool_sessions)}개 세션)")
        lines.append("")
        sorted_items = sorted(tool_sessions.items(), key=lambda kv: kv[1].get("first_ts_ms", 0))
        for sid, info in sorted_items:
            proj = shorten_home(info["project"])
            msg_count = len(info["messages"])
            if not info["messages"]:
                lines.append(f"  {sid[:12]}  {proj}  (메시지 없음)")
            else:
                first = info["messages"][0]["time"]
                last = info["messages"][-1]["time"]
                first_msg = info["messages"][0]["text"].replace("\n", " ")[:80]
                lines.append(f"  {sid[:12]}  {proj}  {first}~{last}  ({msg_count}건)  {first_msg}")
            if tool_name == "Claude Code":
                fpath = idx.get(sid)
            else:
                entry = idx.get(sid)
                fpath = entry["path"] if entry else None
            if fpath:
                lines.append(f"    └ {fpath}")
        lines.append("")

    lines.append(f"총 {len(sessions)}개 세션 (Claude Code: {len(claude_sessions)}, Codex: {len(codex_sessions)})")
    lines.append("")
    lines.append("대화 보기: python3 session_history.py show <세션ID 앞 12자리 이상>")
    lines.append("최근 세션: python3 session_history.py show --last")
    return "\n".join(lines)


def cmd_list(args):
    start_ms, end_ms, label = date_range(args)
    cwd_filter = str(Path.cwd()) if getattr(args, "cwd", False) else None
    sessions = {}
    if args.tool in ("all", "claude"):
        sessions.update(extract_claude_history(start_ms, end_ms, args.project, cwd_filter))
    if args.tool in ("all", "codex"):
        sessions.update(extract_codex_history(start_ms, end_ms, args.project, cwd_filter))

    if getattr(args, "search", None):
        keyword = args.search.lower()
        sessions = {
            sid: info for sid, info in sessions.items()
            if any(keyword in m["text"].lower() for m in info["messages"])
        }

    if args.format == "json":
        print(json.dumps(sessions, ensure_ascii=False, indent=2))
    else:
        print(format_list_text(sessions, label))


# ─── timeline 서브커맨드 ───────────────────────────────────────

def cmd_timeline(args):
    """모든 세션을 시간순으로 나열. 데일리 노트 붙여넣기 용."""
    start_ms, end_ms, label = date_range(args)
    cwd_filter = str(Path.cwd()) if getattr(args, "cwd", False) else None
    sessions = {}
    if args.tool in ("all", "claude"):
        sessions.update(extract_claude_history(start_ms, end_ms, cwd_filter=cwd_filter))
    if args.tool in ("all", "codex"):
        sessions.update(extract_codex_history(start_ms, end_ms, cwd_filter=cwd_filter))

    if not sessions:
        print(f"세션 없음 ({label})")
        return

    # first_ts_ms 기준 정렬
    sorted_sessions = sorted(sessions.items(), key=lambda kv: kv[1].get("first_ts_ms", 0))

    if args.format == "json":
        out = [
            {
                "sid": sid[:12],
                "tool": info["tool"],
                "project": info["project"],
                "time": ts_to_hm(info["first_ts_ms"]) if info["first_ts_ms"] else "",
                "first_msg": info["messages"][0]["text"] if info["messages"] else "",
                "msg_count": len(info["messages"]),
            }
            for sid, info in sorted_sessions
        ]
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return

    lines = [f"# 작업 타임라인 ({label})", ""]

    # 날짜가 여러 개면 날짜별로 그룹
    by_date = defaultdict(list)
    for sid, info in sorted_sessions:
        if info["first_ts_ms"]:
            day = datetime.datetime.fromtimestamp(info["first_ts_ms"] / 1000).strftime("%Y-%m-%d")
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
            tool_tag = "[C]" if info["tool"] == "claude" else "[X]"
            msg_count = len(info["messages"])
            first_msg = info["messages"][0]["text"].replace("\n", " ")[:100] if info["messages"] else "(메시지 없음)"
            lines.append(f"{time_str}  {tool_tag} [{proj}]  {first_msg}  ({msg_count}건)")
            # 후속 메시지 중 주요 분기점 (메시지 수 많으면 중간 스냅샷)
            if msg_count >= 5 and not getattr(args, "compact", False):
                mid = info["messages"][msg_count // 2]
                mid_text = mid["text"].replace("\n", " ")[:80]
                lines.append(f"       ↳ {mid['time']}  {mid_text}")
        lines.append("")

    lines.append(f"총 {len(sorted_sessions)}개 세션")
    lines.append("[C]=Claude Code  [X]=Codex")
    print("\n".join(lines))


# ─── grep 서브커맨드 ───────────────────────────────────────────

def grep_claude_session(fpath: Path, keyword: str, context_lines: int = 0):
    """Claude Code 세션 JSONL에서 keyword 포함 대화·도구 기록 반환."""
    hits = []
    keyword_lower = keyword.lower()
    messages = []

    def add_message(role, text, ts):
        if isinstance(text, str) and text.strip():
            messages.append({"role": role, "text": text.strip(), "ts": ts})

    with open(fpath, encoding="utf-8") as f:
        for line in f:
            try:
                d = json.loads(line.strip())
            except json.JSONDecodeError:
                continue
            entry_type = d.get("type", "")
            ts = d.get("timestamp", "")
            if entry_type == "user":
                msg = d.get("message", {})
                content = msg.get("content", "")
                if isinstance(content, list):
                    for c in content:
                        if isinstance(c, dict) and c.get("type") == "text":
                            add_message("user", c.get("text", ""), ts)
                        elif isinstance(c, dict) and c.get("type") == "tool_result":
                            add_message("tool", c.get("content", ""), ts)
                        elif isinstance(c, str):
                            add_message("user", c, ts)
                else:
                    add_message("user", content, ts)
            elif entry_type == "assistant":
                for part in d.get("message", {}).get("content", []) or []:
                    if isinstance(part, dict) and part.get("type") == "text":
                        add_message("assistant", part.get("text", ""), ts)
                    elif isinstance(part, dict) and part.get("type") == "tool_use":
                        name = part.get("name", "")
                        inp = json.dumps(part.get("input", {}) or {}, ensure_ascii=False)
                        add_message("tool", f"[tool: {name}] {inp}", ts)
            elif entry_type == "tool_result":
                msg = d.get("message", {})
                content = msg.get("content", "")
                if isinstance(content, list):
                    for part in content:
                        if isinstance(part, dict):
                            add_message("tool", part.get("content", ""), ts)
                else:
                    add_message("tool", content, ts)

    for i, msg in enumerate(messages):
        if keyword_lower in msg["text"].lower():
            snippet = msg["text"]
            # keyword 주변 150자
            idx = snippet.lower().find(keyword_lower)
            start = max(0, idx - 60)
            end = min(len(snippet), idx + len(keyword) + 90)
            excerpt = ("..." if start > 0 else "") + snippet[start:end] + ("..." if end < len(snippet) else "")
            hits.append({
                "role": msg["role"],
                "ts": msg["ts"],
                "excerpt": excerpt.replace("\n", " "),
            })

    return hits


def grep_codex_session(fpath: Path, keyword: str):
    """Codex rollout JSONL에서 keyword 포함 대화·도구 기록 반환."""
    hits = []
    keyword_lower = keyword.lower()

    def add_hit(role, text, ts):
        if not isinstance(text, str) or keyword_lower not in text.lower():
            return
        idx = text.lower().find(keyword_lower)
        start = max(0, idx - 60)
        end = min(len(text), idx + len(keyword) + 90)
        excerpt = ("..." if start > 0 else "") + text[start:end] + ("..." if end < len(text) else "")
        hits.append({
            "role": role,
            "ts": ts,
            "excerpt": excerpt.replace("\n", " "),
        })

    with open(fpath, encoding="utf-8") as f:
        for line in f:
            try:
                d = json.loads(line.strip())
            except json.JSONDecodeError:
                continue
            entry_type = d.get("type")
            payload = d.get("payload", {}) or {}
            ts = d.get("timestamp", "")
            if entry_type == "event_msg":
                msg_type = payload.get("type", "")
                if msg_type in ("user_message", "agent_message"):
                    role = "user" if msg_type == "user_message" else "assistant"
                    add_hit(role, (payload.get("message", "") or "").strip(), ts)
                elif msg_type == "patch_apply_begin":
                    add_hit("tool", json.dumps(payload.get("changes", {}) or {}, ensure_ascii=False), ts)
                continue
            if entry_type != "response_item":
                continue
            rtype = payload.get("type", "")
            if rtype in ("function_call", "custom_tool_call"):
                raw = payload.get("arguments", "") or payload.get("input", "")
                if not isinstance(raw, str):
                    raw = json.dumps(raw, ensure_ascii=False)
                add_hit("tool", f"[{payload.get('name', '')}] {raw}", ts)
            elif rtype in ("function_call_output", "custom_tool_call_output"):
                output = payload.get("output", "")
                if not isinstance(output, str):
                    output = json.dumps(output, ensure_ascii=False)
                add_hit("tool", output, ts)
    return hits


def cmd_grep(args):
    """세션 파일 전문 검색. history.jsonl preview가 아닌 실제 대화·도구 기록 검색."""
    keyword = args.keyword
    start_ms, end_ms, label = date_range(args)
    cwd_filter = str(Path.cwd()) if getattr(args, "cwd", False) else None

    # 대상 세션 목록 수집 (날짜 필터 + cwd 필터)
    sessions = {}
    if args.tool in ("all", "claude"):
        sessions.update(extract_claude_history(start_ms, end_ms, cwd_filter=cwd_filter))
    if args.tool in ("all", "codex"):
        sessions.update(extract_codex_history(start_ms, end_ms, cwd_filter=cwd_filter))

    claude_idx = claude_conversation_index()
    codex_idx = codex_session_index()

    results = []  # [{sid, tool, project, first_ts_ms, hits, fpath}]

    for sid, info in sessions.items():
        tool = info["tool"]
        if tool == "claude":
            fpath = claude_idx.get(sid)
            if not fpath or not fpath.exists():
                continue
            try:
                hits = grep_claude_session(fpath, keyword)
            except OSError:
                continue
        else:
            entry = codex_idx.get(sid)
            if not entry:
                continue
            fpath = entry["path"]
            if not fpath.exists():
                continue
            try:
                hits = grep_codex_session(fpath, keyword)
            except OSError:
                continue

        if hits:
            results.append({
                "sid": sid,
                "tool": tool,
                "project": info["project"],
                "first_ts_ms": info.get("first_ts_ms", 0),
                "hits": hits,
                "fpath": fpath,
            })

    results.sort(key=lambda r: r["first_ts_ms"])
    if getattr(args, "limit", None) is not None:
        results = results[:args.limit]

    if args.format == "json":
        out = [{**r, "fpath": str(r["fpath"]), "sid": r["sid"]} for r in results]
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return

    command_label = "rg" if getattr(args, "command", "") == "rg" else "grep"
    lines = [f'# {command_label}: "{keyword}" ({label})', ""]
    if not results:
        lines.append("매칭 없음.")
        print("\n".join(lines))
        return

    lines.append(f"{len(results)}개 세션에서 발견")
    lines.append("─" * 60)

    for r in results:
        proj = shorten_home(r["project"])
        time_str = ts_to_hm(r["first_ts_ms"]) if r["first_ts_ms"] else "??"
        tool_tag = "[Claude]" if r["tool"] == "claude" else "[Codex]"
        lines.append(f"\n{tool_tag} {r['sid'][:12]}  {proj}  {time_str}")
        lines.append(f"  파일: {r['fpath']}")
        for hit in r["hits"][:3]:  # 세션당 최대 3건
            role_icon = {"user": "👤", "assistant": "🤖"}.get(hit["role"], "🔧")
            # ts 파싱
            try:
                if isinstance(hit["ts"], str):
                    dt = datetime.datetime.fromisoformat(hit["ts"].replace("Z", "+00:00"))
                    t = dt.strftime("%H:%M:%S")
                else:
                    t = ts_to_hms(hit["ts"])
            except Exception:
                t = ""
            lines.append(f"  {role_icon} {t}  {hit['excerpt']}")
        if len(r["hits"]) > 3:
            lines.append(f"  ... 외 {len(r['hits']) - 3}건 더")

    lines.append("")
    lines.append("─" * 60)
    lines.append(f"총 {sum(len(r['hits']) for r in results)}건 ({len(results)}개 세션)")
    lines.append("전체 보기: python3 session_history.py show <세션ID>")
    print("\n".join(lines))


# ─── show 서브커맨드 ──────────────────────────────────────────

def find_session(session_prefix: str, tool_filter: str = "all"):
    results = []
    if tool_filter in ("all", "claude"):
        for sid in claude_conversation_index():
            if sid.startswith(session_prefix):
                results.append(("claude", sid))
    if tool_filter in ("all", "codex"):
        for sid in codex_session_index():
            if sid.startswith(session_prefix):
                results.append(("codex", sid))
    return results


def find_latest_session(tool_filter: str = "all"):
    for days in (1, 7):
        ns = argparse.Namespace(date=None, days=days)
        start_ms, end_ms, _ = date_range(ns)
        sessions = {}
        if tool_filter in ("all", "claude"):
            sessions.update(extract_claude_history(start_ms, end_ms))
        if tool_filter in ("all", "codex"):
            sessions.update(extract_codex_history(start_ms, end_ms))
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
    count_label = f"{len(messages)}/{total}건 (--limit {limit})" if truncated else f"{total}건"
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
                    time_str = datetime.datetime.fromtimestamp(ts / 1000).strftime("%H:%M:%S")
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
    full = args.full
    limit = getattr(args, "limit", None)

    if getattr(args, "files", False):
        if tool == "claude":
            changes, bash_hints = extract_claude_changed_files(session_id)
            fpath = find_claude_conversation_file(session_id)
            tool_name = "Claude Code"
        else:
            changes, bash_hints = extract_codex_changed_files(session_id)
            fpath = find_codex_session_file(session_id)
            tool_name = "Codex"

        if changes is None:
            print(f"세션 파일을 찾을 수 없습니다: {session_id}")
            sys.exit(1)

        if args.format == "json":
            print(json.dumps({"changes": changes, "bash_hints": bash_hints}, ensure_ascii=False, indent=2))
        else:
            print(format_changed_files(changes, bash_hints, tool_name, session_id, fpath=fpath))
        return

    if tool == "claude":
        messages, fpath = read_claude_conversation(session_id, full)
        tool_name = "Claude Code"
    else:
        messages, fpath = read_codex_conversation(session_id, full)
        tool_name = "Codex"

    if messages is None:
        print(f"세션 파일을 찾을 수 없습니다: {session_id}")
        sys.exit(1)

    if args.format == "json":
        print(json.dumps(messages, ensure_ascii=False, indent=2))
    else:
        print(format_conversation(messages, tool_name, session_id, full, fpath=fpath, limit=limit))


# ─── main ─────────────────────────────────────────────────────

def main():
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--tool", choices=["all", "claude", "codex"], default="all")
    common.add_argument("--format", choices=["text", "json"], default="text")
    common.add_argument("--include-subagents", action="store_true",
                        help="subagent 세션도 포함 (기본: 제외)")

    parser = argparse.ArgumentParser(
        description="Claude Code + Codex 통합 세션 히스토리",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=[common],
        epilog="""
예시:
  %(prog)s                                 오늘 세션 목록
  %(prog)s list --cwd                      현재 디렉토리 프로젝트만
  %(prog)s list --search pytest            키워드 검색 (preview)
  %(prog)s timeline                        오늘 타임라인 (데일리 노트용)
  %(prog)s timeline --days 3 --cwd         현재 프로젝트 3일 타임라인
  %(prog)s rg "gcloud"                     대화·도구 기록 검색
  %(prog)s rg "gcloud" --days 14           14일간 대화·도구 기록 검색
  %(prog)s show --last                     가장 최근 세션
  %(prog)s show abc12345 --files           수정된 파일 목록
  %(prog)s show abc12345 --limit 20        앞 20개 메시지만
""",
    )

    subparsers = parser.add_subparsers(dest="command")

    # list
    list_parser = subparsers.add_parser("list", help="세션 목록 조회", parents=[common])
    list_parser.add_argument("--date", help="조회할 날짜 (YYYY-MM-DD)")
    list_parser.add_argument("--days", type=int, default=1, help="최근 N일 (기본: 1)")
    list_parser.add_argument("--project", help="특정 프로젝트 경로 필터")
    list_parser.add_argument("--cwd", action="store_true",
                              help="현재 작업 디렉토리 기준으로 프로젝트 필터")
    list_parser.add_argument("--search", help="메시지 텍스트 키워드 필터 (preview 기준)")

    # timeline
    tl_parser = subparsers.add_parser("timeline", help="오늘 작업 시간순 타임라인", parents=[common])
    tl_parser.add_argument("--date", help="조회할 날짜 (YYYY-MM-DD)")
    tl_parser.add_argument("--days", type=int, default=1, help="최근 N일 (기본: 1)")
    tl_parser.add_argument("--cwd", action="store_true", help="현재 디렉토리 프로젝트만")
    tl_parser.add_argument("--compact", action="store_true", help="중간 스냅샷 생략")

    # grep
    grep_parser = subparsers.add_parser("grep", aliases=["rg"], help="세션 전문 검색 (대화·도구 기록)", parents=[common])
    grep_parser.add_argument("keyword", help="검색할 키워드")
    grep_parser.add_argument("--days", type=int, default=7, help="최근 N일 (기본: 7)")
    grep_parser.add_argument("--date", help="조회할 날짜 (YYYY-MM-DD)")
    grep_parser.add_argument("--cwd", action="store_true", help="현재 디렉토리 프로젝트만")
    grep_parser.add_argument("--limit", type=int, default=None, help="결과 세션 최대 N개")

    # show
    show_parser = subparsers.add_parser("show", help="특정 세션 대화 보기", parents=[common])
    show_parser.add_argument("session", nargs="?", default=None,
                             help="세션 ID (앞 12자리 이상 권장)")
    show_parser.add_argument("--last", action="store_true", help="가장 최근 세션 보기")
    show_parser.add_argument("--full", action="store_true", help="도구 호출/결과 포함")
    show_parser.add_argument("--files", action="store_true", help="수정된 파일 목록만")
    show_parser.add_argument("--limit", type=int, default=None, help="앞 N개 메시지만")

    args = parser.parse_args()
    set_include_subagents(getattr(args, "include_subagents", False))

    if args.command is None or args.command == "list":
        if not hasattr(args, "date"):   args.date = None
        if not hasattr(args, "days"):   args.days = 1
        if not hasattr(args, "project"): args.project = None
        if not hasattr(args, "cwd"):    args.cwd = False
        if not hasattr(args, "search"): args.search = None
        cmd_list(args)
    elif args.command == "timeline":
        cmd_timeline(args)
    elif args.command in ("grep", "rg"):
        cmd_grep(args)
    elif args.command == "show":
        cmd_show(args)


if __name__ == "__main__":
    main()
