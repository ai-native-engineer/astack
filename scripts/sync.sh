#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
AGENTS_ROOT="${AGENTS_ROOT:-$HOME/.agents}"
SOURCE_ROOT="$AGENTS_ROOT/skills/shared"
VALIDATORS="$SOURCE_ROOT/skill-manager/scripts"
SKILLS=(
  agent-team
  chrome-devtools-cli
  company-context-research
  communication
  context7-cli
  crawl
  data-go-kr
  ffmpeg
  find-skills
  goal-plan
  html-explainer
  humanize-korean
  imessage
  kakaotalk
  meta-ads-cli
  ocr
  oss-explore
  podcast
  project-collect
  project-organize
  session-history
  similarweb
  stt
  tts
  video-cut-editor
  voice-memos
)

command -v rsync >/dev/null || { echo "error: rsync is required" >&2; exit 1; }
[[ -d "$SOURCE_ROOT" && ! -L "$SOURCE_ROOT" ]] || { echo "error: invalid shared source: $SOURCE_ROOT" >&2; exit 1; }
[[ ! -L "$ROOT/skills" ]] || { echo "error: generated skills directory is a symlink: $ROOT/skills" >&2; exit 1; }
for validator in quick_validate.py lint_skill_authoring.py; do
  [[ -f "$VALIDATORS/$validator" ]] || { echo "error: missing validator: $VALIDATORS/$validator" >&2; exit 1; }
done
stage="$(mktemp -d "${TMPDIR:-/tmp}/astack-sync.XXXXXX")"
trap 'rm -rf "$stage"' EXIT
mkdir -p "$stage/skills"

for skill in "${SKILLS[@]}"; do
  source="$SOURCE_ROOT/$skill"
  [[ -d "$source" ]] || { echo "error: missing shared skill: $source" >&2; exit 1; }
  link="$(find "$source" \
    \( -path "$source/references/transcripts" -o -path "$source/references/corrections.json" \) -prune \
    -o \( -type d \( -name .venv -o -name .git -o -name node_modules -o -name __pycache__ -o -name .cache \) \) -prune \
    -o -type l -print -quit)"
  [[ ! -L "$source" && -z "$link" ]] || { echo "error: symlink in shared skill: ${link:-$source}" >&2; exit 1; }
  python3 "$VALIDATORS/quick_validate.py" "$source"
  python3 "$VALIDATORS/lint_skill_authoring.py" "$source"
  rsync -a \
    --exclude '.env' \
    --exclude '.venv/' \
    --exclude '.git/' \
    --exclude '.cache/' \
    --exclude 'node_modules/' \
    --exclude '__pycache__/' \
    --exclude '*.pyc' \
    --exclude '.DS_Store' \
    --exclude '.omc/' \
    --exclude 'prompts/' \
    --exclude 'work/' \
    --exclude 'references/transcripts' \
    --exclude 'references/corrections.json' \
    "$source/" "$stage/skills/$skill/"
done

find "$stage/skills" -type f \( -name 'SKILL.md' -o -path '*/references/*.md' \) -exec sed -i.bak \
  's|~/.agents/skills/shared/|${CLAUDE_PLUGIN_ROOT}/skills/|g' {} +
find "$stage/skills" -type f -name '*.bak' -delete
privacy_hits="$(rg --pcre2 -n --hidden \
  '(?<![A-Za-z0-9-])(sk-|ghp_|gho_|github_pat_|xox[bp]-)[A-Za-z0-9_-]{8,}|/Users/[^/[:space:]]+' \
  "$stage/skills" || true)"
voice_hits="$(find "$stage/skills" -type f -path '*/voices/*' \
  \( -name '*.aac' -o -name '*.flac' -o -name '*.m4a' -o -name '*.mp3' \
     -o -name '*.ogg' -o -name '*.opus' -o -name '*.wav' \) -print)"
email_hits=""
while IFS= read -r file; do
  [[ -n "$file" ]] || continue
  if head -n 5 "$file" | grep -Fq 'lint-skip: env-values'; then
    continue
  fi
  matches="$(rg --pcre2 -n --with-filename \
    '\b(?!git@github\.com\b)[A-Za-z0-9._%+-]+@(?!example\.)[A-Za-z0-9.-]+\.[A-Za-z]{2,}' \
    "$file" || true)"
  [[ -z "$matches" ]] || email_hits+="${email_hits:+$'\n'}$matches"
done < <(rg --pcre2 -l --hidden \
  '\b(?!git@github\.com\b)[A-Za-z0-9._%+-]+@(?!example\.)[A-Za-z0-9.-]+\.[A-Za-z]{2,}' \
  "$stage/skills" || true)
if [[ -n "$privacy_hits$email_hits$voice_hits" ]]; then
  [[ -z "$privacy_hits" ]] || printf '%s\n' "$privacy_hits"
  [[ -z "$email_hits" ]] || printf '%s\n' "$email_hits"
  [[ -z "$voice_hits" ]] || printf '%s\n' "$voice_hits"
  echo "error: publishability check failed; fix the shared source" >&2
  exit 1
fi
rsync -a --delete "$stage/skills/" "$ROOT/skills/"
python3 "$ROOT/tests/test_repository.py"
echo "synced: ${SKILLS[*]}"
