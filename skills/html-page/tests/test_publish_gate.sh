#!/usr/bin/env bash
# publish-gate.sh 회귀 검사: 미등록 산출물은 block, 등록된 현재 revision은 통과, 등록 뒤 수정은 다시 block.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
skill="$(dirname "$here")"
hook="$skill/scripts/publish-gate.sh"
tmp="$(mktemp -d "${TMPDIR:-/tmp}/publish-gate.XXXXXX")"
trap 'test -n "$tmp" && /bin/rm -rf -- "$tmp"' EXIT
export HTML_REPLY_STATE_DIR="$tmp/state" HTML_ARTIFACTS_DIR="$tmp/artifacts" HTML_TMP_DIR="$tmp/html-pages" HTML_PUBLISH_CMD="publish-cmd"
mkdir -p "$HTML_REPLY_STATE_DIR" "$HTML_ARTIFACTS_DIR" "$HTML_TMP_DIR"
session="11111111-2222-3333-4444-555555555555"
page="$HTML_ARTIFACTS_DIR/261101-claude-code-$session-sample.html"
printf '<!doctype html><title>t</title><p>one</p>\n' > "$page"
payload="$(jq -n --arg s "$session" '{session_id: $s, transcript_path: "", stop_hook_active: false}')"

out="$(printf '%s' "$payload" | bash "$hook")"
[ "$(jq -r .decision <<<"$out")" = "block" ] || { echo "FAIL: unpublished page must block"; echo "$out"; exit 1; }
grep -q "publish-cmd" <<<"$out" || { echo "FAIL: block reason must name the publish command"; exit 1; }

# stop_hook_active면 다시 막지 않는다(무한 루프 방지)
out="$(printf '%s' "$payload" | jq '.stop_hook_active=true' | bash "$hook")"
[ -z "$out" ] || { echo "FAIL: stop_hook_active must pass"; exit 1; }

# 현재 revision으로 등록하면 통과
python3 - "$skill/scripts/reply-bridge.py" "$HTML_REPLY_STATE_DIR" "$page" <<'PY'
import importlib.util, sys
spec = importlib.util.spec_from_file_location("reply_bridge", sys.argv[1])
module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
module.Store(sys.argv[2]).register(sys.argv[3], "sample", "claude", "conv", "default")
PY
out="$(printf '%s' "$payload" | bash "$hook")"
[ -z "$out" ] || { echo "FAIL: registered current revision must pass"; echo "$out"; exit 1; }

# 등록 뒤 수정하면 다시 막는다
printf '<!doctype html><title>t</title><p>two</p>\n' > "$page"
out="$(printf '%s' "$payload" | bash "$hook")"
[ "$(jq -r .decision <<<"$out")" = "block" ] || { echo "FAIL: edited page after registration must block"; exit 1; }

# 전사의 Write 경로도 후보로 잡는다(파일명에 세션 ID가 없을 때)
other="$HTML_ARTIFACTS_DIR/261101-claude-code-other.html"
printf '<!doctype html><title>o</title>\n' > "$other"
transcript="$tmp/transcript.jsonl"
jq -nc --arg p "$other" '{type:"assistant", message:{content:[{type:"tool_use", name:"Write", input:{file_path:$p}}]}}' > "$transcript"
printf '<!doctype html><title>t</title><p>two</p>\n' > "$page"
python3 - "$skill/scripts/reply-bridge.py" "$HTML_REPLY_STATE_DIR" "$page" <<'PY'
import importlib.util, sys
spec = importlib.util.spec_from_file_location("reply_bridge", sys.argv[1])
module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
module.Store(sys.argv[2]).register(sys.argv[3], "sample", "claude", "conv", "default")
PY
out="$(printf '%s' "$payload" | jq --arg t "$transcript" '.transcript_path=$t' | bash "$hook")"
grep -q "$other" <<<"$out" || { echo "FAIL: transcript Write path must be a candidate"; echo "$out"; exit 1; }
# 임시 페이지 경로: 최근에 만든 미등록 파일은 막고, 오래된 파일과 등록된 파일은 통과
ephemeral="$HTML_TMP_DIR/pick-one.html"
printf '<!doctype html><title>e</title>\n' > "$ephemeral"
stale="$HTML_TMP_DIR/old.html"
printf '<!doctype html><title>s</title>\n' > "$stale"; touch -t 202001010000 "$stale"
out="$(printf '%s' "$payload" | bash "$hook")"
grep -q "$ephemeral" <<<"$out" || { echo "FAIL: recent tmp page must block"; echo "$out"; exit 1; }
grep -q "$stale" <<<"$out" && { echo "FAIL: stale tmp page must not be a candidate"; exit 1; }
python3 - "$skill/scripts/reply-bridge.py" "$HTML_REPLY_STATE_DIR" "$ephemeral" <<'REG'
import importlib.util, sys
spec = importlib.util.spec_from_file_location("reply_bridge", sys.argv[1])
module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
module.Store(sys.argv[2]).register(sys.argv[3], "pick", "claude", "conv", "default")
REG
out="$(printf '%s' "$payload" | bash "$hook")"
grep -q "pick-one" <<<"$out" && { echo "FAIL: registered tmp page must pass"; echo "$out"; exit 1; }
# 안전하지 않은 이름과 다른 사용자가 쓸 수 있는 폴더는 후보에서 뺀다
printf '<!doctype html>\n' > "$HTML_TMP_DIR/inject\"name.html"
out="$(printf '%s' "$payload" | bash "$hook")"
grep -q 'inject' <<<"$out" && { echo "FAIL: unsafe filename must be excluded"; echo "$out"; exit 1; }
chmod 0777 "$HTML_TMP_DIR"
printf '<!doctype html><title>w</title>\n' > "$HTML_TMP_DIR/world-writable.html"
out="$(printf '%s' "$payload" | bash "$hook")"
grep -q "world-writable" <<<"$out" && { echo "FAIL: group/other-writable tmp dir must be skipped"; echo "$out"; exit 1; }
chmod 0700 "$HTML_TMP_DIR"
echo "ok: publish-gate"
