#!/usr/bin/env bash
# Validate and publish one MP3 episode through GitHub Releases and Pages.
set -euo pipefail

usage() {
  echo 'usage: publish.sh --repo DIR --audio FILE --title TITLE [--desc NOTES] [--episode N] [--date RFC2822] [--dry-run]' >&2
}

REPO="" AUDIO="" TITLE="" DESC="" EP="" DATE="" DRY_RUN=false
while [ $# -gt 0 ]; do
  case "$1" in
    --repo) REPO="${2:-}"; shift 2 ;;
    --audio) AUDIO="${2:-}"; shift 2 ;;
    --title) TITLE="${2:-}"; shift 2 ;;
    --desc) DESC="${2:-}"; shift 2 ;;
    --episode) EP="${2:-}"; shift 2 ;;
    --date) DATE="${2:-}"; shift 2 ;;
    --dry-run) DRY_RUN=true; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "unknown arg: $1" >&2; usage; exit 2 ;;
  esac
done

[ -n "$REPO" ] && [ -n "$AUDIO" ] && [ -n "$TITLE" ] || { usage; exit 2; }
REPO="${REPO/#\~/$HOME}"
AUDIO="${AUDIO/#\~/$HOME}"
[ -d "$REPO/.git" ] || { echo "repo is not a git checkout: $REPO" >&2; exit 2; }
[ -f "$REPO/show.json" ] || { echo "missing show.json: $REPO" >&2; exit 2; }
[ -r "$AUDIO" ] || { echo "audio is not readable: $AUDIO" >&2; exit 2; }

for tool in git ffprobe python3; do
  command -v "$tool" >/dev/null || { echo "missing required command: $tool" >&2; exit 2; }
done
if [ "$DRY_RUN" = false ]; then
  for tool in gh curl; do
    command -v "$tool" >/dev/null || { echo "missing required command: $tool" >&2; exit 2; }
  done
fi

git -C "$REPO" diff --quiet -- feed.xml episodes.json || {
  echo "feed.xml or episodes.json has uncommitted changes; commit or stash them first" >&2
  exit 2
}
git -C "$REPO" diff --cached --quiet -- feed.xml episodes.json || {
  echo "feed.xml or episodes.json has staged changes; commit or unstage them first" >&2
  exit 2
}

ORIGIN=$(git -C "$REPO" remote get-url origin)
SLUG=$(printf '%s' "$ORIGIN" | sed -E 's#^(git@github.com:|https://github.com/)##; s#\.git$##')
[[ "$SLUG" =~ ^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$ ]] || {
  echo "origin must be a GitHub repository: $ORIGIN" >&2
  exit 2
}
OWNER="${SLUG%%/*}"
NAME="${SLUG##*/}"

if [ -z "$EP" ]; then
  EP=$(python3 - "$REPO/episodes.json" <<'PY'
import json, pathlib, sys
path = pathlib.Path(sys.argv[1])
episodes = json.loads(path.read_text()) if path.exists() else []
print(max((int(item["episode"]) for item in episodes), default=0) + 1)
PY
)
fi
[[ "$EP" =~ ^[1-9][0-9]*$ ]] || { echo "episode must be a positive integer: $EP" >&2; exit 2; }
[ -n "$DATE" ] || DATE=$(LC_ALL=C date "+%a, %d %b %Y %H:%M:%S %z")
python3 - "$DATE" <<'PY'
from email.utils import parsedate_to_datetime
import sys
try:
    value = parsedate_to_datetime(sys.argv[1])
except (TypeError, ValueError) as error:
    raise SystemExit(f"invalid RFC 2822 date: {sys.argv[1]}") from error
if value.utcoffset() is None:
    raise SystemExit("date must include a timezone")
PY

