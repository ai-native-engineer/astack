"""rg와 show가 같은 기준으로 찾고 보여 주는지 실제 Claude 로그 형식으로 확인한다."""

from __future__ import annotations

import datetime
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
CLI = SKILL_ROOT / "scripts" / "session_history.py"
sys.path.insert(0, str(SKILL_ROOT / "scripts"))
import session_history as history  # noqa: E402
from common import Matcher, date_range, hits_from_messages  # noqa: E402

DATE = "2026-08-18"
OLD_SID = "c1000000-0000-4000-8000-000000000001"
NEW_SID = "c2000000-0000-4000-8000-000000000002"
# 도구 출력 앞쪽 500자 밖에 키워드를 둬서 읽을 때 잘라 버리면 못 찾게 한다
LONG_OUTPUT = "x" * 800 + " speedbump " + "y" * 50


def write_jsonl(path: Path, entries):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps(entry, ensure_ascii=False) + "\n" for entry in entries),
        encoding="utf-8",
    )


def local(iso: str, fmt: str) -> str:
    return (
        datetime.datetime.fromisoformat(iso.replace("Z", "+00:00"))
        .astimezone()
        .strftime(fmt)
    )


class TestSearchAndShow(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name)
        self.project = self.home / "work" / "project"
        self.project.mkdir(parents=True)
        self.env = {
            key: value
            for key, value in os.environ.items()
            if key not in history.CURRENT_SESSION_ENV
        }
        self.env.update({"HOME": str(self.home), "PYTHONDONTWRITEBYTECODE": "1"})
        projects = self.home / ".claude" / "projects" / "fixture"
        write_jsonl(
            self.home / ".claude" / "history.jsonl",
            [
                {
                    "display": "old",
                    "timestamp": self._ms("2026-08-18T00:00:00Z"),
                    "sessionId": OLD_SID,
                    "project": str(self.project),
                },
                {
                    "display": "new",
                    "timestamp": self._ms("2026-08-18T03:00:00Z"),
                    "sessionId": NEW_SID,
                    "project": str(self.project),
                },
            ],
        )
        write_jsonl(
            projects / f"{OLD_SID}.jsonl",
            [
                {
                    "type": "user",
                    "timestamp": "2026-08-18T00:00:00Z",
                    "message": {
                        "content": "<system-reminder>이의신청 주입 문맥</system-reminder>계정 정지 이야기"
                    },
                },
                {
                    "type": "assistant",
                    "timestamp": "2026-08-18T00:00:05Z",
                    "message": {
                        "model": "claude-test",
                        "content": [
                            {
                                "type": "tool_use",
                                "id": "toolu_1",
                                "name": "Bash",
                                "input": {"command": "echo speedbump"},
                            }
                        ],
                    },
                },
                {
                    "type": "user",
                    "timestamp": "2026-08-18T00:00:06Z",
                    "message": {
                        "content": [
                            {
                                "type": "tool_result",
                                "tool_use_id": "toolu_1",
                                "content": [{"type": "text", "text": LONG_OUTPUT}],
                            }
                        ]
                    },
                },
                {
                    "type": "assistant",
                    "timestamp": "2026-08-18T00:01:00Z",
                    "message": {
                        "content": [
                            {
                                "type": "tool_use",
                                "id": "toolu_2",
                                "name": "Bash",
                                "input": {
                                    "command": "python3 session_history.py rg 이의신청"
                                },
                            }
                        ]
                    },
                },
                {
                    "type": "user",
                    "timestamp": "2026-08-18T00:01:02Z",
                    "message": {
                        "content": [
                            {
                                "type": "tool_result",
                                "tool_use_id": "toolu_2",
                                "content": "지난 검색이 찾은 이의신청 발췌",
                            }
                        ]
                    },
                },
            ],
        )
        write_jsonl(
            projects / f"{NEW_SID}.jsonl",
            [
                {
                    "type": "user",
                    "timestamp": "2026-08-18T03:00:00Z",
                    "message": {"content": "이의신청 제출"},
                },
                {
                    "type": "assistant",
                    "timestamp": "2026-08-18T03:00:01Z",
                    "message": {
                        "content": [{"type": "text", "text": "거절 답변 확인"}]
                    },
                },
            ],
        )

    @staticmethod
    def _ms(iso: str) -> int:
        return int(
            datetime.datetime.fromisoformat(iso.replace("Z", "+00:00")).timestamp()
            * 1000
        )

    def _run(self, *args):
        return subprocess.run(
            [sys.executable, str(CLI), *args],
            cwd=self.project,
            env=self.env,
            text=True,
            capture_output=True,
            timeout=20,
            check=False,
        )

    def _json(self, *args):
        result = self._run(*args, "--format", "json")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return json.loads(result.stdout)

    def test_show_full_includes_claude_tool_input_and_result(self):
        messages = self._json("show", OLD_SID, "--full")
        calls = [m for m in messages if m["role"] == "tool_call"]
        results = [m for m in messages if m["role"] == "tool_result"]
        self.assertIn('"command": "echo speedbump"', calls[0]["text"])
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["chars"], len(LONG_OUTPUT))
        self.assertNotIn("call_id", results[0])

    def test_show_prints_local_time(self):
        text = self._run("show", OLD_SID).stdout
        self.assertIn(local("2026-08-18T00:00:00Z", "%m-%d %H:%M:%S"), text)

    def test_rg_skips_injected_context_and_search_echo(self):
        hits = self._json("rg", "이의신청", "--date", DATE)
        self.assertEqual([row["sid"] for row in hits], [NEW_SID])
        self.assertEqual(
            hits[0]["start"], local("2026-08-18T03:00:00Z", "%Y-%m-%d %H:%M")
        )

        with_echo = self._json("rg", "이의신청", "--date", DATE, "--include-self")
        echo = next(row for row in with_echo if row["sid"] == OLD_SID)
        # 주입 문맥은 --include-self여도 사용자 발화가 아니다
        self.assertEqual(echo["hit_count"], 2)
        self.assertEqual(
            {hit["role"] for hit in echo["hits"]}, {"tool_call", "tool_result"}
        )

    def test_rg_finds_keyword_past_first_500_chars_of_tool_output(self):
        hits = self._json("rg", "speedbump", "--date", DATE)
        self.assertEqual([row["sid"] for row in hits], [OLD_SID])
        self.assertEqual(hits[0]["hit_count"], 2)

    def test_rg_multiple_keywords_are_or_and_sort_by_talk_hits(self):
        hits = self._json(
            "rg", "speedbump", "이의신청", "--date", DATE, "--sort", "relevance"
        )
        # OLD는 hit 2건이 모두 도구 기록이고 NEW는 사용자 발화 1건이다. 대화 hit가 먼저다
        self.assertEqual([row["sid"] for row in hits], [NEW_SID, OLD_SID])
        self.assertEqual(
            [(row["hit_count"], row["talk_count"]) for row in hits], [(1, 1), (2, 0)]
        )
        self.assertEqual(hits[0]["terms"], {"이의신청": 1})
        self.assertEqual(hits[1]["terms"], {"speedbump": 2})

    def test_rg_regex_and_literal_pipe_note(self):
        literal = self._run("rg", "speedbump|이의신청", "--date", DATE)
        self.assertIn("글자 그대로", literal.stdout)
        self.assertIn("매칭 없음", literal.stdout)
        regex = self._json("rg", "-E", "speedbump|이의신청", "--date", DATE)
        self.assertEqual({row["sid"] for row in regex}, {OLD_SID, NEW_SID})
        bad = self._run("rg", "-E", "(", "--date", DATE)
        self.assertEqual(bad.returncode, 2)
        self.assertIn("정규식 오류", bad.stderr)

    def test_since_and_date_validation(self):
        self.assertEqual(len(self._json("rg", "이의신청", "--since", "2026-08-01")), 1)
        bad = self._run("rg", "이의신청", "--since", "2026-13-01")
        self.assertEqual(bad.returncode, 2)
        self.assertIn("YYYY-MM-DD", bad.stderr)

    def test_show_grep_returns_match_window_with_tool_records(self):
        rows = self._json("show", OLD_SID, "--grep", "speedbump", "--context", "0")
        self.assertEqual([row["index"] for row in rows], [1, 2])
        self.assertTrue(all(row["match"] for row in rows))
        self.assertIn("speedbump", rows[1]["text"])

        text = self._run(
            "show", OLD_SID, "--grep", "speedbump", "--context", "0"
        ).stdout
        self.assertIn("#1 🔧 TOOL CALL", text)
        self.assertIn("speedbump", text.split("#2 ")[1])
        self.assertIn("#번호는 --full 기준", text)
        self.assertIn(f"show {OLD_SID[:12]} --full --offset 1 --limit 20", text)
        # 세션 하나를 고른 뒤에는 지난 검색 명령도 맥락이라 메아리를 거르지 않는다
        gap = self._run(
            "show", OLD_SID, "--grep", "정지", "이의신청", "--context", "0"
        ).stdout
        self.assertIn("#1~#2 생략", gap)
        self.assertIn("#4 🔧 TOOL OUTPUT", gap)

    def test_show_offset_and_limit_page_through(self):
        rows = self._json("show", OLD_SID, "--full", "--offset", "1", "--limit", "2")
        self.assertEqual([row["index"] for row in rows], [1, 2])
        text = self._run(
            "show", OLD_SID, "--full", "--offset", "1", "--limit", "2"
        ).stdout
        self.assertIn(f"show {OLD_SID[:12]} --full --offset 3 --limit 2", text)
        talk_only = self._run("show", OLD_SID, "--limit", "1").stdout
        self.assertIn("#번호는 대화 기준", talk_only)
        self.assertNotIn("이어 보기", talk_only)


