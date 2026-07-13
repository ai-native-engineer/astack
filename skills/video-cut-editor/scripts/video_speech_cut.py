#!/usr/bin/env python3
"""Cut a local video to detected speech-active regions.

This complements video_silence_cut.py. It still reports ffmpeg silencedetect
regions, but the actual keep-list comes from frame-level VAD so cut boundaries
can follow speech starts and ends more closely than sentence-level STT.
"""

from __future__ import annotations

from array import array
import argparse
import json
import math
import platform
import shlex
import statistics
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

from video_silence_cut import (
    TimeRange,
    audio_output_options,
    build_ffmpeg_command,
    build_filter_graph,
    choose_encoder,
    detect_silences,
    fail,
    ffmpeg_encoders,
    ffprobe_json,
    parse_duration,
    require_tool,
    run,
    streams,
    verify_output,
    video_output_options,
)


def default_output(input_file: Path, test_duration: float | None) -> Path:
    suffix = input_file.suffix or ".mp4"
    marker = f".sample-{int(test_duration)}s.speechcut" if test_duration else ".speechcut"
    return input_file.with_name(f"{input_file.stem}{marker}{suffix}")


def percentile(values: list[float], ratio: float) -> float:
    if not values:
        return -120.0
    ordered = sorted(values)
    pos = min(len(ordered) - 1, max(0, int(round((len(ordered) - 1) * ratio))))
    return ordered[pos]


def decode_pcm(
    ffmpeg: str,
    input_file: Path,
    audio_index: int,
    sample_rate: int,
    duration: float,
) -> array:
    proc = subprocess.run(
        [
            ffmpeg,
            "-v",
            "error",
            "-i",
            str(input_file),
            "-t",
            f"{duration:.6f}",
            "-map",
            f"0:a:{audio_index}",
            "-ac",
            "1",
            "-ar",
            str(sample_rate),
            "-f",
            "s16le",
            "-",
        ],
        check=True,
        capture_output=True,
    )
    samples = array("h")
    samples.frombytes(proc.stdout)
    return samples


def frame_stats(samples: array, frame_samples: int) -> list[dict[str, float]]:
    stats: list[dict[str, float]] = []
    scale = 32768.0
    for start in range(0, len(samples), frame_samples):
        chunk = samples[start : start + frame_samples]
        if len(chunk) < frame_samples:
            break
        total_sq = 0.0
        peak = 0
        sign_changes = 0
        prev = 0
        for sample in chunk:
            value = int(sample)
            abs_value = abs(value)
            peak = max(peak, abs_value)
            total_sq += value * value
            sign = 1 if value > 0 else -1 if value < 0 else 0
            if sign and prev and sign != prev:
                sign_changes += 1
            if sign:
                prev = sign
        rms = math.sqrt(total_sq / len(chunk)) / scale
        peak_norm = peak / scale
        rms_db = 20.0 * math.log10(max(rms, 1e-9))
        peak_db = 20.0 * math.log10(max(peak_norm, 1e-9))
        zcr = sign_changes / max(1, len(chunk) - 1)
        stats.append({"rms_db": rms_db, "peak_db": peak_db, "zcr": zcr})
    return stats


def energy_vad_mask(
    stats: list[dict[str, float]],
    vad_db: float,
    margin_db: float,
    noise_percentile: float,
) -> tuple[list[bool], dict[str, float]]:
    rms_values = [item["rms_db"] for item in stats]
    floor = percentile(rms_values, noise_percentile)
    median = statistics.median(rms_values) if rms_values else -120.0
    threshold = max(vad_db, floor + margin_db)

    mask: list[bool] = []
    for item in stats:
        loud_enough = item["rms_db"] >= threshold or item["peak_db"] >= threshold + 8.0
        # A wide ZCR range keeps vowels, consonants, and compressed OBS audio.
        voice_like = 0.002 <= item["zcr"] <= 0.45
        mask.append(bool(loud_enough and voice_like))

    return mask, {
        "noise_floor_db": round(floor, 3),
        "median_rms_db": round(median, 3),
        "threshold_db": round(threshold, 3),
        "absolute_vad_db": round(vad_db, 3),
        "margin_db": round(margin_db, 3),
        "noise_percentile": round(noise_percentile, 3),
    }


