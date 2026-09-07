"""GitHub Copilot session adapter (CLI + VS Code Chat).

두 저장소가 형식은 다르지만 같은 제품이라 하나로 묶는다.
- CLI: `~/.copilot/session-state/<uuid>/{events.jsonl,workspace.yaml}`
- VS Code: `workspaceStorage/<hash>/chatSessions/<sid>.json`
"""

from __future__ import annotations

import functools
import json
import re
from pathlib import Path

from common import (
    BASH_MUTATION_RE,
    COPILOT_SESSION_STATE_DIR,
    VSCODE_WORKSPACE_STORAGE_DIR,
    iso_to_ms,
    path_matches,
    register_cache_clearer,
    ts_to_hm,
)

TOOL = "copilot"
DISPLAY = "GitHub Copilot (CLI/VS Code)"
SHORT = "Copilot"
TAG = "[P]"
SOURCE_PATHS = (COPILOT_SESSION_STATE_DIR, VSCODE_WORKSPACE_STORAGE_DIR)

_UUID_RE = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")
EDIT_TOOLS = {
    "write",
    "edit",
    "str_replace",
    "create_file",
    "apply_patch",
    "str_replace_editor",
}
# 런타임이 끼워 넣는 발화. 사람이 친 프롬프트가 아니다.
_SYNTHETIC_PREFIXES = (
    "<skill-context",
    "<function_results",
    "<tool_result",
    "<system-reminder>",
)


def _loads(raw):
    try:
        return json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        return None


def _real_user_text(text) -> str:
    stripped = str(text or "").strip()
    if not stripped or stripped.startswith(_SYNTHETIC_PREFIXES):
        return ""
    return stripped


def _iter_events(path: Path):
    try:
        fh = path.open(encoding="utf-8", errors="replace")
    except OSError:
        return
    with fh:
        for line in fh:
            entry = _loads(line)
            if isinstance(entry, dict):
                yield entry


def _read_workspace_yaml(path: Path) -> dict:
    """`key: value`만 있는 평면 YAML이라 파서 없이 읽는다."""
    info: dict[str, str] = {}
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return info
    for line in text.splitlines():
        key, sep, value = line.partition(":")
        if not sep or line[:1].isspace():
            continue
        info[key.strip()] = value.strip().strip("'\"")
    return info


def _vscode_session_obj(path: Path):
    try:
        raw = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    if path.suffix == ".json":
        return _loads(raw)
    # `.jsonl` 변형은 첫 줄에 스냅샷 전체가 `v` 키로 들어 있다.
    first = raw.split("\n", 1)[0]
    wrapper = _loads(first)
    return (wrapper or {}).get("v") if isinstance(wrapper, dict) else None


@functools.lru_cache(maxsize=1)
def copilot_session_index():
    """session_id → {path, cwd, ts, kind}."""
    idx: dict[str, dict] = {}

    if COPILOT_SESSION_STATE_DIR.is_dir():
        for sdir in sorted(COPILOT_SESSION_STATE_DIR.iterdir()):
            # `optimistic-chat-*` 같은 임시 골격은 세션이 아니다.
            if not sdir.is_dir() or not _UUID_RE.match(sdir.name):
                continue
            meta = _read_workspace_yaml(sdir / "workspace.yaml")
            ts = iso_to_ms(meta.get("created_at"))
            events = sdir / "events.jsonl"
            cwd = meta.get("cwd") or ""
            if not ts or not cwd:
                for entry in _iter_events(events):
                    if entry.get("type") != "session.start":
                        continue
                    ts = ts or iso_to_ms(entry.get("timestamp"))
                    cwd = cwd or ((entry.get("data") or {}).get("context") or {}).get(
                        "cwd", ""
                    )
                    break
            idx[sdir.name] = {
                "path": events if events.exists() else sdir,
                "cwd": cwd,
                "ts": ts,
                "kind": "cli",
            }

    if VSCODE_WORKSPACE_STORAGE_DIR.is_dir():
        for wsdir in sorted(VSCODE_WORKSPACE_STORAGE_DIR.iterdir()):
            chats = wsdir / "chatSessions"
            if not chats.is_dir():
                continue
            folder = ""
            meta = (
                _loads(
                    (wsdir / "workspace.json").read_text(
                        encoding="utf-8", errors="replace"
                    )
                )
                if (wsdir / "workspace.json").exists()
                else None
            )
            if isinstance(meta, dict):
                folder = str(meta.get("folder") or "").removeprefix("file://")
            for path in sorted(chats.iterdir()):
                if path.suffix not in (".json", ".jsonl"):
                    continue
                obj = _vscode_session_obj(path)
                if not isinstance(obj, dict) or not obj.get("requests"):
                    continue
                sid = str(obj.get("sessionId") or path.stem)
                idx[sid] = {
                    "path": path,
                    "cwd": folder,
                    "ts": int(obj.get("creationDate") or 0),
                    "kind": "vscode",
                }
    return idx


