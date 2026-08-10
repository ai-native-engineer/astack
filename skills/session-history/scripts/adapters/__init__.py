"""Tool adapters for session-history (claude / codex / grok)."""

from __future__ import annotations

from . import claude, codex, grok

ADAPTERS = {
    "claude": claude,
    "codex": codex,
    "grok": grok,
}

ORDER = ("claude", "codex", "grok")


def get_adapter(tool: str):
    return ADAPTERS[tool]


def iter_adapters(tool_filter: str = "all"):
    for name in ORDER:
        if tool_filter in ("all", name):
            yield ADAPTERS[name]
