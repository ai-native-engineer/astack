#!/usr/bin/env bash
set -euo pipefail

TEST_DIR="$(mktemp -d "${TMPDIR:-/tmp}/stt-diarize-test.XXXXXXXX")"
trap 'rm -r -- "$TEST_DIR"' EXIT

PYANNOTE_FAKE="$TEST_DIR/pyannote-python"
MOSS_FAKE="$TEST_DIR/moss-python"
FAKE_BIN="$TEST_DIR/bin"
CALLS="$TEST_DIR/calls.log"
FFMPEG_LOG="$TEST_DIR/ffmpeg.log"
AUDIO="$TEST_DIR/audio.m4a"
mkdir -p "$FAKE_BIN"
touch "$AUDIO"
# Never read or write the user's remembered voices.
export STT_VOICES="$TEST_DIR/voices.json"

cat > "$FAKE_BIN/ffmpeg" <<'SH'
#!/usr/bin/env bash
printf '%s\n' "$@" > "$FFMPEG_LOG"
for last; do :; done
: > "$last"
SH

cat > "$PYANNOTE_FAKE" <<'SH'
#!/usr/bin/env bash
set -euo pipefail
[[ "$1" == */pyannote-chunks.py ]] || exit 70
shift
case "$1" in
  --check) exit 0 ;;
  plan)
    printf '%s\n' plan >> "$CALLS"
    printf '%s' '[[0.0, 70.0]]' > "$3"
    printf '%s' '{"duration": 70.0, "speech": [[0.0, 70.0]]}' > "$4" ;;
  join)
    printf '%s\n' join >> "$CALLS"
    [ -f "$3" ] || exit 71
    if [ "${PYANNOTE_DELAY:-0}" = "1" ]; then
      : > "$PYANNOTE_READY"
      sleep 0.2
    fi
    cat > "$5/transcript.json" <<'JSON'
{"segments": [
  {"start": 0.0, "end": 2.0, "speaker": "SPEAKER_00", "text": "첫 번째"},
  {"start": 2.0, "end": 4.0, "speaker": "SPEAKER_01", "text": "두 번째"},
  {"start": 4.5, "end": 6.0, "speaker": "SPEAKER_01", "text": "이어서"},
  {"start": 30.0, "end": 32.0, "speaker": "SPEAKER_00", "text": "다시"}],
 "gaps": [[6.0, 30.0]]}
JSON
    printf '%s\n' 'SPEAKER audio 1 0.000 2.000 <NA> <NA> SPEAKER_00 <NA> <NA>' > "$5/diar.rttm"
    printf '%s\n' '{"_recording":"fake","SPEAKER_00":{"seconds":10.0,"embedding":[1,0,0]},
      "SPEAKER_01":{"seconds":10.0,"embedding":[0,1,0]}}' > "$5/speakers.json" ;;
  *) exit 64 ;;
esac
SH

cat > "$MOSS_FAKE" <<'SH'
#!/usr/bin/env bash
set -euo pipefail
[[ "$1" == */moss-diarize.py ]] || exit 70
[ "${2:-}" != "--check" ] || exit 0
printf '%s\n' moss >> "$CALLS"
[ "${MOSS_FAIL:-0}" = "0" ] || exit 70
printf '%s' '{"model": "fake", "chunks": [], "segments": []}' > "$4"
SH

chmod +x "$FAKE_BIN/ffmpeg" "$PYANNOTE_FAKE" "$MOSS_FAKE"
export CALLS FFMPEG_LOG

SCRIPT_DIR="$(cd "$(dirname "$0")/../scripts" && pwd)"
FAILURES=0
fail() {
  printf '%s\n' "$1" >&2
  FAILURES=$((FAILURES + 1))
}
run() {
  PATH="$FAKE_BIN:$PATH" PYANNOTE_PYTHON="$PYANNOTE_FAKE" MOSS_PYTHON="$MOSS_FAKE" \
    bash "$SCRIPT_DIR/stt_diarize.sh" "$@"
}

OUTPUT="$(STT_OUT="$TEST_DIR/out" run "$AUDIO")"
OUT_DIR="$(dirname "$OUTPUT")"
[ -f "$OUTPUT" ] || fail 'diarized.md missing'
[ -f "$OUT_DIR/diar.rttm" ] || fail 'diar.rttm missing'
[ -f "$OUT_DIR/transcript.json" ] || fail 'transcript.json missing'
for work in audio.wav chunks.json speech.json moss.json; do
  [ ! -e "$OUT_DIR/$work" ] || fail "work file left behind: $work"
done
[ "$(tr '\n' ' ' < "$CALLS")" = "plan moss join " ] || fail "unexpected step order: $(tr '\n' ' ' < "$CALLS")"

EXPECTED="$(printf '%s\n\n%s\n\n%s\n\n%s' '**[SPEAKER_00]** (00:00) 첫 번째' \
  '**[SPEAKER_01]** (00:02) 두 번째 이어서' '**[gap]** (00:06~00:30)' '**[SPEAKER_00]** (00:30) 다시')"
[ "$(cat "$OUTPUT")" = "$EXPECTED" ] || fail "turns mismatch:
$(cat "$OUTPUT")"