class TestMatcherAndPrefilter(unittest.TestCase):
    def test_hits_skip_echo_calls_and_their_results(self):
        messages = [
            {
                "role": "tool_call",
                "text": "python3 session_history.py rg needle",
                "call_id": "a",
            },
            {"role": "tool_result", "text": "needle from old search", "call_id": "a"},
            {"role": "tool_result", "text": "needle real output", "call_id": "b"},
            {"role": "user", "text": "needle in session_history.py question"},
        ]
        hits = hits_from_messages(messages, Matcher("needle"))
        self.assertEqual(
            [hit["excerpt"] for hit in hits],
            ["needle real output", "needle in session_history.py question"],
        )
        self.assertEqual(
            len(hits_from_messages(messages, Matcher("needle", skip_echo=False))), 4
        )

    def test_raw_forms_cover_escaped_unicode_and_refuse_unsafe_terms(self):
        forms = Matcher(["이의"]).raw_forms()
        self.assertIn("이의", forms)
        self.assertIn("\\uc774\\uc758", forms)
        self.assertIsNone(Matcher(["a.*b"], regex=True).raw_forms())
        self.assertIsNone(Matcher(['say "hi"']).raw_forms())

    @unittest.skipUnless(shutil.which("rg"), "ripgrep not installed")
    def test_prefilter_keeps_raw_and_escaped_matches_only(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            raw = base / "raw.jsonl"
            escaped = base / "escaped.jsonl"
            other = base / "other.jsonl"
            raw.write_text(
                json.dumps({"text": "이의신청"}, ensure_ascii=False), encoding="utf-8"
            )
            escaped.write_text(json.dumps({"text": "이의신청"}), encoding="utf-8")
            other.write_text(json.dumps({"text": "nothing"}), encoding="utf-8")
            found = history.prefilter_paths(
                [str(raw), str(escaped), str(other)], Matcher(["이의신청"])
            )
            self.assertEqual(found, {str(raw), str(escaped)})
            self.assertIsNone(
                history.prefilter_paths([str(raw)], Matcher(["이의"], regex=True))
            )

    def test_since_range_starts_at_that_day(self):
        args = type("Args", (), {"date": None, "since": "2026-08-01", "days": 7})()
        start_ms, _, label = date_range(args)
        start = datetime.datetime.fromtimestamp(start_ms / 1000).astimezone()
        self.assertEqual(start.strftime("%Y-%m-%d %H:%M"), "2026-08-01 00:00")
        self.assertTrue(label.startswith("2026-08-01 ~ "))


if __name__ == "__main__":
    unittest.main()
