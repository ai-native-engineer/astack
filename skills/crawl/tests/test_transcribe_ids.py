#!/usr/bin/env python3
"""Offline fixtures for crawl's lossless caption orchestration (no yt-dlp)."""

import importlib.util
import io
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import tempfile
import textwrap
import unittest
from unittest.mock import Mock, patch


SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
CAPTIONS = SCRIPTS / "captions.py"
if not CAPTIONS.is_file():
    CAPTIONS = SCRIPTS.parent.parent / "youtube" / "scripts" / "captions.py"
SPEC = importlib.util.spec_from_file_location("transcribe_ids", SCRIPTS / "transcribe_ids.py")
transcribe_ids = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(transcribe_ids)
CHANNEL_SPEC = importlib.util.spec_from_file_location("crawl_channels", SCRIPTS / "youtube-channels.py")
channels = importlib.util.module_from_spec(CHANNEL_SPEC)
CHANNEL_SPEC.loader.exec_module(channels)
RUN_PROCESS = subprocess.run
VIDEO = "abcdefghijk"
OTHER = "ZYXwvut987_"


class TranscriptTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="crawl fixtures ")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        self.helpers = self.root / "helpers with spaces"
        self.helpers.mkdir()
        self.destination = self.root / "reports with spaces"
        self.actions = self.helpers / "actions.json"
        self.history = self.helpers / "history.txt"
        self.converter_mode = self.helpers / "converter-mode.txt"
        self.converter_mode.write_text("success", encoding="utf-8")
        self.set_actions("success")
        self.make_helpers()
        self.run = Mock(side_effect=self.run_fixture)
        self.sleep = Mock()

    def make_helpers(self):
        # Use the actual shared validator/renderer: never duplicate caption parsing.
        converter = textwrap.dedent('''\
            import importlib.util
            from pathlib import Path
            spec = importlib.util.spec_from_file_location("fixture_shared_captions", __SHARED__)
            shared = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(shared)

            def load_document(path):
                return shared.load_document(path)

            def markdown(document):
                mode = Path(__file__).with_name("converter-mode.txt").read_text(encoding="utf-8")
                if mode == "error":
                    raise ValueError("fixture converter failed")
                if mode == "empty":
                    return ""
                return shared.markdown(document)
        ''').replace("__SHARED__", repr(str(CAPTIONS)))
        (self.helpers / "captions.py").write_text(converter, encoding="utf-8")
        fetch = textwrap.dedent('''\
            #!/bin/bash
            exec __PYTHON__ - "$@" <<'PY'
            import json
            from pathlib import Path
            import sys

            fixtures = Path(__FIXTURES__)
            actions_path = fixtures / "actions.json"
            actions = json.loads(actions_path.read_text(encoding="utf-8"))
            if not actions:
                print("unexpected fixture acquisition", file=sys.stderr)
                sys.exit(99)
            action = actions.pop(0)
            actions_path.write_text(json.dumps(actions, ensure_ascii=False), encoding="utf-8")
            video = sys.argv[1].split("v=", 1)[1]
            output = Path(sys.argv[2])
            with (fixtures / "history.txt").open("a", encoding="utf-8") as history:
                history.write(video + "\\n")
            mode = action.get("mode", "success")
            if mode == "absent":
                print("no captions: confirmed absence", file=sys.stderr)
                sys.exit(2)
            if mode == "rate_limit":
                print("HTTP 429 rate limit; wait before retrying", file=sys.stderr)
                sys.exit(3)
            if mode == "failure":
                print("unsupported caption language; check configured tracks", file=sys.stderr)
                sys.exit(3)
            if mode == "unclassified":
                print("acquisition failed; check installation", file=sys.stderr)
                sys.exit(3)
            if mode == "mixed_failure":
                print("HTTP 429; another client reported malformed metadata", file=sys.stderr)
                sys.exit(3)
            if mode == "unexpected_status":
                print("fixture acquisition stopped", file=sys.stderr)
                sys.exit(7)
            language = action.get("language", "ko")
            kind = action.get("kind", "manual")
            text = action.get("text", "Hi.")
            srt = output / (video + "." + language + ".srt")
            srt.write_text("1\\n00:00:01,000 --> 00:00:02,000\\n" + text + "\\n", encoding="utf-8")
            metadata = {"id": video, "title": action.get("title", "작은 자막"), "upload_date": "20261026"}
            metadata_path = output / (video + ".metadata.json")
            metadata_path.write_text(json.dumps(metadata, ensure_ascii=False), encoding="utf-8")
            document = {
                "video_id": video, "language": language, "kind": kind,
                "source": {"format": "srt", "path": srt.name, "client": "fixture"},
                "metadata": metadata, "cues": [{"start": 1, "end": 2, "text": text}],
            }
            if mode == "zero_cues":
                document["cues"] = []
            if mode == "wrong_id":
                document["video_id"] = "ZZZZZZZZZZZ"
            path = output / (video + ".captions.json")
            payload = "{broken" if mode == "malformed" else json.dumps(document, ensure_ascii=False, separators=(",", ":"))
            path.write_text(payload, encoding="utf-8")
            if mode == "missing_json":
                path.unlink()
            if mode == "missing_source":
                srt.unlink()
            if mode == "missing_metadata":
                metadata_path.unlink()
            if mode == "mismatched_metadata":
                metadata_path.write_text("{}", encoding="utf-8")
            print("VIDEO_ID=" + video)
            print("TITLE=" + action.get("stdout_title", "fixture title"))
            print("SUB_LANG=" + language)
            print("KIND=" + kind)
            print("CLIENT=fixture")
            print("SRT_PATH=" + str(srt))
            print("CAPTIONS_PATH=" + str(path))
            print("METADATA_PATH=" + str(metadata_path))
            PY
        ''').replace("__PYTHON__", shlex.quote(sys.executable)).replace("__FIXTURES__", repr(str(self.helpers)))
        (self.helpers / "fetch-subs.sh").write_text(fetch, encoding="utf-8")

    def set_actions(self, *actions):
        self.actions.write_text(json.dumps([
            {"mode": action} if isinstance(action, str) else action for action in actions
        ], ensure_ascii=False), encoding="utf-8")

    def run_fixture(self, command, **kwargs):
        self.assertEqual(command[0:2], ["bash", str(self.helpers / "fetch-subs.sh")])
        self.assertEqual(kwargs["stdin"], subprocess.DEVNULL)
        # Only the local fixture may execute; subprocess.run itself is mocked.
        return RUN_PROCESS(command, **kwargs)

    def batch(self, ids=VIDEO + "\n", *, force=False, environ=None, script_dir=None):
        stdout, stderr = io.StringIO(), io.StringIO()
        with patch.object(transcribe_ids.subprocess, "run", side_effect=AssertionError("uninjected subprocess")), patch.object(
            transcribe_ids.time, "sleep", side_effect=AssertionError("real sleep is forbidden"),
        ):
            status = transcribe_ids.transcribe(
                io.StringIO(ids), self.destination, force,
                run=self.run, sleep=self.sleep,
                environ={"YOUTUBE_SCRIPTS": str(self.helpers)} if environ is None else environ,
                script_dir=script_dir, stdout=stdout, stderr=stderr,
            )
        return status, stdout.getvalue(), stderr.getvalue()

    def report(self, video=VIDEO):
        return self.destination / f"{video}.md"

    def video_dir(self, video=VIDEO):
        return self.destination / "transcripts" / video

    def receipt(self, video=VIDEO):
        return json.loads((self.video_dir(video) / "success.json").read_text(encoding="utf-8"))

    def caption_path(self, video=VIDEO):
        return self.video_dir(video) / self.receipt(video)["captions_path"]

    def test_small_captions_keep_selected_kind_metadata_and_raw_files(self):
        for kind, language in (("manual", "ko"), ("auto", "en")):
            with self.subTest(kind=kind):
                self.set_actions({"kind": kind, "language": language})
                status, output, errors = self.batch(force=True)
                self.assertEqual((status, errors), (0, ""))
                self.assertIn("success=1 skip=0 no_captions=0 failure=0", output)
                path = self.caption_path()
                document = json.loads(path.read_text(encoding="utf-8"))
                source = path.parent / document["source"]["path"]
                self.assertTrue(source.is_file())
                self.assertLess(source.stat().st_size, 500)
                self.assertLess(path.stat().st_size, 500)
                self.assertEqual(document["kind"], kind)
                self.assertEqual(document["language"], language)
                self.assertEqual(
                    document["metadata"],
                    json.loads((path.parent / f"{VIDEO}.metadata.json").read_text(encoding="utf-8")),
                )
                markdown = self.report().read_text(encoding="utf-8")
                self.assertIn(f'caption_kind: "{kind}"', markdown)
                self.assertIn(f'lang: "{language}"', markdown)
                self.assertIn(r"Hi\.", markdown)
                self.assertIn("작은 자막", markdown)
                self.assertEqual(list(self.destination.glob("*.md")), [self.report()])

    def test_second_successful_run_skips_only_matching_receipt(self):
        self.assertEqual(self.batch()[0], 0)
        report = self.report().read_bytes()
        status, output, errors = self.batch()
        self.assertEqual((status, errors), (0, ""))
        self.assertIn("success=0 skip=1 no_captions=0 failure=0", output)
        self.assertEqual(self.report().read_bytes(), report)
        self.assertEqual(self.run.call_count, 1)
        self.sleep.assert_not_called()

    def test_modified_report_is_not_a_success_cache(self):
        self.assertEqual(self.batch()[0], 0)
        self.report().write_text("not a successful transcript", encoding="utf-8")
        self.set_actions("success")
        self.assertIn("success=1 skip=0", self.batch()[1])
        self.assertEqual(self.run.call_count, 2)

    def test_modified_valid_json_is_not_a_success_cache(self):
        self.assertEqual(self.batch()[0], 0)
        path = self.caption_path()
        document = json.loads(path.read_text(encoding="utf-8"))
        document["cues"][0]["text"] = "Changed caption"
        path.write_text(json.dumps(document, ensure_ascii=False), encoding="utf-8")
        self.set_actions("success")
        self.assertIn("success=1 skip=0", self.batch()[1])
        self.assertEqual(self.run.call_count, 2)

    def test_matching_hash_does_not_bypass_shared_json_validation(self):
        self.assertEqual(self.batch()[0], 0)
        path = self.caption_path()
        document = json.loads(path.read_text(encoding="utf-8"))
        document["cues"] = []
        path.write_text(json.dumps(document, ensure_ascii=False), encoding="utf-8")
        receipt_path = self.video_dir() / "success.json"
        receipt = self.receipt()
        receipt["captions_sha256"] = transcribe_ids.digest(path.read_bytes())
        receipt_path.write_text(json.dumps(receipt), encoding="utf-8")
        self.set_actions("success")
        self.assertIn("success=1 skip=0", self.batch()[1])
        self.assertEqual(self.run.call_count, 2)

    def test_missing_retained_source_invalidates_cache(self):
        self.assertEqual(self.batch()[0], 0)
        path = self.caption_path()
        document = json.loads(path.read_text(encoding="utf-8"))
        (path.parent / document["source"]["path"]).unlink()
        self.set_actions("success")
        self.assertIn("success=1 skip=0", self.batch()[1])
        self.assertEqual(self.run.call_count, 2)

    def test_existing_markdown_alone_is_not_success(self):
        self.destination.mkdir()
        self.report().write_text("# Previous transcript\n\nSpeech.\n", encoding="utf-8")
        status, output, _ = self.batch()
        self.assertEqual(status, 0)
        self.assertIn("success=1 skip=0", output)
        self.assertEqual(self.run.call_count, 1)

    def test_no_captions_stub_is_rechecked_then_success_can_be_cached(self):
        self.set_actions("absent", "success")
        status, output, errors = self.batch()
        self.assertEqual(status, 0)
        self.assertIn("success=0 skip=0 no_captions=1 failure=0", output)
        self.assertIn("confirmed absence", errors)
        self.assertIn('transcript_status: "no_captions"', self.report().read_text(encoding="utf-8"))
        self.assertFalse((self.video_dir() / "success.json").exists())
        self.assertIn("success=1 skip=0 no_captions=0 failure=0", self.batch()[1])
        self.assertIn("success=0 skip=1 no_captions=0 failure=0", self.batch()[1])
        self.assertEqual(self.run.call_count, 2)

    def test_rate_limit_is_failure_with_one_retry_not_no_captions(self):
        self.set_actions("rate_limit", "rate_limit")
        status, output, errors = self.batch()
        self.assertEqual(status, 1)
        self.assertIn("success=0 skip=0 no_captions=0 failure=1", output)
        self.assertEqual(errors.count("HTTP 429"), 2)
        self.assertIn("retrying once", errors)
        self.assertFalse(self.report().exists())
        self.assertEqual(self.run.call_count, 2)
        self.sleep.assert_called_once_with(4)

    def test_transient_retry_can_succeed_and_preserves_diagnostics(self):
        self.set_actions("rate_limit", "success")
        status, output, errors = self.batch()
        self.assertEqual(status, 0)
        self.assertIn("success=1 skip=0 no_captions=0 failure=0", output)
        self.assertIn("HTTP 429", errors)
        self.assertEqual(self.run.call_count, 2)
        self.sleep.assert_called_once_with(4)
        self.assertEqual(len(list(self.video_dir().glob("attempt-*"))), 2)

    def test_unclassified_or_permanent_failure_does_not_retry(self):
        for mode in ("failure", "unclassified", "mixed_failure", "unexpected_status"):
            with self.subTest(mode=mode):
                self.set_actions(mode)
                self.run.reset_mock()
                self.sleep.reset_mock()
                status, output, errors = self.batch()
                self.assertEqual(status, 1)
                self.assertIn("no_captions=0 failure=1", output)
                self.assertIn("failure " + VIDEO, errors)
                self.assertEqual(self.run.call_count, 1)
                self.sleep.assert_not_called()
                self.assertFalse(self.report().exists())

    def test_invalid_acquired_documents_do_not_retry_or_create_stubs(self):
        for mode in ("malformed", "zero_cues", "wrong_id", "missing_json", "missing_source", "missing_metadata", "mismatched_metadata"):
            with self.subTest(mode=mode):
                self.set_actions(mode)
                self.run.reset_mock()
                self.sleep.reset_mock()
                before = set(self.video_dir().glob("attempt-*"))
                status, output, errors = self.batch()
                self.assertEqual(status, 1)
                self.assertIn("success=0 skip=0 no_captions=0 failure=1", output)
                self.assertIn("Inspect retained files", errors)
                self.assertFalse(self.report().exists())
                self.assertFalse((self.video_dir() / "success.json").exists())
                self.assertEqual(self.run.call_count, 1)
                self.sleep.assert_not_called()
                created = set(self.video_dir().glob("attempt-*")) - before
                self.assertEqual(len(created), 1)
                attempt = created.pop()
                self.assertEqual((attempt / f"{VIDEO}.captions.json").exists(), mode != "missing_json")
                self.assertEqual((attempt / f"{VIDEO}.metadata.json").exists(), mode != "missing_metadata")
                self.assertEqual((attempt / f"{VIDEO}.ko.srt").exists(), mode != "missing_source")

    def test_converter_failure_or_empty_output_is_error_without_retry(self):
        for mode in ("error", "empty"):
            with self.subTest(mode=mode):
                self.converter_mode.write_text(mode, encoding="utf-8")
                self.set_actions("success")
                self.run.reset_mock()
                status, output, errors = self.batch()
                self.assertEqual(status, 1)
                self.assertIn("no_captions=0 failure=1", output)
                self.assertIn("converter", errors)
                self.assertFalse(self.report().exists())
                self.assertEqual(self.run.call_count, 1)
                self.sleep.assert_not_called()
                self.assertTrue(list(self.video_dir().glob(f"attempt-*/{VIDEO}.captions.json")))
                self.assertTrue(list(self.video_dir().glob(f"attempt-*/{VIDEO}.ko.srt")))

    def test_failed_force_keeps_successful_report_and_retries_next_run(self):
        for mode in ("failure", "malformed", "missing_json"):
            with self.subTest(mode=mode):
                self.set_actions("success")
                self.assertEqual(self.batch(force=True)[0], 0)
                report = self.report().read_bytes()
                path = self.caption_path()
                source = path.parent / json.loads(path.read_text(encoding="utf-8"))["source"]["path"]
                originals = {file: file.read_bytes() for file in (path, source, path.parent / f"{VIDEO}.metadata.json")}
                self.set_actions(mode)
                status, output, errors = self.batch(force=True)
                self.assertEqual(status, 1)
                self.assertIn("success=0 skip=0 no_captions=0 failure=1", output)
                self.assertIn("prior report retained", errors)
                self.assertEqual(self.report().read_bytes(), report)
                self.assertFalse((self.video_dir() / "success.json").exists())
                for file, data in originals.items():
                    self.assertEqual(file.read_bytes(), data)
                self.set_actions("success")
                self.assertIn("success=1 skip=0", self.batch()[1])

    def test_forced_conversion_failure_keeps_prior_report(self):
        self.assertEqual(self.batch()[0], 0)
        report = self.report().read_bytes()
        self.converter_mode.write_text("error", encoding="utf-8")
        self.set_actions("success")
        status, output, errors = self.batch(force=True)
        self.assertEqual(status, 1)
        self.assertIn("success=0 skip=0 no_captions=0 failure=1", output)
        self.assertIn("fixture converter failed", errors)
        self.assertEqual(self.report().read_bytes(), report)

    def test_confirmed_absence_keeps_prior_success_but_is_not_success(self):
        self.assertEqual(self.batch()[0], 0)
        report = self.report().read_bytes()
        path = self.caption_path()
        self.set_actions("absent", "success")
        status, output, _ = self.batch(force=True)
        self.assertEqual(status, 0)
        self.assertIn("success=0 skip=0 no_captions=1 failure=0", output)
        self.assertIn("existing report retained; not a current success", output)
        self.assertEqual(self.report().read_bytes(), report)
        self.assertTrue(path.is_file())
        self.assertIn("success=1 skip=0", self.batch()[1])

    def test_unknown_prior_report_is_retained_without_claiming_success(self):
        self.destination.mkdir()
        self.report().write_text("# Prior report without a receipt\n", encoding="utf-8")
        report = self.report().read_bytes()
        self.set_actions("absent")
        status, output, _ = self.batch()
        self.assertEqual(status, 0)
        self.assertIn("success=0 skip=0 no_captions=1 failure=0", output)
        self.assertEqual(self.report().read_bytes(), report)

    def test_publish_failure_preserves_prior_report_without_receipt(self):
        self.assertEqual(self.batch()[0], 0)
        report = self.report().read_bytes()
        write = transcribe_ids.atomic_write

        def fail_report(path, data):
            if path == self.report():
                raise OSError("fixture disk write failure")
            return write(path, data)

        self.set_actions("success")
        with patch.object(transcribe_ids, "atomic_write", side_effect=fail_report):
            status, output, errors = self.batch(force=True)
        self.assertEqual(status, 1)
        self.assertIn("success=0 skip=0 no_captions=0 failure=1", output)
        self.assertIn("disk write failure", errors)
        self.assertEqual(self.report().read_bytes(), report)
        self.assertFalse((self.video_dir() / "success.json").exists())

    def test_invalid_override_never_falls_back_to_valid_bundled_pair(self):
        for value in (str(self.root / "not present"), "", str(self.helpers / "captions.py")):
            with self.subTest(value=value):
                status, output, errors = self.batch(
                    environ={"YOUTUBE_SCRIPTS": value}, script_dir=self.helpers,
                )
                self.assertEqual(status, 1)
                self.assertIn("failure=1", output)
                self.assertIn("YOUTUBE_SCRIPTS", errors)
                self.run.assert_not_called()

    def test_helper_resolution_precedence_and_incomplete_bundle_failure(self):
        script_dir = self.root / "shared" / "crawl" / "scripts"
        canonical = self.root / "shared" / "youtube" / "scripts"
        script_dir.mkdir(parents=True)
        canonical.mkdir(parents=True)
        for name in transcribe_ids.HELPERS:
            (canonical / name).write_text("# fixture\n", encoding="utf-8")
        self.assertEqual(transcribe_ids.resolve_helpers(script_dir, {}), canonical)
        (script_dir / "fetch-subs.sh").write_text("# fixture\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "helpers missing"):
            transcribe_ids.resolve_helpers(script_dir, {})
        (script_dir / "captions.py").write_text("# fixture\n", encoding="utf-8")
        self.assertEqual(transcribe_ids.resolve_helpers(script_dir, {}), script_dir)
        self.assertEqual(
            transcribe_ids.resolve_helpers(script_dir, {"YOUTUBE_SCRIPTS": str(self.helpers)}),
            self.helpers,
        )

    def test_id_validation_is_anchored_and_deduplication_is_stable(self):
        self.set_actions("success", "success")
        ids = f"{OTHER}\n{VIDEO}\n{OTHER}\nhttps://youtu.be/{VIDEO}\nprefix{VIDEO}\n {VIDEO}\n{VIDEO} \n\n"
        status, output, errors = self.batch(ids)
        self.assertEqual(status, 1)
        self.assertIn("success=2 skip=0 no_captions=0 failure=4", output)
        self.assertEqual(self.history.read_text(encoding="utf-8").splitlines(), [OTHER, VIDEO])
        self.assertEqual(errors.count("expected exactly one 11-character"), 4)
        self.assertNotIn("https://", errors)
        self.sleep.assert_called_once_with(4)

    def test_empty_input_does_not_resolve_helpers_or_sleep(self):
        status, output, errors = self.batch("\n", environ={"YOUTUBE_SCRIPTS": ""})
        self.assertEqual((status, errors), (0, ""))
        self.assertEqual(output.strip(), "success=0 skip=0 no_captions=0 failure=0")
        self.run.assert_not_called()
        self.sleep.assert_not_called()

    def test_failure_does_not_stop_later_videos_and_batch_still_fails(self):
        self.set_actions("failure", "success")
        status, output, errors = self.batch(f"{VIDEO}\n{OTHER}\n")
        self.assertEqual(status, 1)
        self.assertIn("success=1 skip=0 no_captions=0 failure=1", output)
        self.assertIn("unsupported caption language", errors)
        self.assertFalse(self.report().exists())
        self.assertTrue(self.report(OTHER).exists())
        self.sleep.assert_called_once_with(4)

    def test_helper_stdout_is_neither_evaluated_nor_printed(self):
        marker = self.root / "must not exist"
        title = "$(touch " + shlex.quote(str(marker)) + "); not-for-output"
        self.set_actions({"stdout_title": title})
        status, output, errors = self.batch()
        self.assertEqual(status, 0)
        self.assertNotIn(title, output + errors)
        self.assertNotIn("not-for-output", output + errors)
        self.assertFalse(marker.exists())

    def test_shell_entrypoint_retains_raw_artifacts_after_process_exit(self):
        # One video: no retry or inter-video wait, even in the separate process.
        for name in ("transcribe-ids.sh", "transcribe_ids.py"):
            shutil.copyfile(SCRIPTS / name, self.helpers / name)
        environment = dict(os.environ, YOUTUBE_SCRIPTS=str(self.helpers))
        result = RUN_PROCESS(
            ["bash", str(self.helpers / "transcribe-ids.sh"), str(self.destination)],
            input=VIDEO + "\n", capture_output=True, text=True, env=environment,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("success=1", result.stdout)
        path = self.caption_path()
        document = json.loads(path.read_text(encoding="utf-8"))
        self.assertTrue((path.parent / document["source"]["path"]).is_file())
        self.assertTrue((path.parent / f"{VIDEO}.metadata.json").is_file())
        self.assertTrue(self.report().is_file())

    def test_channel_render_retains_short_success_and_explicit_absence(self):
        self.assertEqual(self.batch()[0], 0)
        meta = channels.parse_cache(str(self.report()))
        self.assertEqual(meta["transcript_status"], "success")
        self.assertLess(len(meta["transcript"]), 40)
        page = self.root / "page.md"
        channels.render_page(VIDEO, "fixture", meta, str(page))
        text = page.read_text(encoding="utf-8")
        self.assertIn("<details>", text)
        self.assertIn(r"Hi\.", text)
        self.assertIn('captions: "ko"', text)
        channels.render_page(VIDEO, "fixture", {
            "transcript_status": "no_captions", "transcript": "not a caption " * 10,
        }, str(page))
        self.assertNotIn("<details>", page.read_text(encoding="utf-8"))

    def test_channel_parser_decodes_shared_json_frontmatter_strings(self):
        title = 'A "quoted" title with a \\ path'
        self.set_actions({"title": title})
        self.assertEqual(self.batch()[0], 0)
        meta = channels.parse_cache(str(self.report()))
        self.assertEqual(meta["title"], title)
        self.assertEqual(meta["date"], "2026-10-26")
        self.assertEqual(meta["youtube_id"], VIDEO)

    def test_channel_frontmatter_and_body_keep_untrusted_titles_literal(self):
        title = 'C:\\Users\\Aiden "quoted" </summary><img src=x onerror=alert(1)>'
        self.set_actions({"title": title, "text": "첫 줄\n2026"})
        self.assertEqual(self.batch()[0], 0)
        meta = channels.parse_cache(str(self.report()))
        page = self.root / "safe page.md"
        channels.render_page(VIDEO, "fixture", meta, str(page))
        text = page.read_text(encoding="utf-8")
        line = next(line for line in text.splitlines() if line.startswith("title: "))
        self.assertEqual(json.loads(line.partition(": ")[2]), title)
        body = text.split("\n---\n", 1)[1]
        self.assertNotIn("<img", body)
        self.assertEqual(body.count("</summary>"), 1)
        self.assertIn("&lt;img", body)

    def test_emitted_caption_path_cannot_escape_current_attempt(self):
        real_run = self.run_fixture

        def forged(command, **kwargs):
            result = real_run(command, **kwargs)
            output = Path(command[-1])
            result.stdout = result.stdout.replace(str(output / f"{VIDEO}.captions.json"),
                                                  str(self.root / f"{VIDEO}.captions.json"))
            return result

        self.run.side_effect = forged
        status, output, _ = self.batch()
        self.assertEqual(status, 1)
        self.assertIn("failure=1", output)
        self.assertFalse(self.report().exists())

    def test_date_backfill_does_not_mutate_checksummed_success_report(self):
        self.assertEqual(self.batch()[0], 0)
        report = self.report().read_bytes()
        meta = {"transcript_status": "success", "youtube_id": VIDEO}
        response = subprocess.CompletedProcess([], 0, stdout="20261026\n", stderr="")
        with patch.object(channels.subprocess, "run", return_value=response):
            channels.backfill_date(VIDEO, meta, str(self.report()))
        self.assertEqual(meta["date"], "2026-10-26")
        self.assertEqual(self.report().read_bytes(), report)
        self.assertIn("skip=1", self.batch()[1])

    def test_channel_transcribe_keeps_shell_interface_and_failure_status(self):
        response = subprocess.CompletedProcess([], 1)
        with patch.object(channels.subprocess, "run", return_value=response) as run, patch.object(
            channels.sys, "stderr", io.StringIO(),
        ):
            status = channels.transcribe([VIDEO], str(self.destination), force=True)
        self.assertEqual(status, 1)
        run.assert_called_once_with(
            ["bash", str(SCRIPTS / "transcribe-ids.sh"), str(self.destination), "--force"],
            input=VIDEO + "\n", text=True,
        )

    def test_channel_main_propagates_partial_transcription_failure(self):
        argv = [str(SCRIPTS / "youtube-channels.py"), str(self.destination), "fixture:channel"]
        with patch.object(channels.sys, "argv", argv), patch.object(
            channels, "enumerate_channel", return_value=[(VIDEO, "Example")],
        ), patch.object(channels, "transcribe", return_value=1), patch.object(channels.sys, "stdout", io.StringIO()):
            self.assertEqual(channels.main(), 1)


if __name__ == "__main__":
    unittest.main()
