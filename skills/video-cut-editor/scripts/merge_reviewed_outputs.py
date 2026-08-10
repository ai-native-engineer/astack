#!/usr/bin/env python3
"""Merge reviewed edited outputs and verify the final file."""

from __future__ import annotations

import argparse
import json
import shlex
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any

from video_silence_cut import (
    audio_output_options,
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

MIN_AUDIO_BITRATE_RATIO = 0.5


def fail(message: str, code: int = 1) -> int:
    print(f"error: {message}", file=sys.stderr)
    return code


def run_with_log(argv: list[str], log_path: Path) -> subprocess.CompletedProcess[str]:
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
    return subprocess.CompletedProcess(argv, code, stdout="", stderr=tail.decode(errors="replace"))


def video_shape(stream: dict[str, Any]) -> tuple[Any, ...]:
    return (
        stream.get("codec_name"),
        stream.get("codec_tag_string"),
        stream.get("width"),
        stream.get("height"),
        stream.get("avg_frame_rate"),
        stream.get("pix_fmt"),
        stream.get("color_range"),
        stream.get("color_space"),
        stream.get("color_transfer"),
        stream.get("color_primaries"),
    )


def audio_shape(audio_streams: list[dict[str, Any]]) -> tuple[tuple[Any, ...], ...]:
    return tuple(
        (
            stream.get("codec_name"),
            stream.get("sample_rate"),
            stream.get("channels"),
            stream.get("channel_layout"),
        )
        for stream in audio_streams
    )


def stream_bitrate(stream: dict[str, Any]) -> int | None:
    try:
        return int(stream["bit_rate"])
    except (KeyError, TypeError, ValueError):
        return None


def representative_audio_streams(medias: list[dict[str, Any]]) -> list[dict[str, Any]]:
    audio_sets = [streams(media, "audio") for media in medias]
    if not audio_sets:
        return []
    track_count = len(audio_sets[0])
    if any(len(items) != track_count for items in audio_sets):
        raise ValueError("audio track count differs across inputs")
    return [
        max((items[index] for items in audio_sets), key=lambda item: stream_bitrate(item) or 0)
        for index in range(track_count)
    ]


def duration_weighted_audio_bitrates(
    medias: list[dict[str, Any]],
    durations: list[float],
) -> list[int | None]:
    audio_sets = [streams(media, "audio") for media in medias]
    if not audio_sets:
        return []
    track_count = len(audio_sets[0])
    if any(len(items) != track_count for items in audio_sets):
        raise ValueError("audio track count differs across inputs")

    expected: list[int | None] = []
    for index in range(track_count):
        weighted_sum = 0.0
        known_duration = 0.0
        for items, duration in zip(audio_sets, durations):
            bit_rate = stream_bitrate(items[index])
            if bit_rate is None:
                continue
            weighted_sum += bit_rate * duration
            known_duration += duration
        expected.append(round(weighted_sum / known_duration) if known_duration else None)
    return expected


def audio_bitrate_errors(
    reference_bitrates: list[int | None],
    output_streams: list[dict[str, Any]],
) -> list[str]:
    errors: list[str] = []
    for index, (reference_rate, output) in enumerate(zip(reference_bitrates, output_streams)):
        output_rate = stream_bitrate(output)
        if reference_rate and output_rate and output_rate < reference_rate * MIN_AUDIO_BITRATE_RATIO:
            errors.append(
                f"audio stream {index} bitrate collapsed: input weighted estimate {reference_rate} b/s, "
                f"output {output_rate} b/s; pass --audio-bitrate or inspect the merge inputs"
            )
    return errors


def stream_shape(media: dict[str, Any]) -> tuple[Any, ...]:
    videos = streams(media, "video")
    audios = streams(media, "audio")
    if not videos:
        raise ValueError("input has no video stream")
    if not audios:
        raise ValueError("input has no audio stream")
    return (video_shape(videos[0]), audio_shape(audios))


def reencode_compatible(medias: list[dict[str, Any]]) -> bool:
    first_video = streams(medias[0], "video")[0]
    first_audio = streams(medias[0], "audio")
    for media in medias[1:]:
        video = streams(media, "video")[0]
        audio = streams(media, "audio")
        if (video.get("width"), video.get("height")) != (first_video.get("width"), first_video.get("height")):
            return False
        if len(audio) != len(first_audio):
            return False
        for left, right in zip(first_audio, audio):
            if (left.get("sample_rate"), left.get("channels")) != (right.get("sample_rate"), right.get("channels")):
                return False
    return True


def concat_list_file(inputs: list[Path]) -> Path:
    handle = tempfile.NamedTemporaryFile("w", suffix=".ffconcat", delete=False, encoding="utf-8")
    with handle:
        for path in inputs:
            escaped = str(path).replace("'", "'\\''")
            handle.write(f"file '{escaped}'\n")
    return Path(handle.name)


def concat_filter(audio_count: int, input_count: int) -> str:
    labels: list[str] = []
    lines: list[str] = []
    for input_index in range(input_count):
        v_label = f"v{input_index}"
        lines.append(f"[{input_index}:v:0]setpts=PTS-STARTPTS[{v_label}]")
        labels.append(f"[{v_label}]")
        for audio_index in range(audio_count):
            a_label = f"a{audio_index}_{input_index}"
            lines.append(f"[{input_index}:a:{audio_index}]asetpts=PTS-STARTPTS[{a_label}]")
            labels.append(f"[{a_label}]")
    outputs = "[v]" + "".join(f"[a{i}]" for i in range(audio_count))
    lines.append("".join(labels) + f"concat=n={input_count}:v=1:a={audio_count}{outputs}")
    return ";\n".join(lines)


def copy_command(ffmpeg: str, inputs: list[Path], output: Path, overwrite: bool) -> tuple[list[str], Path]:
    list_path = concat_list_file(inputs)
    cmd = [
        ffmpeg,
        "-hide_banner",
        "-nostdin",
        "-y" if overwrite else "-n",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(list_path),
        "-map",
        "0",
        "-c",
        "copy",
        "-map_metadata",
        "0",
        "-movflags",
        "+faststart",
        str(output),
    ]
    return cmd, list_path


def reencode_command(
    ffmpeg: str,
    inputs: list[Path],
    output: Path,
    medias: list[dict[str, Any]],
    overwrite: bool,
    video_encoder: str,
    video_bitrate: str,
    audio_bitrate: str,
) -> list[str]:
    first_media = medias[0]
    video_stream = streams(first_media, "video")[0]
    audio_streams = representative_audio_streams(medias)
    plan = choose_encoder(video_stream, video_encoder, ffmpeg_encoders(ffmpeg))
    audio_opts, audio_warnings = audio_output_options(audio_streams, audio_bitrate)
    for warning in plan.warnings + audio_warnings:
        print(f"warning: {warning}")

    cmd = [ffmpeg, "-hide_banner", "-nostdin", "-y" if overwrite else "-n"]
    for path in inputs:
        cmd += ["-i", str(path)]
    cmd += ["-filter_complex", concat_filter(len(audio_streams), len(inputs)), "-map", "[v]"]
    for index in range(len(audio_streams)):
        cmd += ["-map", f"[a{index}]"]
    cmd += video_output_options(video_stream, plan, output, video_bitrate)
    cmd += audio_opts
    cmd += ["-map_metadata", "0", "-movflags", "+faststart", str(output)]
    return cmd


def verify_merged(
    ffmpeg: str,
    ffprobe: str,
    output: Path,
    first_media: dict[str, Any],
    expected_duration: float,
    expected_video_codec: str,
    expected_audio_count: int,
    reference_audio_bitrates: list[int | None] | None,
) -> tuple[list[str], float | None]:
    errors = verify_output(ffmpeg, ffprobe, first_media, output, expected_video_codec, expected_audio_count)
    if reference_audio_bitrates:
        output_audio = streams(ffprobe_json(ffprobe, output), "audio")
        errors.extend(audio_bitrate_errors(reference_audio_bitrates, output_audio))
    try:
        actual_duration = parse_duration(ffprobe_json(ffprobe, output))
    except Exception as exc:
        errors.append(f"duration check failed: {exc}")
        return errors, None
    tolerance = max(1.0, expected_duration * 0.005)
    if abs(actual_duration - expected_duration) > tolerance:
        errors.append(
            f"duration mismatch: expected about {expected_duration:.3f}s, got {actual_duration:.3f}s"
        )
    return errors, actual_duration


def input_summary(path: Path, media: dict[str, Any], duration: float) -> dict[str, Any]:
    video = streams(media, "video")[0]
    audio = streams(media, "audio")
    return {
        "path": str(path),
        "duration": duration,
        "video": (
            f"{video.get('codec_name', 'unknown')} "
            f"{video.get('width', '?')}x{video.get('height', '?')} "
            f"{video.get('avg_frame_rate', '?')}"
        ),
        "audio_tracks": len(audio),
        "audio": ", ".join(
            f"{item.get('codec_name', 'unknown')}/{item.get('sample_rate', '?')}Hz/{item.get('channels', '?')}ch"
            for item in audio
        ),
    }


def print_preflight(rows: list[dict[str, Any]], copy_ok: bool) -> None:
    print("preflight:")
    for index, row in enumerate(rows, 1):
        print(
            f"  {index}. {Path(row['path']).name} "
            f"{row['duration']:.3f}s video={row['video']} audio_tracks={row['audio_tracks']}"
        )
    print(f"  stream_copy_candidate: {'yes' if copy_ok else 'no'}")


def warning_summary(log_path: Path, limit: int = 12) -> list[str]:
    if not log_path.exists():
        return []
    needles = ("Non-monotonic", "warning", "Warning", "deprecated", "error", "Error")
    seen: set[str] = set()
    warnings: list[str] = []
    for line in log_path.read_text(errors="replace").splitlines():
        stripped = line.strip()
        if not stripped or not any(needle in stripped for needle in needles):
            continue
        if stripped in seen:
            continue
        seen.add(stripped)
        warnings.append(stripped)
        if len(warnings) >= limit:
            break
    return warnings


def json_count(path: Path | None) -> tuple[int | None, int | None]:
    if not path:
        return None, None
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        return None, None
    failed = 0
    for item in data:
        if not isinstance(item, dict):
            continue
        status = item.get("status", item.get("stt_status"))
        if status not in {None, "ok"}:
            failed += 1
    return len(data), failed


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def default_artifact_dir(output: Path) -> Path:
    return output.with_name(f"{output.stem}.video-cut-artifacts")


def default_join_map(path: Path) -> Path:
    return default_artifact_dir(path) / f"{path.stem}.join-map.json"


def load_input_joins(path: Path) -> list[dict[str, Any]]:
    join_map = default_join_map(path)
    if not join_map.exists():
        legacy_join_map = path.with_suffix(".join-map.json")
        if legacy_join_map.exists():
            join_map = legacy_join_map
    if not join_map.exists():
        return []
    data = json.loads(join_map.read_text(encoding="utf-8"))
    joins = data.get("joins", [])
    if not isinstance(joins, list):
        return []
    return [item for item in joins if isinstance(item, dict)]


def build_merge_join_map(output: Path, inputs: list[Path], durations: list[float], mode: str) -> dict[str, Any]:
    joins: list[dict[str, Any]] = []
    offset = 0.0
    next_index = 1
    for input_index, (path, duration) in enumerate(zip(inputs, durations), 1):
        for item in load_input_joins(path):
            copied = dict(item)
            copied["index"] = next_index
            copied["input_index"] = input_index
            copied["input"] = str(path)
            copied["output_time"] = round(offset + float(item["output_time"]), 6)
            joins.append(copied)
            next_index += 1
        offset += duration
        if input_index < len(inputs):
            joins.append(
                {
                    "index": next_index,
                    "type": "merge_join",
                    "output_time": round(offset, 6),
                    "left_input": str(path),
                    "right_input": str(inputs[input_index]),
                    "reasons": ["merge"],
                }
            )
            next_index += 1
    return {
        "schema": "video-cut-editor.join-map.v1",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "output": str(output),
        "merge_mode": mode,
        "inputs": [str(path) for path in inputs],
        "joins": joins,
    }


def write_qa_report(
    path: Path,
    output: Path,
    rows: list[dict[str, Any]],
    mode: str,
    expected_duration: float,
    actual_duration: float | None,
    warnings: list[str],
    requested_audio_bitrate: str,
    output_audio_bitrates: list[str],
    spot_check_summary: Path | None,
    merged_spot_check: Path | None,
    join_map: Path | None,
) -> None:
    marker_count, marker_failed = json_count(spot_check_summary)
    merged_count, merged_failed = json_count(merged_spot_check)
    lines = [
        "# Video Cut QA Report",
        "",
        f"Output: `{output}`",
        f"Merge mode: `{mode}`",
        f"Requested audio bitrate: `{requested_audio_bitrate}`",
        f"Output audio bitrates: `{', '.join(output_audio_bitrates)}`",
        f"Expected duration: `{expected_duration:.3f}s`",
        f"Actual duration: `{actual_duration:.3f}s`" if actual_duration is not None else "Actual duration: `unknown`",
        f"Join map: `{join_map}`" if join_map is not None else "Join map: `not written`",
        "Decode verify: `ok`",
        "",
        "## Inputs",
        "",
        "| # | file | duration | video | audio tracks |",
        "|---:|---|---:|---|---:|",
    ]
    for index, row in enumerate(rows, 1):
        lines.append(
            f"| {index} | `{Path(row['path']).name}` | {row['duration']:.3f}s | "
            f"{row['video']} | {row['audio_tracks']} |"
        )
    lines += [
        "",
        "## Spot Checks",
        "",
        f"- Marker-risk joins: `{marker_count}` checked, `{marker_failed}` failed"
        if marker_count is not None
        else "- Marker-risk joins: `not provided`",
        f"- Merged head/tail: `{merged_count}` checked, `{merged_failed}` failed"
        if merged_count is not None
        else "- Merged head/tail: `not provided`",
        "",
        "## Merge Warnings",
        "",
    ]
    if warnings:
        lines.extend(f"- `{line}`" for line in warnings)
    else:
        lines.append("- `none`")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_self_test() -> int:
    one = {
        "streams": [
            {"codec_type": "video", "codec_name": "hevc", "width": 1920, "height": 1080},
            {
                "codec_type": "audio",
                "codec_name": "aac",
                "sample_rate": "48000",
                "channels": 2,
                "bit_rate": "2000",
            },
        ]
    }
    two = json.loads(json.dumps(one))
    assert stream_shape(one) == stream_shape(two)
    two["streams"][0]["codec_name"] = "h264"
    assert stream_shape(one) != stream_shape(two)
    assert reencode_compatible([one, two])
    two["streams"][1]["bit_rate"] = "128000"
    selected_audio = representative_audio_streams([one, two])
    assert selected_audio[0]["bit_rate"] == "128000"
    weighted_audio = duration_weighted_audio_bitrates([one, two], [1.0, 1.0])
    assert weighted_audio == [65000]
    assert audio_bitrate_errors(weighted_audio, [{"bit_rate": "17000"}])
    assert not audio_bitrate_errors(weighted_audio, [{"bit_rate": "64000"}])
    assert "concat=n=2:v=1:a=1[v][a0]" in concat_filter(1, 2)
    rows = [input_summary(Path("a.mp4"), one, 1.0)]
    assert rows[0]["audio_tracks"] == 1
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        merge_map = build_merge_join_map(root / "out.mp4", [root / "a.mp4", root / "b.mp4"], [1.5, 2.0], "copy")
        assert merge_map["joins"][0]["type"] == "merge_join"
        assert merge_map["joins"][0]["output_time"] == 1.5
    print("self_test: ok")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Merge reviewed edited outputs and verify the final file.")
    parser.add_argument("inputs", nargs="*", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--log-file", type=Path)
    parser.add_argument("--overwrite", "-y", action="store_true")
    parser.add_argument("--force-reencode", action="store_true")
    parser.add_argument("--video-encoder", default="auto")
    parser.add_argument("--video-bitrate", default="auto")
    parser.add_argument(
        "--audio-bitrate",
        default="auto",
        help="FFmpeg audio bitrate for every track; auto uses the highest input bitrate per track",
    )
    parser.add_argument("--qa-report", type=Path)
    parser.add_argument("--spot-check-summary", type=Path)
    parser.add_argument("--merged-spot-check", type=Path)
    parser.add_argument("--join-map", type=Path)
    parser.add_argument("--self-test", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.self_test:
        return run_self_test()
    if not args.output:
        return fail("--output is required")
    inputs = [path.expanduser().resolve() for path in args.inputs]
    if len(inputs) < 2:
        return fail("at least two input files are required")
    missing = [str(path) for path in inputs if not path.exists()]
    if missing:
        return fail("input not found: " + ", ".join(missing))

    output = args.output.expanduser().resolve()
    if output.exists() and not args.overwrite:
        return fail(f"output exists, pass --overwrite: {output}")
    artifact_dir = default_artifact_dir(output)
    log_path = (args.log_file or artifact_dir / f"{output.stem}.merge.log").expanduser().resolve()
    join_map_path = (args.join_map or artifact_dir / f"{output.stem}.join-map.json").expanduser().resolve()

    try:
        ffmpeg = require_tool("ffmpeg")
        ffprobe = require_tool("ffprobe")
        medias = [ffprobe_json(ffprobe, path) for path in inputs]
        durations = [parse_duration(media) for media in medias]
        shapes = [stream_shape(media) for media in medias]
        copy_ok = len(set(shapes)) == 1 and not args.force_reencode
        rows = [input_summary(path, media, duration) for path, media, duration in zip(inputs, medias, durations)]
        print_preflight(rows, copy_ok)

        temp_path: Path | None = None
        reference_audio_bitrates: list[int | None] | None = None
        mode = "copy" if copy_ok else "reencode"
        if copy_ok:
            cmd, temp_path = copy_command(ffmpeg, inputs, output, args.overwrite)
            expected_codec = streams(medias[0], "video")[0].get("codec_name", "unknown")
        else:
            if not reencode_compatible(medias):
                return fail("stream shapes differ beyond re-encode fallback; normalize files before merge")
            cmd = reencode_command(
                ffmpeg,
                inputs,
                output,
                medias,
                args.overwrite,
                args.video_encoder,
                args.video_bitrate,
                args.audio_bitrate,
            )
            if args.audio_bitrate == "auto":
                reference_audio_bitrates = duration_weighted_audio_bitrates(medias, durations)
            expected_codec = choose_encoder(
                streams(medias[0], "video")[0],
                args.video_encoder,
                ffmpeg_encoders(ffmpeg),
            ).expected_video_codec

        try:
            print(f"log: {log_path}")
            result = run_with_log(cmd, log_path)
        finally:
            if temp_path is not None:
                temp_path.unlink(missing_ok=True)
        if result.returncode != 0:
            print("ffmpeg command:", shlex.join(cmd), file=sys.stderr)
            print(f"log: {log_path}", file=sys.stderr)
            return fail((result.stderr or result.stdout).strip()[-4000:])

        errors, actual_duration = verify_merged(
            ffmpeg,
            ffprobe,
            output,
            medias[0],
            sum(durations),
            expected_codec,
            len(streams(medias[0], "audio")),
            reference_audio_bitrates,
        )
        if errors:
            for error in errors:
                print(f"verify_error: {error}", file=sys.stderr)
            return 1
        warnings = warning_summary(log_path)
        output_audio_bitrates = [
            f"{stream_bitrate(item)} b/s" if stream_bitrate(item) is not None else "unknown"
            for item in streams(ffprobe_json(ffprobe, output), "audio")
        ]
        write_json(join_map_path, build_merge_join_map(output, inputs, durations, mode))
        qa_report = (args.qa_report or artifact_dir / f"{output.stem}.qa-report.md").expanduser().resolve()
        write_qa_report(
            qa_report,
            output,
            rows,
            mode,
            sum(durations),
            actual_duration,
            warnings,
            args.audio_bitrate if mode == "reencode" else "stream-copy",
            output_audio_bitrates,
            args.spot_check_summary.expanduser().resolve() if args.spot_check_summary else None,
            args.merged_spot_check.expanduser().resolve() if args.merged_spot_check else None,
            join_map_path,
        )

        print(f"mode: {mode}")
        print(f"output: {output}")
        print(f"inputs: {len(inputs)}")
        print(f"duration: {sum(durations):.3f}s")
        print(f"artifacts: {artifact_dir}")
        print(f"join_map: {join_map_path}")
        print(f"qa_report: {qa_report}")
        print(f"warnings: {len(warnings)}")
        print(f"output_audio_bitrates: {', '.join(output_audio_bitrates)}")
        print("verify: ok")
        return 0
    except Exception as exc:
        return fail(str(exc))


if __name__ == "__main__":
    raise SystemExit(main())
