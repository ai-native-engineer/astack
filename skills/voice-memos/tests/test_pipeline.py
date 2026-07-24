from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import time
import unittest
from contextlib import contextmanager
from pathlib import Path
from unittest import mock

SKILL_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = SKILL_DIR / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

import config  # noqa: E402
import extract  # noqa: E402
import review  # noqa: E402
import transcribe_calls  # noqa: E402


class PipelineTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.transcripts = self.root / "transcripts"

    def tearDown(self):
        self.temporary.cleanup()

    def fake_stt(self, analysis: bool = True) -> Path:
        executable = self.root / ("apple-stt-analysis" if analysis else "apple-stt-legacy")
        help_line = "--analysis-json" if analysis else "legacy only"
        executable.write_text(
            f"""#!/usr/bin/env python3
import hashlib, json, os, pathlib, sys
if '--help' in sys.argv:
    print({help_line!r})
    raise SystemExit(0)
path = pathlib.Path(sys.argv[-1])
with open(os.environ['FAKE_STT_LOG'], 'a', encoding='utf-8') as log:
    log.write(json.dumps(sys.argv[1:]) + '\\n')
if '--analysis-json' not in sys.argv:
    print('테스트 전사')
else:
    terms = []
    if '--vocab-file' in sys.argv:
        vocab = pathlib.Path(sys.argv[sys.argv.index('--vocab-file') + 1])
        terms = [line.strip() for line in vocab.read_text(encoding='utf-8').splitlines() if line.strip()]
    print(json.dumps({{
        'schema_version': 1,
        'engine': 'apple-speech-transcriber',
        'engine_version': hashlib.sha256(pathlib.Path(sys.argv[0]).read_bytes()).hexdigest(),
        'locale': 'ko-KR',
        'offset_unit': 'utf8_bytes',
        'source': {{'audio_sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'duration_ms': 1000}},
        'capabilities': {{'alternatives': False, 'confidence': True, 'audio_time_range': True}},
        'context': {{
            'selected': terms,
            'dropped': [],
            'fingerprint': hashlib.sha256(('\\0'.join(terms)).encode()).hexdigest(),
        }},
        'review_confidence_method': {{'name': 'lower_quantile', 'version': 1, 'quantile': 0.1}},
        'segments': [{{
            'id': 's0001', 'start': 0.0, 'end': 1.0, 'text': '테스트 전사',
            'confidence_spans': [{{'start_byte': 0, 'end_byte': 16, 'confidence': 0.9}}],
            'review_confidence': 0.9,
            'alternatives': [],
        }}],
    }}, ensure_ascii=False))
""",
            encoding="utf-8",
        )
        executable.chmod(0o755)
        return executable

    @contextmanager
    def voice_memo_environment(self, executable: Path, mode: str | None):
        log = self.root / "stt.log"
        values = {
            "VOICE_MEMOS_APPLE_STT": str(executable),
            "FAKE_STT_LOG": str(log),
        }
        if mode is not None:
            values["VOICE_MEMOS_STT_MODE"] = mode
        with (
            mock.patch.dict(os.environ, values, clear=False),
            mock.patch.object(config, "TRANSCRIPTS_DIR", self.transcripts),
            mock.patch.object(config, "LOGS_DIR", self.root / "logs"),
            mock.patch.object(config, "RUNTIME_DIR", self.root / "runtime"),
            mock.patch.object(extract, "TRANSCRIPTS_DIR", self.transcripts),
            mock.patch.object(extract, "CONTEXT_DIR", self.root / "contexts"),
            mock.patch.object(extract, "REVIEW_DB_PATH", self.root / "review.sqlite3"),
            mock.patch.object(extract, "VOCAB_FILE", self.root / "vocab.txt"),
            mock.patch.object(extract, "wait_until_settled", return_value=True),
        ):
            if mode is None:
                os.environ.pop("VOICE_MEMOS_STT_MODE", None)
            yield log

    def audio(self, name: str, content: bytes) -> Path:
        path = self.root / name
        path.write_bytes(content)
        return path

    def test_legacy_default_preserves_output_and_typed_skip(self):
        source = self.audio("20260722 123456-one.m4a", b"first")
        with self.voice_memo_environment(self.fake_stt(), None) as log:
            outcome = extract.process_file(source)
            self.assertEqual(outcome.status, config.OutcomeStatus.PROCESSED)
            transcript = self.transcripts / "20260722" / "123456" / "transcript.md"
            self.assertIn("테스트 전사", transcript.read_text(encoding="utf-8"))
            self.assertFalse((transcript.parent / "analysis.json").exists())
            self.assertNotIn("--analysis-json", log.read_text(encoding="utf-8"))
            source.touch()
            transcript.touch()
            skipped = extract.process_file(source)
            self.assertEqual(skipped.status, config.OutcomeStatus.SKIPPED)

    def test_review_uses_content_identity_and_collision_safe_directories(self):
        first = self.audio("20260722 123456-one.m4a", b"first")
        second = self.audio("20260722 123456-two.m4a", b"second")
        with self.voice_memo_environment(self.fake_stt(), "review") as log:
            outcomes = [extract.process_file(path) for path in (first, second)]

        self.assertTrue(
            all(outcome.status == config.OutcomeStatus.PROCESSED for outcome in outcomes)
        )
        day = self.transcripts / "20260722"
        directories = sorted(day.iterdir())
        self.assertEqual(len(directories), 2)
        expected_hashes = {
            hashlib.sha256(path.read_bytes()).hexdigest() for path in (first, second)
        }
        found_hashes = set()
        for directory in directories:
            analysis = json.loads((directory / "analysis.json").read_text(encoding="utf-8"))
            found_hashes.add(analysis["source"]["audio_sha256"])
            self.assertTrue(directory.name.startswith("123456-"))
            self.assertTrue((directory / "raw.md").exists())
            self.assertTrue((directory / "transcript.md").exists())
            self.assertTrue((directory / "run.json").exists())
        self.assertEqual(found_hashes, expected_hashes)
        invocations = [json.loads(line) for line in log.read_text(encoding="utf-8").splitlines()]
        self.assertTrue(all("--analysis-json" in invocation for invocation in invocations))

    def test_shadow_never_falls_back_when_analysis_mode_is_missing(self):
        source = self.audio("20260722 123456-one.m4a", b"first")
        with self.voice_memo_environment(self.fake_stt(analysis=False), "shadow"):
            outcome = extract.process_file(source)

        self.assertEqual(outcome.status, config.OutcomeStatus.FAILED)
        self.assertEqual(outcome.code, "AnalysisModeUnsupported")
        self.assertFalse(self.transcripts.exists())

    def test_shadow_is_evidence_only(self):
        source = self.audio("20260722 123456-one.m4a", b"first")
        with self.voice_memo_environment(self.fake_stt(), "shadow"):
            outcome = extract.process_file(source)

        directory = next((self.transcripts / "20260722").iterdir())
        self.assertEqual(outcome.status, config.OutcomeStatus.PROCESSED)
        self.assertTrue((directory / "analysis.json").exists())
        self.assertTrue((directory / "raw.md").exists())
        self.assertFalse((directory / "transcript.md").exists())

    def test_context_sidecar_replaces_default_and_records_privacy(self):
        source = self.audio("20260722 123456-one.m4a", b"first")
        recording_id = hashlib.sha256(source.read_bytes()).hexdigest()
        context_dir = self.root / "contexts"
        review.write_context(
            source,
            project="demo",
            participants=["Alice"],
            terms=["명시 용어"],
            privacy="local",
            directory=context_dir,
            reprocess=True,
        )
        vocab = self.root / "vocab.txt"
        vocab.write_text(
            "\n".join(f"공통{index}" for index in range(120)) + "\n",
            encoding="utf-8",
        )
        with review.ReviewStore(self.root / "review.sqlite3") as store:
            store.append_term(
                recording_id=recording_id, term="프로젝트", scope="project:demo"
            )
            store.append_term(recording_id=recording_id, term="전역", scope="global")

        with self.voice_memo_environment(self.fake_stt(), "review") as log:
            outcome = extract.process_file(source)

        self.assertEqual(outcome.status, config.OutcomeStatus.PROCESSED)
        directory = next((self.transcripts / "20260722").iterdir())
        analysis = json.loads((directory / "analysis.json").read_text(encoding="utf-8"))
        self.assertEqual(
            analysis["context"]["selected"][:4],
            ["Alice", "명시 용어", "프로젝트", "전역"],
        )
        self.assertEqual(len(analysis["context"]["selected"]), 100)
        self.assertEqual(len(analysis["context"]["dropped"]), 24)
        run = json.loads((directory / "run.json").read_text(encoding="utf-8"))
        self.assertEqual(run["privacy"], "local")
        self.assertFalse(run["recording_context_missing"])
        self.assertFalse((context_dir / f"{recording_id}.reprocess").exists())
        invocation = json.loads(log.read_text(encoding="utf-8").splitlines()[0])
        self.assertEqual(invocation.count("--vocab-file"), 1)

    def test_analysis_validator_rejects_non_boundary_span_and_empty_segments(self):
        source = self.audio("sample.m4a", b"sample")
        executable = self.fake_stt()
        with self.voice_memo_environment(executable, "review") as log:
            outcome = extract.process_file(source)
        self.assertEqual(outcome.status, config.OutcomeStatus.PROCESSED)
        analysis_path = next(self.transcripts.glob("*/*/analysis.json"))
        analysis = json.loads(analysis_path.read_text(encoding="utf-8"))
        analysis["segments"][0]["confidence_spans"][0]["end_byte"] = 1
        with self.assertRaises(config.AnalysisSchemaError):
            config.validate_analysis_document(analysis)
        analysis["segments"] = []
        with self.assertRaises(config.AnalysisSchemaError):
            config.validate_analysis_document(analysis)
        self.assertTrue(log.exists())

    def test_malformed_context_fails_before_apple_call(self):
        source = self.audio("20260722 123456-one.m4a", b"first")
        recording_id = hashlib.sha256(source.read_bytes()).hexdigest()
        context_dir = self.root / "contexts"
        context_dir.mkdir()
        (context_dir / f"{recording_id}.json").write_text(
            json.dumps({"schema_version": 1, "unknown": True}), encoding="utf-8"
        )
        with self.voice_memo_environment(self.fake_stt(), "review") as log:
            outcome = extract.process_file(source)
        self.assertEqual(outcome.status, config.OutcomeStatus.FAILED)
        self.assertEqual(outcome.code, "ContextValidationError")
        self.assertFalse(log.exists())

    def test_same_audio_under_new_name_reuses_canonical_artifact(self):
        first = self.audio("20260722 123456-one.m4a", b"same")
        second = self.audio("20260723 223344-copy.m4a", b"same")
        with self.voice_memo_environment(self.fake_stt(), "review"):
            self.assertEqual(
                extract.process_file(first).status, config.OutcomeStatus.PROCESSED
            )
            self.assertEqual(
                extract.process_file(second).status, config.OutcomeStatus.SKIPPED
            )
        self.assertEqual(len(list(self.transcripts.glob("*/*/analysis.json"))), 1)

    def test_recording_lock_rejects_second_writer(self):
        recording_id = "a" * 64
        with mock.patch.object(config, "RUNTIME_DIR", self.root / "lock-runtime"):
            with config.recording_lock(recording_id):
                with self.assertRaises(config.RecordingBusy):
                    with config.recording_lock(recording_id):
                        pass

    def test_artifact_path_rejects_escape_components_and_symlinks(self):
        recording_id = "a" * 64
        with mock.patch.object(config, "TRANSCRIPTS_DIR", self.transcripts):
            with self.assertRaises(config.PipelineError):
                config.recording_artifact_dir("..", "000000", recording_id)

            outside = self.root / "outside"
            outside.mkdir()
            self.transcripts.mkdir()
            (self.transcripts / "20260722").symlink_to(outside, target_is_directory=True)
            with self.assertRaises(config.PipelineError):
                config.recording_artifact_dir("20260722", "123456", recording_id)

    def test_call_recording_uses_the_same_analysis_contract(self):
        source = self.audio("홍길동_01012345678_20260722_123456.m4a", b"call")
        log = self.root / "call.log"
        with (
            mock.patch.dict(
                os.environ,
                {
                    "VOICE_MEMOS_APPLE_STT": str(self.fake_stt()),
                    "VOICE_MEMOS_STT_MODE": "review",
                    "FAKE_STT_LOG": str(log),
                },
                clear=False,
            ),
            mock.patch.object(transcribe_calls, "materialize", return_value=True),
            mock.patch.object(transcribe_calls, "wait_until_settled", return_value=True),
            mock.patch.object(config, "RUNTIME_DIR", self.root / "runtime-call"),
            mock.patch.object(transcribe_calls, "CONTEXT_DIR", self.root / "contexts-call"),
            mock.patch.object(transcribe_calls, "REVIEW_DB_PATH", self.root / "review-call.sqlite3"),
            mock.patch.object(transcribe_calls, "VOCAB_FILE", self.root / "vocab-call.txt"),
        ):
            outcome = transcribe_calls.process_file(source)

        self.assertEqual(outcome.status, config.OutcomeStatus.PROCESSED)
        for suffix in (".analysis.json", ".transcript.md", ".run.json"):
            self.assertTrue(source.with_name(f"{source.stem}{suffix}").exists())
        invocation = json.loads(log.read_text(encoding="utf-8").splitlines()[0])
        snapshot = Path(invocation[-1])
        self.assertNotEqual(snapshot, source)
        self.assertFalse(snapshot.exists())

    def test_legacy_call_recording_keeps_timestamps_flag(self):
        source = self.audio("홍길동_20260722_123456.m4a", b"call")
        log = self.root / "call-legacy.log"
        with (
            mock.patch.dict(
                os.environ,
                {
                    "VOICE_MEMOS_APPLE_STT": str(self.fake_stt()),
                    "VOICE_MEMOS_STT_MODE": "legacy",
                    "FAKE_STT_LOG": str(log),
                },
                clear=False,
            ),
            mock.patch.object(transcribe_calls, "materialize", return_value=True),
            mock.patch.object(transcribe_calls, "wait_until_settled", return_value=True),
            mock.patch.object(config, "RUNTIME_DIR", self.root / "runtime-call-legacy"),
        ):
            outcome = transcribe_calls.process_file(source)
        self.assertEqual(outcome.status, config.OutcomeStatus.PROCESSED)
        invocation = json.loads(log.read_text(encoding="utf-8").splitlines()[0])
        self.assertIn("--timestamps", invocation)
        transcript = source.with_name(f"{source.stem}.transcript.md")
        source.write_bytes(b"changed call")
        changed_ns = transcript.stat().st_mtime_ns + 1_000_000
        os.utime(source, ns=(changed_ns, changed_ns))
        with (
            mock.patch.dict(
                os.environ,
                {
                    "VOICE_MEMOS_APPLE_STT": str(self.fake_stt()),
                    "VOICE_MEMOS_STT_MODE": "legacy",
                    "FAKE_STT_LOG": str(log),
                },
                clear=False,
            ),
            mock.patch.object(transcribe_calls, "materialize", return_value=True),
            mock.patch.object(transcribe_calls, "wait_until_settled", return_value=True),
            mock.patch.object(config, "RUNTIME_DIR", self.root / "runtime-call-legacy"),
        ):
            refreshed = transcribe_calls.process_file(source)
        self.assertEqual(refreshed.status, config.OutcomeStatus.PROCESSED)
        self.assertEqual(len(log.read_text(encoding="utf-8").splitlines()), 2)

    def test_unsettled_audio_is_deferred(self):
        source = self.audio("20260722 123456-one.m4a", b"first")
        with self.voice_memo_environment(self.fake_stt(), "review"):
            with mock.patch.object(extract, "wait_until_settled", return_value=False):
                outcome = extract.process_file(source)
        self.assertEqual(outcome.status, config.OutcomeStatus.DEFERRED)
        self.assertEqual(outcome.code, "SettleDeferred")

    def test_source_change_during_transcription_publishes_nothing(self):
        source = self.audio("20260722 123456-one.m4a", b"first")
        seen = {}

        def mutate(snapshot, *_args, **_kwargs):
            seen["snapshot"] = snapshot
            self.assertNotEqual(snapshot, source)
            self.assertEqual(snapshot.read_bytes(), b"first")
            source.write_bytes(b"changed")
            return config.AppleResult(text="stale transcript", analysis=None)

        with self.voice_memo_environment(self.fake_stt(), "legacy"):
            with mock.patch.object(extract, "transcribe", side_effect=mutate):
                outcome = extract.process_file(source)
        self.assertEqual(outcome.status, config.OutcomeStatus.DEFERRED)
        self.assertEqual(outcome.code, "SourceChanged")
        self.assertFalse(self.transcripts.exists())
        self.assertFalse(seen["snapshot"].exists())

    def test_source_change_after_strict_publication_never_finalizes_run(self):
        source = self.audio("20260722 123456-one.m4a", b"first")
        real_write_json = config.atomic_write_json

        def mutate_after_publishing(path, value):
            real_write_json(path, value)
            if path.name == "run.json" and value.get("review_state") == "publishing":
                source.write_bytes(b"changed")

        with self.voice_memo_environment(self.fake_stt(), "review"):
            with mock.patch.object(
                extract, "atomic_write_json", side_effect=mutate_after_publishing
            ):
                outcome = extract.process_file(source)

        self.assertEqual(outcome.status, config.OutcomeStatus.DEFERRED)
        self.assertEqual(outcome.code, "SourceChanged")
        run_path = next(self.transcripts.glob("*/*/run.json"))
        run = json.loads(run_path.read_text(encoding="utf-8"))
        self.assertEqual(run["review_state"], "publishing")

    def test_batch_continues_after_failure_and_exits_nonzero(self):
        outcomes = [
            config.Outcome(config.OutcomeStatus.FAILED, "a" * 64, "SpeechAnalysisError"),
            config.Outcome(config.OutcomeStatus.PROCESSED, "b" * 64),
        ]
        with mock.patch.object(extract, "process_file", side_effect=outcomes) as process:
            status = extract._run([Path("one"), Path("two")], force=False)
        self.assertEqual(status, 1)
        self.assertEqual(process.call_count, 2)

    def test_atomic_write_keeps_previous_artifact_on_rename_failure(self):
        target = self.root / "artifact.md"
        target.write_text("old", encoding="utf-8")
        with mock.patch.object(config.os, "replace", side_effect=OSError("no")):
            with self.assertRaises(config.ArtifactWriteError):
                config.atomic_write_text(target, "new")
        self.assertEqual(target.read_text(encoding="utf-8"), "old")
        self.assertEqual(list(self.root.glob(".artifact.md.*")), [])

    def test_global_lock_queues_and_owner_drains_one_more_pass(self):
        runtime = self.root / "runtime"
        ready = self.root / "ready"
        calls = self.root / "calls"
        fake_python = self.root / "fake-python"
        fake_python.write_text(
            """#!/bin/bash
echo x >> "$FAKE_CALLS"
if mkdir "$FAKE_READY" 2>/dev/null; then sleep 1; fi
exit 0
""",
            encoding="utf-8",
        )
        fake_python.chmod(0o755)
        env = {
            **os.environ,
            "VOICE_MEMOS_RUNTIME_DIR": str(runtime),
            "VOICE_MEMOS_PYTHON": str(fake_python),
            "VOICE_MEMOS_UV": "/usr/bin/true",
            "FAKE_READY": str(ready),
            "FAKE_CALLS": str(calls),
        }
        command = ["/bin/bash", str(SCRIPTS_DIR / "run.sh"), "--skip-notify"]
        owner = subprocess.Popen(command, env=env)
        deadline = time.monotonic() + 5
        while not ready.exists() and time.monotonic() < deadline:
            time.sleep(0.02)
        self.assertTrue(ready.exists())
        contender = subprocess.run(command, env=env, timeout=5)
        self.assertEqual(contender.returncode, 0)
        self.assertEqual(owner.wait(timeout=10), 0)
        self.assertEqual(calls.read_text(encoding="utf-8").count("x"), 4)
        self.assertFalse((runtime / "run.lock").exists())
        self.assertFalse((runtime / "run-queue" / "pending").exists())

    def test_busy_runner_fails_when_pending_marker_is_a_regular_file(self):
        runtime = self.root / "runtime-bad-pending"
        ready = self.root / "bad-pending-ready"
        release = self.root / "bad-pending-release"
        fake_python = self.root / "fake-python-bad-pending"
        fake_python.write_text(
            """#!/bin/bash
if mkdir "$FAKE_READY" 2>/dev/null; then
    while [ ! -f "$FAKE_RELEASE" ]; do /bin/sleep 0.02; done
fi
exit 0
""",
            encoding="utf-8",
        )
        fake_python.chmod(0o755)
        env = {
            **os.environ,
            "VOICE_MEMOS_RUNTIME_DIR": str(runtime),
            "VOICE_MEMOS_PYTHON": str(fake_python),
            "VOICE_MEMOS_UV": "/usr/bin/true",
            "FAKE_READY": str(ready),
            "FAKE_RELEASE": str(release),
        }
        command = ["/bin/bash", str(SCRIPTS_DIR / "run.sh"), "--skip-notify"]
        owner = subprocess.Popen(command, env=env)
        try:
            deadline = time.monotonic() + 5
            while not ready.exists() and time.monotonic() < deadline:
                time.sleep(0.02)
            self.assertTrue(ready.exists())
            pending = runtime / "run-queue" / "pending"
            pending.write_text("stale", encoding="utf-8")
            contender = subprocess.run(command, env=env, timeout=5)
            self.assertNotEqual(contender.returncode, 0)
            self.assertIn(
                "PendingQueueWriteError",
                (runtime / "logs" / "watcher.log").read_text(encoding="utf-8"),
            )
            pending.unlink()
        finally:
            release.touch()
            owner.wait(timeout=10)

    def test_stale_global_lock_is_recovered(self):
        runtime = self.root / "runtime-stale"
        lock = runtime / "run.lock"
        lock.mkdir(parents=True)
        (lock / "owner").write_text(
            "pid=999999\nstart=old\nboot=old\ntoken=old\n", encoding="utf-8"
        )
        env = {
            **os.environ,
            "VOICE_MEMOS_RUNTIME_DIR": str(runtime),
            "VOICE_MEMOS_PYTHON": "/usr/bin/true",
            "VOICE_MEMOS_UV": "/usr/bin/true",
        }
        result = subprocess.run(
            ["/bin/bash", str(SCRIPTS_DIR / "run.sh"), "--skip-notify"],
            env=env,
            timeout=5,
        )
        self.assertEqual(result.returncode, 0)
        self.assertFalse(lock.exists())
        self.assertIn("StalePipelineLock", (runtime / "logs" / "watcher.log").read_text())


if __name__ == "__main__":
    unittest.main()
