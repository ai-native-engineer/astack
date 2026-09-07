"""Cursor agent transcript adapter."""

from __future__ import annotations

import binascii
import datetime
import functools
import json
import re
import sqlite3
from pathlib import Path

from common import (
    BASH_MUTATION_RE,
    CURSOR_CHATS_DIR,
    CURSOR_PROJECTS_DIR,
    HOME,
    include_subagents,
    iso_to_ms,
    path_matches,
    register_cache_clearer,
    ts_to_hm,
)

TOOL = "cursor"
DISPLAY = "Cursor"
SHORT = "Cursor"
TAG = "[R]"
SOURCE_PATHS = (CURSOR_PROJECTS_DIR, CURSOR_CHATS_DIR)

# 인덱스 미리보기는 첫 사용자 발화와 Workspace Path만 필요해 앞부분만 읽는다.
_CHATS_PREVIEW_BLOBS = 24

TIMESTAMP_RE = re.compile(
    r"<timestamp>\s*(.*?)\s*</timestamp>", re.DOTALL | re.IGNORECASE
)
WORKSPACE_PATH_RE = re.compile(r"Workspace Path:\s*(/[^\n<]+)")
PATCH_PATH_RE = re.compile(
    r"^\*\*\*\s+(?:Add|Update|Delete|Move)\s+(?:File|to):\s+(.+?)\s*$",
    re.MULTILINE,
)
EDIT_TOOLS = {
    "Edit",
    "Write",
    "MultiEdit",
    "Delete",
    "EditNotebook",
    "NotebookEdit",
    "search_replace",
    "write",
}
SHELL_TOOLS = {"Shell", "Bash", "run_terminal_command"}


def cursor_content_text(content) -> str:
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for part in content:
            if isinstance(part, str):
                parts.append(part)
            elif isinstance(part, dict) and isinstance(part.get("text"), str):
                parts.append(part["text"])
        return "\n".join(parts)
    if isinstance(content, dict):
        if isinstance(content.get("text"), str):
            return content["text"]
        if isinstance(content.get("content"), str):
            return content["content"]
    return ""


def extract_cursor_user_query(text: str) -> str:
    """Strip Cursor's injected context and keep actual user queries."""
    if not text:
        return ""
    lowered = text.lower()
    start = lowered.rfind("<user_query>")
    if start >= 0:
        start += len("<user_query>")
        end = lowered.find("</user_query>", start)
        if end >= 0:
            return text[start:end].strip()
    stripped = text.strip()
    if stripped.startswith(("<system_reminder>", "<system-reminder>", "<user_info>")):
        return ""
    return stripped


def _timestamp_text_to_ms(value: str) -> int:
    value = value.strip()
    utc_match = re.fullmatch(r"(.+?)\s+\(UTC([+-])(\d{1,2})(?::?(\d{2}))?\)", value)
    if utc_match:
        date_text, sign, hour, minute = utc_match.groups()
        offset_minutes = int(hour) * 60 + int(minute or 0)
        if sign == "-":
            offset_minutes *= -1
        tz = datetime.timezone(datetime.timedelta(minutes=offset_minutes))
        for fmt in (
            "%A, %b %d, %Y, %I:%M %p",
            "%A, %B %d, %Y, %I:%M %p",
            "%b %d, %Y, %I:%M %p",
            "%B %d, %Y, %I:%M %p",
        ):
            try:
                parsed = datetime.datetime.strptime(date_text, fmt).replace(tzinfo=tz)
                return int(parsed.timestamp() * 1000)
            except ValueError:
                continue
    return iso_to_ms(value)


def embedded_cursor_timestamp_ms(text: str) -> int:
    match = TIMESTAMP_RE.search(text or "")
    return _timestamp_text_to_ms(match.group(1)) if match else 0


def _sanitize_cursor_slug_part(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "-", value).strip("-")


