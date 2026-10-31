#!/usr/bin/env bash
# Stop 훅(Claude Code): 이 세션이 $TMPDIR/html-pages/ 또는 ~/.agents/artifacts/에 만든 HTML 중 회신 서비스에 현재 내용으로
# 등록되지 않은 파일이 있으면 턴 종료를 막고 publish를 요구한다. 산출물을 열어만 두고 끝내면
# 사용자는 패널에서 바로 보낼 수 없고 복사해 붙여 넣어야 하는데, 그 단계는 매번 빠진다.
# 세션 식별은 파일명 규약(YYMMDD-<harness>-<session-id>-<name>.html)과 전사의 Write/Edit 경로를 함께 쓴다.
# 테스트용 env: HTML_REPLY_STATE_DIR, HTML_ARTIFACTS_DIR, HTML_TMP_DIR, HTML_PUBLISH_CMD.
set -uo pipefail
command -v jq >/dev/null 2>&1 || exit 0
command -v python3 >/dev/null 2>&1 || exit 0

payload="$(cat)"
[ "$(jq -r '.stop_hook_active // false' <<<"$payload")" = "true" ] && exit 0
session="$(jq -r '.session_id // empty' <<<"$payload")"
transcript="$(jq -r '.transcript_path // empty' <<<"$payload")"
[ -n "$session" ] || exit 0

state="${HTML_REPLY_STATE_DIR:-$HOME/.agents/artifacts/.html-page-replies}"
artifacts="${HTML_ARTIFACTS_DIR:-$HOME/.agents/artifacts}"
# 임시 경로는 사용자 전용이어야 한다. 공용 /tmp로는 내려가지 않고, 내 소유가 아니거나
# 다른 사용자가 쓸 수 있는 폴더는 후보에서 뺀다. 훅 출력은 모델 컨텍스트로 들어가므로
# 남이 놓은 파일 이름이 섞이면 안 된다.
tmp_pages="${HTML_TMP_DIR:-${TMPDIR:-$HOME/.cache}/html-pages}"
private_dir() {
  [ -d "$1" ] || return 1
  [ -O "$1" ] || return 1
  case "$(stat -f '%Lp' "$1" 2>/dev/null || stat -c '%a' "$1" 2>/dev/null)" in
    *[2367]?|*[2367]) return 1 ;;
  esac
  return 0
}
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
publish_cmd="${HTML_PUBLISH_CMD:-python3 $here/reply-bridge.py --state-dir $state publish}"

candidates=""
for root in "$artifacts" "$tmp_pages"; do
  private_dir "$root" || continue
  # 아티팩트는 파일명에 세션 ID가 들어간다. 임시 페이지는 이름 규약이 없어 최근 12시간 안에 바뀐
  # 파일을 모두 본다. 다른 세션의 미등록 임시 페이지도 잡히지만 그것도 publish 대상이다.
  found="$(find "$root" -maxdepth 1 -type f -user "$(id -u)" -name "*${session}*.html" 2>/dev/null)"
  if [ "$root" = "$tmp_pages" ]; then
    found="$(printf '%s\n%s\n' "$found" "$(find "$root" -maxdepth 1 -type f -user "$(id -u)" -name "*.html" -mmin -720 2>/dev/null)")"
  fi
  candidates="$(printf '%s\n%s\n' "$candidates" "$found")"
  if [ -n "$transcript" ] && [ -f "$transcript" ]; then
    from_transcript="$(jq -r --arg d "$root/" '
      select(.type=="assistant") | .message.content[]? | select(.type=="tool_use")
      | select(.name=="Write" or .name=="Edit") | .input.file_path // empty
      | select(startswith($d)) | select(endswith(".html"))' "$transcript" 2>/dev/null)"
    candidates="$(printf '%s\n%s\n' "$candidates" "$from_transcript")"
  fi
done
# 파일 이름은 안전한 문자만 허용한다. 제어 문자나 따옴표가 든 이름은 후보에서 빼고 훅 출력에 싣지 않는다.
candidates="$(printf '%s\n' "$candidates" | sed '/^$/d' | LC_ALL=C grep -E '^[A-Za-z0-9._/ -]+\.html$' | sort -u)"
[ -n "$candidates" ] || exit 0

# 등록 여부는 경로와 현재 내용의 sha256이 artifacts 테이블의 revision과 같은지로 본다.
# 등록 뒤 고친 파일은 옛 revision으로만 남아 있어 다시 publish해야 한다.
unpublished="$(CANDIDATES="$candidates" python3 -I -c '
import hashlib, os, sqlite3, sys
from pathlib import Path
db_path = Path(sys.argv[1])
rows = set()
if db_path.is_file():
    try:
        with sqlite3.connect(f"file:{db_path}?mode=ro", uri=True) as db:
            rows = {(p, r) for p, r in db.execute("SELECT path, revision FROM artifacts")}
    except sqlite3.Error:
        rows = set()
for line in os.environ.get("CANDIDATES", "").splitlines():
    path = line.strip()
    if not path:
        continue
    try:
        text = Path(path).read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        continue
    if (str(Path(path).resolve()), hashlib.sha256(text.encode()).hexdigest()) not in rows:
        print(path)
' "$state/replies.sqlite3")"
[ -n "$unpublished" ] || exit 0

jq -n --arg files "$unpublished" --arg cmd "$publish_cmd" '{
  decision: "block",
  reason: ("아직 회신 서비스에 등록되지 않은 HTML 산출물이 있다. 사용자가 패널에서 바로 보낼 수 있게 각 파일을 publish하고 그 URL을 알린 뒤 끝낸다.\n" + $files + "\n실행: " + $cmd + " <file.html>")
}'
exit 0