def webrtc_vad_mask(
    samples: array,
    sample_rate: int,
    frame_ms: int,
    aggressiveness: int,
) -> list[bool]:
    try:
        import webrtcvad  # type: ignore[import-not-found]
    except Exception as exc:  # pragma: no cover - optional local dependency
        raise RuntimeError("webrtcvad is not installed; use --vad-engine energy") from exc

    if frame_ms not in {10, 20, 30}:
        raise RuntimeError("webrtcvad requires --frame-ms to be 10, 20, or 30")
    vad = webrtcvad.Vad(aggressiveness)
    frame_samples = int(sample_rate * frame_ms / 1000)
    mask: list[bool] = []
    for start in range(0, len(samples), frame_samples):
        chunk = samples[start : start + frame_samples]
        if len(chunk) < frame_samples:
            break
        mask.append(vad.is_speech(chunk.tobytes(), sample_rate))
    return mask


def ranges_from_mask(
    mask: list[bool],
    frame_seconds: float,
    duration: float,
    min_segment: float,
    merge_gap: float,
    padding: float,
) -> list[TimeRange]:
    raw: list[TimeRange] = []
    start: float | None = None
    for index, active in enumerate(mask):
        at = index * frame_seconds
        if active and start is None:
            start = at
        if not active and start is not None:
            end = index * frame_seconds
            if end - start >= min_segment:
                raw.append(TimeRange(start, end))
            start = None
    if start is not None:
        end = min(duration, len(mask) * frame_seconds)
        if end - start >= min_segment:
            raw.append(TimeRange(start, end))

    merged: list[TimeRange] = []
    for item in raw:
        if not merged or item.start - merged[-1].end > merge_gap:
            merged.append(item)
        else:
            merged[-1] = TimeRange(merged[-1].start, item.end)

    padded: list[TimeRange] = []
    for item in merged:
        start = max(0.0, item.start - padding)
        end = min(duration, item.end + padding)
        if padded and start <= padded[-1].end:
            padded[-1] = TimeRange(padded[-1].start, max(padded[-1].end, end))
        else:
            padded.append(TimeRange(start, end))
    return [item for item in padded if item.duration > 0.001]


def detect_speech_segments(
    ffmpeg: str,
    input_file: Path,
    audio_index: int,
    duration: float,
    sample_rate: int,
    frame_ms: int,
    vad_engine: str,
    vad_db: float,
    vad_margin_db: float,
    noise_percentile: float,
    webrtc_aggressiveness: int,
    min_segment: float,
    merge_gap: float,
    padding: float,
) -> tuple[list[TimeRange], dict[str, Any]]:
    samples = decode_pcm(ffmpeg, input_file, audio_index, sample_rate, duration)
    frame_samples = int(sample_rate * frame_ms / 1000)
    frame_seconds = frame_ms / 1000.0
    stats = frame_stats(samples, frame_samples)

    if vad_engine == "webrtc":
        mask = webrtc_vad_mask(samples, sample_rate, frame_ms, webrtc_aggressiveness)
        meta: dict[str, Any] = {
            "engine": "webrtc",
            "sample_rate": sample_rate,
            "frame_ms": frame_ms,
            "aggressiveness": webrtc_aggressiveness,
        }
    else:
        mask, meta = energy_vad_mask(stats, vad_db, vad_margin_db, noise_percentile)
        meta.update({"engine": "energy", "sample_rate": sample_rate, "frame_ms": frame_ms})

    speech_segments = ranges_from_mask(
        mask,
        frame_seconds,
        duration,
        min_segment,
        merge_gap,
        padding,
    )
    meta["active_frames"] = sum(1 for value in mask if value)
    meta["total_frames"] = len(mask)
    meta["active_ratio"] = round((meta["active_frames"] / len(mask)) if mask else 0.0, 6)
    return speech_segments, meta


def range_dict(item: TimeRange) -> dict[str, float]:
    return {
        "start": round(item.start, 6),
        "end": round(item.end, 6),
        "duration": round(item.duration, 6),
    }


