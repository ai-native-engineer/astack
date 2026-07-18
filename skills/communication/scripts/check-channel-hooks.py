#!/usr/bin/env python3
"""Check that direct communication channel skills reference the shared contract."""

from __future__ import annotations

import sys
from pathlib import Path


SHARED_ROOT = Path(__file__).resolve().parents[2]
REQUIRED = "../communication/references/work-message-contract.md"
CHANNEL_SKILLS = ["agent-slack", "agent-discord", "kakaotalk", "gog", "imessage"]


def main() -> int:
    missing: list[str] = []

    for name in CHANNEL_SKILLS:
        skill_path = SHARED_ROOT / name / "SKILL.md"
        if not skill_path.exists():
            missing.append(f"{name}: SKILL.md not found")
            continue

        text = skill_path.read_text(encoding="utf-8")
        if REQUIRED not in text:
            missing.append(f"{name}: missing {REQUIRED}")
        else:
            print(f"OK {name}")

    if missing:
        for item in missing:
            print(f"MISSING {item}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