def _resolve(session_id: str):
    idx = copilot_session_index()
    if session_id in idx:
        return session_id, idx[session_id]
    for sid, info in idx.items():
        if sid.startswith(session_id):
            return sid, info
    return None, None


def find_copilot_session_file(session_id: str) -> Path | None:
    _, info = _resolve(session_id)
    return info["path"] if info else None


def _vscode_response_text(response, full: bool) -> str:
    parts = []
    for part in response or []:
        if not isinstance(part, dict):
            continue
        kind = part.get("kind")
        if kind is None and "value" in part:
            value = part["value"]
            if isinstance(value, dict):
                value = value.get("value")
            if isinstance(value, str):
                parts.append(value)
        elif full and kind == "toolInvocationSerialized":
            message = part.get("invocationMessage")
            if isinstance(message, dict):
                message = message.get("value")
            parts.append(f"[tool: {part.get('toolId', '')}] {message or ''}")
    return "\n".join(p for p in parts if p).strip()


def read_copilot_conversation(session_id: str, full: bool = False):
    _, info = _resolve(session_id)
    if not info:
        return None, None

    messages = []
    if info["kind"] == "vscode":
        obj = _vscode_session_obj(info["path"]) or {}
        for req in obj.get("requests") or []:
            ts = int(req.get("timestamp") or 0) or info["ts"]
            text = _real_user_text((req.get("message") or {}).get("text"))
            if text:
                messages.append({"role": "user", "text": text, "ts": ts})
            reply = _vscode_response_text(req.get("response"), full)
            if reply:
                messages.append(
                    {
                        "role": "assistant",
                        "text": reply,
                        "ts": ts,
                        "model": req.get("modelId") or "",
                    }
                )
        return messages, info["path"]

    for entry in _iter_events(info["path"]):
        etype = entry.get("type")
        data = entry.get("data") or {}
        ts = entry.get("timestamp") or ""
        if etype == "user.message":
            text = _real_user_text(data.get("content"))
            if text:
                messages.append({"role": "user", "text": text, "ts": ts})
        elif etype == "assistant.message":
            text = str(data.get("content") or "").strip()
            if full:
                for req in data.get("toolRequests") or []:
                    if not isinstance(req, dict):
                        continue
                    args = json.dumps(req.get("arguments") or {}, ensure_ascii=False)
                    text += f"\n[tool: {req.get('name', '')}] {args[:200]}"
            if text.strip():
                messages.append(
                    {
                        "role": "assistant",
                        "text": text.strip(),
                        "ts": ts,
                        "model": data.get("model") or "",
                    }
                )
        elif etype == "tool.execution_complete" and full:
            text = str(data.get("result") or data.get("output") or "").strip()
            if text:
                messages.append({"role": "tool_result", "text": text[:500], "ts": ts})
    return messages, info["path"]


def extract_copilot_changed_files(session_id: str):
    _, info = _resolve(session_id)
    if not info:
        return None, None

    changes: list[dict] = []
    bash_hints: list[dict] = []
    seen: set = set()

    def _add(target, tool_name, ts):
        if target and target not in seen:
            seen.add(target)
            changes.append({"file": target, "tool": tool_name, "ts": ts})

    if info["kind"] == "vscode":
        obj = _vscode_session_obj(info["path"]) or {}
        for req in obj.get("requests") or []:
            ts = int(req.get("timestamp") or 0) or info["ts"]
            for part in req.get("response") or []:
                if not isinstance(part, dict):
                    continue
                kind = part.get("kind")
                if kind == "textEditGroup" or (
                    kind == "codeblockUri" and part.get("isEdit")
                ):
                    uri = part.get("uri") or {}
                    _add(uri.get("fsPath") or uri.get("path"), kind, ts)
        return changes, bash_hints

    for entry in _iter_events(info["path"]):
        if entry.get("type") != "tool.execution_start":
            continue
        data = entry.get("data") or {}
        ts = entry.get("timestamp") or ""
        name = str(data.get("toolName") or "")
        args = data.get("arguments")
        if isinstance(args, str):
            args = _loads(args) or {}
        if not isinstance(args, dict):
            continue
        if name.lower() in EDIT_TOOLS:
            _add(
                args.get("path") or args.get("file_path") or args.get("filePath"),
                name,
                ts,
            )
        elif name.lower() in ("bash", "shell", "run_command"):
            cmd = str(args.get("command") or "")
            if cmd and BASH_MUTATION_RE.search(cmd):
                bash_hints.append({"cmd": cmd, "ts": ts})
    return changes, bash_hints


