#!/usr/bin/env bash
# Unit tests for the harness-side completion sentinels:
# zdel-notify (codex notify, argv payload) and zdel-notify-claude (claude Stop hook, stdin payload).
set -euo pipefail
SCRIPTS="$(cd "$(dirname "${BASH_SOURCE[0]}")/../scripts" && pwd)"
fail() { printf 'FAIL: %s\n' "$1" >&2; exit 1; }

D="$(mktemp -d)"
trap '/bin/rm -rf -- "$D"' EXIT

# --- zdel-notify (codex) ---
printf '1\n' > "$D/turn"
"$SCRIPTS/zdel-notify" "$D" '{"type":"other"}'
[ ! -e "$D/turn-1.done" ] || fail "codex: touched on wrong event type"
"$SCRIPTS/zdel-notify" "$D" '{"type":"agent-turn-complete","last-assistant-message":"chat answer"}'
[ -f "$D/turn-1.done" ] || fail "codex: no done file"
grep -q 'chat answer' "$D/turn-1.md" || fail "codex: fallback result missing"
printf '2\n' > "$D/turn"; printf 'model-own\n' > "$D/turn-2.md"
"$SCRIPTS/zdel-notify" "$D" '{"type":"agent-turn-complete","last-assistant-message":"must not overwrite"}'
grep -q 'model-own' "$D/turn-2.md" || fail "codex: overwrote model-written result"
[ -f "$D/turn-2.done" ] || fail "codex: no done file when result pre-existed"
"$SCRIPTS/zdel-notify" "/nonexistent-zdel-dir" '{"type":"agent-turn-complete"}' || fail "codex: stopped worker not a no-op"

# --- zdel-notify-claude ---
T="$D/transcript.jsonl"
printf '%s\n' \
  '{"type":"user","message":{"content":"q"}}' \
  '{"type":"assistant","message":{"content":[{"type":"text","text":"first partial"}]}}' \
  '{"type":"assistant","message":{"content":[{"type":"thinking","thinking":"x"},{"type":"text","text":"last answer"}]}}' > "$T"
printf '3\n' > "$D/turn"
printf '{"hook_event_name":"SessionEnd"}' | "$SCRIPTS/zdel-notify-claude" "$D"
[ ! -e "$D/turn-3.done" ] || fail "claude: touched on wrong event"
printf '{"hook_event_name":"Stop","transcript_path":"%s"}' "$T" | "$SCRIPTS/zdel-notify-claude" "$D"
[ -f "$D/turn-3.done" ] || fail "claude: no done file"
grep -q 'last answer' "$D/turn-3.md" || fail "claude: fallback should use last assistant text"
if grep -q 'first partial' "$D/turn-3.md"; then fail "claude: fallback used stale assistant text"; fi
printf '4\n' > "$D/turn"; printf 'model-own\n' > "$D/turn-4.md"
printf '{"hook_event_name":"Stop","transcript_path":"%s"}' "$T" | "$SCRIPTS/zdel-notify-claude" "$D"
grep -q 'model-own' "$D/turn-4.md" || fail "claude: overwrote model-written result"
printf '{"hook_event_name":"Stop"}' | "$SCRIPTS/zdel-notify-claude" "/nonexistent-zdel-dir" || fail "claude: stopped worker not a no-op"

printf 'zdel notify tests passed\n'
