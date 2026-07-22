#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
MARKER="$TMP/issues-called"

cat > "$TMP/gh" <<'MOCK'
#!/usr/bin/env bash
case " $* " in
  *" search repos "*" --match name,description "*)
    printf '%s\n' '[{"fullName":"demo/direct","stargazersCount":10,"forksCount":2,"description":"direct","url":"https://example.com/direct","homepage":"","updatedAt":"2026-07-22T00:00:00Z","pushedAt":"2026-07-22T00:00:00Z","language":"Shell","license":{"name":"MIT License"},"openIssuesCount":1}]'
    ;;
  *" search repos "*" --match readme "*)
    printf '%s\n' '[{"fullName":"demo/readme","stargazersCount":1000,"forksCount":20,"description":"fallback","url":"https://example.com/readme","homepage":"","updatedAt":"2026-07-21T00:00:00Z","pushedAt":"2026-07-21T00:00:00Z","language":"Python","license":{"name":""},"openIssuesCount":2}]'
    ;;
  *" --topic "*)
    exit 42
    ;;
  *" search issues "*)
    : > "$OSS_EXPLORE_TEST_MARKER"
    printf '%s\n' '[]'
    ;;
  *)
    printf '%s\n' '[]'
    ;;
esac
MOCK
chmod +x "$TMP/gh"

RESULT=$(PATH="$TMP:$PATH" OSS_EXPLORE_TEST_MARKER="$MARKER" "$ROOT/scripts/explore.sh" "음악" --limit 2 --json)

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

echo "test_explore: ok"
