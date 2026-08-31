"""Shared paths and small, dependency-free pipeline primitives."""

from __future__ import annotations

import hashlib
import json
import os
import fcntl
import math
import re
import shutil
import subprocess
import tempfile
import time
import uuid
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = PROJECT_DIR / "scripts"

DATA_DIR = Path(
    os.environ.get(
        "VOICE_MEMOS_DATA_DIR",
        Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/voice-memos",
    )
).expanduser()
TRANSCRIPTS_DIR = DATA_DIR / "transcripts"
RUNTIME_DIR = Path(os.environ.get("VOICE_MEMOS_RUNTIME_DIR", "~/.voice-memos")).expanduser()
LOGS_DIR = RUNTIME_DIR / "logs"
CONTEXT_DIR = Path(
    os.environ.get("VOICE_MEMOS_CONTEXT_DIR", "~/.config/voice-memos/recordings")
).expanduser()
REVIEW_DB_PATH = Path(
    os.environ.get("VOICE_MEMOS_REVIEW_DB", RUNTIME_DIR / "state/review.sqlite3")
).expanduser()
VOCAB_FILE = Path.home() / ".config" / "stt" / "vocab.txt"
ENV_FILE = Path(
    os.environ.get("VOICE_MEMOS_CONFIG_FILE", "~/.config/voice-memos/.env")
).expanduser()
WATCHER_LOG_FILE = LOGS_DIR / "watcher.log"
CALL_RECORDINGS_DIR = Path(
    os.environ.get(
        "VOICE_MEMOS_CALL_RECORDINGS_DIR",
        Path.home() / "Library/Mobile Documents/com~apple~CloudDocs/녹음",
    )
).expanduser()
RECORDINGS_DIR = Path(
    os.environ.get(
        "VOICE_MEMOS_RECORDINGS_DIR",
        Path.home()
        / "Library/Group Containers/group.com.apple.VoiceMemos.shared/Recordings",
    )
).expanduser()
CALL_TRANSCRIPT_SUFFIX = ".transcript.md"
CALL_SUMMARY_SUFFIX = ".summary.md"
CALL_NAME_SUFFIXES = (CALL_TRANSCRIPT_SUFFIX, CALL_SUMMARY_SUFFIX, ".txt", ".m4a")


def is_dataless(path: Path) -> bool:
    """iCloud에 있고 아직 로컬로 내려오지 않은 파일인지. 읽으면 EDEADLK로 실패한다."""
    try:
        return path.stat().st_blocks == 0
    except OSError:
        return False
CALL_DATETIME_RE = re.compile(r"^(?P<prefix>.+)_(?P<date>\d{8})_(?P<time>\d{6})$")
CALL_DATE_TRAILING_RE = re.compile(r"^(?P<prefix>.+)_(?P<date>\d{6})$")
CALL_DATE_LEADING_RE = re.compile(r"^(?P<date>\d{6})-(?P<prefix>.+)$")
CALL_TRAILING_PHONE_RE = re.compile(r"^(?P<contact>.+)_(?P<phone>\d{7,11})$")


@dataclass(frozen=True)
class CallName:
    contact: str
    phone: str
    dt: datetime
    has_time: bool


def parse_call_name(name: str) -> "CallName | None":
    """통화 녹음 파일명에서 상대·전화번호·시각을 파싱한다. 지원 밖 이름은 None.

    지원 형식: `<상대>_<전화번호>_<YYYYMMDD>_<HHMMSS>`, `<상대>_<YYMMDD>`, `<YYMMDD>-<상대>`.
    이 폴더에는 사람이 직접 붙인 이름도 들어오므로 날짜가 앞이든 뒤든 인식한다.
    """
    stem = name
    for suffix in CALL_NAME_SUFFIXES:
        if stem.endswith(suffix):
            stem = stem[: -len(suffix)]
            break

    match = CALL_DATETIME_RE.match(stem)
    has_time = bool(match)
    if match:
        stamp, fmt = f"{match.group('date')}{match.group('time')}", "%Y%m%d%H%M%S"
    else:
        match = CALL_DATE_TRAILING_RE.match(stem) or CALL_DATE_LEADING_RE.match(stem)
        if not match:
            return None
        stamp, fmt = match.group("date"), "%y%m%d"
    try:
        dt = datetime.strptime(stamp, fmt)
    except ValueError:
        return None

    prefix = match.group("prefix")
    phone_match = CALL_TRAILING_PHONE_RE.match(prefix)
    if phone_match:
        return CallName(phone_match.group("contact"), phone_match.group("phone"), dt, has_time)
    return CallName(prefix, "", dt, has_time)