def write_json_report(
    path: Path,
    input_file: Path,
    output_file: Path,
    duration: float,
    speech_segments: list[TimeRange],
    silences: list[TimeRange],
    vad_meta: dict[str, Any],
    args: argparse.Namespace,
) -> None:
    removed = duration - sum(item.duration for item in speech_segments)
    report = {
        "input": str(input_file),
        "output": str(output_file),
        "duration": round(duration, 6),
        "estimated_output": round(sum(item.duration for item in speech_segments), 6),
        "estimated_removed": round(removed, 6),
        "detect_audio": args.detect_audio,
        "vad": vad_meta,
        "speech_segments": [range_dict(item) for item in speech_segments],
        "silencedetect": {
            "silence_db": args.silence_db,
            "min_duration": args.silence_min_duration,
            "silences": [range_dict(item) for item in silences],
        },
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def print_summary(
    input_file: Path,
    output_file: Path,
    duration: float,
    speech_segments: list[TimeRange],
    silences: list[TimeRange],
    vad_meta: dict[str, Any],
    dry_run: bool,
) -> None:
    kept = sum(item.duration for item in speech_segments)
    print(f"input: {input_file}")
    print(f"output: {output_file}")
    print(f"duration: {duration:.3f}s")
    print(f"speech_segments: {len(speech_segments)}")
    print(f"silencedetect_silences: {len(silences)}")
    print(f"estimated_output: {kept:.3f}s")
    print(f"estimated_removed: {duration - kept:.3f}s")
    print(f"vad_engine: {vad_meta.get('engine')}")
    if "threshold_db" in vad_meta:
        print(f"vad_threshold_db: {vad_meta['threshold_db']}")
        print(f"noise_floor_db: {vad_meta['noise_floor_db']}")
    print(f"active_ratio: {vad_meta.get('active_ratio')}")
    if speech_segments:
        print("first_speech_segments:")
        for item in speech_segments[:8]:
            print(f"  {item.start:.3f}-{item.end:.3f} ({item.duration:.3f}s)")
    if silences:
        print("first_silences:")
        for item in silences[:8]:
            print(f"  {item.start:.3f}-{item.end:.3f} ({item.duration:.3f}s)")
    if dry_run:
        print("dry_run: no file written")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Cut a local video to frame-level speech-active regions."
    )
    parser.add_argument("input_file", nargs="?", type=Path)
    parser.add_argument("output_file", nargs="?", type=Path)
    parser.add_argument("--detect-audio", type=int, default=0)
    parser.add_argument("--test-duration", type=float)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--overwrite", "-y", action="store_true")
    parser.add_argument("--open", action="store_true")
    parser.add_argument("--json", type=Path)
    parser.add_argument("--vad-engine", choices=["energy", "webrtc"], default="energy")
    parser.add_argument("--sample-rate", type=int, default=16000)
    parser.add_argument("--frame-ms", type=int, default=20)
    parser.add_argument("--vad-db", type=float, default=-42.0)
    parser.add_argument("--vad-margin-db", type=float, default=12.0)
    parser.add_argument("--noise-percentile", type=float, default=0.20)
    parser.add_argument("--webrtc-aggressiveness", type=int, default=2)
    parser.add_argument("--min-segment", type=float, default=0.08)
    parser.add_argument("--merge-gap", type=float, default=0.70)
    parser.add_argument("--padding", type=float, default=0.30)
    parser.add_argument("--silence-db", default="-35dB")
    parser.add_argument("--silence-min-duration", type=float, default=0.20)
    parser.add_argument("--video-encoder", default="auto")
    parser.add_argument("--video-bitrate", default="auto", help="auto, none, or a value like 16000k")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.input_file:
        return fail("input_file is required")
    if args.padding < 0:
        return fail("--padding must be >= 0")
    if args.merge_gap < 0:
        return fail("--merge-gap must be >= 0")
    if args.min_segment <= 0:
        return fail("--min-segment must be > 0")
    if args.sample_rate not in {8000, 16000, 32000, 48000}:
        return fail("--sample-rate must be one of 8000, 16000, 32000, 48000")
    if args.webrtc_aggressiveness < 0 or args.webrtc_aggressiveness > 3:
        return fail("--webrtc-aggressiveness must be 0..3")
    if args.noise_percentile < 0 or args.noise_percentile > 1:
        return fail("--noise-percentile must be 0..1")

    input_file = args.input_file.expanduser().resolve()
    if not input_file.exists():
        return fail(f"input not found: {input_file}")
    output_file = (args.output_file or default_output(input_file, args.test_duration)).expanduser().resolve()
    if input_file == output_file:
        return fail("input and output must be different")
    if output_file.exists() and not args.dry_run and not args.overwrite:
        return fail(f"output exists, pass --overwrite: {output_file}")

    try:
        ffmpeg = require_tool("ffmpeg")
        ffprobe = require_tool("ffprobe")
        media = ffprobe_json(ffprobe, input_file)
        video_streams = streams(media, "video")
        audio_streams = streams(media, "audio")
        if not video_streams:
            return fail("no video stream found")
        if not audio_streams:
            return fail("no audio stream found")
        if args.detect_audio < 0 or args.detect_audio >= len(audio_streams):
            return fail(f"--detect-audio must be between 0 and {len(audio_streams) - 1}")

        source_duration = parse_duration(media)
        duration = min(source_duration, args.test_duration) if args.test_duration else source_duration
        if duration <= 0:
            return fail("duration is zero")

        speech_segments, vad_meta = detect_speech_segments(
            ffmpeg,
            input_file,
            args.detect_audio,
            duration,
            args.sample_rate,
            args.frame_ms,
            args.vad_engine,
            args.vad_db,
            args.vad_margin_db,
            args.noise_percentile,
            args.webrtc_aggressiveness,
            args.min_segment,
            args.merge_gap,
            args.padding,
        )
        if not speech_segments:
            return fail("no speech-active segments found; lower --vad-db or --vad-margin-db")

        silences = detect_silences(
            ffmpeg,
            input_file,
            args.detect_audio,
            duration,
            args.silence_db,
            args.silence_min_duration,
        )
        plan = choose_encoder(video_streams[0], args.video_encoder, ffmpeg_encoders(ffmpeg))
        print_summary(input_file, output_file, duration, speech_segments, silences, vad_meta, args.dry_run)
        if args.json:
            write_json_report(args.json.expanduser().resolve(), input_file, output_file, duration, speech_segments, silences, vad_meta, args)
        if args.dry_run:
            return 0

        output_file.parent.mkdir(parents=True, exist_ok=True)
        graph = build_filter_graph(speech_segments, len(audio_streams))
        video_opts = video_output_options(video_streams[0], plan, output_file, args.video_bitrate)
        audio_opts, audio_warnings = audio_output_options(audio_streams)
        for warning in plan.warnings + audio_warnings:
            print(f"warning: {warning}")

        with tempfile.NamedTemporaryFile("w", suffix=".ffgraph", delete=False, encoding="utf-8") as handle:
            handle.write(graph)
            graph_path = Path(handle.name)
        try:
            cmd = build_ffmpeg_command(
                ffmpeg,
                input_file,
                output_file,
                graph_path,
                len(audio_streams),
                video_opts,
                audio_opts,
                args.overwrite,
            )
            result = run(cmd)
            if result.returncode != 0:
                print("ffmpeg command:", shlex.join(cmd), file=sys.stderr)
                return fail((result.stderr or result.stdout).strip()[-4000:])
        finally:
            graph_path.unlink(missing_ok=True)

        errors = verify_output(
            ffmpeg,
            ffprobe,
            media,
            output_file,
            plan.expected_video_codec,
            len(audio_streams),
        )
        if errors:
            for error in errors:
                print(f"verify_error: {error}", file=sys.stderr)
            return 1

        print("verify: ok")
        if args.open:
            if platform.system() == "Darwin":
                subprocess.run(["open", str(output_file)], check=False)
            else:
                print("--open is only implemented for macOS")
        return 0
    except Exception as exc:
        return fail(str(exc))


if __name__ == "__main__":
    raise SystemExit(main())
