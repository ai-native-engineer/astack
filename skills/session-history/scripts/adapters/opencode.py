"""opencode session adapter.

정본은 `opencode.db`다. `~/.claude/transcripts/ses_*.jsonl`은 경로 때문에 Claude Code
기록처럼 보이지만 opencode가 쓴 것이고, DB에서 사라진 옛 세션을 보충하는 용도로만 쓴다.
"""

from __future__ import annotations

import contextlib
import functools
import json
import re
import sqlite3
from collections import defaultdict
from pathlib import Path

from common import (
    BASH_MUTATION_RE,
    CLAUDE_OPENCODE_TRANSCRIPTS_DIR,
    OPENCODE_DB,
    include_subagents,
    iso_to_ms,
    path_matches,
    register_cache_clearer,
    ts_to_hm,
)

TOOL = "opencode"
DISPLAY = "opencode"
SHORT = "opencode"
TAG = "[O]"
SOURCE_PATHS = (OPENCODE_DB, CLAUDE_OPENCODE_TRANSCRIPTS_DIR)

EDIT_TOOLS = {"edit", "write"}
APPLY_PATCH_HEADER_RE = re.compile(
    r"^\*\*\*\s+(Update|Add|Delete|Move)\s+(?:File|to):\s+(.+?)\s*$", re.MULTILINE
)
# 첨부 이미지 part는 base64 data URI라 한 행이 수 MB다. 텍스트 조회에서 제외한다.
_NOT_FILE_PART = 'p.data not like \'%"type":"file"%\''


def _connect():
    """읽기 전용 연결. WAL을 보려면 mode=ro가 필요하고, 실패 시에만 immutable로 내린다."""
    if not OPENCODE_DB.exists():
        return None
    for query in ("mode=ro", "mode=ro&immutable=1"):
        try:
            con = sqlite3.connect(f"file:{OPENCODE_DB}?{query}", uri=True)
            con.row_factory = sqlite3.Row
            con.execute("select 1 from session limit 1")
            return con
        except sqlite3.Error:
            continue
    return None


def _loads(raw):
    if not raw:
        return {}
    try:
        value = json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        return {}
    return value if isinstance(value, dict) else {}


def _transcript_path(sid: str) -> Path:
    return CLAUDE_OPENCODE_TRANSCRIPTS_DIR / f"{sid}.jsonl"


def _transcript_first_ts(path: Path) -> int:
    try:
        with path.open(encoding="utf-8") as fh:
            for line in fh:
                entry = _loads(line)
                if entry.get("timestamp"):
                    return iso_to_ms(entry["timestamp"])
    except OSError:
        pass
    try:
        return int(path.stat().st_mtime * 1000)
    except OSError:
        return 0


@functools.lru_cache(maxsize=1)
def opencode_session_index():
    """session_id → {path, cwd, ts, title, model, agent, subagent, src}."""
    idx: dict[str, dict] = {}

    con = _connect()
    if con is not None:
        with contextlib.closing(con):
            rows = con.execute(
                "select id, directory, time_created, title, model, agent, parent_id"
                " from session"
            ).fetchall()
        for row in rows:
            subagent = row["parent_id"] is not None
            if subagent and not include_subagents():
                continue
            idx[row["id"]] = {
                # 대화 본문을 DB에서 읽으므로 표시 경로도 DB여야 출처가 어긋나지 않는다.
                "path": OPENCODE_DB,
                "cwd": row["directory"] or "",
                "ts": int(row["time_created"] or 0),
                "title": row["title"] or "",
                "model": _loads(row["model"]).get("id", ""),
                "agent": row["agent"] or "",
                "subagent": subagent,
                "src": "db",
            }

    # DB에서 사라진 옛 세션은 transcript에만 남아 있다. cwd는 기록되지 않아 빈 값이다.
    if CLAUDE_OPENCODE_TRANSCRIPTS_DIR.is_dir():
        for path in CLAUDE_OPENCODE_TRANSCRIPTS_DIR.glob("ses_*.jsonl"):
            if path.stem in idx:
                continue
            idx[path.stem] = {
                "path": path,
                "cwd": "",
                "ts": _transcript_first_ts(path),
                "title": "",
                "model": "",
                "agent": "",
                "subagent": False,
                "src": "transcript",
            }
    return idx


