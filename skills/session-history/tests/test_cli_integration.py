"""End-to-end CLI tests across every supported local session adapter."""

from __future__ import annotations

import datetime
import json
import os
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from urllib.parse import quote

SKILL_ROOT = Path(__file__).resolve().parents[1]
CLI = SKILL_ROOT / "scripts" / "session_history.py"
TOKEN_CLI = SKILL_ROOT / "scripts" / "token_usage.py"
sys.path.insert(0, str(SKILL_ROOT / "scripts"))
from adapters import ORDER as REGISTERED_TOOLS  # noqa: E402

KST = datetime.timezone(datetime.timedelta(hours=9))
DATE = "2026-08-18"


def write_json(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False), encoding="utf-8")


def write_jsonl(path: Path, entries):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps(entry, ensure_ascii=False) + "\n" for entry in entries),
        encoding="utf-8",
    )


class TestSessionHistoryCli(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name)
        self.project = self.home / "work" / "project"
        self.project.mkdir(parents=True)
        self.env = {
            **os.environ,
            "HOME": str(self.home),
            "PYTHONDONTWRITEBYTECODE": "1",
            "NO_COLOR": "1",
        }
        self.ids = {
            "claude": "10000000-0000-4000-8000-000000000001",
            "codex": "20000000-0000-4000-8000-000000000002",
            "grok": "30000000-0000-4000-8000-000000000003",
            "cursor": "40000000-0000-4000-8000-000000000004",
            "gemini": "50000000-0000-4000-8000-000000000005",
            "opencode": "ses_60000000-0000-4000-8000-000000000006",
            "aside": "70000000-0000-4000-8000-000000000007",
            "openclaw": "80000000-0000-4000-8000-000000000008",
            "copilot": "90000000-0000-4000-8000-000000000009",
        }
        self._write_claude_fixture()
        self._write_codex_fixture()
        self._write_grok_fixture()
        self._write_cursor_fixture()
        self._write_gemini_fixture()
        self._write_opencode_fixture()
        self._write_aside_fixture()
        self._write_openclaw_fixture()
        self._write_copilot_fixture()

    def _run(self, *args, cwd=None):
        return subprocess.run(
            ["python3", str(CLI), *args],
            cwd=cwd or self.project,
            env=self.env,
            text=True,
            capture_output=True,
            timeout=20,
            check=False,
        )

    def _run_json(self, *args, cwd=None):
        result = self._run(*args, cwd=cwd)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return json.loads(result.stdout)

    def _run_token_json(self, *args):
        result = subprocess.run(
            ["python3", str(TOKEN_CLI), *args],
            cwd=self.project,
            env=self.env,
            text=True,
            capture_output=True,
            timeout=20,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return json.loads(result.stdout)

    def _write_claude_fixture(self):
        sid = self.ids["claude"]
        ts_ms = int(
            datetime.datetime(2026, 8, 18, 9, 10, tzinfo=KST).timestamp() * 1000
        )
        write_jsonl(
            self.home / ".claude" / "history.jsonl",
            [
                {
                    "display": "claude fixture needle",
                    "timestamp": ts_ms,
                    "sessionId": sid,
                    "project": str(self.project),
                }
            ],
        )
        write_jsonl(
            self.home / ".claude" / "projects" / "fixture" / f"{sid}.jsonl",
            [
                {
                    "type": "user",
                    "timestamp": "2026-08-18T09:10:00+09:00",
                    "message": {"content": "claude fixture needle"},
                },
                {
                    "type": "assistant",
                    "timestamp": "2026-08-18T09:10:01+09:00",
                    "message": {
                        "model": "claude-test",
                        "content": [{"type": "text", "text": "claude response"}],
                    },
                },
            ],
        )

    def _write_codex_fixture(self):
        sid = self.ids["codex"]
        ts_sec = int(datetime.datetime(2026, 8, 18, 9, 20, tzinfo=KST).timestamp())
        write_jsonl(
            self.home / ".codex" / "history.jsonl",
            [{"session_id": sid, "ts": ts_sec, "text": "codex fixture needle"}],
        )
        write_jsonl(
            self.home
            / ".codex"
            / "sessions"
            / "2026"
            / "08"
            / "18"
            / "rollout-fixture.jsonl",
            [
                {
                    "type": "session_meta",
                    "timestamp": "2026-08-18T09:20:00+09:00",
                    "payload": {
                        "id": sid,
                        "cwd": str(self.project),
                        "timestamp": "2026-08-18T09:20:00+09:00",
                        "source": "cli",
                    },
                },
                {
                    "type": "event_msg",
                    "timestamp": "2026-08-18T09:20:00+09:00",
                    "payload": {
                        "type": "user_message",
                        "message": "codex fixture needle",
                    },
                },
                {
                    "type": "event_msg",
                    "timestamp": "2026-08-18T09:20:01+09:00",
                    "payload": {
                        "type": "agent_message",
                        "message": "codex response",
                    },
                },
            ],
        )

    def _write_grok_fixture(self):
        sid = self.ids["grok"]
        project_root = (
            self.home / ".grok" / "sessions" / quote(str(self.project), safe="")
        )
        session_root = project_root / sid
        write_json(
            session_root / "summary.json",
            {
                "info": {"id": sid, "cwd": str(self.project)},
                "created_at": "2026-08-18T09:30:00+09:00",
                "session_summary": "grok fixture needle",
            },
        )
        write_jsonl(
            session_root / "chat_history.jsonl",
            [
                {
                    "type": "user",
                    "timestamp": "2026-08-18T09:30:00+09:00",
                    "content": "<user_query>grok fixture needle</user_query>",
                },
                {
                    "type": "assistant",
                    "timestamp": "2026-08-18T09:30:01+09:00",
                    "content": "grok response",
                },
            ],
        )
        write_jsonl(
            project_root / "prompt_history.jsonl",
            [
                {
                    "session_id": sid,
                    "timestamp": "2026-08-18T09:30:00+09:00",
                    "prompt": "grok fixture needle",
                }
            ],
        )

    def _write_cursor_fixture(self):
        sid = self.ids["cursor"]
        transcript = (
            self.home
            / ".cursor"
            / "projects"
            / "fixture"
            / "agent-transcripts"
            / sid
            / f"{sid}.jsonl"
        )
        patch = (
            "*** Begin Patch\n"
            f"*** Update File: {self.project / 'cursor.txt'}\n"
            "@@\n-old\n+new\n"
            "*** End Patch\n"
        )
        write_jsonl(
            transcript,
            [
                {
                    "role": "user",
                    "message": {
                        "content": [
                            {
                                "type": "text",
                                "text": (
                                    f"<user_info>Workspace Path: {self.project}</user_info>\n"
                                    "<timestamp>Tuesday, Aug 18, 2026, 9:40 AM (UTC+9)</timestamp>\n"
                                    "<user_query>cursor fixture needle</user_query>"
                                ),
                            }
                        ]
                    },
                },
                {
                    "role": "assistant",
                    "message": {
                        "content": [
                            {"type": "text", "text": "cursor response"},
                            {
                                "type": "tool_use",
                                "name": "ApplyPatch",
                                "input": {"patch": patch},
                            },
                        ]
                    },
                },
            ],
        )

    def _write_gemini_fixture(self):
        sid = self.ids["gemini"]
        write_jsonl(
            self.home
            / ".gemini"
            / "antigravity-cli"
            / "brain"
            / sid
            / ".system_generated"
            / "logs"
            / "transcript_full.jsonl",
            [
                {
                    "step_index": 0,
                    "source": "USER_EXPLICIT",
                    "type": "USER_INPUT",
                    "created_at": "2026-08-18T09:50:00+09:00",
                    "content": "<USER_REQUEST>gemini fixture needle</USER_REQUEST>",
                },
                {
                    "step_index": 1,
                    "source": "MODEL",
                    "type": "PLANNER_RESPONSE",
                    "created_at": "2026-08-18T09:50:01+09:00",
                    "content": "gemini response",
                },
            ],
        )
        write_json(
            self.home
            / ".gemini"
            / "antigravity-cli"
            / "cache"
            / "conversation_metadata.json",
            {
                "conversations": {
                    sid: {
                        "summary": {
                            "WorkspaceURIs": [self.project.as_uri()],
                            "UpdatedAt": "2026-08-18T09:50:00+09:00",
                            "Preview": "gemini fixture needle",
                        },
                        "is_internal": False,
                    }
                }
            },
        )

    def _write_opencode_fixture(self):
        sid = self.ids["opencode"]
        ts_ms = int(
            datetime.datetime(2026, 8, 18, 9, 50, tzinfo=KST).timestamp() * 1000
        )
        db_path = self.home / ".local" / "share" / "opencode" / "opencode.db"
        db_path.parent.mkdir(parents=True, exist_ok=True)
        con = sqlite3.connect(db_path)
        with con:
            con.execute(
                "create table session (id text primary key, directory text,"
                " time_created integer, title text, model text, agent text,"
                " parent_id text)"
            )
            con.execute(
                "create table message (id text primary key, session_id text,"
                " time_created integer, data text)"
            )
            con.execute(
                "create table part (id text primary key, message_id text,"
                " session_id text, time_created integer, data text)"
            )
            con.execute(
                "insert into session values (?,?,?,?,?,?,?)",
                (
                    sid,
                    str(self.project),
                    ts_ms,
                    "opencode fixture",
                    json.dumps({"id": "claude-test"}),
                    "build",
                    None,
                ),
            )
            con.execute(
                "insert into message values (?,?,?,?)",
                (
                    "msg_1",
                    sid,
                    ts_ms,
                    json.dumps({"role": "user", "time": {"created": ts_ms}}),
                ),
            )
            con.execute(
                "insert into message values (?,?,?,?)",
                (
                    "msg_2",
                    sid,
                    ts_ms + 1000,
                    json.dumps(
                        {
                            "role": "assistant",
                            "modelID": "claude-test",
                            "path": {"cwd": str(self.project)},
                            "tokens": {
                                "input": 10,
                                "output": 5,
                                "reasoning": 0,
                                "cache": {"read": 2, "write": 3},
                            },
                        }
                    ),
                ),
            )
            con.execute(
                "insert into part values (?,?,?,?,?)",
                (
                    "prt_1",
                    "msg_1",
                    sid,
                    ts_ms,
                    json.dumps({"type": "text", "text": "opencode fixture needle"}),
                ),
            )
            con.execute(
                "insert into part values (?,?,?,?,?)",
                (
                    "prt_2",
                    "msg_2",
                    sid,
                    ts_ms + 1000,
                    json.dumps(
                        {
                            "type": "tool",
                            "tool": "edit",
                            "state": {
                                "status": "completed",
                                "input": {"filePath": str(self.project / "oc.txt")},
                                "time": {"start": ts_ms + 1000},
                            },
                        }
                    ),
                ),
            )
        con.close()

    def _write_aside_fixture(self):
        sid = self.ids["aside"]
        ts_ms = int(
            datetime.datetime(2026, 8, 18, 10, 0, tzinfo=KST).timestamp() * 1000
        )
        profile = self.home / ".aside" / "u" / "1"
        write_jsonl(
            profile / "sessions" / f"2026-08-18_{sid}" / "messages.jsonl",
            [
                {"role": "user", "content": "aside fixture needle", "timestamp": ts_ms},
                {
                    "role": "assistant",
                    "model": "claude-test",
                    "content": [{"type": "text", "text": "aside response"}],
                    "timestamp": ts_ms + 1000,
                },
            ],
        )
        con = sqlite3.connect(profile / "state.db")
        with con:
            con.execute(
                "create table sessions (id text primary key, title text, model text,"
                " cwd text, created_at integer, parent_id text)"
            )
            con.execute(
                "create table session_runs (id integer primary key, session_id text,"
                " token_usage text, started_at integer, files_changed text)"
            )
            con.execute(
                "insert into sessions values (?,?,?,?,?,?)",
                (
                    sid,
                    "aside fixture",
                    json.dumps({"modelId": "claude-test"}),
                    str(self.project),
                    ts_ms // 1000,
                    None,
                ),
            )
            con.execute(
                "insert into session_runs values (?,?,?,?,?)",
                (
                    1,
                    sid,
                    json.dumps(
                        {"input": 10, "output": 5, "cacheRead": 2, "cacheWrite": 3}
                    ),
                    ts_ms // 1000,
                    json.dumps([str(self.project / "aside.txt")]),
                ),
            )
        con.close()

    def _write_openclaw_fixture(self):
        sid = self.ids["openclaw"]
        write_jsonl(
            self.home / ".senpi" / "agent" / "sessions" / "fixture" / f"{sid}.jsonl",
            [
                {
                    "type": "session",
                    "version": 3,
                    "id": sid,
                    "timestamp": "2026-08-18T10:10:00+09:00",
                    "cwd": str(self.project),
                },
                {
                    "type": "message",
                    "timestamp": "2026-08-18T10:10:00+09:00",
                    "message": {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "A new session was started via /new",
                            }
                        ],
                    },
                },
                {
                    "type": "message",
                    "timestamp": "2026-08-18T10:10:05+09:00",
                    "message": {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "openclaw fixture needle"}
                        ],
                    },
                },
                {
                    "type": "message",
                    "timestamp": "2026-08-18T10:10:06+09:00",
                    "message": {
                        "role": "assistant",
                        "model": "claude-test",
                        "content": [
                            {"type": "text", "text": "openclaw response"},
                            {
                                "type": "toolCall",
                                "id": "call_1",
                                "name": "write",
                                "arguments": {
                                    "file_path": str(self.project / "openclaw.txt")
                                },
                            },
                        ],
                        "usage": {
                            "input": 10,
                            "output": 5,
                            "cacheRead": 2,
                            "cacheWrite": 3,
                        },
                    },
                },
            ],
        )

    def _write_copilot_fixture(self):
        sid = self.ids["copilot"]
        root = self.home / ".copilot" / "session-state"
        sdir = root / sid
        sdir.mkdir(parents=True)
        (sdir / "workspace.yaml").write_text(
            f"id: {sid}\n"
            f"cwd: {self.project}\n"
            "client_name: copilot-cli\n"
            "created_at: 2026-08-18T10:20:00.000Z\n",
            encoding="utf-8",
        )
        write_jsonl(
            sdir / "events.jsonl",
            [
                {
                    "type": "user.message",
                    "timestamp": "2026-08-18T10:20:00+09:00",
                    "data": {
                        "content": "<skill-context name='x'>injected</skill-context>"
                    },
                },
                {
                    "type": "user.message",
                    "timestamp": "2026-08-18T10:20:05+09:00",
                    "data": {"content": "copilot fixture needle"},
                },
                {
                    "type": "assistant.message",
                    "timestamp": "2026-08-18T10:20:06+09:00",
                    "data": {"model": "claude-test", "content": "copilot response"},
                },
                {
                    "type": "tool.execution_start",
                    "timestamp": "2026-08-18T10:20:07+09:00",
                    "data": {
                        "toolName": "write",
                        "arguments": {"path": str(self.project / "copilot.txt")},
                    },
                },
                {
                    "type": "session.shutdown",
                    "timestamp": "2026-08-18T10:20:10+09:00",
                    "data": {
                        "modelMetrics": {
                            "claude-test": {
                                "tokenDetails": {
                                    "input": {"tokenCount": 11},
                                    "output": {"tokenCount": 6},
                                    "cache_read": {"tokenCount": 2},
                                    "cache_write": {"tokenCount": 3},
                                }
                            }
                        }
                    },
                },
            ],
        )
        # UUID가 아닌 임시 골격은 세션으로 세지 않아야 한다.
        (root / "optimistic-chat-scaffold").mkdir()

    def test_sources_and_list_cover_all_adapters(self):
        # 새 어댑터를 등록하고 픽스처를 빠뜨리면 여기서 걸린다.
        self.assertEqual(set(self.ids), set(REGISTERED_TOOLS))
        sources = self._run_json("sources", "--format", "json")
        self.assertEqual({source["tool"] for source in sources}, set(REGISTERED_TOOLS))
        self.assertTrue(all(source["available"] for source in sources))
        self.assertTrue(all(source["sessions"] == 1 for source in sources))

        sessions = self._run_json("list", "--date", DATE, "--format", "json")
        self.assertEqual(set(sessions), set(self.ids.values()))
        self.assertEqual(
            {session["tool"] for session in sessions.values()},
            set(self.ids),
        )

    def test_cwd_and_timeline_cover_all_adapters(self):
        sessions = self._run_json(
            "list",
            "--date",
            DATE,
            "--cwd",
            "--format",
            "json",
            cwd=self.project,
        )
        self.assertEqual(set(sessions), set(self.ids.values()))

        timeline = self._run_json("timeline", "--date", DATE, "--format", "json")
        self.assertEqual(len(timeline), len(self.ids))
        self.assertEqual({entry["tool"] for entry in timeline}, set(self.ids))

    def test_rg_and_show_work_for_each_adapter(self):
        for tool, sid in self.ids.items():
            with self.subTest(tool=tool):
                hits = self._run_json(
                    "rg",
                    "fixture needle",
                    "--date",
                    DATE,
                    "--tool",
                    tool,
                    "--format",
                    "json",
                )
                self.assertEqual(len(hits), 1)
                self.assertEqual(hits[0]["sid"], sid)

                messages = self._run_json(
                    "show",
                    sid[:12],
                    "--tool",
                    tool,
                    "--format",
                    "json",
                )
                self.assertEqual(messages[0]["role"], "user")
                self.assertIn("fixture needle", messages[0]["text"])

    def test_edit_tool_calls_reach_show_files(self):
        # 파트 타입 이름이 어긋나면 조용히 빈 결과가 된다. 도구별로 한 건씩 못 박는다.
        expected = {
            "cursor": "cursor.txt",
            "openclaw": "openclaw.txt",
            "copilot": "copilot.txt",
        }
        for tool, filename in expected.items():
            with self.subTest(tool=tool):
                files = self._run_json(
                    "show",
                    self.ids[tool][:12],
                    "--tool",
                    tool,
                    "--files",
                    "--format",
                    "json",
                )
                self.assertEqual(
                    [change["file"] for change in files["changes"]],
                    [str(self.project / filename)],
                )

    def test_cursor_files_and_missing_session_exit(self):
        files = self._run_json(
            "show",
            self.ids["cursor"][:12],
            "--tool",
            "cursor",
            "--files",
            "--format",
            "json",
        )
        self.assertEqual(
            files["changes"][0]["file"],
            str(self.project / "cursor.txt"),
        )

        missing = self._run("show", "does-not-exist")
        self.assertEqual(missing.returncode, 1)
        self.assertIn("찾을 수 없습니다", missing.stdout)

    def test_conversation_only_adapters_report_no_token_rows(self):
        for tool in ("cursor", "gemini"):
            with self.subTest(tool=tool):
                usage = self._run_token_json(
                    "--date",
                    DATE,
                    "--tool",
                    tool,
                    "--format",
                    "json",
                )
                self.assertEqual(usage["rows"], [])
                self.assertEqual(usage["summary"]["total_tokens"], 0)


if __name__ == "__main__":
    unittest.main()
