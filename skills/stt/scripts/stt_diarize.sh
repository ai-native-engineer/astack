#!/usr/bin/env bash
# Apple text + local pyannote RTTM. Diarization never replaces text.
# usage: stt_diarize.sh <audio> [start_sec] [end_sec]
set -euo pipefail
umask 077

if [ "$#" -lt 1 ] || [ "$#" -gt 3 ]; then
  echo "usage: stt_diarize.sh <audio> [start_sec] [end_sec]" >&2
  exit 64
fi

AUDIO="$1"
START="${2:-}"
END="${3:-}"
HERE="$(cd "$(dirname "$0")" && pwd)"
OUT_ROOT="${STT_OUT:-$PWD/stt}"
OUT="$OUT_ROOT/$(date +%y%m%d-%H%M%S)-$$"

if [ ! -f "$AUDIO" ]; then
  echo "audio file not found: $AUDIO" >&2
  exit 66
fi

for boundary in "$START" "$END"; do
  if [ -n "$boundary" ] && ! [[ "$boundary" =~ ^([0-9]+([.][0-9]*)?|[.][0-9]+)$ ]]; then
    echo "start/end must be nonnegative seconds" >&2
    exit 64
  fi
done
if [ -n "$START" ] && [ -n "$END" ] && ! awk -v start="$START" -v end="$END" 'BEGIN { exit !(end > start) }'; then
  echo "end must be greater than start" >&2
  exit 64
fi

APPLE_STT_BIN="${APPLE_STT_BIN:-$(command -v apple-stt || true)}"
if [ -z "$APPLE_STT_BIN" ]; then
  echo "apple-stt not found; add it to PATH or set APPLE_STT_BIN" >&2
  exit 69
fi

PYANNOTE_PYTHON="${PYANNOTE_PYTHON:-}"
if [ -z "$PYANNOTE_PYTHON" ] && command -v uv >/dev/null 2>&1; then
  PYANNOTE_PYTHON="$(uv tool dir)/whispermlx/bin/python"
fi
if [ ! -x "$PYANNOTE_PYTHON" ]; then
  echo "pyannote runtime missing; install whispermlx with uv tool install --python 3.12 whispermlx, or set PYANNOTE_PYTHON" >&2
  exit 69
fi
"$PYANNOTE_PYTHON" "$HERE/pyannote-diarize.py" --check

mkdir -p "$OUT"
SRC="$AUDIO"
CLIP=""

cleanup() {
  [ -z "$CLIP" ] || rm -- "$CLIP" 2>/dev/null || true
  rm -- "$OUT/apple.json" 2>/dev/null || true
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

if [ -n "$START$END" ]; then
  if ! command -v ffmpeg >/dev/null 2>&1; then
    echo "ffmpeg is required when start/end trimming is requested" >&2
    exit 69
  fi
  CLIP="$OUT/clip.wav"
  ffmpeg_args=(-y)
  [ -z "$START" ] || ffmpeg_args+=(-ss "$START")
  [ -z "$END" ] || ffmpeg_args+=(-to "$END")
  ffmpeg_args+=(-i "$AUDIO")
  ffmpeg_args+=(-vn -ar 16000 -ac 1 -c:a pcm_s16le "$CLIP")
  ffmpeg -v error "${ffmpeg_args[@]}" >/dev/null
  SRC="$CLIP"
fi

"$APPLE_STT_BIN" --json -q "$SRC" > "$OUT/apple.json"
"$PYANNOTE_PYTHON" "$HERE/pyannote-diarize.py" --audio-path "$SRC" --rttm-path "$OUT/diar.rttm" >/dev/null
python3 "$HERE/diar_views.py" "$OUT/apple.json" "$OUT/diar.rttm" "${START:-0}" > "$OUT/diarized.md"

printf '%s\n' "$OUT/diarized.md"