@functools.cache
def _decode_cursor_project_slug(slug: str) -> str:
    """Resolve Cursor's slash-to-dash project slug against existing directories."""
    home_slug = _sanitize_cursor_slug_part(str(HOME).strip("/"))
    if slug == home_slug:
        return str(HOME)
    if not slug.startswith(home_slug + "-"):
        return ""
    remainder = slug[len(home_slug) + 1 :]

    def walk(base: Path, encoded: str, depth: int) -> Path | None:
        if not encoded or depth > 12:
            return base if not encoded else None
        try:
            children = [path for path in base.iterdir() if path.is_dir()]
        except OSError:
            return None
        matches = []
        for child in children:
            child_slug = _sanitize_cursor_slug_part(child.name)
            if encoded == child_slug:
                matches.append((len(child_slug), child))
            elif child_slug and encoded.startswith(child_slug + "-"):
                resolved = walk(child, encoded[len(child_slug) + 1 :], depth + 1)
                if resolved is not None:
                    matches.append((len(str(resolved)), resolved))
        if not matches:
            return None
        return max(matches, key=lambda item: item[0])[1]

    resolved = walk(HOME, remainder, 0)
    return str(resolved) if resolved else ""


def _chats_meta(con) -> dict:
    """meta의 값은 hex로 인코딩된 JSON이다. 평문으로 들어오는 변형도 받는다."""
    try:
        raw = dict(con.execute("select key, value from meta")).get("0")
    except sqlite3.Error:
        return {}
    if raw is None:
        return {}
    text = raw if isinstance(raw, str) else bytes(raw).decode("utf-8", "replace")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    try:
        return json.loads(binascii.unhexlify(text).decode("utf-8", "replace"))
    except (ValueError, binascii.Error):
        return {}


def _chats_blob_refs(raw: bytes, known) -> list[str]:
    """루트 블롭은 자식 blob id 32바이트를 순서대로 품는다. 그 순서가 대화 순서다."""
    refs = []
    i = 0
    while i + 32 <= len(raw):
        candidate = raw[i : i + 32].hex()
        if candidate in known:
            refs.append(candidate)
            i += 32
        else:
            i += 1
    return refs


_CHATS_PART_TYPES = {"tool-call": "tool_use", "tool-result": "tool_result"}


def _chats_entry(blob: dict) -> dict:
    """chats 블롭을 agent-transcripts jsonl과 같은 모양으로 맞춘다."""
    content = blob.get("content")
    if isinstance(content, list):
        parts = []
        for part in content:
            if not isinstance(part, dict):
                continue
            ptype = part.get("type")
            if ptype == "text":
                parts.append(part)
            elif ptype == "tool-call":
                parts.append(
                    {
                        "type": "tool_use",
                        "name": part.get("toolName") or "",
                        "input": part.get("args") or {},
                    }
                )
            elif ptype == "tool-result":
                parts.append({"type": "tool_result", "content": part.get("result")})
        content = parts
    return {"role": blob.get("role") or "", "message": {"content": content}}


def _chats_entries(db: Path, limit: int = 0) -> list[dict]:
    try:
        con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    except sqlite3.Error:
        return []
    entries: list[dict] = []
    try:
        root = _chats_meta(con).get("latestRootBlobId") or ""
        known = {bid for (bid,) in con.execute("select id from blobs")}
        stack = [root]
        seen: set[str] = set()
        while stack:
            bid = stack.pop(0)
            if not bid or bid in seen or bid not in known:
                continue
            seen.add(bid)
            row = con.execute("select data from blobs where id=?", (bid,)).fetchone()
            raw = bytes(row[0]) if row and row[0] else b""
            if raw[:1] == b"{":
                blob = _loads_bytes(raw)
                if isinstance(blob, dict) and blob.get("role"):
                    entries.append(_chats_entry(blob))
                    if limit and len(entries) >= limit:
                        break
                continue
            stack = _chats_blob_refs(raw, known) + stack
    except sqlite3.Error:
        return entries
    finally:
        con.close()
    return entries


def _loads_bytes(raw: bytes):
    try:
        return json.loads(raw.decode("utf-8", "replace"))
    except json.JSONDecodeError:
        return None


