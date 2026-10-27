#!/bin/bash
# 미러의 YouTube 링크를 공용 자막 JSON으로 취득해 <out>/_yt-cache/<ID>.md 로 저장.
# ID 수집만 여기서 하고, 원본 보존·상태 구분·성공 검증은 transcribe-ids.sh가 맡는다.
# 원본과 JSON은 _yt-cache/transcripts/에 남기고, 해시 검증된 성공만 skip한다.
# 자막없음 기록은 재확인하며 --force는 기존 성공도 다시 취득한다.
#
# Usage: youtube-transcripts.sh <out_dir> [--force] [--exclude <glob>]...
#   범용 기본 제외(_yt-cache/**, youtube.com/**)만 내장 -- 도메인 하드코딩 없음(crawl 범용 유지).
#   academy/docs 같은 미러별 트리는 호출자(각 미러 SKILL)가 --exclude 로 넘긴다. 예:
#     youtube-transcripts.sh . --exclude 'anthropic.skilljar.com/**' --exclude 'code.claude.com/**'
#   (academy 트리는 render-video-refs가 이미 전사를 인라인하므로 또 긁으면 watch URL이 중복으로 잡힌다.)
set -uo pipefail
OUT="${1:?usage: youtube-transcripts.sh <out_dir> [--force] [--exclude <glob>]...}"
shift
HERE="$(cd "$(dirname "$0")" && pwd)"
FORCE=""
EXCLUDES=(-g '!_yt-cache/**' -g '!youtube.com/**')
while [ $# -gt 0 ]; do
  case "$1" in
    --force) FORCE="--force" ;;
    --exclude) shift; EXCLUDES+=(-g "!$1") ;;
    *) echo "unknown arg: $1" >&2 ;;
  esac
  shift
done

rg -o -i --max-filesize 2M \
  -e 'youtu\.be/[A-Za-z0-9_-]{11}' \
  -e 'youtube\.com/watch\?v=[A-Za-z0-9_-]{11}' \
  -e 'youtube\.com/embed/[A-Za-z0-9_-]{11}' \
  -e 'youtube\.com/live/[A-Za-z0-9_-]{11}' \
  -e 'youtube\.com/shorts/[A-Za-z0-9_-]{11}' \
  -e 'youtube-nocookie\.com/embed/[A-Za-z0-9_-]{11}' \
  "$OUT" "${EXCLUDES[@]}" 2>/dev/null \
  | grep -oE '[A-Za-z0-9_-]{11}$' \
  | bash "$HERE/transcribe-ids.sh" "$OUT/_yt-cache" $FORCE
