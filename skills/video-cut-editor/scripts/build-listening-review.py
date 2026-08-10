#!/usr/bin/env python3
"""Build or validate an offline HTML editor for human listening review."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any
from urllib.parse import quote

from video_silence_cut import ffprobe_json, parse_duration, require_tool

TEMPLATE = Path(__file__).resolve().parent.parent / "assets" / "listening-review.html"
JOIN_MAP_SCHEMA = "video-cut-editor.join-map.v1"
REVIEW_SCHEMA = "video-cut-editor.listening-review.v1"
RISK_REASONS = (
    "marker",
    "full_retake",
    "local_correction",
    "cut_before_marker",
    "cut_after_marker",
    "intentional_long_cut",
    "repeated_take",
    "abandoned_phrase",
    "self_correction",
)
POINT_MERGE_TOLERANCE_SECONDS = 0.05
# 접합점 앞뒤로 카드에 싣는 전사 범위. 끊긴 문장과 중복된 문장이 한 화면에서 보일 만큼 넓고,
# 카드가 목록을 밀어내지 않을 만큼 좁다.
TRANSCRIPT_WINDOW_SECONDS = 12.0


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_join_map(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema") != JOIN_MAP_SCHEMA:
        raise ValueError(f"join map schema must be {JOIN_MAP_SCHEMA}")
    joins = data.get("joins")
    if not isinstance(joins, list):
        raise ValueError("join map must contain a joins array")
    if not all(isinstance(item, dict) for item in joins):
        raise ValueError("every join must be an object")
    return data


def reason_text(item: dict[str, Any]) -> str:
    reasons = item.get("reasons") or []
    if isinstance(reasons, str):
        reasons = [reasons]
    if not isinstance(reasons, list):
        raise ValueError("join reasons must be a string or array")
    return " / ".join(str(value) for value in reasons)


def source_span(item: dict[str, Any]) -> dict[str, float] | None:
    """반려 시 고칠 원본 좌표. cut plan은 원본 타임라인으로 적히므로 최종본 시각만으로는 못 고친다."""
    keys = ("left_source_end", "right_source_start", "removed_duration")
    if not all(key in item for key in keys):
        return None
    try:
        left, right, removed = (float(item[key]) for key in keys)
    except (TypeError, ValueError):
        return None
    if not all(math.isfinite(value) for value in (left, right, removed)):
        return None
    return {
        "left_end": round(left, 3),
        "right_start": round(right, 3),
        "removed": round(removed, 3),
    }


def priority_points(joins: list[dict[str, Any]]) -> list[dict[str, Any]]:
    points: list[dict[str, Any]] = []
    for item in joins:
        reason = reason_text(item)
        kind = str(item.get("type", "join"))
        if kind != "merge_join" and not any(
            token in reason.lower() for token in RISK_REASONS
        ):
            continue
        try:
            timestamp = float(item["output_time"])
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError("priority join output_time must be numeric") from exc
        if not math.isfinite(timestamp) or timestamp < 0:
            raise ValueError(
                "priority join output_time must be a non-negative finite number"
            )
        point = {
            "id": f"join-{item.get('index', len(points) + 1)}",
            "time": round(timestamp, 6),
            "kind": kind,
            "label": "파일 연결부" if kind == "merge_join" else "마커 접합부",
            "reason": reason or kind,
        }
        span = source_span(item)
        if span:
            point["source"] = span
        points.append(point)
    return points


def srt_seconds(value: str) -> float:
    hours, minutes, rest = value.strip().replace(",", ".").split(":")
    return int(hours) * 3600 + int(minutes) * 60 + float(rest)


def parse_srt(text: str) -> list[dict[str, Any]]:
    segments: list[dict[str, Any]] = []
    for block in re.split(r"\n\s*\n", text.strip()):
        lines = [line for line in block.splitlines() if line.strip()]
        timing = next((line for line in lines if "-->" in line), None)
        if not timing:
            continue
        start, _, end = timing.partition("-->")
        body = " ".join(lines[lines.index(timing) + 1 :]).strip()
        if body:
            segments.append(
                {"start": srt_seconds(start), "end": srt_seconds(end), "text": body}
            )
    return segments


def load_transcript(path: Path) -> list[dict[str, Any]]:
    """apple-stt/whisper의 JSON(`[{start,end,text}]` 또는 `{"segments": [...]}`)과 SRT를 받는다."""
    text = path.read_text(encoding="utf-8")
    if "-->" in text[:400]:
        segments: Any = parse_srt(text)
    else:
        data = json.loads(text)
        segments = data.get("segments") if isinstance(data, dict) else data
    if not isinstance(segments, list):
        raise ValueError(
            "transcript must be a segment array or an object with segments"
        )
    parsed: list[dict[str, Any]] = []
    for segment in segments:
        if not isinstance(segment, dict):
            raise ValueError("every transcript segment must be an object")
        body = str(segment.get("text", "")).strip()
        if not body:
            continue
        try:
            start = float(segment["start"])
            end = float(segment.get("end", segment["start"]))
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError("transcript segments need numeric start/end") from exc
        parsed.append({"start": round(start, 3), "end": round(end, 3), "text": body})
    if not parsed:
        raise ValueError(f"transcript has no usable segments: {path}")
    return sorted(parsed, key=lambda item: item["start"])


def transcript_context(
    segments: list[dict[str, Any]], timestamp: float
) -> list[dict[str, Any]]:
    window: list[dict[str, Any]] = []
    for segment in segments:
        if segment["end"] < timestamp - TRANSCRIPT_WINDOW_SECONDS:
            continue
        if segment["start"] > timestamp + TRANSCRIPT_WINDOW_SECONDS:
            break
        if segment["end"] <= timestamp:
            side = "before"
        elif segment["start"] >= timestamp:
            side = "after"
        else:
            side = "span"
        window.append({**segment, "side": side})
    return window


def parse_point(value: str, index: int) -> dict[str, Any]:
    seconds, separator, label = value.partition(":")
    if not separator or not label.strip():
        raise ValueError("--point must be SECONDS:LABEL")
    timestamp = float(seconds)
    if not math.isfinite(timestamp) or timestamp < 0:
        raise ValueError("--point seconds must be a non-negative finite number")
    return {
        "id": f"manual-{index}",
        "time": round(timestamp, 6),
        "kind": "manual",
        "label": label.strip(),
        "reason": "manual review point",
    }


def merge_review_points(points: list[dict[str, Any]]) -> list[dict[str, Any]]:
    merged = [point for point in points if point["kind"] != "manual"]
    for point in (point for point in points if point["kind"] == "manual"):
        existing = next(
            (
                item
                for item in merged
                if item["kind"] != "manual"
                and abs(float(item["time"]) - float(point["time"]))
                <= POINT_MERGE_TOLERANCE_SECONDS
            ),
            None,
        )
        if existing:
            existing["label"] = point["label"]
        else:
            merged.append(point)
    return sorted(merged, key=lambda item: item["time"])


def json_for_html(value: Any) -> str:
    return (
        json.dumps(value, ensure_ascii=False)
        .replace("&", "\\u0026")
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
        .replace("\u2028", "\\u2028")
        .replace("\u2029", "\\u2029")
    )


def media_context(media: Path, join_map: Path) -> dict[str, Any]:
    return {
        "media": {
            "path": str(media),
            "size_bytes": media.stat().st_size,
            "sha256": sha256(media),
        },
        "join_map": {"path": str(join_map), "sha256": sha256(join_map)},
    }


def validate_join_map(media: Path, data: dict[str, Any], media_duration: float) -> None:
    output = data.get("output")
    if (
        not isinstance(output, str)
        or Path(output).expanduser().resolve() != media.resolve()
    ):
        raise ValueError(f"join map output does not match media: {output!r}")
    mapped_duration = data.get("actual_output_duration")
    if (
        mapped_duration is not None
        and abs(float(mapped_duration) - media_duration) > 0.25
    ):
        raise ValueError(
            f"join map duration {float(mapped_duration):.3f}s does not match media {media_duration:.3f}s"
        )


def build_review(
    media: Path,
    join_map: Path,
    output: Path,
    title: str,
    manual_points: list[str],
    *,
    media_duration: float | None = None,
    transcript: Path | None = None,
) -> int:
    data = load_join_map(join_map)
    duration = media_duration
    if duration is None:
        duration = parse_duration(ffprobe_json(require_tool("ffprobe"), media))
    validate_join_map(media, data, duration)
    points = priority_points(data["joins"])
    points.extend(
        parse_point(value, index) for index, value in enumerate(manual_points, 1)
    )
    points = merge_review_points(points)
    if any(point["time"] > duration for point in points):
        raise ValueError(f"review point exceeds media duration {duration:.3f}s")
    if transcript:
        segments = load_transcript(transcript)
        for point in points:
            point["transcript"] = transcript_context(segments, point["time"])

    output.parent.mkdir(parents=True, exist_ok=True)
    media_url = quote(Path(os.path.relpath(media, output.parent)).as_posix(), safe="/")
    context = media_context(media, join_map)
    rendered = TEMPLATE.read_text(encoding="utf-8")
    replacements = {
        "__TITLE_HTML__": html.escape(title),
        "__TITLE_JSON__": json_for_html(title),
        "__MEDIA_URL_JSON__": json_for_html(media_url),
        "__REVIEW_CONTEXT_JSON__": json_for_html(context),
        "__STORAGE_KEY_JSON__": json_for_html(
            f"video-cut-editor:{context['media']['sha256']}:{context['join_map']['sha256']}"
        ),
        "__POINTS_JSON__": json_for_html(points),
    }
    for placeholder, value in replacements.items():
        rendered = rendered.replace(placeholder, value)
    if any(placeholder in rendered for placeholder in replacements):
        raise RuntimeError("review template contains an unreplaced placeholder")
    output.write_text(rendered, encoding="utf-8")
    return len(points)


def validate_review(media: Path, join_map: Path, review: Path) -> None:
    data = json.loads(review.read_text(encoding="utf-8"))
    if data.get("schema") != REVIEW_SCHEMA:
        raise ValueError(f"review schema must be {REVIEW_SCHEMA}")
    current = media_context(media, join_map)
    for key in ("media", "join_map"):
        recorded = data.get(key)
        if (
            not isinstance(recorded, dict)
            or recorded.get("path") != current[key]["path"]
        ):
            raise ValueError(f"review {key} path does not match current input")
        if recorded.get("sha256") != current[key]["sha256"]:
            raise ValueError(f"review {key} hash does not match current input")
    items = data.get("items")
    if not isinstance(items, list) or not all(isinstance(item, dict) for item in items):
        raise ValueError("review items must be an array of objects")
    expected = {
        point["id"] for point in priority_points(load_join_map(join_map)["joins"])
    }
    approved = {item.get("id") for item in items if item.get("status") == "approved"}
    if not expected.issubset(approved):
        missing = ", ".join(sorted(expected - approved))
        raise ValueError(f"priority review points are not approved: {missing}")
    if data.get("status") != "approved" or data.get("full_listen") is not True:
        raise ValueError("review is not approved or full listening is incomplete")
    if any(item.get("status") != "approved" for item in items):
        raise ValueError("every review item must be approved")


def run_self_test() -> int:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        media = root / "lesson.mp4"
        media.touch()
        join_map = root / "lesson.join-map.json"
        join_map.write_text(
            json.dumps(
                {
                    "schema": JOIN_MAP_SCHEMA,
                    "output": str(media),
                    "actual_output_duration": 50,
                    "joins": [
                        {
                            "index": 1,
                            "type": "edit_join",
                            "output_time": 10,
                            "reasons": ["silence"],
                        },
                        {
                            "index": 2,
                            "type": "edit_join",
                            "output_time": 20,
                            "reasons": ["local_correction"],
                            "left_source_end": 25.5,
                            "right_source_start": 31.25,
                            "removed_duration": 5.75,
                        },
                        {
                            "index": 3,
                            "type": "merge_join",
                            "output_time": 30,
                            "reasons": ["merge"],
                        },
                    ],
                }
            ),
            encoding="utf-8",
        )
        srt = root / "lesson.srt"
        srt.write_text(
            "1\n00:00:14,000 --> 00:00:19,500\n앞 문장입니다\n\n"
            "2\n00:00:19,500 --> 00:00:20,500\n걸친 문장입니다\n\n"
            "3\n00:00:21,000 --> 00:00:26,000\n뒤 문장입니다\n",
            encoding="utf-8",
        )
        output = root / "review.html"
        count = build_review(
            media,
            join_map,
            output,
            "검수",
            ["19.999:수동 설명", "40:경고 지점"],
            media_duration=50,
            transcript=srt,
        )
        rendered = output.read_text(encoding="utf-8")
        assert count == 3
        assert "local_correction" in rendered
        assert "수동 설명" in rendered
        assert "경고 지점" in rendered
        assert "video.playbackRate = 2" in rendered
        assert 'class="review-layout"' in rendered
        assert 'id="active-marker"' in rendered
        assert "updateActivePoint" in rendered
        assert REVIEW_SCHEMA in rendered
        assert "__REVIEW_CONTEXT_JSON__" not in rendered
        assert "point-transcript" in rendered
        assert "앞 문장입니다" in rendered

        points = priority_points(load_join_map(join_map)["joins"])
        corrected = next(point for point in points if point["id"] == "join-2")
        assert corrected["source"] == {
            "left_end": 25.5,
            "right_start": 31.25,
            "removed": 5.75,
        }
        assert "source" not in next(
            point for point in points if point["id"] == "join-3"
        )
        segments = load_transcript(srt)
        sides = [
            line["side"] for line in transcript_context(segments, corrected["time"])
        ]
        assert sides == ["before", "span", "after"], sides

        transcript_json = root / "lesson.stt.json"
        transcript_json.write_text(
            json.dumps([{"start": 19.0, "end": 21.0, "text": "제이슨 문장"}]),
            encoding="utf-8",
        )
        assert load_transcript(transcript_json)[0]["text"] == "제이슨 문장"

        context = media_context(media, join_map)
        review = root / "review.json"
        review.write_text(
            json.dumps(
                {
                    "schema": REVIEW_SCHEMA,
                    **context,
                    "status": "approved",
                    "full_listen": True,
                    "items": [
                        {"id": "join-2", "status": "approved"},
                        {"id": "join-3", "status": "approved"},
                        {"id": "manual-2", "status": "approved"},
                    ],
                }
            ),
            encoding="utf-8",
        )
        validate_review(media, join_map, review)
        media.write_bytes(b"changed")
        try:
            validate_review(media, join_map, review)
        except ValueError:
            pass
        else:
            raise AssertionError("changed media must fail validation")
        media.write_bytes(b"")
        review.write_text(review.read_text().replace('"approved"', '"pending"', 1))
        try:
            validate_review(media, join_map, review)
        except ValueError:
            pass
        else:
            raise AssertionError("pending review must fail validation")
    print("self_test: ok")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a 2x browser listening review editor."
    )
    parser.add_argument("media", nargs="?", type=Path)
    parser.add_argument("join_map", nargs="?", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--title")
    parser.add_argument("--point", action="append", default=[], metavar="SECONDS:LABEL")
    parser.add_argument(
        "--transcript",
        type=Path,
        metavar="JSON_OR_SRT",
        help="final-media transcript; each card then shows what is said around its join",
    )
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--open", action="store_true")
    parser.add_argument("--validate", type=Path, metavar="REVIEW_JSON")
    parser.add_argument("--self-test", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.self_test:
        return run_self_test()
    if not args.media or not args.join_map:
        raise SystemExit("error: media and join_map are required")

    media = args.media.expanduser().resolve()
    join_map = args.join_map.expanduser().resolve()
    if not media.exists():
        raise SystemExit(f"error: media not found: {media}")
    if not join_map.exists():
        raise SystemExit(f"error: join map not found: {join_map}")

    if args.validate:
        review = args.validate.expanduser().resolve()
        if not review.exists():
            raise SystemExit(f"error: review JSON not found: {review}")
        validate_review(media, join_map, review)
        print("review_status: approved")
        return 0

    output = (
        args.output.expanduser().resolve()
        if args.output
        else media.with_name(f"{media.stem}.video-cut-artifacts")
        / f"{media.stem}.listening-review.html"
    )
    if output.exists() and not args.overwrite:
        raise SystemExit(
            f"error: output exists, archive it or pass --overwrite: {output}"
        )
    transcript = args.transcript.expanduser().resolve() if args.transcript else None
    if transcript and not transcript.exists():
        raise SystemExit(f"error: transcript not found: {transcript}")
    title = args.title or f"{media.stem} 청취 검수"
    count = build_review(
        media, join_map, output, title, args.point, transcript=transcript
    )
    print(f"output: {output}")
    print(f"review_points: {count}")
    print("default_speed: 2x")
    print(f"transcript: {transcript or 'not provided'}")

    if args.open:
        opener = shutil.which("open")
        if not opener:
            raise SystemExit("error: --open requires the macOS open command")
        subprocess.run([opener, str(output)], check=True)
        print("opened: yes")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, RuntimeError, ValueError, subprocess.CalledProcessError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1) from None