def _cursor_project_dir(fpath: Path) -> Path | None:
    parts = fpath.parts
    try:
        idx = parts.index("agent-transcripts")
    except ValueError:
        return None
    return Path(*parts[:idx]) if idx > 0 else None


def _tool_directory_candidates(entry: dict):
    if entry.get("role") != "assistant":
        return [], []
    exact = []
    fallback = []
    message = entry.get("message") or {}
    for part in message.get("content") or []:
        if not isinstance(part, dict) or part.get("type") != "tool_use":
            continue
        inp = part.get("input") or {}
        if not isinstance(inp, dict):
            continue
        working = inp.get("working_directory")
        target = inp.get("target_directory")
        if isinstance(working, str) and working.startswith("/"):
            exact.append(working)
        if isinstance(target, str) and target.startswith("/"):
            fallback.append(target)
    return exact, fallback


def _jsonl_entries(fpath: Path) -> list[dict]:
    try:
        fh = fpath.open(encoding="utf-8")
    except OSError:
        return []
    entries = []
    with fh:
        for line in fh:
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return entries


def _entries_for(info: dict, limit: int = 0) -> list[dict]:
    if info.get("kind") == "chats":
        return _chats_entries(info["path"], limit)
    entries = _jsonl_entries(info["path"])
    return entries[:limit] if limit else entries


def _scan_cursor_metadata(entries, fpath: Path | None = None) -> tuple[str, int]:
    workspace = ""
    working_dirs = []
    target_dirs = []
    first_ts_ms = 0
    for entry in entries:
        message = entry.get("message") or {}
        text = cursor_content_text(message.get("content"))
        if entry.get("role") == "user" and not workspace:
            match = WORKSPACE_PATH_RE.search(text)
            if match:
                workspace = match.group(1).strip()
        ts_ms = embedded_cursor_timestamp_ms(text)
        if ts_ms and (not first_ts_ms or ts_ms < first_ts_ms):
            first_ts_ms = ts_ms
        exact, fallback = _tool_directory_candidates(entry)
        working_dirs.extend(exact)
        target_dirs.extend(fallback)

    if not workspace and fpath is not None:
        project_dir = _cursor_project_dir(fpath)
        if project_dir:
            workspace = _decode_cursor_project_slug(project_dir.name)
    if not workspace:
        workspace = next((path for path in working_dirs if Path(path).exists()), "")
    if not workspace:
        workspace = next((path for path in target_dirs if Path(path).exists()), "")
    if not first_ts_ms and fpath is not None:
        try:
            first_ts_ms = int(fpath.stat().st_mtime * 1000)
        except OSError:
            first_ts_ms = 0
    return workspace, first_ts_ms


def _iter_cursor_transcripts():
    if not CURSOR_PROJECTS_DIR.exists():
        return
    for fpath in CURSOR_PROJECTS_DIR.rglob("*.jsonl"):
        parts = fpath.parts
        if "agent-transcripts" not in parts:
            continue
        if not include_subagents() and "subagents" in parts:
            continue
        yield fpath


def _iter_cursor_chat_stores():
    """`chats/<workspace>/<agent-id>/store.db`. projects와 세션 ID가 겹치지 않는다."""
    if not CURSOR_CHATS_DIR.is_dir():
        return
    for db in sorted(CURSOR_CHATS_DIR.glob("*/*/store.db")):
        try:
            con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
        except sqlite3.Error:
            continue
        try:
            info = _chats_meta(con)
        finally:
            con.close()
        if info.get("subagentInfo") and not include_subagents():
            continue
        yield db, info


@functools.lru_cache(maxsize=1)
def cursor_session_index():
    """session_id -> {path, cwd, ts, kind}."""
    idx = {}
    for fpath in _iter_cursor_transcripts() or ():
        sid = fpath.stem
        project, ts_ms = _scan_cursor_metadata(_jsonl_entries(fpath), fpath)
        idx[sid] = {"path": fpath, "cwd": project, "ts": ts_ms, "kind": "jsonl"}
    for db, info in _iter_cursor_chat_stores() or ():
        sid = str(info.get("agentId") or db.parent.name)
        # 같은 세션이 transcript에도 있으면 그쪽이 정본이다.
        # store.db는 compaction 때 앞부분을 잃는다.
        if sid in idx:
            continue
        # 블롭까지 읽으면 인덱스가 253MB를 훑는다. cwd는 필요할 때 채운다.
        idx[sid] = {
            "path": db,
            "cwd": "",
            "ts": int(info.get("createdAt") or 0),
            "kind": "chats",
            "title": str(info.get("name") or ""),
        }
    return idx


