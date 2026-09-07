"""Gemini CLI and Antigravity local transcript adapter."""

from __future__ import annotations

import functools
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlparse

from common import (
    GEMINI_ANTIGRAVITY_DIR,
    GEMINI_ANTIGRAVITY_IDE_DIR,
    GEMINI_TMP_DIR,
    include_subagents,
    iso_to_ms,
    path_matches,
    register_cache_clearer,
    ts_to_hm,
)

TOOL = "gemini"
DISPLAY = "Gemini / Antigravity"
SHORT = "Gemini"
TAG = "[M]"
SOURCE_PATHS = (GEMINI_TMP_DIR, GEMINI_ANTIGRAVITY_DIR, GEMINI_ANTIGRAVITY_IDE_DIR)

ANTIGRAVITY_BRAIN_DIR = GEMINI_ANTIGRAVITY_DIR / "brain"
ANTIGRAVITY_METADATA = GEMINI_ANTIGRAVITY_DIR / "cache" / "conversation_metadata.json"
ANTIGRAVITY_IDE_SUMMARIES = GEMINI_ANTIGRAVITY_IDE_DIR / "agyhub_summaries_proto.pb"
ANTIGRAVITY_IDE_CONVERSATIONS = GEMINI_ANTIGRAVITY_IDE_DIR / "conversations"
ANTIGRAVITY_IDE_LOCKED = (
    "대화 본문(.pb)이 OS 키체인 키로 암호화돼 있어 복원할 수 없다. "
    "제목·작업 경로·시각만 요약 인덱스에서 읽는다."
)
WORKSPACE_DIR_RE = re.compile(
    r"Workspace Directories:.*?^\s*-\s+(/[^\n]+)", re.DOTALL | re.MULTILINE
)


def _content_text(content, include_tools: bool = False) -> str:
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for part in content:
            if isinstance(part, str):
                parts.append(part)
            elif isinstance(part, dict):
                if isinstance(part.get("text"), str):
                    parts.append(part["text"])
                elif include_tools and (
                    "functionCall" in part or "functionResponse" in part
                ):
                    parts.append(json.dumps(part, ensure_ascii=False))
        return "\n".join(parts)
    if isinstance(content, dict):
        if isinstance(content.get("text"), str):
            return content["text"]
        if include_tools:
            return json.dumps(content, ensure_ascii=False)
    return ""


def _real_user_text(text: str) -> str:
    if not text:
        return ""
    lowered = text.lower()
    for tag in ("user_request", "user_query"):
        opening = f"<{tag}>"
        closing = f"</{tag}>"
        start = lowered.rfind(opening)
        if start < 0:
            continue
        start += len(opening)
        end = lowered.find(closing, start)
        if end >= 0:
            return text[start:end].strip()
    stripped = text.strip()
    if stripped.startswith(("<session_context>", "<loaded_context>", "<system")):
        return ""
    return stripped


def _workspace_from_uri(uri: str) -> str:
    if not isinstance(uri, str) or not uri:
        return ""
    if uri.startswith("file://"):
        return unquote(urlparse(uri).path)
    return uri if uri.startswith("/") else ""


