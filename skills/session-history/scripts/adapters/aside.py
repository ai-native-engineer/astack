"""Aside browser agent session adapter.

프로필별로 `~/.aside/u/<n>/state.db`가 메타를, `sessions/<날짜>_<id>/messages.jsonl`이
대화를 담는다. state.db의 시각은 epoch seconds, messages.jsonl은 epoch ms다.
"""

from __future__ import annotations

import contextlib
import functools
import json
import sqlite3
from pathlib import Path

from common import (
    ASIDE_PROFILES_DIR,
    include_subagents,
    path_matches,
    register_cache_clearer,
    ts_to_hm,
)

TOOL = "aside"
DISPLAY = "Aside"
SHORT = "Aside"
TAG = "[A]"
SOURCE_PATHS = (ASIDE_PROFILES_DIR,)

EDIT_TOOLS = {"write", "edit", "str_replace", "create_file", "apply_patch"}


def _profiles():
    if not ASIDE_PROFILES_DIR.is_dir():
        return []
    return sorted(p for p in ASIDE_PROFILES_DIR.iterdir() if p.is_dir())


def _loads(raw):
    if not raw:
        return {}
    try:
        value = json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        return {}
    return value


def _sec_to_ms(value) -> int:
    """state.db는 초, messages.jsonl은 밀리초를 쓴다."""
    try:
        number = int(value or 0)
    except (TypeError, ValueError):
        return 0
    return number * 1000 if 0 < number < 10**12 else number


def _profile_meta(profile: Path) -> dict:
    db = profile / "state.db"
    meta: dict[str, dict] = {}
    if not db.exists():
        return meta
    try:
        con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    except sqlite3.Error:
        return meta
    with contextlib.closing(con):
        try:
            rows = con.execute(
                "select id, title, model, cwd, created_at, parent_id from sessions"
            ).fetchall()
        except sqlite3.Error:
            return meta
        for sid, title, model, cwd, created, parent in rows:
            meta[sid] = {
                "title": title or "",
                "model": _loads(model).get("modelId", ""),
                "cwd": cwd or "",
                "ts": _sec_to_ms(created),
                "subagent": parent is not None,
            }
    return meta


@functools.lru_cache(maxsize=1)
def aside_session_index():
    """session_id → {path, cwd, ts, title, model, subagent, db}."""
    idx: dict[str, dict] = {}
    for profile in _profiles():
        meta = _profile_meta(profile)
        sessions_dir = profile / "sessions"
        if not sessions_dir.is_dir():
            continue
        for session_dir in sorted(sessions_dir.iterdir()):
            messages = session_dir / "messages.jsonl"
            try:
                if not messages.is_file() or messages.stat().st_size == 0:
                    continue
            except OSError:
                continue
            # 디렉토리는 `YYYY-MM-DD_<session-id>` 형태다.
            sid = session_dir.name.split("_", 1)[-1]
            info = dict(meta.get(sid) or {})
            if info.get("subagent") and not include_subagents():
                continue
            if not info.get("ts"):
                try:
                    info["ts"] = int(messages.stat().st_mtime * 1000)
                except OSError:
                    info["ts"] = 0
            info.setdefault("cwd", "")
            info.setdefault("title", "")
            info.setdefault("model", "")
            info.setdefault("subagent", False)
            info["path"] = messages
            info["db"] = profile / "state.db"
            idx[sid] = info
    return idx


def find_aside_session_file(session_id: str) -> Path | None:
    _, info = _resolve(session_id)
    return info["path"] if info else None


def _resolve(session_id: str):
    idx = aside_session_index()
    if session_id in idx:
        return session_id, idx[session_id]
    for sid, info in idx.items():
        if sid.startswith(session_id):
            return sid, info
    return None, None


def _content_text(content, include_thinking: bool = False) -> str:
    if isinstance(content, str):
        return content
    if not isinstance(content, list):
        return ""
    parts = []
    for part in content:
        if not isinstance(part, dict):
            continue
        ptype = part.get("type")
        if ptype == "text":
            parts.append(part.get("text") or "")
        elif ptype == "thinking" and include_thinking:
            parts.append(part.get("thinking") or "")
    return "\n".join(p for p in parts if p)


def _iter_lines(path: Path):
    try:
        fh = path.open(encoding="utf-8", errors="replace")
    except OSError:
        return
    with fh:
        for line in fh:
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue


