"""Codex session adapter."""

from __future__ import annotations

import datetime
import functools
import json
import re
import sqlite3
from collections import defaultdict
from contextlib import closing
from pathlib import Path

from common import (
    BASH_MUTATION_RE,
    CODEX_ARCHIVED_SESSIONS_DIR,
    CODEX_HISTORY,
    CODEX_SESSIONS_DIR,
    hits_from_messages,
    include_subagents,
    path_matches,
    register_cache_clearer,
    ts_to_hm,
)

TOOL = "codex"
DISPLAY = "Codex"
TAG = "[X]"
# 검색은 연결된 rollout과 별도 입력 기록을 함께 읽는다.
GREP_READS_SESSION_FILE = False
SOURCE_PATHS = (CODEX_HISTORY, CODEX_SESSIONS_DIR, CODEX_ARCHIVED_SESSIONS_DIR)
CODEX_STATE_DB = CODEX_SESSIONS_DIR.parent / "state_5.sqlite"
APPLY_PATCH_HEADER_RE = re.compile(
    r"^\*\*\*\s+(Update|Add|Delete|Move)\s+(?:File|to):\s+(.+?)\s*$", re.MULTILINE
)


def _iter_codex_rollouts():
    """활성 세션과 archived_sessions는 같은 rollout 포맷이라 함께 인덱싱한다."""
    for root in (CODEX_SESSIONS_DIR, CODEX_ARCHIVED_SESSIONS_DIR):
        if not root.exists():
            continue
        yield from root.rglob("rollout-*.jsonl")


@functools.lru_cache(maxsize=1)
def codex_session_index():
    """논리 세션별 모든 rollout을 보존하고 최신 segment를 진입점으로 고른다."""
    idx = {}
    for f in _iter_codex_rollouts():
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
        if not include_subagents():
            src = payload.get("source", "")
            originator = payload.get("originator", "")
            if originator == "codex_exec" or src == "exec":
                continue
            if isinstance(src, dict) and "subagent" in src:
                continue
        item = idx.setdefault(sid, {"segments": []})
        item["segments"].append({"path": f, "meta": payload})
    for item in idx.values():
        item["segments"].sort(
            key=lambda segment: (
                segment["meta"].get("timestamp", ""),
                segment["path"].name,
            )
        )
        latest = item["segments"][-1]
        payload = latest["meta"]
        item.update(
            {
                "path": latest["path"],
                "paths": [segment["path"] for segment in item["segments"]],
                "cwd": payload.get("cwd", ""),
                "ts": item["segments"][0]["meta"].get("timestamp", ""),
                "provider": payload.get("model_provider", ""),
                "name": payload.get("name", ""),
            }
        )
    _backfill_state_metadata(idx)
    return idx


def _backfill_state_metadata(index):
    """보조 인덱스의 이름/provider를 읽어 목록 검색에 보충한다."""
    if not CODEX_STATE_DB.exists() or not index:
        return
    try:
        with closing(sqlite3.connect(f"file:{CODEX_STATE_DB}?mode=ro", uri=True)) as db:
            columns = {row[1] for row in db.execute("pragma table_info(threads)")}
            wanted = [c for c in ("id", "name", "model_provider") if c in columns]
            if "id" not in wanted:
                return
            ids = list(index)
            for offset in range(0, len(ids), 500):
                batch = ids[offset : offset + 500]
                placeholders = ",".join("?" for _ in batch)
                rows = db.execute(
                    f"select {', '.join(wanted)} from threads where id in ({placeholders})",
                    batch,
                )
                for row in rows:
                    data = dict(zip(wanted, row))
                    item = index.get(data["id"])
                    if item:
                        item["name"] = data.get("name") or item.get("name", "")
                        item["provider"] = data.get("model_provider") or item.get(
                            "provider", ""
                        )
    except (OSError, sqlite3.Error):
        return


