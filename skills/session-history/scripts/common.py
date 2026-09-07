"""Shared helpers for session-history scripts."""

from __future__ import annotations

import datetime
import datetime as dt
import re
from pathlib import Path

HOME = Path.home()
CLAUDE_HISTORY = HOME / ".claude" / "history.jsonl"
CLAUDE_SESSIONS_DIR = HOME / ".claude" / "sessions"
CLAUDE_PROJECTS_DIR = HOME / ".claude" / "projects"
CLAUDE_DESKTOP_SESSIONS_DIR = (
    HOME / "Library" / "Application Support" / "Claude" / "claude-code-sessions"
)
CLAUDE_DESKTOP_LOCAL_SESSIONS_DIR = (
    HOME / "Library" / "Application Support" / "Claude" / "local-agent-mode-sessions"
)
CLAUDE_OPENCODE_TRANSCRIPTS_DIR = HOME / ".claude" / "transcripts"
# CLAUDE_CONFIG_DIR을 옮겨 실행한 세션은 같은 스키마로 여기에 쌓인다.
CLAUDE_LOCAL_PROJECT_ROOTS = (
    HOME / ".cache" / "claude-local" / "config" / "projects",
    HOME / ".cache" / "claude-local" / "cfg" / "projects",
)
CODEX_HISTORY = HOME / ".codex" / "history.jsonl"
CODEX_SESSIONS_DIR = HOME / ".codex" / "sessions"
CODEX_ARCHIVED_SESSIONS_DIR = HOME / ".codex" / "archived_sessions"
GROK_SESSIONS_DIR = HOME / ".grok" / "sessions"
CURSOR_PROJECTS_DIR = HOME / ".cursor" / "projects"
CURSOR_CHATS_DIR = HOME / ".cursor" / "chats"
GEMINI_DIR = HOME / ".gemini"
GEMINI_TMP_DIR = GEMINI_DIR / "tmp"
GEMINI_ANTIGRAVITY_DIR = GEMINI_DIR / "antigravity-cli"
GEMINI_ANTIGRAVITY_IDE_DIR = GEMINI_DIR / "antigravity"
COPILOT_SESSION_STATE_DIR = HOME / ".copilot" / "session-state"
VSCODE_WORKSPACE_STORAGE_DIR = (
    HOME / "Library" / "Application Support" / "Code" / "User" / "workspaceStorage"
)
OPENCODE_DB = HOME / ".local" / "share" / "opencode" / "opencode.db"
ASIDE_PROFILES_DIR = HOME / ".aside" / "u"
# openclaw 계보를 공유하는 도구들. 세션 JSONL 스키마가 같아 한 어댑터가 읽는다.
OPENCLAW_ROOTS = (
    (HOME / ".openclaw" / "agents" / "main" / "sessions", "openclaw"),
    (HOME / ".senpi" / "agent" / "sessions", "senpi"),
    (HOME / ".gjc" / "agent" / "sessions", "gjc"),
)

BASH_MUTATION_RE = re.compile(
    r"(?:(?:^|[;&|\s])(?:rm|mv|cp|mkdir|rmdir|touch|ln|chmod|chown|sed\s+-i|tee|apply_patch)\b)|(?:\s>>?\s*[^\s;&|])",
)

LOCAL_TZ = dt.datetime.now().astimezone().tzinfo or dt.timezone.utc

_INCLUDE_SUBAGENTS = False
_CACHE_CLEARERS: list = []


def register_cache_clearer(fn) -> None:
    if fn not in _CACHE_CLEARERS:
        _CACHE_CLEARERS.append(fn)


def include_subagents() -> bool:
    return _INCLUDE_SUBAGENTS


def set_include_subagents(value: bool) -> None:
    global _INCLUDE_SUBAGENTS
    if _INCLUDE_SUBAGENTS == bool(value):
        return
    _INCLUDE_SUBAGENTS = bool(value)
    refresh_indexes()


def refresh_indexes() -> None:
    for clearer in _CACHE_CLEARERS:
        clearer()


def shorten_home(path: str) -> str:
    home = str(HOME)
    return path.replace(home, "~") if path else "(unknown)"


def ts_to_hm(ts_ms: int) -> str:
    return datetime.datetime.fromtimestamp(ts_ms / 1000, tz=LOCAL_TZ).strftime("%H:%M")


def ts_to_hms(ts_ms: int) -> str:
    return datetime.datetime.fromtimestamp(ts_ms / 1000, tz=LOCAL_TZ).strftime(
        "%H:%M:%S"
    )


