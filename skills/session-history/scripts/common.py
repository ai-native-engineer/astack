"""Shared helpers for session-history scripts."""

from __future__ import annotations

import datetime
import datetime as dt
import json
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
OPENCLAW_SESSIONS_DIR = HOME / ".openclaw" / "agents" / "main" / "sessions"
SENPI_SESSIONS_DIR = HOME / ".senpi" / "agent" / "sessions"
GJC_SESSIONS_DIR = HOME / ".gjc" / "agent" / "sessions"

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
    """session_history용: (start_ms, end_ms, label). --date > --since > --days 순."""
    since = getattr(args, "since", None)
    if args.date:
        target = datetime.datetime.strptime(args.date, "%Y-%m-%d").replace(
            tzinfo=LOCAL_TZ
        )
        start = target
        end = target + datetime.timedelta(days=1)
        label = args.date
    elif since:
        start = datetime.datetime.strptime(since, "%Y-%m-%d").replace(tzinfo=LOCAL_TZ)
        now = datetime.datetime.now(tz=LOCAL_TZ)
        end = now + datetime.timedelta(days=1)
        label = f"{since} ~ {now.strftime('%Y-%m-%d')}"
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


def local_time(value, fmt: str = "%m-%d %H:%M") -> str:
    """ISO(UTC 포함)·epoch 시각을 로컬 시각 문자열로. 해석 못 하면 빈 문자열."""
    parsed = parse_ts(value) if value else None
    return parsed.strftime(fmt) if parsed else ""


# ─── 검색 매칭 ─────────────────────────────────────────────────

# 이 스크립트를 부른 도구 호출과 그 출력은 검색 대상이 아니라 검색의 메아리다.
# 같은 주제를 다시 찾을 때 지난 검색 세션이 상위를 차지하지 않도록 거른다.
ECHO_MARKER = "session_history.py"
TOOL_ROLES = frozenset({"tool", "tool_call", "tool_result"})
EXCERPT_BEFORE = 60
EXCERPT_AFTER = 90


class Matcher:
    """여러 키워드를 OR로 묶는다. 기본은 대소문자 무시 고정 문자열, regex=True면 정규식."""

    def __init__(self, terms, regex: bool = False, skip_echo: bool = True):
        if isinstance(terms, str):
            terms = [terms]
        self.terms = [term for term in terms if term]
        self.regex = regex
        self.skip_echo = skip_echo
        self._patterns = [
            (term, re.compile(term if regex else re.escape(term), re.IGNORECASE))
            for term in self.terms
        ]

    def first(self, text: str):
        """가장 앞에서 걸린 (term, start, end). 없으면 None."""
        best = None
        for term, pattern in self._patterns:
            found = pattern.search(text)
            if found and (best is None or found.start() < best[1]):
                best = (term, found.start(), found.end())
        return best

    def raw_forms(self):
        """로그 원문(JSON 한 겹)에서 찾을 고정 문자열들. 사전 필터를 쓸 수 없으면 None.

        정규식은 원문과 해석이 달라(앵커, 이스케이프) 거르면 결과가 빠질 수 있다.
        따옴표·역슬래시·제어문자는 JSON 인코딩에서 모양이 바뀌어 같은 이유로 뺀다.
        """
        if self.regex or not self.terms:
            return None
        forms = []
        for term in self.terms:
            if any(ch in term for ch in '"\\') or any(ord(ch) < 32 for ch in term):
                return None
            for variant in (term, term.lower(), term.upper()):
                # 비ASCII를 \uXXXX로 쓰는 기록기도 있어 두 모양을 함께 넘긴다
                for form in (variant, json.dumps(variant)[1:-1]):
                    if form not in forms:
                        forms.append(form)
        return forms


def as_matcher(value) -> Matcher:
    return value if isinstance(value, Matcher) else Matcher(value)


def make_excerpt(text: str, start: int, end: int) -> str:
    lo = max(0, start - EXCERPT_BEFORE)
    hi = min(len(text), end + EXCERPT_AFTER)
    return (
        ("..." if lo > 0 else "") + text[lo:hi] + ("..." if hi < len(text) else "")
    ).replace("\n", " ")


def hits_from_messages(messages, matcher) -> list[dict]:
    """어댑터가 뽑은 메시지 목록에서 검색 hit를 만든다. 모든 어댑터의 공통 매칭 지점이다.

    메시지에 `call_id`가 있으면 메아리 호출의 출력까지 짝지어 거른다.
    """
    matcher = as_matcher(matcher)
    echo_calls: set = set()
    hits = []
    for message in messages or []:
        text = message.get("text") or ""
        if not isinstance(text, str) or not text:
            continue
        role = message.get("role") or ""
        call_id = message.get("call_id")
        if matcher.skip_echo and role in TOOL_ROLES:
            if call_id and call_id in echo_calls:
                continue
            if ECHO_MARKER in text:
                if call_id:
                    echo_calls.add(call_id)
                continue
        found = matcher.first(text)
        if not found:
            continue
        term, start, end = found
        hits.append(
            {
                "role": role,
                "ts": message.get("ts") or "",
                "term": term,
                "excerpt": make_excerpt(text, start, end),
            }
        )
    return hits


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