# ─── Codex session IO ──────────────────────────────────────────

_CONVERSATION_STATUS: dict[str, dict] = {}
_UUID_RE = re.compile(r"[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}")
# history는 제출 시각을 초 단위로, rollout은 전달 시각을 기록한다.
# 확인한 전달 지연(5초 미만)까지만 대응하고 불확실한 입력은 삭제하지 않는다.
_HISTORY_DELIVERY_WINDOW_SECONDS = 5
_INJECTED_PREFIXES = (
    "# AGENTS.md instructions",
    "<environment_context>",
    "<INSTRUCTIONS>",
    "<turn_aborted>",
    "<permissions instructions>",
)


def _resolve_session(session_id):
    index = codex_session_index()
    if session_id in index:
        return session_id, index[session_id]
    matches = [(sid, info) for sid, info in index.items() if sid.startswith(session_id)]
    return matches[0] if len(matches) == 1 else (None, None)


def conversation_status(session_id):
    """직전 읽기의 출처/누락 상태. 원본이나 Codex 인덱스를 수정하지 않는다."""
    sid, _ = _resolve_session(session_id)
    return _CONVERSATION_STATUS.get(sid, {})


def _warning(status, message):
    if message not in status["warnings"]:
        status["warnings"].append(message)


def _session_records(session_id):
    sid, info = _resolve_session(session_id)
    if not info:
        return
    status = {
        "warnings": [],
        "files": [],
        "history_only_count": 0,
        "_excluded_inputs": [],
    }
    _CONVERSATION_STATUS[sid] = status
    segments = {}
    for entry in codex_session_index().values():
        for segment in entry["segments"]:
            # 분할 filename의 마지막 UUID가 storage id다. payload.id는 논리 id로 반복된다.
            ids = _UUID_RE.findall(segment["path"].stem)
            storage_id = (
                ids[-1]
                if ids
                else segment["meta"].get("session_id", segment["meta"].get("id"))
            )
            segments[storage_id] = segment
    visiting = set()
    excluded_ids = set()

    def exclude(row):
        entry = _record_user_input(row)
        if entry:
            if any(
                old["text"] == entry["text"]
                and old["representation"] != entry["representation"]
                and not (old["id"] and entry["id"] and old["id"] != entry["id"])
                and abs(_timestamp(old["ts"]) - _timestamp(entry["ts"])) <= 1
                for old in status["_excluded_inputs"][-3:]
            ):
                return
            key = (entry.get("id") or entry["ts"], entry["text"])
            if key not in excluded_ids:
                excluded_ids.add(key)
                status["_excluded_inputs"].append(entry)

    def visit(segment, cutoff=None):
        path, meta = segment["path"], segment["meta"]
        if path in visiting:
            _warning(status, "rollout 연결에 순환이 있어 일부 기록을 읽지 못했습니다.")
            return
        visiting.add(path)
        base = meta.get("history_base")
        if isinstance(base, dict):
            parent = segments.get(base.get("thread_id"))
            if parent is None:
                _warning(status, "이전 rollout 파일이 없어 앞부분 전사는 불완전합니다.")
            else:
                parent_cutoff = dict(base)
                inherited = cutoff.get("end_ordinal_exclusive") if cutoff else None
                boundary = parent_cutoff.get("end_ordinal_exclusive")
                if isinstance(inherited, int) and isinstance(boundary, int):
                    parent_cutoff["end_ordinal_exclusive"] = min(inherited, boundary)
                yield from visit(parent, parent_cutoff)
        status["files"].append(str(path))
        try:
            size = path.stat().st_size
            end_byte = cutoff.get("end_byte_offset") if cutoff else None
            end_ordinal = cutoff.get("end_ordinal_exclusive") if cutoff else None
            valid_byte = isinstance(end_byte, int) and 0 <= end_byte <= size
            if isinstance(end_byte, int) and not valid_byte:
                _warning(
                    status,
                    "rollout byte offset이 파일 크기를 벗어납니다. ordinal로 읽은 복원본이며 Codex resume 복구가 아닙니다.",
                )
            with path.open("rb") as stream:
                offset = 0
                for number, line in enumerate(stream, 1):
                    start = offset
                    offset += len(line)
                    try:
                        row = json.loads(line)
                    except (ValueError, UnicodeDecodeError):
                        _warning(
                            status,
                            "해석할 수 없는 rollout 행이 있어 전사는 불완전합니다.",
                        )
                        continue
                    if not isinstance(row, dict) or row.get("type") == "session_meta":
                        continue
                    ordinal = row.get("ordinal")
                    if isinstance(end_ordinal, int) and isinstance(ordinal, int):
                        if ordinal >= end_ordinal:
                            exclude(row)
                            continue
                    elif valid_byte:
                        if start >= end_byte:
                            exclude(row)
                            continue
                    elif cutoff:
                        _warning(
                            status,
                            "이전 rollout 경계를 확인할 수 없어 일부 중복이나 폐기된 기록이 포함될 수 있습니다.",
                        )
                    yield path, number, row
        except OSError:
            _warning(status, "rollout 파일을 읽지 못해 전사는 불완전합니다.")
        visiting.remove(path)

    yield from visit(info["segments"][-1])


