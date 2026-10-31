#!/usr/bin/env python3
"""Render a speaker-labelled transcript as readable turns.

Usage: diar_views.py [--names names.json] <transcript-json> [source-offset-seconds]

The transcript comes from pyannote-chunks.py join: MOSS segments with one
global speaker label each, plus the stretches MOSS left empty although there
was speech. Consecutive segments of one speaker form a turn. When only one
speaker is found, a pause or a long monologue starts a new turn so a lecture
does not become one paragraph. Empty stretches are listed in time order so
the reader knows where text may be missing. Text is never changed.
``--names`` shows remembered voices (scripts/voices.py match) instead of
anonymous labels.
"""

from __future__ import annotations

import json
import math
import re
import sys
from pathlib import Path

Segment = tuple[float, float, str, str]

# Same split rule as Alt's single-speaker turns.
SINGLE_SPEAKER_PAUSE = 2.0
SINGLE_SPEAKER_MAX_TURN = 60.0


def load_transcript(path: Path) -> tuple[list[Segment], list[tuple[float, float]]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or not isinstance(payload.get("segments"), list):
        raise ValueError("transcript JSON must be an object with segments")
    segments: list[Segment] = []
    for index, item in enumerate(payload["segments"]):
        if not isinstance(item, dict):
            raise ValueError(f"invalid segment {index}")
        start, end = float(item["start"]), float(item["end"])
        if start < 0 or end < start:
            raise ValueError(f"invalid range at segment {index}")
        text = str(item.get("text", "")).strip()
        if text:
            segments.append((start, end, str(item.get("speaker") or "?"), text))
    gaps = [(float(a), float(b)) for a, b in payload.get("gaps", [])]
    return sorted(segments), sorted(gaps)


def timestamp(seconds: float) -> str:
    minutes, whole_seconds = divmod(max(0, int(seconds)), 60)
    return f"{minutes:02d}:{whole_seconds:02d}"


def display(label: str, names: dict) -> str:
    hit = names.get(label)
    if not hit:
        return label
    return hit["name"] if hit.get("sure") else f"{label} {hit['name']}?"


def turn_rows(segments: list[Segment], gaps: list[tuple[float, float]],
              names: dict | None = None) -> list[dict]:
    """Consecutive segments of one displayed speaker become one row; gaps get rows of their own.

    Two labels given the same name merge, since one person can still end up
    with two labels.
    """
    names = names or {}
    single = len({label for _, _, label, _ in segments} - {"?"}) == 1
    events = [(start, 0, (start, end, label, text)) for start, end, label, text in segments]
    events += [(start, 1, (start, end, "gap", "")) for start, end in gaps]
    rows: list[dict] = []
    previous_end = 0.0
    for _, _, (start, end, label, text) in sorted(events):
        if label == "gap":
            rows.append({"label": label, "start": start, "end": end, "text": ""})
            continue
        split = single and rows and (
            start - previous_end >= SINGLE_SPEAKER_PAUSE
            or end - rows[-1]["start"] > SINGLE_SPEAKER_MAX_TURN
        )
        last = rows[-1] if rows else None
        if last and last["label"] != "gap" and display(last["label"], names) == display(label, names) and not split:
            last["end"] = end
            last["text"] += " " + text
        else:
            rows.append({"label": label, "start": start, "end": end, "text": text})
        previous_end = end
    for row in rows:
        row["text"] = re.sub(r"\s+", " ", row["text"]).strip()
    return rows


def render(segments: list[Segment], gaps: list[tuple[float, float]],
           source_offset: float = 0.0, names: dict | None = None) -> str:
    names = names or {}
    lines = []
    for row in turn_rows(segments, gaps, names):
        at = timestamp(row["start"] + source_offset)
        if row["label"] == "gap":
            lines.append(f"**[gap]** ({at}~{timestamp(row['end'] + source_offset)})")
        else:
            lines.append(f"**[{display(row['label'], names)}]** ({at}) {row['text']}")
    return "\n\n".join(lines)


def main(argv: list[str]) -> int:
    names_path = None
    if len(argv) > 2 and argv[1] == "--names":
        names_path, argv = Path(argv[2]), argv[:1] + argv[3:]
    if len(argv) not in (2, 3):
        print("usage: diar_views.py [--names names.json] <transcript-json> [source-offset-seconds]",
              file=sys.stderr)
        return 64
    try:
        names = json.loads(names_path.read_text(encoding="utf-8")) if names_path else {}
        source_offset = float(argv[2]) if len(argv) == 3 else 0.0
        if not math.isfinite(source_offset) or source_offset < 0:
            raise ValueError("source offset must be nonnegative seconds")
        output = render(*load_transcript(Path(argv[1])), source_offset, names)
    except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        print(f"diarization render failed: {exc}", file=sys.stderr)
        return 65
    if output:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
