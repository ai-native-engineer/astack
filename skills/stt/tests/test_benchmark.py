from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock


SCRIPT = Path(__file__).parents[1] / "scripts" / "benchmark.py"
SPEC = importlib.util.spec_from_file_location("stt_benchmark", SCRIPT)
benchmark = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(benchmark)


class BenchmarkTest(unittest.TestCase):
    def _scaffold_input(self, root: Path) -> Path:
        (root / "cal.m4a").write_bytes(b"calibration audio")
        (root / "eval.m4a").write_bytes(b"evaluation audio")
        (root / "frozen-vocab.txt").write_text("Caret\n", encoding="utf-8")
        metadata = {
            "schema_version": 1,
            "recordings": [
                {
                    "id": "cal-01",
                    "split": "calibration",
                    "environment": "quiet-room",
                    "speaker_configuration": "single",
                    "audio_file": "cal.m4a",
                    "result_file": "recordings/cal-01.json",
                    "vocab_file": "frozen-vocab.txt",
                    "context": ["ClovaNote"],
                    "transcript": "MUST NOT LEAK",
                },
                {
                    "id": "eval-01",
                    "split": "evaluation",
                    "environment": "meeting-room",
                    "speaker_configuration": "multi",
                    "audio_file": "eval.m4a",
                    "result_file": "recordings/eval-01.json",
                },
            ],
        }
        path = root / "metadata.json"
        path.write_text(json.dumps(metadata, ensure_ascii=False), encoding="utf-8")
        return path

    def _fake_apple_stt(self, root: Path) -> Path:
        path = root / "fake-apple-stt"
        path.write_text(
            f"""#!{sys.executable}
import hashlib, json, sys
from pathlib import Path
args = sys.argv[1:]
audio = Path(args[-1])
vocab = Path(args[args.index('--vocab-file') + 1])
terms = [line.strip() for line in vocab.read_text(encoding='utf-8').splitlines() if line.strip()]
binary_hash = hashlib.sha256(Path(sys.argv[0]).read_bytes()).hexdigest()
audio_hash = hashlib.sha256(audio.read_bytes()).hexdigest()
context_hash = hashlib.sha256('\\0'.join(terms).encode()).hexdigest()
print(json.dumps({{
    'schema_version': 1,
    'engine': 'apple-speech-transcriber',
    'engine_version': binary_hash,
    'locale': args[args.index('--locale') + 1],
    'source': {{'audio_sha256': audio_hash, 'duration_ms': 1000}},
    'context': {{'fingerprint': context_hash, 'selected': terms, 'dropped': []}},
    'segments': [{{'id': 's0001', 'start': 0, 'end': 1, 'text': 'PRIVATE TRANSCRIPT'}}],
}}))
""",
            encoding="utf-8",
        )
        path.chmod(0o700)
        return path

    def _fake_legacy_stt(
        self,
        root: Path,
        payload: object,
        expected_vocab_text: str | None = None,
        mutate_ambient: bool = False,
    ) -> Path:
        path = root / "fake-legacy-apple-stt"
        encoded = json.dumps(payload, ensure_ascii=False)
        path.write_text(
            f"""#!{sys.executable}
import json, sys
from pathlib import Path
args = sys.argv[1:]
expected_vocab = {expected_vocab_text!r}
vocab = Path(args[args.index('--vocab-file') + 1]) if '--vocab-file' in args else None
if (
    '--json' not in args
    or '--analysis-json' in args
    or vocab is None
    or not vocab.is_file()
    or (expected_vocab is not None and vocab.read_text(encoding='utf-8') != expected_vocab)
):
    raise SystemExit(9)
if {mutate_ambient!r}:
    (Path.home() / '.config/stt/vocab.txt').write_text('CHANGED DURING CAPTURE\\n', encoding='utf-8')
print(json.dumps(json.loads({encoded!r}), ensure_ascii=False))
""",
            encoding="utf-8",
        )
        path.chmod(0o700)
        return path

    def test_scaffold_hashes_explicit_audio_without_copying_transcript(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            metadata = self._scaffold_input(root)
            manifest = root / "private" / "manifest.json"
            completed = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "scaffold",
                    "--input",
                    str(metadata),
                    "--output",
                    str(manifest),
                    "--allow-root",
                    str(root),
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            value = json.loads(manifest.read_text(encoding="utf-8"))
            self.assertEqual({item["split"] for item in value["recordings"]}, {"calibration", "evaluation"})
            self.assertEqual(len({item["audio_sha256"] for item in value["recordings"]}), 2)
            self.assertNotIn("MUST NOT LEAK", manifest.read_text(encoding="utf-8"))
            self.assertNotIn("transcript", value["recordings"][0])
            self.assertNotIn("utterances", value["recordings"][0])
            self.assertEqual(manifest.stat().st_mode & 0o777, 0o600)
            self.assertEqual(manifest.parent.stat().st_mode & 0o777, 0o700)
            self.assertFalse(manifest.with_name("gold-signoff.json").exists())
            self.assertNotIn(str(root), completed.stdout)

    def test_scaffold_rejects_duplicate_audio_and_unapproved_root(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            metadata = self._scaffold_input(root)
            value = json.loads(metadata.read_text(encoding="utf-8"))
            value["recordings"][1]["audio_file"] = "cal.m4a"
            metadata.write_text(json.dumps(value), encoding="utf-8")
            manifest = root / "manifest.json"
            duplicate = subprocess.run(
                [sys.executable, str(SCRIPT), "scaffold", "--input", str(metadata), "--output", str(manifest), "--allow-root", str(root)],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(duplicate.returncode, 2)
            self.assertFalse(manifest.exists())

            value["recordings"][1]["audio_file"] = "eval.m4a"
            metadata.write_text(json.dumps(value), encoding="utf-8")
            outside = subprocess.run(
                [sys.executable, str(SCRIPT), "scaffold", "--input", str(metadata), "--output", str(manifest)],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(outside.returncode, 2)
            self.assertFalse(manifest.exists())

            real_root = root / "real-root"
            real_root.mkdir()
            linked_root = root / "linked-root"
            linked_root.symlink_to(real_root, target_is_directory=True)
            symlinked = subprocess.run(
                [sys.executable, str(SCRIPT), "scaffold", "--input", str(metadata), "--output", str(linked_root / "manifest.json"), "--allow-root", str(linked_root)],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(symlinked.returncode, 2)
            self.assertFalse((real_root / "manifest.json").exists())

    def test_capture_uses_frozen_or_explicit_empty_context_and_is_immutable(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            metadata = self._scaffold_input(root)
            manifest = root / "manifest.json"
            scaffold = subprocess.run(
                [sys.executable, str(SCRIPT), "scaffold", "--input", str(metadata), "--output", str(manifest), "--allow-root", str(root)],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(scaffold.returncode, 0, scaffold.stderr)
            binary = self._fake_apple_stt(root)
            run_dir = root / "runs" / "candidate"
            command = [
                sys.executable,
                str(SCRIPT),
                "capture",
                "--manifest",
                str(manifest),
                "--binary",
                str(binary),
                "--run-dir",
                str(run_dir),
                "--locale",
                "ko-KR",
                "--allow-root",
                str(root),
            ]
            captured = subprocess.run(command, text=True, capture_output=True, check=False)
            self.assertEqual(captured.returncode, 0, captured.stderr)
            self.assertNotIn(str(root), captured.stdout)
            self.assertNotIn("PRIVATE TRANSCRIPT", captured.stdout + captured.stderr)
            run = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
            self.assertEqual(run["result_mode"], "strict")
            self.assertEqual(run["manifest_sha256"], benchmark.canonical_hash(json.loads(manifest.read_text(encoding="utf-8"))))
            self.assertEqual(run["fingerprints"]["binary_sha256"], benchmark.hashlib.sha256(binary.read_bytes()).hexdigest())
            self.assertRegex(run["fingerprints"]["config_sha256"], r"^[0-9a-f]{64}$")
            self.assertNotIn("PRIVATE TRANSCRIPT", json.dumps(run))
            self.assertNotIn("ClovaNote", json.dumps(run))
            self.assertEqual((run_dir / "run.json").stat().st_mode & 0o777, 0o600)
            self.assertEqual(run_dir.stat().st_mode & 0o777, 0o700)
            self.assertFalse((run_dir / "signoff.json").exists())

            cal_result = json.loads((run_dir / "recordings" / "cal-01.json").read_text(encoding="utf-8"))
            eval_result = json.loads((run_dir / "recordings" / "eval-01.json").read_text(encoding="utf-8"))
            self.assertEqual(cal_result["context"]["selected"], ["Caret", "ClovaNote"])
            self.assertEqual(eval_result["context"]["selected"], [])

            before = (run_dir / "run.json").read_bytes()
            repeated = subprocess.run(command, text=True, capture_output=True, check=False)
            self.assertEqual(repeated.returncode, 2)
            self.assertEqual((run_dir / "run.json").read_bytes(), before)

            common_vocab = root / "common-vocab.txt"
            common_vocab.write_text("CommonTerm\n", encoding="utf-8")
            context_dir = root / "runs" / "context"
            context_command = command.copy()
            context_command[context_command.index("--run-dir") + 1] = str(context_dir)
            context_command[context_command.index("--allow-root"):context_command.index("--allow-root")] = [
                "--vocab-file",
                str(common_vocab),
            ]
            context_capture = subprocess.run(
                context_command, text=True, capture_output=True, check=False
            )
            self.assertEqual(context_capture.returncode, 0, context_capture.stderr)
            context_result = json.loads(
                (context_dir / "recordings" / "cal-01.json").read_text(encoding="utf-8")
            )
            context_run = json.loads((context_dir / "run.json").read_text(encoding="utf-8"))
            self.assertEqual(context_result["context"]["selected"], ["CommonTerm"])
            self.assertEqual(context_run["manifest_sha256"], run["manifest_sha256"])

            gated = subprocess.run(
                [sys.executable, str(SCRIPT), "compare", "--manifest", str(manifest), "--baseline-dir", str(run_dir), "--candidate-dir", str(run_dir), "--gate"],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(gated.returncode, 1, gated.stderr)

    def test_legacy_capture_is_benchmark_only_bound_and_private(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            metadata = self._scaffold_input(root)
            manifest = root / "manifest.json"
            scaffold = subprocess.run(
                [sys.executable, str(SCRIPT), "scaffold", "--input", str(metadata), "--output", str(manifest), "--allow-root", str(root)],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(scaffold.returncode, 0, scaffold.stderr)
            vocab = root / ".config" / "stt" / "vocab.txt"
            vocab.parent.mkdir(parents=True)
            vocab.write_text("Caret\ncaret\nCaret\n", encoding="utf-8")
            binary = self._fake_legacy_stt(
                root,
                [{"start": 0, "end": 1.25, "text": "PRIVATE LEGACY TRANSCRIPT"}],
                "Caret\ncaret\nCaret\n",
            )
            run_dir = root / "runs" / "legacy"
            captured = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "capture",
                    "--legacy-json",
                    "--manifest",
                    str(manifest),
                    "--binary",
                    str(binary),
                    "--vocab-file",
                    str(vocab),
                    "--run-dir",
                    str(run_dir),
                    "--allow-root",
                    str(root),
                ],
                text=True,
                capture_output=True,
                check=False,
                env={**os.environ, "HOME": str(root)},
            )
            self.assertEqual(captured.returncode, 0, captured.stderr)
            self.assertNotIn(str(root), captured.stdout)
            self.assertNotIn("PRIVATE LEGACY TRANSCRIPT", captured.stdout + captured.stderr)

            manifest_value = json.loads(manifest.read_text(encoding="utf-8"))
            run = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
            result = json.loads((run_dir / "recordings" / "cal-01.json").read_text(encoding="utf-8"))
            adapter = result["benchmark_adapter"]
            profile = adapter["vocab_input_profile"]
            self.assertEqual(run["manifest_sha256"], benchmark.canonical_hash(manifest_value))
            self.assertEqual(run["result_mode"], "legacy")
            self.assertEqual(result["engine_version"], run["fingerprints"]["binary_sha256"])
            self.assertEqual(result["source"]["audio_sha256"], manifest_value["recordings"][0]["audio_sha256"])
            self.assertEqual(result["segments"][0]["id"], "s0001")
            self.assertEqual(adapter["name"], "apple-stt-legacy-json")
            self.assertEqual(adapter["duration_source"], "max_segment_end")
            self.assertEqual(adapter["strict_analysis_compatible"], False)
            self.assertEqual(adapter["script_sha256"], benchmark._file_hash(SCRIPT))
            self.assertEqual(profile["non_comment_entries"], 3)
            self.assertTrue(profile["deployed_voice_memos"])
            self.assertEqual(profile["input_mode"], "ambient_plus_explicit_same_file")
            self.assertEqual(profile["ambient_file_sha256"], benchmark._file_hash(vocab))
            self.assertEqual(profile["explicit_file_sha256"], benchmark._file_hash(vocab))
            self.assertEqual(profile["ambient_entries"], 3)
            self.assertEqual(profile["explicit_entries"], 3)
            self.assertEqual(profile["effective_hint_entries"], 6)
            self.assertEqual(profile["exact_duplicate_entries"], 1)
            self.assertEqual(profile["casefold_duplicate_entries"], 2)
            self.assertNotIn("offset_unit", result)
            self.assertNotIn("context", result)
            self.assertEqual((run_dir / "run.json").stat().st_mode & 0o777, 0o600)
            self.assertEqual((run_dir / "recordings" / "cal-01.json").stat().st_mode & 0o777, 0o600)
            self.assertEqual(run_dir.stat().st_mode & 0o777, 0o700)

    def test_legacy_capture_rejects_empty_or_invalid_intervals_without_publish(self):
        payloads = (
            [],
            [{"start": 0, "end": 0, "text": "PRIVATE"}],
            [{"start": 2, "end": 1, "text": "PRIVATE"}],
            [{"start": True, "end": 1, "text": "PRIVATE"}],
            [{"start": 10**400, "end": 10**401, "text": "PRIVATE"}],
        )
        for index, payload in enumerate(payloads):
            with self.subTest(payload=payload), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary).resolve()
                metadata = self._scaffold_input(root)
                manifest = root / "manifest.json"
                scaffold = subprocess.run(
                    [sys.executable, str(SCRIPT), "scaffold", "--input", str(metadata), "--output", str(manifest), "--allow-root", str(root)],
                    text=True,
                    capture_output=True,
                    check=False,
                )
                self.assertEqual(scaffold.returncode, 0, scaffold.stderr)
                vocab = root / ".config" / "stt" / "vocab.txt"
                vocab.parent.mkdir(parents=True)
                vocab.write_text("", encoding="utf-8")
                binary = self._fake_legacy_stt(root, payload)
                run_dir = root / "runs" / f"invalid-{index}"
                captured = subprocess.run(
                    [
                        sys.executable,
                        str(SCRIPT),
                        "capture",
                        "--legacy-json",
                        "--manifest",
                        str(manifest),
                        "--binary",
                        str(binary),
                        "--vocab-file",
                        str(vocab),
                        "--run-dir",
                        str(run_dir),
                        "--allow-root",
                        str(root),
                    ],
                    text=True,
                    capture_output=True,
                    check=False,
                    env={**os.environ, "HOME": str(root)},
                )
                self.assertEqual(captured.returncode, 2)
                self.assertFalse(run_dir.exists())
                self.assertNotIn("PRIVATE", captured.stdout + captured.stderr)
                self.assertNotIn("unrecognized arguments", captured.stderr)

    def test_legacy_capture_rejects_a_vocab_different_from_deployed_ambient(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            metadata = self._scaffold_input(root)
            manifest = root / "manifest.json"
            scaffold = subprocess.run(
                [sys.executable, str(SCRIPT), "scaffold", "--input", str(metadata), "--output", str(manifest), "--allow-root", str(root)],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(scaffold.returncode, 0, scaffold.stderr)
            ambient = root / ".config" / "stt" / "vocab.txt"
            ambient.parent.mkdir(parents=True)
            ambient.write_text("DeployedTerm\n", encoding="utf-8")
            different = root / "different-vocab.txt"
            different.write_text("DifferentTerm\n", encoding="utf-8")
            binary = self._fake_legacy_stt(
                root, [{"start": 0, "end": 1, "text": "PRIVATE"}]
            )
            run_dir = root / "runs" / "mismatched-vocab"
            captured = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "capture",
                    "--legacy-json",
                    "--manifest",
                    str(manifest),
                    "--binary",
                    str(binary),
                    "--vocab-file",
                    str(different),
                    "--run-dir",
                    str(run_dir),
                    "--allow-root",
                    str(root),
                ],
                text=True,
                capture_output=True,
                check=False,
                env={**os.environ, "HOME": str(root)},
            )
            self.assertEqual(captured.returncode, 2)
            self.assertFalse(run_dir.exists())
            self.assertNotIn("PRIVATE", captured.stdout + captured.stderr)

    def test_legacy_capture_rejects_missing_or_changed_ambient_without_publish(self):
        for case in ("missing", "changed_during_capture"):
            with self.subTest(case=case), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary).resolve()
                metadata = self._scaffold_input(root)
                manifest = root / "manifest.json"
                scaffold = subprocess.run(
                    [sys.executable, str(SCRIPT), "scaffold", "--input", str(metadata), "--output", str(manifest), "--allow-root", str(root)],
                    text=True,
                    capture_output=True,
                    check=False,
                )
                self.assertEqual(scaffold.returncode, 0, scaffold.stderr)
                ambient = root / ".config" / "stt" / "vocab.txt"
                if case == "changed_during_capture":
                    ambient.parent.mkdir(parents=True)
                    ambient.write_text("DeployedTerm\n", encoding="utf-8")
                    explicit = ambient
                else:
                    explicit = root / "frozen-vocab-snapshot.txt"
                    explicit.write_text("DeployedTerm\n", encoding="utf-8")
                binary = self._fake_legacy_stt(
                    root,
                    [{"start": 0, "end": 1, "text": "PRIVATE"}],
                    "DeployedTerm\n",
                    mutate_ambient=case == "changed_during_capture",
                )
                run_dir = root / "runs" / case
                captured = subprocess.run(
                    [
                        sys.executable,
                        str(SCRIPT),
                        "capture",
                        "--legacy-json",
                        "--manifest",
                        str(manifest),
                        "--binary",
                        str(binary),
                        "--vocab-file",
                        str(explicit),
                        "--run-dir",
                        str(run_dir),
                        "--allow-root",
                        str(root),
                    ],
                    text=True,
                    capture_output=True,
                    check=False,
                    env={**os.environ, "HOME": str(root)},
                )
                self.assertEqual(captured.returncode, 2)
                self.assertFalse(run_dir.exists())
                self.assertNotIn("PRIVATE", captured.stdout + captured.stderr)

    def test_normalization_and_cer(self):
        self.assertEqual(benchmark.normalize_surface(" A\n B "), "A B")
        self.assertEqual(benchmark.normalize_content("가, 나!"), "가나")
        self.assertEqual(benchmark.edit_distance("가나다", "가마"), 2)

    def test_capture_result_rejects_unbound_context_fingerprint(self):
        recording = {"id": "sample", "audio_sha256": "a" * 64}
        value = {
            "schema_version": 1,
            "engine": "apple-speech-transcriber",
            "engine_version": "b" * 64,
            "locale": "ko-KR",
            "source": {"audio_sha256": "a" * 64, "duration_ms": 1000},
            "context": {"fingerprint": "0" * 64, "selected": ["term"], "dropped": []},
            "segments": [{"id": "s1", "start": 0, "end": 1, "text": "text"}],
        }
        with self.assertRaisesRegex(benchmark.BenchmarkError, "bound"):
            benchmark._capture_result(value, recording, "b" * 64, "ko-KR")

    def test_many_to_many_alignment_keeps_unmapped_ranges(self):
        gold = [
            {"id": "g1", "start_ms": 0, "end_ms": 1000, "text": "하나"},
            {"id": "g2", "start_ms": 1000, "end_ms": 2000, "text": "둘"},
            {"id": "g3", "start_ms": 3000, "end_ms": 4000, "text": "셋"},
        ]
        hypothesis = [
            {"id": "s1", "start_ms": 0, "end_ms": 1500, "text": "하나 둘"},
            {"id": "s2", "start_ms": 1500, "end_ms": 2000, "text": "계속"},
        ]
        components = benchmark.align_components(gold, hypothesis)
        self.assertEqual([[item["id"] for item in group["gold"]] for group in components], [["g1", "g2"], ["g3"]])
        self.assertEqual([item["id"] for item in components[0]["hypothesis"]], ["s1", "s2"])
        self.assertTrue(components[1]["manual_signoff_required"])

    def test_reference_and_hypothesis_utf8_offsets_are_mapped_separately(self):
        reference = "가나다"
        hypothesis = "가너다"
        self.assertEqual(benchmark.map_reference_span(reference, hypothesis, 3, 6), (3, 6))
        self.assertIsNone(benchmark.map_reference_span(reference, hypothesis, 1, 6))
        self.assertIsNone(benchmark.map_reference_span("가나다라", "가XY라", 3, 6))

    def test_result_file_cannot_escape_through_symlink(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            run = root / "run"
            outside = root / "outside"
            run.mkdir()
            outside.mkdir()
            (run / "recordings").symlink_to(outside, target_is_directory=True)
            with self.assertRaises(benchmark.BenchmarkError):
                benchmark._safe_result_path(
                    run, {"id": "fixture", "result_file": "recordings/result.json"}
                )

    def test_audio_fingerprint_cannot_leak_between_splits(self):
        recording = {
            "environment": "room",
            "speaker_configuration": "single",
            "audio_sha256": "a" * 64,
            "utterances": [],
            "named_terms": [],
            "required_phrases": [],
            "correction_targets": [],
        }
        manifest = {
            "schema_version": 1,
            "recordings": [
                {**recording, "id": "cal", "split": "calibration"},
                {**recording, "id": "eval", "split": "evaluation"},
            ],
        }
        with self.assertRaisesRegex(benchmark.BenchmarkError, "fingerprint"):
            benchmark._validate_manifest(manifest)

    def test_duplicate_normalized_result_files_and_insecure_root_are_rejected(self):
        recording = {
            "environment": "room",
            "speaker_configuration": "single",
            "utterances": [],
            "named_terms": [],
            "required_phrases": [],
            "correction_targets": [],
        }
        manifest = {
            "schema_version": 1,
            "recordings": [
                {**recording, "id": "cal", "split": "calibration", "audio_sha256": "a" * 64, "result_file": "recordings/result.json"},
                {**recording, "id": "eval", "split": "evaluation", "audio_sha256": "b" * 64, "result_file": "recordings/./result.json"},
            ],
        }
        with self.assertRaisesRegex(benchmark.BenchmarkError, "result_file"):
            benchmark._validate_manifest(manifest)

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            metadata = self._scaffold_input(root)
            root.chmod(0o755)
            manifest_path = root / "manifest.json"
            completed = subprocess.run(
                [sys.executable, str(SCRIPT), "scaffold", "--input", str(metadata), "--output", str(manifest_path), "--allow-root", str(root)],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(completed.returncode, 2)
            self.assertFalse(manifest_path.exists())
            self.assertEqual(root.stat().st_mode & 0o777, 0o755)

    def test_scaffold_race_never_overwrites_a_concurrently_created_manifest(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary).resolve()
            metadata = self._scaffold_input(root)
            manifest_path = root / "private" / "manifest.json"
            raced_content = '{"created_by":"other-process"}\n'
            original_atomic_create = benchmark._atomic_create

            def create_racer_then_publish(path: Path, content: str) -> None:
                path.write_text(raced_content, encoding="utf-8")
                original_atomic_create(path, content)

            with mock.patch.object(
                benchmark, "_atomic_create", side_effect=create_racer_then_publish
            ), self.assertRaisesRegex(benchmark.BenchmarkError, "already exists"):
                benchmark.scaffold(metadata, manifest_path, root)

            self.assertEqual(manifest_path.read_text(encoding="utf-8"), raced_content)

    def _fixture(self, root: Path, recordings_per_split: int = 6, annotations_per_recording: int = 9):
        manifest = {"schema_version": 1, "recordings": []}
        baseline_results = {}
        candidate_results = {}
        for split in ("calibration", "evaluation"):
            for index in range(recordings_per_split):
                recording_id = f"{split}-{index}"
                terms = [f"용어{index}_{number}" for number in range(annotations_per_recording)]
                first_text = " ".join(terms) + " 정확"
                utterances = []
                for segment_index in range(10):
                    utterances.append(
                        {
                            "id": f"g{segment_index}",
                            "start_ms": segment_index * 1000,
                            "end_ms": (segment_index + 1) * 1000,
                            "text": first_text if segment_index == 0 else f"일반 문장 {segment_index}",
                        }
                    )
                manifest["recordings"].append(
                    {
                        "id": recording_id,
                        "split": split,
                        "environment": f"env-{index % 3}",
                        "speaker_configuration": "single" if index % 2 == 0 else "multi",
                        "audio_sha256": benchmark.hashlib.sha256(recording_id.encode()).hexdigest(),
                        "utterances": utterances,
                        "named_terms": [{"utterance_id": "g0", "term": term} for term in terms],
                        "required_phrases": [{"utterance_id": "g1", "text": "일반 문장"}],
                        "correction_targets": [
                            {
                                "id": f"target-{number}",
                                "utterance_id": "g0",
                                "start_byte": 0,
                                "end_byte": len(terms[0].encode("utf-8")),
                                "label": "replace",
                                "allowed_replacements": [terms[0]],
                            }
                            for number in range(annotations_per_recording)
                        ],
                    }
                )
                baseline_results[recording_id] = self._analysis(
                    manifest["recordings"][-1], first_text.replace("정확", "부정확")
                )
                candidate_results[recording_id] = self._analysis(manifest["recordings"][-1], first_text)

        manifest_path = root / "manifest.json"
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")
        manifest_hash = benchmark.canonical_hash(manifest)
        (root / "gold-signoff.json").write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "manifest_sha256": manifest_hash,
                    "recording_ids": sorted(item["id"] for item in manifest["recordings"]),
                    "human_verified": True,
                }
            ),
            encoding="utf-8",
        )
        calibration_hash = benchmark.canonical_hash(
            [item for item in manifest["recordings"] if item["split"] == "calibration"]
        )
        baseline_dir, candidate_dir = root / "baseline", root / "candidate"
        for run_dir, results in ((baseline_dir, baseline_results), (candidate_dir, candidate_results)):
            (run_dir / "recordings").mkdir(parents=True)
            for recording_id, result in results.items():
                (run_dir / "recordings" / f"{recording_id}.json").write_text(
                    json.dumps(result, ensure_ascii=False), encoding="utf-8"
                )

        fingerprints = {
            "binary_sha256": "a" * 64,
            "macos_build": "25F84",
            "locale": "ko-KR",
            "config_sha256": benchmark.canonical_hash(
                {
                    "locale": "ko-KR",
                    "result_mode": "strict",
                    "recordings": {
                        recording["id"]: {
                            "context_fingerprint": benchmark.hashlib.sha256(b"").hexdigest(),
                            "result_file": f"recordings/{recording['id']}.json",
                        }
                        for recording in manifest["recordings"]
                    },
                }
            ),
            "locale_model_state": "installed",
        }
        thresholds = {
            "candidate_error_recall_min": 0.8,
            "candidate_segment_ratio_max": 0.1,
            "candidate_duration_ratio_max": 0.2,
            "candidate_character_ratio_max": 1.0,
            "review_minutes_per_audio_hour_max": 10.0,
            "calibration_split_sha256": calibration_hash,
        }
        for run_dir in (baseline_dir, candidate_dir):
            per_recording = {}
            for recording in manifest["recordings"]:
                per_recording[recording["id"]] = {
                    "candidate_segment_ids": ["s0"],
                    "review_seconds": {"s0": 1},
                    "processing_seconds": 2,
                    "peak_memory_mb": 100,
                    "auto_applied_count": 0,
                    "wrong_approved_count": 0,
                    "residual_error_count": 0,
                    "context_fingerprint": benchmark.hashlib.sha256(b"").hexdigest(),
                    "result_sha256": benchmark._file_hash(
                        run_dir / "recordings" / f"{recording['id']}.json"
                    ),
                }
            (run_dir / "run.json").write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "result_mode": "strict",
                        "manifest_sha256": manifest_hash,
                        "fingerprints": fingerprints,
                        "frozen_thresholds": thresholds,
                        "recordings": per_recording,
                    }
                ),
                encoding="utf-8",
            )

        changed = [
            f"{recording['id']}:s0"
            for recording in manifest["recordings"]
            if recording["split"] == "evaluation"
        ]
        (candidate_dir / "signoff.json").write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "manifest_sha256": manifest_hash,
                    "baseline_bundle_sha256": benchmark._run_bundle_hash(baseline_dir, manifest["recordings"]),
                    "candidate_bundle_sha256": benchmark._run_bundle_hash(candidate_dir, manifest["recordings"]),
                    "changed_segment_ids": changed,
                    "alignment_issue_ids": [],
                }
            ),
            encoding="utf-8",
        )
        return manifest_path, baseline_dir, candidate_dir

    @staticmethod
    def _analysis(recording: dict, first_text: str) -> dict:
        segments = []
        for index, utterance in enumerate(recording["utterances"]):
            segments.append(
                {
                    "id": f"s{index}",
                    "start": utterance["start_ms"] / 1000,
                    "end": utterance["end_ms"] / 1000,
                    "text": first_text if index == 0 else utterance["text"],
                }
            )
        return {
            "schema_version": 1,
            "engine": "apple-speech-transcriber",
            "engine_version": "a" * 64,
            "locale": "ko-KR",
            "source": {"audio_sha256": recording["audio_sha256"], "duration_ms": 10_000},
            "context": {
                "fingerprint": benchmark.hashlib.sha256(b"").hexdigest(),
                "selected": [],
                "dropped": [],
            },
            "segments": segments,
        }

    @staticmethod
    def _rebind_run(run_dir: Path, recordings: list[dict]) -> None:
        run = json.loads((run_dir / "run.json").read_text(encoding="utf-8"))
        config_recordings = {}
        for recording in recordings:
            result_path = run_dir / "recordings" / f"{recording['id']}.json"
            result = json.loads(result_path.read_text(encoding="utf-8"))
            context_fingerprint = result["context"]["fingerprint"]
            run["recordings"][recording["id"]]["context_fingerprint"] = context_fingerprint
            run["recordings"][recording["id"]]["result_sha256"] = benchmark._file_hash(result_path)
            config_recordings[recording["id"]] = {
                "context_fingerprint": context_fingerprint,
                "result_file": f"recordings/{recording['id']}.json",
            }
        run["fingerprints"]["config_sha256"] = benchmark.canonical_hash(
            {
                "locale": run["fingerprints"]["locale"],
                "result_mode": run["result_mode"],
                "recordings": config_recordings,
            }
        )
        (run_dir / "run.json").write_text(json.dumps(run), encoding="utf-8")

    @staticmethod
    def _convert_run_to_legacy(
        run_dir: Path, recordings: list[dict], vocab_file_sha256: str
    ) -> None:
        profile = benchmark._vocab_input_profile(
            "Caret\n", vocab_file_sha256, vocab_file_sha256
        )
        adapter = {
            "name": "apple-stt-legacy-json",
            "version": 1,
            "source_flag": "--json",
            "duration_source": "max_segment_end",
            "strict_analysis_compatible": False,
            "script_sha256": benchmark._file_hash(SCRIPT),
            "vocab_input_profile": profile,
        }
        profile_hash = benchmark.canonical_hash(profile)
        run_path = run_dir / "run.json"
        run = json.loads(run_path.read_text(encoding="utf-8"))
        run["result_mode"] = "legacy"
        run["benchmark_adapter"] = adapter
        config_recordings = {}
        for recording in recordings:
            result_path = run_dir / "recordings" / f"{recording['id']}.json"
            result = json.loads(result_path.read_text(encoding="utf-8"))
            result.pop("context")
            result["benchmark_adapter"] = adapter
            result_path.write_text(json.dumps(result), encoding="utf-8")
            run_recording = run["recordings"][recording["id"]]
            run_recording.pop("context_fingerprint")
            run_recording["vocab_profile_sha256"] = profile_hash
            run_recording["result_sha256"] = benchmark._file_hash(result_path)
            config_recordings[recording["id"]] = {
                "result_file": f"recordings/{recording['id']}.json",
                "vocab_profile_sha256": profile_hash,
            }
        run["fingerprints"]["config_sha256"] = benchmark.canonical_hash(
            {
                "locale": run["fingerprints"]["locale"],
                "result_mode": "legacy",
                "recordings": config_recordings,
            }
        )
        run_path.write_text(json.dumps(run), encoding="utf-8")

    def test_legacy_run_rejects_adapter_from_different_evaluator_source(self):
        with tempfile.TemporaryDirectory() as temporary:
            manifest, _, candidate = self._fixture(Path(temporary).resolve())
            manifest_value = json.loads(manifest.read_text(encoding="utf-8"))
            recordings = manifest_value["recordings"]
            self._convert_run_to_legacy(candidate, recordings, "d" * 64)

            run_path = candidate / "run.json"
            run = json.loads(run_path.read_text(encoding="utf-8"))
            run["benchmark_adapter"]["script_sha256"] = "0" * 64
            for recording in recordings:
                result_path = candidate / "recordings" / f"{recording['id']}.json"
                result = json.loads(result_path.read_text(encoding="utf-8"))
                result["benchmark_adapter"]["script_sha256"] = "0" * 64
                result_path.write_text(json.dumps(result), encoding="utf-8")
                run["recordings"][recording["id"]]["result_sha256"] = benchmark._file_hash(
                    result_path
                )
            run_path.write_text(json.dumps(run), encoding="utf-8")

            with self.assertRaisesRegex(benchmark.BenchmarkError, "adapter provenance"):
                benchmark._load_run(
                    candidate, recordings, benchmark.canonical_hash(manifest_value)
                )

    @staticmethod
    def _rebind_signoff(manifest: Path, baseline: Path, candidate: Path) -> None:
        recordings = json.loads(manifest.read_text(encoding="utf-8"))["recordings"]
        signoff_path = candidate / "signoff.json"
        signoff = json.loads(signoff_path.read_text(encoding="utf-8"))
        signoff["baseline_bundle_sha256"] = benchmark._run_bundle_hash(baseline, recordings)
        signoff["candidate_bundle_sha256"] = benchmark._run_bundle_hash(candidate, recordings)
        signoff_path.write_text(json.dumps(signoff), encoding="utf-8")

    def test_strict_run_rejects_engine_locale_context_and_config_mismatch(self):
        for mismatch in ("engine", "locale", "context", "config"):
            with self.subTest(mismatch=mismatch), tempfile.TemporaryDirectory() as temporary:
                manifest, baseline, candidate = self._fixture(Path(temporary).resolve())
                manifest_value = json.loads(manifest.read_text(encoding="utf-8"))
                recording = manifest_value["recordings"][0]
                result_path = candidate / "recordings" / f"{recording['id']}.json"
                result = json.loads(result_path.read_text(encoding="utf-8"))
                run_path = candidate / "run.json"
                run = json.loads(run_path.read_text(encoding="utf-8"))
                if mismatch == "engine":
                    result["engine_version"] = "c" * 64
                elif mismatch == "locale":
                    result["locale"] = "en-US"
                elif mismatch == "context":
                    result["context"]["fingerprint"] = "d" * 64
                else:
                    run["fingerprints"]["config_sha256"] = "e" * 64
                result_path.write_text(json.dumps(result), encoding="utf-8")
                run["recordings"][recording["id"]]["result_sha256"] = benchmark._file_hash(result_path)
                run_path.write_text(json.dumps(run), encoding="utf-8")
                with self.assertRaises(benchmark.BenchmarkError):
                    benchmark.compare(manifest, baseline, candidate)

    def test_run_rejects_invalid_platform_fingerprints(self):
        invalid_values = (
            ("macos_build", ""),
            ("macos_build", None),
            ("locale_model_state", ""),
            ("locale_model_state", "downloaded"),
        )
        for key, value in invalid_values:
            with self.subTest(key=key, value=value), tempfile.TemporaryDirectory() as temporary:
                manifest, baseline, candidate = self._fixture(Path(temporary).resolve())
                run_path = candidate / "run.json"
                run = json.loads(run_path.read_text(encoding="utf-8"))
                run["fingerprints"][key] = value
                run_path.write_text(json.dumps(run), encoding="utf-8")
                with self.assertRaisesRegex(benchmark.BenchmarkError, "runtime fingerprints"):
                    benchmark.compare(manifest, baseline, candidate)

    def test_declared_run_mode_rejects_a_mixed_strict_and_legacy_bundle(self):
        with tempfile.TemporaryDirectory() as temporary:
            manifest, baseline, candidate = self._fixture(Path(temporary).resolve())
            recordings = json.loads(manifest.read_text(encoding="utf-8"))["recordings"]
            recording = recordings[0]
            result_path = candidate / "recordings" / f"{recording['id']}.json"
            result = json.loads(result_path.read_text(encoding="utf-8"))
            profile = benchmark._vocab_input_profile("Caret\n", "e" * 64, "e" * 64)
            result["benchmark_adapter"] = {
                "name": "apple-stt-legacy-json",
                "version": 1,
                "source_flag": "--json",
                "duration_source": "max_segment_end",
                "strict_analysis_compatible": False,
                "script_sha256": "f" * 64,
                "vocab_input_profile": profile,
            }
            result_path.write_text(json.dumps(result), encoding="utf-8")
            run_path = candidate / "run.json"
            run = json.loads(run_path.read_text(encoding="utf-8"))
            run["recordings"][recording["id"]]["result_sha256"] = benchmark._file_hash(
                result_path
            )
            run_path.write_text(json.dumps(run), encoding="utf-8")

            with self.assertRaisesRegex(benchmark.BenchmarkError, "result_mode"):
                benchmark.compare(manifest, baseline, candidate)

    def test_context_only_relation_is_explicit_and_not_required_for_binary_upgrade(self):
        with tempfile.TemporaryDirectory() as temporary:
            manifest, baseline, candidate = self._fixture(Path(temporary).resolve())
            command = [
                sys.executable,
                str(SCRIPT),
                "compare",
                "--manifest",
                str(manifest),
                "--baseline-dir",
                str(baseline),
                "--candidate-dir",
                str(candidate),
                "--expect-context-only-change",
                "--gate",
            ]
            unchanged = subprocess.run(command, text=True, capture_output=True, check=False)
            self.assertEqual(unchanged.returncode, 1, unchanged.stderr)

            recordings = json.loads(manifest.read_text(encoding="utf-8"))["recordings"]
            context_fingerprint = benchmark.hashlib.sha256(b"CommonTerm").hexdigest()
            for recording in recordings:
                path = candidate / "recordings" / f"{recording['id']}.json"
                result = json.loads(path.read_text(encoding="utf-8"))
                result["context"] = {
                    "fingerprint": context_fingerprint,
                    "selected": ["CommonTerm"],
                    "dropped": [],
                }
                path.write_text(json.dumps(result), encoding="utf-8")
            self._rebind_run(candidate, recordings)
            self._rebind_signoff(manifest, baseline, candidate)
            context_report = benchmark.compare(
                manifest, baseline, candidate, expect_context_only_change=True
            )
            self.assertEqual(context_report["status"], "pass")
            self.assertEqual(
                next(item for item in context_report["gates"] if item["name"] == "context_only_change")["status"],
                "pass",
            )

            run_path = candidate / "run.json"
            run = json.loads(run_path.read_text(encoding="utf-8"))
            run["fingerprints"]["binary_sha256"] = "c" * 64
            run_path.write_text(json.dumps(run), encoding="utf-8")
            for recording in recordings:
                path = candidate / "recordings" / f"{recording['id']}.json"
                result = json.loads(path.read_text(encoding="utf-8"))
                result["engine_version"] = "c" * 64
                path.write_text(json.dumps(result), encoding="utf-8")
            self._rebind_run(candidate, recordings)
            self._rebind_signoff(manifest, baseline, candidate)
            self.assertEqual(benchmark.compare(manifest, baseline, candidate)["status"], "pass")
            relation = benchmark.compare(
                manifest, baseline, candidate, expect_context_only_change=True
            )
            self.assertEqual(
                next(item for item in relation["gates"] if item["name"] == "context_only_change")["status"],
                "fail",
            )

    def test_context_only_relation_rejects_legacy_adapter_runs(self):
        with tempfile.TemporaryDirectory() as temporary:
            manifest, baseline, candidate = self._fixture(Path(temporary).resolve())
            recordings = json.loads(manifest.read_text(encoding="utf-8"))["recordings"]
            self._convert_run_to_legacy(baseline, recordings, "d" * 64)
            self._convert_run_to_legacy(candidate, recordings, "e" * 64)
            self._rebind_signoff(manifest, baseline, candidate)

            self.assertEqual(benchmark.compare(manifest, baseline, candidate)["status"], "pass")
            relation = benchmark.compare(
                manifest, baseline, candidate, expect_context_only_change=True
            )
            self.assertEqual(
                next(
                    item
                    for item in relation["gates"]
                    if item["name"] == "context_only_change"
                )["status"],
                "fail",
            )

    def test_release_gate_passes_and_writes_redacted_reports(self):
        with tempfile.TemporaryDirectory() as temporary:
            manifest, baseline, candidate = self._fixture(Path(temporary).resolve())
            completed = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "compare",
                    "--manifest",
                    str(manifest),
                    "--baseline-dir",
                    str(baseline),
                    "--candidate-dir",
                    str(candidate),
                    "--gate",
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertNotIn(str(manifest.parent), completed.stdout)
            self.assertEqual(json.loads(completed.stdout)["profile"], "full")
            report = json.loads((candidate / "report.json").read_text(encoding="utf-8"))
            self.assertEqual(report["status"], "pass")
            self.assertLess(report["evaluation_deltas"]["content_cer"]["value"], 0)
            self.assertEqual(report["metrics"]["evaluation"]["candidate"]["denominators"]["error_targets"], 54)
            self.assertEqual(
                report["signoff_binding"]["candidate_bundle_sha256"],
                benchmark._run_bundle_hash(candidate, json.loads(manifest.read_text(encoding="utf-8"))["recordings"]),
            )
            report_text = (candidate / "report.md").read_text(encoding="utf-8")
            self.assertNotIn("용어", report_text)

    def test_missing_denominators_is_insufficient_and_gate_is_nonzero(self):
        with tempfile.TemporaryDirectory() as temporary:
            manifest, baseline, candidate = self._fixture(Path(temporary).resolve(), 1, 1)
            completed = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "compare",
                    "--manifest",
                    str(manifest),
                    "--baseline-dir",
                    str(baseline),
                    "--candidate-dir",
                    str(candidate),
                    "--gate",
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(completed.returncode, 1, completed.stderr)
            report = json.loads((candidate / "report.json").read_text(encoding="utf-8"))
            self.assertEqual(report["status"], "insufficient_data")
            error_gate = next(item for item in report["gates"] if item["name"] == "evaluation_error_targets")
            self.assertEqual(error_gate["status"], "insufficient_data")

    def test_gold_requires_explicit_human_signoff_bound_to_manifest(self):
        with tempfile.TemporaryDirectory() as temporary:
            manifest, baseline, candidate = self._fixture(Path(temporary).resolve())
            manifest.with_name("gold-signoff.json").unlink()
            report = benchmark.compare(manifest, baseline, candidate)
            self.assertNotEqual(report["status"], "pass")
            gold_gate = next(item for item in report["gates"] if item["name"] == "human_gold_signoff")
            self.assertEqual(gold_gate["status"], "insufficient_data")

    def test_transcription_profile_does_not_require_review_selector_thresholds(self):
        with tempfile.TemporaryDirectory() as temporary:
            manifest, baseline, candidate = self._fixture(Path(temporary).resolve())
            manifest_value = json.loads(manifest.read_text(encoding="utf-8"))
            for recording in manifest_value["recordings"]:
                recording["correction_targets"] = []
            manifest.write_text(json.dumps(manifest_value), encoding="utf-8")
            manifest_hash = benchmark.canonical_hash(manifest_value)
            for directory in (baseline, candidate):
                run = json.loads((directory / "run.json").read_text(encoding="utf-8"))
                run["manifest_sha256"] = manifest_hash
                if directory == candidate:
                    run.pop("frozen_thresholds")
                (directory / "run.json").write_text(json.dumps(run), encoding="utf-8")
            manifest.with_name("gold-signoff.json").write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "manifest_sha256": manifest_hash,
                        "recording_ids": sorted(item["id"] for item in manifest_value["recordings"]),
                        "human_verified": True,
                    }
                ),
                encoding="utf-8",
            )
            signoff = json.loads((candidate / "signoff.json").read_text(encoding="utf-8"))
            signoff["manifest_sha256"] = manifest_hash
            signoff["baseline_bundle_sha256"] = benchmark._run_bundle_hash(baseline, manifest_value["recordings"])
            signoff["candidate_bundle_sha256"] = benchmark._run_bundle_hash(candidate, manifest_value["recordings"])
            (candidate / "signoff.json").write_text(json.dumps(signoff), encoding="utf-8")

            full = benchmark.compare(manifest, baseline, candidate)
            transcription = benchmark.compare(manifest, baseline, candidate, profile="transcription")
            self.assertEqual(full["status"], "insufficient_data")
            self.assertEqual(transcription["status"], "pass")
            self.assertEqual(transcription["profile"], "transcription")
            self.assertNotIn("candidate_error_recall", {item["name"] for item in transcription["gates"]})

    def test_auto_apply_and_missing_signoff_fail_gate(self):
        with tempfile.TemporaryDirectory() as temporary:
            manifest, baseline, candidate = self._fixture(Path(temporary).resolve())
            run = json.loads((candidate / "run.json").read_text(encoding="utf-8"))
            evaluation_id = next(key for key in run["recordings"] if key.startswith("evaluation"))
            run["recordings"][evaluation_id]["auto_applied_count"] = 1
            (candidate / "run.json").write_text(json.dumps(run), encoding="utf-8")
            (candidate / "signoff.json").write_text(
                json.dumps({"schema_version": 1, "changed_segment_ids": [], "alignment_issue_ids": []}),
                encoding="utf-8",
            )
            report = benchmark.compare(manifest, baseline, candidate)
            self.assertEqual(report["status"], "fail")
            statuses = {item["name"]: item["status"] for item in report["gates"]}
            self.assertEqual(statuses["zero_auto_applied"], "fail")
            self.assertEqual(statuses["signoff_bundle"], "fail")
            self.assertEqual(statuses["changed_segment_signoff"], "fail")

    def test_requested_claude_gate_uses_validated_non_abstaining_denominator(self):
        with tempfile.TemporaryDirectory() as temporary:
            manifest, baseline, candidate = self._fixture(Path(temporary).resolve())
            run = json.loads((candidate / "run.json").read_text(encoding="utf-8"))
            run["requested_features"] = ["claude_suggestions"]
            run["claude_fingerprints"] = {
                "model_id": "test-model",
                "cli_version": "test",
                "sdk_version": "test",
                "uv_lock_sha256": "c" * 64,
                "prompt_sha256": "d" * 64,
                "schema_sha256": "e" * 64,
                "batch_size": 20,
                "retry_count": 1,
                "client_mode": "fake",
            }
            for recording_id, metadata in run["recordings"].items():
                if recording_id.startswith("evaluation-"):
                    index = int(recording_id.rsplit("-", 1)[1])
                    metadata["suggestions"] = [
                        {
                            "status": "suggested",
                            "target_id": f"target-{number % 9}",
                            "replacement": f"용어{index}_0",
                            "alignment": "aligned",
                            "approved": False,
                        }
                        for number in range(5)
                    ]
            (candidate / "run.json").write_text(json.dumps(run), encoding="utf-8")
            signoff = json.loads((candidate / "signoff.json").read_text(encoding="utf-8"))
            manifest_value = json.loads(manifest.read_text(encoding="utf-8"))
            signoff["candidate_bundle_sha256"] = benchmark._run_bundle_hash(
                candidate, manifest_value["recordings"]
            )
            (candidate / "signoff.json").write_text(json.dumps(signoff), encoding="utf-8")
            report = benchmark.compare(manifest, baseline, candidate)
            self.assertEqual(report["status"], "pass")
            claude = report["metrics"]["evaluation"]["candidate"]["claude_suggestions"]
            self.assertEqual(claude["valid_non_abstaining"], 30)
            self.assertEqual(claude["precision"]["value"], 1.0)


if __name__ == "__main__":
    unittest.main()