def _content_text(value):
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return "\n".join(filter(None, (_content_text(item) for item in value)))
    if isinstance(value, dict):
        if value.get("type") in (
            "input_image",
            "image",
            "image_url",
            "encrypted_content",
        ):
            return ""
        if isinstance(value.get("text"), str):
            return value["text"]
        if "content" in value:
            return _content_text(value["content"])
        return json.dumps(value, ensure_ascii=False)
    return "" if value is None else str(value)


def _prompt_key(text):
    # history에는 첨부 마커만, rollout에는 같은 마커 앞뒤의 image tag도 남는다.
    text = re.sub(r"</?image\b[^>]*>", "", text)
    return " ".join(text.split())


def _record_user_input(row):
    payload = row.get("payload") or {}
    if not isinstance(payload, dict):
        return None
    kind, typ = row.get("type"), payload.get("type")
    if kind == "event_msg" and typ == "item_completed":
        payload = payload.get("item") or {}
        if not isinstance(payload, dict) or payload.get("type") != "userMessage":
            return None
        text = _content_text(payload.get("content", ""))
    elif kind == "event_msg" and typ == "user_message":
        text = _content_text(payload.get("message", ""))
    elif kind == "response_item" and typ == "message" and payload.get("role") == "user":
        text = _content_text(payload.get("content", ""))
    else:
        return None
    text = text.strip()
    if not text or text.startswith(_INJECTED_PREFIXES):
        return None
    return {
        "text": text,
        "ts": row.get("timestamp", ""),
        "id": str(payload.get("id") or "").removeprefix("msg_"),
        "representation": f"{kind}/{typ}",
    }


@functools.lru_cache(maxsize=1)
def _input_history():
    entries = defaultdict(list)
    try:
        with CODEX_HISTORY.open(encoding="utf-8") as stream:
            for number, line in enumerate(stream, 1):
                try:
                    row = json.loads(line)
                    text = row.get("text", "")
                    timestamp = datetime.datetime.fromtimestamp(
                        float(row.get("ts", 0)), datetime.timezone.utc
                    ).isoformat()
                    if isinstance(text, str) and text.strip():
                        entries[row.get("session_id", "")].append(
                            {
                                "role": "user",
                                "text": text.strip(),
                                "ts": timestamp,
                                "source": "history",
                                "source_path": str(CODEX_HISTORY),
                                "source_line": number,
                            }
                        )
                except (ValueError, TypeError, AttributeError, OverflowError, OSError):
                    continue
    except OSError:
        pass
    return entries