CODEC=$(ffprobe -v error -select_streams a:0 -show_entries stream=codec_name -of default=nk=1:nw=1 "$AUDIO" | head -1)
[ "$CODEC" = mp3 ] || { echo "audio must contain an MP3 stream, got: ${CODEC:-none}" >&2; exit 2; }
LEN=$(stat -f%z "$AUDIO" 2>/dev/null || stat -c%s "$AUDIO")
DUR=$(ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 "$AUDIO" | cut -d. -f1)
[[ "$DUR" =~ ^[0-9]+$ ]] || { echo "could not read audio duration: $AUDIO" >&2; exit 2; }

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TMP=$(mktemp -d)
cleanup() { /bin/rm -rf "$TMP"; }
trap cleanup EXIT
PLAN_REPO="$TMP/repo"
mkdir "$PLAN_REPO"
cp "$REPO/show.json" "$PLAN_REPO/show.json"
if [ -f "$REPO/episodes.json" ]; then
  cp "$REPO/episodes.json" "$PLAN_REPO/episodes.json"
else
  printf '[]\n' > "$PLAN_REPO/episodes.json"
fi

TAG="ep$EP"
ASSET="$TMP/$TAG.mp3"
cp "$AUDIO" "$ASSET"
URL="https://github.com/$OWNER/$NAME/releases/download/$TAG/$TAG.mp3"
python3 - "$PLAN_REPO/episodes.json" "$TITLE" "$DESC" "$URL" "$LEN" "$DUR" "$DATE" "$EP" "$OWNER" "$NAME" <<'PY'
import json, pathlib, sys
from email.utils import parsedate_to_datetime

path = pathlib.Path(sys.argv[1])
title, description, url, length, duration, date = sys.argv[2:8]
episode_number = int(sys.argv[8])
owner, repo = sys.argv[9:11]
episodes = json.loads(path.read_text())
existing = next((item for item in episodes if int(item.get("episode", 0)) == episode_number), None)
guid = existing.get("guid") if existing else None
if not guid:
    year = parsedate_to_datetime(date).year
    guid = f"tag:github.com,{year}:{owner}/{repo}:episode:{episode_number}"
episodes = [item for item in episodes if int(item.get("episode", 0)) != episode_number]
episodes.append({
    "title": title,
    "description": description,
    "audio_url": url,
    "length": int(length),
    "duration": int(duration),
    "pubDate": date,
    "guid": guid,
    "episode": episode_number,
})
path.write_text(json.dumps(episodes, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
PY
python3 "$SCRIPT_DIR/gen_feed.py" --repo "$PLAN_REPO"

if [ "$DRY_RUN" = true ]; then
  echo "[publish] dry-run OK: $SLUG $TAG, ${LEN} bytes, ${DUR}s"
  exit 0
fi

gh auth status >/dev/null
gh repo view "$SLUG" >/dev/null
if gh release view "$TAG" --repo "$SLUG" >/dev/null 2>&1; then
  gh release upload "$TAG" "$ASSET" --repo "$SLUG" --clobber
  gh release edit "$TAG" --repo "$SLUG" --title "$TITLE" --notes "$DESC"
else
  gh release create "$TAG" "$ASSET" --repo "$SLUG" --title "$TITLE" --notes "$DESC"
fi

HTTP_CODE=$(curl -L -sS -o /dev/null -r 0-1 -w '%{http_code}' "$URL")
[ "$HTTP_CODE" = 206 ] || { echo "release asset byte-range check failed: HTTP $HTTP_CODE" >&2; exit 1; }
REMOTE_LEN=$(curl -L -sSI "$URL" | awk 'tolower($1)=="content-length:" {gsub("\r", "", $2); value=$2} END {print value}')
[ "$REMOTE_LEN" = "$LEN" ] || { echo "release asset size mismatch: local=$LEN remote=$REMOTE_LEN" >&2; exit 1; }

cp "$PLAN_REPO/episodes.json" "$REPO/episodes.json"
cp "$PLAN_REPO/feed.xml" "$REPO/feed.xml"
git -C "$REPO" add episodes.json feed.xml
if git -C "$REPO" diff --cached --quiet; then
  echo "[publish] release updated; feed metadata unchanged"
else
  git -C "$REPO" commit -m "publish: $TAG - $TITLE"
fi
git -C "$REPO" push
echo "[publish] done: $URL"
