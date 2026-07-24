#!/usr/bin/env python3
"""Merge Apple transcript ranges with Argmax diarization without replacing text.

Usage: diar_views.py <apple-json> <diar-rttm> [source-offset-seconds]

An Apple range that overlaps more than one speaker is labelled ``mixed``. Text is
never split heuristically or reassigned to the dominant speaker.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path


def load_turns(path: Path) -> list[tuple[float, float, str]]:
    turns: list[tuple[float, float, str]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        fields = line.split()
        if not fields or fields[0] != "SPEAKER":
            continue
        if len(fields) < 9:
            raise ValueError(f"invalid RTTM line {line_number}: expected at least 9 fields")
        try:
            start = float(fields[-7])
            duration = float(fields[-6])
        except ValueError as exc:
            raise ValueError(f"invalid RTTM time at line {line_number}") from exc
        if start < 0 or duration <= 0:
            raise ValueError(f"invalid RTTM range at line {line_number}")
        turns.append((start, start + duration, fields[-3]))
    return sorted(turns)


def load_segments(path: Path) -> list[tuple[float, float, str]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    raw_segments = payload.get("segments", []) if isinstance(payload, dict) else payload
    if not isinstance(raw_segments, list):
        raise ValueError("Apple JSON must be a segment array or an object with segments")

    segments: list[tuple[float, float, str]] = []
    for index, item in enumerate(raw_segments):
        if not isinstance(item, dict):
            raise ValueError(f"invalid Apple segment at index {index}")
        start = float(item.get("start", 0.0))
        end = float(item.get("end", start))
        text = str(item.get("text", "")).strip()
        if start < 0 or end < start:
            raise ValueError(f"invalid Apple range at index {index}")
        if text:
            segments.append((start, end, text))
    return segments


def speaker_label(start: float, end: float, turns: list[tuple[float, float, str]]) -> str:
    speakers = {
        speaker
        for turn_start, turn_end, speaker in turns
        if min(end, turn_end) - max(start, turn_start) > 0
    }
    if not speakers:
        return "?"
    if len(speakers) > 1:
        return "mixed"
    return next(iter(speakers))


def timestamp(seconds: float) -> str:
    minutes, whole_seconds = divmod(max(0, int(seconds)), 60)
    return f"{minutes:02d}:{whole_seconds:02d}"


def render(
    segments: list[tuple[float, float, str]],
    turns: list[tuple[float, float, str]],
    source_offset: float = 0.0,
) -> str:
    rows: list[str] = []
    current_label: str | None = None
    current_start = 0.0
    buffer: list[str] = []

    for start, end, text in segments:
        label = speaker_label(start, end, turns)
        if label != current_label:
            if buffer:
                rows.append(
                    f"**[{current_label}]** ({timestamp(current_start + source_offset)}) "
                    + " ".join(buffer)
                )
            current_label = label
            current_start = start
            buffer = [text]
        else:
            buffer.append(text)

    if buffer:
        rows.append(
            f"**[{current_label}]** ({timestamp(current_start + source_offset)}) "
            + " ".join(buffer)
        )
    return "\n\n".join(rows)


def main(argv: list[str]) -> int:
    if len(argv) not in (3, 4):
        print(
            "usage: diar_views.py <apple-json> <diar-rttm> [source-offset-seconds]",
            file=sys.stderr,
        )
        return 64
    try:
        source_offset = float(argv[3]) if len(argv) == 4 else 0.0
        if not math.isfinite(source_offset) or source_offset < 0:
            raise ValueError("source offset must be nonnegative seconds")
        output = render(
            load_segments(Path(argv[1])), load_turns(Path(argv[2])), source_offset
        )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"diarization merge failed: {exc}", file=sys.stderr)
        return 65
    if output:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
