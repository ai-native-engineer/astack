#!/bin/bash
# YouTube 자막(SRT) 취득 - youtube 스킬 전체의 단일 구현.
#
# yt-dlp 기본 player client는 PO token 없이 자막 트랙을 숨겨, 자막이 실재해도
# "has no automatic captions"로 응답한다. client를 바꿔가며 탐지해 이 오탐을 없앤다.
#
# Usage: fetch-subs.sh <YouTube URL> [output_dir]
# stdout: VIDEO_ID= / TITLE= / SUB_LANG= / KIND= / CLIENT= / SRT_PATH=
# exit: 0 취득 / 2 모든 client에서 자막 없음 / 3 자막은 탐지됐으나 내려받기 실패

set -uo pipefail

URL="${1:-}"
OUTPUT_DIR="${2:-.}"

if [ -z "$URL" ]; then
  echo "Usage: $0 <YouTube URL> [output_dir]" >&2
  exit 1
fi

mkdir -p "$OUTPUT_DIR"

# 기본 client가 막혔을 때 순서대로 시도한다. default를 먼저 둬 정상 영상은 추가 호출 없이 끝낸다.
CLIENTS="${YT_SUB_CLIENTS:-default web_embedded web_safari mweb tv_embedded}"
COOKIE_BROWSER="${YT_COOKIES_FROM_BROWSER:-chrome}"

# 쿠키는 있으면 쓰고 없으면 없는 대로 간다. 연령제한·지역제한 영상에서만 실제로 필요하다.
COOKIE_ARGS=()
[ -n "$COOKIE_BROWSER" ] && COOKIE_ARGS=(--cookies-from-browser "$COOKIE_BROWSER")

run_ytdlp() {
  local client="$1"; shift
  local extra=()
  [ "$client" != "default" ] && extra=(--extractor-args "youtube:player_client=$client")
  # macOS 기본 bash 3.2는 set -u에서 빈 배열 전개를 오류로 처리한다.
  yt-dlp ${COOKIE_ARGS[@]+"${COOKIE_ARGS[@]}"} ${extra[@]+"${extra[@]}"} "$@" 2>&1
}

# --- 1. 자막을 내주는 client 탐지 ---
FOUND_CLIENT=""
SUBS_INFO=""
for client in $CLIENTS; do
  info=$(run_ytdlp "$client" --list-subs --skip-download "$URL")
  if echo "$info" | grep -q "Available subtitles\|Available automatic captions"; then
    FOUND_CLIENT="$client"
    SUBS_INFO="$info"
    break
  fi
done

if [ -z "$FOUND_CLIENT" ]; then
  echo "자막 없음: 시도한 client(${CLIENTS})에서 수동·자동 자막 트랙이 모두 확인되지 않았습니다." >&2
  echo "자막이 있다고 알고 있다면 yt-dlp를 업데이트하거나 PO token provider 플러그인을 설치하세요." >&2
  exit 2
fi

echo "자막 트랙 확인: client=$FOUND_CLIENT" >&2

# --- 2. 받을 언어 1개를 확정 ---
# 다국어를 한 번에 요청하면 영상당 요청 수가 배로 늘어 429가 빨리 터진다. 탐지 목록에서 1개만 고른다.
section_langs() {
  echo "$SUBS_INFO" | awk -v want="$1" '
    /Available subtitles/            {s="manual"; next}
    /Available automatic captions/   {s="auto";   next}
    s==want && /^[a-zA-Z]/ && $0 !~ /^Language/ {print $1}'
}
MANUAL_LANGS=$(section_langs manual)
AUTO_LANGS=$(section_langs auto)

# 수동 자막이 자동보다 정확하고, 자동 안에서는 원어(-orig)가 기계번역본보다 정확하다.
pick_lang() {
  local list="$1"; shift
  for want in "$@"; do
    if [ "$want" = "*-orig" ]; then
      local hit; hit=$(echo "$list" | grep -- '-orig$' | head -1)
      [ -n "$hit" ] && { echo "$hit"; return 0; }
    elif echo "$list" | grep -qx -- "$want"; then
      echo "$want"; return 0
    fi
  done
  return 1
}

SUB_LANG=$(pick_lang "$MANUAL_LANGS" ko en) && KIND=manual
if [ -z "${SUB_LANG:-}" ]; then
  SUB_LANG=$(pick_lang "$AUTO_LANGS" '*-orig' ko en) && KIND=auto
fi

if [ -z "${SUB_LANG:-}" ]; then
  echo "취득 실패: 자막 트랙은 있으나 ko/en/원어가 아닌 언어만 제공합니다." >&2
  echo "$SUBS_INFO" | grep -A5 "Available" >&2
  exit 3
fi

echo "선택: lang=$SUB_LANG kind=$KIND" >&2

# --- 3. 다운로드 ---
# 탐지에 성공한 client를 그대로 쓴다. 탐지와 내려받기 조건이 다르면 다시 오탐이 난다.
WRITE_FLAG=$([ "$KIND" = manual ] && echo --write-sub || echo --write-auto-sub)
# --print은 simulate를 켜서 파일을 쓰지 않는다. --no-simulate로 되돌려야 파일이 저장된다.
# 자동 자막은 vtt로 내려오므로 --convert-subs로 srt를 보장한다(ffmpeg 필요).
META=$(run_ytdlp "$FOUND_CLIENT" "$WRITE_FLAG" --sub-lang "$SUB_LANG" \
  --skip-download --sub-format "srt/best" --convert-subs srt \
  --print "%(id)s|%(title)s" --no-simulate \
  -o "$OUTPUT_DIR/%(id)s.%(ext)s" "$URL" | tee /dev/stderr | grep -m1 '|')

VIDEO_ID="${META%%|*}"
TITLE="${META#*|}"

# ffmpeg가 없으면 변환이 생략돼 원본 확장자로 남는다. 실제로 생긴 파일을 쓴다.
SRT_PATH=""
for ext in srt vtt; do
  if [ -f "$OUTPUT_DIR/${VIDEO_ID}.${SUB_LANG}.${ext}" ]; then
    SRT_PATH="$OUTPUT_DIR/${VIDEO_ID}.${SUB_LANG}.${ext}"
    break
  fi
done

if [ -z "$SRT_PATH" ]; then
  echo "취득 실패: client=$FOUND_CLIENT lang=$SUB_LANG 트랙은 보였으나 자막 파일이 생성되지 않았습니다." >&2
  exit 3
fi

echo "VIDEO_ID=$VIDEO_ID"
echo "TITLE=$TITLE"
echo "SUB_LANG=$SUB_LANG"
echo "KIND=$KIND"
echo "CLIENT=$FOUND_CLIENT"
echo "SRT_PATH=$SRT_PATH"
