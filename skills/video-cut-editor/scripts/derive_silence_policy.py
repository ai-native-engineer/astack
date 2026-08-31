#!/usr/bin/env python3
"""Derive a long-silence cut policy from a recording's own pause distribution."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


# A recording's silences are two mixed populations: speech rhythm (breaths, sentence
# boundaries) and waiting (loading, thinking, setup). Only the second may be cut.
# p93 sits past the rhythm population's decay in screen-recording lecture audio;
# below it a threshold starts eating ordinary sentence-boundary pauses.
THRESHOLD_PERCENTILE = 0.93
# Padding leaves half a typical long pause on each side, so a join reads as an
# ordinary pause instead of a splice. p75 is that typical long pause.
PADDING_PERCENTILE = 0.75
# A join costs continuity, so a cut has to buy back real time to be worth making.
DEFAULT_MIN_GAIN = 1.0
PADDING_BOUNDS = (0.30, 0.60)


def fail(message: str, code: int = 1) -> int:
    print(f"error: {message}", file=sys.stderr)
    return code


def load_durations(paths: list[Path]) -> tuple[list[float], list[str]]:
    durations: list[float] = []
    missing: list[str] = []
    for path in paths:
        if not path.is_file():
            missing.append(str(path))
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        silences = data.get("silencedetect", {}).get("silences", [])
        durations += [float(item["duration"]) for item in silences]
    return durations, missing


def percentile(sorted_values: list[float], fraction: float) -> float:
    if not sorted_values:
        raise ValueError("no silence candidates")
    index = min(len(sorted_values) - 1, int(len(sorted_values) * fraction))
    return sorted_values[index]


def histogram(sorted_values: list[float]) -> list[dict[str, Any]]:
    edges = [0.2, 0.5, 0.8, 1.0, 1.3, 1.6, 2.0, 2.5, 3.0, 4.0, 6.0, 10.0]
    rows = []
    for low, high in zip(edges, edges[1:] + [float("inf")]):
        count = sum(1 for value in sorted_values if low <= value < high)
        rows.append(
            {"low": low, "high": None if high == float("inf") else high, "count": count}
        )
    return rows


def derive(durations: list[float], min_gain: float) -> dict[str, Any]:
    values = sorted(durations)
    low, high = PADDING_BOUNDS
    padding = round(min(high, max(low, percentile(values, PADDING_PERCENTILE) / 2)), 2)
    # A threshold below 2*padding + min_gain cannot produce a cut that clears the
    # gain gate, so raise it to the point where every surviving cut is worth making.
    floor = 2 * padding + min_gain
    threshold = round(max(percentile(values, THRESHOLD_PERCENTILE), floor), 2)
    return {
        "min_duration": threshold,
        "padding": padding,
        "min_cut_gain": min_gain,
        "evidence": {
            "silences": len(values),
            "percentiles": {
                f"p{int(p * 100)}": round(percentile(values, p), 2)
                for p in (0.50, 0.75, 0.90, 0.93, 0.95, 0.98)
            },
            "threshold_source": (
                "percentile"
                if percentile(values, THRESHOLD_PERCENTILE) >= floor
                else "gain_floor"
            ),
            "histogram": histogram(values),
        },
    }


def render_report(policy: dict[str, Any], sources: list[Path]) -> str:
    evidence = policy["evidence"]
    lines = [
        "# Silence Policy",
        "",
        f"Sources: {', '.join(str(path) for path in sources)}",
        f"Silence candidates: {evidence['silences']}",
        "",
        "## Derived policy",
        "",
        f"- `--min-silence-duration {policy['min_duration']}`",
        f"- `--silence-padding {policy['padding']}`",
        f"- `--min-cut-gain {policy['min_cut_gain']}`",
        f"- each cut removes at least {round(policy['min_duration'] - 2 * policy['padding'], 2)}s",
        f"- each join keeps {round(2 * policy['padding'], 2)}s of pause",
        f"- threshold came from: {evidence['threshold_source']}",
        "",
        "## Pause distribution",
        "",
        "| percentile | " + " | ".join(evidence["percentiles"]) + " |",
        "|---|" + "---|" * len(evidence["percentiles"]),
        "| seconds | "
        + " | ".join(f"{v}" for v in evidence["percentiles"].values())
        + " |",
        "",
        "| range (s) | count |",
        "|---|---:|",
    ]
    for row in evidence["histogram"]:
        label = (
            f"{row['low']}+" if row["high"] is None else f"{row['low']} - {row['high']}"
        )
        lines.append(f"| {label} | {row['count']} |")
    lines += [
        "",
        "Cut only the waiting population. Confirm screen context before rendering; "
        "length alone does not justify a cut.",
    ]
    return "\n".join(lines) + "\n"


def run_self_test() -> int:
    # Rhythm population plus a waiting tail: the threshold must land past the rhythm.
    rhythm = [0.3] * 60 + [0.5] * 25 + [0.9] * 10
    waiting = [3.0, 5.0, 8.0, 20.0, 30.0]
    policy = derive(rhythm + waiting, DEFAULT_MIN_GAIN)
    assert policy["min_duration"] >= 1.6, policy
    assert PADDING_BOUNDS[0] <= policy["padding"] <= PADDING_BOUNDS[1], policy

    # Every surviving cut clears the gain gate.
    gain = policy["min_duration"] - 2 * policy["padding"]
    assert gain >= DEFAULT_MIN_GAIN - 1e-6, (gain, policy)

    # A recording with no dead air still gets a threshold above its own pauses.
    quiet = derive([0.3] * 200, DEFAULT_MIN_GAIN)
    assert quiet["min_duration"] >= 2 * quiet["padding"] + DEFAULT_MIN_GAIN - 1e-6, (
        quiet
    )
    assert quiet["evidence"]["threshold_source"] == "gain_floor", quiet

    assert percentile([1.0, 2.0, 3.0, 4.0], 0.5) == 3.0
    print("self_test: ok")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Derive a long-silence cut policy from a recording's pause distribution."
    )
    parser.add_argument("speech_json", nargs="*", type=Path)
    parser.add_argument(
        "--min-cut-gain",
        type=float,
        default=DEFAULT_MIN_GAIN,
        help="seconds a single cut must remove to be worth its join",
    )
    parser.add_argument("--output-json", type=Path)
    parser.add_argument("--output-md", type=Path)
    parser.add_argument("--self-test", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.self_test:
        return run_self_test()
    if not args.speech_json:
        return fail(
            "pass one or more speech.json paths from video_cut_workflow.py analyze"
        )

    paths = [path.expanduser().resolve() for path in args.speech_json]
    durations, missing = load_durations(paths)
    if missing:
        return fail(f"speech.json not found: {', '.join(missing)}")
    if not durations:
        return fail("no silence candidates in the given speech.json files")

    policy = derive(durations, args.min_cut_gain)
    policy["sources"] = [str(path) for path in paths]

    if args.output_json:
        args.output_json.parent.mkdir(parents=True, exist_ok=True)
        args.output_json.write_text(
            json.dumps(policy, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        print(f"json: {args.output_json}")
    if args.output_md:
        args.output_md.parent.mkdir(parents=True, exist_ok=True)
        args.output_md.write_text(render_report(policy, paths), encoding="utf-8")
        print(f"md: {args.output_md}")

    print(f"silences: {policy['evidence']['silences']}")
    print(f"min_duration: {policy['min_duration']}")
    print(f"padding: {policy['padding']}")
    print(f"min_cut_gain: {policy['min_cut_gain']}")
    print(f"threshold_source: {policy['evidence']['threshold_source']}")
    print(
        "build_mixed_cut_plan.py "
        f"--min-silence-duration {policy['min_duration']} "
        f"--silence-padding {policy['padding']} "
        f"--min-cut-gain {policy['min_cut_gain']}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
