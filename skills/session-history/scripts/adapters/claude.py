"""Claude Code session adapter."""

from __future__ import annotations

import functools
import json
from collections import defaultdict
from pathlib import Path

from common import (
    BASH_MUTATION_RE,
    CLAUDE_HISTORY,
    CLAUDE_PROJECTS_DIR,
    include_subagents,
    path_matches,
    register_cache_clearer,
    ts_to_hm,
)

TOOL = "claude"
DISPLAY = "Claude Code"
TAG = "[C]"
EDIT_TOOLS = {"Edit", "Write", "MultiEdit", "NotebookEdit"}


@functools.lru_cache(maxsize=1)
def claude_conversation_index():
    """session_id (stem) → conversation jsonl Path."""
    idx = {}
    if not CLAUDE_PROJECTS_DIR.exists():
        return idx
    for f in CLAUDE_PROJECTS_DIR.rglob("*.jsonl"):
        if not include_subagents() and "/subagents/" in str(f):
            continue
        idx[f.stem] = f
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


# Public adapter surface (stable names for CLI)
session_index = claude_conversation_index
find_session_file = find_claude_conversation_file
read_conversation = read_claude_conversation
extract_changed_files = extract_claude_changed_files
extract_history = extract_claude_history
grep_session = grep_claude_session

register_cache_clearer(claude_conversation_index.cache_clear)


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
    if not CLAUDE_PROJECTS_DIR.exists():
        return []

    def is_subagent_path(path: Path) -> bool:
        return "/subagents/" in str(path)

    for path in CLAUDE_PROJECTS_DIR.rglob("*.jsonl"):
        if getattr(args, "main_only", False) and is_subagent_path(path):
            continue
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
                if getattr(args, "cwd", False) and not path_matches(cwd, str(Path.cwd())):
                    continue
                if getattr(args, "project", None) and args.project not in cwd:
                    continue

                request_id = entry.get("requestId") or message.get("id") or f"{path}:{line_no}"
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
                    "cache_read_input_tokens": int(usage.get("cache_read_input_tokens") or 0),
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
