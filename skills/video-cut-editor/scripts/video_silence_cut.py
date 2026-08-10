#!/usr/bin/env python3
"""Remove silence from a local video while preserving the source shape."""

from __future__ import annotations

import argparse
import json
import math
import platform
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any


NUMBER = r"[-+]?\d+(?:\.\d+)?(?:e[-+]?\d+)?"


@dataclass(frozen=True)
class TimeRange:
    start: float
    end: float

    @property
    def duration(self) -> float:
        return self.end - self.start


@dataclass(frozen=True)
class EncodePlan:
    encoder: str
    expected_video_codec: str
    warnings: list[str]


def run(argv: list[str], *, capture: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        argv,
        check=False,
        text=True,
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.PIPE if capture else None,
    )


def fail(message: str, code: int = 1) -> int:
    print(f"error: {message}", file=sys.stderr)
    return code


def require_tool(name: str) -> str:
    path = shutil.which(name)
    if not path:
        raise RuntimeError(f"{name} not found in PATH")
    return path


def ffprobe_json(ffprobe: str, path: Path) -> dict[str, Any]:
    result = run(
        [
            ffprobe,
            "-v",
            "error",
            "-show_entries",
            (
                "format=duration,format_name,bit_rate:"
                "stream=index,codec_type,codec_name,codec_tag_string,width,height,"
                "r_frame_rate,avg_frame_rate,pix_fmt,color_range,color_space,"
                "color_transfer,color_primaries,sample_rate,channels,channel_layout,bit_rate"
            ),
            "-of",
            "json",
            str(path),
        ]
    )
    if result.returncode != 0:
        raise RuntimeError((result.stderr or result.stdout).strip())
    return json.loads(result.stdout)


def parse_duration(media: dict[str, Any]) -> float:
    duration = media.get("format", {}).get("duration")
    if not duration:
        raise RuntimeError("input duration not found")
    return float(duration)


def streams(media: dict[str, Any], codec_type: str) -> list[dict[str, Any]]:
    return [s for s in media.get("streams", []) if s.get("codec_type") == codec_type]


def ffmpeg_encoders(ffmpeg: str) -> set[str]:
    result = run([ffmpeg, "-hide_banner", "-encoders"])
    if result.returncode != 0:
        return set()
    names: set[str] = set()
    for line in result.stdout.splitlines():
        parts = line.split()
        if len(parts) >= 2 and parts[0].startswith("V"):
            names.add(parts[1])
    return names


def choose_encoder(video: dict[str, Any], requested: str, encoders: set[str]) -> EncodePlan:
    codec = video.get("codec_name", "")
    warnings: list[str] = []

    if requested != "auto":
        if requested in {"hevc", "h265", "libx265", "hevc_videotoolbox"}:
            return EncodePlan(requested, "hevc", warnings)
        if requested in {"h264", "libx264", "h264_videotoolbox"}:
            return EncodePlan(requested, "h264", warnings)
        warnings.append(f"custom video encoder {requested}; codec preservation cannot be verified")
        return EncodePlan(requested, codec or "unknown", warnings)

    if codec == "hevc":
        if "hevc_videotoolbox" in encoders and platform.system() == "Darwin":
            return EncodePlan("hevc_videotoolbox", "hevc", warnings)
        if "libx265" in encoders:
            return EncodePlan("libx265", "hevc", warnings)

    if codec == "h264":
        if "h264_videotoolbox" in encoders and platform.system() == "Darwin":
            return EncodePlan("h264_videotoolbox", "h264", warnings)
        if "libx264" in encoders:
            return EncodePlan("libx264", "h264", warnings)

    if "libx264" in encoders:
        warnings.append(f"video codec {codec or 'unknown'} is not handled; falling back to h264")
        return EncodePlan("libx264", "h264", warnings)

    raise RuntimeError("no supported video encoder found")


def parse_rate(value: str | None) -> str | None:
    if not value or value in {"0/0", "N/A"}:
        return None
    return value