PROCESS_MARKERS = (
    "<!-- corrected -->",
    "<!-- summarized -->",
    "<!-- notified -->",
)


class OutcomeStatus(str, Enum):
    PROCESSED = "processed"
    SKIPPED = "skipped"
    DEFERRED = "deferred"
    FAILED = "failed"


@dataclass(frozen=True)
class Outcome:
    status: OutcomeStatus
    recording_id: str = ""
    code: str = ""


@dataclass(frozen=True)
class AppleResult:
    text: str
    analysis: dict | None


class PipelineError(RuntimeError):
    code = "PipelineError"


class AnalysisModeUnsupported(PipelineError):
    code = "AnalysisModeUnsupported"


class AppleSTTError(PipelineError):
    code = "SpeechAnalysisError"


class AnalysisSchemaError(PipelineError):
    code = "AnalysisSchemaInvalid"


class RunSchemaError(PipelineError):
    code = "RunSchemaInvalid"


class NoRecognizableSpeech(PipelineError):
    code = "NoRecognizableSpeech"


class ArtifactWriteError(PipelineError):
    code = "ArtifactWriteError"


class RecordingBusy(PipelineError):
    code = "RecordingBusy"


def ensure_runtime_dirs() -> None:
    """Create local and transcript runtime directories."""
    for path in (TRANSCRIPTS_DIR, LOGS_DIR):
        path.mkdir(parents=True, exist_ok=True)


def source_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def create_audio_snapshot(path: Path) -> Path:
    """Copy one settled input so hashing and Apple analysis see identical bytes."""
    snapshot: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            "wb", prefix="voice-memos-audio-", suffix=path.suffix, delete=False
        ) as output:
            snapshot = Path(output.name)
            with path.open("rb") as source:
                shutil.copyfileobj(source, output, length=1024 * 1024)
            output.flush()
            os.fsync(output.fileno())
        return snapshot
    except OSError:
        if snapshot is not None:
            snapshot.unlink(missing_ok=True)
        raise


def _is_number(value: object) -> bool:
    return not isinstance(value, bool) and isinstance(value, (int, float)) and math.isfinite(value)


