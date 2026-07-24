#!/usr/bin/env python3
"""Transcribe iCloud call recordings with the same Apple evidence contract."""

from __future__ import annotations

import os
import re
import subprocess
import sys
import time
from collections import Counter
from datetime import datetime
from pathlib import Path

from config import (
    AppleResult,
    AnalysisSchemaError,
    CALL_RECORDINGS_DIR,
    CALL_TRANSCRIPT_SUFFIX,
    CONTEXT_DIR,
    Outcome,
    OutcomeStatus,
    PipelineError,
    REVIEW_DB_PATH,
    RecordingBusy,
    VOCAB_FILE,
    analysis_is_fresh,
    apple_binary_sha256,
    atomic_write_json,
    atomic_write_text,
    create_audio_snapshot,
    recording_lock,
    run_apple_stt,
    run_is_fresh,
    run_record,
    source_sha256,
    stt_mode,
    wait_until_settled,
)
from review import (
    ContextValidationError,
    ReviewStore,
    build_context_pack,
    candidate_segments,
    context_for_recording,
    context_path,
)

CALLS_DIR = CALL_RECORDINGS_DIR
FILENAME_RE = re.compile(r"^(?P<prefix>.+)_(?P<date>\d{8})_(?P<time>\d{6})\.m4a$")
TRAILING_PHONE_RE = re.compile(r"^(?P<contact>.+)_(?P<phone>\d{7,11})$")
DOWNLOAD_TIMEOUT = 180
DOWNLOAD_POLL_INTERVAL = 2


def is_dataless(path: Path) -> bool:
    return path.stat().st_blocks == 0


def materialize(path: Path) -> bool:
    if not is_dataless(path):
        return True
    subprocess.run(["brctl", "download", str(path)], check=False, capture_output=True)
    deadline = time.monotonic() + DOWNLOAD_TIMEOUT
    while time.monotonic() < deadline:
        if not is_dataless(path):
            return True
        time.sleep(DOWNLOAD_POLL_INTERVAL)
    return not is_dataless(path)


def parse_filename(name: str):
    match = FILENAME_RE.match(name)
    if not match:
        return None
    prefix = match.group("prefix")
    phone_match = TRAILING_PHONE_RE.match(prefix)
    contact = phone_match.group("contact") if phone_match else prefix
    phone = phone_match.group("phone") if phone_match else ""
    date_part = match.group("date")
    time_part = match.group("time")
    try:
        parsed = datetime.strptime(f"{date_part}{time_part}", "%Y%m%d%H%M%S")
    except ValueError:
        return None
    return contact, phone, date_part, time_part, parsed


def transcript_has_body(path: Path) -> bool:
    try:
        content = path.read_text(encoding="utf-8")
    except OSError:
        return False
    marker = "## 전사 내용"
    index = content.find(marker)
    if index == -1:
        return False
    return bool(re.sub(r"<!--.*?-->", "", content[index + len(marker) :]).strip())


def transcribe(
    path: Path,
    recording_id: str,
    mode: str,
    context_terms: list[str] | None = None,
) -> AppleResult:
    return run_apple_stt(
        path,
        recording_id=recording_id,
        mode=mode,
        context_terms=context_terms,
        timestamps=mode == "legacy",
    )


def generate_markdown(contact: str, phone: str, dt: datetime, name: str, text: str) -> str:
    date_string = dt.strftime("%Y-%m-%d %H:%M:%S")
    contact_label = contact[:-1] if contact.endswith("님") else contact
    return "\n".join(
        [
            f"# {date_string} {contact_label}님과의 통화",
            "",
            f"- **녹음일시**: {date_string}",
            f"- **상대**: {contact}" + (f" ({phone})" if phone else ""),
            "- **언어**: ko-KR",
            f"- **원본파일**: `{name}`",
            "- **전사**: apple-stt (화자 라벨 없음)",
            "",
            "## 전사 내용",
            "",
            text,
            "",
        ]
    )


