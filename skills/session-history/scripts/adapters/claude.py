"""Claude Code session adapter."""

from __future__ import annotations

import functools
import json
import os
import re
from collections import defaultdict
from pathlib import Path

from common import (
    BASH_MUTATION_RE,
    CLAUDE_DESKTOP_LOCAL_SESSIONS_DIR,
    CLAUDE_DESKTOP_SESSIONS_DIR,
    CLAUDE_HISTORY,
    CLAUDE_LOCAL_PROJECT_ROOTS,
    CLAUDE_PROJECTS_DIR,
    include_subagents,
    iso_to_ms,
    path_matches,
    register_cache_clearer,
    ts_to_hm,
)

TOOL = "claude"
DISPLAY = "Claude Code"
TAG = "[C]"
EDIT_TOOLS = {"Edit", "Write", "MultiEdit", "NotebookEdit"}
SOURCE_PATHS = (
    CLAUDE_PROJECTS_DIR,
    *CLAUDE_LOCAL_PROJECT_ROOTS,
    CLAUDE_DESKTOP_SESSIONS_DIR,
    CLAUDE_DESKTOP_LOCAL_SESSIONS_DIR,
)

# transcript 앞부분에는 주입 컨텍스트가 먼저 오므로 첫 사용자 발화까지 여유를 둔다.
_META_SCAN_MAX_LINES = 200

_SYSTEM_REMINDER_RE = re.compile(r"<system-reminder>.*?</system-reminder>", re.DOTALL)
_COMMAND_NAME_RE = re.compile(r"<command-name>(.*?)</command-name>", re.DOTALL)
_COMMAND_ARGS_RE = re.compile(r"<command-args>(.*?)</command-args>", re.DOTALL)
_META_PREFIXES = (
    "<local-command-stdout>",
    "<local-command-stderr>",
    "<user-prompt-submit-hook>",
    "<command-message>",
    "Caveat:",
)


def _claude_user_entry_text(entry: dict) -> str:
    """user record의 텍스트만 모은다. tool_result 블록은 대화가 아니라 도구 출력이다."""
    content = (entry.get("message") or {}).get("content", "")
    if isinstance(content, str):
        return content
    if not isinstance(content, list):
        return ""
    parts = []
    for part in content:
        if isinstance(part, str):
            parts.append(part)
        elif isinstance(part, dict) and part.get("type") == "text":
            parts.append(part.get("text") or "")
    return "\n".join(parts)


def _real_user_text(text: str) -> str:
    """주입 컨텍스트를 걷어내고 사용자가 실제로 입력한 문장만 남긴다."""
    if not text:
        return ""
    text = _SYSTEM_REMINDER_RE.sub("", text)
    args_match = _COMMAND_ARGS_RE.search(text)
    if args_match:
        # 슬래시 커맨드는 이름과 인자를 합쳐야 history.jsonl의 표시 문자열과 같아진다.
        name_match = _COMMAND_NAME_RE.search(text)
        body = args_match.group(1).strip()
        name = name_match.group(1).strip() if name_match else ""
        return f"{name} {body}".strip()
    stripped = text.strip()
    if stripped.startswith(_META_PREFIXES):
        return ""
    return stripped


def _claude_transcript_roots():
    roots = [(CLAUDE_PROJECTS_DIR, False)]
    roots.extend((root, False) for root in CLAUDE_LOCAL_PROJECT_ROOTS)
    roots.append((CLAUDE_DESKTOP_LOCAL_SESSIONS_DIR, True))
    return roots


def _iter_claude_conversation_files(include_subagent_files: bool):
    """transcript 경로를 순회한다. subagent 트리는 제외 시 아예 걷지 않는다."""
    for root_dir, bridge_only in _claude_transcript_roots():
        if not root_dir.exists():
            continue
        for dirpath, dirnames, filenames in os.walk(root_dir):
            if not include_subagent_files and "subagents" in dirnames:
                dirnames.remove("subagents")
            if bridge_only and "/.claude/projects/" not in f"{dirpath}/":
                continue
            for name in filenames:
                if name.endswith(".jsonl"):
                    yield Path(dirpath) / name