@functools.lru_cache(maxsize=1)
def _antigravity_metadata():
    if not ANTIGRAVITY_METADATA.exists():
        return {}
    try:
        data = json.loads(ANTIGRAVITY_METADATA.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    conversations = data.get("conversations") or {}
    return conversations if isinstance(conversations, dict) else {}


def _antigravity_meta_values(sid: str):
    entry = _antigravity_metadata().get(sid) or {}
    summary = entry.get("summary") or {}
    uris = summary.get("WorkspaceURIs") or []
    project = next(
        (_workspace_from_uri(uri) for uri in uris if _workspace_from_uri(uri)), ""
    )
    ts_ms = iso_to_ms(summary.get("UpdatedAt") or entry.get("last_modified_time"))
    return {
        "cwd": project,
        "ts": ts_ms,
        "title": summary.get("Preview") or summary.get("Title") or "",
        "internal": bool(entry.get("is_internal")),
    }


def _pb_varint(buf: bytes, i: int) -> tuple[int, int]:
    value = shift = 0
    while i < len(buf):
        byte = buf[i]
        i += 1
        value |= (byte & 0x7F) << shift
        if not byte & 0x80:
            return value, i
        shift += 7
    raise ValueError("truncated varint")


def _pb_fields(buf: bytes):
    """스키마 없이 protobuf wire format만 걸어 필드를 뽑는다."""
    i = 0
    while i < len(buf):
        key, i = _pb_varint(buf, i)
        fnum, wtype = key >> 3, key & 7
        if wtype == 0:
            value, i = _pb_varint(buf, i)
        elif wtype == 1:
            value, i = buf[i : i + 8], i + 8
        elif wtype == 2:
            length, i = _pb_varint(buf, i)
            if i + length > len(buf):
                raise ValueError("truncated field")
            value, i = buf[i : i + length], i + length
        elif wtype == 5:
            value, i = buf[i : i + 4], i + 4
        else:
            raise ValueError(f"unsupported wire type {wtype}")
        yield fnum, wtype, value


def _pb_strings(buf: bytes, depth: int = 0):
    if depth > 6:
        return
    try:
        items = list(_pb_fields(buf))
    except ValueError:
        return
    for _, wtype, value in items:
        if wtype != 2:
            continue
        try:
            text = value.decode("utf-8")
        except UnicodeDecodeError:
            text = ""
        if text and text.isprintable():
            yield text
        else:
            yield from _pb_strings(value, depth + 1)


def _pb_epoch_seconds(buf: bytes, depth: int = 0):
    """중첩된 google.protobuf.Timestamp의 seconds 필드만 그럴듯한 범위로 거른다."""
    if depth > 6:
        return
    try:
        items = list(_pb_fields(buf))
    except ValueError:
        return
    for fnum, wtype, value in items:
        if wtype == 0 and fnum == 1 and 1_500_000_000 < value < 2_100_000_000:
            yield value
        elif wtype == 2:
            yield from _pb_epoch_seconds(value, depth + 1)


@functools.lru_cache(maxsize=1)
def _antigravity_ide_summaries():
    """session_id -> {title, cwd, ts}. 요약 인덱스만 평문이다."""
    try:
        raw = ANTIGRAVITY_IDE_SUMMARIES.read_bytes()
    except OSError:
        return {}
    records = {}
    try:
        top = list(_pb_fields(raw))
    except ValueError:
        return {}
    for _, wtype, record in top:
        if wtype != 2:
            continue
        sid = ""
        detail = b""
        try:
            parts = list(_pb_fields(record))
        except ValueError:
            continue
        for fnum, part_type, value in parts:
            if part_type != 2:
                continue
            if fnum == 1 and not sid:
                sid = value.decode("utf-8", "replace")
            elif fnum == 2 and not detail:
                detail = value
        if not sid or not detail:
            continue
        title = ""
        for fnum, part_type, value in _pb_fields(detail):
            if fnum == 1 and part_type == 2:
                title = value.decode("utf-8", "replace")
                break
        workspace = next(
            (
                _workspace_from_uri(text)
                for text in _pb_strings(detail)
                if text.startswith("file://")
            ),
            "",
        )
        seconds = sorted(_pb_epoch_seconds(detail))
        records[sid] = {
            "title": title,
            "cwd": workspace,
            "ts": seconds[0] * 1000 if seconds else 0,
        }
    return records


def _first_json_line(path: Path):
    try:
        with path.open(encoding="utf-8") as fh:
            for line in fh:
                if not line.strip():
                    continue
                try:
                    return json.loads(line)
                except json.JSONDecodeError:
                    return {}
    except OSError:
        return {}
    return {}


def _gemini_cli_project(path: Path) -> str:
    try:
        with path.open(encoding="utf-8") as fh:
            for line in fh:
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue
                for message in _messages_from_gemini_op(entry):
                    text = _content_text(message.get("content"))
                    match = WORKSPACE_DIR_RE.search(text)
                    if match:
                        return match.group(1).strip()
    except OSError:
        pass
    return ""


@functools.lru_cache(maxsize=1)
def gemini_session_index():
    """session_id -> {path, cwd, ts, format, title}."""
    idx = {}

    if ANTIGRAVITY_BRAIN_DIR.exists():
        for path in ANTIGRAVITY_BRAIN_DIR.glob(
            "*/.system_generated/logs/transcript_full.jsonl"
        ):
            sid = path.parents[2].name
            meta = _antigravity_meta_values(sid)
            if meta["internal"] and not include_subagents():
                continue
            ts_ms = int(meta["ts"] or 0)
            if not ts_ms:
                first = _first_json_line(path)
                ts_ms = iso_to_ms(first.get("created_at"))
            if not ts_ms:
                try:
                    ts_ms = int(path.stat().st_mtime * 1000)
                except OSError:
                    ts_ms = 0
            idx[sid] = {
                "path": path,
                "cwd": meta["cwd"],
                "ts": ts_ms,
                "format": "antigravity",
                "title": meta["title"],
            }

    if ANTIGRAVITY_IDE_CONVERSATIONS.is_dir():
        summaries = _antigravity_ide_summaries()
        for path in sorted(ANTIGRAVITY_IDE_CONVERSATIONS.glob("*.pb")):
            sid = path.stem
            if sid in idx:
                continue
            meta = summaries.get(sid) or {}
            ts_ms = int(meta.get("ts") or 0)
            if not ts_ms:
                try:
                    ts_ms = int(path.stat().st_mtime * 1000)
                except OSError:
                    ts_ms = 0
            idx[sid] = {
                "path": path,
                "cwd": meta.get("cwd") or "",
                "ts": ts_ms,
                "format": "antigravity-ide",
                "title": meta.get("title") or "",
            }

    if GEMINI_TMP_DIR.exists():
        for path in GEMINI_TMP_DIR.glob("*/chats/session-*.jsonl"):
            meta = _first_json_line(path)
            sid = meta.get("sessionId") or path.stem.removeprefix("session-")
            if not sid:
                continue
            if not include_subagents() and meta.get("kind") not in (None, "", "main"):
                continue
            ts_ms = iso_to_ms(meta.get("startTime") or meta.get("lastUpdated"))
            if not ts_ms:
                try:
                    ts_ms = int(path.stat().st_mtime * 1000)
                except OSError:
                    ts_ms = 0
            idx[sid] = {
                "path": path,
                "cwd": _gemini_cli_project(path),
                "ts": ts_ms,
                "format": "gemini-cli",
                "title": "",
            }
    return idx


def find_gemini_session_file(session_id: str) -> Path | None:
    idx = gemini_session_index()
    if session_id in idx:
        return idx[session_id]["path"]
    for sid, info in idx.items():
        if sid.startswith(session_id):
            return info["path"]
    return None


def _messages_from_gemini_op(entry: dict):
    messages = []
    direct = entry.get("messages")
    if isinstance(direct, list):
        messages.extend(direct)
    for operator in ("$set", "$push"):
        payload = entry.get(operator)
        if not isinstance(payload, dict):
            continue
        value = payload.get("messages")
        if isinstance(value, list):
            messages.extend(value)
        elif isinstance(value, dict):
            each = value.get("$each")
            if isinstance(each, list):
                messages.extend(each)
            elif "type" in value or "content" in value:
                messages.append(value)
    return [message for message in messages if isinstance(message, dict)]


def _antigravity_messages(path: Path, full: bool):
    messages = []
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue
            source = str(entry.get("source") or "").upper()
            entry_type = str(entry.get("type") or "").upper()
            content = entry.get("content")
            ts = entry.get("created_at") or ""
            if source in {"USER", "USER_EXPLICIT"} or entry_type == "USER_INPUT":
                text = _real_user_text(_content_text(content))
                if text:
                    messages.append({"role": "user", "text": text, "ts": ts})
            elif source == "MODEL":
                text = _content_text(content).strip()
                if text:
                    messages.append({"role": "assistant", "text": text, "ts": ts})
            elif full and source != "SYSTEM":
                text = _content_text(content, include_tools=True).strip()
                if text:
                    messages.append({"role": "tool_result", "text": text, "ts": ts})
    return messages


def _gemini_cli_messages(path: Path, full: bool):
    messages = []
    seen = set()
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue
            for message in _messages_from_gemini_op(entry):
                message_id = message.get("id")
                dedupe_key = message_id or json.dumps(
                    message, ensure_ascii=False, sort_keys=True
                )
                if dedupe_key in seen:
                    continue
                seen.add(dedupe_key)
                message_type = str(message.get("type") or "").lower()
                ts = message.get("timestamp") or ""
                if message_type == "user":
                    text = _real_user_text(_content_text(message.get("content")))
                    if text:
                        messages.append({"role": "user", "text": text, "ts": ts})
                elif message_type in {"gemini", "assistant", "model"}:
                    text = _content_text(
                        message.get("content"), include_tools=full
                    ).strip()
                    if text:
                        messages.append(
                            {
                                "role": "assistant",
                                "text": text,
                                "ts": ts,
                                "model": message.get("model") or "",
                            }
                        )
                elif full:
                    text = _content_text(
                        message.get("content"), include_tools=True
                    ).strip()
                    if text:
                        messages.append({"role": "tool_result", "text": text, "ts": ts})
    return messages


def _read_indexed_messages(info: dict, full: bool):
    fmt = info.get("format")
    if fmt == "antigravity-ide":
        # 빈 목록을 돌려주면 "대화 없음"으로 읽힌다. 못 읽는다는 사실을 남긴다.
        messages = [{"role": "system", "text": ANTIGRAVITY_IDE_LOCKED, "ts": ""}]
        if info.get("title"):
            messages.append(
                {"role": "user", "text": str(info["title"]), "ts": info.get("ts") or ""}
            )
        return messages
    if fmt == "antigravity":
        return _antigravity_messages(info["path"], full)
    return _gemini_cli_messages(info["path"], full)


def read_gemini_conversation(session_id: str, full: bool = False):
    info = gemini_session_index().get(session_id)
    if not info:
        for sid, candidate in gemini_session_index().items():
            if sid.startswith(session_id):
                info = candidate
                break
    if not info or not info["path"].exists():
        return None, None
    return _read_indexed_messages(info, full), info["path"]


def extract_gemini_changed_files(session_id: str):
    fpath = find_gemini_session_file(session_id)
    if not fpath or not fpath.exists():
        return None, None
    # Both local formats preserve conversation text, but neither exposes a
    # stable structured edit-event contract across versions.
    return [], []


def extract_gemini_history(start_ms, end_ms, project_filter=None, cwd_filter=None):
    sessions = {}
    for sid, info in gemini_session_index().items():
        project = info.get("cwd") or ""
        if project_filter and project_filter not in project:
            continue
        if cwd_filter and not path_matches(project, cwd_filter):
            continue
        try:
            conversation = _read_indexed_messages(info, full=False)
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
            index_ts = int(info.get("ts") or 0)
            if not (start_ms <= index_ts < end_ms):
                continue
            # 주입 컨텍스트만 있고 사용자 발화가 없는 세션도 존재 자체는 남긴다.
            first_ts_ms = index_ts
            if info.get("title"):
                previews.append(
                    {"time": ts_to_hm(first_ts_ms), "text": str(info["title"])[:300]}
                )
        sessions[sid] = {
            "project": project,
            "messages": previews,
            "tool": TOOL,
            "first_ts_ms": first_ts_ms,
        }
    return sessions


def grep_gemini_session(fpath: Path, keyword: str, session_id: str | None = None):
    info = next(
        (
            candidate
            for candidate in gemini_session_index().values()
            if candidate["path"] == fpath
        ),
        None,
    )
    if not info:
        return []
    hits = []
    needle = keyword.lower()
    for message in _read_indexed_messages(info, full=True):
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
    notes = []
    locked = sum(
        1
        for info in gemini_session_index().values()
        if info.get("format") == "antigravity-ide"
    )
    if locked:
        notes.append(f"Antigravity IDE 세션 {locked}건은 {ANTIGRAVITY_IDE_LOCKED}")
    notes.append(
        "changed-file 이벤트 계약이 없어 `show --files`의 빈 결과가 무변경을 뜻하지 않는다"
    )
    return notes


def collect_token_rows(start, end, args):
    """These local Gemini transcript formats do not expose stable token usage."""
    return []


def add_token_usage(totals, usage):
    return None


session_index = gemini_session_index
find_session_file = find_gemini_session_file
read_conversation = read_gemini_conversation
extract_changed_files = extract_gemini_changed_files
extract_history = extract_gemini_history
grep_session = grep_gemini_session

register_cache_clearer(gemini_session_index.cache_clear)
register_cache_clearer(_antigravity_metadata.cache_clear)
register_cache_clearer(_antigravity_ide_summaries.cache_clear)
