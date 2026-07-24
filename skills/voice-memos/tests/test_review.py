import contextlib
import hashlib
import io
import json
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import anyio
from claude_agent_sdk import AssistantMessage, ClaudeAgentOptions, TextBlock
from claude_agent_sdk._internal.transport.subprocess_cli import SubprocessCLITransport


SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import correct  # noqa: E402
import config  # noqa: E402
import notify  # noqa: E402
import review  # noqa: E402
import summarize  # noqa: E402


HASH = "a" * 64


def run_for(**overrides) -> dict:
    value = {
        "schema_version": 1,
        "run_id": "1" * 32,
        "recording_id": HASH,
        "mode": "review",
        "privacy": "standard",
        "source": {"audio_sha256": HASH},
        "parents": {
            "engine_version": "e" * 64,
            "context_fingerprint": "c" * 64,
        },
        "recording_context_missing": False,
        "review_state": "finalizable",
        "candidate_count": 0,
        "summary_state": "missing",
        "summary_parent_sha256": None,
        "summary_body_sha256": None,
        "summary_generator_fingerprint": None,
        "result": "processed",
        "error_code": None,
    }
    value.update(overrides)
    return value


def analysis_for(text: str = "가나다라마바사") -> dict:
    return {
        "schema_version": 1,
        "engine": "apple-speech-transcriber",
        "engine_version": "e" * 64,
        "locale": "ko-KR",
        "offset_unit": "utf8_bytes",
        "source": {"audio_sha256": HASH, "duration_ms": 1250},
        "capabilities": {
            "alternatives": True,
            "confidence": True,
            "audio_time_range": True,
        },
        "context": {
            "project": "demo",
            "selected": [],
            "dropped": [],
            "fingerprint": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        },
        "review_confidence_method": {
            "name": "lower_quantile",
            "version": 1,
            "quantile": 0.1,
        },
        "segments": [
            {
                "id": "s0001",
                "start": 0.0,
                "end": 1.25,
                "text": text,
                "confidence_spans": [],
                "review_confidence": 0.5,
                "alternatives": [
                    {
                        "text": "다른 문장",
                        "start": 0.0,
                        "end": 1.25,
                        "confidence": None,
                    }
                ],
            }
        ],
    }


