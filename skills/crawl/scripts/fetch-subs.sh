#!/bin/bash
# Fetch one caption track and retain its SRT, yt-dlp metadata, and captions JSON.
# Usage: fetch-subs.sh URL [output_dir]
# Env: YT_SUB_CLIENTS; YT_COOKIES_FROM_BROWSER (default chrome, empty disables).
# stdout: VIDEO_ID, TITLE, SUB_LANG, KIND, CLIENT, SRT_PATH, CAPTIONS_PATH,
#         METADATA_PATH as key=value lines. TITLE escapes backslashes/control
#         characters; the exact title is in metadata JSON. Never eval stdout.
# output_dir owns unique .captions-attempt-* bundles. Consume emitted paths;
# successful files stay together there and are never replaced by later calls.
# exit: 0 success; 2 confirmed absence on every client; 3 acquisition failure.
# Python owns JSON/process handling so titles and metadata never become shell.
set -euo pipefail

if [ "${1:-}" = --help ] || [ "${1:-}" = -h ]; then
  printf 'Usage: %s URL [output_dir]\n' "$0"
  exit 0
fi
if [ "$#" -lt 1 ] || [ "$#" -gt 2 ] || [ -z "$1" ]; then
  printf 'Usage: %s URL [output_dir]\n' "$0" >&2
  exit 1
fi
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
# Co-location is the only dependency, including flattened crawl plugin copies.
exec python3 - "$SCRIPT_DIR" "$@" <<'PY'
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
sys.path.insert(0, sys.argv[1])
try:
    from captions import make_document, write_document
except ImportError:
    print("fetch-subs: captions.py must be alongside fetch-subs.sh", file=sys.stderr)
    sys.exit(3)

DEFAULT_CLIENTS = "default web_embedded web_safari mweb tv_embedded"
SAFE_COMPONENT = re.compile(r"[A-Za-z0-9_-]+\Z")
NETWORK_ERROR = re.compile(
    r"\b429\b|too many requests|HTTP(?: Error)?\s+[45][0-9]{2}\b|unable to download|failed to download|"
    r"time(?:d? out|out)|connection (?:reset|refused)|network(?: is)? unreachable|"
    r"temporary failure in name resolution|"
    r"certificate verify failed|sign in to confirm|not a bot|ERROR:|"
    r"PO Token.*(?:required|missing)|requires?.*PO Token",
    re.IGNORECASE,
)
INCOMPLETE_TRACKS = re.compile(
    r"(?:subtitles?|captions?).*(?:failed|error|missing|skipp|unavailable|not provided)|"
    r"(?:failed|unable).*(?:subtitles?|captions?|player response)|"
    r"PO Token.*(?:not provided|missing)",
    re.IGNORECASE,
)


def fail(message):
    print(f"fetch-subs: {message}", file=sys.stderr)


def decode_metadata(text):
    def reject_constant(value):
        raise ValueError("nonfinite metadata number")

    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("duplicate metadata key")
            result[key] = value
        return result

    metadata = json.loads(text, parse_constant=reject_constant, object_pairs_hook=unique)
    if not isinstance(metadata, dict) or metadata.get("_type", "video") != "video":
        raise ValueError("expected one video metadata object")
    video_id = metadata.get("id")
    if not isinstance(video_id, str) or not SAFE_COMPONENT.fullmatch(video_id):
        raise ValueError("missing or unsafe video ID")
    if not isinstance(metadata.get("title"), str):
        raise ValueError("missing video title")
    for name in ("subtitles", "automatic_captions"):
        tracks = metadata.get(name)
        if not isinstance(tracks, dict):
            raise ValueError("missing subtitle track maps")
        for language, formats in tracks.items():
            if language == "live_chat":
                continue
            if not SAFE_COMPONENT.fullmatch(language) or not isinstance(formats, list) or not formats:
                raise ValueError("invalid subtitle track")
            if any(not isinstance(track, dict) for track in formats):
                raise ValueError("invalid subtitle format")
            if not any(
                isinstance(track.get("ext"), str)
                and any(isinstance(track.get(key), str) and track[key] for key in ("url", "data"))
                for track in formats
            ):
                raise ValueError("subtitle track has no usable format")
    # Also reject numeric overflow (JSON 1e999 parses as infinity).
    json.dumps(metadata, allow_nan=False)
    return metadata


