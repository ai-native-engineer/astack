#!/usr/bin/env python3
"""Run a goal Proof command as a bounded Claude/Codex Stop hook."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


# Keep hook feedback small enough to remain useful as a continuation prompt.
MAX_FEEDBACK_CHARS = 4_000


def event_input() -> dict[str, object]:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid hook input JSON: {exc}") from exc
    if not isinstance(payload, dict):
        raise ValueError("hook input must be a JSON object")
    return payload


def feedback(command: str, returncode: int, output: str) -> str:
    detail = output.strip() or "(no output)"
    if len(detail) > MAX_FEEDBACK_CHARS:
        detail = "..." + detail[-MAX_FEEDBACK_CHARS:]
    return (
        f"Goal Proof failed with exit {returncode}. Fix the root cause and rerun it.\n"
        f"Command: {command}\n"
        f"Output:\n{detail}"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--proof-command", required=True, help="Exact Proof command to run")
    args = parser.parse_args(argv)

    try:
        event = event_input()
    except ValueError as exc:
        print(f"goal-plan Stop gate: {exc}", file=sys.stderr)
        return 2

    cwd_value = event.get("cwd")
    cwd = Path(cwd_value) if isinstance(cwd_value, str) and cwd_value else Path.cwd()
    result = subprocess.run(
        args.proof_command,
        cwd=cwd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    if result.returncode == 0:
        print("{}")
        return 0

    # Block one stop attempt. The active /goal loop owns further retries and bounds.
    if event.get("stop_hook_active") is True:
        print("{}")
        return 0

    print(feedback(args.proof_command, result.returncode, result.stdout), file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