class ContextTests(unittest.TestCase):
    def test_context_is_strict_and_canonical(self):
        value = review.validate_context(
            {
                "schema_version": 1,
                "participants": [" 승원 ", "승원"],
                "terms": ["Apple", "Apple", "Speech"],
            }
        )
        self.assertEqual(value["privacy"], "standard")
        self.assertEqual(value["participants"], ["승원"])
        self.assertEqual(value["terms"], ["Apple", "Speech"])

        bad_values = (
            {"schema_version": 1, "unknown": True},
            {"schema_version": True},
            {"schema_version": 1, "privacy": "private"},
            {"schema_version": 1, "privacy": None},
            {"schema_version": 1, "topic": "bad\nvalue"},
            {"schema_version": 1, "terms": ["x" * 129]},
            {"schema_version": 1, "terms": [str(index) for index in range(101)]},
        )
        for bad in bad_values:
            with self.subTest(bad=bad), self.assertRaises(review.ContextValidationError):
                review.validate_context(bad)

    def test_context_command_uses_audio_hash_and_private_atomic_file(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            audio = root / "name;$(ignored).m4a"
            audio.write_bytes(b"audio bytes")
            with mock.patch.object(config, "RUNTIME_DIR", root / "runtime"):
                recording_id, path, context = review.write_context(
                    audio,
                    project="demo",
                    participants=["A", "A"],
                    terms=["용어"],
                    privacy="local",
                    directory=root / "contexts",
                    reprocess=True,
                )
            self.assertEqual(recording_id, review.recording_id_for(audio))
            self.assertEqual(review.load_context(path), context)
            self.assertEqual(path.stat().st_mode & 0o777, 0o600)
            self.assertTrue(path.with_suffix(".reprocess").exists())


class SpanTests(unittest.TestCase):
    def test_utf8_boundaries_and_exact_text(self):
        text = "가🙂e\u0301나"
        encoded = text.encode("utf-8")
        emoji_start = len("가".encode("utf-8"))
        emoji_end = emoji_start + len("🙂".encode("utf-8"))
        self.assertEqual(review.utf8_slice(text, emoji_start, emoji_end), "🙂")
        self.assertEqual(
            review.validate_exact_span(text, emoji_end, len(encoded) - 3, "e\u0301"),
            "e\u0301",
        )
        with self.assertRaises(review.CorrectionConflict):
            review.utf8_slice(text, emoji_start + 1, emoji_end)
        with self.assertRaises(review.CorrectionConflict):
            review.validate_exact_span(text, emoji_start, emoji_end, "가")

    def test_fingerprints_and_span_targets_are_stable_and_independent(self):
        first = review.segment_fingerprint(HASH, 0, 1000, "가나다")
        self.assertEqual(first, review.segment_fingerprint(HASH, 0, 1000, "가나다"))
        self.assertNotEqual(first, review.segment_fingerprint(HASH, 0, 1001, "가나다"))
        self.assertNotEqual(
            review.target_id(first, 0, 3, "가"),
            review.target_id(first, 3, 6, "나"),
        )


class StoreTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.db = Path(self.temp.name) / "review.sqlite3"
        self.store = review.ReviewStore(self.db)

    def tearDown(self):
        self.store.close()
        self.temp.cleanup()

    def append(self, start: int, end: int, original: str, replacement: str, **kwargs):
        return self.store.append_decision(
            recording_id=HASH,
            segment_id="s0001",
            source_audio_sha256=HASH,
            start_ms=0,
            end_ms=1250,
            segment_text="가나다라마바사",
            start_byte=start,
            end_byte=end,
            original_text=original,
            decision="manual",
            replacement=replacement,
            **kwargs,
        )

    def test_append_only_revision_and_idempotent_event(self):
        first = self.append(0, 3, "가", "A", event_id="event-1")
        duplicate = self.append(0, 3, "가", "A", event_id="event-1")
        second = self.append(0, 3, "가", "AA", event_id="event-2")
        other_span = self.append(6, 9, "다", "C", event_id="event-3")
        self.assertEqual(first, duplicate)
        self.assertEqual(second["revision"], 2)
        self.assertEqual(second["supersedes_event_id"], "event-1")
        self.assertEqual(other_span["revision"], 1)

        with self.assertRaises(sqlite3.IntegrityError):
            self.store.connection.execute(
                "UPDATE events SET replacement = 'unsafe' WHERE event_id = 'event-1'"
            )
        with self.assertRaises(sqlite3.IntegrityError):
            self.store.connection.execute("DELETE FROM events WHERE event_id = 'event-1'")

    def test_failed_event_rolls_back_and_exact_span_is_required(self):
        with self.assertRaises(review.CorrectionConflict):
            self.append(1, 3, "가", "A")
        count = self.store.connection.execute("SELECT COUNT(*) FROM events").fetchone()[0]
        self.assertEqual(count, 0)

    def test_render_applies_latest_non_overlapping_spans_only(self):
        self.append(0, 3, "가", "A")
        self.append(0, 3, "가", "AA")
        self.append(6, 9, "다", "C")
        self.assertEqual(
            review.render_final_transcript(analysis_for(), self.store),
            "AA나C라마바사\n",
        )
        stale = analysis_for("가나다라마바")
        self.assertEqual(review.render_final_transcript(stale, self.store), "가나다라마바\n")

    def test_scoped_terms_save_and_revoke(self):
        self.store.append_term(recording_id=HASH, term="전문 용어", scope="project:demo")
        self.store.append_term(recording_id=HASH, term="공통", scope="global")
        self.assertEqual(self.store.active_terms(project="demo"), ["전문 용어", "공통"])
        self.store.append_term(
            recording_id=HASH,
            term="전문 용어",
            scope="project:demo",
            revoke=True,
        )
        self.assertEqual(self.store.active_terms(project="demo"), ["공통"])
        with self.assertRaises(review.CorrectionConflict):
            self.store.append_term(recording_id=HASH, term="bad", scope="project:../")

    def test_read_only_on_unsupported_or_damaged_store(self):
        self.store.close()
        connection = sqlite3.connect(self.db)
        connection.execute("PRAGMA user_version = 99")
        connection.close()
        self.store = review.ReviewStore(self.db)
        self.assertTrue(self.store.read_only)
        with self.assertRaises(review.CorrectionStoreError):
            self.append(0, 3, "가", "A")

        self.store.close()
        damaged = Path(self.temp.name) / "damaged.sqlite3"
        damaged.write_bytes(b"not sqlite")
        broken = review.ReviewStore(damaged)
        try:
            self.assertTrue(broken.read_only)
            self.assertIn("restore", broken.error)
        finally:
            broken.close()

    def test_existing_version_zero_store_gets_online_backup(self):
        self.store.close()
        old = sqlite3.connect(self.db)
        old.execute("PRAGMA user_version = 0")
        old.execute("CREATE TABLE legacy(value TEXT)")
        old.commit()
        old.close()
        self.store = review.ReviewStore(self.db)
        self.assertFalse(self.store.read_only)
        self.assertEqual(self.db.stat().st_mode & 0o777, 0o600)
        self.assertEqual(
            self.store.connection.execute("PRAGMA user_version").fetchone()[0], 1
        )
        backups = list(self.db.parent.glob("review.sqlite3.backup-*"))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].stat().st_mode & 0o777, 0o600)