def _chats_cwd(info: dict) -> str:
    if info.get("kind") != "chats" or info.get("cwd"):
        return info.get("cwd") or ""
    workspace, _ = _scan_cursor_metadata(_entries_for(info, _CHATS_PREVIEW_BLOBS))
    info["cwd"] = workspace
    return workspace


def find_cursor_session_file(session_id: str) -> Path | None:
    idx = cursor_session_index()
    if session_id in idx:
        return idx[session_id]["path"]
    for sid, info in idx.items():
        if sid.startswith(session_id):
            return info["path"]
    return None


def _cursor_messages(entries, full: bool):
    messages = []
    current_ts = 0
    for entry in entries:
        role = entry.get("role") or ""
        message = entry.get("message") or {}
        content = message.get("content") or []
        raw_text = cursor_content_text(content)
        embedded_ts = embedded_cursor_timestamp_ms(raw_text)
        if embedded_ts:
            current_ts = embedded_ts
        ts = entry.get("timestamp") or message.get("timestamp") or current_ts

        if role == "user":
            text = extract_cursor_user_query(raw_text)
            if text:
                messages.append({"role": "user", "text": text, "ts": ts})
            if full and isinstance(content, list):
                for part in content:
                    if not isinstance(part, dict) or part.get("type") != "tool_result":
                        continue
                    result = cursor_content_text(part.get("content"))
                    if result.strip():
                        messages.append(
                            {
                                "role": "tool_result",
                                "text": result.strip(),
                                "ts": ts,
                            }
                        )
            continue

        if role == "assistant":
            texts = []
            for part in content if isinstance(content, list) else []:
                if not isinstance(part, dict):
                    continue
                if part.get("type") == "text" and isinstance(part.get("text"), str):
                    texts.append(part["text"])
                elif part.get("type") == "tool_use" and full:
                    name = part.get("name") or ""
                    inp = part.get("input") or {}
                    if not isinstance(inp, str):
                        inp = json.dumps(inp, ensure_ascii=False)
                    messages.append(
                        {
                            "role": "tool_call",
                            "text": f"[{name}] {inp}",
                            "ts": ts,
                        }
                    )
            text = "\n".join(texts).strip()
            if text:
                messages.append(
                    {
                        "role": "assistant",
                        "text": text,
                        "ts": ts,
                        "model": message.get("model") or entry.get("model") or "",
                    }
                )
            continue

        if full and role in {"tool", "tool_result"}:
            text = cursor_content_text(content)
            if text.strip():
                messages.append({"role": "tool_result", "text": text.strip(), "ts": ts})
    return messages


def _resolve_cursor(session_id: str):
    idx = cursor_session_index()
    if session_id in idx:
        return idx[session_id]
    for sid, info in idx.items():
        if sid.startswith(session_id):
            return info
    return None


def read_cursor_conversation(session_id: str, full: bool = False):
    info = _resolve_cursor(session_id)
    if not info or not info["path"].exists():
        return None, None
    return _cursor_messages(_entries_for(info), full), info["path"]


def _iter_cursor_tool_calls(entries):
    current_ts = 0
    for entry in entries:
        message = entry.get("message") or {}
        content = message.get("content") or []
        text = cursor_content_text(content)
        current_ts = embedded_cursor_timestamp_ms(text) or current_ts
        if entry.get("role") != "assistant" or not isinstance(content, list):
            continue
        for part in content:
            if isinstance(part, dict) and part.get("type") == "tool_use":
                yield part.get("name") or "", part.get("input") or {}, current_ts


