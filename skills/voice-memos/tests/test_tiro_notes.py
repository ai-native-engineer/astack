from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SKILL_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = SKILL_DIR / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import tiro_notes  # noqa: E402


class TiroNotesTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.config = self.root / "tiro.json"
        self.patches = [
            mock.patch.object(tiro_notes, "CONFIG_PATH", self.config),
            mock.patch.dict(os.environ, {}, clear=False),
        ]
        for patch in self.patches:
            patch.start()
        os.environ.pop("TIRO_WORKSPACE", None)

    def tearDown(self):
        for patch in self.patches:
            patch.stop()
        self.temporary.cleanup()

    def test_workspace_from_env(self):
        os.environ["TIRO_WORKSPACE"] = "ws-env"
        self.assertEqual(tiro_notes.resolve_workspace(), "ws-env")

    def test_workspace_from_config(self):
        self.config.write_text('{"workspace": "ws-config"}\n', encoding="utf-8")
        self.assertEqual(tiro_notes.resolve_workspace(), "ws-config")

    def test_workspace_from_single_listing(self):
        listing = [{"guid": "ws-only", "name": "Personal"}]
        with mock.patch.object(tiro_notes, "list_workspaces", return_value=listing):
            self.assertEqual(tiro_notes.resolve_workspace(), "ws-only")
        saved = json.loads(self.config.read_text(encoding="utf-8"))
        self.assertEqual(saved["workspace"], "ws-only")

    def test_multiple_workspaces_require_config(self):
        listing = [
            {"guid": "ws-a", "name": "A"},
            {"guid": "ws-b", "name": "B"},
        ]
        with mock.patch.object(tiro_notes, "list_workspaces", return_value=listing):
            with self.assertRaises(tiro_notes.TiroError) as raised:
                tiro_notes.resolve_workspace()
        self.assertIn("ws-a", str(raised.exception))
        self.assertIn("ws-b", str(raised.exception))

    def test_tiro_argv_uses_agents_env_and_workspace(self):
        argv = tiro_notes.tiro_argv(["notes", "list", "--limit", "3"], workspace="ws-1")
        self.assertEqual(
            argv[:5],
            ["agents-env", "run", "TIRO_TOKEN", "--", "tiro"],
        )
        self.assertIn("--workspace", argv)
        self.assertEqual(argv[argv.index("--workspace") + 1], "ws-1")

    def test_parse_ndjson_skips_warnings(self):
        raw = (
            "⚠ Credential is not bound\n"
            '{"guid":"note-1","title":"hello"}\n'
            '{"_cursor":"abc"}\n'
        )
        notes, cursor = tiro_notes.parse_ndjson(raw)
        self.assertEqual(notes, [{"guid": "note-1", "title": "hello"}])
        self.assertEqual(cursor, "abc")

    def test_date_flags_map_to_since_until(self):
        flags = tiro_notes.date_flags("2026-08-18")
        self.assertEqual(flags["since"], "2026-08-18")
        self.assertEqual(flags["until"], "2026-08-19")


if __name__ == "__main__":
    unittest.main()