class ReviewCoreTests(unittest.TestCase):
    def test_status_has_no_transcript_body_and_tracks_stale(self):
        with tempfile.TemporaryDirectory() as temp:
            with review.ReviewStore(Path(temp) / "review.sqlite3") as store:
                value = analysis_for("secret transcript")
                status = review.render_status(value, store)
                self.assertIn("candidates: 1", status)
                self.assertIn("pending: 1", status)
                self.assertNotIn("secret transcript", status)

    def test_correct_shim_never_mutates(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "transcript.md"
            path.write_text("wrong wrong\n", encoding="utf-8")
            stderr = io.StringIO()
            with contextlib.redirect_stderr(stderr):
                result = correct.main()
            self.assertEqual(result, 2)
            self.assertEqual(path.read_text(encoding="utf-8"), "wrong wrong\n")
            self.assertIn("review.py", stderr.getvalue())

    def test_render_refuses_read_only_store(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            analysis_path = root / "analysis.json"
            analysis_path.write_text(
                json.dumps(analysis_for(), ensure_ascii=False), encoding="utf-8"
            )
            db = root / "review.sqlite3"
            connection = sqlite3.connect(db)
            connection.execute("PRAGMA user_version = 99")
            connection.close()
            output = root / "final.txt"
            stderr = io.StringIO()
            with contextlib.redirect_stderr(stderr):
                result = review.main(
                    [
                        "render",
                        "--analysis",
                        str(analysis_path),
                        "--db",
                        str(db),
                        "--output",
                        str(output),
                    ]
                )
            self.assertEqual(result, 2)
            self.assertFalse(output.exists())
            self.assertIn("unsupported schema version", stderr.getvalue())


class SummaryPrivacyTests(unittest.TestCase):
    def transcript(self, root: Path) -> Path:
        path = root / "transcript.md"
        path.write_text(
            "# memo\n\n## 전사 내용\n\n" + ("충분히 긴 전사 데이터입니다. " * 30),
            encoding="utf-8",
        )
        return path

    def test_local_privacy_makes_zero_sdk_calls(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            path = self.transcript(root)
            (root / "run.json").write_text(
                json.dumps(run_for(privacy="local")), encoding="utf-8"
            )
            called = False

            async def fake_query(*args, **kwargs):
                nonlocal called
                called = True
                if False:
                    yield None

            with mock.patch.object(summarize, "query", fake_query):
                result = anyio.run(summarize.summarize_file, path)
            self.assertFalse(result)
            self.assertFalse(called)

    def test_malformed_run_missing_privacy_fails_before_sidecar_or_sdk(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            path = self.transcript(root)
            contexts = root / "contexts"
            malformed = run_for()
            malformed.pop("privacy")
            (root / "run.json").write_text(
                json.dumps(malformed), encoding="utf-8"
            )
            sidecar = review.context_path(HASH, contexts)
            sidecar.parent.mkdir()
            sidecar.write_text(
                json.dumps({"schema_version": 1, "privacy": "local"}),
                encoding="utf-8",
            )
            with (
                mock.patch.object(summarize, "DEFAULT_CONTEXT_DIR", contexts),
                mock.patch.object(config, "RUNTIME_DIR", root / "runtime"),
                mock.patch.object(summarize, "query") as query,
            ):
                with self.assertRaises(review.PrivacyModeValidationError):
                    anyio.run(summarize.summarize_file, path)
            query.assert_not_called()

    def test_strict_mode_without_run_metadata_makes_zero_sdk_calls(self):
        with tempfile.TemporaryDirectory() as temp:
            path = self.transcript(Path(temp))
            with (
                mock.patch.dict(
                    config.os.environ,
                    {"VOICE_MEMOS_STT_MODE": "review"},
                    clear=False,
                ),
                mock.patch.object(summarize, "query") as query,
            ):
                self.assertFalse(anyio.run(summarize.summarize_file, path))
            query.assert_not_called()

    def test_standard_summary_disables_tools_and_allows_one_turn(self):
        with tempfile.TemporaryDirectory() as temp:
            path = self.transcript(Path(temp))
            captured = {}

            async def fake_query(*, prompt, options):
                captured["prompt"] = prompt
                captured["options"] = options
                if False:
                    yield None

            with mock.patch.object(summarize, "query", fake_query):
                with self.assertRaisesRegex(RuntimeError, "빈 응답"):
                    anyio.run(summarize.summarize_file, path)
            self.assertEqual(captured["options"].tools, [])
            self.assertEqual(captured["options"].max_turns, 1)
            self.assertIn("신뢰할 수 없는 데이터", captured["prompt"])

    def test_sdk_serializes_empty_tools_without_allowed_tools(self):
        options = ClaudeAgentOptions(tools=[], cli_path="/tmp/claude")
        command = SubprocessCLITransport("prompt", options)._build_command()
        tools_index = command.index("--tools")
        self.assertEqual(command[tools_index + 1], "")
        self.assertNotIn("--allowedTools", command)

    def test_unknown_privacy_fails_before_sdk_call(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            path = self.transcript(root)
            (root / "run.json").write_text(
                json.dumps(run_for(privacy="unknown")), encoding="utf-8"
            )
            with mock.patch.object(summarize, "query") as query:
                with self.assertRaises(review.PrivacyModeValidationError):
                    anyio.run(summarize.summarize_file, path)
            query.assert_not_called()

    def test_review_pending_makes_zero_sdk_calls(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            path = self.transcript(root)
            (root / "run.json").write_text(
                json.dumps(run_for(review_state="review_pending", candidate_count=1)),
                encoding="utf-8",
            )
            with mock.patch.object(summarize, "query") as query:
                self.assertFalse(anyio.run(summarize.summarize_file, path))
            query.assert_not_called()

    def test_publishing_state_makes_zero_sdk_calls(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            path = self.transcript(root)
            (root / "run.json").write_text(
                json.dumps(run_for(review_state="publishing")),
                encoding="utf-8",
            )
            with mock.patch.object(summarize, "query") as query:
                self.assertFalse(anyio.run(summarize.summarize_file, path))
            query.assert_not_called()

    def test_current_local_sidecar_overrides_stale_standard_run(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            path = self.transcript(root)
            contexts = root / "contexts"
            contexts.mkdir()
            (root / "run.json").write_text(
                json.dumps(run_for()),
                encoding="utf-8",
            )
            review.context_path(HASH, contexts).write_text(
                json.dumps({"schema_version": 1, "privacy": "local"}),
                encoding="utf-8",
            )
            with (
                mock.patch.object(summarize, "DEFAULT_CONTEXT_DIR", contexts),
                mock.patch.object(config, "RUNTIME_DIR", root / "runtime"),
                mock.patch.object(summarize, "query") as query,
            ):
                self.assertFalse(anyio.run(summarize.summarize_file, path))
            query.assert_not_called()

    def test_notify_fails_closed_for_pending_or_local_artifact(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            path = self.transcript(root)
            summary_path = root / "summary.md"
            summary_path.write_text("## 요약\n본문\n", encoding="utf-8")
            metadata = run_for(
                review_state="review_pending",
                candidate_count=1,
                summary_state="fresh",
                summary_parent_sha256=config.source_sha256(path),
                summary_body_sha256=hashlib.sha256(
                    config.strip_process_markers(
                        summary_path.read_text(encoding="utf-8")
                    ).encode("utf-8")
                ).hexdigest(),
                summary_generator_fingerprint="f" * 64,
            )
            (root / "run.json").write_text(json.dumps(metadata), encoding="utf-8")
            self.assertIs(notify._strict_delivery_metadata(path), False)
            metadata["review_state"] = "finalizable"
            metadata["privacy"] = "local"
            (root / "run.json").write_text(json.dumps(metadata), encoding="utf-8")
            self.assertIs(notify._strict_delivery_metadata(path), False)

    def test_notify_fails_closed_in_strict_mode_without_run_metadata(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            path = self.transcript(root)
            (root / "summary.md").write_text("## 요약\n본문\n", encoding="utf-8")
            with mock.patch.dict(
                config.os.environ,
                {"VOICE_MEMOS_STT_MODE": "review"},
                clear=False,
            ):
                self.assertIs(notify._strict_delivery_metadata(path), False)

    def test_stale_summary_is_regenerated_and_bound_to_transcript(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            path = self.transcript(root)
            (root / "analysis.json").write_text(
                json.dumps(analysis_for(), ensure_ascii=False), encoding="utf-8"
            )
            run = run_for()
            (root / "run.json").write_text(json.dumps(run), encoding="utf-8")
            (root / "summary.md").write_text(
                "stale\n<!-- notified -->\n", encoding="utf-8"
            )

            async def fake_query(*_args, **_kwargs):
                yield AssistantMessage(
                    content=[TextBlock("## 제목\n새 제목\n\n## 요약\n새 요약")],
                    model="fake",
                )

            with (
                mock.patch.object(config, "RUNTIME_DIR", root / "runtime"),
                mock.patch.object(summarize, "query", fake_query),
            ):
                self.assertTrue(anyio.run(summarize.summarize_file, path))

            updated = json.loads((root / "run.json").read_text(encoding="utf-8"))
            self.assertEqual(updated["summary_state"], "fresh")
            self.assertEqual(
                updated["summary_parent_sha256"], config.source_sha256(path)
            )
            self.assertEqual(
                updated["summary_generator_fingerprint"],
                summarize.SUMMARY_GENERATOR_FINGERPRINT,
            )
            summary = (root / "summary.md").read_text(encoding="utf-8")
            self.assertIn("새 요약", summary)
            self.assertNotIn("<!-- notified -->", summary)
            self.assertEqual(
                updated["summary_body_sha256"],
                hashlib.sha256(
                    config.strip_process_markers(summary).encode("utf-8")
                ).hexdigest(),
            )


if __name__ == "__main__":
    unittest.main()