def read_aside_conversation(session_id: str, full: bool = False):
    _, info = _resolve(session_id)
    if not info:
        return None, None

    messages = []
    for entry in _iter_lines(info["path"]):
        role = entry.get("role")
        ts = entry.get("timestamp")
        if role == "user":
            text = _content_text(entry.get("content")).strip()
            if text:
                messages.append({"role": "user", "text": text, "ts": ts})
        elif role == "assistant":
            text = _content_text(entry.get("content")).strip()
            if full:
                for part in entry.get("content") or []:
                    if isinstance(part, dict) and part.get("type") == "toolUse":
                        args = json.dumps(part.get("input") or {}, ensure_ascii=False)
                        text += f"\n[tool: {part.get('name', '')}] {args[:200]}"
            if text.strip():
                messages.append(
                    {
                        "role": "assistant",
                        "text": text.strip(),
                        "ts": ts,
                        "model": entry.get("model") or info.get("model", ""),
                    }
                )
        elif role == "toolResult" and full:
            text = _content_text(entry.get("content")).strip()
            if text:
                messages.append({"role": "tool_result", "text": text[:500], "ts": ts})
        # system-message와 user-message-metadata는 사람 발화가 아니다.
    return messages, info["path"]


def extract_aside_changed_files(session_id: str):
    sid, info = _resolve(session_id)
    if not info:
        return None, None

    changes: list[dict] = []
    bash_hints: list[dict] = []
    seen: set = set()

    db = info.get("db")
    if db and db.exists():
        try:
            con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
        except sqlite3.Error:
            con = None
        if con is not None:
            with contextlib.closing(con):
                try:
                    rows = con.execute(
                        "select files_changed, started_at from session_runs"
                        " where session_id = ?",
                        (sid,),
                    ).fetchall()
                except sqlite3.Error:
                    rows = []
                for raw, started in rows:
                    for file_path in _loads(raw) or []:
                        name = (
                            file_path.get("path")
                            if isinstance(file_path, dict)
                            else file_path
                        )
                        if name and name not in seen:
                            seen.add(name)
                            changes.append(
                                {
                                    "file": name,
                                    "tool": "session_run",
                                    "ts": _sec_to_ms(started),
                                }
                            )

    from common import BASH_MUTATION_RE

    for entry in _iter_lines(info["path"]):
        if entry.get("role") != "assistant":
            continue
        for part in entry.get("content") or []:
            if not isinstance(part, dict) or part.get("type") != "toolUse":
                continue
            name = part.get("name", "")
            inp = part.get("input") or {}
            if not isinstance(inp, dict):
                continue
            if name in EDIT_TOOLS:
                target = inp.get("path") or inp.get("file_path") or inp.get("filePath")
                if target and target not in seen:
                    seen.add(target)
                    changes.append(
                        {"file": target, "tool": name, "ts": entry.get("timestamp")}
                    )
            elif name == "bash":
                cmd = str(inp.get("command") or "")
                if cmd and BASH_MUTATION_RE.search(cmd):
                    bash_hints.append({"cmd": cmd, "ts": entry.get("timestamp")})
    return changes, bash_hints


def extract_aside_history(start_ms, end_ms, project_filter=None, cwd_filter=None):
    sessions = {}
    for sid, info in aside_session_index().items():
        project = info.get("cwd") or ""
        if project_filter and project_filter not in project:
            continue
        if cwd_filter and not path_matches(project, cwd_filter):
            continue

        previews = []
        first_ts_ms = 0
        for entry in _iter_lines(info["path"]):
            if entry.get("role") != "user":
                continue
            ts = _sec_to_ms(entry.get("timestamp")) or info["ts"]
            if not (start_ms <= ts < end_ms):
                continue
            first_ts_ms = ts if not first_ts_ms else min(first_ts_ms, ts)
            text = _content_text(entry.get("content")).strip()
            if text:
                previews.append({"time": ts_to_hm(ts), "text": text[:300]})

        if not previews:
            if not (start_ms <= info["ts"] < end_ms):
                continue
            first_ts_ms = info["ts"]
            if info.get("title"):
                previews.append(
                    {"time": ts_to_hm(first_ts_ms), "text": info["title"][:300]}
                )
        sessions[sid] = {
            "project": project,
            "messages": previews,
            "tool": TOOL,
            "first_ts_ms": first_ts_ms,
        }
    return sessions


