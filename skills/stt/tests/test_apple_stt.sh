#!/bin/bash
set -euo pipefail

ROOT=$(cd "$(dirname "$0")/.." && pwd)
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
BIN="$TMP/apple-stt"

swiftc -O -parse-as-library -target arm64-apple-macos26.0 \
  "$ROOT/native/apple-stt.swift" -o "$BIN"

HELP=$($BIN --help)
grep -q -- '--analysis-json' <<<"$HELP"
grep -q -- '--json' <<<"$HELP"
grep -q -- '--vocab-file' <<<"$HELP"

if "$BIN" --analysis-json --json missing.m4a >/dev/null 2>&1; then
  echo "analysis mode must reject legacy output flags" >&2
  exit 1
fi

{
  printf '첫용어\n중복\n중복\n'
  for i in $(seq 1 105); do printf '용어%03d\n' "$i"; done
} > "$TMP/vocab.txt"

cat > "$TMP/context_test.swift" <<'SWIFT'
import Foundation

@main
struct ContextTest {
    static func main() throws {
        var options = Options()
        options.vocabFile = CommandLine.arguments[1]
        options.oneOffVocab = ["중복", "일회성"]
        let context = try contextTerms(for: options)
        precondition(context.selected.count == 100)
        precondition(context.selected[0] == "첫용어")
        precondition(context.selected[1] == "중복")
        precondition(context.selected.filter { $0 == "중복" }.count == 1)
        precondition(context.dropped.count == 8)
        precondition(!context.selected.contains("일회성"))

        let segment = Segment(
            start: 1.0, end: 2.25, text: "테스트", confidenceSpans: [],
            reviewConfidence: nil, alternatives: []
        )
        var timestamps = Options()
        timestamps.timestamps = true
        let timestampText = try render([segment], options: timestamps, analysis: nil)
        precondition(timestampText == "[00:01] 테스트")
        var subtitles = Options()
        subtitles.srt = true
        let subtitleText = try render([segment], options: subtitles, analysis: nil)
        precondition(subtitleText == "1\n00:00:01,000 --> 00:00:02,250\n테스트\n")
    }
}
SWIFT

swiftc -DAPPLE_STT_TESTING -parse-as-library -target arm64-apple-macos26.0 \
  "$ROOT/native/apple-stt.swift" "$TMP/context_test.swift" -o "$TMP/context-test"
"$TMP/context-test" "$TMP/vocab.txt"

python3 - "$ROOT/tests/fixtures/apple-capability-ko-KR.json" <<'PY'
import json
import sys

document = json.load(open(sys.argv[1], encoding="utf-8"))
assert document["schema_version"] == 1
for segment in document["segments"]:
    boundaries = {0}
    offset = 0
    for character in segment["text"]:
        offset += len(character.encode("utf-8"))
        boundaries.add(offset)
    for span in segment["confidence_spans"]:
        assert span["start_byte"] in boundaries
        assert span["end_byte"] in boundaries
        assert span["start_byte"] < span["end_byte"] <= offset
PY

if [ -n "${APPLE_STT_TEST_AUDIO:-}" ]; then
  "$BIN" --quiet "$APPLE_STT_TEST_AUDIO" > "$TMP/plain.txt"
  "$BIN" --quiet --timestamps "$APPLE_STT_TEST_AUDIO" > "$TMP/timestamps.txt"
  "$BIN" --quiet --srt "$APPLE_STT_TEST_AUDIO" > "$TMP/subtitles.srt"
  "$BIN" --quiet --json "$APPLE_STT_TEST_AUDIO" > "$TMP/legacy.json"
  "$BIN" --quiet --analysis-json --vocab-file "$TMP/vocab.txt" \
    "$APPLE_STT_TEST_AUDIO" > "$TMP/analysis.json"
  grep -Eq '^\[[0-9]{2}:[0-9]{2}\]' "$TMP/timestamps.txt"
  grep -Eq '^[0-9]+$' "$TMP/subtitles.srt"
  grep -q -- '-->' "$TMP/subtitles.srt"
  python3 - "$TMP/legacy.json" "$TMP/analysis.json" <<'PY'
import json
import sys

legacy = json.load(open(sys.argv[1], encoding="utf-8"))
analysis = json.load(open(sys.argv[2], encoding="utf-8"))
assert isinstance(legacy, list) and legacy
assert set(legacy[0]) == {"start", "end", "text"}
assert analysis["schema_version"] == 1
assert analysis["offset_unit"] == "utf8_bytes"
assert len(analysis["context"]["selected"]) <= 100
assert analysis["segments"]
assert set(analysis["segments"][0]) == {
    "id", "start", "end", "text", "confidence_spans",
    "review_confidence", "alternatives",
}
PY
fi

echo "apple-stt checks passed"
