#!/usr/bin/env python3
"""Audit rendered waveform continuity only at known edit joins."""

from __future__ import annotations

import argparse
import json
import math
import shutil
import subprocess
import sys
import tempfile
from array import array
from datetime import datetime
from pathlib import Path
from typing import Any


SAMPLE_RATE = 48000
FRAME_SAMPLES = 480  # 10 ms at 48 kHz.
FRAME_BYTES = FRAME_SAMPLES * 2
QUIET_DB = -45.0
ACTIVE_DB = -42.0


def fail(message: str, code: int = 1) -> int:
    print(f"error: {message}", file=sys.stderr)
    return code


def require_tool(name: str) -> str:
    path = shutil.which(name)
    if not path:
        raise RuntimeError(f"missing required tool: {name}")
    return path


def db_from_rms(rms: float) -> float:
    if rms <= 0:
        return -120.0
    return 20.0 * math.log10(rms / 32768.0)


def format_time(seconds: float) -> str:
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    remain = seconds - hours * 3600 - minutes * 60
    if hours:
        return f"{hours:02d}:{minutes:02d}:{remain:06.3f}"
    return f"{minutes:02d}:{remain:06.3f}"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def extract_pcm(ffmpeg: str, media: Path, audio_track: str, output: Path) -> None:
    proc = subprocess.run(
        [
            ffmpeg,
            "-hide_banner",
            "-nostdin",
            "-v",
            "error",
            "-i",
            str(media),
            "-map",
            audio_track,
            "-ac",
            "1",
            "-ar",
            str(SAMPLE_RATE),
            "-f",
            "s16le",
            str(output),
        ],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if proc.returncode != 0:
        raise RuntimeError((proc.stderr or proc.stdout).strip())


def pcm_frames(path: Path) -> tuple[list[float], list[int], list[int], list[int]]:
    rms: list[float] = []
    first: list[int] = []
    last: list[int] = []
    maxdiff: list[int] = []
    with path.open("rb") as handle:
        while True:
            data = handle.read(FRAME_BYTES)
            if len(data) < FRAME_BYTES:
                break
            samples = array("h")
            samples.frombytes(data)
            if sys.byteorder != "little":
                samples.byteswap()
            sumsq = 0
            md = 0
            prev = samples[0]
            for value in samples:
                sumsq += value * value
                diff = abs(value - prev)
                if diff > md:
                    md = diff
                prev = value
            rms.append(math.sqrt(sumsq / len(samples)))
            first.append(samples[0])
            last.append(samples[-1])
            maxdiff.append(md)
    return rms, first, last, maxdiff


def classify_join(
    seconds: float,
    rms: list[float],
    first: list[int],
    last: list[int],
    maxdiff: list[int],
) -> dict[str, Any]:
    index = max(0, min(len(rms) - 1, int(seconds * 100)))
    prefix = [0.0]
    for value in rms:
        prefix.append(prefix[-1] + value)

    def avg(start: int, end: int) -> float:
        start = max(0, start)
        end = min(len(rms), end)
        if end <= start:
            return 0.0
        return (prefix[end] - prefix[start]) / (end - start)

    pre_db = db_from_rms(avg(index - 25, index))
    post_db = db_from_rms(avg(index, index + 25))
    jump_db = abs(post_db - pre_db)
    around_db = [db_from_rms(value) for value in rms[max(0, index - 10) : min(len(rms), index + 10)]]
    quiet_frames = sum(1 for value in around_db if value < QUIET_DB)
    boundary_delta = abs(first[index] - last[index - 1]) / 32768.0 if index > 0 else 0.0
    nearby_delta = max(maxdiff[max(0, index - 3) : min(len(maxdiff), index + 4)] or [0]) / 32768.0

    flags: list[str] = []
    severity = "ok"
    if boundary_delta > 0.12 or nearby_delta > 0.35:
        flags.append("sample_discontinuity")
        severity = "review"
    elif pre_db > ACTIVE_DB and post_db > ACTIVE_DB and quiet_frames < 4 and jump_db > 6.0:
        flags.append("tight_active_to_active_join")
        severity = "listen"
    elif quiet_frames == 0 and jump_db > 12.0:
        flags.append("no_quiet_padding_level_change")
        severity = "listen"

    return {
        "time": round(seconds, 6),
        "timecode": format_time(seconds),
        "severity": severity,
        "pre_250ms_db": round(pre_db, 2),
        "post_250ms_db": round(post_db, 2),
        "level_jump_db": round(jump_db, 2),
        "quiet_frames_around_200ms": quiet_frames,
        "boundary_sample_delta_ratio": round(boundary_delta, 4),
        "nearby_max_sample_delta_ratio": round(nearby_delta, 4),
        "flags": flags,
    }


def audit(media: Path, join_map: Path, audio_track: str) -> dict[str, Any]:
    join_data = load_json(join_map)
    joins = [item for item in join_data.get("joins", []) if isinstance(item, dict)]
    if not joins:
        raise ValueError("join map has no joins")

    ffmpeg = require_tool("ffmpeg")
    with tempfile.TemporaryDirectory() as tmp:
        pcm_path = Path(tmp) / "audio.s16le"
        extract_pcm(ffmpeg, media, audio_track, pcm_path)
        rms, first, last, maxdiff = pcm_frames(pcm_path)

    checked = []
    for item in joins:
        if "output_time" not in item:
            continue
        metrics = classify_join(float(item["output_time"]), rms, first, last, maxdiff)
        metrics["join"] = item
        checked.append(metrics)

    return {
        "schema": "video-cut-editor.waveform-join-audit.v1",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "media": str(media),
        "join_map": str(join_map),
        "audio_track": audio_track,
        "thresholds": {
            "quiet_db": QUIET_DB,
            "active_db": ACTIVE_DB,
            "review_boundary_delta_ratio_gt": 0.12,
            "review_nearby_delta_ratio_gt": 0.35,
            "listen_active_to_active_jump_db_gt": 6.0,
        },
        "summary": {
            "joins": len(checked),
            "review": sum(1 for item in checked if item["severity"] == "review"),
            "listen": sum(1 for item in checked if item["severity"] == "listen"),
            "ok": sum(1 for item in checked if item["severity"] == "ok"),
        },
        "joins": checked,
    }


def write_markdown(path: Path, report: dict[str, Any]) -> None:
    summary = report["summary"]
    lines = [
        "# Waveform Join Audit",
        "",
        f"Media: `{report['media']}`",
        f"Join map: `{report['join_map']}`",
        f"Audio track: `{report['audio_track']}`",
        "",
        "## Summary",
        "",
        f"- Joins checked: `{summary['joins']}`",
        f"- Review: `{summary['review']}`",
        f"- Listen: `{summary['listen']}`",
        f"- OK: `{summary['ok']}`",
        "",
        "## Joins",
        "",
    ]
    for item in report["joins"]:
        join = item["join"]
        label = join.get("type", "join")
        reasons = ",".join(str(reason) for reason in join.get("reasons", [])) or "none"
        flags = ",".join(item["flags"]) or "none"
        lines.append(
            f"- `{item['timecode']}` `{item['severity']}` `{label}` "
            f"jump `{item['level_jump_db']}dB`, quiet `{item['quiet_frames_around_200ms']}`, "
            f"boundary `{item['boundary_sample_delta_ratio']}`, nearby `{item['nearby_max_sample_delta_ratio']}`, "
            f"flags `{flags}`, reasons `{reasons}`"
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_self_test() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        pcm = Path(tmp) / "test.s16le"
        samples = array("h")
        samples.extend([0] * (SAMPLE_RATE // 2))
        samples.extend([30000] * (SAMPLE_RATE // 2))
        pcm.write_bytes(samples.tobytes())
        rms, first, last, maxdiff = pcm_frames(pcm)
        result = classify_join(0.5, rms, first, last, maxdiff)
        assert result["severity"] == "review", result
    print("self_test: ok")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit waveform continuity at known edit joins.")
    parser.add_argument("media", nargs="?", type=Path)
    parser.add_argument("join_map", nargs="?", type=Path)
    parser.add_argument("--audio-track", default="0:a:0")
    parser.add_argument("--output-json", type=Path)
    parser.add_argument("--output-md", type=Path)
    parser.add_argument("--fail-on-review", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.self_test:
        return run_self_test()
    if not args.media or not args.join_map:
        return fail("media and join_map are required")
    media = args.media.expanduser().resolve()
    join_map = args.join_map.expanduser().resolve()
    if not media.exists():
        return fail(f"media not found: {media}")
    if not join_map.exists():
        return fail(f"join map not found: {join_map}")
    try:
        report = audit(media, join_map, args.audio_track)
    except Exception as exc:
        return fail(str(exc))

    output_json = (args.output_json or join_map.with_suffix(".waveform-audit.json")).expanduser().resolve()
    output_md = (args.output_md or join_map.with_suffix(".waveform-audit.md")).expanduser().resolve()
    write_json(output_json, report)
    write_markdown(output_md, report)

    summary = report["summary"]
    print(f"joins: {summary['joins']}")
    print(f"review: {summary['review']}")
    print(f"listen: {summary['listen']}")
    print(f"ok: {summary['ok']}")
    print(f"json: {output_json}")
    print(f"md: {output_md}")
    if args.fail_on_review and summary["review"]:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