def _desktop_project(data: dict) -> str:
    folders = data.get("userSelectedFolders") or []
    for folder in folders:
        if isinstance(folder, str) and folder.startswith("/"):
            return folder
        if isinstance(folder, dict):
            path = folder.get("path") or folder.get("uri") or ""
            if isinstance(path, str) and path.startswith("/"):
                return path
    return data.get("originCwd") or data.get("cwd") or ""


@functools.lru_cache(maxsize=1)
def claude_desktop_metadata():
    """cliSessionId -> Claude Desktop/Cowork metadata."""
    idx = {}
    for root in (CLAUDE_DESKTOP_SESSIONS_DIR, CLAUDE_DESKTOP_LOCAL_SESSIONS_DIR):
        if not root.exists():
            continue
        for path in root.rglob("local_*.json"):
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
            sid = data.get("cliSessionId") or ""
            if not sid:
                continue
            idx[sid] = {
                **data,
                "metadata_path": path,
                "project": _desktop_project(data),
            }
    return idx


@functools.lru_cache(maxsize=1)
def claude_conversation_index():
    """session_id (stem) → conversation jsonl Path."""
    return {sid: path for sid, (path, _) in claude_transcript_mtimes().items()}


def _scan_claude_transcript(path: Path) -> dict:
    """transcript 앞부분에서 cwd, 최초 시각, 최초 사용자 발화를 뽑는다.

    첫 줄은 last-prompt·mode 같은 메타 record라 cwd와 timestamp가 없는 경우가 많다.
    """
    cwd = ""
    ts = ""
    first_user = ""
    try:
        with path.open(encoding="utf-8") as fh:
            for line_no, line in enumerate(fh):
                if line_no >= _META_SCAN_MAX_LINES:
                    break
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if not cwd:
                    cwd = entry.get("cwd") or ""
                if not ts:
                    ts = entry.get("timestamp") or ""
                if (
                    not first_user
                    and entry.get("type") == "user"
                    and not entry.get("isMeta")
                ):
                    first_user = _real_user_text(_claude_user_entry_text(entry))
                if cwd and ts and first_user:
                    break
    except OSError:
        pass
    ts_ms = iso_to_ms(ts)
    if not ts_ms:
        # 시각 record가 없는 transcript도 파일 수정 시각으로 날짜 범위에 들어와야 한다.
        try:
            ts_ms = int(path.stat().st_mtime * 1000)
        except OSError:
            ts_ms = 0
    return {"path": path, "cwd": cwd, "ts_ms": ts_ms, "first_user": first_user}


@functools.lru_cache(maxsize=1)
def claude_transcript_mtimes():
    """session_id → (path, mtime_ms). 범위 밖 transcript를 열지 않기 위한 색인."""
    idx = {}
    for fpath in _iter_claude_conversation_files(include_subagents()):
        if fpath.stem in idx:
            continue
        try:
            mtime_ms = int(fpath.stat().st_mtime * 1000)
        except OSError:
            mtime_ms = 0
        idx[fpath.stem] = (fpath, mtime_ms)
    return idx


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
                if d.get("isMeta"):
                    # 스킬 본문·런타임 컨텍스트 주입은 사용자 발화가 아니다.
                    continue
                text = _real_user_text(_claude_user_entry_text(d))
                if text:
                    messages.append({"role": "user", "text": text, "ts": ts})

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
                    messages.append(
                        {
                            "role": "assistant",
                            "text": text.strip(),
                            "ts": ts,
                            "model": msg.get("model", ""),
                        }
                    )

            elif entry_type == "tool_result" and full:
                msg = d.get("message", {})
                content = msg.get("content", [])
                for part in content:
                    if isinstance(part, dict) and part.get("type") == "tool_result":
                        result_text = part.get("content", "")
                        if isinstance(result_text, str) and result_text.strip():
                            messages.append(
                                {"role": "tool", "text": result_text[:500], "ts": ts}
                            )

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
                if name in EDIT_TOOLS:
                    path = inp.get("file_path") or inp.get("notebook_path") or ""
                    if path:
                        changes.append({"file": path, "tool": name, "ts": ts})
                elif name == "Bash":
                    cmd = inp.get("command", "")
                    if cmd and BASH_MUTATION_RE.search(cmd):
                        bash_hints.append({"cmd": cmd, "ts": ts})
    return changes, bash_hints


# ─── Codex session IO ──────────────────────────────────────────


