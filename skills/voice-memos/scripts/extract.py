#!/usr/bin/env python3
"""Transcribe Apple Voice Memos with the local Apple SpeechTranscriber CLI."""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
import tempfile
from collections import Counter
from datetime import datetime
from pathlib import Path

from config import (
    AppleResult,
    AppleSTTError,
    AnalysisSchemaError,
    CONTEXT_DIR,
    Outcome,
    OutcomeStatus,
    PipelineError,
    RECORDINGS_DIR,
    REVIEW_DB_PATH,
    RecordingBusy,
    TRANSCRIPTS_DIR,
    VOCAB_FILE,
    analysis_is_fresh,
    apple_binary_sha256,
    atomic_write_json,
    atomic_write_text,
    create_audio_snapshot,
    ensure_runtime_dirs,
    recording_artifact_dir,
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

LOCALE = "ko-KR"
_TIMESTAMP_RE = re.compile(r"(\d{8})\s+(\d{6})")


def _convert_to_m4a(filepath: Path) -> Path:
    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg is None:
        raise AppleSTTError("ffmpeg is required to convert this audio")
    temporary = tempfile.NamedTemporaryFile(suffix=".m4a", prefix="vm_qta_", delete=False)
    temporary.close()
    converted = Path(temporary.name)
    try:
        subprocess.run(
            [
                ffmpeg,
                "-y",
                "-i",
                str(filepath),
                "-vn",
                "-map",
                "0:a:0",
                "-c:a",
                "aac",
                str(converted),
            ],
            capture_output=True,
            text=True,
            check=True,
            timeout=600,
        )
        if converted.stat().st_size == 0:
            raise AppleSTTError("audio conversion produced an empty file")
        return converted
    except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as error:
        converted.unlink(missing_ok=True)
        raise AppleSTTError("audio conversion failed") from error


def transcribe(
    filepath: Path,
    recording_id: str,
    mode: str,
    context_terms: list[str] | None = None,
) -> AppleResult:
    """Keep the existing conversion fallback without changing text authority."""
    if filepath.suffix.lower() == ".qta":
        converted = _convert_to_m4a(filepath)
        try:
            return run_apple_stt(
                converted,
                recording_id=recording_id,
                mode=mode,
                locale=LOCALE,
                context_terms=context_terms,
            )
        finally:
            converted.unlink(missing_ok=True)

    try:
        return run_apple_stt(
            filepath,
            recording_id=recording_id,
            mode=mode,
            locale=LOCALE,
            context_terms=context_terms,
        )
    except AppleSTTError:
        converted = _convert_to_m4a(filepath)
        try:
            return run_apple_stt(
                converted,
                recording_id=recording_id,
                mode=mode,
                locale=LOCALE,
                context_terms=context_terms,
            )
        finally:
            converted.unlink(missing_ok=True)


def parse_filename(filename: str) -> tuple[str, str, str]:
    match = _TIMESTAMP_RE.search(filename)
    if match:
        date_part, time_part = match.groups()
        try:
            parsed = datetime.strptime(f"{date_part} {time_part}", "%Y%m%d %H%M%S")
            return date_part, time_part, parsed.strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            return date_part, time_part, f"{date_part} {time_part}"
    base = filename.removesuffix(".m4a").removesuffix(".qta").split("-")[0].strip()
    date_part = base[:8] or "00000000"
    if date_part in {".", ".."}:
        date_part = "00000000"
    return date_part, "000000", base


def generate_markdown(filepath: Path, text: str) -> str:
    _, _, date_string = parse_filename(filepath.name)
    return "\n".join(
        [
            f"# {date_string}",
            "",
            f"- **녹음일시**: {date_string}",
            f"- **언어**: {LOCALE}",
            f"- **원본파일**: `{filepath.name}`",
            "- **전사엔진**: apple-stt",
            "",
            "## 전사 내용",
            "",
            text,
            "",
        ]
    )


def process_file(filepath: Path, force: bool = False) -> Outcome:
    recording_id = ""
    snapshot_path: Path | None = None
    try:
        mode = stt_mode()
        if not filepath.exists():
            return Outcome(OutcomeStatus.FAILED, code="AudioFileNotFound")
        date_part, time_part, _ = parse_filename(filepath.name)
        if mode == "legacy" and not force:
            legacy_transcript = TRANSCRIPTS_DIR / date_part / time_part / "transcript.md"
            if (
                legacy_transcript.exists()
                and filepath.stat().st_mtime <= legacy_transcript.stat().st_mtime
            ):
                return Outcome(OutcomeStatus.SKIPPED, code="FreshArtifact")
        if not wait_until_settled(filepath):
            return Outcome(OutcomeStatus.DEFERRED, code="SettleDeferred")

        snapshot_path = create_audio_snapshot(filepath)
        recording_id = source_sha256(snapshot_path)
        if source_sha256(filepath) != recording_id:
            return Outcome(OutcomeStatus.DEFERRED, recording_id, "SourceChanged")
        source_mtime_ns = filepath.stat().st_mtime_ns
        with recording_lock(recording_id):
            if source_sha256(filepath) != recording_id:
                return Outcome(OutcomeStatus.DEFERRED, recording_id, "SourceChanged")
            context = None
            context_missing = True
            context_pack = None
            engine_version = ""
            reprocess_marker = None

            if mode == "legacy":
                out_dir = TRANSCRIPTS_DIR / date_part / time_part
                transcript_path = out_dir / "transcript.md"
                if (
                    transcript_path.exists()
                    and not force
                    and filepath.stat().st_mtime <= transcript_path.stat().st_mtime
                ):
                    return Outcome(OutcomeStatus.SKIPPED, recording_id, "FreshArtifact")
            else:
                context, context_missing = context_for_recording(recording_id, CONTEXT_DIR)
                with ReviewStore(REVIEW_DB_PATH) as store:
                    context_pack = build_context_pack(context, store, VOCAB_FILE)
                reprocess_marker = context_path(recording_id, CONTEXT_DIR).with_suffix(
                    ".reprocess"
                )
                force = force or reprocess_marker.exists()
                engine_version = apple_binary_sha256()
                out_dir = recording_artifact_dir(date_part, time_part, recording_id)
                analysis_path = out_dir / "analysis.json"
                transcript_path = out_dir / "transcript.md"
                run_path = out_dir / "run.json"
                if (
                    not force
                    and analysis_is_fresh(
                        analysis_path,
                        recording_id,
                        engine_version=engine_version,
                        context_fingerprint=context_pack["fingerprint"],
                        locale=LOCALE,
                    )
                    and run_is_fresh(
                        run_path,
                        recording_id,
                        mode=mode,
                        engine_version=engine_version,
                        context_fingerprint=context_pack["fingerprint"],
                    )
                    and (out_dir / "raw.md").exists()
                    and (mode == "shadow" or transcript_path.exists())
                ):
                    return Outcome(OutcomeStatus.SKIPPED, recording_id, "FreshArtifact")

            result = transcribe(
                snapshot_path,
                recording_id,
                mode,
                None if context_pack is None else context_pack["selected"],
            )
            if source_sha256(filepath) != recording_id:
                return Outcome(OutcomeStatus.DEFERRED, recording_id, "SourceChanged")
            markdown = generate_markdown(filepath, result.text)
            ensure_runtime_dirs()
            if mode == "legacy":
                if source_sha256(filepath) != recording_id:
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
                atomic_write_text(out_dir / "raw.md", markdown)
                if mode == "review":
                    atomic_write_text(transcript_path, markdown)
                if source_sha256(filepath) != recording_id:
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

    parser = argparse.ArgumentParser(description="Apple Voice Memos transcription")
    parser.add_argument("--file", help="process one audio file")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--all", action="store_true")
    args = parser.parse_args()

    if args.file:
        raise SystemExit(_run([Path(args.file).expanduser()], args.force))
    files = sorted(
        path for pattern in ("*.m4a", "*.qta") for path in RECORDINGS_DIR.glob(pattern)
    )
    raise SystemExit(_run(files, args.force))


if __name__ == "__main__":
    main()
