#!/usr/bin/env bash
# Generate diarized.md beside an existing Voice Memos transcript.
# usage: diarize.sh <audio> <transcript_dir> [start_sec] [end_sec]
set -euo pipefail

if [ "$#" -lt 2 ] || [ "$#" -gt 4 ]; then
  echo "usage: diarize.sh <audio> <transcript_dir> [start_sec] [end_sec]" >&2
  exit 64
fi

AUDIO="$1"
TRANSCRIPT_DIR="$2"
START="${3:-}"
END="${4:-}"
SKILLS_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
STT_SCRIPT="$SKILLS_DIR/stt/scripts/stt_diarize.sh"

mkdir -p "$TRANSCRIPT_DIR"
GENERATED="$(bash "$STT_SCRIPT" "$AUDIO" "$START" "$END")"
DESTINATION="$TRANSCRIPT_DIR/diarized.md"
mv "$GENERATED" "$DESTINATION"
if [ -f "$(dirname "$GENERATED")/diar.rttm" ]; then
  mv "$(dirname "$GENERATED")/diar.rttm" "$TRANSCRIPT_DIR/diar.rttm"
fi
rmdir "$(dirname "$GENERATED")" 2>/dev/null || true
printf '%s\n' "$DESTINATION"
