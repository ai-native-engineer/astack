"""Grok session adapter."""

from __future__ import annotations

import functools
import json
import re
from collections import defaultdict
from pathlib import Path
from urllib.parse import unquote

from common import (
    BASH_MUTATION_RE,
    GROK_SESSIONS_DIR,
    iso_to_ms,
    path_matches,
    register_cache_clearer,
    ts_to_hm,
)

TOOL = "grok"
DISPLAY = "Grok"
TAG = "[G]"
EDIT_TOOLS = {"search_replace", "write"}
USER_QUERY_RE = re.compile(r"<user_query>\s*(.*?)\s*</user_query>", re.DOTALL | re.IGNORECASE)


def grok_content_text(content) -> str:
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for part in content:
            if isinstance(part, dict):
                if part.get("type") == "text":
                    parts.append(part.get("text") or "")
                elif isinstance(part.get("text"), str):
                    parts.append(part["text"])
                elif isinstance(part.get("content"), str):
                    parts.append(part["content"])
            elif isinstance(part, str):
                parts.append(part)
        return "\n".join(parts)
    if isinstance(content, dict):
        if isinstance(content.get("text"), str):
            return content["text"]
        if isinstance(content.get("content"), str):
            return content["content"]
        return json.dumps(content, ensure_ascii=False)
    return str(content)

def extract_user_query_text(text: str) -> str:
    if not text:
        return ""
    match = USER_QUERY_RE.search(text)
    if match:
        return match.group(1).strip()
    return text.strip()

def is_real_grok_user_message(entry: dict) -> bool:
    if entry.get("type") != "user":
        return False
    if entry.get("synthetic_reason"):
        return False
    text = grok_content_text(entry.get("content"))
    if not text.strip():
        return False
    if "<user_query>" in text:
        return True
    stripped = text.lstrip()
    if stripped.startswith(("<user_info>", "<system-reminder>", "You are Grok")):
        return False
    return True