def find_opencode_session_file(session_id: str) -> Path | None:
    idx = opencode_session_index()
    info = idx.get(session_id)
    if info is None:
        for sid, candidate in idx.items():
            if sid.startswith(session_id):
                info = candidate
                break
    return info["path"] if info else None


def _resolve(session_id: str):
    idx = opencode_session_index()
    if session_id in idx:
        return session_id, idx[session_id]
    for sid, info in idx.items():
        if sid.startswith(session_id):
            return sid, info
    return None, None


def _db_messages(con, sid: str, full: bool):
    messages = []
    rows = con.execute(
        "select p.time_created ts, p.data pdata, m.data mdata"
        " from part p join message m on m.id = p.message_id"
        f" where p.session_id = ? and {_NOT_FILE_PART} order by p.id",
        (sid,),
    )
    for row in rows:
        part = _loads(row["pdata"])
        role = _loads(row["mdata"]).get("role")
        ptype = part.get("type")
        ts = row["ts"]
        if ptype == "text":
            text = (part.get("text") or "").strip()
            if not text or part.get("synthetic"):
                continue
            if role == "user":
                messages.append({"role": "user", "text": text, "ts": ts})
            else:
                messages.append(
                    {
                        "role": "assistant",
                        "text": text,
                        "ts": ts,
                        "model": _loads(row["mdata"]).get("modelID", ""),
                    }
                )
        elif ptype == "tool" and full:
            state = part.get("state") or {}
            inp = state.get("input") or {}
            label = _tool_arg(inp)
            messages.append(
                {
                    "role": "tool_call",
                    "text": f"[{part.get('tool', '')}] {label[:200]}",
                    "ts": (state.get("time") or {}).get("start") or ts,
                }
            )
            output = state.get("output") or state.get("error") or ""
            if str(output).strip():
                messages.append(
                    {
                        "role": "tool_result",
                        "text": str(output).strip()[:500],
                        "ts": (state.get("time") or {}).get("end") or ts,
                    }
                )
    return messages


def _tool_arg(inp) -> str:
    if not isinstance(inp, dict):
        return str(inp)
    for key in ("command", "filePath", "pattern", "query", "url", "description"):
        value = inp.get(key)
        if value:
            return str(value)
    return json.dumps(inp, ensure_ascii=False)


def _transcript_messages(path: Path, full: bool):
    """transcript에는 assistant 텍스트가 없다. writer가 user와 도구 호출만 기록한다."""
    messages = []
    try:
        fh = path.open(encoding="utf-8")
    except OSError:
        return messages
    with fh:
        for line in fh:
            entry = _loads(line)
            etype = entry.get("type")
            ts = entry.get("timestamp", "")
            if etype == "user":
                text = str(entry.get("content") or "").strip()
                if text:
                    messages.append({"role": "user", "text": text, "ts": ts})
            elif etype == "tool_use" and full:
                label = _tool_arg(entry.get("tool_input"))
                messages.append(
                    {
                        "role": "tool_call",
                        "text": f"[{entry.get('tool_name', '')}] {label[:200]}",
                        "ts": ts,
                    }
                )
            elif etype == "tool_result" and full:
                output = entry.get("tool_output")
                text = (
                    output
                    if isinstance(output, str)
                    else json.dumps(output, ensure_ascii=False)
                )
                if text.strip():
                    messages.append(
                        {"role": "tool_result", "text": text.strip()[:500], "ts": ts}
                    )
    return messages


def read_opencode_conversation(session_id: str, full: bool = False):
    sid, info = _resolve(session_id)
    if not info:
        return None, None
    if info["src"] == "db":
        con = _connect()
        if con is not None:
            with contextlib.closing(con):
                return _db_messages(con, sid, full), info["path"]
        return [], info["path"]
    return _transcript_messages(info["path"], full), info["path"]


def _add_change(changes, seen, file_path, tool, ts):
    key = (file_path, tool)
    if not file_path or key in seen:
        return
    seen.add(key)
    changes.append({"file": file_path, "tool": tool, "ts": ts})


def _collect_tool_changes(tool, inp, ts, changes, seen, bash_hints):
    if tool in EDIT_TOOLS:
        _add_change(changes, seen, inp.get("filePath") or "", tool, ts)
    elif tool == "apply_patch":
        patch = inp.get("patchText") or inp.get("input") or ""
        if isinstance(patch, str):
            for op, path in APPLY_PATCH_HEADER_RE.findall(patch):
                _add_change(changes, seen, path.strip(), f"apply_patch/{op}", ts)
    elif tool == "bash":
        cmd = str(inp.get("command") or "")
        if cmd and BASH_MUTATION_RE.search(cmd):
            bash_hints.append({"cmd": cmd, "ts": ts})


