#!/usr/bin/env python3
"""Analyze marker-based retake cuts and render reviewed cut plans."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime
from typing import Any

from video_silence_cut import (
    TimeRange,
    audio_output_options,
    build_ffmpeg_command,
    build_filter_graph,
    choose_encoder,
    ffmpeg_encoders,
    ffprobe_json,
    parse_duration,
    require_tool,
    run,
    streams,
    verify_output,
    video_output_options,
)


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MARKER = ROOT / "assets" / "triple-pulse.wav"


def fail(message: str, code: int = 1) -> int:
    print(f"error: {message}", file=sys.stderr)
    return code


def format_time(seconds: float) -> str:
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    remain = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{remain:06.3f}"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def run_checked(argv: list[str]) -> subprocess.CompletedProcess[str]:
    proc = subprocess.run(argv, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode != 0:
        raise RuntimeError((proc.stderr or proc.stdout).strip())
    return proc


def run_with_log(argv: list[str], log_path: Path | None) -> subprocess.CompletedProcess[str]:
    if log_path is None:
        return run(argv)

    log_path.parent.mkdir(parents=True, exist_ok=True)
    tail = bytearray()
    with log_path.open("ab") as log:
        log.write(f"\n=== {datetime.now().isoformat(timespec='seconds')} ===\n".encode())
        log.write(f"$ {shlex.join(argv)}\n".encode())
        log.flush()

        proc = subprocess.Popen(argv, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        assert proc.stdout is not None
        while True:
            chunk = proc.stdout.read(4096)
            if not chunk:
                break
            log.write(chunk)
            log.flush()
            tail.extend(chunk)
            if len(tail) > 65536:
                del tail[:-65536]
        code = proc.wait()

    return subprocess.CompletedProcess(
        argv,
        code,
        stdout="",
        stderr=tail.decode(errors="replace"),
    )


def default_workspace(media: Path) -> Path:
    return media.with_name(f"edit-{media.stem}-video-cut-editor")


def default_artifact_dir(output: Path) -> Path:
    return output.with_name(f"{output.stem}.video-cut-artifacts")


def extract_window(ffmpeg: str, media: Path, start: float, end: float, out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    run_checked(
        [
            ffmpeg,
            "-y",
            "-v",
            "error",
            "-ss",
            f"{max(0.0, start):.6f}",
            "-to",
            f"{max(0.0, end):.6f}",
            "-i",
            str(media),
            "-map",
            "0:a:0",
            "-c:a",
            "pcm_s16le",
            str(out),
        ]
    )


def transcribe_if_available(audio: Path, out_json: Path) -> str:
    apple_stt = shutil.which("apple-stt")
    if not apple_stt:
        return "apple-stt not found; STT skipped"
    proc = subprocess.run(
        [apple_stt, "--json", "-q", "-o", str(out_json), str(audio)],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if proc.returncode != 0:
        return "apple-stt failed: " + (proc.stderr or proc.stdout).strip()[:300]
    return "ok"


def transcript_text(path: Path) -> str:
    if not path.exists():
        return ""
    try:
        rows = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return ""
    return " ".join(str(row.get("text", "")).strip() for row in rows if row.get("text"))


def write_review_md(
    path: Path,
    media: Path,
    marker_json: Path,
    speech_json: Path,
    plan_json: Path,
    predictions: list[dict[str, Any]],
    windows: list[dict[str, Any]],
) -> None:
    lines = [
        "# Video Cut Review",
        "",
        f"Source: `{media}`",
        f"Marker evidence: `{marker_json}`",
        f"Speech/VAD evidence: `{speech_json}`",
        f"Plan template: `{plan_json}`",
        "",
        "## Marker Candidates",
        "",
        "| # | time | score | window transcript |",
        "|---:|---:|---:|---|",
    ]
    for index, prediction in enumerate(predictions, 1):
        window = windows[index - 1] if index - 1 < len(windows) else {}
        text = str(window.get("transcript_text", "")).replace("|", "\\|")
        if len(text) > 180:
            text = text[:177] + "..."
        lines.append(
            f"| {index} | {prediction.get('timecode', format_time(float(prediction.get('time', 0))))} "
            f"| {float(prediction.get('accuracy_percent', 0)):.2f}% | {text} |"
        )
    if not predictions:
        lines.append("| - | - | - | no marker candidates |")

    lines += [
        "",
        "## Marker Decisions",
        "",
        "Use marker/VAD for timeline boundaries and STT only for semantic evidence.",
        "",
        "- `full_retake`: failed clause or sentence before marker is repeated after marker.",
        "- `local_correction`: only the failed word or short phrase before marker should be removed.",
        "- `cut_before_marker`: alias for `full_retake`; use only when the whole failed clause or sentence is repeated.",
        "- `cut_after_marker`: marker is followed by filler such as 다시 할게요 before the real retake.",
        "- `skip`: marker is accidental or no retake exists.",
        "- `needs_manual`: evidence is ambiguous; do not auto-render.",
        "",
        "For marker + silence work, review marker cuts first, then build the final mixed plan from the remaining speech timeline.",
        "",
        "After review, edit `remove_intervals` in the plan JSON and run render.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def analyze(args: argparse.Namespace) -> int:
    media = args.media.expanduser().resolve()
    if not media.exists():
        return fail(f"input not found: {media}")
    marker = args.marker.expanduser().resolve()
    if not marker.exists():
        return fail(f"marker not found: {marker}")
    workspace = (args.workspace or default_workspace(media)).expanduser().resolve()
    workspace.mkdir(parents=True, exist_ok=True)

    ffmpeg = require_tool("ffmpeg")
    marker_json = workspace / "markers.json"
    speech_json = workspace / "speech.json"
    plan_json = workspace / "cut-plan.json"
    review_md = workspace / "review.md"

    run_checked(
        [
            sys.executable,
            str(ROOT / "scripts" / "detect_cut_markers.py"),
            str(media),
            "--marker",
            str(marker),
            "--threshold",
            str(args.threshold),
            "--json",
            str(marker_json),
        ]
    )
    run_checked(
        [
            sys.executable,
            str(ROOT / "scripts" / "video_speech_cut.py"),
            str(media),
            str(workspace / "_speechcut-preview.mp4"),
            "--dry-run",
            "--padding",
            str(args.padding),
            "--merge-gap",
            str(args.merge_gap),
            "--vad-db",
            str(args.vad_db),
            "--json",
            str(speech_json),
        ]
    )

    marker_data = load_json(marker_json)
    predictions = marker_data.get("predictions", [])
    windows: list[dict[str, Any]] = []
    for index, prediction in enumerate(predictions, 1):
        t = float(prediction["time"])
        wav = workspace / "windows" / f"marker-{index:03d}-{format_time(t).replace(':', '-')}.wav"
        stt_json = wav.with_suffix(".stt.json")
        extract_window(ffmpeg, media, t - args.window, t + args.window, wav)
        stt_status = "skipped"
        if not args.no_stt:
            stt_status = transcribe_if_available(wav, stt_json)
        windows.append(
            {
                "marker_index": index,
                "marker_time": t,
                "window_start": max(0.0, t - args.window),
                "window_end": t + args.window,
                "audio_path": str(wav),
                "stt_json": str(stt_json) if stt_json.exists() else None,
                "stt_status": stt_status,
                "transcript_text": transcript_text(stt_json),
            }
        )

    plan = {
        "source": str(media),
        "output": str(media.with_name(f"{media.stem}.cut.mp4")),
        "status": "draft",
        "remove_intervals": [],
        "evidence": {"markers": str(marker_json), "speech": str(speech_json), "windows": windows},
        "render_notes": [
            "Review marker windows before adding remove_intervals.",
            "Use original source timeline seconds.",
            "Render once from the original timeline.",
        ],
    }
    write_json(plan_json, plan)
    write_review_md(review_md, media, marker_json, speech_json, plan_json, predictions, windows)

    print(f"workspace: {workspace}")
    print(f"markers: {len(predictions)}")
    print(f"review: {review_md}")
    print(f"plan: {plan_json}")
    return 0


def keep_segments(duration: float, removals: list[dict[str, Any]]) -> list[TimeRange]:
    kept: list[TimeRange] = []
    cursor = 0.0
    for item in sorted(removals, key=lambda x: float(x["start"])):
        start = max(0.0, min(duration, float(item["start"])))
        end = max(0.0, min(duration, float(item["end"])))
        if end <= start:
            raise ValueError(f"invalid removal interval: {item}")
        if start < cursor:
            raise ValueError(f"overlapping removal interval: {item}")
        if start > cursor + 0.001:
            kept.append(TimeRange(cursor, start))
        cursor = end
    if cursor < duration - 0.001:
        kept.append(TimeRange(cursor, duration))
    return kept


def reasons_for_gap(removals: list[dict[str, Any]], start: float, end: float) -> list[str]:
    reasons = []
    for item in removals:
        cut_start = float(item["start"])
        cut_end = float(item["end"])
        if cut_end <= start + 0.001 or cut_start >= end - 0.001:
            continue
        reason = str(item.get("reason", "cut")).strip() or "cut"
        reasons.append(reason)
    return reasons or ["cut"]


def build_join_map(
    plan_path: Path,
    source: Path,
    output: Path,
    duration: float,
    segments: list[TimeRange],
    removals: list[dict[str, Any]],
) -> dict[str, Any]:
    joins: list[dict[str, Any]] = []
    output_time = 0.0
    for index, (left, right) in enumerate(zip(segments, segments[1:]), 1):
        output_time += left.end - left.start
        gap_start = left.end
        gap_end = right.start
        joins.append(
            {
                "index": index,
                "type": "edit_join",
                "output_time": round(output_time, 6),
                "left_source_end": round(gap_start, 6),
                "right_source_start": round(gap_end, 6),
                "removed_duration": round(gap_end - gap_start, 6),
                "reasons": reasons_for_gap(removals, gap_start, gap_end),
            }
        )
    return {
        "schema": "video-cut-editor.join-map.v1",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "source": str(source),
        "output": str(output),
        "plan": str(plan_path),
        "source_duration": round(duration, 6),
        "joins": joins,
    }


def run_self_test() -> int:
    removals = [
        {"start": 2.0, "end": 3.0, "reason": "silence"},
        {"start": 5.0, "end": 8.0, "reason": "full_retake"},
    ]
    segments = keep_segments(10.0, removals)
    assert [(item.start, item.end) for item in segments] == [(0.0, 2.0), (3.0, 5.0), (8.0, 10.0)]
    join_map = build_join_map(Path("plan.json"), Path("in.mp4"), Path("out.mp4"), 10.0, segments, removals)
    assert [item["output_time"] for item in join_map["joins"]] == [2.0, 4.0]
    assert join_map["joins"][1]["removed_duration"] == 3.0
    print("self_test: ok")
    return 0


def render(args: argparse.Namespace) -> int:
    plan_path = args.plan.expanduser().resolve()
    plan = load_json(plan_path)
    source = Path(plan["source"]).expanduser().resolve()
    output = Path(args.output).expanduser().resolve() if args.output else Path(plan["output"]).expanduser().resolve()
    removals = plan.get("remove_intervals", [])
    if not removals:
        return fail("plan has no remove_intervals; review and fill the plan before render")
    if plan.get("status") != "reviewed" and not args.allow_draft:
        return fail("plan status must be reviewed before render; set status to reviewed or pass --allow-draft")
    if not source.exists():
        return fail(f"source not found: {source}")
    if output.exists() and not args.overwrite:
        return fail(f"output exists, pass --overwrite: {output}")

    ffmpeg = require_tool("ffmpeg")
    ffprobe = require_tool("ffprobe")
    media = ffprobe_json(ffprobe, source)
    video_streams = streams(media, "video")
    audio_streams = streams(media, "audio")
    if not video_streams:
        return fail("no video stream found")
    if not audio_streams:
        return fail("no audio stream found")
    duration = parse_duration(media)
    segments = keep_segments(duration, removals)
    plan_encode = choose_encoder(video_streams[0], args.video_encoder, ffmpeg_encoders(ffmpeg))
    video_opts = video_output_options(video_streams[0], plan_encode, output, args.video_bitrate)
    audio_opts, audio_warnings = audio_output_options(audio_streams)

    output.parent.mkdir(parents=True, exist_ok=True)
    artifact_dir = default_artifact_dir(output)
    default_log_file = artifact_dir / f"{output.stem}.render.log"
    default_join_map = artifact_dir / f"{output.stem}.join-map.json"
    log_file = None if args.dry_run else (args.log_file or default_log_file).expanduser().resolve()
    join_map_path = None if args.dry_run else (args.join_map or default_join_map).expanduser().resolve()
    graph = build_filter_graph(segments, len(audio_streams))
    with tempfile.NamedTemporaryFile("w", suffix=".ffgraph", delete=False, encoding="utf-8") as handle:
        handle.write(graph)
        graph_path = Path(handle.name)
    try:
        cmd = build_ffmpeg_command(
            ffmpeg,
            source,
            output,
            graph_path,
            len(audio_streams),
            video_opts,
            audio_opts,
            True,
        )
        if args.dry_run:
            print("ffmpeg command:", shlex.join(cmd))
            print(f"kept_segments: {len(segments)}")
            print(f"joins: {max(0, len(segments) - 1)}")
            print(f"removed: {sum(float(i['end']) - float(i['start']) for i in removals):.3f}s")
            print(f"artifacts: {artifact_dir}")
            return 0
        print(f"log: {log_file}")
        result = run_with_log(cmd, log_file)
        if result.returncode != 0:
            print("ffmpeg command:", shlex.join(cmd), file=sys.stderr)
            if log_file is not None:
                print(f"log: {log_file}", file=sys.stderr)
            return fail((result.stderr or result.stdout).strip()[-4000:])
    finally:
        graph_path.unlink(missing_ok=True)

    for warning in plan_encode.warnings + audio_warnings:
        print(f"warning: {warning}")
    errors = verify_output(ffmpeg, ffprobe, media, output, plan_encode.expected_video_codec, len(audio_streams))
    if errors:
        for error in errors:
            print(f"verify_error: {error}", file=sys.stderr)
        return 1
    if join_map_path is not None:
        write_json(join_map_path, build_join_map(plan_path, source, output, duration, segments, removals))
    print(f"output: {output}")
    print(f"kept_segments: {len(segments)}")
    print(f"artifacts: {artifact_dir}")
    if join_map_path is not None:
        print(f"join_map: {join_map_path}")
    print("verify: ok")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Marker-based video cut editing workflow.")
    parser.add_argument("--self-test", action="store_true")
    sub = parser.add_subparsers(dest="command")

    analyze_parser = sub.add_parser("analyze", help="detect markers, speech regions, and review evidence")
    analyze_parser.add_argument("media", type=Path)
    analyze_parser.add_argument("--marker", type=Path, default=DEFAULT_MARKER)
    analyze_parser.add_argument("--workspace", type=Path)
    analyze_parser.add_argument("--threshold", type=float, default=0.90)
    analyze_parser.add_argument("--window", type=float, default=8.0)
    analyze_parser.add_argument("--padding", type=float, default=0.35)
    analyze_parser.add_argument("--merge-gap", type=float, default=0.85)
    analyze_parser.add_argument("--vad-db", type=float, default=-42.0)
    analyze_parser.add_argument("--no-stt", action="store_true")

    render_parser = sub.add_parser("render", help="render a reviewed cut-plan JSON")
    render_parser.add_argument("plan", type=Path)
    render_parser.add_argument("--output", type=Path)
    render_parser.add_argument("--overwrite", "-y", action="store_true")
    render_parser.add_argument("--dry-run", action="store_true")
    render_parser.add_argument("--allow-draft", action="store_true")
    render_parser.add_argument("--video-encoder", default="auto")
    render_parser.add_argument("--video-bitrate", default="auto")
    render_parser.add_argument("--log-file", type=Path)
    render_parser.add_argument("--join-map", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        if args.self_test:
            return run_self_test()
        if args.command == "analyze":
            return analyze(args)
        if args.command == "render":
            return render(args)
        if not args.command:
            return fail("command is required unless --self-test is used")
        return fail(f"unknown command: {args.command}")
    except Exception as exc:
        return fail(str(exc))


if __name__ == "__main__":
    raise SystemExit(main())
