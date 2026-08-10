#!/usr/bin/env bash
# Apple first; only a process failure falls back to Handy's selected local model.
set -euo pipefail

usage() {
  echo "usage: stt-fallback.sh <audio>" >&2
}

if [ "${1:-}" = "-h" ] || [ "${1:-}" = "--help" ]; then
  usage
  exit 0
fi
if [ "$#" -ne 1 ]; then
  usage
  exit 64
fi

AUDIO="$1"
if [ ! -f "$AUDIO" ]; then
  echo "audio file not found: $AUDIO" >&2
  exit 66
fi

WORK_DIR="$(mktemp -d "${TMPDIR:-/tmp}/stt-fallback.XXXXXXXX")"
cleanup() {
  /bin/rm -rf -- "$WORK_DIR"
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

APPLE_BIN="${APPLE_STT_BIN:-$(command -v apple-stt || true)}"
if [ -n "$APPLE_BIN" ]; then
  if "$APPLE_BIN" -q "$AUDIO" > "$WORK_DIR/apple.txt" 2> "$WORK_DIR/apple.err"; then
    /bin/cat "$WORK_DIR/apple.txt"
    exit 0
  fi
  echo "apple-stt failed; using Handy's selected local model" >&2
  [ ! -s "$WORK_DIR/apple.err" ] || /bin/cat "$WORK_DIR/apple.err" >&2
else
  echo "apple-stt not found; using Handy's selected local model" >&2
fi

FFMPEG="${FFMPEG_BIN:-$(command -v ffmpeg || true)}"
if [ -z "$FFMPEG" ]; then
  echo "ffmpeg not found; install it or set FFMPEG_BIN" >&2
  exit 69
fi

HANDY="${HANDY_BIN:-$(command -v handy || true)}"
if [ -z "$HANDY" ] && [ -x /Applications/Handy.app/Contents/MacOS/handy ]; then
  HANDY=/Applications/Handy.app/Contents/MacOS/handy
fi
if [ -z "$HANDY" ]; then
  echo "Handy CLI not found; install Handy or set HANDY_BIN" >&2
  exit 69
fi

WAV="$WORK_DIR/input.wav"
"$FFMPEG" -v error -y -i "$AUDIO" -vn -ac 1 -ar 16000 -c:a pcm_s16le "$WAV"
"$HANDY" --transcribe-file "$WAV"
