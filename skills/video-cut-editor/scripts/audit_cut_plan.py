#!/usr/bin/env python3
"""Audit cut plans before rendering marker-based video edits."""

from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
from pathlib import Path
from typing import Any


MARKER_RE = re.compile(r"marker\s+(\d+)\s+at\s+([0-9]+(?:\.[0-9]+)?)s", re.IGNORECASE)
SAFE_LONG_REASONS = ("full_retake", "intentional_long_cut")
# VAD ranges include boundary padding, so allow a small edge overlap while
# rejecting silence cuts that extend materially into detected speech.
MAX_VAD_OVERLAP_SECONDS = 0.08


def fail(message: str, code: int = 1) -> int:
    print(f"error: {message}", file=sys.stderr)
    return code


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def speech_path_from_plan(plan: dict[str, Any], plan_path: Path) -> Path | None:
    evidence = plan.get("evidence", {})
    raw = evidence.get("speech")
    if isinstance(raw, str):
        return Path(raw).expanduser()

    marker_plan = evidence.get("marker_plan")
    if isinstance(marker_plan, str):
        marker_plan_path = Path(marker_plan).expanduser()
        if not marker_plan_path.is_absolute():
            marker_plan_path = (plan_path.parent / marker_plan_path).resolve()
        try:
            nested = load_json(marker_plan_path)
        except Exception:
            return None
        nested_speech = nested.get("evidence", {}).get("speech")
        if isinstance(nested_speech, str):
            return Path(nested_speech).expanduser()
    return None


def speech_segments(plan: dict[str, Any], plan_path: Path) -> list[dict[str, float]]:
    speech_path = speech_path_from_plan(plan, plan_path)
    if not speech_path:
        return []
    if not speech_path.is_absolute():
        speech_path = (plan_path.parent / speech_path).resolve()
    try:
        data = load_json(speech_path)
    except Exception:
        return []
    return [
        {"start": float(item["start"]), "end": float(item["end"])}
        for item in data.get("speech_segments", [])
        if "start" in item and "end" in item
    ]


def media_duration(plan: dict[str, Any]) -> float | None:
    value = plan.get("duration")
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def marker_hits(reason: str) -> list[tuple[int | None, float]]:
    hits: list[tuple[int | None, float]] = []
    for marker_id, at in MARKER_RE.findall(reason):
        hits.append((int(marker_id), float(at)))
    return hits


def neighbors(
    segments: list[dict[str, float]], at: float
) -> tuple[dict[str, float] | None, dict[str, float] | None]:
    prev = None
    nxt = None
    for item in segments:
        if item["end"] <= at:
            prev = item
        elif item["start"] >= at and nxt is None:
            nxt = item
    return prev, nxt


def has_following_speech(segments: list[dict[str, float]], at: float) -> bool:
    return any(item["end"] > at + 0.15 for item in segments)


def audit_plan(plan: dict[str, Any], plan_path: Path, max_marker_cut: float) -> list[str]:
    findings: list[str] = []
    segments = speech_segments(plan, plan_path)
    duration = media_duration(plan)
    silence_items = [
        item
        for item in plan.get("remove_intervals", [])
        if "silence" in str(item.get("reason", "")).lower()
    ]
    policy = plan.get("silence_policy")
    if silence_items and not isinstance(policy, dict):
        findings.append("automatic silence cuts are missing silence_policy; rebuild with build_mixed_cut_plan.py")
    elif silence_items:
        min_duration = float(policy.get("min_duration", 0))
        padding = float(policy.get("padding", -1))
        if min_duration < 0.8:
            findings.append(f"silence_policy min_duration {min_duration:.3f}s is below the 0.8s safety floor")
        if padding < 0:
            findings.append("silence_policy padding must be >= 0")
        for index, item in enumerate(silence_items, 1):
            sources = item.get("silence_sources")
            if not isinstance(sources, list) or not sources:
                findings.append(f"silence interval {index}: missing explicit silencedetect source")
                continue
            for source in sources:
                if not isinstance(source, dict) or not all(
                    key in source for key in ("start", "end", "duration")
                ):
                    findings.append(
                        f"silence interval {index}: source must record start, end, and duration"
                    )
                    continue
                source_start = float(source["start"])
                source_end = float(source["end"])
                source_duration = source_end - source_start
                if abs(float(source["duration"]) - source_duration) > 0.01:
                    findings.append(
                        f"silence interval {index}: source duration does not match start and end"
                    )
                if source_duration + 0.001 < min_duration:
                    findings.append(
                        f"silence interval {index}: detected silence {source_duration:.3f}s "
                        f"is shorter than policy minimum {min_duration:.3f}s"
                    )
                cut_start = 0.0 if source_start <= 0.001 else source_start + padding
                cut_end = duration if duration is not None and source_end >= duration - 0.001 else source_end - padding
                for segment in segments:
                    overlap = min(cut_end, segment["end"]) - max(cut_start, segment["start"])
                    if overlap > MAX_VAD_OVERLAP_SECONDS:
                        findings.append(
                            f"silence interval {index}: planned silence overlaps VAD speech by {overlap:.3f}s"
                        )
                        break

    for index, item in enumerate(plan.get("remove_intervals", []), 1):
        start = float(item["start"])
        end = float(item["end"])
        reason = str(item.get("reason", ""))
        reason_lower = reason.lower()
        span = end - start
        is_speech_cut = not (
            reason_lower.startswith("silence") and "marker" not in reason_lower
        )
        if is_speech_cut and not marker_hits(reason):
            source_timestamp = item.get("source_timestamp")
            if not isinstance(source_timestamp, (int, float)):
                findings.append(
                    f"interval {index}: speech cut lacks detected marker or numeric source_timestamp"
                )
                continue
            if not start <= float(source_timestamp) <= end:
                findings.append(
                    f"interval {index}: source_timestamp must fall inside the removal interval"
                )
                continue
        hits = marker_hits(reason)
        if not hits:
            continue

        safe_long = any(label in reason for label in SAFE_LONG_REASONS)
        if span > max_marker_cut and not safe_long:
            findings.append(
                f"interval {index}: broad marker cut {start:.3f}-{end:.3f} "
                f"({span:.3f}s); use local_correction or mark a supported full_retake"
            )

        for marker_id, marker_at in hits:
            prev, nxt = neighbors(segments, marker_at) if segments else (None, None)
            label = f"marker {marker_id}" if marker_id is not None else "marker"
            if prev and start <= prev["start"] + 0.15 and span > max_marker_cut and not safe_long:
                findings.append(
                    f"interval {index}: {label} starts at previous VAD segment "
                    f"{prev['start']:.3f}; verify this is not a local correction"
                )
            if segments and not has_following_speech(segments, marker_at) and not safe_long:
                findings.append(f"interval {index}: {label} has no following speech retake; use skip or trailing trim")
            if duration is not None and end >= duration - 0.05 and not safe_long:
                findings.append(f"interval {index}: {label} cuts to end of file; tail markers need explicit review")

    return findings