def date_range(args):
    """session_history용: (start_ms, end_ms, label)."""
    if args.date:
        target = datetime.datetime.strptime(args.date, "%Y-%m-%d").replace(
            tzinfo=LOCAL_TZ
        )
        start = target
        end = target + datetime.timedelta(days=1)
        label = args.date
    else:
        now = datetime.datetime.now(tz=LOCAL_TZ)
        start = now.replace(
            hour=0, minute=0, second=0, microsecond=0
        ) - datetime.timedelta(days=args.days - 1)
        end = now + datetime.timedelta(days=1)
        label = (
            start.strftime("%Y-%m-%d")
            if args.days == 1
            else f"{start.strftime('%Y-%m-%d')} ~ {now.strftime('%Y-%m-%d')}"
        )
    return int(start.timestamp() * 1000), int(end.timestamp() * 1000), label


def date_range_dt(args):
    """token_usage용: (start_dt|None, end_dt|None, label). --all-time / --month 지원."""
    if getattr(args, "all_time", False):
        return None, None, "전체 기간"

    month = getattr(args, "month", None)
    if month:
        now = dt.datetime.now(tz=LOCAL_TZ)
        if month in (True, "current", ""):
            year, mon = now.year, now.month
        else:
            try:
                year_s, mon_s = str(month).split("-", 1)
                year, mon = int(year_s), int(mon_s)
                if not (1 <= mon <= 12):
                    raise ValueError("month out of range")
            except ValueError as exc:
                raise SystemExit(f"--month must be YYYY-MM (got {month!r})") from exc
        start = dt.datetime(year, mon, 1, tzinfo=LOCAL_TZ)
        if mon == 12:
            end = dt.datetime(year + 1, 1, 1, tzinfo=LOCAL_TZ)
        else:
            end = dt.datetime(year, mon + 1, 1, tzinfo=LOCAL_TZ)
        # For current month, cap end at now so "recent" is accurate
        if end > now and year == now.year and mon == now.month:
            end = now
        label = f"{year:04d}-{mon:02d}"
        return start, end, label

    if args.date:
        start = dt.datetime.strptime(args.date, "%Y-%m-%d").replace(tzinfo=LOCAL_TZ)
        end = start + dt.timedelta(days=1)
        label = args.date
    else:
        now = dt.datetime.now(tz=LOCAL_TZ)
        today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        start = today - dt.timedelta(days=args.days - 1)
        end = now
        label = (
            start.strftime("%Y-%m-%d")
            if args.days == 1
            else f"{start:%Y-%m-%d} ~ {now:%Y-%m-%d}"
        )
    return start, end, label


def parse_ts(value):
    """ISO/epoch → aware datetime (LOCAL_TZ)."""
    if value is None:
        return None
    try:
        if isinstance(value, (int, float)):
            seconds = value / 1000 if value > 10**12 else value
            return dt.datetime.fromtimestamp(seconds, tz=LOCAL_TZ)
        if isinstance(value, str):
            if value.endswith("Z"):
                parsed = dt.datetime.fromisoformat(value[:-1] + "+00:00")
            else:
                parsed = dt.datetime.fromisoformat(value)
            if parsed.tzinfo is None:
                parsed = parsed.replace(tzinfo=LOCAL_TZ)
            return parsed.astimezone(LOCAL_TZ)
    except (OSError, ValueError, TypeError):
        return None
    return None


def in_range(timestamp, start, end) -> bool:
    if timestamp is None:
        return False
    if start is None and end is None:
        return True
    return start <= timestamp < end


def path_matches(project: str, filter_path: str) -> bool:
    """cwd 기준 프로젝트 매칭.

    - project가 cwd 하위 경로 -> 매칭 (서브프로젝트)
    - cwd가 project 하위 경로 -> 매칭 (하위 폴더에서 작업 중)
      단, project가 홈 디렉토리와 동일하면 제외 (너무 광범위)
    """
    if not project or not filter_path:
        return False
    try:
        project_path = Path(project).expanduser()
        filter_path_obj = Path(filter_path).expanduser()
        if not project_path.is_absolute() or not filter_path_obj.is_absolute():
            return False
        project_path = project_path.resolve(strict=False)
        filter_path_obj = filter_path_obj.resolve(strict=False)
        home_path = HOME.resolve(strict=False)
    except (OSError, RuntimeError):
        return False
    if project_path == home_path:
        return False
    return (
        project_path == filter_path_obj
        or project_path in filter_path_obj.parents
        or filter_path_obj in project_path.parents
    )


def iso_to_ms(value) -> int:
    if not value:
        return 0
    try:
        if isinstance(value, (int, float)):
            return int(value if value > 10**12 else value * 1000)
        s = str(value)
        if s.endswith("Z"):
            s = s[:-1] + "+00:00"
        d = datetime.datetime.fromisoformat(s)
        if d.tzinfo is None:
            d = d.replace(tzinfo=datetime.timezone.utc)
        return int(d.timestamp() * 1000)
    except (ValueError, OSError, TypeError):
        return 0
