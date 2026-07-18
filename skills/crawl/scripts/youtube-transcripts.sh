#!/bin/bash
# 미러 페이지에 포함된 YouTube 링크의 자막을 youtube-digest 방식으로 추출해 <out>/_yt-cache/<ID>.md 로 저장.
# ID 수집(rg)만 여기서 하고, 전사 루프(429 백오프·자막없음 stub·증분 skip)는 transcribe-ids.sh 와 공유한다.
# 증분: 기존 <out>/_yt-cache/<ID>.md 는 skip. --force 로 전체 재추출.
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