def run_self_test() -> int:
    broad = {
        "duration": 30.0,
        "remove_intervals": [
            {
                "start": 10.0,
                "end": 18.0,
                "reason": "cut_before_marker: marker 1 at 15.0s",
            },
            {
                "start": 24.0,
                "end": 30.0,
                "reason": "cut_before_marker: marker 2 at 27.0s",
            },
        ],
    }
    findings = audit_plan(broad, Path("/tmp/plan.json"), 4.0)
    assert any("broad marker cut" in item for item in findings), findings
    assert any("cuts to end" in item for item in findings), findings

    safe = {
        "remove_intervals": [
            {
                "start": 14.2,
                "end": 15.4,
                "reason": "local_correction: marker 1 at 15.0s",
            }
        ]
    }
    assert not audit_plan(safe, Path("/tmp/plan.json"), 4.0)
    unmarked = {
        "remove_intervals": [
            {"start": 14.2, "end": 15.4, "reason": "local_correction: repeated phrase"}
        ]
    }
    findings = audit_plan(unmarked, Path("/tmp/plan.json"), 4.0)
    assert any("lacks detected marker or numeric source_timestamp" in item for item in findings), findings
    user_marked = {
        "remove_intervals": [
            {
                "start": 14.2,
                "end": 15.4,
                "source_timestamp": 15.0,
                "reason": "local_correction: user-selected location",
            }
        ]
    }
    assert not audit_plan(user_marked, Path("/tmp/plan.json"), 4.0)
    unsafe_silence = {
        "duration": 30.0,
        "remove_intervals": [{"start": 1.0, "end": 1.2, "reason": "silence"}],
    }
    findings = audit_plan(unsafe_silence, Path("/tmp/plan.json"), 4.0)
    assert any("missing silence_policy" in item for item in findings), findings
    reviewed_silence = {
        "duration": 30.0,
        "silence_policy": {"min_duration": 1.0, "padding": 0.3},
        "remove_intervals": [
            {
                "start": 1.3,
                "end": 4.7,
                "reason": "silence",
                "silence_sources": [{"start": 1.0, "end": 5.0, "duration": 4.0}],
            }
        ],
    }
    assert not audit_plan(reviewed_silence, Path("/tmp/plan.json"), 4.0)
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        speech = root / "speech.json"
        speech.write_text(json.dumps({"speech_segments": [{"start": 1.0, "end": 20.0}]}), encoding="utf-8")
        local_inside_segment = {
            "evidence": {"speech": str(speech)},
            "remove_intervals": [
                {
                    "start": 14.8,
                    "end": 15.2,
                    "reason": "local_correction: marker 1 at 15.0s",
                }
            ],
        }
        findings = audit_plan(local_inside_segment, root / "plan.json", 4.0)
        assert not any("no following speech retake" in item for item in findings), findings
    print("self_test: ok")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit reviewed video cut plans before render.")
    parser.add_argument("plan", nargs="?", type=Path)
    parser.add_argument("--max-marker-cut", type=float, default=4.0)
    parser.add_argument("--allow-findings", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.self_test:
        return run_self_test()
    if not args.plan:
        return fail("plan is required")
    plan_path = args.plan.expanduser().resolve()
    if not plan_path.exists():
        return fail(f"plan not found: {plan_path}")
    findings = audit_plan(load_json(plan_path), plan_path, args.max_marker_cut)
    if findings:
        for item in findings:
            print(f"finding: {item}")
        return 0 if args.allow_findings else 1
    print("audit: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