def extract_copilot_history(start_ms, end_ms, project_filter=None, cwd_filter=None):
    sessions = {}
    for sid, info in copilot_session_index().items():
        project = info["cwd"]
        if project_filter and project_filter not in project:
            continue
        if cwd_filter and not path_matches(project, cwd_filter):
            continue

        previews = []
        first_ts_ms = 0
        messages, _ = read_copilot_conversation(sid)
        for message in messages or []:
            if message.get("role") != "user":
                continue
            ts = (
                message["ts"]
                if isinstance(message["ts"], int)
                else iso_to_ms(message["ts"])
            )
            ts = ts or info["ts"]
            if not (start_ms <= ts < end_ms):
                continue
            first_ts_ms = ts if not first_ts_ms else min(first_ts_ms, ts)
            previews.append({"time": ts_to_hm(ts), "text": message["text"][:300]})

        if not previews:
            # 본문이 비어도 세션이 있었다는 사실은 남긴다.
            if not info["ts"] or not (start_ms <= info["ts"] < end_ms):
                continue
            first_ts_ms = info["ts"]
        sessions[sid] = {
            "project": project,
            "messages": previews,
            "tool": TOOL,
            "first_ts_ms": first_ts_ms,
        }
    return sessions


def grep_copilot_session(fpath: Path, keyword: str, session_id: str | None = None):
    sid = session_id
    if not sid:
        sid = next(
            (
                key
                for key, info in copilot_session_index().items()
                if info["path"] == fpath
            ),
            None,
        )
    if not sid:
        return []
    messages, _ = read_copilot_conversation(sid, full=True)
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


def source_notes() -> list[str]:
    notes = []
    idx = copilot_session_index()
    bodyless = sum(
        1
        for info in idx.values()
        if info["kind"] == "cli" and info["path"].name != "events.jsonl"
    )
    if bodyless:
        notes.append(f"CLI 세션 {bodyless}건은 events.jsonl이 없어 메타데이터만 보인다")
    notes.append("VS Code Chat은 token usage를 남기지 않아 비용 집계에서 빠진다")
    return notes


session_index = copilot_session_index
find_session_file = find_copilot_session_file
read_conversation = read_copilot_conversation
extract_changed_files = extract_copilot_changed_files
extract_history = extract_copilot_history
grep_session = grep_copilot_session

register_cache_clearer(copilot_session_index.cache_clear)


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
    cwd_filter = str(Path.cwd()) if getattr(args, "cwd", False) else None
    project_filter = getattr(args, "project", None)

    for sid, info in copilot_session_index().items():
        # VS Code Chat 기록에는 usage가 없다.
        if info["kind"] != "cli" or info["path"].name != "events.jsonl":
            continue
        cwd = info["cwd"]
        if cwd_filter and not path_matches(cwd, cwd_filter):
            continue
        if project_filter and project_filter not in cwd:
            continue
        for entry in _iter_events(info["path"]):
            # 세션 종료 시점의 modelMetrics가 유일한 누적 집계다.
            if entry.get("type") != "session.shutdown":
                continue
            timestamp = parse_ts(entry.get("timestamp"))
            if not in_range(timestamp, start, end):
                continue
            metrics = (entry.get("data") or {}).get("modelMetrics") or {}
            for model, detail in metrics.items():
                if not isinstance(detail, dict):
                    continue
                counts = detail.get("tokenDetails") or {}

                def _count(key, counts=counts):
                    return int((counts.get(key) or {}).get("tokenCount") or 0)

                row = {
                    "tool": TOOL,
                    "timestamp": timestamp.isoformat() if timestamp else None,
                    "session_id": sid,
                    "cwd": cwd,
                    "path": str(info["path"]),
                    "model": model,
                    "subagent": False,
                    "input_tokens": _count("input"),
                    "output_tokens": _count("output"),
                    "cache_read_input_tokens": _count("cache_read"),
                    "cache_creation_input_tokens": _count("cache_write"),
                    "cache_creation_5m_tokens": _count("cache_write"),
                    "cache_creation_1h_tokens": 0,
                }
                row["total_tokens"] = (
                    row["input_tokens"]
                    + row["output_tokens"]
                    + row["cache_read_input_tokens"]
                    + row["cache_creation_input_tokens"]
                )
                if row["total_tokens"]:
                    rows.append(row)
    return rows