def process_file(path: Path, force: bool = False) -> Outcome:
    recording_id = ""
    snapshot_path: Path | None = None
    try:
        mode = stt_mode()
        parsed = parse_filename(path.name)
        if parsed is None:
            return Outcome(OutcomeStatus.FAILED, code="FilenameUnsupported")
        if not path.exists():
            return Outcome(OutcomeStatus.FAILED, code="AudioFileNotFound")
        contact, phone, _date, _time, dt = parsed
        transcript_path = path.with_name(f"{path.stem}{CALL_TRANSCRIPT_SUFFIX}")
        analysis_path = path.with_name(f"{path.stem}.analysis.json")
        run_path = path.with_name(f"{path.stem}.run.json")
        if (
            mode == "legacy"
            and not force
            and transcript_has_body(transcript_path)
            and path.stat().st_mtime_ns <= transcript_path.stat().st_mtime_ns
        ):
            return Outcome(OutcomeStatus.SKIPPED, code="FreshArtifact")
        if not materialize(path):
            return Outcome(OutcomeStatus.FAILED, code="AudioMaterializeError")
        if not wait_until_settled(path):
            return Outcome(OutcomeStatus.DEFERRED, code="SettleDeferred")

        snapshot_path = create_audio_snapshot(path)
        recording_id = source_sha256(snapshot_path)
        if source_sha256(path) != recording_id:
            return Outcome(OutcomeStatus.DEFERRED, recording_id, "SourceChanged")
        source_mtime_ns = path.stat().st_mtime_ns
        with recording_lock(recording_id):
            if source_sha256(path) != recording_id:
                return Outcome(OutcomeStatus.DEFERRED, recording_id, "SourceChanged")
            context = None
            context_missing = True
            context_pack = None
            engine_version = ""
            reprocess_marker = None
            if mode != "legacy":
                context, context_missing = context_for_recording(recording_id, CONTEXT_DIR)
                with ReviewStore(REVIEW_DB_PATH) as store:
                    context_pack = build_context_pack(context, store, VOCAB_FILE)
                reprocess_marker = context_path(recording_id, CONTEXT_DIR).with_suffix(
                    ".reprocess"
                )
                force = force or reprocess_marker.exists()
                engine_version = apple_binary_sha256()
                if (
                    not force
                    and analysis_is_fresh(
                        analysis_path,
                        recording_id,
                        engine_version=engine_version,
                        context_fingerprint=context_pack["fingerprint"],
                        locale="ko-KR",
                    )
                    and run_is_fresh(
                        run_path,
                        recording_id,
                        mode=mode,
                        engine_version=engine_version,
                        context_fingerprint=context_pack["fingerprint"],
                    )
                    and (mode == "shadow" or transcript_has_body(transcript_path))
                ):
                    return Outcome(OutcomeStatus.SKIPPED, recording_id, "FreshArtifact")

            result = transcribe(
                snapshot_path,
                recording_id,
                mode,
                None if context_pack is None else context_pack["selected"],
            )
            if source_sha256(path) != recording_id:
                return Outcome(OutcomeStatus.DEFERRED, recording_id, "SourceChanged")
            markdown = generate_markdown(contact, phone, dt, path.name, result.text)
            if mode == "legacy":
                if source_sha256(path) != recording_id:
                    return Outcome(
                        OutcomeStatus.DEFERRED, recording_id, "SourceChanged"
                    )
                atomic_write_text(transcript_path, markdown)
                os.utime(
                    transcript_path,
                    ns=(source_mtime_ns, source_mtime_ns),
                )
            else:
                if result.analysis is None:
                    raise AnalysisSchemaError("analysis result missing")
                apple_context = result.analysis.get("context")
                if not isinstance(apple_context, dict):
                    raise AnalysisSchemaError("analysis context missing")
                if apple_context.get("selected") != context_pack["selected"]:
                    raise AnalysisSchemaError("Apple context does not match requested pack")
                if result.analysis.get("engine_version") != engine_version:
                    raise AnalysisSchemaError("analysis engine hash mismatch")
                apple_context.update(context_pack)
                candidate_count = (
                    len(candidate_segments(result.analysis)) if mode == "review" else 0
                )
                final_run = run_record(
                    recording_id,
                    mode,
                    OutcomeStatus.PROCESSED,
                    privacy=context["privacy"],
                    context_fingerprint=context_pack["fingerprint"],
                    context_missing=context_missing,
                    engine_version=engine_version,
                    review_state=(
                        "review_pending" if candidate_count else "finalizable"
                    ),
                    candidate_count=candidate_count,
                )
                publishing_run = {**final_run, "review_state": "publishing"}
                atomic_write_json(run_path, publishing_run)
                atomic_write_json(analysis_path, result.analysis)
                if mode == "review":
                    atomic_write_text(transcript_path, markdown)
                if source_sha256(path) != recording_id:
                    return Outcome(
                        OutcomeStatus.DEFERRED, recording_id, "SourceChanged"
                    )
                atomic_write_json(run_path, final_run)
                if reprocess_marker is not None:
                    reprocess_marker.unlink(missing_ok=True)
            return Outcome(OutcomeStatus.PROCESSED, recording_id)
    except RecordingBusy:
        return Outcome(OutcomeStatus.DEFERRED, recording_id, "RecordingBusy")
    except ContextValidationError:
        return Outcome(OutcomeStatus.FAILED, recording_id, "ContextValidationError")
    except PipelineError as error:
        return Outcome(OutcomeStatus.FAILED, recording_id, error.code)
    except OSError:
        return Outcome(OutcomeStatus.FAILED, recording_id, "AudioFileError")
    finally:
        if snapshot_path is not None:
            snapshot_path.unlink(missing_ok=True)


def _run(files: list[Path], force: bool) -> int:
    outcomes = [process_file(path, force=force) for path in files]
    counts = Counter(outcome.status.value for outcome in outcomes)
    print(
        "  "
        + " ".join(
            f"{status.value}={counts[status.value]}" for status in OutcomeStatus
        )
    )
    for outcome in outcomes:
        if outcome.status == OutcomeStatus.FAILED:
            print(
                f"  [ERROR] {outcome.recording_id[:8] or 'unknown'} {outcome.code}",
                file=sys.stderr,
            )
    return 1 if counts[OutcomeStatus.FAILED.value] else 0


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Call recording transcription")
    parser.add_argument("--file", help="process one .m4a file")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--all", action="store_true")
    args = parser.parse_args()

    if args.file:
        raise SystemExit(_run([Path(args.file).expanduser()], args.force))
    files = sorted(CALLS_DIR.glob("*.m4a")) if CALLS_DIR.exists() else []
    raise SystemExit(_run(files, args.force))


if __name__ == "__main__":
    main()
