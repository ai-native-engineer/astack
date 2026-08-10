#!/usr/bin/env bash
set -euo pipefail

TEST_DIR="$(mktemp -d "${TMPDIR:-/tmp}/stt-fallback-test.XXXXXXXX")"
trap '/bin/rm -rf -- "$TEST_DIR"' EXIT

SCRIPT_DIR="$(cd "$(dirname "$0")/../scripts" && pwd)"
AUDIO="$TEST_DIR/audio.m4a"
APPLE_OK="$TEST_DIR/apple-ok"
APPLE_FAIL="$TEST_DIR/apple-fail"
FFMPEG_FAKE="$TEST_DIR/ffmpeg"
HANDY_FAKE="$TEST_DIR/handy"
touch "$AUDIO"

cat > "$APPLE_OK" <<'SH'
#!/usr/bin/env bash
printf '%s\n' 'apple result'
SH
cat > "$APPLE_FAIL" <<'SH'
#!/usr/bin/env bash
echo 'synthetic apple failure' >&2
exit 70
SH
cat > "$FFMPEG_FAKE" <<'SH'
#!/usr/bin/env bash
for output; do :; done
touch "$output"
SH
cat > "$HANDY_FAKE" <<'SH'
#!/usr/bin/env bash
[ "$1" = "--transcribe-file" ]
[ -f "$2" ]
printf '%s\n' 'qwen result'
SH
chmod +x "$APPLE_OK" "$APPLE_FAIL" "$FFMPEG_FAKE" "$HANDY_FAKE"

result="$(
  APPLE_STT_BIN="$APPLE_OK" \
  FFMPEG_BIN="$FFMPEG_FAKE" \
  HANDY_BIN="$HANDY_FAKE" \
  bash "$SCRIPT_DIR/stt-fallback.sh" "$AUDIO"
)"
[ "$result" = "apple result" ]

result="$(
  APPLE_STT_BIN="$APPLE_FAIL" \
  FFMPEG_BIN="$FFMPEG_FAKE" \
  HANDY_BIN="$HANDY_FAKE" \
  bash "$SCRIPT_DIR/stt-fallback.sh" "$AUDIO" 2> "$TEST_DIR/fallback.err"
)"
[ "$result" = "qwen result" ]
rg -q "apple-stt failed; using Handy's selected local model" "$TEST_DIR/fallback.err"
rg -q 'synthetic apple failure' "$TEST_DIR/fallback.err"

set +e
bash "$SCRIPT_DIR/stt-fallback.sh" "$TEST_DIR/missing.m4a" >/dev/null 2>&1
status=$?
set -e
[ "$status" -eq 66 ]

printf '%s\n' 'test_fallback: ok'
