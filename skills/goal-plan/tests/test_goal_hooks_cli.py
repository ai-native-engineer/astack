#!/usr/bin/env python3
"""Runnable checks for the goal_hooks.py CLI: add to both runtimes, dedupe, list, fire, remove, refusals."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
HOOKS = SKILL_ROOT / "scripts" / "goal_hooks.py"


def run(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, "-I", str(HOOKS), "--root", str(root), *args], capture_output=True, text=True)


def read(root: Path, rel: str) -> dict:
    return json.loads((root / rel).read_text(encoding="utf-8"))


class GoalHooksTests(unittest.TestCase):
    def test_add_lands_in_both_runtimes_once(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".claude").mkdir()
            (root / ".claude" / "settings.json").write_text(json.dumps({"permissions": {"allow": ["Bash(ls:*)"]}}), encoding="utf-8")
            first = run(root, "add", "--event", "PostToolUse", "--matcher", "Edit|Write", "--command", "echo lint")
            self.assertEqual(first.returncode, 0, first.stderr)
            gid = first.stdout.strip().splitlines()[-1]
            self.assertEqual(len(gid), 8)
            for rel in (".claude/settings.json", ".codex/hooks.json"):
                data = read(root, rel)
                self.assertEqual(data["hooks"]["PostToolUse"], [{"hooks": [{"type": "command", "command": "echo lint"}], "matcher": "Edit|Write"}])
            self.assertEqual(read(root, ".claude/settings.json")["permissions"], {"allow": ["Bash(ls:*)"]})

            again = run(root, "add", "--event", "PostToolUse", "--matcher", "Edit|Write", "--command", "echo lint")
            self.assertEqual(again.returncode, 0)
            self.assertIn("kept", again.stdout)
            self.assertEqual(len(read(root, ".codex/hooks.json")["hooks"]["PostToolUse"]), 1)

            listed = run(root, "list")
            self.assertIn(gid, listed.stdout)
            self.assertIn(".claude+.codex", listed.stdout)

            removed = run(root, "remove", gid)
            self.assertEqual(removed.returncode, 0, removed.stderr)
            self.assertNotIn("hooks", read(root, ".codex/hooks.json"))
            self.assertEqual(read(root, ".claude/settings.json"), {"permissions": {"allow": ["Bash(ls:*)"]}})
            self.assertEqual(run(root, "remove", gid).returncode, 2)

    def test_fire_runs_matching_hooks_with_sample_payload(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            capture = root / "seen.json"
            run(root, "add", "--event", "PostToolUse", "--matcher", "Edit|Write", "--command", f"cat > {capture}")
            run(root, "add", "--event", "PostToolUse", "--matcher", "Bash", "--command", "exit 1")
            fired = run(root, "fire", "--trust-workspace", "PostToolUse", "--tool", "Edit", "--file", "src/x.ts")
            self.assertEqual(fired.returncode, 0, fired.stdout + fired.stderr)
            self.assertIn("fired 1 hook(s)", fired.stdout)
            payload = json.loads(capture.read_text(encoding="utf-8"))
            self.assertEqual(payload["hook_event_name"], "PostToolUse")
            self.assertEqual(payload["tool_name"], "Edit")
            self.assertTrue(payload["tool_input"]["file_path"].endswith("src/x.ts"))

            broken = run(root, "fire", "--trust-workspace", "PostToolUse", "--tool", "Bash")
            self.assertEqual(broken.returncode, 1)
            self.assertIn("FAIL", broken.stdout)

            none = run(root, "fire", "--trust-workspace", "Stop")
            self.assertEqual(none.returncode, 2)
            self.assertIn("no Stop hook", none.stderr)

    def test_fire_without_trust_lists_commands_and_runs_nothing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            marker = root / "ran"
            run(root, "add", "--event", "Stop", "--command", f"touch {marker}")
            dry = run(root, "fire", "Stop")
            self.assertEqual(dry.returncode, 2, dry.stdout + dry.stderr)
            self.assertIn(f"touch {marker}", dry.stdout)
            self.assertIn("--trust-workspace", dry.stderr)
            self.assertFalse(marker.exists())
            self.assertEqual(run(root, "fire", "--trust-workspace", "Stop").returncode, 0)
            self.assertTrue(marker.exists())

    def test_listing_escapes_control_characters(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".claude").mkdir()
            sneaky = "echo safe\x1b[2K\rrm -rf /"
            (root / ".claude" / "settings.json").write_text(json.dumps(
                {"hooks": {"Stop": [{"hooks": [{"type": "command", "command": sneaky}]}]}}), encoding="utf-8")
            data = json.loads((root / ".claude" / "settings.json").read_text(encoding="utf-8"))
            data["hooks"]["Weird\x1b[31m"] = data["hooks"]["Stop"]
            (root / ".claude" / "settings.json").write_text(json.dumps(data), encoding="utf-8")
            for result in (run(root, "list"), run(root, "fire", "Stop")):
                self.assertNotIn("\x1b", result.stdout)
                self.assertNotIn("\r", result.stdout.replace("\r\n", "\n"))
                self.assertIn("\\x1b[2K\\rrm -rf /", result.stdout)

    def test_fire_expect_block_distinguishes_deliberate_exit_2(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            run(root, "add", "--event", "PreToolUse", "--matcher", "Edit", "--command", "grep -q '\\.env' && echo blocked >&2 && exit 2 || exit 0")
            blocked = run(root, "fire", "--trust-workspace", "PreToolUse", "--tool", "Edit", "--file", ".env", "--expect-block")
            self.assertEqual(blocked.returncode, 0, blocked.stdout + blocked.stderr)
            allowed = run(root, "fire", "--trust-workspace", "PreToolUse", "--tool", "Edit", "--file", "src/ok.ts")
            self.assertEqual(allowed.returncode, 0, allowed.stdout + allowed.stderr)
            wrong = run(root, "fire", "--trust-workspace", "PreToolUse", "--tool", "Edit", "--file", "src/ok.ts", "--expect-block")
            self.assertEqual(wrong.returncode, 1)

    def test_refuses_symlinked_runtime_dir_and_bad_event(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            outside = root / "outside"
            outside.mkdir()
            (root / ".codex").symlink_to(outside)
            result = run(root, "add", "--event", "Stop", "--command", "echo hi")
            self.assertEqual(result.returncode, 2)
            self.assertIn("symlink", result.stderr)
            self.assertFalse((root / ".claude" / "settings.json").exists())
            self.assertEqual(list(outside.iterdir()), [])
            (root / ".codex").unlink()
            bad = run(root, "add", "--event", "OnSave", "--command", "echo hi")
            self.assertEqual(bad.returncode, 2)
            self.assertIn("unknown event", bad.stderr)
            matcher = run(root, "add", "--event", "Stop", "--matcher", "Edit", "--command", "echo hi")
            self.assertEqual(matcher.returncode, 2)

    def test_keeps_foreign_groups_untouched(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".codex").mkdir()
            foreign = {"hooks": {"Stop": [{"hooks": [{"type": "command", "command": "python3 stop_gate.py"}]}]}}
            (root / ".codex" / "hooks.json").write_text(json.dumps(foreign), encoding="utf-8")
            added = run(root, "add", "--event", "Stop", "--command", "echo extra")
            gid = added.stdout.strip().splitlines()[-1]
            data = read(root, ".codex/hooks.json")
            self.assertEqual(len(data["hooks"]["Stop"]), 2)
            self.assertEqual(data["hooks"]["Stop"][0], foreign["hooks"]["Stop"][0])
            run(root, "remove", gid)
            self.assertEqual(read(root, ".codex/hooks.json"), foreign)
            listed = run(root, "list")
            self.assertIn("one runtime only", listed.stdout)


if __name__ == "__main__":
    unittest.main()