def grep_aside_session(fpath: Path, keyword: str, session_id: str | None = None):
    sid = session_id
    if not sid:
        sid = next(
            (
                key
                for key, info in aside_session_index().items()
                if info["path"] == fpath
            ),
            None,
        )
    if not sid:
        return []
    messages, _ = read_aside_conversation(sid, full=True)
    hits = []
    needle = keyword.lower()
    for message in messages or []:
        text = message.get("text") or ""
        lowered = text.lower()
        if needle not in lowered:
            continue
        idx = lowered.find(needle)
        start = max(0, idx - 60)
        end = min(len(text), idx + len(keyword) + 90)
        hits.append(
            {
                "role": message.get("role") or "",
                "ts": message.get("ts") or "",
                "excerpt": (
                    ("..." if start else "")
                    + text[start:end]
                    + ("..." if end < len(text) else "")
                ).replace("\n", " "),
            }
        )
    return hits


session_index = aside_session_index
find_session_file = find_aside_session_file
read_conversation = read_aside_conversation
extract_changed_files = extract_aside_changed_files
extract_history = extract_aside_history
grep_session = grep_aside_session

register_cache_clearer(aside_session_index.cache_clear)


# ─── token usage ───────────────────────────────────────────────


def add_token_usage(totals, usage):
    input_tokens = int(usage.get("input_tokens") or 0)
    output_tokens = int(usage.get("output_tokens") or 0)
    cache_write = int(usage.get("cache_creation_input_tokens") or 0)
    cache_read = int(usage.get("cache_read_input_tokens") or 0)
    totals["input_tokens"] += input_tokens
    totals["output_tokens"] += output_tokens
    totals["cache_creation_input_tokens"] += cache_write
    totals["cache_creation_5m_tokens"] += cache_write
    totals["cache_read_input_tokens"] += cache_read
    totals["total_tokens"] += input_tokens + output_tokens + cache_write + cache_read
    totals["effective_tokens"] += input_tokens + output_tokens + cache_write
    totals["pure_tokens"] += input_tokens + output_tokens
    totals["cache_tokens"] += cache_read
    totals["calls"] += 1


def collect_token_rows(start, end, args):
    from common import in_range, parse_ts

    rows = []
    index = aside_session_index()
    main_only = getattr(args, "main_only", False)
    cwd_filter = str(Path.cwd()) if getattr(args, "cwd", False) else None
    project_filter = getattr(args, "project", None)

    for profile in _profiles():
        db = profile / "state.db"
        if not db.exists():
            continue
        try:
            con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
        except sqlite3.Error:
            continue
        with contextlib.closing(con):
            try:
                runs = con.execute(
                    "select session_id, token_usage, started_at from session_runs"
                ).fetchall()
            except sqlite3.Error:
                continue
            for sid, raw, started in runs:
                usage = _loads(raw)
                if not usage:
                    continue
                info = index.get(sid)
                subagent = bool(info and info.get("subagent"))
                if main_only and subagent:
                    continue
                cwd = (info or {}).get("cwd", "")
                if cwd_filter and not path_matches(cwd, cwd_filter):
                    continue
                if project_filter and project_filter not in cwd:
                    continue
                timestamp = parse_ts(_sec_to_ms(started))
                if not in_range(timestamp, start, end):
                    continue
                entry = {
                    "tool": TOOL,
                    "timestamp": timestamp.isoformat() if timestamp else None,
                    "session_id": sid,
                    "cwd": cwd,
                    "path": str(db),
                    "model": (info or {}).get("model", ""),
                    "subagent": subagent,
                    "input_tokens": int(usage.get("input") or 0),
                    "output_tokens": int(usage.get("output") or 0),
                    "cache_read_input_tokens": int(usage.get("cacheRead") or 0),
                    "cache_creation_input_tokens": int(usage.get("cacheWrite") or 0),
                    "cache_creation_5m_tokens": int(usage.get("cacheWrite") or 0),
                    "cache_creation_1h_tokens": 0,
                }
                entry["total_tokens"] = (
                    entry["input_tokens"]
                    + entry["output_tokens"]
                    + entry["cache_read_input_tokens"]
                    + entry["cache_creation_input_tokens"]
                )
                if entry["total_tokens"]:
                    rows.append(entry)
    return rows
