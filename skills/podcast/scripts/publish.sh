#!/usr/bin/env bash
# Publish one podcast episode: upload audio to a GitHub Release, update
# episodes.json, regenerate feed.xml, commit & push. Spotify/Apple pull the
# updated RSS automatically. Requires: gh (authed), ffprobe, python3.
#
# Usage:
#   publish.sh --repo <dir> --audio <mp3> --title "..." --desc "..." [--episode N] [--date "RFC822"]
set -euo pipefail

REPO="" AUDIO="" TITLE="" DESC="" EP="" DATE=""
while [ $# -gt 0 ]; do
  case "$1" in
    --repo) REPO="$2"; shift 2;;
    --audio) AUDIO="$2"; shift 2;;
    --title) TITLE="$2"; shift 2;;
    --desc) DESC="$2"; shift 2;;
    --episode) EP="$2"; shift 2;;
    --date) DATE="$2"; shift 2;;
    *) echo "unknown arg: $1" >&2; exit 1;;
  esac
done
[ -n "$REPO" ] && [ -n "$AUDIO" ] && [ -n "$TITLE" ] || { echo "need --repo --audio --title" >&2; exit 1; }
REPO="${REPO/#\~/$HOME}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

SLUG=$(git -C "$REPO" remote get-url origin | sed -E 's#.*github.com[:/]##; s#\.git$##')
OWNER="${SLUG%%/*}"; NAME="${SLUG##*/}"

EPCOUNT=$(python3 -c "import json,os;p=os.path.join('$REPO','episodes.json');print(len(json.load(open(p))) if os.path.exists(p) else 0)")
[ -n "$EP" ] || EP=$((EPCOUNT+1))
TAG="ep$EP"

TMP=$(mktemp -d); ASSET="$TMP/ep$EP.mp3"; cp "$AUDIO" "$ASSET"
LEN=$(stat -f%z "$ASSET" 2>/dev/null || stat -c%s "$ASSET")
DUR=$(ffprobe -v error -show_entries format=duration -of default=nk=1:nw=1 "$ASSET" | cut -d. -f1)
[ -n "$DATE" ] || DATE=$(LC_ALL=C date "+%a, %d %b %Y %H:%M:%S %z")   # RFC-822 (영문 로케일 강제)

if gh release view "$TAG" --repo "$OWNER/$NAME" >/dev/null 2>&1; then
  gh release upload "$TAG" "$ASSET" --repo "$OWNER/$NAME" --clobber
else
  gh release create "$TAG" "$ASSET" --repo "$OWNER/$NAME" --title "$TITLE" --notes "$DESC"
fi
URL="https://github.com/$OWNER/$NAME/releases/download/$TAG/ep$EP.mp3"

python3 - "$REPO" "$TITLE" "$DESC" "$URL" "$LEN" "$DUR" "$DATE" "$EP" <<'PY'
import json, sys, os
repo, title, desc, url, length, dur, date, ep = sys.argv[1:9]
p = os.path.join(repo, 'episodes.json')
eps = json.load(open(p)) if os.path.exists(p) else []
eps = [e for e in eps if e.get('episode') != int(ep)]   # replace same-numbered ep
eps.append({"title": title, "description": desc, "audio_url": url, "length": int(length),
            "duration": int(dur), "pubDate": date, "guid": url, "episode": int(ep)})
json.dump(eps, open(p, 'w'), ensure_ascii=False, indent=2)
print(f"[publish] episode {ep}: {length} bytes, {dur}s")
PY

python3 "$SCRIPT_DIR/gen_feed.py" --repo "$REPO"
git -C "$REPO" add feed.xml episodes.json
git -C "$REPO" commit -q -m "publish: ep$EP — $TITLE"
git -C "$REPO" push -q
rm -rf "$TMP"
echo "[publish] done → $URL"
echo "[publish] feed will refresh at GitHub Pages; Spotify/Apple re-poll within ~minutes-hours"
