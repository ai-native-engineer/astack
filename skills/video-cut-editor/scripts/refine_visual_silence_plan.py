#!/usr/bin/env python3
"""Split reviewed silence cuts around detected screen changes."""

from __future__ import annotations

import argparse
import copy
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


PTS_RE = re.compile(r"pts_time:([0-9.]+)")


def fail(message: str, code: int = 1) -> int:
    print(f"error: {message}", file=sys.stderr)
    return code


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def merge_windows(windows: list[tuple[float, float]], gap: float = 0.1) -> list[tuple[float, float]]:
    merged: list[list[float]] = []
    for start, end in sorted(windows):
        if merged and start <= merged[-1][1] + gap:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return [(start, end) for start, end in merged]


def split_silence(
    duration: float,
    events: list[float],
    preserve_short: float,
    before: float,
    after: float,
    no_event_tail: float,
    min_cut: float,
) -> tuple[list[tuple[float, float]], list[tuple[float, float]]]:
    if duration <= preserve_short:
        return [], [(0.0, duration)]
    if events:
        preserved = merge_windows(
            [(max(0.0, event - before), min(duration, event + after)) for event in events]
        )
    else:
        # ponytail: this favors a safe tail for static/gradual changes; use optical flow if those become common.
        preserved = [(max(0.0, duration - no_event_tail), duration)]

    cuts: list[tuple[float, float]] = []
    cursor = 0.0
    for start, end in preserved:
        if start - cursor >= min_cut:
            cuts.append((cursor, start))
        cursor = max(cursor, end)
    if duration - cursor >= min_cut:
        cuts.append((cursor, duration))
    return cuts, preserved