def bitrate_k(stream: dict[str, Any], multiplier: float = 1.25) -> str | None:
    raw = stream.get("bit_rate")
    if not raw:
        return None
    try:
        return f"{max(1, math.ceil(int(raw) * multiplier / 1000))}k"
    except ValueError:
        return None


def detect_silences(
    ffmpeg: str,
    input_file: Path,
    audio_index: int,
    limit: float,
    silence_db: str,
    min_duration: float,
) -> list[TimeRange]:
    cmd = [
        ffmpeg,
        "-hide_banner",
        "-nostats",
        "-i",
        str(input_file),
        "-t",
        f"{limit:.6f}",
        "-map",
        f"0:a:{audio_index}",
        "-af",
        f"silencedetect=noise={silence_db}:d={min_duration}",
        "-f",
        "null",
        "-",
    ]
    result = run(cmd)
    if result.returncode != 0:
        raise RuntimeError((result.stderr or result.stdout).strip())

    start_re = re.compile(rf"silence_start:\s*({NUMBER})")
    end_re = re.compile(rf"silence_end:\s*({NUMBER}).*silence_duration:\s*({NUMBER})")

    silences: list[TimeRange] = []
    current_start: float | None = None
    for line in result.stderr.splitlines():
        start_match = start_re.search(line)
        if start_match:
            current_start = float(start_match.group(1))
            continue

        end_match = end_re.search(line)
        if end_match and current_start is not None:
            end = min(float(end_match.group(1)), limit)
            if end > current_start:
                silences.append(TimeRange(current_start, end))
            current_start = None

    if current_start is not None and current_start < limit:
        silences.append(TimeRange(current_start, limit))

    return silences


def keep_segments(duration: float, silences: list[TimeRange], padding: float) -> list[TimeRange]:
    kept: list[TimeRange] = []
    current = 0.0

    for silence in sorted(silences, key=lambda item: item.start):
        start = max(0.0, min(duration, silence.start))
        end = max(0.0, min(duration, silence.end))
        if end <= start:
            continue

        cut_start = 0.0 if start <= 0.001 else min(duration, start + padding)
        cut_end = duration if end >= duration - 0.001 else max(0.0, end - padding)
        if cut_end <= cut_start:
            continue

        if cut_start > current + 0.001:
            kept.append(TimeRange(current, cut_start))
        current = max(current, cut_end)

    if current < duration - 0.001:
        kept.append(TimeRange(current, duration))

    return [segment for segment in kept if segment.duration > 0.001]


def clamp_silences(silences: list[TimeRange], duration: float) -> list[TimeRange]:
    clipped: list[TimeRange] = []
    for silence in silences:
        start = max(0.0, min(duration, silence.start))
        end = max(0.0, min(duration, silence.end))
        if end > start:
            clipped.append(TimeRange(start, end))
    return clipped


def build_filter_graph(segments: list[TimeRange], audio_count: int) -> str:
    lines: list[str] = []
    concat_inputs: list[str] = []

    for segment_index, segment in enumerate(segments):
        start = f"{segment.start:.6f}"
        end = f"{segment.end:.6f}"
        v_label = f"v{segment_index}"
        lines.append(
            f"[0:v:0]trim=start={start}:end={end},setpts=PTS-STARTPTS[{v_label}]"
        )
        concat_inputs.append(f"[{v_label}]")

        for audio_index in range(audio_count):
            a_label = f"a{audio_index}_{segment_index}"
            lines.append(
                f"[0:a:{audio_index}]atrim=start={start}:end={end},"
                f"asetpts=PTS-STARTPTS[{a_label}]"
            )
            concat_inputs.append(f"[{a_label}]")

    outputs = "[v]" + "".join(f"[a{i}]" for i in range(audio_count))
    lines.append(
        "".join(concat_inputs)
        + f"concat=n={len(segments)}:v=1:a={audio_count}{outputs}"
    )
    return ";\n".join(lines)


