#!/usr/bin/env bash
# 로컬 STT + 화자분리 뷰 생성: apple-stt 텍스트와 argmax 화자 타임라인을 정렬해 화자 라벨 전사본을 만든다.
#
# usage: stt_diarize.sh <audio> <apple|argmax|both> [start_sec] [end_sec]
#   apple  : apple-stt 텍스트 + argmax 화자(굵음). 가벼움(전사 모델 없이 diarize만 다운로드)
#   argmax : argmax(WhisperKit) 텍스트 + 단어단위 정밀 화자. 무거움(632MB 모델)
#   both   : 둘 다 생성. 정확도 최고 / 토큰 최다
#   [start end] : 구간만 처리(초). 이동·잡음 구간 제외해 화자 과검출 방지. 예) 0 752
#
# env:
#   ARGMAX_CLI  argmax-cli 경로 (기본: PATH의 argmax-cli)
#   STT_OUT     출력 루트 (기본 ./stt)
#   STT_LANG    전사 언어 코드 (기본 ko)
# 출력: <STT_OUT>/YYMMDD-HHMM/{transcript.md, diarized.md}
set -euo pipefail

AUDIO="$1"; MODE="${2:-apple}"; START="${3:-}"; END="${4:-}"
CLI="${ARGMAX_CLI:-argmax-cli}"
LANG_CODE="${STT_LANG:-ko}"
HERE="$(cd "$(dirname "$0")" && pwd)"
OUT="${STT_OUT:-$PWD/stt}/$(date +%y%m%d-%H%M)"
mkdir -p "$OUT"

# 구간 트림(선택) — 이동·잡음 구간이 가짜 화자로 잡히는 것 방지
SRC="$AUDIO"
if [ -n "$START$END" ]; then
  SRC="$OUT/clip.m4a"
  args=(-y); [ -n "$START" ] && args+=(-ss "$START"); args+=(-i "$AUDIO")
  [ -n "$END" ] && args+=(-to "$END"); args+=(-c copy "$SRC")
  ffmpeg "${args[@]}" >/dev/null 2>&1
fi

case "$MODE" in apple|argmax|both) ;; *) echo "MODE: apple|argmax|both"; exit 1 ;; esac

# 화자 타임라인은 두 뷰 공통 입력 → 항상 생성(전사 없이 가벼움)
"$CLI" diarize --audio-path "$SRC" --rttm-path "$OUT/diar.rttm" >/dev/null 2>&1

made=()
if [ "$MODE" = apple ] || [ "$MODE" = both ]; then
  apple-stt "$SRC" --json > "$OUT/apple.json" 2>/dev/null
  python3 "$HERE/diar_views.py" apple "$OUT/apple.json" "$OUT/diar.rttm" > "$OUT/transcript.md"
  made+=("$OUT/transcript.md")
fi
AJSON=""
if [ "$MODE" = argmax ] || [ "$MODE" = both ]; then
  "$CLI" transcribe --audio-path "$SRC" --model large-v3-v20240930_turbo_632MB \
     --language "$LANG_CODE" --diarization --word-timestamps --report --report-path "$OUT" >/dev/null 2>&1
  AJSON="$OUT/$(basename "${SRC%.*}").json"
  python3 "$HERE/diar_views.py" argmax "$AJSON" "$OUT/diar.rttm" > "$OUT/diarized.md"
  made+=("$OUT/diarized.md")
fi

# 중간 파일 정리 — _view.md만 남김
rm -f "$OUT/apple.json" "$OUT/diar.rttm" "$OUT"/*.srt
[ -n "$AJSON" ] && rm -f "$AJSON"
[ -n "$START$END" ] && rm -f "$OUT/clip.m4a"

printf '%s\n' "${made[@]}"