def validate_analysis_document(
    value: object, *, expected_audio_sha256: str | None = None
) -> dict:
    """Validate the Apple evidence boundary, including UTF-8 byte spans."""
    if not isinstance(value, dict) or value.get("schema_version") != 1:
        raise AnalysisSchemaError("analysis schema_version must be 1")
    if value.get("engine") != "apple-speech-transcriber":
        raise AnalysisSchemaError("analysis engine is invalid")
    engine_version = value.get("engine_version")
    if not isinstance(engine_version, str) or len(engine_version) != 64 or any(
        char not in "0123456789abcdef" for char in engine_version
    ):
        raise AnalysisSchemaError("analysis engine_version is invalid")
    if not isinstance(value.get("locale"), str) or not value["locale"]:
        raise AnalysisSchemaError("analysis locale is invalid")
    if value.get("offset_unit") != "utf8_bytes":
        raise AnalysisSchemaError("analysis offset_unit must be utf8_bytes")

    source = value.get("source")
    if not isinstance(source, dict):
        raise AnalysisSchemaError("analysis source is missing")
    audio_sha256 = source.get("audio_sha256")
    if not isinstance(audio_sha256, str) or len(audio_sha256) != 64 or any(
        char not in "0123456789abcdef" for char in audio_sha256
    ):
        raise AnalysisSchemaError("analysis source hash is invalid")
    if expected_audio_sha256 is not None and audio_sha256 != expected_audio_sha256:
        raise AnalysisSchemaError("analysis source hash does not match CLI input")
    duration_ms = source.get("duration_ms")
    if isinstance(duration_ms, bool) or not isinstance(duration_ms, int) or duration_ms < 0:
        raise AnalysisSchemaError("analysis duration_ms is invalid")

    capabilities = value.get("capabilities")
    if not isinstance(capabilities, dict) or any(
        not isinstance(capabilities.get(name), bool)
        for name in ("alternatives", "confidence", "audio_time_range")
    ):
        raise AnalysisSchemaError("analysis capabilities are invalid")
    context = value.get("context")
    if not isinstance(context, dict):
        raise AnalysisSchemaError("analysis context is missing")
    selected = context.get("selected")
    dropped = context.get("dropped")
    fingerprint = context.get("fingerprint")
    if (
        not isinstance(selected, list)
        or len(selected) > 100
        or any(not isinstance(term, str) for term in selected)
        or not isinstance(dropped, list)
        or any(not isinstance(term, str) for term in dropped)
        or not isinstance(fingerprint, str)
        or len(fingerprint) != 64
        or any(char not in "0123456789abcdef" for char in fingerprint)
    ):
        raise AnalysisSchemaError("analysis context is invalid")

    method = value.get("review_confidence_method")
    if not isinstance(method, dict) or method.get("name") != "lower_quantile":
        raise AnalysisSchemaError("analysis review confidence method is invalid")
    if method.get("version") != 1 or not _is_number(method.get("quantile")):
        raise AnalysisSchemaError("analysis review confidence method is invalid")

    segments = value.get("segments")
    if not isinstance(segments, list) or not segments:
        raise AnalysisSchemaError("analysis segments are missing")
    seen_ids: set[str] = set()
    for segment in segments:
        if not isinstance(segment, dict):
            raise AnalysisSchemaError("analysis segment is invalid")
        segment_id = segment.get("id")
        text = segment.get("text")
        if (
            not isinstance(segment_id, str)
            or not segment_id
            or segment_id in seen_ids
            or not isinstance(text, str)
            or not text.strip()
        ):
            raise AnalysisSchemaError("analysis segment identity/text is invalid")
        seen_ids.add(segment_id)
        start, end = segment.get("start"), segment.get("end")
        if not _is_number(start) or not _is_number(end) or start < 0 or end < start:
            raise AnalysisSchemaError("analysis segment time is invalid")

        boundaries = {0}
        offset = 0
        for character in text:
            offset += len(character.encode("utf-8"))
            boundaries.add(offset)
        spans = segment.get("confidence_spans")
        if not isinstance(spans, list):
            raise AnalysisSchemaError("analysis confidence_spans is invalid")
        for span in spans:
            if not isinstance(span, dict):
                raise AnalysisSchemaError("analysis confidence span is invalid")
            span_start, span_end = span.get("start_byte"), span.get("end_byte")
            confidence = span.get("confidence")
            if (
                isinstance(span_start, bool)
                or not isinstance(span_start, int)
                or isinstance(span_end, bool)
                or not isinstance(span_end, int)
                or span_start not in boundaries
                or span_end not in boundaries
                or span_start >= span_end
                or not _is_number(confidence)
                or not 0 <= confidence <= 1
            ):
                raise AnalysisSchemaError("analysis confidence span is invalid")
        review_confidence = segment.get("review_confidence")
        if review_confidence is not None and (
            not _is_number(review_confidence) or not 0 <= review_confidence <= 1
        ):
            raise AnalysisSchemaError("analysis review_confidence is invalid")
        alternatives = segment.get("alternatives")
        if not isinstance(alternatives, list):
            raise AnalysisSchemaError("analysis alternatives are invalid")
        for alternative in alternatives:
            if not isinstance(alternative, dict) or not isinstance(
                alternative.get("text"), str
            ):
                raise AnalysisSchemaError("analysis alternative is invalid")
            alt_start, alt_end = alternative.get("start"), alternative.get("end")
            confidence = alternative.get("confidence")
            if (
                not _is_number(alt_start)
                or not _is_number(alt_end)
                or alt_start < 0
                or alt_end < alt_start
                or (
                    confidence is not None
                    and (not _is_number(confidence) or not 0 <= confidence <= 1)
                )
            ):
                raise AnalysisSchemaError("analysis alternative is invalid")
    return value


