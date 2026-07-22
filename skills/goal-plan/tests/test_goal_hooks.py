#!/usr/bin/env python3
"""Runnable checks for goal-plan Stop-hook integration."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parent.parent
INIT = SKILL_ROOT / "scripts" / "init_goal_plan.py"
STOP_GATE = SKILL_ROOT / "scripts" / "stop_gate.py"


class GoalHookTests(unittest.TestCase):
    def test_scaffold_writes_both_runtime_hooks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "goal"
            proof = "python3 -c 'print(\"proof ok\")'"
            result = subprocess.run(
                [sys.executable, str(INIT), str(target), "--goal", "ship it", "--proof-command", proof],
                capture_output=True,
                text=True,
                check=True,
            )

            agents = (target / "AGENTS.md").read_text(encoding="utf-8")
            claude = json.loads((target / ".claude" / "settings.json").read_text(encoding="utf-8"))
            codex = json.loads((target / ".codex" / "hooks.json").read_text(encoding="utf-8"))

            self.assertIn(proof, agents)
            self.assertIn("wrote Stop hook", result.stdout)
            for config in (claude, codex):
                command = config["hooks"]["Stop"][0]["hooks"][0]["command"]
                self.assertIn(str(STOP_GATE), command)
                self.assertIn("--proof-command", command)

    def test_stop_gate_blocks_once_then_allows_stop(self) -> None:
        failing = f"{sys.executable} -c 'raise SystemExit(7)'"

        first = subprocess.run(
            [sys.executable, str(STOP_GATE), "--proof-command", failing],
            input=json.dumps({"cwd": str(SKILL_ROOT), "stop_hook_active": False}),
            capture_output=True,
            text=True,
        )
        self.assertEqual(first.returncode, 2)
        self.assertIn("exit 7", first.stderr)

        retry = subprocess.run(
            [sys.executable, str(STOP_GATE), "--proof-command", failing],
            input=json.dumps({"cwd": str(SKILL_ROOT), "stop_hook_active": True}),
            capture_output=True,
            text=True,
        )
        self.assertEqual(retry.returncode, 0)
        self.assertEqual(json.loads(retry.stdout), {})

    def test_stop_gate_allows_passing_proof(self) -> None:
        passing = f"{sys.executable} -c 'print(\"ok\")'"
        result = subprocess.run(
            [sys.executable, str(STOP_GATE), "--proof-command", passing],
            input=json.dumps({"cwd": str(SKILL_ROOT), "stop_hook_active": False}),
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout), {})

    def test_scaffold_replaces_its_hook_and_preserves_existing_hooks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "goal"
            hooks_path = target / ".codex" / "hooks.json"
            hooks_path.parent.mkdir(parents=True)
            hooks_path.write_text(
                json.dumps({"hooks": {"Stop": [{"hooks": [{"type": "command", "command": "echo keep"}]}]}}),
                encoding="utf-8",
            )

            for proof in ("printf first", "printf second"):
                subprocess.run(
                    [sys.executable, str(INIT), str(target), "--goal", "ship it", "--proof-command", proof],
                    capture_output=True,
                    text=True,
                    check=True,
                )

            config = json.loads(hooks_path.read_text(encoding="utf-8"))
            commands = [handler["command"] for group in config["hooks"]["Stop"] for handler in group["hooks"]]
            self.assertIn("echo keep", commands)
            self.assertEqual(sum(str(STOP_GATE) in command for command in commands), 1)
            self.assertIn("printf second", next(command for command in commands if str(STOP_GATE) in command))
            self.assertNotIn("printf first", next(command for command in commands if str(STOP_GATE) in command))

    def test_invalid_existing_hook_config_fails_before_scaffold_writes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "goal"
            hooks_path = target / ".codex" / "hooks.json"
            hooks_path.parent.mkdir(parents=True)
            hooks_path.write_text("{", encoding="utf-8")

            result = subprocess.run(
                [sys.executable, str(INIT), str(target), "--goal", "ship it", "--proof-command", "true"],
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 2)
            self.assertIn("invalid hook config JSON", result.stderr)
            self.assertFalse((target / "AGENTS.md").exists())


if __name__ == "__main__":
    unittest.main()
