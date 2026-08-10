#!/bin/bash
# YouTube 자막 추출
# Usage: ./extract_transcript.sh <URL> [output_dir]
# 1단계: 수동 자막 시도 → 2단계: 자동 자막 폴백
# 영어 원본 영상이면 영어 자막, 한국어 원본이면 한국어 자막 우선

URL="$1"
OUTPUT_DIR="${2:-.}"

if [ -z "$URL" ]; then
  echo "Usage: $0 <YouTube URL> [output_dir]"
  exit 1
fi

echo "$OUTPUT_DIR"

# 사용 가능한 자막 목록 확인
SUBS_INFO=$(yt-dlp --list-subs --skip-download "$URL" 2>&1)

# 원본 언어 감지 (en-orig가 있으면 영어 원본)
if echo "$SUBS_INFO" | grep -q "en-orig"; then
  LANG_PRIORITY="en-orig,en,ko"
elif echo "$SUBS_INFO" | grep -q "ko-orig"; then
  LANG_PRIORITY="ko-orig,ko,en"
else
  # 수동 자막에 ko가 있으면 한국어 우선, 아니면 영어 우선
  if echo "$SUBS_INFO" | grep -B100 "Available automatic captions" | grep -q "^ko "; then
    LANG_PRIORITY="ko,en"
  else
    LANG_PRIORITY="en,ko"
  fi
fi

echo "자막 우선순위: $LANG_PRIORITY"

# 1단계: 수동 자막 시도
yt-dlp --write-sub --sub-lang "$LANG_PRIORITY" --skip-download --sub-format srt \
  --cookies-from-browser chrome \
  -o "$OUTPUT_DIR/%(id)s.%(ext)s" "$URL" 2>&1

# 수동 자막 파일이 있는지 확인
ID=$(yt-dlp --print id --skip-download "$URL" 2>/dev/null)
FOUND_SUB=false
for lang in ${LANG_PRIORITY//,/ }; do
  if [ -f "$OUTPUT_DIR/${ID}.${lang}.srt" ]; then
    echo "수동 자막 발견: ${lang}"
    FOUND_SUB=true
    break
  fi
done

# 2단계: 수동 자막이 없으면 자동 자막 폴백
if [ "$FOUND_SUB" = false ]; then
  echo "수동 자막 없음 → 자동 자막 추출 시도"
  yt-dlp --write-auto-sub --sub-lang "$LANG_PRIORITY" --skip-download --sub-format srt \
    --cookies-from-browser chrome \
    -o "$OUTPUT_DIR/%(id)s.%(ext)s" "$URL" 2>&1
fi