def _is_sha256(value: object) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(char in "0123456789abcdef" for char in value)
    )


def validate_run_document(value: object) -> dict:
    """Validate strict run metadata before any derived artifact or egress."""
    if not isinstance(value, dict) or value.get("schema_version") != 1:
        raise RunSchemaError("run schema_version must be 1")
    recording_id = value.get("recording_id")
    run_id = value.get("run_id")
    source = value.get("source")
    parents = value.get("parents")
    candidate_count = value.get("candidate_count")
    if not _is_sha256(recording_id):
        raise RunSchemaError("run recording_id is invalid")
    if (
        not isinstance(run_id, str)
        or len(run_id) != 32
        or any(char not in "0123456789abcdef" for char in run_id)
    ):
        raise RunSchemaError("run run_id is invalid")
    if value.get("mode") not in {"shadow", "review"}:
        raise RunSchemaError("run mode is invalid")
    if value.get("privacy") not in {"standard", "local"}:
        raise RunSchemaError("run privacy is invalid")
    if not isinstance(source, dict) or source.get("audio_sha256") != recording_id:
        raise RunSchemaError("run source is invalid")
    if (
        not isinstance(parents, dict)
        or not _is_sha256(parents.get("engine_version"))
        or not _is_sha256(parents.get("context_fingerprint"))
    ):
        raise RunSchemaError("run parents are invalid")
    if not isinstance(value.get("recording_context_missing"), bool):
        raise RunSchemaError("run context status is invalid")
    if value.get("review_state") not in {
        "publishing",
        "finalizable",
        "review_pending",
    }:
        raise RunSchemaError("run review_state is invalid")
    if (
        isinstance(candidate_count, bool)
        or not isinstance(candidate_count, int)
        or candidate_count < 0
    ):
        raise RunSchemaError("run candidate_count is invalid")
    if value.get("result") != OutcomeStatus.PROCESSED.value:
        raise RunSchemaError("run result is invalid")
    if value.get("error_code") is not None:
        raise RunSchemaError("run error_code is invalid")

    summary_state = value.get("summary_state")
    if summary_state not in {"missing", "fresh"}:
        raise RunSchemaError("run summary_state is invalid")
    summary_hashes = (
        value.get("summary_parent_sha256"),
        value.get("summary_body_sha256"),
        value.get("summary_generator_fingerprint"),
    )
    if summary_state == "fresh":
        if any(not _is_sha256(item) for item in summary_hashes):
            raise RunSchemaError("fresh summary fingerprints are invalid")
    elif any(item is not None for item in summary_hashes):
        raise RunSchemaError("missing summary cannot have fingerprints")
    return value


