#!/usr/bin/env python3
"""Apple-only STT regression comparison and release gate."""

from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import random
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import time
import unicodedata


class BenchmarkError(ValueError):
    pass


DEFAULT_MANIFEST_ROOT = Path.home() / ".config" / "stt" / "benchmarks"
DEFAULT_RUN_ROOT = Path.home() / ".voice-memos" / "benchmarks"
SAFE_RECORDING_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")


def canonical_hash(value: object) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _absolute(path: Path, base: Path | None = None) -> Path:
    expanded = path.expanduser()
    if not expanded.is_absolute():
        expanded = (base or Path.cwd()) / expanded
    return Path(os.path.abspath(expanded))


def _reject_unsafe_components(path: Path) -> None:
    current = Path(path.anchor)
    for part in path.parts[1:]:
        current /= part
        try:
            mode = current.lstat().st_mode
        except FileNotFoundError:
            break
        if stat.S_ISLNK(mode):
            raise BenchmarkError(f"symlink path component is not allowed: {current}")
        if current != path and not stat.S_ISDIR(mode):
            raise BenchmarkError(f"irregular path component is not allowed: {current}")


def _regular_file(path: Path, *, base: Path | None = None, label: str = "file") -> Path:
    candidate = _absolute(path, base)
    _reject_unsafe_components(candidate)
    try:
        mode = candidate.lstat().st_mode
    except FileNotFoundError as error:
        raise BenchmarkError(f"{label} does not exist: {candidate}") from error
    if not stat.S_ISREG(mode):
        raise BenchmarkError(f"{label} must be a regular file: {candidate}")
    return candidate


def _contained(path: Path, root: Path, *, label: str) -> tuple[Path, Path]:
    candidate, allowed = _absolute(path), _absolute(root)
    _reject_unsafe_components(allowed)
    _reject_unsafe_components(candidate)
    if candidate == allowed or not candidate.is_relative_to(allowed):
        raise BenchmarkError(f"{label} must be below approved root {allowed}")
    return candidate, allowed


def _private_directory(path: Path) -> None:
    created = False
    try:
        info = path.lstat()
    except FileNotFoundError:
        path.mkdir(parents=True, exist_ok=False, mode=0o700)
        path.chmod(0o700)
        info = path.lstat()
        created = True
    if stat.S_ISLNK(info.st_mode) or not stat.S_ISDIR(info.st_mode):
        raise BenchmarkError(f"private path must be a directory: {path}")
    if info.st_uid != os.getuid() or stat.S_IMODE(info.st_mode) != 0o700:
        action = "created" if created else "existing"
        raise BenchmarkError(f"{action} private directory must be owned by the current user with mode 0700")


def _private_parent(path: Path, root: Path) -> None:
    candidate, allowed = _contained(path, root, label="output")
    _private_directory(allowed)
    current = allowed
    for part in candidate.parent.relative_to(allowed).parts:
        current /= part
        _private_directory(current)


def _file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def normalize_surface(text: str) -> str:
    return re.sub(r"\s+", " ", unicodedata.normalize("NFC", text)).strip()


def normalize_content(text: str) -> str:
    return "".join(
        char
        for char in unicodedata.normalize("NFC", text)
        if not char.isspace() and not unicodedata.category(char).startswith("P")
    )


def edit_distance(left: str, right: str) -> int:
    if len(left) > len(right):
        left, right = right, left
    previous = list(range(len(left) + 1))
    for row, right_char in enumerate(right, 1):
        current = [row]
        for column, left_char in enumerate(left, 1):
            current.append(
                min(
                    current[-1] + 1,
                    previous[column] + 1,
                    previous[column - 1] + (left_char != right_char),
                )
            )
        previous = current
    return previous[-1]


def _byte_to_character(text: str, offset: int) -> int | None:
    if not isinstance(offset, int) or offset < 0:
        return None
    total = 0
    for index, char in enumerate(text):
        if total == offset:
            return index
        total += len(char.encode("utf-8"))
    return len(text) if total == offset else None


def map_reference_span(
    reference: str, hypothesis: str, start_byte: int, end_byte: int
) -> tuple[int, int] | None:
    """Map one reference-local UTF-8 span to a hypothesis-local UTF-8 span.

    Only a span contained by one equal/replace edit opcode is deterministic.
    Insertions, deletions, and spans crossing edit blocks remain unaligned.
    """

    start = _byte_to_character(reference, start_byte)
    end = _byte_to_character(reference, end_byte)
    if start is None or end is None or start >= end:
        return None
    for tag, ref_start, ref_end, hyp_start, hyp_end in difflib.SequenceMatcher(
        None, reference, hypothesis, autojunk=False
    ).get_opcodes():
        if ref_start <= start and end <= ref_end and tag in {"equal", "replace"} and hyp_start < hyp_end:
            if tag == "equal":
                hyp_start += start - ref_start
                hyp_end = hyp_start + (end - start)
            elif (ref_start, ref_end) != (start, end):
                return None
            return (
                len(hypothesis[:hyp_start].encode("utf-8")),
                len(hypothesis[:hyp_end].encode("utf-8")),
            )
    return None


def _validate_intervals(items: list[dict], label: str) -> list[dict]:
    seen: set[str] = set()
    clean: list[dict] = []
    for item in items:
        if not isinstance(item, dict):
            raise BenchmarkError(f"{label} entries must be objects")
        item_id = item.get("id")
        text = item.get("text")
        start = item.get("start_ms")
        end = item.get("end_ms")
        if not isinstance(item_id, str) or not item_id or item_id in seen:
            raise BenchmarkError(f"{label} ids must be non-empty and unique")
        if (
            not isinstance(text, str)
            or isinstance(start, bool)
            or not isinstance(start, (int, float))
            or isinstance(end, bool)
            or not isinstance(end, (int, float))
        ):
            raise BenchmarkError(f"{label} {item_id} has invalid text or time")
        try:
            finite = math.isfinite(start) and math.isfinite(end)
        except OverflowError:
            finite = False
        if not finite or start < 0 or start >= end:
            raise BenchmarkError(f"{label} {item_id} has invalid interval")
        seen.add(item_id)
        clean.append({"id": item_id, "text": text, "start_ms": float(start), "end_ms": float(end)})
    return clean


def align_components(gold: list[dict], hypothesis: list[dict]) -> list[dict]:
    """Build connected many-to-many components using half-open interval overlap."""

    gold = _validate_intervals(gold, "gold utterance")
    hypothesis = _validate_intervals(hypothesis, "hypothesis segment")
    nodes = [("gold", item) for item in gold] + [("hypothesis", item) for item in hypothesis]
    parent = list(range(len(nodes)))

    def find(index: int) -> int:
        while parent[index] != index:
            parent[index] = parent[parent[index]]
            index = parent[index]
        return index

    def union(left: int, right: int) -> None:
        left, right = find(left), find(right)
        if left != right:
            parent[right] = left

    active: list[int] = []
    for index in sorted(range(len(nodes)), key=lambda i: (nodes[i][1]["start_ms"], nodes[i][1]["end_ms"], i)):
        side, item = nodes[index]
        active = [other for other in active if nodes[other][1]["end_ms"] > item["start_ms"]]
        for other in active:
            other_side, other_item = nodes[other]
            if side != other_side and other_item["start_ms"] < item["end_ms"]:
                union(index, other)
        active.append(index)

    groups: dict[int, list[int]] = {}
    for index in range(len(nodes)):
        groups.setdefault(find(index), []).append(index)

    components: list[dict] = []
    for indices in groups.values():
        by_side = {
            side: sorted(
                [nodes[index][1] for index in indices if nodes[index][0] == side],
                key=lambda item: (item["start_ms"], item["end_ms"], item["id"]),
            )
            for side in ("gold", "hypothesis")
        }
        tied = any(
            len({(item["start_ms"], item["end_ms"]) for item in by_side[side]}) < len(by_side[side])
            for side in by_side
        )
        components.append(
            {
                **by_side,
                "start_ms": min(nodes[index][1]["start_ms"] for index in indices),
                "end_ms": max(nodes[index][1]["end_ms"] for index in indices),
                "manual_signoff_required": not all(by_side.values()) or tied,
            }
        )
    components.sort(key=lambda item: (item["start_ms"], item["end_ms"]))
    return components


def _read_json(path: Path, *, required: bool = True) -> dict:
    if not path.exists() and not required:
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise BenchmarkError(f"cannot read JSON {path}: {error}") from error
    if not isinstance(value, dict):
        raise BenchmarkError(f"{path} must contain one JSON object")
    return value


