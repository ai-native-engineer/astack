"""Tool adapters for session-history."""

from __future__ import annotations

from common import GJC_SESSIONS_DIR, OPENCLAW_SESSIONS_DIR, SENPI_SESSIONS_DIR

from . import aside, claude, codex, copilot, cursor, gemini, grok, opencode
from .openclaw import SessionJsonlAdapter

ADAPTERS = {
    "claude": claude,
    "codex": codex,
    "grok": grok,
    "cursor": cursor,
    "gemini": gemini,
    "opencode": opencode,
    "aside": aside,
    "openclaw": SessionJsonlAdapter(
        "openclaw", "OpenClaw", "[W]", OPENCLAW_SESSIONS_DIR
    ),
    "senpi": SessionJsonlAdapter("senpi", "senpi", "[S]", SENPI_SESSIONS_DIR),
    "gjc": SessionJsonlAdapter("gjc", "gjc", "[J]", GJC_SESSIONS_DIR),
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
    "senpi",
    "gjc",
    "copilot",
)


def get_adapter(tool: str):
    return ADAPTERS[tool]


def iter_adapters(tool_filter: str = "all"):
    for name in ORDER:
        if tool_filter in ("all", name):
            yield ADAPTERS[name]
