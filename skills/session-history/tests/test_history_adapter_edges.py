"""Edge-case tests for the established Claude, Codex, and Grok adapters."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock
from urllib.parse import quote

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from adapters import claude, codex, grok
from common import set_include_subagents


def write_json(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")


def write_jsonl(path: Path, entries):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps(entry, ensure_ascii=False) + "\n" for entry in entries),
        encoding="utf-8",
    )


class TestGrokFiltering(unittest.TestCase):
    def setUp(self):
        set_include_subagents(False)
        grok.grok_session_index.cache_clear()

    def tearDown(self):
        grok.grok_session_index.cache_clear()
        set_include_subagents(False)

    def test_prefers_last_explicit_query_and_skips_synthetic_user(self):
        wrapped = (
            "문서에 `<user_query>`라는 표기가 있다.\n"
            "<user_query>real grok needle</user_query>"
        )
        self.assertEqual(grok.extract_user_query_text(wrapped), "real grok needle")
        self.assertFalse(
            grok.is_real_grok_user_message(
                {
                    "type": "user",
                    "synthetic_reason": "runtime",
                    "content": "<user_query>synthetic</user_query>",
                }
            )
        )

        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            project = "/tmp/grok-project"
            sid = "30000000-0000-4000-8000-000000000003"
            project_root = root / quote(project, safe="")
            session_root = project_root / sid
            write_json(
                session_root / "summary.json",
                {
                    "info": {"id": sid, "cwd": project},
                    "created_at": "2026-08-18T09:30:00+09:00",
                },
            )
            write_jsonl(
                session_root / "chat_history.jsonl",
                [
                    {
                        "type": "user",
                        "timestamp": "2026-08-18T09:30:00+09:00",
                        "content": wrapped,
                    },
                    {
                        "type": "user",
                        "synthetic_reason": "runtime",
                        "timestamp": "2026-08-18T09:30:01+09:00",
                        "content": "<user_query>synthetic</user_query>",
                    },
                ],
            )

            with mock.patch.object(grok, "GROK_SESSIONS_DIR", root):
                grok.grok_session_index.cache_clear()
                messages, _ = grok.read_grok_conversation(sid)
                self.assertEqual(len(messages), 1)
                self.assertEqual(messages[0]["text"], "real grok needle")


class TestCodexSubagentFiltering(unittest.TestCase):
    def setUp(self):
        set_include_subagents(False)
        codex.codex_session_index.cache_clear()

    def tearDown(self):
        codex.codex_session_index.cache_clear()
        set_include_subagents(False)

    def test_exec_sessions_are_opt_in(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            main_sid = "20000000-0000-4000-8000-000000000002"
            exec_sid = "20000000-0000-4000-8000-000000000003"
            write_jsonl(
                root / "rollout-main.jsonl",
                [
                    {
                        "type": "session_meta",
                        "payload": {
                            "id": main_sid,
                            "cwd": "/tmp/project",
                            "source": "cli",
                        },
                    }
                ],
            )
            write_jsonl(
                root / "rollout-exec.jsonl",
                [
                    {
                        "type": "session_meta",
                        "payload": {
                            "id": exec_sid,
                            "cwd": "/tmp/project",
                            "source": "exec",
                        },
                    }
                ],
            )

            with (
                mock.patch.object(codex, "CODEX_SESSIONS_DIR", root),
                mock.patch.object(
                    codex, "CODEX_ARCHIVED_SESSIONS_DIR", root / "archived"
                ),
            ):
                codex.codex_session_index.cache_clear()
                self.assertEqual(set(codex.codex_session_index()), {main_sid})

                set_include_subagents(True)
                self.assertEqual(
                    set(codex.codex_session_index()),
                    {main_sid, exec_sid},
                )


class TestClaudeChangedFiles(unittest.TestCase):
    def setUp(self):
        set_include_subagents(False)
        claude.claude_conversation_index.cache_clear()

    def tearDown(self):
        claude.claude_conversation_index.cache_clear()
        set_include_subagents(False)

    def test_collects_structured_edits_and_shell_hints(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            projects = base / "projects"
            sid = "10000000-0000-4000-8000-000000000001"
            transcript = projects / "fixture" / f"{sid}.jsonl"
            write_jsonl(
                transcript,
                [
                    {
                        "type": "assistant",
                        "timestamp": "2026-08-18T09:10:00+09:00",
                        "message": {
                            "content": [
                                {
                                    "type": "tool_use",
                                    "name": "Edit",
                                    "input": {"file_path": "/tmp/project/a.py"},
                                },
                                {
                                    "type": "tool_use",
                                    "name": "Bash",
                                    "input": {"command": "touch /tmp/project/b.py"},
                                },
                            ]
                        },
                    }
                ],
            )

            with (
                mock.patch.object(claude, "CLAUDE_LOCAL_PROJECT_ROOTS", ()),
                mock.patch.object(claude, "CLAUDE_PROJECTS_DIR", projects),
                mock.patch.object(
                    claude,
                    "CLAUDE_DESKTOP_LOCAL_SESSIONS_DIR",
                    base / "local",
                ),
            ):
                claude.claude_conversation_index.cache_clear()
                changes, hints = claude.extract_claude_changed_files(sid)
                self.assertEqual(changes[0]["file"], "/tmp/project/a.py")
                self.assertEqual(hints[0]["cmd"], "touch /tmp/project/b.py")


if __name__ == "__main__":
    unittest.main()