def _timestamp(value):
    try:
        return datetime.datetime.fromisoformat(value.replace("Z", "+00:00")).timestamp()
    except (AttributeError, ValueError):
        return 0


def find_codex_session_file(session_id: str) -> Path | None:
    _, info = _resolve_session(session_id)
    return info["path"] if info else None


def read_codex_conversation(session_id: str, full: bool = False):
    """연결된 전사에 누락된 입력만 history에서 보충하고 출처를 표시한다."""
    sid, _ = _resolve_session(session_id)
    fpath = find_codex_session_file(session_id)
    if not fpath:
        return None, None

    messages, representations, identities, seen_ids = [], [], [], set()
    for path, line, row in _session_records(sid):
        payload = row.get("payload") or {}
        if not isinstance(payload, dict):
            continue
        kind, typ = row.get("type"), payload.get("type")
        role, text, ident = None, "", payload.get("id")
        representation = kind
        if kind == "event_msg" and typ == "item_completed":
            payload = payload.get("item") or {}
            if not isinstance(payload, dict):
                continue
            typ, ident = payload.get("type"), payload.get("id")
            representation = "item_completed"
            if typ in ("userMessage", "agentMessage"):
                role = "user" if typ == "userMessage" else "assistant"
                text = _content_text(payload.get("content", payload.get("text", "")))
        elif kind == "event_msg" and typ in ("user_message", "agent_message"):
            role = "user" if typ == "user_message" else "assistant"
            text = _content_text(payload.get("message", ""))
        elif kind == "response_item" and typ == "message":
            role = payload.get("role")
            if role not in ("user", "assistant"):
                continue
            text = _content_text(payload.get("content", ""))
        elif kind == "response_item" and full:
            if typ in ("function_call", "custom_tool_call"):
                role = "tool_call"
                text = f"[{payload.get('name', '')}] " + _content_text(
                    payload.get("arguments") or payload.get("input", "")
                )
            elif typ in ("function_call_output", "custom_tool_call_output"):
                role, text = "tool_result", _content_text(payload.get("output", ""))
        elif kind == "event_msg" and full and typ == "patch_apply_begin":
            role, text = (
                "tool",
                json.dumps(payload.get("changes") or {}, ensure_ascii=False),
            )
        text = text.strip()
        if (
            not role
            or not text
            or (role == "user" and text.startswith(_INJECTED_PREFIXES))
        ):
            continue
        ts = row.get("timestamp", "")
        ident_key = None
        if role in ("user", "assistant"):
            ident_key = (role, str(ident).removeprefix("msg_")) if ident else None
            if ident_key and ident_key in seen_ids:
                continue
            # Legacy events may have no id. Only collapse a different representation
            # of the same immediate message, never repeated user submissions.
            if any(
                old["role"] == role
                and old["text"] == text
                and rep != representation
                and not (ident_key and old_id and ident_key != old_id)
                and abs(_timestamp(old["ts"]) - _timestamp(ts)) <= 1
                for old, rep, old_id in zip(
                    messages[-3:], representations[-3:], identities[-3:]
                )
            ):
                continue
            if ident_key:
                seen_ids.add(ident_key)
        msg = {
            "role": role,
            "text": text,
            "ts": ts,
            "source": "rollout",
            "source_path": str(path),
            "source_line": line,
        }
        if payload.get("phase"):
            msg["phase"] = payload["phase"]
        if payload.get("call_id"):
            msg["call_id"] = payload["call_id"]
        messages.append(msg)
        representations.append(representation)
        identities.append(ident_key)
    inputs = _input_history().get(sid, [])
    unmatched = set(range(len(inputs)))
    status = _CONVERSATION_STATUS[sid]
    user_entries = [(msg, False) for msg in messages if msg["role"] == "user"]
    user_entries.extend((entry, True) for entry in status.pop("_excluded_inputs", []))
    excluded_matches = 0
    for msg, excluded in user_entries:
        key = _prompt_key(msg["text"])
        candidates = [
            i
            for i in unmatched
            if _prompt_key(inputs[i]["text"]) == key
            and 0
            <= _timestamp(msg["ts"]) - _timestamp(inputs[i]["ts"])
            <= _HISTORY_DELIVERY_WINDOW_SECONDS
        ]
        if candidates:
            # 같은 문장을 여러 번 제출했다면 저장된 메시지와 가장 가까운 입력을 대응한다.
            closest = min(
                candidates,
                key=lambda i: (
                    abs(_timestamp(inputs[i]["ts"]) - _timestamp(msg["ts"])),
                    i,
                ),
            )
            unmatched.remove(closest)
            excluded_matches += int(excluded)
    recovered = [dict(inputs[i]) for i in sorted(unmatched)]
    status["excluded_history_count"] = excluded_matches
    if excluded_matches:
        _warning(
            status,
            f"분기 경계에서 제외된 사용자 입력 {excluded_matches}건은 현재 전사에 다시 넣지 않았습니다.",
        )
    status["history_only_count"] = len(recovered)
    if recovered:
        _warning(
            status,
            f"history.jsonl에서 사용자 입력 {len(recovered)}건만 보충했습니다. 해당 응답/도구 실행은 미확인입니다. 전사 끝을 세션의 마지막 요청으로 단정하지 마세요.",
        )
        messages.extend(recovered)
        messages.sort(key=lambda msg: _timestamp(msg["ts"]))
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

    for _, _, d in _session_records(session_id):
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
                    raw = (
                        args_obj.get("input", "") if isinstance(args_obj, dict) else ""
                    )
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
            cmd_field = (
                args_obj.get("command", "") if isinstance(args_obj, dict) else ""
            )
            cmd = " ".join(cmd_field) if isinstance(cmd_field, list) else str(cmd_field)
            if cmd and BASH_MUTATION_RE.search(cmd):
                bash_hints.append({"cmd": cmd, "ts": ts})

    return changes, bash_hints


