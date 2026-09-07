"""Tool adapters for session-history."""

from __future__ import annotations

from . import aside, claude, codex, copilot, cursor, gemini, grok, openclaw, opencode

ADAPTERS = {
    "claude": claude,
    "codex": codex,
    "grok": grok,
    "cursor": cursor,
    "gemini": gemini,
    "opencode": opencode,
    "aside": aside,
    "openclaw": openclaw,
    "copilot": copilot,
}

ORDER = (
    "claude",
    "codex",
    "grok",
    "cursor",
    "gemini",
    "opencode",
    "aside",
    "openclaw",
    "copilot",
)


def get_adapter(tool: str):
    return ADAPTERS[tool]


def iter_adapters(tool_filter: str = "all"):
    for name in ORDER:
        if tool_filter in ("all", name):
            yield ADAPTERS[name]