@functools.lru_cache(maxsize=1)
def grok_session_index():
    """session_id → {path(chat_history), summary_path, cwd, ts, title}."""
    idx = {}
    if not GROK_SESSIONS_DIR.exists():
        return idx
    for summary in GROK_SESSIONS_DIR.rglob("summary.json"):
        if summary.name.endswith(".lock"):
            continue
        try:
            data = json.loads(summary.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        info = data.get("info") or {}
        sid = info.get("id") or summary.parent.name
        if not sid:
            continue
        cwd = info.get("cwd") or ""
        if not cwd:
            try:
                cwd = unquote(summary.parent.parent.name)
            except Exception:
                cwd = ""
        chat = summary.parent / "chat_history.jsonl"
        created = data.get("created_at") or data.get("last_active_at") or data.get("updated_at") or ""
        title = (
            data.get("session_summary")
            or data.get("generated_title")
            or ""
        )
        idx[sid] = {
            "path": chat if chat.exists() else None,
            "summary_path": summary,
            "cwd": cwd,
            "ts": created,
            "title": title,
            "updated_at": data.get("updated_at") or data.get("last_active_at") or created,
        }
    return idx

def find_grok_session_file(session_id: str) -> Path | None:
    idx = grok_session_index()
    if session_id in idx:
        return idx[session_id].get("path")
    for sid, info in idx.items():
        if sid.startswith(session_id):
            return info.get("path")
    return None

def grok_first_user_message(fpath: Path | None, max_lines: int = 300) -> str:
    if not fpath or not fpath.exists():
        return ""
    try:
        with open(fpath, encoding="utf-8") as f:
            for i, line in enumerate(f):
                if i >= max_lines:
                    break
                try:
                    d = json.loads(line.strip())
                except json.JSONDecodeError:
                    continue
                if not is_real_grok_user_message(d):
                    continue
                text = extract_user_query_text(grok_content_text(d.get("content")))
                if text:
                    return text
    except OSError:
        pass
    return ""

def read_grok_conversation(session_id: str, full: bool = False):
    """(messages, fpath) 반환. chat_history 항목에는 타임스탬프가 없을 수 있다."""
    fpath = find_grok_session_file(session_id)
    if not fpath or not fpath.exists():
        return None, None

    messages = []
    with open(fpath, encoding="utf-8") as f:
        for line in f:
            try:
                d = json.loads(line.strip())
            except json.JSONDecodeError:
                continue
            entry_type = d.get("type", "")
            ts = d.get("timestamp") or d.get("ts") or ""

            if entry_type == "user":
                if not is_real_grok_user_message(d):
                    continue
                text = extract_user_query_text(grok_content_text(d.get("content")))
                if text.strip():
                    messages.append({"role": "user", "text": text.strip(), "ts": ts})
                continue

            if entry_type == "assistant":
                text = grok_content_text(d.get("content")).strip()
                tool_calls = d.get("tool_calls") or []
                if full and tool_calls:
                    labels = []
                    for tc in tool_calls:
                        if not isinstance(tc, dict):
                            continue
                        name = tc.get("name") or ""
                        args = tc.get("arguments") or ""
                        if not isinstance(args, str):
                            args = json.dumps(args, ensure_ascii=False)
                        labels.append(f"[tool: {name}] {args[:200]}")
                    if labels:
                        text = (text + "\n" if text else "") + "\n".join(labels)
                if text.strip():
                    messages.append({
                        "role": "assistant",
                        "text": text.strip(),
                        "ts": ts,
                        "model": d.get("model_id") or "",
                    })
                continue

            if entry_type == "tool_result" and full:
                result = grok_content_text(d.get("content"))
                if result.strip():
                    messages.append({"role": "tool", "text": result[:500], "ts": ts})

    return messages, fpath

def extract_grok_changed_files(session_id: str):
    fpath = find_grok_session_file(session_id)
    if not fpath or not fpath.exists():
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
            ts = d.get("timestamp") or d.get("ts") or ""
            for tc in d.get("tool_calls") or []:
                if not isinstance(tc, dict):
                    continue
                name = tc.get("name") or ""
                raw_args = tc.get("arguments") or {}
                if isinstance(raw_args, str):
                    try:
                        args = json.loads(raw_args) if raw_args else {}
                    except json.JSONDecodeError:
                        args = {}
                elif isinstance(raw_args, dict):
                    args = raw_args
                else:
                    args = {}

                if name in EDIT_TOOLS:
                    path = args.get("file_path") or args.get("path") or ""
                    if path:
                        changes.append({"file": path, "tool": name, "ts": ts})
                elif name == "run_terminal_command":
                    cmd = args.get("command") or ""
                    if cmd and BASH_MUTATION_RE.search(cmd):
                        bash_hints.append({"cmd": cmd, "ts": ts})
    return changes, bash_hints

def extract_grok_history(start_ms, end_ms, project_filter=None, cwd_filter=None):
    sessions = defaultdict(lambda: {
        "project": "", "messages": [], "tool": "grok", "first_ts_ms": 0,
    })
    index = grok_session_index()

    # prompt_history.jsonl: cwd 폴더 단위 user prompt 인덱스
    if GROK_SESSIONS_DIR.exists():
        for ph in GROK_SESSIONS_DIR.rglob("prompt_history.jsonl"):
            try:
                with open(ph, encoding="utf-8") as f:
                    for line in f:
                        try:
                            d = json.loads(line.strip())
                        except json.JSONDecodeError:
                            continue
                        sid = d.get("session_id") or ""
                        if not sid or sid not in index:
                            continue
                        ts_ms = iso_to_ms(d.get("timestamp"))
                        if not ts_ms or not (start_ms <= ts_ms < end_ms):
                            continue
                        project = index[sid].get("cwd") or ""
                        if project_filter and project_filter not in project:
                            continue
                        if cwd_filter and not path_matches(project, cwd_filter):
                            continue
                        text = (d.get("prompt") or "").strip()
                        if d.get("is_bash"):
                            continue
                        if not sessions[sid]["project"] and project:
                            sessions[sid]["project"] = project
                        if not sessions[sid]["first_ts_ms"]:
                            sessions[sid]["first_ts_ms"] = ts_ms
                        else:
                            sessions[sid]["first_ts_ms"] = min(sessions[sid]["first_ts_ms"], ts_ms)
                        if text:
                            sessions[sid]["messages"].append({
                                "time": ts_to_hm(ts_ms),
                                "text": text[:300],
                            })
            except OSError:
                continue

    # summary 기반 보강: prompt_history가 없거나 비어 있어도 세션이 목록에 남게
    for sid, info in index.items():
        ts_ms = iso_to_ms(info.get("ts") or info.get("updated_at"))
        if not ts_ms or not (start_ms <= ts_ms < end_ms):
            # 이미 prompt_history로 잡힌 세션은 유지
            if sid in sessions:
                continue
            continue
        project = info.get("cwd") or ""
        if project_filter and project_filter not in project:
            continue
        if cwd_filter and not path_matches(project, cwd_filter):
            continue
        if sid in sessions:
            if not sessions[sid]["project"] and project:
                sessions[sid]["project"] = project
            if sessions[sid]["messages"]:
                continue
        entry = sessions[sid]
        entry["project"] = project or entry["project"]
        if not entry["first_ts_ms"]:
            entry["first_ts_ms"] = ts_ms
        if not entry["messages"]:
            first = grok_first_user_message(info.get("path"))
            if not first:
                first = info.get("title") or ""
            if first:
                entry["messages"].append({"time": ts_to_hm(ts_ms), "text": first[:300]})

    return dict(sessions)


# ─── Claude Code session IO ────────────────────────────────────

def grep_grok_session(fpath: Path, keyword: str):
    """Grok chat_history.jsonl에서 keyword 포함 대화·도구 기록 반환."""
    hits = []
    keyword_lower = keyword.lower()

    def add_hit(role, text, ts=""):
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
            entry_type = d.get("type", "")
            ts = d.get("timestamp") or d.get("ts") or ""
            if entry_type == "user":
                if not is_real_grok_user_message(d):
                    continue
                text = extract_user_query_text(grok_content_text(d.get("content")))
                add_hit("user", text, ts)
            elif entry_type == "assistant":
                text = grok_content_text(d.get("content"))
                add_hit("assistant", text, ts)
                for tc in d.get("tool_calls") or []:
                    if not isinstance(tc, dict):
                        continue
                    name = tc.get("name") or ""
                    args = tc.get("arguments") or ""
                    if not isinstance(args, str):
                        args = json.dumps(args, ensure_ascii=False)
                    add_hit("tool", f"[{name}] {args}", ts)
            elif entry_type == "tool_result":
                add_hit("tool", grok_content_text(d.get("content")), ts)
    return hits


session_index = grok_session_index
find_session_file = find_grok_session_file
read_conversation = read_grok_conversation
extract_changed_files = extract_grok_changed_files
extract_history = extract_grok_history
grep_session = grep_grok_session

register_cache_clearer(grok_session_index.cache_clear)


# ─── token usage ───────────────────────────────────────────────

SHORT = "Grok"


def add_token_usage(totals, usage):
    # Grok inputTokens includes cachedReadTokens (like Codex input).
    input_tokens = int(usage.get("input_tokens") or 0)
    cached_read = int(usage.get("cached_read_tokens") or 0)
    cache_create = int(usage.get("cache_creation_tokens") or 0)
    output_tokens = int(usage.get("output_tokens") or 0)
    reasoning_output = int(usage.get("reasoning_tokens") or 0)
    total_tokens = int(usage.get("total_tokens") or (input_tokens + output_tokens))
    totals["input_tokens"] += input_tokens
    totals["cached_read_tokens"] += cached_read
    totals["cache_creation_tokens"] += cache_create
    totals["output_tokens"] += output_tokens
    totals["reasoning_tokens"] += reasoning_output
    totals["total_tokens"] += total_tokens
    pure_tokens = max(0, input_tokens - cached_read) + output_tokens
    totals["effective_tokens"] += pure_tokens + cache_create
    totals["pure_tokens"] += pure_tokens
    totals["cache_tokens"] += cached_read
    totals["calls"] += 1
    if usage.get("cost_usd_ticks") is not None:
        totals["cost_usd_ticks"] += int(usage.get("cost_usd_ticks") or 0)
    if usage.get("cost_usd") is not None:
        # defaultdict(int) truncates floats; store milli-USD cents as int micros.
        # Keep float sum on a parallel key when present as float-capable dict.
        try:
            totals["cost_usd"] = float(totals.get("cost_usd") or 0) + float(usage.get("cost_usd") or 0)
        except (TypeError, ValueError):
            pass


def _read_grok_summary(session_dir: Path) -> dict:
    summary_path = session_dir / "summary.json"
    if not summary_path.exists():
        return {}
    try:
        return json.loads(summary_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def _grok_session_cwd(session_dir: Path, summary: dict | None = None) -> str:
    summary = summary if summary is not None else _read_grok_summary(session_dir)
    info = summary.get("info") or {}
    cwd = info.get("cwd") or ""
    if cwd:
        return cwd
    try:
        return unquote(session_dir.parent.name)
    except Exception:
        return ""


def collect_token_rows(start, end, args):
    from pathlib import Path

    from common import GROK_SESSIONS_DIR, in_range, parse_ts, path_matches

    rows = []
    if not GROK_SESSIONS_DIR.exists():
        return rows

    for updates_path in GROK_SESSIONS_DIR.rglob("updates.jsonl"):
        session_dir = updates_path.parent
        session_id = session_dir.name
        summary = _read_grok_summary(session_dir)
        cwd = _grok_session_cwd(session_dir, summary)
        if getattr(args, "cwd", False) and not path_matches(cwd, str(Path.cwd())):
            continue
        if getattr(args, "project", None) and args.project not in cwd:
            continue
        model = summary.get("current_model_id") or ""

        try:
            fh = updates_path.open(encoding="utf-8")
        except OSError:
            continue
        with fh:
            for line_no, line in enumerate(fh, 1):
                if "turn_completed" not in line or "inputTokens" not in line:
                    continue
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue
                params = entry.get("params") or {}
                update = params.get("update") or {}
                if update.get("sessionUpdate") != "turn_completed":
                    continue
                usage = update.get("usage") or {}
                if not usage:
                    continue
                timestamp = parse_ts(entry.get("timestamp"))
                if timestamp is None:
                    timestamp = parse_ts(summary.get("last_active_at") or summary.get("created_at"))
                if not in_range(timestamp, start, end):
                    continue

                input_tokens = int(usage.get("inputTokens") or 0)
                output_tokens = int(usage.get("outputTokens") or 0)
                cached_read = int(usage.get("cachedReadTokens") or 0)
                cache_create = int(usage.get("cacheCreationTokens") or 0)
                reasoning = int(usage.get("reasoningTokens") or 0)
                total_tokens = int(usage.get("totalTokens") or (input_tokens + output_tokens))
                model_usage = usage.get("modelUsage") or {}
                if isinstance(model_usage, dict) and model_usage:
                    model = next(iter(model_usage.keys()), model) or model

                cost_ticks = usage.get("costUsdTicks")
                cost_usd = None
                if cost_ticks is not None:
                    try:
                        cost_ticks = int(cost_ticks)
                        # 10_000_000_000 ticks = $1 (provider scale)
                        cost_usd = cost_ticks / 10_000_000_000
                    except (TypeError, ValueError):
                        cost_ticks = None

                meta = params.get("_meta") or {}
                event_id = meta.get("eventId") or f"{session_id}:{line_no}"
                rows.append({
                    "tool": TOOL,
                    "timestamp": timestamp.isoformat() if timestamp else None,
                    "session_id": session_id,
                    "cwd": cwd,
                    "path": str(updates_path),
                    "model": model,
                    "subagent": False,
                    "event_id": event_id,
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                    "cached_read_tokens": cached_read,
                    "cache_creation_tokens": cache_create,
                    "reasoning_tokens": reasoning,
                    "total_tokens": total_tokens,
                    "model_calls": int(usage.get("modelCalls") or 0),
                    "cost_usd_ticks": cost_ticks,
                    "cost_usd": cost_usd,
                })

    return rows