def select_track(metadata):
    manual, auto = metadata["subtitles"], metadata["automatic_captions"]
    for language in ("ko", "en"):
        if language in manual:
            return language, "manual"
    original = [language for language in auto if language.endswith("-orig")]
    native = metadata.get("language")
    if isinstance(native, str) and native in auto and native != "live_chat":
        original.append(native)
    for language in original + ["ko", "en"]:
        if language in auto:
            return language, "auto"
    return None


def run_ytdlp(client, arguments, url):
    command = ["yt-dlp", "--ignore-config", "--no-playlist", "--no-progress"]
    browser = os.environ.get("YT_COOKIES_FROM_BROWSER", "chrome")
    if browser:
        command.extend(["--cookies-from-browser", browser])
    if client != "default":
        command.extend(["--extractor-args", f"youtube:player_client={client}"])
    result = subprocess.run(command + arguments + ["--", url], capture_output=True, check=False)
    # Decode machine data strictly below; only non-persisted diagnostics may
    # replace undecodable bytes. A damaged title must never look successful.
    result.stderr = result.stderr.decode("utf-8", errors="replace")
    return result


def process_problem(result):
    # Do not echo yt-dlp's raw output: it can contain cookie locations/tokens.
    stderr = result.stderr
    if re.search(r"\b429\b|too many requests", stderr, re.IGNORECASE):
        return "HTTP 429 rate limit; wait before retrying rather than treating this as no captions"
    if re.search(r"ffmpeg|conversion|convert(?:ing)? subtitles", stderr, re.IGNORECASE):
        return "SRT conversion failed; install/check ffmpeg and retry (downloaded originals retained)"
    if re.search(
        r"authentication|sign in|not a bot|HTTP(?: Error)?\s+(?:401|403)\b|"
        r"(?:failed|unable|cannot|could not)\s+(?:to\s+)?(?:read|load|extract|decrypt)\b.*\bcookies?\b|"
        r"cookie access failed|permission denied|"
        r"PO Token.*(?:required|missing|not provided)|requires?.*PO Token",
        stderr, re.IGNORECASE,
    ):
        return "authentication failed; check configured browser access and yt-dlp client support"
    status = re.search(r"\bHTTP(?: Error)?\s+(408|500|502|503|504)\b", stderr, re.IGNORECASE)
    if status:
        return f"HTTP {status.group(1)} transient request failure; retry later"
    if re.search(r"time(?:d? out|out)", stderr, re.IGNORECASE):
        return "request timed out; retry later"
    if re.search(r"network(?: is)? unreachable", stderr, re.IGNORECASE):
        return "network is unreachable; retry later"
    for category in ("connection reset", "connection refused", "temporary failure in name resolution"):
        if category in stderr.lower():
            return f"{category}; retry later"
    if NETWORK_ERROR.search(stderr):
        return "network/track request failed; check connectivity and yt-dlp client support"
    return f"yt-dlp failed (exit {result.returncode}); check yt-dlp, connectivity, and configured browser access"


def save_metadata(path, metadata):
    text = json.dumps(metadata, ensure_ascii=False, allow_nan=False, indent=2) + "\n"
    with path.open("x", encoding="utf-8") as handle:
        handle.write(text)


def title_line(title):
    # Keep the line protocol unambiguous; JSON retains the unmodified title.
    text = json.dumps(title, ensure_ascii=False)[1:-1]
    for number in (0x85, 0x2028, 0x2029):
        text = text.replace(chr(number), f"\\u{number:04x}")
    return text


