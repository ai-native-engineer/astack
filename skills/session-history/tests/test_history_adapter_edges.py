"""Edge-case tests for the established Claude, Codex, and Grok adapters."""

from __future__ import annotations

import json
import os
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock
from urllib.parse import quote

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from adapters import claude, codex, grok
from common import iso_to_ms, set_include_subagents


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

    def test_state_metadata_backfill_batches_large_indexes(self):
        with tempfile.TemporaryDirectory() as temp:
            db_path = Path(temp) / "state.sqlite"
            rows = [(f"sid-{i}", f"session-{i}", "openai") for i in range(1005)]
            db = sqlite3.connect(db_path)
            try:
                db.execute(
                    "create table threads (id text primary key, name text, model_provider text)"
                )
                db.executemany("insert into threads values (?, ?, ?)", rows)
                db.commit()
            finally:
                db.close()

            index = {sid: {"name": "", "provider": ""} for sid, _, _ in rows}
            with mock.patch.object(codex, "CODEX_STATE_DB", db_path):
                codex._backfill_state_metadata(index)

            self.assertEqual(
                index["sid-1004"],
                {"name": "session-1004", "provider": "openai"},
            )


class TestClaudeContextBoundaries(unittest.TestCase):
    def setUp(self):
        set_include_subagents(False)
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name)
        self.projects = self.home / ".claude" / "projects"
        self.history = self.home / ".claude" / "history.jsonl"
        self.desktop = self.home / "desktop"
        self.sid = "10000000-0000-4000-8000-000000000090"
        self.transcript = self.projects / "fixture" / f"{self.sid}.jsonl"
        self.summary = "compact-context-needle: generated prior context"
        self.notification = (
            "<task-notification>notification-only-needle "
            + "x" * 900
            + " notification-tail-needle</task-notification>"
        )
        write_jsonl(
            self.transcript,
            [
                self._user(self.summary, isCompactSummary=True),
                self._user(
                    [{"type": "text", "text": "meta compact context"}],
                    isCompactSummary=True,
                    isMeta=True,
                ),
                self._user(self.notification),
                self._user(
                    "<system-reminder><task-notification>wrapped-notice</task-notification>"
                    "</system-reminder>",
                    isMeta=True,
                ),
                self._user(
                    [
                        {"type": "text", "text": "actual request\n" + self.notification},
                        {"type": "tool_result", "content": "ordinary tool result"},
                    ]
                ),
            ],
        )
        timestamp = iso_to_ms("2026-08-18T09:10:00+09:00") / 1000
        os.utime(self.transcript, (timestamp, timestamp))
        for name, value in {
            "CLAUDE_PROJECTS_DIR": self.projects,
            "CLAUDE_LOCAL_PROJECT_ROOTS": (),
            "CLAUDE_HISTORY": self.history,
            "CLAUDE_DESKTOP_SESSIONS_DIR": self.desktop,
            "CLAUDE_DESKTOP_LOCAL_SESSIONS_DIR": self.home / "local",
        }.items():
            patcher = mock.patch.object(claude, name, value)
            patcher.start()
            self.addCleanup(patcher.stop)
        self._clear()
        self.addCleanup(self._clear)
        self.addCleanup(set_include_subagents, False)

    @staticmethod
    def _clear():
        claude.claude_conversation_index.cache_clear()
        claude.claude_transcript_mtimes.cache_clear()
        claude.claude_desktop_metadata.cache_clear()

    @staticmethod
    def _user(content, **flags):
        return {
            "type": "user",
            "timestamp": "2026-08-18T09:10:00+09:00",
            "cwd": "/tmp/context-fixture",
            "message": {"content": content},
            **flags,
        }

    def _history(self):
        return claude.extract_claude_history(
            iso_to_ms("2026-08-18T00:00:00+09:00"),
            iso_to_ms("2026-08-19T00:00:00+09:00"),
        )

    def _run(self, *args):
        env = {
            key: value
            for key, value in os.environ.items()
            if key not in {
                "CLAUDE_CODE_SESSION_ID", "CODEX_THREAD_ID", "UNSUPPORTED_SESSION_ID"
            }
        }
        env.update({
            "HOME": str(self.home),
            "PYTHONDONTWRITEBYTECODE": "1",
            "TZ": "Asia/Seoul",
        })
        result = subprocess.run(
            [sys.executable, str(SCRIPTS / "session_history.py"), *args, "--tool", "claude"],
            cwd=self.home,
            env=env,
            text=True,
            capture_output=True,
            timeout=20,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return result.stdout

    def test_compact_context_has_its_own_role_and_notifications_are_full_only(self):
        messages, found = claude.read_claude_conversation(self.sid)
        self.assertEqual(found, self.transcript)
        self.assertEqual([m["role"] for m in messages], ["summary", "summary", "user"])
        self.assertEqual(messages[0]["text"], self.summary)
        self.assertEqual(messages[-1]["text"], "actual request")

        full, _ = claude.read_claude_conversation(self.sid, full=True)
        notifications = [m for m in full if m.get("phase") == "task-notification"]
        self.assertEqual(len(notifications), 3)
        self.assertTrue(all(m["role"] == "tool_result" for m in notifications))
        self.assertEqual(notifications[0]["text"], self.notification)
        self.assertIn("ordinary tool result", [m["text"] for m in full])
        self.assertEqual(
            [m["text"] for m in full if m["role"] == "user"], ["actual request"]
        )

    def test_summary_is_searchable_context_but_notification_is_not_a_search_hit(self):
        hits = claude.grep_claude_session(self.transcript, "compact-context-needle")
        self.assertEqual([hit["role"] for hit in hits], ["summary"])
        for keyword in ("notification-only-needle", "notification-tail-needle", "wrapped-notice"):
            self.assertEqual(claude.grep_claude_session(self.transcript, keyword), [])
        self.assertEqual(
            [hit["role"] for hit in claude.grep_claude_session(self.transcript, "ordinary tool")],
            ["tool_result"],
        )

    def test_preview_uses_real_intent_for_transcript_desktop_and_history(self):
        self.assertEqual(self._history()[self.sid]["messages"][0]["text"], "actual request")
        write_json(
            self.desktop / "account" / "local_fixture.json",
            {
                "cliSessionId": self.sid,
                "createdAt": iso_to_ms("2026-08-18T09:10:00+09:00"),
                "originCwd": "/tmp/context-fixture",
            },
        )
        self._clear()
        self.assertEqual(self._history()[self.sid]["messages"][0]["text"], "actual request")
        records = []
        for display, flags in (
            (self.summary, {"isCompactSummary": True}),
            ("meta context", {"isMeta": True}),
            (self.notification, {}),
            (self.notification + "\nactual history request", {}),
        ):
            records.append({
                "sessionId": self.sid,
                "timestamp": iso_to_ms("2026-08-18T09:10:00+09:00"),
                "project": "/tmp/context-fixture",
                "display": display,
                **flags,
            })
        write_jsonl(self.history, records)
        self.assertEqual(
            [m["text"] for m in self._history()[self.sid]["messages"]],
            ["actual history request"],
        )

    def test_context_only_transcript_has_no_user_preview(self):
        write_jsonl(
            self.transcript,
            [self._user(self.summary + self.notification, isCompactSummary=True)],
        )
        timestamp = iso_to_ms("2026-08-18T09:10:00+09:00") / 1000
        os.utime(self.transcript, (timestamp, timestamp))
        self.assertEqual(self._history()[self.sid]["messages"], [])
        messages, _ = claude.read_claude_conversation(self.sid)
        self.assertEqual([m["role"] for m in messages], ["summary"])
        self.assertEqual(messages[0]["text"], self.summary)
        self.assertEqual(claude.grep_claude_session(self.transcript, "notification-only-needle"), [])

    def test_notification_blocks_preserve_surrounding_intent_and_truncated_tail(self):
        for text, expected in (
            (self.notification + "\nreal question", "real question"),
            ("before" + self.notification + "after", "beforeafter"),
            ("real question\n<task-notification>unfinished", "real question"),
            ("real question\n<task-notification source='worker'>notice</task-notification>", "real question"),
        ):
            with self.subTest(text=text[:30]):
                self.assertEqual(claude._real_user_text(text), expected)
        self.assertEqual(claude._claude_real_user_text(self._user(self.summary)), self.summary)

    def test_cli_role_search_and_bounded_full_output(self):
        normal = json.loads(self._run("show", self.sid, "--format", "json"))
        self.assertEqual([m["role"] for m in normal], ["summary", "summary", "user"])
        full = json.loads(self._run("show", self.sid, "--full", "--format", "json"))
        notification = next(m for m in full if m.get("phase") == "task-notification")
        self.assertEqual(notification["role"], "tool_result")
        self.assertEqual(notification["chars"], len(self.notification))
        self.assertLessEqual(len(notification["text"]), 506)
        text = self._run("show", self.sid, "--full")
        self.assertIn("task-notification", text)
        self.assertNotIn("x" * 301, text)
        hits = json.loads(self._run("rg", "compact-context-needle", "--date", "2026-08-18", "--format", "json"))
        self.assertEqual(hits[0]["talk_count"], 0)
        self.assertEqual(hits[0]["hits"][0]["role"], "summary")
        for command in (
            ("rg", "notification-only-needle", "--include-self"),
            ("list", "--search", "compact-context-needle"),
            ("list", "--search", "notification-only-needle"),
        ):
            result = json.loads(self._run(*command, "--date", "2026-08-18", "--format", "json"))
            self.assertFalse(result)


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