def _result_file(recording_id: str, value: object | None) -> str:
    relative = value if value is not None else f"recordings/{recording_id}.json"
    if not isinstance(relative, str) or not relative:
        raise BenchmarkError(f"recording {recording_id} has invalid result_file")
    path = Path(relative)
    if path.is_absolute() or ".." in path.parts or path.suffix != ".json":
        raise BenchmarkError(f"recording {recording_id} has unsafe result_file")
    return path.as_posix()


def _safe_result_path(run_dir: Path, recording: dict) -> Path:
    relative = _result_file(recording["id"], recording.get("result_file"))
    root = run_dir.resolve()
    candidate = (run_dir / relative).resolve()
    if not candidate.is_relative_to(root):
        raise BenchmarkError(f"recording {recording['id']} result_file escapes run directory")
    return candidate


def scaffold(metadata_path: Path, output_path: Path, allowed_root: Path) -> dict:
    metadata_file = _regular_file(metadata_path, label="scaffold metadata")
    output, root = _contained(output_path, allowed_root, label="manifest output")
    if output.exists() or output.is_symlink():
        raise BenchmarkError(f"manifest output already exists: {output}")
    value = _read_json(metadata_file)
    if value.get("schema_version") != 1 or not isinstance(value.get("recordings"), list):
        raise BenchmarkError("scaffold input must use schema_version 1 and contain recordings")

    recordings: list[dict] = []
    audio_hashes: set[str] = set()
    splits: set[str] = set()
    for raw in value["recordings"]:
        if not isinstance(raw, dict):
            raise BenchmarkError("scaffold recordings must be objects")
        recording_id = raw.get("id")
        split = raw.get("split")
        if not isinstance(recording_id, str) or not SAFE_RECORDING_ID.fullmatch(recording_id):
            raise BenchmarkError("scaffold recording ids must use letters, digits, dot, dash, or underscore")
        if split not in {"calibration", "evaluation"}:
            raise BenchmarkError(f"recording {recording_id} has invalid split")
        environment = raw.get("environment")
        speakers = raw.get("speaker_configuration")
        if not isinstance(environment, str) or not environment:
            raise BenchmarkError(f"recording {recording_id} needs environment")
        if not isinstance(speakers, str) or not speakers:
            raise BenchmarkError(f"recording {recording_id} needs speaker_configuration")
        audio_value = raw.get("audio_file")
        if not isinstance(audio_value, str) or not audio_value:
            raise BenchmarkError(f"recording {recording_id} needs audio_file")
        audio = _regular_file(Path(audio_value), base=metadata_file.parent, label=f"audio for {recording_id}")
        audio_hash = _file_hash(audio)
        if audio_hash in audio_hashes:
            raise BenchmarkError("one audio fingerprint appears more than once in scaffold input")

        context = raw.get("context")
        if context is not None and (
            not isinstance(context, list)
            or not all(isinstance(term, str) and term.strip() for term in context)
        ):
            raise BenchmarkError(f"recording {recording_id} context must be an array of strings")
        vocab_value = raw.get("vocab_file")
        vocab = None
        if vocab_value is not None:
            if not isinstance(vocab_value, str) or not vocab_value:
                raise BenchmarkError(f"recording {recording_id} has invalid vocab_file")
            vocab = _regular_file(Path(vocab_value), base=metadata_file.parent, label=f"vocab for {recording_id}")

        recording = {
            "id": recording_id,
            "split": split,
            "environment": environment,
            "speaker_configuration": speakers,
            "audio_file": str(audio),
            "audio_sha256": audio_hash,
            "result_file": _result_file(recording_id, raw.get("result_file")),
        }
        if vocab is not None:
            recording["vocab_file"] = str(vocab)
        if context is not None:
            recording["context"] = [term.strip() for term in context]
        recordings.append(recording)
        audio_hashes.add(audio_hash)
        splits.add(split)

    if splits != {"calibration", "evaluation"}:
        raise BenchmarkError("scaffold input needs explicit calibration and evaluation recordings")
    manifest = {"schema_version": 1, "recordings": recordings}
    _validate_manifest(manifest)
    _private_parent(output, root)
    _atomic_create(output, json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    return manifest


def _validate_manifest(value: dict) -> list[dict]:
    if value.get("schema_version") != 1 or not isinstance(value.get("recordings"), list):
        raise BenchmarkError("manifest must use schema_version 1 and contain recordings")
    seen_recordings: set[str] = set()
    seen_audio: dict[str, str] = {}
    seen_results: set[str] = set()
    recordings: list[dict] = []
    for raw in value["recordings"]:
        if not isinstance(raw, dict):
            raise BenchmarkError("recordings must be objects")
        recording_id = raw.get("id")
        split = raw.get("split")
        if not isinstance(recording_id, str) or not recording_id or recording_id in seen_recordings:
            raise BenchmarkError("recording ids must be non-empty and unique")
        if split not in {"calibration", "evaluation"}:
            raise BenchmarkError(f"recording {recording_id} has invalid split")
        if not isinstance(raw.get("environment"), str) or not raw["environment"]:
            raise BenchmarkError(f"recording {recording_id} needs environment")
        if not isinstance(raw.get("speaker_configuration"), str) or not raw["speaker_configuration"]:
            raise BenchmarkError(f"recording {recording_id} needs speaker_configuration")
        utterances = _validate_intervals(raw.get("utterances", []), f"recording {recording_id} utterance")
        utterance_ids = {item["id"] for item in utterances}
        named_terms = raw.get("named_terms", [])
        phrases = raw.get("required_phrases", [])
        targets = raw.get("correction_targets", [])
        if not all(isinstance(items, list) for items in (named_terms, phrases, targets)):
            raise BenchmarkError(f"recording {recording_id} annotations must be arrays")
        for annotation, key in [(item, "term") for item in named_terms] + [(item, "text") for item in phrases]:
            if not isinstance(annotation, dict) or not isinstance(annotation.get(key), str) or not annotation[key]:
                raise BenchmarkError(f"recording {recording_id} has invalid {key} annotation")
            if annotation.get("utterance_id") not in utterance_ids:
                raise BenchmarkError(f"recording {recording_id} annotation has unknown utterance_id")
        target_ids: set[str] = set()
        for target in targets:
            if (
                not isinstance(target, dict)
                or not isinstance(target.get("id"), str)
                or not target["id"]
                or target["id"] in target_ids
            ):
                raise BenchmarkError(f"recording {recording_id} has invalid correction target")
            target_ids.add(target.get("id"))
            if target.get("utterance_id") not in utterance_ids or target.get("label") not in {"replace", "no_change"}:
                raise BenchmarkError(f"recording {recording_id} correction target has invalid reference")
            utterance = next(item for item in utterances if item["id"] == target["utterance_id"])
            start, end = target.get("start_byte"), target.get("end_byte")
            if _byte_to_character(utterance["text"], start) is None or _byte_to_character(utterance["text"], end) is None or start >= end:
                raise BenchmarkError(f"recording {recording_id} correction target has invalid UTF-8 span")
            allowed = target.get("allowed_replacements", [])
            if target["label"] == "replace" and (not isinstance(allowed, list) or not allowed or not all(isinstance(x, str) and x for x in allowed)):
                raise BenchmarkError(f"recording {recording_id} replace target needs allowed_replacements")
        audio_hash = raw.get("audio_sha256")
        if not isinstance(audio_hash, str) or not re.fullmatch(r"[0-9a-f]{64}", audio_hash):
            raise BenchmarkError(f"recording {recording_id} has invalid audio_sha256")
        previous_split = seen_audio.get(audio_hash)
        if previous_split is not None:
            raise BenchmarkError("one audio fingerprint appears more than once in the manifest")
        result_file = _result_file(recording_id, raw.get("result_file"))
        if result_file in seen_results:
            raise BenchmarkError("one normalized result_file appears more than once in the manifest")
        seen_audio[audio_hash] = split
        seen_results.add(result_file)
        seen_recordings.add(recording_id)
        recordings.append({**raw, "utterances": utterances})
    return recordings


def _run_bundle_hash(run_dir: Path, recordings: list[dict]) -> str:
    files = {"run.json": _file_hash(_regular_file(run_dir / "run.json", label="run metadata"))}
    for recording in recordings:
        result = _safe_result_path(run_dir, recording)
        relative = result.relative_to(run_dir.resolve()).as_posix()
        files[relative] = _file_hash(_regular_file(result, label=f"result for {recording['id']}"))
    return canonical_hash(files)


def _load_run(run_dir: Path, recordings: list[dict], manifest_hash: str) -> dict:
    metadata = _read_json(run_dir / "run.json", required=False)
    if metadata and metadata.get("schema_version") != 1:
        raise BenchmarkError(f"{run_dir}/run.json must use schema_version 1")
    metadata_recordings = metadata.get("recordings", {})
    if metadata and not isinstance(metadata_recordings, dict):
        raise BenchmarkError(f"{run_dir}/run.json recordings must be an object")
    fingerprints = metadata.get("fingerprints", {})
    if metadata and not isinstance(fingerprints, dict):
        raise BenchmarkError(f"{run_dir}/run.json fingerprints must be an object")
    binary_hash = fingerprints.get("binary_sha256")
    locale = fingerprints.get("locale")
    macos_build = fingerprints.get("macos_build")
    config_hash = fingerprints.get("config_sha256")
    locale_model_state = fingerprints.get("locale_model_state")
    if metadata and (
        not isinstance(binary_hash, str)
        or not re.fullmatch(r"[0-9a-f]{64}", binary_hash)
        or not isinstance(locale, str)
        or not locale
        or locale.strip() != locale
        or not isinstance(macos_build, str)
        or not macos_build.strip()
        or not isinstance(config_hash, str)
        or not re.fullmatch(r"[0-9a-f]{64}", config_hash)
        or locale_model_state != "installed"
    ):
        raise BenchmarkError(f"{run_dir}/run.json has invalid runtime fingerprints")
    run_mode = metadata.get("result_mode")
    declared_adapter = metadata.get("benchmark_adapter")
    if metadata and run_mode not in {"strict", "legacy"}:
        raise BenchmarkError(f"{run_dir}/run.json must declare strict or legacy result_mode")
    if metadata and (
        (run_mode == "strict" and declared_adapter is not None)
        or (run_mode == "legacy" and not isinstance(declared_adapter, dict))
    ):
        raise BenchmarkError(f"{run_dir}/run.json result_mode does not match adapter provenance")

    results: dict[str, dict] = {}
    config_recordings: dict[str, dict] = {}
    for recording in recordings:
        result_path = _safe_result_path(run_dir, recording)
        value = _read_json(result_path)
        if (
            value.get("schema_version") != 1
            or value.get("engine") != "apple-speech-transcriber"
            or not isinstance(value.get("segments"), list)
        ):
            raise BenchmarkError(f"result for {recording['id']} is not analysis schema v1")
        run_recording = metadata_recordings.get(recording["id"], {})
        if metadata and not isinstance(run_recording, dict):
            raise BenchmarkError(f"run metadata for {recording['id']} must be an object")
        if metadata and run_recording.get("result_sha256") != _file_hash(result_path):
            raise BenchmarkError(f"result for {recording['id']} does not match run hash binding")
        if metadata and value.get("engine_version") != binary_hash:
            raise BenchmarkError(f"result for {recording['id']} does not match run binary")
        if metadata and value.get("locale") != locale:
            raise BenchmarkError(f"result for {recording['id']} does not match run locale")

        result_config = {
            "result_file": _result_file(recording["id"], recording.get("result_file"))
        }
        adapter = value.get("benchmark_adapter")
        result_mode = "legacy" if adapter is not None else "strict"
        if metadata and result_mode != run_mode:
            raise BenchmarkError(
                f"result for {recording['id']} does not match run result_mode"
            )
        if adapter is None:
            context = value.get("context")
            selected = context.get("selected") if isinstance(context, dict) else None
            dropped = context.get("dropped") if isinstance(context, dict) else None
            context_fingerprint = context.get("fingerprint") if isinstance(context, dict) else None
            if (
                not isinstance(selected, list)
                or len(selected) > 100
                or not all(isinstance(term, str) for term in selected)
                or not isinstance(dropped, list)
                or dropped
                or context_fingerprint
                != hashlib.sha256("\0".join(selected or []).encode("utf-8")).hexdigest()
            ):
                raise BenchmarkError(f"strict result for {recording['id']} has invalid context")
            if metadata and run_recording.get("context_fingerprint") != context_fingerprint:
                raise BenchmarkError(f"strict result for {recording['id']} does not match run context")
            result_config["context_fingerprint"] = context_fingerprint
        else:
            profile = adapter.get("vocab_input_profile") if isinstance(adapter, dict) else None
            counts = (
                profile.get("non_comment_entries"),
                profile.get("unique_exact_entries"),
                profile.get("exact_duplicate_entries"),
                profile.get("unique_casefold_entries"),
                profile.get("casefold_duplicate_entries"),
            ) if isinstance(profile, dict) else ()
            hint_counts = (
                profile.get("ambient_entries"),
                profile.get("explicit_entries"),
                profile.get("effective_hint_entries"),
            ) if isinstance(profile, dict) else ()
            if (
                not isinstance(adapter, dict)
                or adapter.get("name") != "apple-stt-legacy-json"
                or adapter.get("version") != 1
                or adapter.get("source_flag") != "--json"
                or adapter.get("duration_source") != "max_segment_end"
                or adapter.get("strict_analysis_compatible") is not False
                or adapter.get("script_sha256") != _file_hash(Path(__file__))
                or not isinstance(profile, dict)
                or not isinstance(profile.get("ambient_file_sha256"), str)
                or not re.fullmatch(r"[0-9a-f]{64}", profile["ambient_file_sha256"])
                or not isinstance(profile.get("explicit_file_sha256"), str)
                or not re.fullmatch(r"[0-9a-f]{64}", profile["explicit_file_sha256"])
                or profile["ambient_file_sha256"] != profile["explicit_file_sha256"]
                or len(counts) != 5
                or any(isinstance(count, bool) or not isinstance(count, int) or count < 0 for count in counts)
                or counts[1] + counts[2] != counts[0]
                or counts[3] + counts[4] != counts[0]
                or counts[3] > counts[1]
                or profile.get("deployed_voice_memos") is not True
                or profile.get("input_mode") != "ambient_plus_explicit_same_file"
                or len(hint_counts) != 3
                or any(
                    isinstance(count, bool) or not isinstance(count, int) or count < 0
                    for count in hint_counts
                )
                or hint_counts[0] != counts[0]
                or hint_counts[1] != counts[0]
                or hint_counts[2] != counts[0] * 2
                or profile.get("applied_terms_observable") is not False
                or declared_adapter != adapter
            ):
                raise BenchmarkError(f"legacy result for {recording['id']} has invalid adapter provenance")
            profile_hash = canonical_hash(profile)
            if metadata and run_recording.get("vocab_profile_sha256") != profile_hash:
                raise BenchmarkError(f"legacy result for {recording['id']} does not match vocab profile")
            result_config["vocab_profile_sha256"] = profile_hash

        segments = _analysis_segments(value["segments"], f"result {recording['id']} segment")
        source = value.get("source", {})
        if recording.get("audio_sha256") and source.get("audio_sha256") != recording["audio_sha256"]:
            raise BenchmarkError(f"result for {recording['id']} has wrong source audio")
        duration_ms = source.get("duration_ms")
        if (
            isinstance(duration_ms, bool)
            or not isinstance(duration_ms, (int, float))
            or not math.isfinite(duration_ms)
            or duration_ms <= 0
        ):
            raise BenchmarkError(f"result for {recording['id']} has invalid source duration")
        results[recording["id"]] = {"segments": segments, "duration_ms": float(duration_ms)}
        config_recordings[recording["id"]] = result_config

    if metadata:
        expected_ids = {recording["id"] for recording in recordings}
        if set(metadata_recordings) != expected_ids:
            raise BenchmarkError(f"{run_dir}/run.json recording bindings do not match manifest")
        expected_config = canonical_hash(
            {"locale": locale, "result_mode": run_mode, "recordings": config_recordings}
        )
        if fingerprints.get("config_sha256") != expected_config:
            raise BenchmarkError(f"{run_dir}/run.json config fingerprint does not match results")
    return {
        "metadata": metadata,
        "result_mode": run_mode,
        "manifest_match": metadata.get("manifest_sha256") == manifest_hash,
        "results": results,
        "recordings": metadata_recordings,
    }


def _ratio(numerator: int | float, denominator: int | float, *, interval: bool = False) -> dict:
    if denominator <= 0:
        return {"status": "insufficient_data", "numerator": numerator, "denominator": denominator, "value": None}
    value = numerator / denominator
    result = {"status": "ok", "numerator": numerator, "denominator": denominator, "value": value}
    if interval:
        z = 1.959963984540054
        scale = 1 + z * z / denominator
        center = (value + z * z / (2 * denominator)) / scale
        radius = z * math.sqrt(value * (1 - value) / denominator + z * z / (4 * denominator * denominator)) / scale
        result["interval_95"] = [max(0.0, center - radius), min(1.0, center + radius)]
    return result


def _union_duration(items: list[dict]) -> float:
    ranges = sorted((item["start_ms"], item["end_ms"]) for item in items)
    total = 0.0
    end = -1.0
    for start, next_end in ranges:
        if start >= end:
            total += next_end - start
        elif next_end > end:
            total += next_end - end
        end = max(end, next_end)
    return total


def _recording_metrics(recording: dict, run: dict, run_label: str) -> dict:
    result = run["results"][recording["id"]]
    metadata = run["recordings"].get(recording["id"], {})
    if not isinstance(metadata, dict):
        raise BenchmarkError(f"run metadata for {recording['id']} must be an object")
    components = align_components(recording["utterances"], result["segments"])
    utterance_component: dict[str, dict] = {}
    for component in components:
        for utterance in component["gold"]:
            utterance_component[utterance["id"]] = component

    surface_errors = surface_chars = content_errors = content_chars = 0
    alignment_issues: list[str] = []
    for index, component in enumerate(components, 1):
        reference = " ".join(item["text"] for item in component["gold"])
        hypothesis = " ".join(item["text"] for item in component["hypothesis"])
        surface_ref, surface_hyp = normalize_surface(reference), normalize_surface(hypothesis)
        content_ref, content_hyp = normalize_content(reference), normalize_content(hypothesis)
        surface_errors += edit_distance(surface_ref, surface_hyp)
        surface_chars += len(surface_ref)
        content_errors += edit_distance(content_ref, content_hyp)
        content_chars += len(content_ref)
        if component["manual_signoff_required"]:
            alignment_issues.append(f"{run_label}:{recording['id']}:c{index:04d}")

    named_found = 0
    for occurrence in recording.get("named_terms", []):
        component = utterance_component[occurrence["utterance_id"]]
        hypothesis = normalize_content(" ".join(item["text"] for item in component["hypothesis"]))
        named_found += normalize_content(occurrence["term"]) in hypothesis

    omissions = 0
    for phrase in recording.get("required_phrases", []):
        component = utterance_component[phrase["utterance_id"]]
        hypothesis = normalize_content(" ".join(item["text"] for item in component["hypothesis"]))
        omissions += normalize_content(phrase["text"]) not in hypothesis

    segment_by_id = {item["id"]: item for item in result["segments"]}
    candidate_ids = metadata.get("candidate_segment_ids", [])
    if not isinstance(candidate_ids, list) or not all(isinstance(item, str) for item in candidate_ids):
        raise BenchmarkError(f"candidate_segment_ids for {recording['id']} must be strings")
    if any(item not in segment_by_id for item in candidate_ids):
        raise BenchmarkError(f"candidate_segment_ids for {recording['id']} contains unknown id")
    candidate_set = set(candidate_ids)
    error_targets = [item for item in recording.get("correction_targets", []) if item["label"] == "replace"]
    covered = 0
    for target in error_targets:
        component = utterance_component[target["utterance_id"]]
        covered += any(item["id"] in candidate_set for item in component["hypothesis"])
    review_seconds = metadata.get("review_seconds", {})
    if not isinstance(review_seconds, dict):
        raise BenchmarkError(f"review_seconds for {recording['id']} must be an object")
    try:
        capped_review_seconds = sum(
            min(120.0, max(0.0, float(review_seconds.get(item, 0)))) for item in candidate_set
        )
    except (TypeError, ValueError) as error:
        raise BenchmarkError(f"review_seconds for {recording['id']} must be numeric") from error

    suggestions = metadata.get("suggestions", [])
    if not isinstance(suggestions, list):
        raise BenchmarkError(f"suggestions for {recording['id']} must be an array")
    target_by_id = {item["id"]: item for item in recording.get("correction_targets", [])}
    suggestion_counts = {
        "attempts": len(suggestions),
        "valid_non_abstaining": 0,
        "true_positive": 0,
        "approved": 0,
        "wrong_approved": 0,
        "invalid_or_refusal": 0,
        "abstention": 0,
        "transport_failure": 0,
    }
    for suggestion in suggestions:
        if not isinstance(suggestion, dict):
            raise BenchmarkError(f"suggestions for {recording['id']} must contain objects")
        status = suggestion.get("status")
        if status in {"invalid", "refusal"}:
            suggestion_counts["invalid_or_refusal"] += 1
            continue
        if status == "abstain":
            suggestion_counts["abstention"] += 1
            continue
        if status == "transport_failure":
            suggestion_counts["transport_failure"] += 1
            continue
        if status != "suggested" or not isinstance(suggestion.get("replacement"), str):
            raise BenchmarkError(f"suggestion for {recording['id']} has invalid status or replacement")
        suggestion_counts["valid_non_abstaining"] += 1
        target = target_by_id.get(suggestion.get("target_id"))
        true_positive = bool(
            target
            and target["label"] == "replace"
            and suggestion.get("alignment") == "aligned"
            and normalize_content(suggestion["replacement"])
            in {normalize_content(item) for item in target.get("allowed_replacements", [])}
        )
        suggestion_counts["true_positive"] += true_positive
        approved = suggestion.get("approved") is True
        suggestion_counts["approved"] += approved
        suggestion_counts["wrong_approved"] += approved and not true_positive

    correction = metadata.get("correction", {})
    if not isinstance(correction, dict):
        raise BenchmarkError(f"correction for {recording['id']} must be an object")
    correction_values = (
        correction.get("content_errors_before"),
        correction.get("content_errors_after"),
        correction.get("content_reference_chars"),
    )
    if any(value is not None and (not isinstance(value, int) or value < 0) for value in correction_values):
        raise BenchmarkError(f"correction counters for {recording['id']} must be non-negative integers")

    return {
        "surface_errors": surface_errors,
        "surface_chars": surface_chars,
        "content_errors": content_errors,
        "content_chars": content_chars,
        "named_found": named_found,
        "named_total": len(recording.get("named_terms", [])),
        "omissions": omissions,
        "required_phrases": len(recording.get("required_phrases", [])),
        "error_targets": len(error_targets),
        "candidate_errors_covered": covered,
        "segments": len(result["segments"]),
        "candidate_segments": len(candidate_set),
        "candidate_duration_ms": _union_duration([segment_by_id[item] for item in candidate_set]),
        "characters": sum(len(normalize_content(item["text"])) for item in result["segments"]),
        "candidate_characters": sum(len(normalize_content(segment_by_id[item]["text"])) for item in candidate_set),
        "audio_duration_ms": result["duration_ms"],
        "review_seconds": capped_review_seconds,
        "processing_seconds": metadata.get("processing_seconds"),
        "peak_memory_mb": metadata.get("peak_memory_mb"),
        "auto_applied_count": metadata.get("auto_applied_count"),
        "wrong_approved_count": (
            suggestion_counts["wrong_approved"] if suggestions else metadata.get("wrong_approved_count")
        ),
        "residual_error_count": metadata.get("residual_error_count"),
        "suggestions": suggestion_counts,
        "correction_errors_before": correction_values[0],
        "correction_errors_after": correction_values[1],
        "correction_reference_chars": correction_values[2],
        "alignment_issues": alignment_issues,
    }


def _aggregate(rows: list[dict]) -> dict:
    total = lambda key: sum(row[key] for row in rows)
    duration_ms = total("audio_duration_ms")
    processing = [row["processing_seconds"] for row in rows if isinstance(row["processing_seconds"], (int, float))]
    memory = [row["peak_memory_mb"] for row in rows if isinstance(row["peak_memory_mb"], (int, float))]
    auto_values = [row["auto_applied_count"] for row in rows if isinstance(row["auto_applied_count"], int)]
    wrong_values = [row["wrong_approved_count"] for row in rows if isinstance(row["wrong_approved_count"], int)]
    residual_values = [row["residual_error_count"] for row in rows if isinstance(row["residual_error_count"], int)]
    suggestion_total = lambda key: sum(row["suggestions"][key] for row in rows)
    correction_ready = all(
        isinstance(row[key], int)
        for row in rows
        for key in ("correction_errors_before", "correction_errors_after", "correction_reference_chars")
    )
    correction_denominator = total("correction_reference_chars") if correction_ready else 0
    correction_delta = (
        _ratio(total("correction_errors_after") - total("correction_errors_before"), correction_denominator)
        if correction_ready
        else {"status": "insufficient_data", "numerator": None, "denominator": None, "value": None}
    )
    return {
        "recordings": len(rows),
        "surface_cer": _ratio(total("surface_errors"), total("surface_chars")),
        "content_cer": _ratio(total("content_errors"), total("content_chars")),
        "named_term_recall": _ratio(total("named_found"), total("named_total"), interval=True),
        "omissions": _ratio(total("omissions"), total("required_phrases")),
        "candidate_error_recall": _ratio(total("candidate_errors_covered"), total("error_targets"), interval=True),
        "candidate_segment_ratio": _ratio(total("candidate_segments"), total("segments")),
        "candidate_duration_ratio": _ratio(total("candidate_duration_ms"), duration_ms),
        "candidate_character_ratio": _ratio(total("candidate_characters"), total("characters")),
        "active_review_minutes_per_audio_hour": _ratio(total("review_seconds") / 60, duration_ms / 3_600_000),
        "processing_seconds": {"status": "ok" if len(processing) == len(rows) else "insufficient_data", "total": sum(processing)},
        "peak_memory_mb": {"status": "ok" if len(memory) == len(rows) else "insufficient_data", "maximum": max(memory, default=None)},
        "auto_applied_count": {"status": "ok" if len(auto_values) == len(rows) else "insufficient_data", "value": sum(auto_values) if len(auto_values) == len(rows) else None},
        "wrong_approved_count": {"status": "ok" if len(wrong_values) == len(rows) else "insufficient_data", "value": sum(wrong_values) if len(wrong_values) == len(rows) else None},
        "residual_error_count": {"status": "ok" if len(residual_values) == len(rows) else "insufficient_data", "value": sum(residual_values) if len(residual_values) == len(rows) else None},
        "correction_content_cer_delta": correction_delta,
        "claude_suggestions": {
            "precision": _ratio(suggestion_total("true_positive"), suggestion_total("valid_non_abstaining"), interval=True),
            "approval_rate": _ratio(suggestion_total("approved"), suggestion_total("valid_non_abstaining"), interval=True),
            "invalid_refusal_rate": _ratio(suggestion_total("invalid_or_refusal"), suggestion_total("attempts"), interval=True),
            **({key: suggestion_total(key) for key in rows[0]["suggestions"]} if rows else {}),
        },
        "alignment_issue_ids": [item for row in rows for item in row["alignment_issues"]],
        "denominators": {"error_targets": total("error_targets"), "named_term_occurrences": total("named_total")},
    }


def _bootstrap_delta(baseline: list[dict], candidate: list[dict], numerator: str, denominator: str) -> dict:
    if not baseline or len(baseline) != len(candidate):
        return {"status": "insufficient_data", "value": None, "interval_95": None}
    base_den = sum(row[denominator] for row in baseline)
    cand_den = sum(row[denominator] for row in candidate)
    if base_den <= 0 or cand_den <= 0:
        return {"status": "insufficient_data", "value": None, "interval_95": None}
    point = sum(row[numerator] for row in candidate) / cand_den - sum(row[numerator] for row in baseline) / base_den
    rng = random.Random(0)
    samples = []
    for _ in range(1000):
        indices = [rng.randrange(len(baseline)) for _ in baseline]
        sampled_base_den = sum(baseline[i][denominator] for i in indices)
        sampled_cand_den = sum(candidate[i][denominator] for i in indices)
        if sampled_base_den and sampled_cand_den:
            samples.append(
                sum(candidate[i][numerator] for i in indices) / sampled_cand_den
                - sum(baseline[i][numerator] for i in indices) / sampled_base_den
            )
    samples.sort()
    return {
        "status": "ok",
        "value": point,
        "interval_95": [samples[int(0.025 * (len(samples) - 1))], samples[int(0.975 * (len(samples) - 1))]],
    }


def _changed_segments(recordings: list[dict], baseline: dict, candidate: dict) -> list[str]:
    changed = []
    for recording in recordings:
        recording_id = recording["id"]
        left = {item["id"]: item for item in baseline["results"][recording_id]["segments"]}
        right = {item["id"]: item for item in candidate["results"][recording_id]["segments"]}
        for segment_id in sorted(left.keys() | right.keys()):
            if left.get(segment_id) != right.get(segment_id):
                changed.append(f"{recording_id}:{segment_id}")
    return changed


def _gate(name: str, passed: bool | None, detail: str) -> dict:
    return {"name": name, "status": "insufficient_data" if passed is None else ("pass" if passed else "fail"), "detail": detail}


def _macos_build() -> str:
    sw_vers = shutil.which("sw_vers")
    if sw_vers:
        completed = subprocess.run(
            [sw_vers, "-buildVersion"], text=True, capture_output=True, check=False
        )
        if completed.returncode == 0 and completed.stdout.strip():
            return completed.stdout.strip()
    return platform.platform()


def _analysis_segments(value: object, label: str) -> list[dict]:
    if not isinstance(value, list) or not value:
        raise BenchmarkError(f"{label} needs timed segments")
    converted = []
    for segment in value:
        if not isinstance(segment, dict):
            raise BenchmarkError(f"{label} has invalid segment")
        start, end, segment_text = segment.get("start"), segment.get("end"), segment.get("text")
        if (
            isinstance(start, bool)
            or not isinstance(start, (int, float))
            or isinstance(end, bool)
            or not isinstance(end, (int, float))
            or not isinstance(segment_text, str)
            or not segment_text.strip()
        ):
            raise BenchmarkError(f"{label} has invalid segment")
        converted.append(
            {
                "id": segment.get("id"),
                "start_ms": start * 1000,
                "end_ms": end * 1000,
                "text": segment_text,
            }
        )
    return _validate_intervals(converted, label)


def _capture_result(value: object, recording: dict, binary_hash: str, locale: str) -> dict:
    if not isinstance(value, dict):
        raise BenchmarkError(f"capture for {recording['id']} did not return a JSON object")
    source = value.get("source")
    context = value.get("context")
    selected = context.get("selected") if isinstance(context, dict) else None
    dropped = context.get("dropped") if isinstance(context, dict) else None
    context_fingerprint = context.get("fingerprint") if isinstance(context, dict) else None
    duration_ms = source.get("duration_ms") if isinstance(source, dict) else None
    if (
        value.get("schema_version") != 1
        or value.get("engine") != "apple-speech-transcriber"
        or value.get("engine_version") != binary_hash
        or value.get("locale") != locale
        or not isinstance(value.get("segments"), list)
        or not value.get("segments")
        or not isinstance(source, dict)
        or source.get("audio_sha256") != recording["audio_sha256"]
        or not isinstance(context, dict)
        or isinstance(duration_ms, bool)
        or not isinstance(duration_ms, (int, float))
        or not math.isfinite(duration_ms)
        or duration_ms <= 0
        or not isinstance(selected, list)
        or not all(isinstance(term, str) for term in selected)
        or len(selected) > 100
        or not isinstance(dropped, list)
        or not all(isinstance(term, str) for term in dropped)
        or context_fingerprint
        != hashlib.sha256("\0".join(selected or []).encode("utf-8")).hexdigest()
    ):
        raise BenchmarkError(f"capture for {recording['id']} is not bound Apple analysis schema v1")
    if dropped:
        raise BenchmarkError(f"capture context for {recording['id']} exceeds Apple limits")
    _analysis_segments(value["segments"], f"capture {recording['id']} segment")
    return value


def _vocab_input_profile(
    text: str, explicit_file_sha256: str, ambient_file_sha256: str
) -> dict:
    entries = [
        line.strip()
        for line in text.splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]
    exact = set(entries)
    casefolded = {entry.casefold() for entry in entries}
    return {
        "ambient_file_sha256": ambient_file_sha256,
        "explicit_file_sha256": explicit_file_sha256,
        "deployed_voice_memos": True,
        "input_mode": "ambient_plus_explicit_same_file",
        "non_comment_entries": len(entries),
        "ambient_entries": len(entries),
        "explicit_entries": len(entries),
        "effective_hint_entries": len(entries) * 2,
        "unique_exact_entries": len(exact),
        "exact_duplicate_entries": len(entries) - len(exact),
        "unique_casefold_entries": len(casefolded),
        "casefold_duplicate_entries": len(entries) - len(casefolded),
        "applied_terms_observable": False,
    }


def _legacy_capture_result(
    value: object,
    recording: dict,
    binary_hash: str,
    locale: str,
    adapter: dict,
) -> dict:
    if not isinstance(value, list) or not value:
        raise BenchmarkError(f"legacy capture for {recording['id']} needs timed segments")
    segments = []
    for index, segment in enumerate(value, 1):
        if not isinstance(segment, dict) or set(segment) != {"start", "end", "text"}:
            raise BenchmarkError(f"legacy capture for {recording['id']} has invalid segments")
        start, end, segment_text = segment["start"], segment["end"], segment["text"]
        if (
            isinstance(start, bool)
            or not isinstance(start, (int, float))
            or isinstance(end, bool)
            or not isinstance(end, (int, float))
            or not isinstance(segment_text, str)
            or not segment_text.strip()
        ):
            raise BenchmarkError(f"legacy capture for {recording['id']} has invalid segments")
        segments.append(
            {
                "id": f"s{index:04d}",
                "start_ms": start * 1000,
                "end_ms": end * 1000,
                "text": segment_text.strip(),
            }
        )
    clean = _validate_intervals(segments, f"legacy capture {recording['id']} segment")
    return {
        "schema_version": 1,
        "engine": "apple-speech-transcriber",
        "engine_version": binary_hash,
        "locale": locale,
        "source": {
            "audio_sha256": recording["audio_sha256"],
            "duration_ms": max(1, round(max(segment["end_ms"] for segment in clean))),
        },
        "benchmark_adapter": adapter,
        "segments": [
            {
                "id": segment["id"],
                "start": segment["start_ms"] / 1000,
                "end": segment["end_ms"] / 1000,
                "text": segment["text"],
            }
            for segment in clean
        ],
    }


def capture(
    manifest_path: Path,
    binary_path: Path,
    run_dir: Path,
    locale: str,
    manifest_root: Path,
    run_root: Path,
    vocab_override: Path | None = None,
    legacy_json: bool = False,
) -> dict:
    manifest_file, _ = _contained(manifest_path, manifest_root, label="capture manifest")
    manifest_file = _regular_file(manifest_file, label="capture manifest")
    target, approved_run_root = _contained(run_dir, run_root, label="capture run directory")
    if os.path.lexists(target):
        raise BenchmarkError(f"capture run directory already exists: {target}")
    if not locale or any(char.isspace() for char in locale):
        raise BenchmarkError("capture locale must be one BCP-47 identifier")

    try:
        binary = _regular_file(_absolute(binary_path).resolve(strict=True), label="Apple STT binary")
    except (FileNotFoundError, OSError) as error:
        raise BenchmarkError(f"Apple STT binary does not exist: {binary_path}") from error
    if not os.access(binary, os.X_OK):
        raise BenchmarkError(f"Apple STT binary is not executable: {binary}")
    binary_hash = _file_hash(binary)

    override: Path | None = None
    override_text = None
    override_hash = None
    if vocab_override is not None:
        override = _regular_file(vocab_override, label="capture vocab override")
        try:
            override_bytes = override.read_bytes()
            override_text = override_bytes.decode("utf-8")
        except UnicodeDecodeError as error:
            raise BenchmarkError("capture vocab override must be UTF-8") from error
        override_hash = hashlib.sha256(override_bytes).hexdigest()
    if legacy_json and override_text is None:
        raise BenchmarkError("legacy JSON capture requires an explicit frozen vocab file")

    ambient_vocab: Path | None = None
    ambient_hash: str | None = None
    if legacy_json:
        ambient_vocab = _regular_file(
            Path.home() / ".config" / "stt" / "vocab.txt",
            label="deployed ambient vocab",
        )
        ambient_hash = _file_hash(ambient_vocab)
        if ambient_hash != override_hash:
            raise BenchmarkError(
                "legacy JSON capture vocab must match the deployed ambient vocab snapshot"
            )

    adapter = None
    if legacy_json:
        adapter = {
            "name": "apple-stt-legacy-json",
            "version": 1,
            "source_flag": "--json",
            "duration_source": "max_segment_end",
            "strict_analysis_compatible": False,
            "script_sha256": _file_hash(Path(__file__)),
            "vocab_input_profile": _vocab_input_profile(
                override_text or "", override_hash or "", ambient_hash or ""
            ),
        }

    manifest = _read_json(manifest_file)
    recordings = _validate_manifest(manifest)
    _private_parent(target, approved_run_root)
    stage = Path(tempfile.mkdtemp(prefix=f".{target.name}.", dir=target.parent))
    stage.chmod(0o700)
    per_recording: dict[str, dict] = {}
    config_recordings: dict[str, dict] = {}

    def verify_legacy_vocab_snapshot() -> None:
        if not legacy_json:
            return
        assert ambient_vocab is not None and override is not None and override_hash is not None
        for vocab, label in (
            (ambient_vocab, "deployed ambient vocab"),
            (override, "capture vocab override"),
        ):
            current = _regular_file(vocab, label=label)
            if _file_hash(current) != override_hash:
                raise BenchmarkError("legacy JSON vocab snapshot changed during capture")

    try:
        for recording in recordings:
            audio_value = recording.get("audio_file")
            if not isinstance(audio_value, str) or not audio_value:
                raise BenchmarkError(f"capture recording {recording['id']} needs audio_file")
            audio = _regular_file(
                Path(audio_value), base=manifest_file.parent, label=f"audio for {recording['id']}"
            )
            if _file_hash(audio) != recording["audio_sha256"]:
                raise BenchmarkError(f"audio fingerprint changed for {recording['id']}")
            verify_legacy_vocab_snapshot()

            context_parts: list[str] = [] if override_text is None else [override_text]
            if override_text is None:
                vocab_value = recording.get("vocab_file")
                if vocab_value is not None:
                    if not isinstance(vocab_value, str) or not vocab_value:
                        raise BenchmarkError(f"recording {recording['id']} has invalid vocab_file")
                    vocab = _regular_file(
                        Path(vocab_value), base=manifest_file.parent, label=f"vocab for {recording['id']}"
                    )
                    try:
                        context_parts.append(vocab.read_text(encoding="utf-8"))
                    except UnicodeError as error:
                        raise BenchmarkError(f"vocab for {recording['id']} must be UTF-8") from error
                inline = recording.get("context", [])
                if not isinstance(inline, list) or not all(isinstance(term, str) and term.strip() for term in inline):
                    raise BenchmarkError(f"recording {recording['id']} context must be an array of strings")
                context_parts.extend(term.strip() for term in inline)

            with tempfile.NamedTemporaryFile(
                "w", encoding="utf-8", dir=stage, prefix=".context-", delete=False
            ) as handle:
                handle.write("\n".join(context_parts))
                context_path = Path(handle.name)
            context_path.chmod(0o600)
            command = [
                str(binary),
                "--json" if legacy_json else "--analysis-json",
                "--quiet",
                "--locale",
                locale,
                "--vocab-file",
                str(context_path),
                str(audio),
            ]
            started = time.monotonic()
            try:
                completed = subprocess.run(command, text=True, capture_output=True, check=False)
            except OSError as error:
                raise BenchmarkError(f"Apple capture could not start for {recording['id']}") from error
            finally:
                context_path.unlink(missing_ok=True)
            processing_seconds = time.monotonic() - started
            verify_legacy_vocab_snapshot()
            if completed.returncode != 0:
                raise BenchmarkError(
                    f"Apple capture failed for {recording['id']} with exit {completed.returncode}"
                )
            try:
                analysis = json.loads(completed.stdout)
            except json.JSONDecodeError as error:
                raise BenchmarkError(f"Apple capture returned invalid JSON for {recording['id']}") from error
            analysis = (
                _legacy_capture_result(analysis, recording, binary_hash, locale, adapter)
                if adapter is not None
                else _capture_result(analysis, recording, binary_hash, locale)
            )
            if _file_hash(audio) != recording["audio_sha256"] or _file_hash(binary) != binary_hash:
                raise BenchmarkError(f"capture inputs changed while processing {recording['id']}")

            result_path = _safe_result_path(stage, recording)
            _private_parent(result_path, stage)
            _atomic_write(result_path, json.dumps(analysis, ensure_ascii=False, indent=2) + "\n")
            per_recording[recording["id"]] = {
                "candidate_segment_ids": [],
                "review_seconds": {},
                "processing_seconds": processing_seconds,
                "peak_memory_mb": None,
                "auto_applied_count": 0,
                "wrong_approved_count": 0,
                "residual_error_count": None,
                "result_sha256": _file_hash(result_path),
            }
            config_recordings[recording["id"]] = {
                "result_file": _result_file(recording["id"], recording.get("result_file"))
            }
            if adapter is None:
                context_fingerprint = analysis["context"]["fingerprint"]
                per_recording[recording["id"]]["context_fingerprint"] = context_fingerprint
                config_recordings[recording["id"]]["context_fingerprint"] = context_fingerprint
            else:
                profile_hash = canonical_hash(adapter["vocab_input_profile"])
                per_recording[recording["id"]]["vocab_profile_sha256"] = profile_hash
                config_recordings[recording["id"]]["vocab_profile_sha256"] = profile_hash

        result_mode = "legacy" if adapter is not None else "strict"
        run = {
            "schema_version": 1,
            "result_mode": result_mode,
            "manifest_sha256": canonical_hash(manifest),
            "fingerprints": {
                "binary_sha256": binary_hash,
                "macos_build": _macos_build(),
                "locale": locale,
                "config_sha256": canonical_hash(
                    {
                        "locale": locale,
                        "result_mode": result_mode,
                        "recordings": config_recordings,
                    }
                ),
                "locale_model_state": "installed",
            },
            "recordings": per_recording,
        }
        if adapter is not None:
            run["benchmark_adapter"] = adapter
        _atomic_write(stage / "run.json", json.dumps(run, ensure_ascii=False, indent=2) + "\n")
        if os.path.lexists(target):
            raise BenchmarkError(f"capture run directory already exists: {target}")
        stage.rename(target)
        target.chmod(0o700)
        return run
    finally:
        if stage.exists():
            shutil.rmtree(stage)


def compare(
    manifest_path: Path,
    baseline_dir: Path,
    candidate_dir: Path,
    *,
    profile: str = "full",
    expect_context_only_change: bool = False,
) -> dict:
    if profile not in {"full", "transcription"}:
        raise BenchmarkError("compare profile must be full or transcription")
    manifest = _read_json(manifest_path)
    recordings = _validate_manifest(manifest)
    manifest_hash = canonical_hash(manifest)
    split_hashes = {
        split: canonical_hash([item for item in manifest["recordings"] if item["split"] == split])
        for split in ("calibration", "evaluation")
    }
    baseline = _load_run(baseline_dir, recordings, manifest_hash)
    candidate = _load_run(candidate_dir, recordings, manifest_hash)
    rows: dict[str, dict[str, list[dict]]] = {label: {} for label in ("baseline", "candidate")}
    for label, run in (("baseline", baseline), ("candidate", candidate)):
        for split in ("calibration", "evaluation"):
            rows[label][split] = [
                _recording_metrics(item, run, label)
                for item in recordings
                if item["split"] == split
            ]
    metrics = {
        split: {label: _aggregate(rows[label][split]) for label in ("baseline", "candidate")}
        for split in ("calibration", "evaluation")
    }
    deltas = {
        "content_cer": _bootstrap_delta(
            rows["baseline"]["evaluation"], rows["candidate"]["evaluation"], "content_errors", "content_chars"
        ),
        "named_term_recall": _bootstrap_delta(
            rows["baseline"]["evaluation"], rows["candidate"]["evaluation"], "named_found", "named_total"
        ),
    }
    changed = _changed_segments([item for item in recordings if item["split"] == "evaluation"], baseline, candidate)
    signoff = _read_json(candidate_dir / "signoff.json", required=False)
    expected_signoff = {
        "schema_version": 1,
        "manifest_sha256": manifest_hash,
        "baseline_bundle_sha256": _run_bundle_hash(baseline_dir, recordings),
        "candidate_bundle_sha256": _run_bundle_hash(candidate_dir, recordings),
    }
    signoff_bound = (
        None
        if not signoff
        else all(signoff.get(key) == expected for key, expected in expected_signoff.items())
    )

    gold_signoff = _read_json(manifest_path.with_name("gold-signoff.json"), required=False)
    expected_recording_ids = sorted(item["id"] for item in recordings)
    gold_recording_ids = gold_signoff.get("recording_ids") if gold_signoff else None
    gold_bound = (
        None
        if not gold_signoff
        else gold_signoff.get("schema_version") == 1
        and gold_signoff.get("manifest_sha256") == manifest_hash
        and isinstance(gold_recording_ids, list)
        and all(isinstance(item, str) for item in gold_recording_ids)
        and len(gold_recording_ids) == len(set(gold_recording_ids))
        and set(gold_recording_ids) == set(expected_recording_ids)
        and gold_signoff.get("human_verified") is True
    )

    def signoff_values(key: str) -> set[str]:
        values = signoff.get(key, [])
        if not isinstance(values, list) or not all(isinstance(item, str) for item in values):
            raise BenchmarkError(f"signoff.json {key} must be an array of strings")
        return set(values)

    signed_changed = signoff_values("changed_segment_ids")
    signed_alignment = signoff_values("alignment_issue_ids")
    alignment_issues = (
        metrics["evaluation"]["baseline"]["alignment_issue_ids"]
        + metrics["evaluation"]["candidate"]["alignment_issue_ids"]
    )
    missing_signoff = sorted(set(changed) - signed_changed)
    missing_alignment_signoff = sorted(set(alignment_issues) - signed_alignment)

    gates: list[dict] = []
    gates.append(_gate("human_gold_signoff", gold_bound, f"{len(expected_recording_ids)} recording ids"))
    for split in ("calibration", "evaluation"):
        split_recordings = [item for item in recordings if item["split"] == split]
        split_gates = [
            _gate(f"{split}_recordings", True if len(split_recordings) >= 6 else None, f"{len(split_recordings)}/6"),
            _gate(f"{split}_environments", True if len({item['environment'] for item in split_recordings}) >= 3 else None, f"{len({item['environment'] for item in split_recordings})}/3"),
            _gate(f"{split}_speaker_configurations", True if len({item['speaker_configuration'] for item in split_recordings}) >= 2 else None, f"{len({item['speaker_configuration'] for item in split_recordings})}/2"),
            _gate(f"{split}_named_terms", True if metrics[split]["candidate"]["denominators"]["named_term_occurrences"] >= 50 else None, f"{metrics[split]['candidate']['denominators']['named_term_occurrences']}/50"),
        ]
        if profile == "full":
            split_gates.append(
                _gate(f"{split}_error_targets", True if metrics[split]["candidate"]["denominators"]["error_targets"] >= 50 else None, f"{metrics[split]['candidate']['denominators']['error_targets']}/50")
            )
        gates.extend(split_gates)
    gates.append(_gate("baseline_manifest_match", baseline["manifest_match"] if baseline["metadata"] else None, manifest_hash))
    gates.append(_gate("candidate_manifest_match", candidate["manifest_match"] if candidate["metadata"] else None, manifest_hash))
    fingerprint_keys = {"binary_sha256", "macos_build", "config_sha256", "locale", "locale_model_state"}
    for label, run in (("baseline", baseline), ("candidate", candidate)):
        fingerprints = run["metadata"].get("fingerprints", {})
        complete = isinstance(fingerprints, dict) and fingerprint_keys <= fingerprints.keys()
        gates.append(_gate(f"{label}_fingerprints", True if complete else None, ", ".join(sorted(fingerprint_keys))))
    if expect_context_only_change:
        baseline_fingerprints = baseline["metadata"].get("fingerprints", {})
        candidate_fingerprints = candidate["metadata"].get("fingerprints", {})
        same_keys = {"binary_sha256", "macos_build", "locale", "locale_model_state"}
        fingerprints_ready = all(
            isinstance(values, dict) and fingerprint_keys <= values.keys()
            for values in (baseline_fingerprints, candidate_fingerprints)
        )
        strict_pair = baseline["result_mode"] == candidate["result_mode"] == "strict"
        context_only = None
        if fingerprints_ready:
            context_only = strict_pair and all(
                baseline_fingerprints[key] == candidate_fingerprints[key]
                for key in same_keys
            ) and baseline_fingerprints["config_sha256"] != candidate_fingerprints["config_sha256"]
        gates.append(
            _gate(
                "context_only_change",
                context_only,
                "same binary, macOS, locale/model; different bound config",
            )
        )

    thresholds = candidate["metadata"].get("frozen_thresholds", {})
    required_thresholds = {
        "candidate_error_recall_min",
        "candidate_segment_ratio_max",
        "candidate_duration_ratio_max",
        "candidate_character_ratio_max",
        "review_minutes_per_audio_hour_max",
        "calibration_split_sha256",
    }
    thresholds_ready = isinstance(thresholds, dict) and required_thresholds <= thresholds.keys()
    if profile == "full":
        gates.append(_gate("frozen_calibration_thresholds", thresholds_ready and thresholds["calibration_split_sha256"] == split_hashes["calibration"] if thresholds_ready else None, split_hashes["calibration"]))

    evaluation = metrics["evaluation"]["candidate"]
    content_delta = deltas["content_cer"]
    named_delta = deltas["named_term_recall"]
    gates.append(_gate("content_cer_regression", content_delta["interval_95"][1] <= 0.005 if content_delta["status"] == "ok" else None, "upper 95% delta <= 0.005"))
    gates.append(_gate("named_term_regression", named_delta["interval_95"][0] >= 0 if named_delta["status"] == "ok" else None, "lower 95% delta >= 0"))
    if content_delta["status"] == "ok" and named_delta["status"] == "ok":
        improvement = content_delta["value"] < 0 or named_delta["value"] > 0
    else:
        improvement = None
    gates.append(_gate("primary_metric_improvement", improvement, "content CER decreases or named-term recall increases"))

    def metric_gate(name: str, metric: str, threshold: str, mode: str, hard_limit: float | None = None) -> None:
        value = evaluation[metric]["value"]
        if not thresholds_ready or value is None or not isinstance(thresholds.get(threshold), (int, float)):
            passed = None
        else:
            limit = thresholds[threshold]
            if hard_limit is not None:
                limit = max(limit, hard_limit) if mode == "min" else min(limit, hard_limit)
            passed = value >= limit if mode == "min" else value <= limit
        gates.append(_gate(name, passed, f"{metric} vs frozen {threshold}"))

    if profile == "full":
        metric_gate("candidate_error_recall", "candidate_error_recall", "candidate_error_recall_min", "min", 0.8)
        metric_gate("candidate_segment_ratio", "candidate_segment_ratio", "candidate_segment_ratio_max", "max", 0.1)
        metric_gate("candidate_duration_ratio", "candidate_duration_ratio", "candidate_duration_ratio_max", "max")
        metric_gate("candidate_character_ratio", "candidate_character_ratio", "candidate_character_ratio_max", "max")
        metric_gate("active_review_time", "active_review_minutes_per_audio_hour", "review_minutes_per_audio_hour_max", "max")

        auto = evaluation["auto_applied_count"]
        wrong = evaluation["wrong_approved_count"]
        gates.append(_gate("zero_auto_applied", auto["value"] == 0 if auto["status"] == "ok" else None, "auto_applied_count == 0"))
        gates.append(_gate("zero_wrong_approved", wrong["value"] == 0 if wrong["status"] == "ok" else None, "wrong_approved_count == 0"))
    gates.append(_gate("signoff_bundle", signoff_bound, "manifest plus baseline and candidate bundles"))
    gates.append(_gate("changed_segment_signoff", not missing_signoff, f"missing {len(missing_signoff)}"))
    gates.append(_gate("alignment_signoff", not missing_alignment_signoff, f"missing {len(missing_alignment_signoff)}"))

    requested_features = candidate["metadata"].get("requested_features", [])
    if not isinstance(requested_features, list) or not all(isinstance(item, str) for item in requested_features):
        raise BenchmarkError("candidate run requested_features must be an array of strings")
    claude = evaluation["claude_suggestions"]
    claude_gate = {"status": "not_requested", "required_non_abstaining": 30}
    if profile == "transcription":
        claude_gate = {"status": "not_evaluated", "required_non_abstaining": 30}
    elif "claude_suggestions" in requested_features:
        enough = claude.get("valid_non_abstaining", 0) >= 30
        gates.append(_gate("claude_suggestion_denominator", True if enough else None, f"{claude.get('valid_non_abstaining', 0)}/30"))
        gates.append(_gate("claude_suggestion_precision", claude["precision"]["value"] >= 0.8 if enough else None, "precision >= 0.8"))
        invalid_rate = claude["invalid_refusal_rate"]["value"]
        gates.append(_gate("claude_invalid_refusal_rate", invalid_rate <= 0.1 if invalid_rate is not None else None, "invalid/refusal rate <= 0.1"))
        claude_fingerprints = candidate["metadata"].get("claude_fingerprints", {})
        required_claude_fingerprints = {
            "model_id",
            "cli_version",
            "sdk_version",
            "uv_lock_sha256",
            "prompt_sha256",
            "schema_sha256",
            "batch_size",
            "retry_count",
            "client_mode",
        }
        fingerprints_complete = (
            isinstance(claude_fingerprints, dict)
            and required_claude_fingerprints <= claude_fingerprints.keys()
        )
        gates.append(_gate("claude_fingerprints", True if fingerprints_complete else None, ", ".join(sorted(required_claude_fingerprints))))
        claude_gate = {"status": "required", "required_non_abstaining": 30}

    statuses = {item["status"] for item in gates}
    overall = "fail" if "fail" in statuses else ("insufficient_data" if "insufficient_data" in statuses else "pass")
    return {
        "schema_version": 1,
        "profile": profile,
        "status": overall,
        "manifest_sha256": manifest_hash,
        "split_sha256": split_hashes,
        "fingerprints": {
            "baseline": baseline["metadata"].get("fingerprints", {}),
            "candidate": candidate["metadata"].get("fingerprints", {}),
        },
        "frozen_thresholds": thresholds,
        "metrics": metrics,
        "evaluation_deltas": deltas,
        "changed_segment_ids": changed,
        "manual_signoff": {
            "missing_changed_segment_ids": missing_signoff,
            "missing_alignment_issue_ids": missing_alignment_signoff,
        },
        "signoff_binding": expected_signoff,
        "claude_enablement": claude_gate,
        "gates": gates,
    }


def _markdown(report: dict) -> str:
    lines = [
        "# Apple-only STT benchmark",
        "",
        f"Status: **{report['status']}**",
        "",
        "| Gate | Status | Detail |",
        "|---|---|---|",
    ]
    lines.extend(f"| {item['name']} | {item['status']} | {item['detail']} |" for item in report["gates"])
    lines.extend(["", f"Changed evaluation segments: {len(report['changed_segment_ids'])}", ""])
    return "\n".join(lines)


def _atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as handle:
        handle.write(content)
        handle.flush()
        os.fsync(handle.fileno())
        temporary = handle.name
    os.chmod(temporary, 0o600)
    os.replace(temporary, path)
    path.chmod(0o600)


def _atomic_create(path: Path, content: str) -> None:
    """Publish one complete file without ever replacing an existing path."""
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", dir=path.parent, delete=False
    ) as handle:
        handle.write(content)
        handle.flush()
        os.fsync(handle.fileno())
        temporary = Path(handle.name)
    try:
        temporary.chmod(0o600)
        try:
            os.link(temporary, path, follow_symlinks=False)
        except FileExistsError as error:
            raise BenchmarkError(f"manifest output already exists: {path}") from error
    finally:
        temporary.unlink(missing_ok=True)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    scaffold_parser = subparsers.add_parser("scaffold", help="create a private manifest skeleton")
    scaffold_parser.add_argument("--input", type=Path, required=True, help="JSON recording metadata")
    scaffold_parser.add_argument("--output", type=Path, required=True, help="private manifest.json")
    scaffold_parser.add_argument("--allow-root", type=Path, help="explicit alternate private root")

    capture_parser = subparsers.add_parser("capture", help="capture one immutable Apple analysis run")
    capture_parser.add_argument("--manifest", type=Path, required=True)
    capture_parser.add_argument("--binary", type=Path, required=True)
    capture_parser.add_argument("--run-dir", type=Path, required=True)
    capture_parser.add_argument("--locale", default="ko-KR")
    capture_parser.add_argument("--vocab-file", type=Path, help="frozen context replacing every manifest context")
    capture_parser.add_argument("--legacy-json", action="store_true", help="benchmark-only adapter for installed --json output")
    capture_parser.add_argument("--allow-root", type=Path, help="explicit alternate private root")

    compare_parser = subparsers.add_parser("compare", help="compare two Apple STT runs")
    compare_parser.add_argument("--manifest", type=Path, required=True)
    compare_parser.add_argument("--baseline-dir", type=Path, required=True)
    compare_parser.add_argument("--candidate-dir", type=Path, required=True)
    compare_parser.add_argument("--profile", choices=("full", "transcription"), default="full")
    compare_parser.add_argument("--expect-context-only-change", action="store_true")
    compare_parser.add_argument("--gate", action="store_true", help="exit nonzero unless all required gates pass")
    args = parser.parse_args(argv)
    try:
        if args.command == "scaffold":
            root = args.allow_root or DEFAULT_MANIFEST_ROOT
            manifest = scaffold(args.input, args.output, root)
            print(json.dumps({"status": "scaffolded", "recordings": len(manifest["recordings"]), "manifest_sha256": canonical_hash(manifest)}, ensure_ascii=False))
            return 0
        if args.command == "capture":
            manifest_root = args.allow_root or DEFAULT_MANIFEST_ROOT
            run_root = args.allow_root or DEFAULT_RUN_ROOT
            run = capture(
                args.manifest,
                args.binary,
                args.run_dir,
                args.locale,
                manifest_root,
                run_root,
                args.vocab_file,
                args.legacy_json,
            )
            print(json.dumps({"status": "captured", "recordings": len(run["recordings"])}, ensure_ascii=False))
            return 0

        report = compare(
            args.manifest,
            args.baseline_dir,
            args.candidate_dir,
            profile=args.profile,
            expect_context_only_change=args.expect_context_only_change,
        )
        _atomic_write(args.candidate_dir / "report.json", json.dumps(report, ensure_ascii=False, indent=2) + "\n")
        _atomic_write(args.candidate_dir / "report.md", _markdown(report))
    except (BenchmarkError, OSError) as error:
        print(f"benchmark input error: {error}", file=sys.stderr)
        return 2
    print(
        json.dumps(
            {
                "status": report["status"],
                "profile": report["profile"],
                "manifest_sha256": report["manifest_sha256"],
            },
            ensure_ascii=False,
        )
    )
    return int(args.gate and report["status"] != "pass")


if __name__ == "__main__":
    raise SystemExit(main())