def main():
    url = sys.argv[2]
    output = Path(sys.argv[3] if len(sys.argv) > 3 else ".").resolve()
    if any(ord(character) < 32 or ord(character) in (0x7f, 0x85, 0x2028, 0x2029) for character in str(output)):
        fail("output directory must not contain control characters")
        return 3
    output.mkdir(parents=True, exist_ok=True)
    clients = (os.environ.get("YT_SUB_CLIENTS") or DEFAULT_CLIENTS).split()
    if not clients or any(not SAFE_COMPONENT.fullmatch(client) for client in clients):
        fail("YT_SUB_CLIENTS must contain space-separated player client names")
        return 3
    absent = 0
    expected_id = None
    for client in clients:
        probe = run_ytdlp(client, ["--dump-single-json", "--skip-download"], url)
        if probe.returncode or NETWORK_ERROR.search(probe.stderr):
            fail(f"client={client}: {process_problem(probe)}")
            continue
        try:
            metadata = decode_metadata(probe.stdout.decode("utf-8"))
            if expected_id is not None and metadata["id"] != expected_id:
                raise ValueError("client metadata refers to a different video")
            expected_id = metadata["id"]
        except (ValueError, UnicodeError):
            fail(f"client={client}: invalid metadata/track JSON; update yt-dlp and retry")
            continue
        selected = select_track(metadata)
        if selected is None:
            available = set(metadata["subtitles"]) | set(metadata["automatic_captions"])
            if available - {"live_chat"}:
                fail(f"client={client}: unsupported caption language; need manual ko/en or auto original/ko/en")
            elif INCOMPLETE_TRACKS.search(probe.stderr):
                fail(f"client={client}: incomplete caption discovery; check yt-dlp client/token support before retrying")
            else:
                absent += 1
            continue
        language, kind = selected
        video_id = metadata["id"]
        attempt = Path(tempfile.mkdtemp(prefix=".captions-attempt-", dir=output))
        save_metadata(attempt / f"{video_id}.probe.json", metadata)
        flags = ["--write-subs", "--no-write-auto-subs"] if kind == "manual" else ["--no-write-subs", "--write-auto-subs"]
        download = run_ytdlp(client, flags + [
            "--sub-langs", f"^{re.escape(language)}$", "--skip-download",
            "--sub-format", "srt/best", "--convert-subs", "srt", "--keep-video",
            "--dump-single-json", "--no-simulate", "-o",
            str(attempt).replace("%", "%%") + "/%(id)s.%(ext)s",
        ], url)
        if download.returncode or NETWORK_ERROR.search(download.stderr):
            fail(f"client={client}: {process_problem(download)}; files retained at {attempt}")
            continue
        srt = attempt / f"{video_id}.{language}.srt"
        try:
            downloaded_metadata = decode_metadata(download.stdout.decode("utf-8"))
            if downloaded_metadata["id"] != video_id:
                raise ValueError("download metadata ID does not match selected video")
            requested = downloaded_metadata.get("requested_subtitles")
            if not isinstance(requested, dict) or set(requested) != {language}:
                raise ValueError("download metadata does not match the selected single track")
            track_map = "subtitles" if kind == "manual" else "automatic_captions"
            if language not in downloaded_metadata[track_map] or not isinstance(requested[language], dict):
                raise ValueError("download metadata does not match the selected source kind")
            if not srt.is_file() or srt.is_symlink():
                raise ValueError("SRT conversion did not produce an SRT file; check ffmpeg (VTT is not SRT)")
            if attempt.is_symlink() or srt.resolve().parent != attempt:
                raise ValueError("SRT must remain inside its private attempt directory")
            captions_path = attempt / f"{video_id}.captions.json"
            metadata_path = attempt / f"{video_id}.metadata.json"
            if captions_path.exists() or captions_path.is_symlink():
                raise ValueError("captions JSON target already exists in the private attempt")
            requested[language].update(filepath=str(srt), ext="srt")
            document = make_document(
                srt, video_id, language, kind, metadata=downloaded_metadata, client=client,
            )
            # Unique paths are the commit boundary: finish the validated bundle
            # before emitting any path, without ever touching an older attempt.
            save_metadata(metadata_path, downloaded_metadata)
            write_document(document, captions_path)
        except (OSError, ValueError, UnicodeError) as error:
            # Only local validation messages are displayed, never external stderr.
            detail = str(error) if isinstance(error, ValueError) and not isinstance(error, json.JSONDecodeError) else "invalid metadata or output I/O failure"
            fail(f"client={client}: {detail}; originals retained at {attempt}")
            continue
        values = {
            "VIDEO_ID": video_id,
            "TITLE": title_line(downloaded_metadata["title"]),
            "SUB_LANG": language,
            "KIND": kind,
            "CLIENT": client,
            "SRT_PATH": str(srt),
            "CAPTIONS_PATH": str(captions_path),
            "METADATA_PATH": str(metadata_path),
        }
        for key, value in values.items():
            print(f"{key}={value}")
        return 0
    if absent == len(clients):
        fail("no captions: every client returned valid metadata with no caption tracks")
        return 2
    fail("caption acquisition failed; absence was not confirmed across clients (see diagnostics above)")
    return 3


try:
    sys.exit(main())
except (OSError, ValueError, UnicodeError):
    fail("unable to run yt-dlp or write outputs; check installation, permissions, and output directory")
    sys.exit(3)
PY
