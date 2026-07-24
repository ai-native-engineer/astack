#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
MARKER="$TMP/issues-called"
LOG="$TMP/gh.log"

cat > "$TMP/gh" <<'MOCK'
#!/usr/bin/env bash
printf '%s\n' "$*" >> "$OSS_EXPLORE_TEST_LOG"
case "${OSS_EXPLORE_TEST_CASE:-nonlatin}: $*" in
  "all-fail:"*" search repos "*)
    echo "network unavailable" >&2
    exit 42
    ;;
  "partial:"*" --match name,description "*)
    echo "auth failed" >&2
    exit 42
    ;;
  "partial:"*" --topic "*)
    printf '%s\n' '[{"fullName":"demo/topic","stargazersCount":5,"forksCount":1,"description":"topic","url":"https://example.com/topic","homepage":"","updatedAt":"2026-07-22T00:00:00Z","pushedAt":"2026-07-22T00:00:00Z","language":"Shell","license":{"name":"MIT License"},"openIssuesCount":1}]'
    ;;
  "merge:"*" --match name,description "*)
    printf '%s\n' '[{"fullName":"demo/shared","stargazersCount":20,"forksCount":2,"description":"shared","url":"https://example.com/shared","homepage":"","updatedAt":"2026-07-22T00:00:00Z","pushedAt":"2026-07-22T00:00:00Z","language":"Shell","license":{"name":"MIT License"},"openIssuesCount":1},{"fullName":"demo/direct","stargazersCount":10,"forksCount":1,"description":"direct","url":"https://example.com/direct","homepage":"","updatedAt":"2026-07-22T00:00:00Z","pushedAt":"2026-07-22T00:00:00Z","language":"Shell","license":{"name":"MIT License"},"openIssuesCount":1}]'
    ;;
  "merge:"*" --topic "*)
    printf '%s\n' '[{"fullName":"demo/shared","stargazersCount":20,"forksCount":2,"description":"shared","url":"https://example.com/shared","homepage":"","updatedAt":"2026-07-22T00:00:00Z","pushedAt":"2026-07-22T00:00:00Z","language":"Shell","license":{"name":"MIT License"},"openIssuesCount":1},{"fullName":"demo/topic","stargazersCount":15,"forksCount":1,"description":"topic","url":"https://example.com/topic","homepage":"","updatedAt":"2026-07-22T00:00:00Z","pushedAt":"2026-07-22T00:00:00Z","language":"Go","license":{"name":"Apache License 2.0"},"openIssuesCount":1}]'
    ;;
  *" search repos "*" --match name,description "*)
    printf '%s\n' '[{"fullName":"demo/direct","stargazersCount":10,"forksCount":2,"description":"direct","url":"https://example.com/direct","homepage":"","updatedAt":"2026-07-22T00:00:00Z","pushedAt":"2026-07-22T00:00:00Z","language":"Shell","license":{"name":"MIT License"},"openIssuesCount":1}]'
    ;;
  *" search repos "*" --match readme "*)
    printf '%s\n' '[{"fullName":"demo/readme","stargazersCount":1000,"forksCount":20,"description":"fallback","url":"https://example.com/readme","homepage":"","updatedAt":"2026-07-21T00:00:00Z","pushedAt":"2026-07-21T00:00:00Z","language":"Python","license":{"name":""},"openIssuesCount":2}]'
    ;;
  *" --topic "*)
    printf '%s\n' '[]'
    ;;
  *" search issues "*)
    : > "$OSS_EXPLORE_TEST_MARKER"
    printf '%s\n' '[{"url":"https://example.com/1"},{"url":"https://example.com/2"}]'
    ;;
  *)
    printf '%s\n' '[]'
    ;;
esac
MOCK
chmod +x "$TMP/gh"

run_explore() {
  PATH="$TMP:$PATH" \
    OSS_EXPLORE_TEST_LOG="$LOG" \
    OSS_EXPLORE_TEST_MARKER="$MARKER" \
    OSS_EXPLORE_TEST_CASE="$1" \
    "$ROOT/scripts/explore.sh" "${@:2}"
}

RESULT=$(run_explore nonlatin "음악" --license mit --limit 2 --no-issues --json)

echo "$RESULT" | jq -e '
  .query.with_issues == false
  and .count == 2
  and .repos[0].repo == "demo/direct"
  and .repos[0].matched_by == ["name/description"]
  and .repos[0].license == "MIT License"
  and .repos[1].repo == "demo/readme"
  and .repos[1].matched_by == ["readme"]
  and .repos[1].license == "unknown"
' >/dev/null
[ ! -e "$MARKER" ]
grep -q -- '--license mit' "$LOG"
! grep -q -- '--topic' "$LOG"

: > "$LOG"
RESULT=$(run_explore merge "vector database" --limit 3 --json)
echo "$RESULT" | jq -e '
  .count == 3
  and (.repos[] | select(.repo == "demo/shared").matched_by | sort) == ["name/description", "topic"]
' >/dev/null
grep -q -- '--topic vector-database' "$LOG"

: > "$LOG"
rm -f "$MARKER"
RESULT=$(run_explore issues "rust cli" --limit 1 --issues --json)
echo "$RESULT" | jq -e '.query.with_issues and .repos[0].gfi == 2 and .repos[0].hw == 2' >/dev/null
[ -e "$MARKER" ]

: > "$LOG"
ERR="$TMP/partial.err"
RESULT=$(run_explore partial "vector" --limit 1 --json 2>"$ERR")
echo "$RESULT" | jq -e '.repos[0].repo == "demo/topic"' >/dev/null
grep -q 'warning: name/description search failed: auth failed' "$ERR"

if run_explore all-fail "vector" --limit 1 --json >"$TMP/all.out" 2>"$TMP/all.err"; then
  echo "all failed searches should exit non-zero" >&2
  exit 1
fi
grep -q 'error: all repository searches failed' "$TMP/all.err"

echo "test_explore: ok"
