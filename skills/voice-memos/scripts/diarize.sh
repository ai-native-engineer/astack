#!/usr/bin/env bash
# Diarize a Voice Memos recording and keep the whole stt result in <transcript_dir>/diarization.
# usage: diarize.sh <audio> [transcript_dir|-] [start_sec] [end_sec]
#   Without transcript_dir, or with "-", the folder the pipeline uses for this recording.
set -euo pipefail
umask 077

if [ "$#" -lt 1 ] || [ "$#" -gt 4 ]; then
  echo "usage: diarize.sh <audio> [transcript_dir|-] [start_sec] [end_sec]" >&2
  exit 64
fi

AUDIO="$1"
TRANSCRIPT_DIR="${2:--}"
START="${3:-}"
END="${4:-}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
STT_SCRIPT="${VOICE_MEMOS_STT_DIARIZE:-$(cd "$SCRIPT_DIR/../.." && pwd)/stt/scripts/stt_diarize.sh}"

if [ "$TRANSCRIPT_DIR" = "-" ]; then
  TRANSCRIPT_DIR="$(python3 -I -c '
import sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
import config
try:
    print(config.transcript_dir_for_audio(Path(sys.argv[2])))
except config.PipelineError as error:
    sys.exit(f"cannot choose a transcript folder for {sys.argv[2]}: {error}; pass transcript_dir")
' "$SCRIPT_DIR" "$AUDIO")"
fi

# stt writes into STT_OUT (default: ./stt under the caller's directory), so give it a
# private scratch folder and move the whole result. The review screen needs run.json,
# names.json and speakers.json next to diarized.md, and speakers.json holds voice
# embeddings that must not be left in whatever directory the caller happened to be in.
# The result gets its own subfolder: stt's run.json is not the pipeline's run.json, and
# beside transcript.md it would be read as strict run metadata and fail every summary pass.
WORK="$(mktemp -d "${TMPDIR:-/tmp}/voice-memos-diarize.XXXXXX")"
GENERATED="$(STT_OUT="$WORK" bash "$STT_SCRIPT" "$AUDIO" "$START" "$END")"
RESULT_DIR="$(dirname "$GENERATED")"
DIARIZATION_DIR="$TRANSCRIPT_DIR/diarization"
mkdir -p "$DIARIZATION_DIR"
for file in "$RESULT_DIR"/*; do
  mv -f -- "$file" "$DIARIZATION_DIR/"
done
rmdir "$RESULT_DIR" "$WORK"
printf '%s\n' "$DIARIZATION_DIR/diarized.md"
