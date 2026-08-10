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


def silence_intervals(
    speech_data: dict[str, Any],
    duration: float,
    min_duration: float,
    padding: float,
) -> list[dict[str, Any]]:
    removals: list[dict[str, Any]] = []
    for item in speech_data.get("silencedetect", {}).get("silences", []):
        raw_start = max(0.0, min(duration, float(item["start"])))
        raw_end = max(0.0, min(duration, float(item["end"])))
        raw_duration = raw_end - raw_start
        if raw_duration + 0.001 < min_duration:
            continue
        start = 0.0 if raw_start <= 0.001 else raw_start + padding
        end = duration if raw_end >= duration - 0.001 else raw_end - padding
        if end <= start + 0.001:
            continue
        removals.append(
            {
                "start": round(start, 6),
                "end": round(end, 6),
                "reason": "silence",
                "silence_sources": [
                    {
                        "start": round(raw_start, 6),
                        "end": round(raw_end, 6),
                        "duration": round(raw_duration, 6),
                    }
                ],
            }
        )
    return removals


def merge_removals(
    markers: list[dict[str, Any]], silences: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    tagged = [
        {**item, "marker_reasons": [str(item["reason"])], "silence_sources": []}
        for item in markers
    ] + [
        {**item, "marker_reasons": [], "silence_sources": list(item["silence_sources"])}
        for item in silences
    ]
    merged: list[dict[str, Any]] = []
    for item in sorted(tagged, key=lambda value: (float(value["start"]), float(value["end"]))):
        if not merged or float(item["start"]) > float(merged[-1]["end"]) + 0.001:
            merged.append(dict(item))
            continue
        current = merged[-1]
        current["end"] = max(float(current["end"]), float(item["end"]))
        current["marker_reasons"].extend(item["marker_reasons"])
        current["silence_sources"].extend(item["silence_sources"])

    output: list[dict[str, Any]] = []
    for item in merged:
        marker_reasons = list(dict.fromkeys(item.pop("marker_reasons")))
        silence_sources = item.get("silence_sources", [])
        if marker_reasons and silence_sources:
            item["reason"] = f"marker+silence: {'; '.join(marker_reasons)}"
        elif marker_reasons:
            item["reason"] = "; ".join(marker_reasons)
            item.pop("silence_sources", None)
        else:
            item["reason"] = "silence"
        item["start"] = round(float(item["start"]), 6)
        item["end"] = round(float(item["end"]), 6)
        output.append(item)
    return output


def build_plan(
    marker_plan_path: Path,
    speech_json_path: Path | None,
    output_plan_path: Path,
    final_output: Path | None,
    allow_draft: bool,
    min_silence_duration: float,
    silence_padding: float,
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
    silences = silence_intervals(speech_data, duration, min_silence_duration, silence_padding)
    removals = merge_removals(markers, silences)
    final_output = final_output.expanduser().resolve() if final_output else source.with_name(f"{source.stem}.edited{source.suffix}")

    return {
        "source": str(source),
        "output": str(final_output),
        "status": "reviewed",
        "duration": round(duration, 6),
        "silence_policy": {
            "source": "ffmpeg_silencedetect",
            "min_duration": min_silence_duration,
            "padding": silence_padding,
        },
        "remove_intervals": removals,
        "evidence": {
            "marker_plan": str(marker_plan_path),
            "speech": str(speech_json_path),
            "markers": marker_plan.get("evidence", {}).get("markers"),
            "windows": marker_plan.get("evidence", {}).get("windows", []),
        },
        "render_notes": [
            "Marker intervals were reviewed before silence removal.",
            "Only explicit long silences from ffmpeg silencedetect were removed.",
            "Times are original source seconds; render once from original.",
        ],
    }


def run_self_test() -> int:
    from audit_cut_plan import audit_plan

    speech_data = {
        "silencedetect": {
            "silences": [
                {"start": 0.0, "end": 0.4},
                {"start": 5.0, "end": 7.0},
                {"start": 9.0, "end": 10.0},
            ]
        }
    }
    silences = silence_intervals(speech_data, 10.0, 1.0, 0.3)
    assert [(item["start"], item["end"]) for item in silences] == [(5.3, 6.7), (9.3, 10.0)]
    markers = [{"start": 10.0, "end": 27.0, "reason": "cut_before_marker: marker 1 at 15.0s"}]
    assert merge_removals(markers, [])[0]["reason"] == "cut_before_marker: marker 1 at 15.0s"
    mixed = {
        "remove_intervals": [
            {"start": 10.0, "end": 27.0, "reason": "cut_before_marker: marker 1 at 15.0s"}
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
    parser.add_argument("--min-silence-duration", type=float, default=1.0)
    parser.add_argument("--silence-padding", type=float, default=0.30)
    parser.add_argument("--allow-draft", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.self_test:
        return run_self_test()
    if not args.marker_plan:
        return fail("--marker-plan is required")
    if args.min_silence_duration < 0.8:
        return fail("--min-silence-duration must be >= 0.8")
    if args.silence_padding < 0:
        return fail("--silence-padding must be >= 0")
    output_plan = args.output_plan or args.marker_plan.expanduser().resolve().with_name("cut-plan.json")
    try:
        plan = build_plan(
            args.marker_plan,
            args.speech_json,
            output_plan,
            args.final_output,
            args.allow_draft,
            args.min_silence_duration,
            args.silence_padding,
        )
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
