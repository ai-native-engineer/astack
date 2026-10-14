#!/usr/bin/env bash
set -euo pipefail

TEST_DIR="$(mktemp -d "${TMPDIR:-/tmp}/stt-diarize-test.XXXXXXXX")"
trap 'rm -r -- "$TEST_DIR"' EXIT

APPLE_FAKE="$TEST_DIR/apple-stt"
PYANNOTE_FAKE="$TEST_DIR/pyannote-python"
FFMPEG_FAKE="$TEST_DIR/ffmpeg"
PYANNOTE_LOG="$TEST_DIR/pyannote.log"
FFMPEG_LOG="$TEST_DIR/ffmpeg.log"
AUDIO="$TEST_DIR/audio.m4a"
touch "$AUDIO"

cat > "$APPLE_FAKE" <<'SH'
#!/usr/bin/env bash
printf '%s\n' '[{"start":0.0,"end":4.0,"text":"첫 번째 두 번째"}]'
SH

cat > "$PYANNOTE_FAKE" <<'SH'
#!/usr/bin/env bash
set -euo pipefail
[[ "$1" == */pyannote-diarize.py ]] || exit 70
shift
[ "${1:-}" != "--check" ] || exit 0
printf '%s\n' "diarize" >> "$PYANNOTE_LOG"
while [ "$#" -gt 0 ]; do
  case "$1" in
    --rttm-path) rttm_path="$2"; shift 2 ;;
    *) shift ;;
  esac
done
if [ "${PYANNOTE_DELAY:-0}" = "1" ]; then
  : > "$PYANNOTE_READY"
  sleep 0.2
fi
cat > "$rttm_path" <<'RTTM'
SPEAKER audio 1 0.0 2.0 <NA> <NA> SPEAKER_00 <NA> <NA>
SPEAKER audio 1 2.0 2.0 <NA> <NA> SPEAKER_01 <NA> <NA>
RTTM
SH

cat > "$FFMPEG_FAKE" <<'SH'
#!/usr/bin/env bash
printf '%s\n' "$@" > "$FFMPEG_LOG"
SH

chmod +x "$APPLE_FAKE" "$PYANNOTE_FAKE" "$FFMPEG_FAKE"
export PYANNOTE_LOG FFMPEG_LOG

SCRIPT_DIR="$(cd "$(dirname "$0")/../scripts" && pwd)"
OUTPUT="$(
  STT_OUT="$TEST_DIR/out" \
  APPLE_STT_BIN="$APPLE_FAKE" \
  PYANNOTE_PYTHON="$PYANNOTE_FAKE" \
  bash "$SCRIPT_DIR/stt_diarize.sh" "$AUDIO"
)"

[ -f "$OUTPUT" ]
[ -f "$(dirname "$OUTPUT")/diar.rttm" ]
rg -q '\*\*\[mixed\]\*\*' "$OUTPUT"
[ "$(wc -l < "$PYANNOTE_LOG" | tr -d ' ')" = "1" ]
[ "$(sed -n '1p' "$PYANNOTE_LOG")" = "diarize" ]

FAILURES=0
TRIM_OUTPUT="$(
  PATH="$TEST_DIR:$PATH" \
  STT_OUT="$TEST_DIR/trim-out" \
  APPLE_STT_BIN="$APPLE_FAKE" \
  PYANNOTE_PYTHON="$PYANNOTE_FAKE" \
  bash "$SCRIPT_DIR/stt_diarize.sh" "$AUDIO" 30 40
)"
[ -f "$TRIM_OUTPUT" ]
for expected in '6:-to' '7:40' '8:-i' "9:$AUDIO"; do
  line="${expected%%:*}"
  value="${expected#*:}"
  actual="$(sed -n "${line}p" "$FFMPEG_LOG")"
  if [ "$actual" != "$value" ]; then
    printf 'ffmpeg arg %s: expected %s, got %s\n' "$line" "$value" "$actual" >&2
    FAILURES=$((FAILURES + 1))
  fi
done
rg -q '^pcm_s16le$' "$FFMPEG_LOG"
if ! rg -q '\(00:30\)' "$TRIM_OUTPUT"; then
  printf '%s\n' 'trimmed diarization must retain the source start timestamp' >&2
  FAILURES=$((FAILURES + 1))
fi

expect_invalid_range() {
  local status
  set +e
  PATH="$TEST_DIR:$PATH" \
  STT_OUT="$TEST_DIR/invalid-out" \
  APPLE_STT_BIN="$APPLE_FAKE" \
  PYANNOTE_PYTHON="$PYANNOTE_FAKE" \
  bash "$SCRIPT_DIR/stt_diarize.sh" "$AUDIO" "$@" >/dev/null 2>&1
  status=$?
  set -e
  if [ "$status" -ne 64 ]; then
    printf 'invalid range %s must exit 64, got %s\n' "$*" "$status" >&2
    FAILURES=$((FAILURES + 1))
  fi
}
expect_invalid_range -1 40
expect_invalid_range 40 30

PYANNOTE_READY="$TEST_DIR/pyannote.ready"
export PYANNOTE_READY
set +e
STT_OUT="$TEST_DIR/signal-out" \
PYANNOTE_DELAY=1 \
APPLE_STT_BIN="$APPLE_FAKE" \
PYANNOTE_PYTHON="$PYANNOTE_FAKE" \
bash "$SCRIPT_DIR/stt_diarize.sh" "$AUDIO" >/dev/null 2>&1 &
SCRIPT_PID=$!
for _ in {1..100}; do
  [ ! -e "$PYANNOTE_READY" ] || break
  sleep 0.01
done
if [ ! -e "$PYANNOTE_READY" ]; then
  kill -TERM "$SCRIPT_PID" 2>/dev/null
  wait "$SCRIPT_PID"
  exit 1
fi
kill -TERM "$SCRIPT_PID"
wait "$SCRIPT_PID"
STATUS=$?
set -e
[ "$STATUS" -eq 143 ]
SIGNAL_DIR="$(find "$TEST_DIR/signal-out" -mindepth 1 -maxdepth 1 -type d -print -quit)"
[ -n "$SIGNAL_DIR" ]
[ ! -e "$SIGNAL_DIR/apple.json" ]
[ "$FAILURES" -eq 0 ]

printf '%s\n' "test_diarize: ok"