def extract_opencode_changed_files(session_id: str):
    sid, info = _resolve(session_id)
    if not info:
        return None, None

    changes: list[dict] = []
    bash_hints: list[dict] = []
    seen: set = set()

    if info["src"] == "db":
        con = _connect()
        if con is None:
            return changes, bash_hints
        with contextlib.closing(con):
            rows = con.execute(
                f"select p.time_created ts, p.data pdata from part p"
                f" where p.session_id = ? and {_NOT_FILE_PART} order by p.id",
                (sid,),
            )
            for row in rows:
                part = _loads(row["pdata"])
                ptype = part.get("type")
                if ptype == "patch":
                    for file_path in part.get("files") or []:
                        _add_change(changes, seen, file_path, "patch", row["ts"])
                elif ptype == "tool":
                    state = part.get("state") or {}
                    if state.get("status") != "completed":
                        continue
                    _collect_tool_changes(
                        part.get("tool", ""),
                        state.get("input") or {},
                        (state.get("time") or {}).get("start") or row["ts"],
                        changes,
                        seen,
                        bash_hints,
                    )
        return changes, bash_hints

    try:
        fh = info["path"].open(encoding="utf-8")
    except OSError:
        return changes, bash_hints
    with fh:
        for line in fh:
            entry = _loads(line)
            # tool_result가 tool_input을 재수록하므로 tool_use만 읽어 중복을 피한다.
            if entry.get("type") != "tool_use":
                continue
            _collect_tool_changes(
                entry.get("tool_name", ""),
                entry.get("tool_input") or {},
                entry.get("timestamp", ""),
                changes,
                seen,
                bash_hints,
            )
    return changes, bash_hints


def extract_opencode_history(start_ms, end_ms, project_filter=None, cwd_filter=None):
    sessions = {}
    wanted = []
    for sid, info in opencode_session_index().items():
        ts = info["ts"]
        if not ts or not (start_ms <= ts < end_ms):
            continue
        project = info["cwd"]
        if project_filter and project_filter not in project:
            continue
        if cwd_filter and not path_matches(project, cwd_filter):
            continue
        sessions[sid] = {
            "project": project,
            "messages": [],
            "tool": TOOL,
            "first_ts_ms": ts,
        }
        wanted.append((sid, info))

    if not wanted:
        return sessions

    db_ids = [sid for sid, info in wanted if info["src"] == "db"]
    if db_ids:
        con = _connect()
        if con is not None:
            with contextlib.closing(con):
                placeholders = ",".join("?" * len(db_ids))
                rows = con.execute(
                    "select p.session_id sid, p.time_created ts, p.data pdata,"
                    " m.data mdata from part p join message m on m.id = p.message_id"
                    f" where p.session_id in ({placeholders}) and {_NOT_FILE_PART}"
                    " order by p.id",
                    db_ids,
                )
                for row in rows:
                    part = _loads(row["pdata"])
                    if part.get("type") != "text" or part.get("synthetic"):
                        continue
                    if _loads(row["mdata"]).get("role") != "user":
                        continue
                    text = (part.get("text") or "").strip()
                    entry = sessions.get(row["sid"])
                    if not text or entry is None:
                        continue
                    ts = int(row["ts"] or 0)
                    entry["messages"].append({"time": ts_to_hm(ts), "text": text[:300]})
                    if ts:
                        entry["first_ts_ms"] = min(entry["first_ts_ms"], ts)

    for sid, info in wanted:
        if info["src"] != "transcript":
            continue
        for message in _transcript_messages(info["path"], full=False):
            ts = iso_to_ms(message["ts"]) or info["ts"]
            sessions[sid]["messages"].append(
                {"time": ts_to_hm(ts), "text": message["text"][:300]}
            )
    return sessions


