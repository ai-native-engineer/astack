#!/usr/bin/env bash
# MOSS text and speakers per chunk, chunk speakers joined by voice, all local.
# Speakers whose voices were remembered with scripts/voices.py enroll are shown by name.
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

if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "ffmpeg not found in PATH" >&2
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

# Pinned to the mlx-audio release the MOSS output parsing was measured with.
if [ -n "${MOSS_PYTHON:-}" ]; then
  MOSS=("$MOSS_PYTHON")
elif command -v uv >/dev/null 2>&1; then
  MOSS=(uv run --quiet --no-project --python 3.14 --with mlx-audio==0.5.9 --with jinja2 python)
else
  echo "uv not found; install uv or set MOSS_PYTHON to a Python with mlx-audio 0.5.9" >&2
  exit 69
fi

"$PYANNOTE_PYTHON" "$HERE/pyannote-chunks.py" --check
"${MOSS[@]}" "$HERE/moss-diarize.py" --check

mkdir -p "$OUT"

cleanup() {
  /bin/rm -f -- "$OUT/audio.wav" "$OUT/chunks.json" "$OUT/speech.json" "$OUT/moss.json"
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

# run.json tells diar_review.py which audio to play and where the times start.
python3 -c 'import json, os, sys; json.dump({"audio": os.path.abspath(sys.argv[1]), "start": float(sys.argv[2] or 0),
  "end": float(sys.argv[3]) if sys.argv[3] else None}, open(sys.argv[4], "w"))' \
  "$AUDIO" "$START" "$END" "$OUT/run.json"

ffmpeg_args=(-nostdin -v error -y)
[ -z "$START" ] || ffmpeg_args+=(-ss "$START")
[ -z "$END" ] || ffmpeg_args+=(-to "$END")
ffmpeg_args+=(-i "$AUDIO" -vn -ar 16000 -ac 1 -c:a pcm_s16le "$OUT/audio.wav")
ffmpeg "${ffmpeg_args[@]}"

"$PYANNOTE_PYTHON" "$HERE/pyannote-chunks.py" plan "$OUT/audio.wav" "$OUT/chunks.json" "$OUT/speech.json"
if ! "${MOSS[@]}" "$HERE/moss-diarize.py" "$OUT/audio.wav" "$OUT/chunks.json" "$OUT/moss.json"; then
  echo "MOSS diarization failed; for text without speakers run scripts/stt-fallback.sh" >&2
  exit 70
fi
"$PYANNOTE_PYTHON" "$HERE/pyannote-chunks.py" join "$OUT/audio.wav" "$OUT/moss.json" "$OUT/speech.json" "$OUT"
python3 "$HERE/voices.py" match "$OUT"
python3 "$HERE/diar_views.py" --names "$OUT/names.json" "$OUT/transcript.json" "${START:-0}" \
  > "$OUT/diarized.md"

printf '%s\n' "$OUT/diarized.md"
