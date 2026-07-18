#!/usr/bin/env bash
# voice-memos 전사본 디렉토리에 diarized.md 생성
# usage: diarize.sh <audio> <transcript_dir> [apple|argmax|both] [start_sec] [end_sec]
#   transcript_dir : transcript.md가 있는 YYYYMMDD/HHMMSS/ 경로
#   mode 기본값   : argmax
set -euo pipefail

AUDIO="$1"
TRANSCRIPT_DIR="$2"
MODE="${3:-argmax}"
START="${4:-}"
END="${5:-}"

SKILLS_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
STT_SCRIPT="$SKILLS_DIR/stt/scripts/stt_diarize.sh"

# stt_diarize.sh 실행 후 생성된 파일 목록 수집
mapfile -t MADE < <(bash "$STT_SCRIPT" "$AUDIO" "$MODE" "$START" "$END")

# 결과물을 transcript_dir로 이동, 임시 폴더 제거
for f in "${MADE[@]}"; do
  mv "$f" "$TRANSCRIPT_DIR/"
done
rmdir "$(dirname "${MADE[0]}")" 2>/dev/null || true

printf '%s\n' "${MADE[@]/#*\//$(realpath "$TRANSCRIPT_DIR")/}"
