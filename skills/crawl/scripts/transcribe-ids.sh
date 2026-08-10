#!/bin/bash
# 표준입력으로 받은 YouTube video ID들(한 줄에 하나, 11자)의 자막을 youtube-digest 방식으로
# 추출해 <dest>/<ID>.md 로 저장. youtube-transcripts.sh(페이지 링크)·youtube-channels.py(채널)가 공유하는 전사 루프.
# (raw yt-dlp 직접 호출 금지 -- extract_transcript.sh 가 chrome 쿠키로 429 를 회피하는 정본)
# 증분: 기존 <dest>/<ID>.md 는 skip. --force 로 전체 재추출. 429 회피를 위해 순차 실행한다.
#
# Usage: <id 생성기> | transcribe-ids.sh <dest_dir> [--force]
set -uo pipefail
DEST="${1:?usage: <ids on stdin> | transcribe-ids.sh <dest_dir> [--force]}"
FORCE="${2:-}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
YT="$SCRIPT_DIR"
if [ ! -f "$YT/extract_transcript.sh" ] || [ ! -f "$YT/srt-to-md.sh" ]; then
  YT="${YOUTUBE_DIGEST_SCRIPTS:-$SCRIPT_DIR/../../youtube/youtube-digest/scripts}"
fi
if [ ! -f "$YT/extract_transcript.sh" ] || [ ! -f "$YT/srt-to-md.sh" ]; then
  echo "youtube transcript helpers not found; set YOUTUBE_DIGEST_SCRIPTS" >&2
  exit 69
fi
mkdir -p "$DEST"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

ids="$(grep -oE '[A-Za-z0-9_-]{11}' | sort -u)"

# 유효한 srt 한 장을 골라 .md로 변환. 성공 시 0, 자막 없음 1, 429류 일시실패 2 반환.
# 빈 srt(429로 38바이트 헤더만 옴)는 자막 없음이 아니라 일시실패로 본다(>500B만 유효).
try_one() {
  local id="$1" md="$2"
  rm -f "$TMP"/*.srt 2>/dev/null
  local out; out="$(bash "$YT/extract_transcript.sh" "https://www.youtube.com/watch?v=$id" "$TMP" 2>&1)"
  # en-orig > en > ko 순으로 500바이트 넘는 첫 srt 선택
  local srt=""
  for lang in en-orig en ko ko-orig; do
    local f="$TMP/${id}.${lang}.srt"
    if [ -f "$f" ] && [ "$(wc -c < "$f")" -gt 500 ]; then srt="$f"; break; fi
  done
  if [ -z "$srt" ]; then
    srt="$(find "$TMP" -name "${id}.*.srt" -size +500c 2>/dev/null | head -1)"
  fi
  if [ -z "$srt" ]; then
    echo "$out" | grep -q "429" && return 2   # 429 -> 일시실패(재시도 대상)
    return 1                                   # 진짜 자막 없음
  fi
  bash "$YT/srt-to-md.sh" "$srt" "$md" >/dev/null 2>&1
  [ -s "$md" ] && return 0 || return 2
}

write_no_caption_stub() {
  local id="$1" md="$2" processed
  processed="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
  cat > "$md" <<EOF
---
title: "YouTube $id"
url: https://youtu.be/$id
youtube_id: $id
transcript_status: "no_captions"
processed_at: $processed
---

# YouTube $id

## 자막

_(자막 없음)_
EOF
}

total="$(printf '%s\n' "$ids" | grep -c .)"
echo "고유 video ID: $total"
done=0; ok=0; skip=0; fail=0; nocap=0; streak=0
for id in $ids; do
  done=$((done+1))
  md="$DEST/${id}.md"
  if [ -z "$FORCE" ] && [ -f "$md" ]; then skip=$((skip+1)); continue; fi
  try_one "$id" "$md"; rc=$?
  if [ "$rc" = 2 ]; then            # 429/일시실패 -> 백오프 후 1회 재시도
    streak=$((streak+1))
    nap=20; [ "$streak" -ge 3 ] && nap=60   # 연속 실패 누적 시 더 길게 (429 누그러뜨림)
    echo "  [$done/$total] 429 추정 -> ${nap}s 대기 후 재시도 $id"
    sleep "$nap"
    try_one "$id" "$md"; rc=$?
  fi
  case "$rc" in
    0) echo "  [$done/$total] OK $id"; ok=$((ok+1)); streak=0 ;;
    1) write_no_caption_stub "$id" "$md"; echo "  [$done/$total] 자막없음 $id"; nocap=$((nocap+1)); streak=0 ;;
    *) echo "  [$done/$total] FAIL(429지속) $id"; fail=$((fail+1)) ;;
  esac
  sleep 4   # 영상 간 간격으로 rate limit 완화
done
echo "자막 추출: 성공 $ok / 스킵 $skip / 자막없음 $nocap / 실패(429) $fail / 총 $total"
if [ "$fail" -gt 0 ]; then
  echo "(실패분은 시간 두고 재실행하면 증분으로 자동 재시도됨)"
fi
