"""OpenClaw 계열(openclaw, senpi, gjc) session adapter.

세 도구가 같은 JSONL 계보를 쓴다. 첫 줄이 `{"type":"session", ...}` 헤더이고
이후 `{"type":"message","message":{"role":...}}`가 이어진다. 어댑터를 하나로 두면
도구가 늘어도 ROOTS만 추가하면 된다.
"""

from __future__ import annotations

import functools
import json
from pathlib import Path

from common import (
    BASH_MUTATION_RE,
    OPENCLAW_ROOTS,
    include_subagents,
    iso_to_ms,
    path_matches,
    register_cache_clearer,
    ts_to_hm,
)

TOOL = "openclaw"
DISPLAY = "OpenClaw/senpi/gjc"
SHORT = "OpenClaw"
TAG = "[W]"
SOURCE_PATHS = tuple(root for root, _ in OPENCLAW_ROOTS)

EDIT_TOOLS = {"write", "edit", "str_replace", "create_file", "apply_patch"}
SHELL_TOOLS = {"bash", "exec", "shell"}
# 사람이 입력한 게 아니라 런타임이 끼워넣는 발화들.
_SYNTHETIC_PREFIXES = (
    "A new session was started via",
    "Conversation info (untrusted metadata):",
    "[Queued messages while agent was busy]",
    "<skill name=",
    "<system-reminder>",
    "<user_info>",
    "<omo-senpi-task>",
)


def _loads(raw):
    try:
        return json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        return None


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


def _real_user_text(text: str) -> str:
    stripped = (text or "").strip()
    if not stripped or stripped.startswith(_SYNTHETIC_PREFIXES):
        return ""
    return stripped


def _iter_lines(path: Path):
    try:
        fh = path.open(encoding="utf-8", errors="replace")
    except OSError:
        return
    with fh:
        for line in fh:
            entry = _loads(line)
            if entry is not None:
                yield entry


def _session_header(path: Path):
    for entry in _iter_lines(path):
        return entry if entry.get("type") == "session" else None
    return None


@functools.lru_cache(maxsize=1)
def openclaw_session_index():
    """session_id → {path, cwd, ts, brand, archived}."""
    idx: dict[str, dict] = {}
    for root, brand in OPENCLAW_ROOTS:
        if not root.is_dir():
            continue
        for path in sorted(root.rglob("*.jsonl*")):
            try:
                if not path.is_file() or path.stat().st_size == 0:
                    continue
            except OSError:
                continue
            header = _session_header(path)
            if not header:
                continue
            sid = header.get("id") or path.stem
            # `.jsonl.reset.<ts>`는 같은 세션의 이전 회차라 ID가 겹친다.
            archived = ".reset." in path.name
            if sid in idx:
                if not archived:
                    idx[sid].update({"path": path, "archived": False})
                    continue
                sid = f"{sid}@{path.name.split('.reset.')[-1]}"
            if archived and not include_subagents():
                # 리셋 이전 기록은 기본 목록에서 빼되 요청하면 볼 수 있게 둔다.
                continue
            idx[sid] = {
                "path": path,
                "cwd": header.get("cwd") or "",
                "ts": iso_to_ms(header.get("timestamp")),
                "brand": brand,
                "archived": archived,
            }
    return idx


def _resolve(session_id: str):
    idx = openclaw_session_index()
    if session_id in idx:
        return session_id, idx[session_id]
    for sid, info in idx.items():
        if sid.startswith(session_id):
            return sid, info
    return None, None


def find_openclaw_session_file(session_id: str) -> Path | None:
    _, info = _resolve(session_id)
    return info["path"] if info else None


def read_openclaw_conversation(session_id: str, full: bool = False):
    _, info = _resolve(session_id)
    if not info:
        return None, None

    messages = []
    for entry in _iter_lines(info["path"]):
        if entry.get("type") != "message":
            continue
        message = entry.get("message") or {}
        role = message.get("role")
        ts = entry.get("timestamp") or ""
        if role == "user":
            text = _real_user_text(_content_text(message.get("content")))
            if text:
                messages.append({"role": "user", "text": text, "ts": ts})
        elif role == "assistant":
            text = _content_text(message.get("content")).strip()
            if full:
                for part in message.get("content") or []:
                    if isinstance(part, dict) and part.get("type") == "toolCall":
                        args = json.dumps(
                            part.get("arguments") or {}, ensure_ascii=False
                        )
                        text += f"\n[tool: {part.get('name', '')}] {args[:200]}"
            if text.strip():
                messages.append(
                    {
                        "role": "assistant",
                        "text": text.strip(),
                        "ts": ts,
                        "model": message.get("model") or "",
                    }
                )
        elif role == "toolResult" and full:
            text = _content_text(message.get("content")).strip()
            if text:
                messages.append({"role": "tool_result", "text": text[:500], "ts": ts})
    return messages, info["path"]