def grep_opencode_session(fpath: Path, keyword: str, session_id: str | None = None):
    if session_id:
        sid, info = _resolve(session_id)
    else:
        # DB 세션은 모두 같은 파일 경로를 공유하므로 경로만으로는 특정할 수 없다.
        sid = fpath.stem if fpath.name.startswith("ses_") else None
        info = opencode_session_index().get(sid) if sid else None
    if not info:
        return []

    if info["src"] == "db":
        con = _connect()
        if con is None:
            return []
        with contextlib.closing(con):
            messages = _db_messages(con, sid, full=True)
    else:
        messages = _transcript_messages(info["path"], full=True)

    hits = []
    needle = keyword.lower()
    for message in messages:
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


def source_notes():
    counts = defaultdict(int)
    for info in opencode_session_index().values():
        counts[info["src"]] += 1
    notes = []
    if counts["transcript"]:
        notes.append(
            f"~/.claude/transcripts의 {counts['transcript']}개 세션은 opencode가 남긴 것으로"
            " cwd 기록이 없어 --cwd 필터에 걸리지 않고 assistant 답변도 저장되지 않는다"
        )
    return notes


session_index = opencode_session_index
find_session_file = find_opencode_session_file
read_conversation = read_opencode_conversation
extract_changed_files = extract_opencode_changed_files
extract_history = extract_opencode_history
grep_session = grep_opencode_session

register_cache_clearer(opencode_session_index.cache_clear)


# ─── token usage ───────────────────────────────────────────────


def add_token_usage(totals, usage):
    input_tokens = int(usage.get("input_tokens") or 0)
    output_tokens = int(usage.get("output_tokens") or 0)
    cache_write = int(usage.get("cache_creation_input_tokens") or 0)
    cache_read = int(usage.get("cache_read_input_tokens") or 0)
    reasoning = int(usage.get("reasoning_output_tokens") or 0)
    totals["input_tokens"] += input_tokens
    totals["output_tokens"] += output_tokens
    totals["cache_creation_input_tokens"] += cache_write
    totals["cache_creation_5m_tokens"] += cache_write
    totals["cache_read_input_tokens"] += cache_read
    totals["reasoning_output_tokens"] += reasoning
    totals["total_tokens"] += input_tokens + output_tokens + cache_write + cache_read
    totals["effective_tokens"] += input_tokens + output_tokens + cache_write
    totals["pure_tokens"] += input_tokens + output_tokens
    totals["cache_tokens"] += cache_read
    totals["calls"] += 1


def collect_token_rows(start, end, args):
    from common import in_range, parse_ts

    rows = []
    con = _connect()
    if con is None:
        return rows

    index = opencode_session_index()
    main_only = getattr(args, "main_only", False)
    cwd_filter = str(Path.cwd()) if getattr(args, "cwd", False) else None
    project_filter = getattr(args, "project", None)

    with contextlib.closing(con):
        for row in con.execute("select session_id, time_created, data from message"):
            data = _loads(row["data"])
            if data.get("role") != "assistant":
                continue
            tokens = data.get("tokens") or {}
            if not tokens:
                continue
            info = index.get(row["session_id"])
            subagent = bool(info and info["subagent"])
            if main_only and subagent:
                continue
            cwd = (data.get("path") or {}).get("cwd") or (info or {}).get("cwd") or ""
            if cwd_filter and not path_matches(cwd, cwd_filter):
                continue
            if project_filter and project_filter not in cwd:
                continue
            timestamp = parse_ts(row["time_created"])
            if not in_range(timestamp, start, end):
                continue
            cache = tokens.get("cache") or {}
            entry = {
                "tool": TOOL,
                "timestamp": timestamp.isoformat() if timestamp else None,
                "session_id": row["session_id"],
                "cwd": cwd,
                "path": str(OPENCODE_DB),
                "model": data.get("modelID") or "",
                "subagent": subagent,
                "input_tokens": int(tokens.get("input") or 0),
                "output_tokens": int(tokens.get("output") or 0),
                "reasoning_output_tokens": int(tokens.get("reasoning") or 0),
                "cache_creation_input_tokens": int(cache.get("write") or 0),
                "cache_creation_5m_tokens": int(cache.get("write") or 0),
                "cache_creation_1h_tokens": 0,
                "cache_read_input_tokens": int(cache.get("read") or 0),
            }
            entry["total_tokens"] = (
                entry["input_tokens"]
                + entry["output_tokens"]
                + entry["cache_creation_input_tokens"]
                + entry["cache_read_input_tokens"]
            )
            rows.append(entry)
    return rows
