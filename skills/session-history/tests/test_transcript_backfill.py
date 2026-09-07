"""Regression tests for session discovery that does not depend on history.jsonl."""

from __future__ import annotations

import contextlib
import datetime
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from adapters import claude, codex, gemini
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


def set_mtime(path: Path, ts_ms: int):
    seconds = ts_ms / 1000
    os.utime(path, (seconds, seconds))


class TestClaudeTranscriptBackfill(unittest.TestCase):
    """history.jsonl에 없는 세션도 transcript만으로 list에 나와야 한다."""

    def setUp(self):
        set_include_subagents(False)
        self._clear()

    def tearDown(self):
        self._clear()
        set_include_subagents(False)

    @staticmethod
    def _clear():
        claude.claude_transcript_mtimes.cache_clear()
        claude.claude_conversation_index.cache_clear()
        claude.claude_desktop_metadata.cache_clear()

    @staticmethod
    @contextlib.contextmanager
    def _patched(base: Path, history: Path):
        """어댑터가 실제 홈 디렉토리를 읽지 않도록 소스 경로를 전부 격리한다."""
        with (
            mock.patch.object(claude, "CLAUDE_PROJECTS_DIR", base / "projects"),
            mock.patch.object(claude, "CLAUDE_LOCAL_PROJECT_ROOTS", ()),
            mock.patch.object(claude, "CLAUDE_HISTORY", history),
            mock.patch.object(claude, "CLAUDE_DESKTOP_SESSIONS_DIR", base / "desktop"),
            mock.patch.object(
                claude, "CLAUDE_DESKTOP_LOCAL_SESSIONS_DIR", base / "local"
            ),
        ):
            yield

    def test_session_missing_from_history_is_recovered(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            sid = "aaaaaaaa-0000-4000-8000-000000000001"
            transcript = base / "projects" / "proj" / f"{sid}.jsonl"
            write_jsonl(
                transcript,
                [
                    {"type": "last-prompt", "sessionId": sid},
                    {
                        "type": "user",
                        "timestamp": "2026-08-18T01:00:00Z",
                        "cwd": "/tmp/backfill-project",
                        "message": {"content": "transcript needle"},
                    },
                ],
            )
            set_mtime(transcript, ms(2026, 8, 18, 10))

            with self._patched(base, base / "no-history.jsonl"):
                self._clear()
                result = claude.extract_claude_history(ms(2026, 8, 18), ms(2026, 8, 19))
                self.assertIn(sid, result)
                self.assertEqual(result[sid]["project"], "/tmp/backfill-project")
                self.assertEqual(
                    result[sid]["messages"][0]["text"], "transcript needle"
                )

    def test_transcript_outside_range_is_not_listed(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            sid = "aaaaaaaa-0000-4000-8000-000000000002"
            transcript = base / "projects" / "proj" / f"{sid}.jsonl"
            write_jsonl(
                transcript,
                [
                    {
                        "type": "user",
                        "timestamp": "2026-08-10T01:00:00Z",
                        "cwd": "/tmp/old-project",
                        "message": {"content": "old needle"},
                    }
                ],
            )
            set_mtime(transcript, ms(2026, 8, 10, 10))

            with self._patched(base, base / "no-history.jsonl"):
                self._clear()
                result = claude.extract_claude_history(ms(2026, 8, 18), ms(2026, 8, 19))
                self.assertNotIn(sid, result)

    def test_history_lines_without_session_id_make_no_phantom_session(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            history = base / "history.jsonl"
            write_jsonl(
                history,
                [
                    {
                        "display": "프로젝트 A 프롬프트",
                        "timestamp": ms(2026, 8, 18, 9),
                        "project": "/tmp/a",
                    },
                    {
                        "display": "프로젝트 B 프롬프트",
                        "timestamp": ms(2026, 8, 18, 10),
                        "project": "/tmp/b",
                    },
                ],
            )
            (base / "projects").mkdir(parents=True, exist_ok=True)

            with self._patched(base, history):
                self._clear()
                result = claude.extract_claude_history(ms(2026, 8, 18), ms(2026, 8, 19))
                self.assertEqual(result, {})

    def test_subagent_transcripts_are_opt_in(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            main_sid = "aaaaaaaa-0000-4000-8000-000000000003"
            sub_sid = "aaaaaaaa-0000-4000-8000-000000000004"
            session_dir = base / "projects" / "proj"
            write_jsonl(session_dir / f"{main_sid}.jsonl", [])
            write_jsonl(session_dir / "subagents" / f"{sub_sid}.jsonl", [])

            with self._patched(base, base / "no-history.jsonl"):
                self._clear()
                self.assertEqual(set(claude.claude_conversation_index()), {main_sid})

                set_include_subagents(True)
                self.assertEqual(
                    set(claude.claude_conversation_index()), {main_sid, sub_sid}
                )


class TestClaudeUserTextFilter(unittest.TestCase):
    """주입 컨텍스트가 사용자 발화로 새지 않아야 한다."""

    def test_slash_command_keeps_name_and_args(self):
        raw = (
            "<command-message>session-history</command-message>\n"
            "<command-name>/session-history</command-name>\n"
            "<command-args>커버리지 진단</command-args>"
        )
        self.assertEqual(claude._real_user_text(raw), "/session-history 커버리지 진단")

    def test_system_reminder_is_stripped(self):
        raw = "<system-reminder>무시할 것</system-reminder>\n실제 질문"
        self.assertEqual(claude._real_user_text(raw), "실제 질문")

    def test_local_command_output_is_not_user_text(self):
        self.assertEqual(
            claude._real_user_text("<local-command-stdout>결과</local-command-stdout>"),
            "",
        )

    def test_tool_result_blocks_are_not_user_text(self):
        entry = {
            "type": "user",
            "message": {
                "content": [
                    {"type": "tool_result", "content": "도구 출력"},
                    {"type": "text", "text": "사용자 질문"},
                ]
            },
        }
        self.assertEqual(claude._claude_user_entry_text(entry), "사용자 질문")


class TestGeminiSessionWithoutUserTurn(unittest.TestCase):
    """주입 컨텍스트만 있는 세션도 색인 수와 list 수가 어긋나면 안 된다."""

    def setUp(self):
        set_include_subagents(False)
        gemini.gemini_session_index.cache_clear()
        gemini._antigravity_metadata.cache_clear()

    def tearDown(self):
        gemini.gemini_session_index.cache_clear()
        gemini._antigravity_metadata.cache_clear()
        set_include_subagents(False)

    def test_context_only_session_is_still_listed(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            sid = "cccccccc-0000-4000-8000-000000000001"
            transcript = base / "tmp" / "demo" / "chats" / "session-demo.jsonl"
            write_jsonl(
                transcript,
                [
                    {
                        "sessionId": sid,
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
                                }
                            ]
                        }
                    },
                ],
            )

            with (
                mock.patch.object(gemini, "ANTIGRAVITY_BRAIN_DIR", base / "brain"),
                mock.patch.object(
                    gemini, "ANTIGRAVITY_IDE_CONVERSATIONS", base / "ide"
                ),
                mock.patch.object(
                    gemini, "ANTIGRAVITY_METADATA", base / "missing.json"
                ),
                mock.patch.object(gemini, "GEMINI_TMP_DIR", base / "tmp"),
            ):
                gemini.gemini_session_index.cache_clear()
                gemini._antigravity_metadata.cache_clear()
                index = gemini.gemini_session_index()
                history = gemini.extract_gemini_history(
                    ms(2026, 8, 18), ms(2026, 8, 19)
                )
                self.assertEqual(set(index), set(history))
                self.assertEqual(history[sid]["project"], "/tmp/gemini-work")
                self.assertEqual(history[sid]["messages"], [])


class TestCodexArchivedSessions(unittest.TestCase):
    """archived_sessions도 활성 세션과 같은 rollout 포맷이므로 함께 색인한다."""

    def setUp(self):
        set_include_subagents(False)
        codex.codex_session_index.cache_clear()

    def tearDown(self):
        codex.codex_session_index.cache_clear()
        set_include_subagents(False)

    def test_archived_rollouts_are_indexed(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            active_sid = "bbbbbbbb-0000-4000-8000-000000000001"
            archived_sid = "bbbbbbbb-0000-4000-8000-000000000002"
            write_jsonl(
                base / "sessions" / "rollout-active.jsonl",
                [
                    {
                        "type": "session_meta",
                        "payload": {
                            "id": active_sid,
                            "cwd": "/tmp/project",
                            "source": "cli",
                            "timestamp": "2026-08-18T01:00:00Z",
                        },
                    }
                ],
            )
            write_jsonl(
                base / "archived" / "rollout-archived.jsonl",
                [
                    {
                        "type": "session_meta",
                        "payload": {
                            "id": archived_sid,
                            "cwd": "/tmp/project",
                            "source": "cli",
                            "timestamp": "2026-08-18T02:00:00Z",
                        },
                    }
                ],
            )

            with (
                mock.patch.object(codex, "CODEX_SESSIONS_DIR", base / "sessions"),
                mock.patch.object(
                    codex, "CODEX_ARCHIVED_SESSIONS_DIR", base / "archived"
                ),
                mock.patch.object(codex, "CODEX_HISTORY", base / "no-history.jsonl"),
            ):
                codex.codex_session_index.cache_clear()
                self.assertEqual(
                    set(codex.codex_session_index()), {active_sid, archived_sid}
                )

                history = codex.extract_codex_history(ms(2026, 8, 18), ms(2026, 8, 19))
                self.assertIn(archived_sid, history)


if __name__ == "__main__":
    unittest.main()
