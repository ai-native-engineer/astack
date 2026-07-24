#!/usr/bin/env bash
# Completion ownership tests for zdel and its Codex/Claude hooks.
set -euo pipefail
SCRIPTS="$(cd "$(dirname "${BASH_SOURCE[0]}")/../scripts" && pwd)"
fail() { printf 'FAIL: %s\n' "$1" >&2; exit 1; }

D="$(mktemp -d)"
trap '/bin/rm -rf -- "$D"' EXIT

MOCK_BIN="$D/bin"
LOG="$D/zellij.log"
STATE="$D/state"
mkdir -p "$MOCK_BIN"
printf '%s\n' \
  '#!/usr/bin/env bash' \
  'printf '\''%q '\'' "$@" >> "$ZDEL_TEST_LOG"' \
  'printf '\''\n'\'' >> "$ZDEL_TEST_LOG"' \
  'if [ "${1:-}" = run ]; then printf '\''terminal_1\n'\''; fi' \
  >"$MOCK_BIN/zellij"
chmod +x "$MOCK_BIN/zellij"

run_zdel() {
  env PATH="$MOCK_BIN:$PATH" ZDEL_BASE="$STATE" ZELLIJ_SESSION_NAME=test ZDEL_TEST_LOG="$LOG" "$SCRIPTS/zdel" "$@"
}

# Codex/Claude hooks are the sole completion owner; generic commands keep the prompt contract.
run_zdel start codex-worker "first task" -- codex >/dev/null
[ "$(sed -n '1p' "$STATE/test/codex-worker/completion-mode")" = hook ] || fail "codex: wrong completion mode"
grep -q 'zdel-notify' "$LOG" || fail "codex: notify hook not installed"
if grep -q 'turn-1.md' "$LOG"; then fail "codex: prompt also owns completion"; fi

: >"$LOG"
run_zdel start claude-worker "first task" -- claude >/dev/null
[ "$(sed -n '1p' "$STATE/test/claude-worker/completion-mode")" = hook ] || fail "claude: wrong completion mode"
grep -q 'zdel-notify' "$LOG" || fail "claude: Stop hook not installed"
if grep -q 'turn-1.md' "$LOG"; then fail "claude: prompt also owns completion"; fi

: >"$LOG"
run_zdel start shell-worker "first task" -- bash >/dev/null
[ "$(sed -n '1p' "$STATE/test/shell-worker/completion-mode")" = prompt ] || fail "generic: wrong completion mode"
grep -q 'turn-1.md' "$LOG" || fail "generic: completion prompt missing"

# A new turn cannot claim the mutable turn pointer before the previous hook finishes.
if run_zdel send codex-worker "too soon" >"$D/send.out" 2>&1; then
  fail "send: advanced before previous completion"
fi
grep -q 'still running' "$D/send.out" || fail "send: missing unfinished-turn error"
[ "$(sed -n '1p' "$STATE/test/codex-worker/turn")" = 1 ] || fail "send: changed turn after rejection"

CODEX_DIR="$STATE/test/codex-worker"
"$SCRIPTS/zdel-notify" "$CODEX_DIR" '{"type":"other"}'
[ ! -e "$CODEX_DIR/turn-1.done" ] || fail "codex: touched on wrong event type"
"$SCRIPTS/zdel-notify" "$CODEX_DIR" '{"type":"agent-turn-complete","last-assistant-message":"turn one"}'
[ -f "$CODEX_DIR/turn-1.done" ] || fail "codex: no done file"
grep -q 'turn one' "$CODEX_DIR/turn-1.md" || fail "codex: result missing"

: >"$LOG"
run_zdel send codex-worker "second task" >/dev/null
[ "$(sed -n '1p' "$CODEX_DIR/turn")" = 2 ] || fail "send: did not advance completed turn"
if grep -q 'turn-2.md' "$LOG"; then fail "send: hook worker prompt also owns completion"; fi
"$SCRIPTS/zdel-notify" "$CODEX_DIR" '{"type":"agent-turn-complete","last-assistant-message":"turn two"}'
grep -q 'turn two' "$CODEX_DIR/turn-2.md" || fail "codex: second turn result missing"

# Claude uses the Stop payload's final message, not a possibly stale transcript entry.
CLAUDE_DIR="$STATE/test/claude-worker"
printf '{"hook_event_name":"SessionEnd","last_assistant_message":"wrong"}' | "$SCRIPTS/zdel-notify" "$CLAUDE_DIR"
[ ! -e "$CLAUDE_DIR/turn-1.done" ] || fail "claude: touched on wrong event"
printf '{"hook_event_name":"Stop","transcript_path":"stale","last_assistant_message":"current answer"}' | "$SCRIPTS/zdel-notify" "$CLAUDE_DIR"
[ -f "$CLAUDE_DIR/turn-1.done" ] || fail "claude: no done file"
grep -q 'current answer' "$CLAUDE_DIR/turn-1.md" || fail "claude: direct result missing"

"$SCRIPTS/zdel-notify" "/nonexistent-zdel-dir" '{"type":"agent-turn-complete"}' || fail "codex: stopped worker not a no-op"
printf '{"hook_event_name":"Stop"}' | "$SCRIPTS/zdel-notify" "/nonexistent-zdel-dir" || fail "claude: stopped worker not a no-op"

printf 'zdel notify tests passed\n'
