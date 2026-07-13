#!/usr/bin/env python3
"""Build a final marker+silence cut plan after marker review."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def fail(message: str, code: int = 1) -> int:
    print(f"error: {message}", file=sys.stderr)
    return code


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def speech_path(marker_plan: dict[str, Any], marker_plan_path: Path, explicit: Path | None) -> Path:
    if explicit is not None:
        return explicit.expanduser().resolve()
    raw = marker_plan.get("evidence", {}).get("speech")
    if not isinstance(raw, str):
        raise ValueError("--speech-json is required when marker plan has no evidence.speech")
    path = Path(raw).expanduser()
    return path if path.is_absolute() else (marker_plan_path.parent / path).resolve()


def marker_intervals(marker_plan: dict[str, Any]) -> list[dict[str, Any]]:
    intervals = []
    for item in marker_plan.get("remove_intervals", []):
        start = float(item["start"])
        end = float(item["end"])
        if end <= start:
            raise ValueError(f"invalid marker interval: {item}")
        reason = str(item.get("reason", "marker")).strip() or "marker"
        if "marker" not in reason.lower():
            reason = f"marker: {reason}"
        intervals.append({"start": start, "end": end, "reason": reason})
    return sorted(intervals, key=lambda item: float(item["start"]))


def subtract_intervals(
    speech_segments: list[dict[str, Any]],
    cuts: list[tuple[float, float]],
) -> list[tuple[float, float]]:
    kept: list[tuple[float, float]] = []
    for segment in speech_segments:
        parts = [(float(segment["start"]), float(segment["end"]))]
        for cut_start, cut_end in cuts:
            next_parts = []
            for start, end in parts:
                if cut_end <= start or cut_start >= end:
                    next_parts.append((start, end))
                    continue
                if cut_start > start:
                    next_parts.append((start, min(cut_start, end)))
                if cut_end < end:
                    next_parts.append((max(cut_end, start), end))
            parts = next_parts
        kept.extend((start, end) for start, end in parts if end - start > 0.001)
    return sorted(kept)


def complement(duration: float, kept: list[tuple[float, float]]) -> list[tuple[float, float]]:
    removals = []
    cursor = 0.0
    for start, end in kept:
        start = max(0.0, min(duration, start))
        end = max(0.0, min(duration, end))
        if start > cursor + 0.001:
            removals.append((cursor, start))
        cursor = max(cursor, end)
    if cursor < duration - 0.001:
        removals.append((cursor, duration))
    return [(round(start, 6), round(end, 6)) for start, end in removals if end - start > 0.001]


def marker_tuples(markers: list[dict[str, Any]]) -> list[tuple[float, float]]:
    return [(float(item["start"]), float(item["end"])) for item in markers]


def removal_reason(start: float, end: float, markers: list[dict[str, Any]]) -> str:
    hits = [
        item
        for item in markers
        if float(item["end"]) > start + 0.001 and float(item["start"]) < end - 0.001
    ]
    if not hits:
        return "silence"

    reasons = []
    seen = set()
    marker_start = min(float(item["start"]) for item in hits)
    marker_end = max(float(item["end"]) for item in hits)
    for item in hits:
        reason = str(item["reason"])
        if reason in seen:
            continue
        seen.add(reason)
        reasons.append(reason)
    prefix = "marker+silence" if start < marker_start - 0.001 or end > marker_end + 0.001 else "marker"
    return f"{prefix}: {'; '.join(reasons)}"


def build_plan(
    marker_plan_path: Path,
    speech_json_path: Path | None,
    output_plan_path: Path,
    final_output: Path | None,
    allow_draft: bool,
) -> dict[str, Any]:
    marker_plan_path = marker_plan_path.expanduser().resolve()
    marker_plan = load_json(marker_plan_path)
    if marker_plan.get("status") != "reviewed" and not allow_draft:
        raise ValueError("marker plan status must be reviewed; pass --allow-draft to bypass")

    source = Path(marker_plan["source"]).expanduser().resolve()
    speech_json_path = speech_path(marker_plan, marker_plan_path, speech_json_path)
    speech_data = load_json(speech_json_path)
    duration = float(speech_data["duration"])
    markers = marker_intervals(marker_plan)
    kept = subtract_intervals(speech_data.get("speech_segments", []), marker_tuples(markers))
    removals = complement(duration, kept)
    final_output = final_output.expanduser().resolve() if final_output else source.with_name(f"{source.stem}.edited{source.suffix}")

    return {
        "source": str(source),
        "output": str(final_output),
        "status": "reviewed",
        "duration": round(duration, 6),
        "remove_intervals": [
            {"start": start, "end": end, "reason": removal_reason(start, end, markers)}
            for start, end in removals
        ],
        "evidence": {
            "marker_plan": str(marker_plan_path),
            "speech": str(speech_json_path),
            "markers": marker_plan.get("evidence", {}).get("markers"),
            "windows": marker_plan.get("evidence", {}).get("windows", []),
        },
        "render_notes": [
            "Marker intervals were reviewed before silence removal.",
            "Final removals are the complement of speech after reviewed marker cuts.",
            "Times are original source seconds; render once from original.",
        ],
    }


def run_self_test() -> int:
    from audit_cut_plan import audit_plan

    speech = [{"start": 1.0, "end": 5.0}, {"start": 7.0, "end": 9.0}]
    kept = subtract_intervals(speech, [(2.0, 3.0), (8.0, 8.5)])
    assert kept == [(1.0, 2.0), (3.0, 5.0), (7.0, 8.0), (8.5, 9.0)], kept
    assert complement(10.0, kept) == [(0.0, 1.0), (2.0, 3.0), (5.0, 7.0), (8.0, 8.5), (9.0, 10.0)]
    markers = [{"start": 10.0, "end": 27.0, "reason": "cut_before_marker: marker 1 at 15.0s"}]
    assert removal_reason(10.0, 27.0, markers) == "marker: cut_before_marker: marker 1 at 15.0s"
    assert removal_reason(9.0, 27.0, markers).startswith("marker+silence: cut_before_marker")
    assert removal_reason(1.0, 2.0, markers) == "silence"
    mixed = {
        "remove_intervals": [
            {"start": 10.0, "end": 27.0, "reason": removal_reason(10.0, 27.0, markers)}
        ]
    }
    findings = audit_plan(mixed, Path("/tmp/mixed-cut-plan.json"), 4.0)
    assert any("broad marker cut" in item for item in findings), findings
    print("self_test: ok")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a final marker+silence cut plan after marker review.")
    parser.add_argument("--marker-plan", type=Path, required=False)
    parser.add_argument("--speech-json", type=Path)
    parser.add_argument("--output-plan", type=Path)
    parser.add_argument("--final-output", type=Path)
    parser.add_argument("--allow-draft", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.self_test:
        return run_self_test()
    if not args.marker_plan:
        return fail("--marker-plan is required")
    output_plan = args.output_plan or args.marker_plan.expanduser().resolve().with_name("cut-plan.json")
    try:
        plan = build_plan(args.marker_plan, args.speech_json, output_plan, args.final_output, args.allow_draft)
    except Exception as exc:
        return fail(str(exc))
    write_json(output_plan.expanduser().resolve(), plan)
    removed = sum(float(item["end"]) - float(item["start"]) for item in plan["remove_intervals"])
    print(f"plan: {output_plan.expanduser().resolve()}")
    print(f"remove_intervals: {len(plan['remove_intervals'])}")
    print(f"estimated_removed: {removed:.3f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
