#!/bin/bash
# SRT 자막 → Obsidian 호환 Markdown
# - frontmatter: title, url, channel, date, duration, lang, youtube_id, processed_at
# - 본문: 영상 메타 헤더 + 1분 간격 [HH:MM] 마커 자막 (srt_to_txt.sh 로직 재사용)
# - SRT 원본 변환 후 자동 제거
# Usage: ./srt-to-md.sh <input.srt> [output.md]
#
# 입력 SRT 파일명은 yt-dlp 표준 `<videoId>.<lang>.srt` 형식이어야 메타 fetch 가능.

set -euo pipefail

INPUT="${1:-}"
OUTPUT="${2:-}"

if [ -z "$INPUT" ] || [ ! -f "$INPUT" ]; then
  echo "Usage: $0 <input.srt> [output.md]" >&2
  exit 1
fi

if [ -z "$OUTPUT" ]; then
  OUTPUT="${INPUT%.srt}.md"
fi

# 파일명에서 video ID·언어 파싱 (yt-dlp 표준: <id>.<lang>.srt)
BASENAME=$(basename "$INPUT")
STEM="${BASENAME%.srt}"
LANG="${STEM##*.}"
VIDEO_ID="${STEM%.*}"
URL="https://youtu.be/${VIDEO_ID}"

echo "Video ID: $VIDEO_ID" >&2
echo "Language: $LANG" >&2

# yt-dlp로 메타 fetch (cookies-from-browser chrome — 429 우회 + 로그인 전용 영상)
META_JSON=$(yt-dlp --dump-json --no-download \
  --cookies-from-browser chrome \
  "$URL" 2>/dev/null || echo "{}")

TITLE=$(echo "$META_JSON" | jq -r --arg fallback "YouTube $VIDEO_ID" '.title // $fallback')
TITLE_YAML=$(printf '%s' "$TITLE" | jq -R -s '.')
CHANNEL=$(echo "$META_JSON" | jq -r '.channel // ""')
CHANNEL_YAML=$(printf '%s' "$CHANNEL" | jq -R -s '.')
CHANNEL_URL=$(echo "$META_JSON" | jq -r '.channel_url // ""')
DURATION_STR=$(echo "$META_JSON" | jq -r '.duration_string // ""')
UPLOAD_DATE=$(echo "$META_JSON" | jq -r '.upload_date // ""')

if [ "${#UPLOAD_DATE}" -eq 8 ]; then
  UPLOAD_ISO="${UPLOAD_DATE:0:4}-${UPLOAD_DATE:4:2}-${UPLOAD_DATE:6:2}"
else
  UPLOAD_ISO="$UPLOAD_DATE"
fi

PROCESSED_AT=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# SRT → body: 1분 간격 [HH:MM] 마커, HTML 태그 제거, 롤링 자막 중복 제거
# 자동 자막은 한 문장이 한 단어씩 자라며 여러 큐에 겹쳐 저장된다("나는"→"나는 오늘"→...).
# buf에 현재 줄을 물고 있다가, 다음 줄이 확장이면 buf를 늘리고, 새 문장이면 buf를 flush한다.
# → 접두사로 자라는 롤링을 최종 최장 문장 하나로 접고, 타임스탬프는 문장 시작 시점으로 남긴다.
BODY=$(awk '
BEGIN { buf = ""; buf_min = -1; last_min = -1 }
function flush(   h, m) {
  if (buf == "") return
  if (buf_min >= 0 && buf_min != last_min && (last_min == -1 || buf_min > last_min)) {
    h = int(buf_min / 60); m = buf_min % 60
    printf "\n[%02d:%02d]\n", h, m
    last_min = buf_min
  }
  print buf; buf = ""
}
/^[0-9]{2}:[0-9]{2}:[0-9]{2}/ {
  split($1, t, ":")
  cur_min = t[1] * 60 + t[2]
  next
}
/^[0-9]+$/ { next }
/^[[:space:]]*$/ { next }
{
  gsub(/<[^>]+>/, "")
  gsub(/^[[:space:]]+|[[:space:]]+$/, "")
  if ($0 == "") next
  line = $0
  if (buf == "") { buf = line; buf_min = cur_min; next }
  if (line == buf) next                       # 완전 중복
  if (index(line, buf) == 1) { buf = line; next }   # 롤링 확장: buf가 line의 접두사
  if (index(buf, line) == 1) next             # line이 buf의 부분집합
  flush(); buf = line; buf_min = cur_min
}
END { flush() }
' "$INPUT")

# 채널 라인 (URL 있으면 마크다운 링크)
if [ -n "$CHANNEL" ] && [ -n "$CHANNEL_URL" ]; then
  CHANNEL_LINE="- 채널: [$CHANNEL]($CHANNEL_URL)"
elif [ -n "$CHANNEL" ]; then
  CHANNEL_LINE="- 채널: $CHANNEL"
else
  CHANNEL_LINE=""
fi

# MD 작성
{
  echo "---"
  echo "title: $TITLE_YAML"
  echo "url: $URL"
  echo "channel: $CHANNEL_YAML"
  [ -n "$UPLOAD_ISO" ] && echo "date: $UPLOAD_ISO"
  [ -n "$DURATION_STR" ] && echo "duration: \"$DURATION_STR\""
  echo "lang: $LANG"
  echo "youtube_id: $VIDEO_ID"
  echo "processed_at: $PROCESSED_AT"
  echo "---"
  echo ""
  echo "# $TITLE"
  echo ""
  [ -n "$CHANNEL_LINE" ] && echo "$CHANNEL_LINE"
  [ -n "$UPLOAD_ISO" ] && echo "- 발행: $UPLOAD_ISO"
  [ -n "$DURATION_STR" ] && echo "- 길이: $DURATION_STR"
  echo "- 영상: <$URL>"
  echo ""
  echo "## 자막 ($LANG)"
  echo ""
  echo "$BODY"
} > "$OUTPUT"

# 결과 통계
input_lines=$(wc -l < "$INPUT")
output_lines=$(wc -l < "$OUTPUT")
output_size=$(wc -c < "$OUTPUT" | tr -d ' ')

echo "변환 완료: $OUTPUT" >&2
echo "  SRT: ${input_lines} lines → MD: ${output_lines} lines ($(echo "scale=0; $output_size/1024" | bc)KB)" >&2

# SRT 원본 제거 (srt_to_txt.sh 패턴)
rm "$INPUT"
echo "  SRT 원본 제거: $INPUT" >&2