def extract_openclaw_changed_files(session_id: str):
    _, info = _resolve(session_id)
    if not info:
        return None, None

    changes: list[dict] = []
    bash_hints: list[dict] = []
    seen: set = set()
    for entry in _iter_lines(info["path"]):
        if entry.get("type") != "message":
            continue
        message = entry.get("message") or {}
        if message.get("role") != "assistant":
            continue
        ts = entry.get("timestamp") or ""
        for part in message.get("content") or []:
            if not isinstance(part, dict) or part.get("type") != "toolCall":
                continue
            name = part.get("name", "")
            inp = part.get("arguments") or {}
            if not isinstance(inp, dict):
                continue
            if name in EDIT_TOOLS:
                target = inp.get("path") or inp.get("file_path") or inp.get("filePath")
                if target and target not in seen:
                    seen.add(target)
                    changes.append({"file": target, "tool": name, "ts": ts})
            elif name in SHELL_TOOLS:
                cmd = str(inp.get("command") or "")
                if cmd and BASH_MUTATION_RE.search(cmd):
                    bash_hints.append({"cmd": cmd, "ts": ts})
    return changes, bash_hints


def extract_openclaw_history(start_ms, end_ms, project_filter=None, cwd_filter=None):
    sessions = {}
    for sid, info in openclaw_session_index().items():
        project = info["cwd"]
        if project_filter and project_filter not in project:
            continue
        if cwd_filter and not path_matches(project, cwd_filter):
            continue

        previews = []
        first_ts_ms = 0
        for entry in _iter_lines(info["path"]):
            if entry.get("type") != "message":
                continue
            message = entry.get("message") or {}
            if message.get("role") != "user":
                continue
            text = _real_user_text(_content_text(message.get("content")))
            if not text:
                continue
            ts = iso_to_ms(entry.get("timestamp")) or info["ts"]
            if not (start_ms <= ts < end_ms):
                continue
            first_ts_ms = ts if not first_ts_ms else min(first_ts_ms, ts)
            previews.append({"time": ts_to_hm(ts), "text": text[:300]})

        if not previews:
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


def grep_openclaw_session(fpath: Path, keyword: str, session_id: str | None = None):
    sid = session_id
    if not sid:
        sid = next(
            (
                key
                for key, info in openclaw_session_index().items()
                if info["path"] == fpath
            ),
            None,
        )
    if not sid:
        return []
    messages, _ = read_openclaw_conversation(sid, full=True)
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


session_index = openclaw_session_index
find_session_file = find_openclaw_session_file
read_conversation = read_openclaw_conversation
extract_changed_files = extract_openclaw_changed_files
extract_history = extract_openclaw_history
grep_session = grep_openclaw_session

register_cache_clearer(openclaw_session_index.cache_clear)


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

    for sid, info in openclaw_session_index().items():
        cwd = info["cwd"]
        if cwd_filter and not path_matches(cwd, cwd_filter):
            continue
        if project_filter and project_filter not in cwd:
            continue
        for entry in _iter_lines(info["path"]):
            if entry.get("type") != "message":
                continue
            message = entry.get("message") or {}
            if message.get("role") != "assistant":
                continue
            usage = message.get("usage") or {}
            if not usage:
                continue
            timestamp = parse_ts(entry.get("timestamp"))
            if not in_range(timestamp, start, end):
                continue
            row = {
                "tool": TOOL,
                "timestamp": timestamp.isoformat() if timestamp else None,
                "session_id": sid,
                "cwd": cwd,
                "path": str(info["path"]),
                "model": message.get("model") or "",
                "subagent": False,
                "input_tokens": int(usage.get("input") or 0),
                "output_tokens": int(usage.get("output") or 0),
                "cache_read_input_tokens": int(usage.get("cacheRead") or 0),
                "cache_creation_input_tokens": int(usage.get("cacheWrite") or 0),
                "cache_creation_5m_tokens": int(usage.get("cacheWrite") or 0),
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