def video_output_options(
    video: dict[str, Any],
    plan: EncodePlan,
    output_file: Path,
    requested_bitrate: str,
) -> list[str]:
    opts = ["-c:v", plan.encoder]

    if plan.expected_video_codec == "hevc" and output_file.suffix.lower() in {".mp4", ".m4v", ".mov"}:
        opts += ["-tag:v", "hvc1"]

    if requested_bitrate != "none":
        if requested_bitrate == "auto":
            bit_rate = bitrate_k(video) or "12000k"
        else:
            bit_rate = requested_bitrate
        opts += ["-b:v", bit_rate]

    fps = parse_rate(video.get("avg_frame_rate"))
    if fps and fps == parse_rate(video.get("r_frame_rate")):
        opts += ["-r", fps]

    pix_fmt = video.get("pix_fmt")
    if pix_fmt and pix_fmt != "unknown":
        opts += ["-pix_fmt", pix_fmt]

    color_map = {
        "color_range": "-color_range",
        "color_space": "-colorspace",
        "color_transfer": "-color_trc",
        "color_primaries": "-color_primaries",
    }
    for key, option in color_map.items():
        value = video.get(key)
        if value and value != "unknown":
            opts += [option, value]

    return opts


def audio_output_options(
    audio_streams: list[dict[str, Any]],
    requested_bitrate: str = "auto",
) -> tuple[list[str], list[str]]:
    opts: list[str] = []
    warnings: list[str] = []

    for index, stream in enumerate(audio_streams):
        codec = stream.get("codec_name")
        if codec == "aac":
            encoder = "aac"
        elif codec == "mp3":
            encoder = "libmp3lame"
        else:
            encoder = "aac"
            warnings.append(f"audio stream {index} codec {codec or 'unknown'} re-encoded as aac")

        opts += [f"-c:a:{index}", encoder]

        if requested_bitrate == "auto":
            bit_rate = bitrate_k(stream, multiplier=1.0)
        elif requested_bitrate == "none":
            bit_rate = None
        else:
            bit_rate = requested_bitrate
        if bit_rate and encoder in {"aac", "libmp3lame"}:
            opts += [f"-b:a:{index}", bit_rate]

        sample_rate = stream.get("sample_rate")
        if sample_rate:
            opts += [f"-ar:a:{index}", str(sample_rate)]

        channels = stream.get("channels")
        if channels:
            opts += [f"-ac:a:{index}", str(channels)]

    return opts, warnings


def build_ffmpeg_command(
    ffmpeg: str,
    input_file: Path,
    output_file: Path,
    filter_script: Path,
    audio_count: int,
    video_opts: list[str],
    audio_opts: list[str],
    overwrite: bool,
) -> list[str]:
    cmd = [ffmpeg, "-hide_banner", "-nostdin"]
    cmd.append("-y" if overwrite else "-n")
    cmd += ["-i", str(input_file), "-filter_complex_script", str(filter_script), "-map", "[v]"]
    for index in range(audio_count):
        cmd += ["-map", f"[a{index}]"]
    cmd += video_opts
    cmd += audio_opts
    cmd += ["-map_metadata", "0", "-movflags", "+faststart", str(output_file)]
    return cmd


def default_output(input_file: Path, test_duration: float | None) -> Path:
    suffix = input_file.suffix or ".mp4"
    marker = f".sample-{int(test_duration)}s.silencecut" if test_duration else ".silencecut"
    return input_file.with_name(f"{input_file.stem}{marker}{suffix}")