def detect_scene_events(
    ffmpeg: str, source: Path, start: float, duration: float, threshold: float
) -> list[float]:
    proc = subprocess.run(
        [
            ffmpeg,
            "-hide_banner",
            "-nostdin",
            "-ss",
            f"{start:.6f}",
            "-t",
            f"{duration:.6f}",
            "-i",
            str(source),
            "-vf",
            f"scale=640:-2,select='gt(scene,{threshold})',showinfo",
            "-an",
            "-f",
            "null",
            "-",
        ],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if proc.returncode != 0:
        raise RuntimeError((proc.stderr or proc.stdout).strip())
    return [float(value) for value in PTS_RE.findall(proc.stderr)]


def same_interval(left: dict[str, Any], right: dict[str, Any], tolerance: float = 1e-6) -> bool:
    return abs(float(left["start"]) - float(right["start"])) < tolerance and abs(
        float(left["end"]) - float(right["end"])
    ) < tolerance


def build_plan(
    plan: dict[str, Any],
    reviewed: list[dict[str, Any]],
    output_media: Path,
    threshold: float,
    preserve_short: float,
    before: float,
    after: float,
    no_event_tail: float,
    min_cut: float,
) -> tuple[dict[str, Any], dict[str, Any]]:
    if plan.get("status") != "reviewed":
        raise ValueError("input plan status must be reviewed")
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise RuntimeError("missing required tool: ffmpeg")
    source = Path(str(plan["source"])).expanduser().resolve()
    if not source.is_file():
        raise FileNotFoundError(f"source not found: {source}")

    pending = [dict(item) for item in reviewed]
    revised: list[dict[str, Any]] = []
    details: list[dict[str, Any]] = []
    for interval in plan.get("remove_intervals", []):
        match = next((item for item in pending if same_interval(interval, item)), None)
        if not match:
            revised.append(interval)
            continue
        if str(interval.get("reason", "")).strip() != "silence":
            raise ValueError(f"refusing to change a non-silence interval: {interval}")
        if not interval.get("silence_sources"):
            raise ValueError(f"silence interval is missing silencedetect evidence: {interval}")
        pending.remove(match)
        start = float(interval["start"])
        end = float(interval["end"])
        duration = end - start
        if duration <= 0:
            raise ValueError(f"invalid silence interval: {interval}")
        events = (
            detect_scene_events(ffmpeg, source, start, duration, threshold)
            if duration > preserve_short
            else []
        )
        cuts, preserved = split_silence(
            duration, events, preserve_short, before, after, no_event_tail, min_cut
        )
        replacements: list[dict[str, float]] = []
        for local_start, local_end in cuts:
            piece = copy.deepcopy(interval)
            piece["start"] = round(start + local_start, 6)
            piece["end"] = round(start + local_end, 6)
            piece["reason"] = "silence (visual-safe split)"
            revised.append(piece)
            replacements.append({"start": piece["start"], "end": piece["end"]})
        details.append(
            {
                "original": {"start": start, "end": end, "duration": duration},
                "scene_events_local": events,
                "preserved_local": [{"start": a, "end": b} for a, b in preserved],
                "replacement_cuts": replacements,
            }
        )
    if pending:
        raise ValueError(f"reviewed intervals were not found in the plan: {pending}")

    result = copy.deepcopy(plan)
    result["output"] = str(output_media.resolve())
    result["status"] = "draft"
    result["remove_intervals"] = sorted(revised, key=lambda item: (item["start"], item["end"]))
    notes = result.setdefault("render_notes", [])
    if not isinstance(notes, list):
        raise ValueError("render_notes must be a list when present")
    notes.append("Visual-risk silence intervals were split around scene changes; review this draft before render.")
    report = {
        "schema": "video-cut-editor.visual-silence-refinement.v1",
        "settings": {
            "scene_threshold": threshold,
            "preserve_short": preserve_short,
            "before": before,
            "after": after,
            "no_event_tail": no_event_tail,
            "min_cut": min_cut,
        },
        "reviewed_intervals": len(details),
        "intervals": details,
    }
    return result, report


def run_self_test() -> int:
    cuts, kept = split_silence(5.0, [2.0, 2.4], 2.0, 0.3, 0.5, 0.8, 0.3)
    assert kept == [(1.7, 2.9)], kept
    assert cuts == [(0.0, 1.7), (2.9, 5.0)], cuts
    cuts, kept = split_silence(5.0, [], 2.0, 0.3, 0.5, 0.8, 0.3)
    assert kept == [(4.2, 5.0)] and cuts == [(0.0, 4.2)]
    assert split_silence(1.5, [0.7], 2.0, 0.3, 0.5, 0.8, 0.3) == (
        [],
        [(0.0, 1.5)],
    )
    print("self_test: ok")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a draft plan that preserves scene changes inside reviewed silence cuts."
    )
    parser.add_argument("plan", nargs="?", type=Path)
    parser.add_argument("reviewed_intervals", nargs="?", type=Path)
    parser.add_argument("--output-plan", type=Path)
    parser.add_argument("--output-media", type=Path)
    parser.add_argument("--report", type=Path)
    parser.add_argument("--scene-threshold", type=float, default=0.005)
    parser.add_argument("--preserve-short", type=float, default=2.0)
    parser.add_argument("--before", type=float, default=0.3)
    parser.add_argument("--after", type=float, default=0.5)
    parser.add_argument("--no-event-tail", type=float, default=0.8)
    parser.add_argument("--min-cut", type=float, default=0.3)
    parser.add_argument("--self-test", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.self_test:
        return run_self_test()
    required = [args.plan, args.reviewed_intervals, args.output_plan, args.output_media, args.report]
    if any(value is None for value in required):
        return fail(
            "plan, reviewed_intervals, --output-plan, --output-media, and --report are required"
        )
    numeric = [
        args.scene_threshold,
        args.preserve_short,
        args.before,
        args.after,
        args.no_event_tail,
        args.min_cut,
    ]
    if (
        not 0.0 < args.scene_threshold < 1.0
        or any(value < 0 for value in numeric[1:])
        or args.min_cut == 0
    ):
        return fail(
            "scene threshold must be between 0 and 1; timing values must be non-negative and --min-cut must be positive"
        )

    plan_path = args.plan.expanduser().resolve()
    reviewed_path = args.reviewed_intervals.expanduser().resolve()
    output_plan = args.output_plan.expanduser().resolve()
    output_media = args.output_media.expanduser().resolve()
    report_path = args.report.expanduser().resolve()
    if len({output_plan, output_media, report_path}) != 3:
        return fail("--output-plan, --output-media, and --report must use distinct paths")
    if not plan_path.is_file():
        return fail(f"plan not found: {plan_path}")
    if not reviewed_path.is_file():
        return fail(f"reviewed intervals not found: {reviewed_path}")
    for path in (output_plan, output_media, report_path):
        if path.exists():
            return fail(f"refusing to overwrite output: {path}")
    try:
        plan = load_json(plan_path)
        reviewed = load_json(reviewed_path)
        if not isinstance(plan, dict) or not isinstance(reviewed, list):
            raise ValueError("plan must be an object and reviewed_intervals must be a JSON array")
        result, report = build_plan(
            plan,
            reviewed,
            output_media,
            args.scene_threshold,
            args.preserve_short,
            args.before,
            args.after,
            args.no_event_tail,
            args.min_cut,
        )
        report["plan"] = str(plan_path)
        report["source"] = result["source"]
        report["output_plan"] = str(output_plan)
        report["output_media"] = str(output_media)
        write_json(output_plan, result)
        write_json(report_path, report)
    except Exception as exc:
        return fail(str(exc))

    print(f"plan: {output_plan}")
    print(f"status: {result['status']}")
    print(f"reviewed_visual_silences: {report['reviewed_intervals']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