def atomic_write_text(path: Path, content: str) -> None:
    """Replace a text artifact only after its sibling temporary file is durable."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            "w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            delete=False,
        ) as output:
            temp_path = Path(output.name)
            output.write(content)
            output.flush()
            os.fsync(output.fileno())
        os.replace(temp_path, path)
    except OSError as error:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)
        raise ArtifactWriteError(str(error)) from error


def atomic_write_json(path: Path, value: dict) -> None:
    atomic_write_text(
        path,
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
    )


def analysis_is_fresh(
    path: Path,
    recording_id: str,
    *,
    engine_version: str | None = None,
    context_fingerprint: str | None = None,
    locale: str | None = None,
) -> bool:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, OSError, json.JSONDecodeError):
        return False
    try:
        validate_analysis_document(value)
    except AnalysisSchemaError:
        return False
    source = value.get("source")
    context = value.get("context") if isinstance(value, dict) else None
    return (
        value.get("schema_version") == 1
        and isinstance(source, dict)
        and source.get("audio_sha256") == recording_id
        and (engine_version is None or value.get("engine_version") == engine_version)
        and (locale is None or value.get("locale") == locale)
        and (
            context_fingerprint is None
            or (
                isinstance(context, dict)
                and context.get("fingerprint") == context_fingerprint
            )
        )
    )


def run_is_fresh(
    path: Path,
    recording_id: str,
    *,
    mode: str,
    engine_version: str,
    context_fingerprint: str,
) -> bool:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, OSError, json.JSONDecodeError):
        return False
    try:
        validate_run_document(value)
    except RunSchemaError:
        return False
    source = value.get("source")
    parents = value.get("parents")
    return (
        value.get("schema_version") == 1
        and value.get("recording_id") == recording_id
        and value.get("mode") == mode
        and value.get("privacy") in {"standard", "local"}
        and value.get("result") == OutcomeStatus.PROCESSED.value
        and value.get("review_state") in {"finalizable", "review_pending"}
        and isinstance(source, dict)
        and source.get("audio_sha256") == recording_id
        and isinstance(parents, dict)
        and parents.get("engine_version") == engine_version
        and parents.get("context_fingerprint") == context_fingerprint
    )


def run_record(
    recording_id: str,
    mode: str,
    status: OutcomeStatus,
    code: str = "",
    *,
    privacy: str = "standard",
    context_fingerprint: str = "",
    context_missing: bool = True,
    engine_version: str = "",
    review_state: str = "finalizable",
    candidate_count: int = 0,
    summary_state: str = "missing",
) -> dict:
    return {
        "schema_version": 1,
        "run_id": uuid.uuid4().hex,
        "recording_id": recording_id,
        "mode": mode,
        "privacy": privacy,
        "source": {"audio_sha256": recording_id},
        "parents": {
            "engine_version": engine_version or None,
            "context_fingerprint": context_fingerprint or None,
        },
        "recording_context_missing": context_missing,
        "review_state": review_state,
        "candidate_count": candidate_count,
        "summary_state": summary_state,
        "summary_parent_sha256": None,
        "summary_body_sha256": None,
        "result": status.value,
        "error_code": code or None,
    }


def stt_mode() -> str:
    mode = os.environ.get("VOICE_MEMOS_STT_MODE", "legacy").strip().lower()
    if mode not in {"legacy", "shadow", "review"}:
        raise PipelineError(
            "VOICE_MEMOS_STT_MODE must be legacy, shadow, or review"
        )
    return mode


def resolve_apple_stt() -> str:
    configured = os.environ.get("VOICE_MEMOS_APPLE_STT", "apple-stt")
    resolved = shutil.which(configured)
    if resolved is None:
        raise AppleSTTError("apple-stt command not found")
    return resolved


def apple_binary_sha256() -> str:
    return source_sha256(Path(resolve_apple_stt()))


@contextmanager
def recording_lock(recording_id: str):
    """Serialize publish/review for one recording; OS releases the lock on crash."""
    if len(recording_id) != 64 or any(
        char not in "0123456789abcdef" for char in recording_id
    ):
        raise PipelineError("invalid recording ID for lock")
    directory = RUNTIME_DIR / "recording-locks"
    directory.mkdir(parents=True, exist_ok=True)
    handle = (directory / f"{recording_id}.lock").open("a+")
    try:
        try:
            fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as error:
            raise RecordingBusy("recording artifacts are locked") from error
        yield
    finally:
        try:
            fcntl.flock(handle, fcntl.LOCK_UN)
        finally:
            handle.close()


def _supports_analysis_mode(executable: str) -> bool:
    result = subprocess.run(
        [executable, "--help"], capture_output=True, text=True, check=False
    )
    return "--analysis-json" in f"{result.stdout}\n{result.stderr}"


def run_apple_stt(
    audio_path: Path,
    *,
    recording_id: str,
    mode: str,
    locale: str = "ko-KR",
    context_terms: list[str] | None = None,
    timestamps: bool = False,
) -> AppleResult:
    """Run the sole text authority and validate the explicit analysis contract."""
    executable = resolve_apple_stt()
    cmd = [executable, "--quiet", "--locale", locale]
    if mode == "legacy" and timestamps:
        cmd.append("--timestamps")
    if mode != "legacy":
        if not _supports_analysis_mode(executable):
            raise AnalysisModeUnsupported(
                "apple-stt does not advertise --analysis-json"
            )
        cmd.append("--analysis-json")
    context_file: Path | None = None
    if context_terms is not None:
        with tempfile.NamedTemporaryFile(
            "w", encoding="utf-8", prefix="voice-memos-context-", delete=False
        ) as handle:
            handle.write("\n".join(context_terms) + ("\n" if context_terms else ""))
            context_file = Path(handle.name)
        cmd.extend(["--vocab-file", str(context_file)])
    cmd.append(str(audio_path))
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as error:
        raise AppleSTTError(error.stderr.strip() or "apple-stt failed") from error
    finally:
        if context_file is not None:
            context_file.unlink(missing_ok=True)

    if mode == "legacy":
        text = result.stdout.strip()
        if not text:
            raise NoRecognizableSpeech("apple-stt returned no text")
        return AppleResult(text=text, analysis=None)

    try:
        analysis = json.loads(result.stdout)
    except json.JSONDecodeError as error:
        raise AnalysisSchemaError("analysis output is not one JSON object") from error
    input_sha256 = source_sha256(audio_path)
    validate_analysis_document(analysis, expected_audio_sha256=input_sha256)
    source = analysis["source"]
    segments = analysis["segments"]
    # Converted .qta/.m4a input is an implementation detail; artifacts bind to source bytes.
    source["audio_sha256"] = recording_id

    texts = []
    for segment in segments:
        if not isinstance(segment, dict) or not isinstance(segment.get("text"), str):
            raise AnalysisSchemaError("analysis segment text is invalid")
        if segment["text"].strip():
            texts.append(segment["text"].strip())
    if not texts:
        raise NoRecognizableSpeech("analysis contains no recognizable text")
    return AppleResult(text="\n".join(texts), analysis=analysis)


def wait_until_settled(
    path: Path,
    *,
    quiet_seconds: float = 3.0,
    max_wait: float = 90.0,
    poll_interval: float = 2.0,
) -> bool:
    deadline = time.monotonic() + max_wait
    last_signature = None
    quiet_since = None
    while time.monotonic() < deadline:
        try:
            stat = path.stat()
        except FileNotFoundError:
            return False
        if stat.st_size > 0 and time.time() - stat.st_mtime >= quiet_seconds:
            return True
        signature = (stat.st_size, stat.st_mtime_ns)
        if signature != last_signature:
            last_signature = signature
            quiet_since = time.monotonic()
        elif quiet_since is not None and time.monotonic() - quiet_since >= quiet_seconds:
            return True
        time.sleep(poll_interval)
    return False


def _artifact_recording_id(directory: Path) -> str | None:
    for name in ("analysis.json", "run.json"):
        try:
            value = json.loads((directory / name).read_text(encoding="utf-8"))
        except (FileNotFoundError, OSError, json.JSONDecodeError):
            continue
        source = value.get("source") if isinstance(value, dict) else None
        if isinstance(source, dict) and isinstance(source.get("audio_sha256"), str):
            return source["audio_sha256"]
        if isinstance(value, dict) and isinstance(value.get("recording_id"), str):
            return value["recording_id"]
    return None


def recording_artifact_dir(date: str, time_part: str, recording_id: str) -> Path:
    """Return an HHMMSS-id directory without merging an unknown/different source."""
    if (
        len(recording_id) != 64
        or any(char not in "0123456789abcdef" for char in recording_id)
        or not date
        or date in {".", ".."}
        or "/" in date
        or "\0" in date
        or len(time_part) != 6
        or not time_part.isdigit()
    ):
        raise PipelineError("invalid recording artifact identity")
    root = TRANSCRIPTS_DIR.resolve()
    # ponytail: linear lookup is enough for a single-user corpus; add an index only if measured.
    if TRANSCRIPTS_DIR.exists():
        for analysis_path in TRANSCRIPTS_DIR.glob("*/*/analysis.json"):
            directory = analysis_path.parent
            if root not in directory.resolve().parents:
                continue
            if _artifact_recording_id(directory) == recording_id:
                return analysis_path.parent
    for prefix_length in range(8, 65, 4):
        candidate = TRANSCRIPTS_DIR / date / f"{time_part}-{recording_id[:prefix_length]}"
        if root not in candidate.resolve().parents:
            raise PipelineError("recording artifact path escapes transcript root")
        if not candidate.exists() or _artifact_recording_id(candidate) == recording_id:
            return candidate
    raise PipelineError("RecordingIdentityConflict")


def is_call_transcript(path: Path) -> bool:
    return path.parent == CALL_RECORDINGS_DIR and path.name.endswith(CALL_TRANSCRIPT_SUFFIX)


def is_call_summary(path: Path) -> bool:
    return path.parent == CALL_RECORDINGS_DIR and path.name.endswith(CALL_SUMMARY_SUFFIX)


def iter_transcript_files(base_dir: Path) -> list[Path]:
    files = sorted(base_dir.rglob("transcript.md")) if base_dir.exists() else []
    if base_dir == TRANSCRIPTS_DIR and CALL_RECORDINGS_DIR.exists():
        files.extend(sorted(CALL_RECORDINGS_DIR.glob(f"*{CALL_TRANSCRIPT_SUFFIX}")))
    return sorted(files)


def summary_path_for(transcript_path: Path) -> Path:
    if is_call_transcript(transcript_path):
        stem = transcript_path.name[: -len(CALL_TRANSCRIPT_SUFFIX)]
        return transcript_path.with_name(f"{stem}{CALL_SUMMARY_SUFFIX}")
    return transcript_path.parent / "summary.md"


def run_path_for(transcript_path: Path) -> Path:
    if transcript_path.name.endswith(CALL_TRANSCRIPT_SUFFIX):
        stem = transcript_path.name[: -len(CALL_TRANSCRIPT_SUFFIX)]
        return transcript_path.with_name(f"{stem}.run.json")
    return transcript_path.parent / "run.json"


def analysis_path_for(transcript_path: Path) -> Path:
    if transcript_path.name.endswith(CALL_TRANSCRIPT_SUFFIX):
        stem = transcript_path.name[: -len(CALL_TRANSCRIPT_SUFFIX)]
        return transcript_path.with_name(f"{stem}.analysis.json")
    return transcript_path.parent / "analysis.json"


def transcript_path_for(summary_path: Path) -> Path:
    if is_call_summary(summary_path):
        stem = summary_path.name[: -len(CALL_SUMMARY_SUFFIX)]
        return summary_path.with_name(f"{stem}{CALL_TRANSCRIPT_SUFFIX}")
    return summary_path.parent / "transcript.md"


def strip_process_markers(content: str) -> str:
    lines = [
        line for line in content.splitlines() if line.strip() not in PROCESS_MARKERS
    ]
    return "\n".join(lines).strip()