# The review page needs the source audio and start time of a finished run.
python3 -c 'import json, os, sys; m = json.load(open(sys.argv[1]))
assert m["audio"] == os.path.abspath(sys.argv[2]) and m["start"] == 0 and m["end"] is None' \
  "$OUT_DIR/run.json" "$AUDIO" 2>/dev/null || fail 'a finished run must record its audio in run.json'

# A remembered voice replaces its anonymous label in later runs.
python3 "$SCRIPT_DIR/voices.py" enroll "$OUT_DIR" SPEAKER_01 민지 >/dev/null
[ "$(stat -f '%Lp' "$STT_VOICES")" = "600" ] || fail 'voice store must be readable only by the owner'
: > "$CALLS"
NAMED="$(STT_OUT="$TEST_DIR/named-out" run "$AUDIO" 2>/dev/null)"
rg -q '^\*\*\[민지\]\*\* \(00:02\) 두 번째 이어서$' "$NAMED" || fail "remembered voice mismatch:
$(cat "$NAMED")"
rg -q '^\*\*\[SPEAKER_00\]\*\* \(00:00\)' "$NAMED" || fail 'unremembered speaker must keep its label'
python3 "$SCRIPT_DIR/voices.py" forget 민지 >/dev/null
if rg -q 민지 "$STT_VOICES"; then
  fail 'forget must remove every sample of the name'
fi

# One speaker: a 2 s pause or a turn over 60 s starts a new paragraph.
printf '%s\n' '{"segments": [
  {"start": 0.0, "end": 1.0, "speaker": "SPEAKER_00", "text": "하나"},
  {"start": 3.0, "end": 4.0, "speaker": "SPEAKER_00", "text": "둘"},
  {"start": 4.0, "end": 62.0, "speaker": "SPEAKER_00", "text": "셋"},
  {"start": 62.0, "end": 63.5, "speaker": "SPEAKER_00", "text": "넷"}]}' > "$TEST_DIR/single.json"
SINGLE="$(python3 "$SCRIPT_DIR/diar_views.py" "$TEST_DIR/single.json")"
EXPECTED_SINGLE="$(printf '%s\n\n%s\n\n%s' '**[SPEAKER_00]** (00:00) 하나' \
  '**[SPEAKER_00]** (00:03) 둘 셋' '**[SPEAKER_00]** (01:02) 넷')"
[ "$SINGLE" = "$EXPECTED_SINGLE" ] || fail "single-speaker split mismatch:
$SINGLE"

: > "$CALLS"
TRIM_OUTPUT="$(STT_OUT="$TEST_DIR/trim-out" run "$AUDIO" 30 40)"
TRIM_ARGS="$(tr '\n' ' ' < "$FFMPEG_LOG")"
[[ "$TRIM_ARGS" == *"-ss 30 -to 40 -i $AUDIO "* ]] || fail "trim args: $TRIM_ARGS"
[[ "$TRIM_ARGS" == *"-ar 16000 -ac 1 -c:a pcm_s16le "* ]] || fail "decode args: $TRIM_ARGS"
rg -q '^\*\*\[SPEAKER_00\]\*\* \(00:30\)' "$TRIM_OUTPUT" || fail 'trimmed output must keep the source start time'
rg -q '^\*\*\[gap\]\*\* \(00:36~01:00\)$' "$TRIM_OUTPUT" || fail 'gap times must keep the source start time'

expect_status() {
  local want="$1" status
  shift
  set +e
  STT_OUT="$TEST_DIR/status-out" run "$@" >/dev/null 2>"$TEST_DIR/status.err"
  status=$?
  set -e
  [ "$status" -eq "$want" ] || fail "args $* must exit $want, got $status"
}
expect_status 64 "$AUDIO" -1 40
expect_status 64 "$AUDIO" 40 30
expect_status 66 "$TEST_DIR/missing.m4a"

: > "$CALLS"
export MOSS_FAIL=1
expect_status 70 "$AUDIO"
unset MOSS_FAIL
rg -q 'stt-fallback.sh' "$TEST_DIR/status.err" || fail 'MOSS failure must point to the plain transcription script'
if rg -q '^join$' "$CALLS"; then
  fail 'join must not run after MOSS fails'
fi

PYANNOTE_READY="$TEST_DIR/pyannote.ready"
export PYANNOTE_READY
set +e
# Start the script itself in the background so TERM reaches it, not a wrapper.
PATH="$FAKE_BIN:$PATH" PYANNOTE_PYTHON="$PYANNOTE_FAKE" MOSS_PYTHON="$MOSS_FAKE" \
  STT_OUT="$TEST_DIR/signal-out" PYANNOTE_DELAY=1 \
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
[ "$STATUS" -eq 143 ] || fail "TERM must exit 143, got $STATUS"
SIGNAL_DIR="$(find "$TEST_DIR/signal-out" -mindepth 1 -maxdepth 1 -type d -print -quit)"
[ -n "$SIGNAL_DIR" ] || fail 'signal run made no output directory'
for work in audio.wav chunks.json speech.json moss.json; do
  [ ! -e "$SIGNAL_DIR/$work" ] || fail "work file left after TERM: $work"
done
[ "$FAILURES" -eq 0 ]

printf '%s\n' "test_diarize: ok"