def extract_claude_history(start_ms, end_ms, project_filter=None, cwd_filter=None):
    sessions = defaultdict(
        lambda: {
            "project": "",
            "messages": [],
            "tool": "claude",
            "first_ts_ms": 0,
        }
    )
    if CLAUDE_HISTORY.exists():
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
                if not sid:
                    # sessionId 없는 줄을 모으면 서로 다른 프로젝트의 프롬프트가
                    # 하나의 가짜 세션으로 합쳐진다.
                    continue
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
                    sessions[sid]["messages"].append(
                        {"time": ts_to_hm(ts), "text": display[:300]}
                    )

    # Claude Desktop and Cowork do not consistently append to ~/.claude/history.
    # Their metadata links the UI session to the real Claude Code transcript.
    transcript_index = claude_conversation_index()
    for sid, meta in claude_desktop_metadata().items():
        if sid in sessions:
            continue
        ts = iso_to_ms(meta.get("createdAt") or meta.get("lastActivityAt"))
        if not ts or not (start_ms <= ts < end_ms):
            continue
        project = meta.get("project") or ""
        if project_filter and project_filter not in project:
            continue
        if cwd_filter and not path_matches(project, cwd_filter):
            continue
        display = ""
        fpath = transcript_index.get(sid)
        if fpath:
            try:
                with fpath.open(encoding="utf-8") as fh:
                    for line in fh:
                        try:
                            entry = json.loads(line)
                        except json.JSONDecodeError:
                            continue
                        if entry.get("type") != "user":
                            continue
                        content = (entry.get("message") or {}).get("content", "")
                        if isinstance(content, str):
                            display = content.strip()
                        elif isinstance(content, list):
                            display = "\n".join(
                                part.get("text", "")
                                for part in content
                                if isinstance(part, dict) and part.get("type") == "text"
                            ).strip()
                        if display:
                            break
            except OSError:
                display = ""
        display = (
            display
            or str(meta.get("initialMessage") or meta.get("title") or "").strip()
        )
        sessions[sid]["project"] = project
        sessions[sid]["first_ts_ms"] = ts
        if display:
            sessions[sid]["messages"].append(
                {"time": ts_to_hm(ts), "text": display[:300]}
            )

    # history.jsonl은 대화형 입력만 기록한다. transcript가 정본이므로 여기서 채운다.
    for sid, (path, mtime_ms) in claude_transcript_mtimes().items():
        if sid in sessions:
            continue
        # 마지막 기록이 조회 범위보다 이르면 세션 시작도 범위 밖이다.
        if mtime_ms < start_ms:
            continue
        meta = _scan_claude_transcript(path)
        ts = meta["ts_ms"]
        if not ts or not (start_ms <= ts < end_ms):
            continue
        project = meta["cwd"]
        if project_filter and project_filter not in project:
            continue
        if cwd_filter and not path_matches(project, cwd_filter):
            continue
        entry = sessions[sid]
        entry["project"] = project
        entry["first_ts_ms"] = ts
        if meta["first_user"]:
            entry["messages"].append(
                {"time": ts_to_hm(ts), "text": meta["first_user"][:300]}
            )
    return dict(sessions)


def grep_claude_session(
    fpath: Path, keyword: str, context_lines: int = 0, session_id: str | None = None
):
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
                        inp = json.dumps(
                            part.get("input", {}) or {}, ensure_ascii=False
                        )
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
            excerpt = (
                ("..." if start > 0 else "")
                + snippet[start:end]
                + ("..." if end < len(snippet) else "")
            )
            hits.append(
                {
                    "role": msg["role"],
                    "ts": msg["ts"],
                    "excerpt": excerpt.replace("\n", " "),
                }
            )

    return hits


# Public adapter surface (stable names for CLI)
session_index = claude_conversation_index
find_session_file = find_claude_conversation_file
read_conversation = read_claude_conversation
extract_changed_files = extract_claude_changed_files
extract_history = extract_claude_history
grep_session = grep_claude_session

register_cache_clearer(claude_conversation_index.cache_clear)
register_cache_clearer(claude_transcript_mtimes.cache_clear)
register_cache_clearer(claude_desktop_metadata.cache_clear)


