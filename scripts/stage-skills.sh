#!/usr/bin/env bash
# sync와 drift가 공유하는 배포 변환. 출력은 호출자가 만든 빈 임시 디렉터리뿐이다.
set -euo pipefail

if [[ $# -lt 3 ]]; then
  printf 'usage: bash stage-skills.sh SOURCE_ROOT EMPTY_STAGE SKILL...\n' >&2
  exit 2
fi
source_root="$1"
stage_root="$2"
shift 2

[[ -d "$source_root" && ! -L "$source_root" ]] || { printf 'error: invalid source root\n' >&2; exit 1; }
[[ -d "$stage_root" && ! -L "$stage_root" ]] || { printf 'error: stage must be a real, empty directory\n' >&2; exit 1; }
source_root="$(cd "$source_root" && pwd -P)"
stage_root="$(cd "$stage_root" && pwd -P)"
case "$stage_root/" in
  "$source_root/"*) printf 'error: stage must be outside source root\n' >&2; exit 1 ;;
esac
[[ -z "$(find "$stage_root" -mindepth 1 -print -quit)" ]] || { printf 'error: stage is not empty\n' >&2; exit 1; }
command -v rsync >/dev/null || { printf 'error: rsync is required\n' >&2; exit 1; }

# 복사 전에 입력 전체를 확인해 누락된 정본으로 부분 stage가 생기지 않게 한다.
for skill in "$@"; do
  [[ "$skill" =~ ^[a-z0-9][a-z0-9-]*$ ]] || { printf 'error: invalid skill name\n' >&2; exit 1; }
  [[ -d "$source_root/$skill" && ! -L "$source_root/$skill" ]] || { printf 'error: missing or linked shared skill: %s\n' "$skill" >&2; exit 1; }
  if [[ "$skill" == crawl ]]; then
    for helper in captions.py fetch-subs.sh; do
      [[ -f "$source_root/youtube/scripts/$helper" ]] || { printf 'error: missing crawl helper: %s\n' "$helper" >&2; exit 1; }
    done
  fi
done

for skill in "$@"; do
  rsync -a \
    --exclude '.env' \
    --exclude '.venv/' \
    --exclude '.git/' \
    --exclude '.cache/' \
    --exclude 'node_modules/' \
    --exclude '__pycache__/' \
    --exclude '*.pyc' \
    --exclude '.pytest_cache/' \
    --exclude '.ruff_cache/' \
    --exclude '.DS_Store' \
    --exclude '.omc/' \
    --exclude 'prompts/' \
    --exclude 'work/' \
    --exclude 'references/transcripts' \
    --exclude 'references/corrections.json' \
    "$source_root/$skill/" "$stage_root/$skill/"
done

if [[ -d "$stage_root/crawl" ]]; then
  mkdir -p "$stage_root/crawl/scripts"
  for helper in captions.py fetch-subs.sh; do
    rsync -a "$source_root/youtube/scripts/$helper" "$stage_root/crawl/scripts/$helper"
  done
fi

find "$stage_root" -type f \( -name 'SKILL.md' -o -path '*/references/*.md' \) -exec sed -i.bak \
  -e 's|\$HOME/.agents/skills/shared/|${CLAUDE_PLUGIN_ROOT}/skills/|g' \
  -e 's|~/.agents/skills/shared/|${CLAUDE_PLUGIN_ROOT}/skills/|g' {} +
find "$stage_root" -type f -name '*.bak' -delete