def summarize(
    input_file: Path,
    output_file: Path,
    duration: float,
    silences: list[TimeRange],
    segments: list[TimeRange],
    plan: EncodePlan,
    audio_count: int,
    dry_run: bool,
) -> None:
    removed = duration - sum(segment.duration for segment in segments)
    print(f"input: {input_file}")
    print(f"output: {output_file}")
    print(f"duration: {duration:.3f}s")
    print(f"silences: {len(silences)}")
    print(f"kept_segments: {len(segments)}")
    print(f"estimated_output: {sum(segment.duration for segment in segments):.3f}s")
    print(f"estimated_removed: {removed:.3f}s")
    print(f"video_encoder: {plan.encoder}")
    print(f"expected_video_codec: {plan.expected_video_codec}")
    print(f"audio_tracks: {audio_count}")
    if silences:
        print("first_silences:")
        for silence in silences[:8]:
            print(f"  {silence.start:.3f}-{silence.end:.3f} ({silence.duration:.3f}s)")
    for warning in plan.warnings:
        print(f"warning: {warning}")
    if dry_run:
        print("dry_run: no file written")


def verify_output(
    ffmpeg: str,
    ffprobe: str,
    input_media: dict[str, Any],
    output_file: Path,
    expected_video_codec: str,
    expected_audio_count: int,
) -> list[str]:
    output_media = ffprobe_json(ffprobe, output_file)
    input_video = streams(input_media, "video")[0]
    output_video = streams(output_media, "video")[0]
    output_audio = streams(output_media, "audio")

    errors: list[str] = []
    for key in ("width", "height"):
        if input_video.get(key) != output_video.get(key):
            errors.append(f"video {key} changed: {input_video.get(key)} -> {output_video.get(key)}")

    if output_video.get("codec_name") != expected_video_codec:
        errors.append(
            "video codec mismatch: "
            f"expected {expected_video_codec}, got {output_video.get('codec_name')}"
        )

    if len(output_audio) != expected_audio_count:
        errors.append(f"audio track count changed: {expected_audio_count} -> {len(output_audio)}")

    decode = run([ffmpeg, "-v", "error", "-i", str(output_file), "-f", "null", "-"])
    if decode.returncode != 0 or (decode.stderr or "").strip():
        errors.append("decode check failed: " + (decode.stderr or decode.stdout or "").strip()[:1000])

    return errors


