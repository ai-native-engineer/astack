#!/usr/bin/env bash
# ElevenLabs Scribe 전사 + 화자분리
# 사용: transcribe-elevenlabs.sh <audio> [key@tag] [language_code]
#   language_code 생략 시 자동감지. model_id=scribe_v1, diarize=true 고정.
# 키는 agents-env로 주입(평문 노출 없음). 응답은 raw JSON(words[].speaker_id 포함).
# 같은 키 이름에 태그가 여럿이면 두번째 인자로 ELEVENLABS_API_KEY@<태그> 지정.
set -euo pipefail

AUDIO="${1:?usage: transcribe-elevenlabs.sh <audio> [key@tag] [language_code]}"
KEYSEL="${2:-ELEVENLABS_API_KEY}"
KEYNAME="${KEYSEL%@*}"

LANGOPT=()
[ -n "${3:-}" ] && LANGOPT=(-F language_code="$3")

agents-env run "$KEYSEL" -- curl -sS https://api.elevenlabs.io/v1/speech-to-text \
  -H "xi-api-key: {{${KEYNAME}}}" \
  -F model_id=scribe_v1 \
  -F file=@"$AUDIO" \
  -F diarize=true \
  ${LANGOPT[@]+"${LANGOPT[@]}"}