def source_notes():
    """sources의 세션 수와 list 결과가 다른 이유를 밝힌다."""
    indexed = set(claude_conversation_index())
    history_only = set()
    if CLAUDE_HISTORY.exists():
        try:
            with CLAUDE_HISTORY.open(encoding="utf-8") as fh:
                for line in fh:
                    try:
                        sid = json.loads(line).get("sessionId") or ""
                    except json.JSONDecodeError:
                        continue
                    if sid and sid not in indexed:
                        history_only.add(sid)
        except OSError:
            return []
    notes = ["위 수치는 transcript 기준이며 show·rg로 열람 가능한 세션 수다"]
    if history_only:
        notes.append(
            f"프롬프트 기록만 남은 세션 {len(history_only)}개는 list에는 나오지만 "
            "show는 실패한다 (Claude Code가 오래된 transcript를 정리)"
        )
    return notes


# ─── token usage ───────────────────────────────────────────────

SHORT = "Claude"


def add_token_usage(totals, usage):
    input_tokens = int(usage.get("input_tokens") or 0)
    output_tokens = int(usage.get("output_tokens") or 0)
    cache_create = int(usage.get("cache_creation_input_tokens") or 0)
    cache_read = int(usage.get("cache_read_input_tokens") or 0)
    cache_5m = int(usage.get("cache_creation_5m_tokens") or 0)
    cache_1h = int(usage.get("cache_creation_1h_tokens") or 0)
    totals["input_tokens"] += input_tokens
    totals["output_tokens"] += output_tokens
    totals["cache_creation_input_tokens"] += cache_create
    totals["cache_read_input_tokens"] += cache_read
    totals["cache_creation_5m_tokens"] += cache_5m
    totals["cache_creation_1h_tokens"] += cache_1h
    totals["total_tokens"] += input_tokens + output_tokens + cache_create + cache_read
    totals["effective_tokens"] += input_tokens + output_tokens + cache_create
    totals["pure_tokens"] += input_tokens + output_tokens
    totals["cache_tokens"] += cache_read
    totals["calls"] += 1


def collect_token_rows(start, end, args):
    from pathlib import Path

    from common import CLAUDE_PROJECTS_DIR, in_range, parse_ts, path_matches

    rows_by_request = {}
    if (
        not CLAUDE_PROJECTS_DIR.exists()
        and not CLAUDE_DESKTOP_LOCAL_SESSIONS_DIR.exists()
    ):
        return []

    def is_subagent_path(path: Path) -> bool:
        return "/subagents/" in str(path)

    include_subagent_files = not getattr(args, "main_only", False)
    for path in _iter_claude_conversation_files(include_subagent_files):
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
                if getattr(args, "cwd", False) and not path_matches(
                    cwd, str(Path.cwd())
                ):
                    continue
                if getattr(args, "project", None) and args.project not in cwd:
                    continue

                request_id = (
                    entry.get("requestId") or message.get("id") or f"{path}:{line_no}"
                )
                cache_creation = usage.get("cache_creation") or {}
                if not isinstance(cache_creation, dict):
                    cache_creation = {}
                cache_5m = int(cache_creation.get("ephemeral_5m_input_tokens") or 0)
                cache_1h = int(cache_creation.get("ephemeral_1h_input_tokens") or 0)
                cache_create_total = int(usage.get("cache_creation_input_tokens") or 0)
                # Prefer explicit 5m/1h split; fall back to total when split missing.
                if cache_5m == 0 and cache_1h == 0 and cache_create_total:
                    cache_5m = cache_create_total
                row = {
                    "tool": TOOL,
                    "timestamp": timestamp.isoformat() if timestamp else None,
                    "session_id": entry.get("sessionId") or path.stem,
                    "cwd": cwd,
                    "path": str(path),
                    "model": message.get("model") or "",
                    "subagent": (
                        is_subagent_path(path)
                        or bool(entry.get("isSidechain"))
                        or bool(entry.get("attributionAgent"))
                    ),
                    "input_tokens": int(usage.get("input_tokens") or 0),
                    "output_tokens": int(usage.get("output_tokens") or 0),
                    "cache_creation_input_tokens": cache_create_total,
                    "cache_creation_5m_tokens": cache_5m,
                    "cache_creation_1h_tokens": cache_1h,
                    "cache_read_input_tokens": int(
                        usage.get("cache_read_input_tokens") or 0
                    ),
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
