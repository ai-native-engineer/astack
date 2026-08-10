#!/usr/bin/env python3
"""Triage visual continuity at every known edit or merge join."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


SSIM_RE = re.compile(r"\bAll:([0-9.]+)")


def fail(message: str, code: int = 1) -> int:
    print(f"error: {message}", file=sys.stderr)
    return code


def require_tool(name: str) -> str:
    path = shutil.which(name)
    if not path:
        raise RuntimeError(f"missing required tool: {name}")
    return path


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def ssim_filter(width: int) -> str:
    return (
        f"[0:v:0]setpts=PTS-STARTPTS,scale={width}:-2[left];"
        f"[1:v:0]setpts=PTS-STARTPTS,scale={width}:-2[right];"
        "[left][right]ssim"
    )


def parse_ssim(text: str) -> float:
    matches = SSIM_RE.findall(text)
    if not matches:
        raise ValueError("ffmpeg SSIM output did not contain an All score")
    return float(matches[-1])


def measure_ssim(ffmpeg: str, media: Path, at: float, frame_gap: float, width: int) -> float:
    before = max(0.0, at - frame_gap)
    after = at + frame_gap
    proc = subprocess.run(
        [
            ffmpeg,
            "-hide_banner",
            "-nostdin",
            "-v",
            "info",
            "-ss",
            f"{before:.6f}",
            "-i",
            str(media),
            "-ss",
            f"{after:.6f}",
            "-i",
            str(media),
            "-filter_complex",
            ssim_filter(width),
            "-an",
            "-frames:v",
            "1",
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
    return parse_ssim(proc.stderr)


def write_review_strip(ffmpeg: str, media: Path, at: float, width: int, output: Path) -> None:
    start = max(0.0, at - 0.5)
    proc = subprocess.run(
        [
            ffmpeg,
            "-hide_banner",
            "-nostdin",
            "-v",
            "error",
            "-y",
            "-ss",
            f"{start:.6f}",
            "-t",
            "1.0",
            "-i",
            str(media),
            "-vf",
            f"fps=10,scale={width}:-2,tile=5x2:padding=4:margin=4:color=black",
            "-frames:v",
            "1",
            "-q:v",
            "2",
            str(output),
        ],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if proc.returncode != 0:
        raise RuntimeError((proc.stderr or proc.stdout).strip())


def audit(
    media: Path,
    join_map: Path,
    threshold: float,
    frame_gap: float,
    width: int,
    review_dir: Path,
    force: bool,
) -> dict[str, Any]:
    data = load_json(join_map)
    joins = [item for item in data.get("joins", []) if isinstance(item, dict)]
    if not joins:
        raise ValueError("join map has no joins")

    ffmpeg = require_tool("ffmpeg")
    review_dir.mkdir(parents=True, exist_ok=True)
    checked: list[dict[str, Any]] = []
    for position, join in enumerate(joins, 1):
        if "output_time" not in join:
            raise ValueError(f"join {position} has no output_time")
        at = float(join["output_time"])
        score = measure_ssim(ffmpeg, media, at, frame_gap, width)
        candidate = score < threshold
        item: dict[str, Any] = {
            "index": join.get("index", position),
            "output_time": round(at, 6),
            "type": join.get("type", "join"),
            "ssim": round(score, 6),
            "status": "candidate" if candidate else "similar",
            "join": join,
        }
        if candidate:
            strip = review_dir / f"join-{position:03d}-ssim-{score:.6f}.jpg"
            if strip.exists() and not force:
                raise FileExistsError(f"refusing to overwrite review strip; pass --force: {strip}")
            write_review_strip(ffmpeg, media, at, width, strip)
            item["review_strip"] = str(strip)
        checked.append(item)
        print(f"join {position}/{len(joins)}: {score:.6f} {item['status']}")

    candidates = sum(1 for item in checked if item["status"] == "candidate")
    return {
        "schema": "video-cut-editor.visual-join-audit.v1",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "media": str(media),
        "join_map": str(join_map),
        "settings": {"threshold": threshold, "frame_gap": frame_gap, "width": width},
        "summary": {
            "joins": len(checked),
            "candidates": candidates,
            "similar": len(checked) - candidates,
            "direct_review_required": candidates,
        },
        "joins": checked,
    }


def write_markdown(path: Path, report: dict[str, Any]) -> None:
    summary = report["summary"]
    lines = [
        "# Visual Join Audit",
        "",
        f"Media: `{report['media']}`",
        f"Join map: `{report['join_map']}`",
        "",
        "SSIM ranks candidates only. Every candidate remains unresolved until its frame strip is inspected.",
        "",
        "## Summary",
        "",
        f"- Joins checked: `{summary['joins']}`",
        f"- Candidates: `{summary['candidates']}`",
        f"- Similar: `{summary['similar']}`",
        "",
        "## Candidates",
        "",
    ]
    candidates = [item for item in report["joins"] if item["status"] == "candidate"]
    if not candidates:
        lines.append("- None")
    for item in candidates:
        lines.append(
            f"- join `{item['index']}` at `{item['output_time']:.3f}s`: "
            f"SSIM `{item['ssim']:.6f}`, strip `{item['review_strip']}`"
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_self_test() -> int:
    sample = "[Parsed_ssim_4] SSIM Y:0.9 U:0.9 V:0.9 All:0.876935 (9.0)"
    assert parse_ssim(sample) == 0.876935
    filter_text = ssim_filter(640)
    assert filter_text.count("setpts=PTS-STARTPTS") == 2, filter_text
    assert "[left][right]ssim" in filter_text
    print("self_test: ok")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Triage visual continuity at every known video join.")
    parser.add_argument("media", nargs="?", type=Path)
    parser.add_argument("join_map", nargs="?", type=Path)
    parser.add_argument("--threshold", type=float, default=0.95)
    parser.add_argument("--frame-gap", type=float, default=0.10)
    parser.add_argument("--width", type=int, default=640)
    parser.add_argument("--output-json", type=Path)
    parser.add_argument("--output-md", type=Path)
    parser.add_argument("--review-dir", type=Path)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.self_test:
        return run_self_test()
    if not args.media or not args.join_map:
        return fail("media and join_map are required")
    if not 0.0 < args.threshold <= 1.0:
        return fail("--threshold must be greater than 0 and at most 1")
    if args.frame_gap <= 0 or args.width <= 0:
        return fail("--frame-gap and --width must be greater than 0")

    media = args.media.expanduser().resolve()
    join_map = args.join_map.expanduser().resolve()
    if not media.is_file():
        return fail(f"media not found: {media}")
    if not join_map.is_file():
        return fail(f"join map not found: {join_map}")
    output_json = (args.output_json or join_map.with_suffix(".visual-audit.json")).expanduser().resolve()
    output_md = (args.output_md or join_map.with_suffix(".visual-audit.md")).expanduser().resolve()
    review_dir = (args.review_dir or join_map.parent / "visual-review").expanduser().resolve()
    if output_json == output_md or review_dir in (output_json, output_md):
        return fail("output JSON, Markdown, and review directory must use distinct paths")
    existing = [path for path in (output_json, output_md) if path.exists()]
    if existing and not args.force:
        return fail(f"refusing to overwrite output; pass --force: {existing[0]}")
    try:
        report = audit(
            media, join_map, args.threshold, args.frame_gap, args.width, review_dir, args.force
        )
        write_json(output_json, report)
        write_markdown(output_md, report)
    except Exception as exc:
        return fail(str(exc))

    print(f"json: {output_json}")
    print(f"md: {output_md}")
    print(f"candidates: {report['summary']['candidates']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
