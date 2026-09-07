"""Fixture tests for Cursor, Gemini, and Claude Desktop discovery."""

from __future__ import annotations

import datetime
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from adapters import claude, cursor, gemini
from common import set_include_subagents

KST = datetime.timezone(datetime.timedelta(hours=9))


def ms(year, month, day, hour=0, minute=0):
    return int(
        datetime.datetime(year, month, day, hour, minute, tzinfo=KST).timestamp() * 1000
    )


def write_jsonl(path: Path, entries):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps(entry, ensure_ascii=False) + "\n" for entry in entries),
        encoding="utf-8",
    )


class TestCursorAdapter(unittest.TestCase):
    def setUp(self):
        set_include_subagents(False)
        cursor.cursor_session_index.cache_clear()

    def tearDown(self):
        cursor.cursor_session_index.cache_clear()
        set_include_subagents(False)

    def test_extracts_real_query_and_tool_records(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "projects"
            sid = "11111111-2222-4333-8444-555555555555"
            transcript = (
                root / "Users-test-work" / "agent-transcripts" / sid / f"{sid}.jsonl"
            )
            user_text = (
                "<manually_attached_skills>문서에 `<user_query>` 표기가 있음</manually_attached_skills>\n"
                "<user_info>\nWorkspace Path: /tmp/cursor-work\n</user_info>\n"
                "<timestamp>Tuesday, Aug 18, 2026, 3:31 AM (UTC+9)</timestamp>\n"
                "<user_query>cursor needle 검색</user_query>"
            )
            patch_text = "*** Begin Patch\n*** Update File: /tmp/cursor-work/a.py\n@@\n-old\n+new\n*** End Patch\n"
            write_jsonl(
                transcript,
                [
                    {
                        "role": "user",
                        "message": {"content": [{"type": "text", "text": user_text}]},
                    },
                    {
                        "role": "assistant",
                        "message": {
                            "content": [
                                {"type": "text", "text": "완료했습니다."},
                                {
                                    "type": "tool_use",
                                    "name": "ApplyPatch",
                                    "input": {"patch": patch_text},
                                },
                            ]
                        },
                    },
                ],
            )

            with (
                mock.patch.object(cursor, "CURSOR_PROJECTS_DIR", root),
                mock.patch.object(cursor, "CURSOR_CHATS_DIR", Path(temp) / "chats"),
            ):
                cursor.cursor_session_index.cache_clear()
                history = cursor.extract_cursor_history(
                    ms(2026, 8, 18),
                    ms(2026, 8, 19),
                )
                self.assertEqual(history[sid]["project"], "/tmp/cursor-work")
                self.assertEqual(
                    history[sid]["messages"][0]["text"], "cursor needle 검색"
                )

                messages, found = cursor.read_cursor_conversation(sid, full=True)
                self.assertEqual(found, transcript)
                self.assertEqual(messages[0]["role"], "user")
                self.assertEqual(messages[0]["text"], "cursor needle 검색")
                self.assertTrue(cursor.grep_cursor_session(transcript, "needle"))

                changes, _ = cursor.extract_cursor_changed_files(sid)
                self.assertEqual(changes[0]["file"], "/tmp/cursor-work/a.py")

    def test_subagent_transcripts_are_opt_in(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "projects"
            main_sid = "11111111-2222-4333-8444-555555555555"
            sub_sid = "66666666-7777-4888-8999-000000000000"
            session_root = root / "fixture" / "agent-transcripts" / main_sid
            write_jsonl(session_root / f"{main_sid}.jsonl", [])
            write_jsonl(session_root / "subagents" / f"{sub_sid}.jsonl", [])

            with (
                mock.patch.object(cursor, "CURSOR_PROJECTS_DIR", root),
                mock.patch.object(cursor, "CURSOR_CHATS_DIR", Path(temp) / "chats"),
            ):
                cursor.cursor_session_index.cache_clear()
                self.assertEqual(set(cursor.cursor_session_index()), {main_sid})

                set_include_subagents(True)
                self.assertEqual(
                    set(cursor.cursor_session_index()),
                    {main_sid, sub_sid},
                )


class TestGeminiAdapter(unittest.TestCase):
    def setUp(self):
        set_include_subagents(False)
        gemini.gemini_session_index.cache_clear()
        gemini._antigravity_metadata.cache_clear()

    def tearDown(self):
        gemini.gemini_session_index.cache_clear()
        gemini._antigravity_metadata.cache_clear()
        set_include_subagents(False)

    def test_antigravity_and_gemini_cli_formats(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            brain = base / "brain"
            metadata = base / "conversation_metadata.json"
            gemini_tmp = base / "tmp"

            anti_sid = "aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeeeeeee"
            anti_transcript = (
                brain
                / anti_sid
                / ".system_generated"
                / "logs"
                / "transcript_full.jsonl"
            )
            write_jsonl(
                anti_transcript,
                [
                    {
                        "step_index": 0,
                        "source": "USER_EXPLICIT",
                        "type": "USER_INPUT",
                        "created_at": "2026-08-18T01:00:00Z",
                        "content": "<USER_REQUEST>antigravity needle</USER_REQUEST>",
                    },
                    {
                        "step_index": 1,
                        "source": "MODEL",
                        "type": "PLANNER_RESPONSE",
                        "created_at": "2026-08-18T01:00:01Z",
                        "content": "찾았습니다.",
                    },
                ],
            )
            metadata.write_text(
                json.dumps(
                    {
                        "conversations": {
                            anti_sid: {
                                "summary": {
                                    "WorkspaceURIs": ["file:///tmp/antigravity-work"],
                                    "UpdatedAt": "2026-08-18T01:00:00Z",
                                    "Preview": "antigravity needle",
                                },
                                "is_internal": False,
                            }
                        }
                    }
                ),
                encoding="utf-8",
            )

            cli_sid = "bbbbbbbb-cccc-4ddd-8eee-ffffffffffff"
            cli_transcript = gemini_tmp / "demo" / "chats" / "session-demo.jsonl"
            write_jsonl(
                cli_transcript,
                [
                    {
                        "sessionId": cli_sid,
                        "startTime": "2026-08-18T02:00:00Z",
                        "kind": "main",
                    },
                    {
                        "$set": {
                            "messages": [
                                {
                                    "id": "context",
                                    "timestamp": "2026-08-18T02:00:00Z",
                                    "type": "user",
                                    "content": [
                                        {
                                            "text": (
                                                "<session_context>\n"
                                                "- **Workspace Directories:**\n"
                                                "  - /tmp/gemini-work\n"
                                                "</session_context>"
                                            )
                                        }
                                    ],
                                },
                                {
                                    "id": "user",
                                    "timestamp": "2026-08-18T02:01:00Z",
                                    "type": "user",
                                    "content": [{"text": "gemini needle"}],
                                },
                                {
                                    "id": "model",
                                    "timestamp": "2026-08-18T02:01:01Z",
                                    "type": "gemini",
                                    "content": [{"text": "응답"}],
                                },
                            ]
                        }
                    },
                ],
            )

            with (
                mock.patch.object(gemini, "ANTIGRAVITY_BRAIN_DIR", brain),
                mock.patch.object(
                    gemini, "ANTIGRAVITY_IDE_CONVERSATIONS", brain.parent / "ide"
                ),
                mock.patch.object(gemini, "ANTIGRAVITY_METADATA", metadata),
                mock.patch.object(gemini, "GEMINI_TMP_DIR", gemini_tmp),
            ):
                gemini.gemini_session_index.cache_clear()
                gemini._antigravity_metadata.cache_clear()
                index = gemini.gemini_session_index()
                self.assertEqual(index[anti_sid]["cwd"], "/tmp/antigravity-work")
                self.assertEqual(index[cli_sid]["cwd"], "/tmp/gemini-work")

                history = gemini.extract_gemini_history(
                    ms(2026, 8, 18),
                    ms(2026, 8, 19),
                )
                self.assertEqual(
                    history[anti_sid]["messages"][0]["text"], "antigravity needle"
                )
                self.assertEqual(
                    history[cli_sid]["messages"][0]["text"], "gemini needle"
                )
                self.assertTrue(gemini.grep_gemini_session(anti_transcript, "needle"))
                self.assertTrue(gemini.grep_gemini_session(cli_transcript, "needle"))

    def test_internal_antigravity_sessions_are_opt_in(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            brain = base / "brain"
            metadata = base / "conversation_metadata.json"
            sid = "aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeeeeeee"
            transcript = (
                brain / sid / ".system_generated" / "logs" / "transcript_full.jsonl"
            )
            write_jsonl(
                transcript,
                [
                    {
                        "source": "USER_EXPLICIT",
                        "type": "USER_INPUT",
                        "created_at": "2026-08-18T01:00:00Z",
                        "content": "<USER_REQUEST>internal</USER_REQUEST>",
                    }
                ],
            )
            metadata.write_text(
                json.dumps(
                    {
                        "conversations": {
                            sid: {
                                "summary": {
                                    "UpdatedAt": "2026-08-18T01:00:00Z",
                                },
                                "is_internal": True,
                            }
                        }
                    }
                ),
                encoding="utf-8",
            )

            with (
                mock.patch.object(gemini, "ANTIGRAVITY_BRAIN_DIR", brain),
                mock.patch.object(
                    gemini, "ANTIGRAVITY_IDE_CONVERSATIONS", brain.parent / "ide"
                ),
                mock.patch.object(gemini, "ANTIGRAVITY_METADATA", metadata),
                mock.patch.object(gemini, "GEMINI_TMP_DIR", base / "tmp"),
            ):
                gemini.gemini_session_index.cache_clear()
                gemini._antigravity_metadata.cache_clear()
                self.assertNotIn(sid, gemini.gemini_session_index())

                set_include_subagents(True)
                self.assertIn(sid, gemini.gemini_session_index())


class TestClaudeDesktopDiscovery(unittest.TestCase):
    def setUp(self):
        set_include_subagents(False)
        claude.claude_conversation_index.cache_clear()
        claude.claude_transcript_mtimes.cache_clear()
        claude.claude_desktop_metadata.cache_clear()

    def tearDown(self):
        claude.claude_conversation_index.cache_clear()
        claude.claude_transcript_mtimes.cache_clear()
        claude.claude_desktop_metadata.cache_clear()
        set_include_subagents(False)

    def test_metadata_adds_desktop_session_missing_from_history(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            projects = base / "projects"
            desktop = base / "desktop"
            local = base / "local"
            history_file = base / "missing-history.jsonl"
            sid = "cccccccc-dddd-4eee-8fff-000000000000"
            transcript = projects / "project" / f"{sid}.jsonl"
            write_jsonl(
                transcript,
                [
                    {
                        "type": "user",
                        "timestamp": "2026-08-18T00:00:00Z",
                        "message": {"content": "cowork needle"},
                    }
                ],
            )
            metadata_path = desktop / "account" / "workspace" / "local_fixture.json"
            metadata_path.parent.mkdir(parents=True, exist_ok=True)
            metadata_path.write_text(
                json.dumps(
                    {
                        "sessionId": "local_fixture",
                        "cliSessionId": sid,
                        "originCwd": "/tmp/cowork-project",
                        "createdAt": ms(2026, 8, 18, 9),
                        "title": "Cowork fixture",
                    }
                ),
                encoding="utf-8",
            )

            with (
                mock.patch.object(claude, "CLAUDE_LOCAL_PROJECT_ROOTS", ()),
                mock.patch.object(claude, "CLAUDE_PROJECTS_DIR", projects),
                mock.patch.object(claude, "CLAUDE_HISTORY", history_file),
                mock.patch.object(claude, "CLAUDE_DESKTOP_SESSIONS_DIR", desktop),
                mock.patch.object(claude, "CLAUDE_DESKTOP_LOCAL_SESSIONS_DIR", local),
            ):
                claude.claude_conversation_index.cache_clear()
                claude.claude_desktop_metadata.cache_clear()
                result = claude.extract_claude_history(
                    ms(2026, 8, 18),
                    ms(2026, 8, 19),
                )
                self.assertEqual(result[sid]["project"], "/tmp/cowork-project")
                self.assertEqual(result[sid]["messages"][0]["text"], "cowork needle")

    def test_discovers_isolated_cowork_transcript(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            projects = base / "projects"
            desktop = base / "desktop"
            local = base / "local"
            local_session = local / "account" / "workspace" / "local_fixture"
            sid = "dddddddd-eeee-4fff-8000-111111111111"
            transcript = (
                local_session / ".claude" / "projects" / "fixture" / f"{sid}.jsonl"
            )
            write_jsonl(
                transcript,
                [
                    {
                        "type": "user",
                        "timestamp": "2026-08-18T00:00:00Z",
                        "message": {"content": "isolated cowork needle"},
                    }
                ],
            )
            metadata_path = local_session.with_suffix(".json")
            metadata_path.parent.mkdir(parents=True, exist_ok=True)
            metadata_path.write_text(
                json.dumps(
                    {
                        "sessionId": "local_fixture",
                        "cliSessionId": sid,
                        "userSelectedFolders": ["/tmp/original-project"],
                        "createdAt": ms(2026, 8, 18, 9),
                    }
                ),
                encoding="utf-8",
            )

            with (
                mock.patch.object(claude, "CLAUDE_LOCAL_PROJECT_ROOTS", ()),
                mock.patch.object(claude, "CLAUDE_PROJECTS_DIR", projects),
                mock.patch.object(claude, "CLAUDE_HISTORY", base / "missing.jsonl"),
                mock.patch.object(claude, "CLAUDE_DESKTOP_SESSIONS_DIR", desktop),
                mock.patch.object(claude, "CLAUDE_DESKTOP_LOCAL_SESSIONS_DIR", local),
            ):
                claude.claude_conversation_index.cache_clear()
                claude.claude_desktop_metadata.cache_clear()
                self.assertEqual(
                    claude.claude_conversation_index()[sid],
                    transcript,
                )
                result = claude.extract_claude_history(
                    ms(2026, 8, 18),
                    ms(2026, 8, 19),
                )
                self.assertEqual(result[sid]["project"], "/tmp/original-project")
                self.assertEqual(
                    result[sid]["messages"][0]["text"],
                    "isolated cowork needle",
                )


if __name__ == "__main__":
    unittest.main()