def run_self_test() -> int:
    silences = [
        TimeRange(0.0, 3.656),
        TimeRange(16.059, 26.853),
        TimeRange(28.460, 30.236),
    ]
    segments = keep_segments(60.0, silences, 0.15)
    expected = [
        TimeRange(3.506, 16.209),
        TimeRange(26.703, 28.610),
        TimeRange(30.086, 60.0),
    ]
    assert len(segments) == len(expected), segments
    for actual, want in zip(segments, expected):
        assert abs(actual.start - want.start) < 0.001, (actual, want)
        assert abs(actual.end - want.end) < 0.001, (actual, want)
    graph = build_filter_graph(segments[:2], 2)
    assert "concat=n=2:v=1:a=2[v][a0][a1]" in graph
    audio = [
        {"codec_name": "aac", "bit_rate": "128000", "sample_rate": "48000", "channels": 2}
    ]
    fixed_audio_opts, _ = audio_output_options(audio, "160k")
    assert fixed_audio_opts[fixed_audio_opts.index("-b:a:0") + 1] == "160k"
    print("self_test: ok")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Remove detected silence from a local video and preserve stream shape."
    )
    parser.add_argument("input_file", nargs="?", type=Path)
    parser.add_argument("output_file", nargs="?", type=Path)
    parser.add_argument("--silence-db", default="-35dB")
    parser.add_argument("--min-duration", type=float, default=0.8)
    parser.add_argument("--padding", type=float, default=0.15)
    parser.add_argument("--detect-audio", type=int, default=0)
    parser.add_argument("--test-duration", type=float)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--overwrite", "-y", action="store_true")
    parser.add_argument("--open", action="store_true")
    parser.add_argument("--video-encoder", default="auto")
    parser.add_argument("--video-bitrate", default="auto", help="auto, none, or a value like 16000k")
    parser.add_argument("--self-test", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.self_test:
        return run_self_test()

    if not args.input_file:
        return fail("input_file is required")
    input_file = args.input_file.expanduser().resolve()
    if not input_file.exists():
        return fail(f"input not found: {input_file}")

    output_file = (args.output_file or default_output(input_file, args.test_duration)).expanduser().resolve()
    if input_file == output_file:
        return fail("input and output must be different")
    if output_file.exists() and not args.dry_run and not args.overwrite:
        return fail(f"output exists, pass --overwrite: {output_file}")

    if args.padding < 0:
        return fail("--padding must be >= 0")
    if args.min_duration <= 0:
        return fail("--min-duration must be > 0")

    try:
        ffmpeg = require_tool("ffmpeg")
        ffprobe = require_tool("ffprobe")
        media = ffprobe_json(ffprobe, input_file)
        video_streams = streams(media, "video")
        audio_streams = streams(media, "audio")
        if not video_streams:
            return fail("no video stream found")
        if not audio_streams:
            return fail("no audio stream found")
        if args.detect_audio < 0 or args.detect_audio >= len(audio_streams):
            return fail(f"--detect-audio must be between 0 and {len(audio_streams) - 1}")

        source_duration = parse_duration(media)
        duration = min(source_duration, args.test_duration) if args.test_duration else source_duration
        if duration <= 0:
            return fail("duration is zero")
        # ponytail: scan a little past sample end so a silence that starts at
        # 59.3s in a 60s test still gets detected if it continues after 60s.
        scan_duration = (
            min(source_duration, duration + args.min_duration + args.padding)
            if args.test_duration
            else duration
        )

        detected_silences = detect_silences(
            ffmpeg,
            input_file,
            args.detect_audio,
            scan_duration,
            args.silence_db,
            args.min_duration,
        )
        silences = clamp_silences(detected_silences, duration)
        segments = keep_segments(duration, silences, args.padding)
        if not segments:
            return fail("all content would be removed; increase padding or lower the silence threshold")

        plan = choose_encoder(video_streams[0], args.video_encoder, ffmpeg_encoders(ffmpeg))
        summarize(
            input_file,
            output_file,
            duration,
            silences,
            segments,
            plan,
            len(audio_streams),
            args.dry_run,
        )
        if args.dry_run:
            return 0

        output_file.parent.mkdir(parents=True, exist_ok=True)
        graph = build_filter_graph(segments, len(audio_streams))
        video_opts = video_output_options(video_streams[0], plan, output_file, args.video_bitrate)
        audio_opts, audio_warnings = audio_output_options(audio_streams)
        for warning in audio_warnings:
            print(f"warning: {warning}")

        with tempfile.NamedTemporaryFile("w", suffix=".ffgraph", delete=False, encoding="utf-8") as handle:
            handle.write(graph)
            graph_path = Path(handle.name)
        try:
            cmd = build_ffmpeg_command(
                ffmpeg,
                input_file,
                output_file,
                graph_path,
                len(audio_streams),
                video_opts,
                audio_opts,
                args.overwrite,
            )
            result = run(cmd)
            if result.returncode != 0:
                print("ffmpeg command:", shlex.join(cmd), file=sys.stderr)
                return fail((result.stderr or result.stdout).strip()[-4000:])
        finally:
            graph_path.unlink(missing_ok=True)

        errors = verify_output(
            ffmpeg,
            ffprobe,
            media,
            output_file,
            plan.expected_video_codec,
            len(audio_streams),
        )
        if errors:
            for error in errors:
                print(f"verify_error: {error}", file=sys.stderr)
            return 1

        print("verify: ok")
        if args.open:
            if platform.system() == "Darwin":
                subprocess.run(["open", str(output_file)], check=False)
            else:
                print("--open is only implemented for macOS")
        return 0

    except Exception as exc:
        return fail(str(exc))


if __name__ == "__main__":
    raise SystemExit(main())
