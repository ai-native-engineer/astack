"""Codex session adapter."""

from __future__ import annotations

import datetime
import functools
import json
import re
from collections import defaultdict
from pathlib import Path

from common import (
    BASH_MUTATION_RE,
    CODEX_HISTORY,
    CODEX_SESSIONS_DIR,
    include_subagents,
    path_matches,
    register_cache_clearer,
    ts_to_hm,
)

TOOL = "codex"
DISPLAY = "Codex"
TAG = "[X]"
APPLY_PATCH_HEADER_RE = re.compile(
    r"^\*\*\*\s+(Update|Add|Delete|Move)\s+(?:File|to):\s+(.+?)\s*$", re.MULTILINE
)


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
        if not include_subagents():
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


# ─── Grok session IO ───────────────────────────────────────────

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


session_index = codex_session_index
find_session_file = find_codex_session_file
read_conversation = read_codex_conversation
extract_changed_files = extract_codex_changed_files
extract_history = extract_codex_history
grep_session = grep_codex_session

register_cache_clearer(codex_session_index.cache_clear)


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

    from common import CODEX_SESSIONS_DIR, in_range, parse_ts, path_matches

    rows = []
    if not CODEX_SESSIONS_DIR.exists():
        return rows

    for path in CODEX_SESSIONS_DIR.rglob("rollout-*.jsonl"):
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
        current_model = (
            meta.get("model")
            or meta.get("default_model")
            or ""
        )
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
                model = (
                    current_model
                    or info.get("model")
                    or ""
                )
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
                    "reasoning_output_tokens": int(usage.get("reasoning_output_tokens") or 0),
                    "total_tokens": int(usage.get("total_tokens") or 0),
                }
                if not row["total_tokens"]:
                    row["total_tokens"] = row["input_tokens"] + row["output_tokens"]
                rows.append(row)

    return rows