# ─── History extraction ────────────────────────────────────────


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
                p = d.get("payload", {}) or {}
                text = ""
                if d.get("type") == "event_msg" and p.get("type") == "user_message":
                    text = _content_text(p.get("message", ""))
                elif (
                    d.get("type") == "response_item"
                    and p.get("type") == "message"
                    and p.get("role") == "user"
                ):
                    text = _content_text(p.get("content", ""))
                text = text.strip()
                if text and not text.startswith(_INJECTED_PREFIXES):
                    return text
    except OSError:
        pass
    return ""


def extract_codex_history(start_ms, end_ms, project_filter=None, cwd_filter=None):
    sessions = defaultdict(
        lambda: {
            "project": "",
            "messages": [],
            "tool": "codex",
            "first_ts_ms": 0,
            "name": "",
            "provider": "",
        }
    )
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
                sessions[sid]["name"] = index[sid].get("name", "")
                sessions[sid]["provider"] = index[sid].get("provider", "")
                if not sessions[sid]["first_ts_ms"]:
                    sessions[sid]["first_ts_ms"] = ts_ms
                else:
                    sessions[sid]["first_ts_ms"] = min(
                        sessions[sid]["first_ts_ms"], ts_ms
                    )
                if text:
                    sessions[sid]["messages"].append(
                        {"time": ts_to_hm(ts_ms), "text": text[:300]}
                    )

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
        entry["name"] = info.get("name", "")
        entry["provider"] = info.get("provider", "")
        entry["first_ts_ms"] = ts_ms
        first_msg = codex_first_user_message(info["path"])
        if first_msg:
            entry["messages"].append({"time": ts_to_hm(ts_ms), "text": first_msg[:300]})

    return dict(sessions)


# ─── list 서브커맨드 ──────────────────────────────────────────


