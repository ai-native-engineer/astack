#!/usr/bin/env bash
# OpenAI gpt-4o-transcribe-diarize 전사 + 화자분리
# 사용: transcribe-openai.sh <audio> [key@tag] [response_format]
#   response_format: diarized_json(기본) | json | text
# 키는 agents-env로 주입(평문 노출 없음). 30초+ 오디오는 chunking_strategy=auto 자동.
# 같은 키 이름에 태그가 여럿이면 두번째 인자로 OPENAI_API_KEY@<태그> 지정.
set -euo pipefail

AUDIO="${1:?usage: transcribe-openai.sh <audio> [key@tag] [diarized_json|json|text]}"
KEYSEL="${2:-OPENAI_API_KEY}"
FMT="${3:-diarized_json}"
KEYNAME="${KEYSEL%@*}"

# 30초 초과면 chunking_strategy 필요
DUR=$(ffprobe -i "$AUDIO" -show_entries format=duration -v quiet -of csv=p=0 2>/dev/null || echo 0)
CHUNK=()
awk "BEGIN{exit !($DUR > 30)}" && CHUNK=(-F chunking_strategy=auto)

agents-env run "$KEYSEL" -- curl -sS https://api.openai.com/v1/audio/transcriptions \
  -H "Authorization: Bearer {{${KEYNAME}}}" \
  -F file=@"$AUDIO" \
  -F model=gpt-4o-transcribe-diarize \
  -F response_format="$FMT" \
  ${CHUNK[@]+"${CHUNK[@]}"}
