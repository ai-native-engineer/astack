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
  "issues-fail:"*" search issues "*)
    echo "API unavailable" >&2
    exit 42
    ;;
  "stderr-success:"*" --match name,description "*)
    echo "rate-limit notice" >&2
    printf '%s\n' '[{"fullName":"demo/clean","stargazersCount":1,"forksCount":0,"description":"clean","url":"https://example.com/clean","homepage":"","updatedAt":"2026-08-10T00:00:00Z","pushedAt":"2026-08-10T00:00:00Z","language":"Shell","license":{"name":"MIT License"},"openIssuesCount":0}]'
    ;;
  "updated:"*" --match name,description "*)
    printf '%s\n' '[{"fullName":"demo/recent-update","stargazersCount":1,"forksCount":0,"description":"updated","url":"https://example.com/recent-update","homepage":"","updatedAt":"2026-08-10T00:00:00Z","pushedAt":"2026-01-01T00:00:00Z","language":"Shell","license":{"name":"MIT License"},"openIssuesCount":0},{"fullName":"demo/recent-push","stargazersCount":1,"forksCount":0,"description":"pushed","url":"https://example.com/recent-push","homepage":"","updatedAt":"2026-08-01T00:00:00Z","pushedAt":"2026-08-09T00:00:00Z","language":"Shell","license":{"name":"MIT License"},"openIssuesCount":0}]'
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
grep -q -- '--visibility public' "$LOG"
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
echo "$RESULT" | jq -e '.query.with_issues and .issue_lookup_failures == 0 and .repos[0].gfi == 2 and .repos[0].hw == 2' >/dev/null
[ -e "$MARKER" ]

ERR="$TMP/issues-fail.err"
RESULT=$(run_explore issues-fail "rust cli" --limit 1 --issues --json 2>"$ERR")
echo "$RESULT" | jq -e '.issue_lookup_failures == 1 and .repos[0].gfi == null and .repos[0].hw == null' >/dev/null
echo "$RESULT" | python3 "$ROOT/scripts/render_html.py" | grep -q '조회 실패 1곳은 ?로 표시했습니다'
grep -q 'warning: issue lookup failed for 1 repository' "$ERR"
grep -q 'gh auth status or gh api rate_limit' "$ERR"
run_explore issues-fail "rust cli" --limit 1 --issues 2>/dev/null | grep -q '| ? | ? |'

: > "$LOG"
ERR="$TMP/partial.err"
RESULT=$(run_explore partial "vector" --limit 1 --json 2>"$ERR")
echo "$RESULT" | jq -e '.repos[0].repo == "demo/topic"' >/dev/null
grep -q 'auth failed' "$ERR"
grep -q 'warning: name/description search failed' "$ERR"

: > "$LOG"
ERR="$TMP/stderr-success.err"
RESULT=$(run_explore stderr-success "clean" --limit 1 --json 2>"$ERR")
echo "$RESULT" | jq -e '.repos[0].repo == "demo/clean"' >/dev/null
grep -q 'rate-limit notice' "$ERR"

RESULT=$(run_explore updated "tool" --sort updated --limit 2 --json)
echo "$RESULT" | jq -e '.repos[0].repo == "demo/recent-update"' >/dev/null

if run_explore all-fail "vector" --limit 1 --json >"$TMP/all.out" 2>"$TMP/all.err"; then
  echo "all failed searches should exit non-zero" >&2
  exit 1
fi
grep -q 'error: all repository searches failed' "$TMP/all.err"

echo "test_explore: ok"
