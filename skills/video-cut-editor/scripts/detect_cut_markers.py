#!/usr/bin/env python3
"""Detect triple-pulse edit markers in a local media file."""

from __future__ import annotations

import argparse
from array import array
import hashlib
import json
import math
from pathlib import Path
import shutil
import subprocess
import sys
from typing import Any


DEFAULT_MARKER = Path(__file__).resolve().parents[1] / "assets" / "triple-pulse.wav"
SAMPLE_RATE = 48_000
FRAME_SECONDS = 0.01
FRAME_SAMPLES = int(SAMPLE_RATE * FRAME_SECONDS)


def fail(message: str, code: int = 1) -> int:
    print(f"error: {message}", file=sys.stderr)
    return code


def require_tool(name: str) -> str:
    path = shutil.which(name)
    if not path:
        raise RuntimeError(f"{name} not found in PATH")
    return path


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def ffprobe_duration(ffprobe: str, path: Path) -> float:
    proc = subprocess.run(
        [
            ffprobe,
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=nk=1:nw=1",
            str(path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return float(proc.stdout.strip())


def decode_i16(ffmpeg: str, path: Path, high_band: bool) -> array:
    afilters: list[str] = []
    if high_band:
        afilters.extend(["highpass=f=8000", "lowpass=f=19000"])
    afilters.extend([f"aresample={SAMPLE_RATE}", "aformat=sample_fmts=s16:channel_layouts=mono"])
    proc = subprocess.run(
        [
            ffmpeg,
            "-v",
            "error",
            "-i",
            str(path),
            "-af",
            ",".join(afilters),
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


def envelope(samples: array) -> list[float]:
    values: list[float] = []
    denom = 32768.0 * FRAME_SAMPLES
    for start in range(0, len(samples), FRAME_SAMPLES):
        chunk = samples[start : start + FRAME_SAMPLES]
        if len(chunk) < FRAME_SAMPLES:
            break
        values.append(sum(abs(int(x)) for x in chunk) / denom)
    return values


def trimmed_template(values: list[float]) -> list[float]:
    if not values:
        return values
    peak = max(values)
    if peak <= 0:
        return values
    threshold = peak * 0.08
    active = [i for i, value in enumerate(values) if value >= threshold]
    if not active:
        return values
    start = max(0, active[0] - 2)
    end = min(len(values), active[-1] + 3)
    return values[start:end]


def centered(values: list[float]) -> tuple[list[float], float]:
    if not values:
        return [], 0.0
    mean = sum(values) / len(values)
    centered_values = [value - mean for value in values]
    norm = math.sqrt(sum(value * value for value in centered_values))
    return centered_values, norm


def prefix(values: list[float]) -> tuple[list[float], list[float]]:
    sums = [0.0]
    squares = [0.0]
    total = 0.0
    total_sq = 0.0
    for value in values:
        total += value
        total_sq += value * value
        sums.append(total)
        squares.append(total_sq)
    return sums, squares


def channel_scores(series: list[float], template: list[float]) -> list[float]:
    m = len(template)
    n = len(series)
    if m < 3 or n < m:
        return []
    template_centered, template_norm = centered(template)
    if template_norm <= 1e-12:
        return [0.0] * (n - m + 1)

    sums, squares = prefix(series)
    scores: list[float] = []
    for i in range(0, n - m + 1):
        window_sum = sums[i + m] - sums[i]
        window_sq = squares[i + m] - squares[i]
        window_mean = window_sum / m
        window_var = max(0.0, window_sq - (window_sum * window_sum / m))
        window_norm = math.sqrt(window_var)
        if window_norm <= 1e-12:
            scores.append(0.0)
            continue
        dot = 0.0
        for j, template_value in enumerate(template_centered):
            dot += (series[i + j] - window_mean) * template_value
        scores.append(dot / (window_norm * template_norm))
    return scores


def marker_weight(marker_full: list[float], marker_high: list[float]) -> float:
    full_energy = sum(value * value for value in marker_full)
    high_energy = sum(value * value for value in marker_high)
    if full_energy <= 1e-12:
        return 0.5
    return max(0.25, min(0.88, high_energy / full_energy))


def combine_scores(full_scores: list[float], high_scores: list[float], high_weight: float) -> list[float]:
    count = min(len(full_scores), len(high_scores))
    full_weight = 1.0 - high_weight
    return [
        full_weight * max(0.0, full_scores[i]) + high_weight * max(0.0, high_scores[i])
        for i in range(count)
    ]


def non_max_suppression(scores: list[float], threshold: float, distance_frames: int) -> list[tuple[int, float]]:
    peaks: list[tuple[int, float]] = []
    for i, score in enumerate(scores):
        if score < threshold:
            continue
        left = max(0, i - distance_frames)
        right = min(len(scores), i + distance_frames + 1)
        if score < max(scores[left:right]):
            continue
        if peaks and i - peaks[-1][0] < distance_frames:
            if score > peaks[-1][1]:
                peaks[-1] = (i, score)
        else:
            peaks.append((i, score))
    return peaks


def format_time(seconds: float) -> str:
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    remain = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{remain:06.3f}"


def detect(ffmpeg: str, ffprobe: str, media: Path, marker: Path, threshold: float) -> dict[str, Any]:
    media_full = envelope(decode_i16(ffmpeg, media, high_band=False))
    media_high = envelope(decode_i16(ffmpeg, media, high_band=True))
    marker_full = trimmed_template(envelope(decode_i16(ffmpeg, marker, high_band=False)))
    marker_high = trimmed_template(envelope(decode_i16(ffmpeg, marker, high_band=True)))

    template_frames = min(len(marker_full), len(marker_high))
    marker_full = marker_full[:template_frames]
    marker_high = marker_high[:template_frames]
    if template_frames < 3:
        raise RuntimeError("marker template is too short after trimming")

    full_scores = channel_scores(media_full, marker_full)
    high_scores = channel_scores(media_high, marker_high)
    high_weight = marker_weight(marker_full, marker_high)
    scores = combine_scores(full_scores, high_scores, high_weight)
    distance_frames = max(4, int(template_frames * 0.75))
    peaks = non_max_suppression(scores, threshold, distance_frames)

    predictions = [
        {
            "time": round(index * FRAME_SECONDS, 6),
            "timecode": format_time(index * FRAME_SECONDS),
            "accuracy": round(score, 6),
            "accuracy_percent": round(score * 100, 2),
            "duration": round(template_frames * FRAME_SECONDS, 6),
        }
        for index, score in peaks
    ]
    return {
        "media_path": str(media),
        "media_sha256": sha256_file(media),
        "media_duration": ffprobe_duration(ffprobe, media),
        "marker_path": str(marker),
        "marker_sha256": sha256_file(marker),
        "marker_duration": ffprobe_duration(ffprobe, marker),
        "threshold": threshold,
        "threshold_percent": round(threshold * 100, 2),
        "template_frames": template_frames,
        "high_band_weight": round(high_weight, 6),
        "predictions": predictions,
    }


def print_table(predictions: list[dict[str, Any]]) -> None:
    print("| 시간 | 정확도 |")
    print("|---:|---:|")
    for prediction in predictions:
        print(f"| {prediction['timecode']} | {prediction['accuracy_percent']:.2f}% |")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Detect triple-pulse cut marker timestamps in a media file."
    )
    parser.add_argument("media", type=Path, help="Input media file")
    parser.add_argument(
        "--marker",
        type=Path,
        default=DEFAULT_MARKER,
        help="Marker WAV path (default: bundled assets/triple-pulse.wav)",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.90,
        help="Minimum correlation score; 0.90 means 90%% confidence (default: 0.90)",
    )
    parser.add_argument("--json", type=Path, help="Optional JSON output path")
    parser.add_argument("--format", choices=["table", "json"], default="table")
    args = parser.parse_args()

    media = args.media.expanduser().resolve()
    marker = args.marker.expanduser().resolve()
    if not media.exists():
        return fail(f"media not found: {media}", 2)
    if not marker.exists():
        return fail(f"marker not found: {marker}", 2)
    if not 0.0 < args.threshold <= 1.0:
        return fail("--threshold must be between 0 and 1", 2)

    try:
        ffmpeg = require_tool("ffmpeg")
        ffprobe = require_tool("ffprobe")
        result = detect(ffmpeg, ffprobe, media, marker, args.threshold)
    except (RuntimeError, subprocess.CalledProcessError, ValueError) as exc:
        return fail(str(exc), 1)

    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_table(result["predictions"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