def grep_codex_session(fpath: Path, keyword, session_id: str | None = None):
    """show와 같은 연결 전사/입력 복원본을 검색한다."""
    if session_id is None:
        session_id = next(
            (
                sid
                for sid, info in codex_session_index().items()
                if fpath in info["paths"]
            ),
            None,
        )
    if session_id is None:
        return []
    messages, _ = read_codex_conversation(session_id, full=True)
    return hits_from_messages(messages, keyword)


session_index = codex_session_index
find_session_file = find_codex_session_file
read_conversation = read_codex_conversation
extract_changed_files = extract_codex_changed_files
extract_history = extract_codex_history
grep_session = grep_codex_session

register_cache_clearer(codex_session_index.cache_clear)
register_cache_clearer(_input_history.cache_clear)
register_cache_clearer(_CONVERSATION_STATUS.clear)


# ─── token usage ───────────────────────────────────────────────

SHORT = "Codex"


def add_token_usage(totals, usage):
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
    pure_tokens = max(0, input_tokens - cached_input) + output_tokens
    totals["effective_tokens"] += pure_tokens
    totals["pure_tokens"] += pure_tokens
    totals["cache_tokens"] += cached_input
    totals["calls"] += 1


def _read_codex_meta(path: Path):
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


def _extract_thread_model(payload: dict) -> str:
    """thread_settings_applied.payload.thread_settings.model (not model_provider)."""
    settings = payload.get("thread_settings") or {}
    if isinstance(settings, dict):
        model = settings.get("model") or ""
        if model:
            return str(model)
    model = payload.get("model") or ""
    return str(model) if model else ""


def collect_token_rows(start, end, args):
    from pathlib import Path

    from common import in_range, parse_ts, path_matches

    rows = []
    for path in _iter_codex_rollouts():
        meta = _read_codex_meta(path)
        cwd = meta.get("cwd") or ""
        source = meta.get("source")
        subagent = (
            meta.get("originator") == "codex_exec"
            or source == "exec"
            or (isinstance(source, dict) and "subagent" in source)
        )
        if getattr(args, "main_only", False) and subagent:
            continue
        if getattr(args, "cwd", False) and not path_matches(cwd, str(Path.cwd())):
            continue
        if getattr(args, "project", None) and args.project not in cwd:
            continue

        # Prefer real model from thread_settings_applied; never use model_provider.
        current_model = meta.get("model") or meta.get("default_model") or ""
        # Provider/tool labels are not model ids (openai/codex/…).
        if current_model in ("", "openai", "codex", "anthropic", "xai"):
            current_model = ""

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
                ptype = payload.get("type")
                if ptype == "thread_settings_applied":
                    model = _extract_thread_model(payload)
                    if model:
                        current_model = model
                    continue
                if ptype != "token_count":
                    continue
                timestamp = parse_ts(entry.get("timestamp"))
                if not in_range(timestamp, start, end):
                    continue
                info = payload.get("info") or {}
                usage = info.get("last_token_usage") or {}
                if not usage:
                    continue
                # Some token_count events may carry model on info
                model = current_model or info.get("model") or ""
                row = {
                    "tool": TOOL,
                    "timestamp": timestamp.isoformat() if timestamp else None,
                    "session_id": meta.get("id") or path.stem,
                    "cwd": cwd,
                    "path": str(path),
                    "model": model,
                    "subagent": subagent,
                    "input_tokens": int(usage.get("input_tokens") or 0),
                    "cached_input_tokens": int(usage.get("cached_input_tokens") or 0),
                    "output_tokens": int(usage.get("output_tokens") or 0),
                    "reasoning_output_tokens": int(
                        usage.get("reasoning_output_tokens") or 0
                    ),
                    "total_tokens": int(usage.get("total_tokens") or 0),
                }
                if not row["total_tokens"]:
                    row["total_tokens"] = row["input_tokens"] + row["output_tokens"]
                rows.append(row)

    return rows