def extract_cursor_changed_files(session_id: str):
    info = _resolve_cursor(session_id)
    if not info or not info["path"].exists():
        return None, None
    changes = []
    bash_hints = []
    for name, raw_input, ts in _iter_cursor_tool_calls(_entries_for(info)):
        inp = raw_input if isinstance(raw_input, dict) else {}
        if name in EDIT_TOOLS:
            path = (
                inp.get("file_path")
                or inp.get("path")
                or inp.get("notebook_path")
                or inp.get("target_notebook")
                or ""
            )
            if path:
                changes.append({"file": path, "tool": name, "ts": ts})
        elif name == "ApplyPatch":
            patch = (
                raw_input
                if isinstance(raw_input, str)
                else (
                    inp.get("patch")
                    or inp.get("input")
                    or json.dumps(inp, ensure_ascii=False)
                )
            )
            for path in PATCH_PATH_RE.findall(patch):
                changes.append({"file": path.strip(), "tool": name, "ts": ts})
        elif name in SHELL_TOOLS:
            command = inp.get("command") or inp.get("cmd") or ""
            if isinstance(command, list):
                command = " ".join(str(item) for item in command)
            if command and BASH_MUTATION_RE.search(str(command)):
                bash_hints.append({"cmd": str(command), "ts": ts})
    return changes, bash_hints


def extract_cursor_history(start_ms, end_ms, project_filter=None, cwd_filter=None):
    sessions = {}
    for sid, info in cursor_session_index().items():
        if info.get("kind") == "chats":
            # 범위 밖 세션은 블롭을 열지 않는다.
            if not info["ts"] or not (start_ms <= info["ts"] < end_ms):
                continue
            project = _chats_cwd(info)
        else:
            project = info.get("cwd") or ""
        if project_filter and project_filter not in project:
            continue
        if cwd_filter and not path_matches(project, cwd_filter):
            continue
        try:
            limit = _CHATS_PREVIEW_BLOBS if info.get("kind") == "chats" else 0
            conversation = _cursor_messages(_entries_for(info, limit), full=False)
        except OSError:
            continue
        previews = []
        first_ts_ms = 0
        for message in conversation:
            if message.get("role") != "user":
                continue
            ts_ms = iso_to_ms(message.get("ts")) or int(info.get("ts") or 0)
            if not (start_ms <= ts_ms < end_ms):
                continue
            first_ts_ms = ts_ms if not first_ts_ms else min(first_ts_ms, ts_ms)
            previews.append({"time": ts_to_hm(ts_ms), "text": message["text"][:300]})
        if not previews:
            if info.get("kind") != "chats":
                continue
            # 주입 컨텍스트만 남은 세션도 제목으로 존재를 남긴다.
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


def grep_cursor_session(fpath: Path, keyword: str, session_id: str | None = None):
    info = _resolve_cursor(session_id) if session_id else None
    if info is None:
        info = next(
            (i for i in cursor_session_index().values() if i["path"] == fpath),
            {"path": fpath, "kind": "jsonl"},
        )
    hits = []
    needle = keyword.lower()
    for message in _cursor_messages(_entries_for(info), full=True):
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


def source_notes() -> list[str]:
    only_chats = sum(
        1 for info in cursor_session_index().values() if info.get("kind") == "chats"
    )
    notes = ["transcript에 없는 세션만 ~/.cursor/chats의 store.db에서 채운다"]
    if only_chats:
        notes.append(
            f"store.db로만 남은 세션 {only_chats}건은 대화 시각이 세션 생성 시각뿐이다"
        )
    notes.append("transcript에 token usage가 없어 비용 집계에서 빠진다")
    return notes


def collect_token_rows(start, end, args):
    """Cursor transcripts do not expose model token usage."""
    return []


def add_token_usage(totals, usage):
    return None


session_index = cursor_session_index
find_session_file = find_cursor_session_file
read_conversation = read_cursor_conversation
extract_changed_files = extract_cursor_changed_files
extract_history = extract_cursor_history
grep_session = grep_cursor_session

register_cache_clearer(cursor_session_index.cache_clear)
register_cache_clearer(_decode_cursor_project_slug.cache_clear)
