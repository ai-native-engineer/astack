#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
LOG="$TMP/gh.log"

cat > "$TMP/gh" <<'MOCK'
#!/usr/bin/env bash
printf '%s\n' "$*" >> "$OSS_EXPLORE_TEST_LOG"

if [ "$1" = "api" ]; then
  case "$*" in
    *"--paginate user/orgs"*)
      [ "${OSS_EXPLORE_TEST_CASE:-}" != "org-fail" ] || { echo "org API failed" >&2; exit 42; }
      printf '%s\n' 'MyOrg'
      ;;
    *"--paginate users/"*"/orgs"*) printf '%s\n' 'MyOrg' ;;
    "api user --jq .login") printf '%s\n' 'Me' ;;
    *"users/"*" --jq .login") printf '%s\n' 'Me' ;;
    *"contents/data.json"*)
      [ "${OSS_EXPLORE_TEST_CASE:-}" != "cache-refresh-fail" ] || { echo "cache API failed" >&2; exit 42; }
      printf '%s\n' '[]'
      ;;
    *) printf '%s\n' '[]' ;;
  esac
  exit 0
fi

case "$1 $2" in
  "search issues")
    case "${OSS_EXPLORE_TEST_CASE:-}" in
      discover-fail|trending-issues-fail) echo "search failed" >&2; exit 42 ;;
      discover-meta-fail|summary-meta-fail)
        printf '%s\n' '[{"repository":{"nameWithOwner":"demo/repo"},"title":"Starter","url":"https://example.com/issue","labels":[{"name":"easy"}],"updatedAt":"2026-08-10T00:00:00Z","commentsCount":0}]'
        ;;
      *) printf '%s\n' '[]' ;;
    esac
    ;;
  "search prs")
    if [[ "${OSS_EXPLORE_TEST_CASE:-}" == stats* ]]; then
      case " $* " in
        *" --merged "*) printf '%s\n' '[{"repository":{"nameWithOwner":"outside/lib"},"closedAt":"2026-08-10T00:00:00Z"}]' ;;
        *) printf '%s\n' '[{"createdAt":"2020-01-01T00:00:00Z"}]' ;;
      esac
    else
      printf '%s\n' '[{"repository":{"nameWithOwner":"me/own"}},{"repository":{"nameWithOwner":"myorg/team"}},{"repository":{"nameWithOwner":"outside/lib"}},{"repository":{"nameWithOwner":"outside/lib"}}]'
    fi
    ;;
  "repo view")
    case "${OSS_EXPLORE_TEST_CASE:-}:$*" in
      discover-meta-fail:*|summary-meta-fail:*|contributions-meta-fail:*|stats-language-fail:*)
        echo "metadata API failed" >&2
        exit 42
        ;;
      *"--json primaryLanguage"*) printf '%s\n' 'Python' ;;
      *) printf '%s\n' '{"stargazerCount":42,"description":"Library","url":"https://github.com/outside/lib"}' ;;
    esac
    ;;
  *) printf '%s\n' '[]' ;;
esac
MOCK
chmod +x "$TMP/gh"

cat > "$TMP/curl" <<'MOCK'
#!/usr/bin/env bash
echo "raw fetch failed" >&2
exit 42
MOCK
chmod +x "$TMP/curl"

cat > "$TMP/python3" <<'MOCK'
#!/usr/bin/env bash
if [ "${OSS_EXPLORE_TEST_CASE:-}" = "trending-empty" ]; then
  printf '%s\n' '{"type":"trending","language":"","since":"daily","generated":"2026-08-10T00:00:00+09:00","source_url":"https://github.com/trending?since=daily","repos":[]}'
else
  printf '%s\n' '{"type":"trending","language":"","since":"daily","generated":"2026-08-10T00:00:00+09:00","source_url":"https://github.com/trending?since=daily","repos":[{"repo":"demo/repo","period_stars":5,"total_stars":10,"language":"Shell","description":"Demo"}]}'
fi
MOCK
chmod +x "$TMP/python3"

run_script() {
  PATH="$TMP:$PATH" \
    XDG_CACHE_HOME="$TMP/cache" \
    OSS_EXPLORE_TEST_LOG="$LOG" \
    OSS_EXPLORE_TEST_CASE="$1" \
    "$ROOT/scripts/$2" "${@:3}"
}

if run_script discover-fail discover.sh --label easy --limit 1 --json >"$TMP/discover.out" 2>"$TMP/discover.err"; then
  echo "discover search failure must exit non-zero" >&2
  exit 1
fi
grep -q 'search failed' "$TMP/discover.err"

mkdir -p "$TMP/cache/oss-explore"
cat > "$TMP/cache/oss-explore/awesome-for-beginners.json" <<'JSON'
{"repositories":[{"link":"https://github.com/demo/repo","label":"starter","technologies":["Shell"]}]}
JSON
: > "$LOG"
run_script curated discover.sh --curated --topic docs --include-linked --stale-ok --limit 1 --json >/dev/null
grep -q 'created:>=2008-01-01 docs' "$LOG"
! grep -q -- '-linked:pr' "$LOG"
! grep -q -- '-label:blocked' "$LOG"
grep -q -- '--visibility public' "$LOG"

CACHE_FILE="$TMP/cache/oss-explore/awesome-for-beginners.json"
CACHE_BEFORE=$(cksum "$CACHE_FILE")
touch -t 202001010000 "$CACHE_FILE"
run_script cache-refresh-fail discover.sh --curated --limit 1 --json >"$TMP/cache.out" 2>"$TMP/cache.err"
[ "$CACHE_BEFORE" = "$(cksum "$CACHE_FILE")" ]
grep -q 'using the existing valid cache' "$TMP/cache.err"

jq -n '{repositories: [range(0;5000) | {link:("https://github.com/demo/repo" + tostring), label:"starter", technologies:["Shell"]}]}' > "$CACHE_FILE"
: > "$LOG"
run_script curated-large discover.sh --curated --limit 40 --json >/dev/null
[ "$(grep -c -- '--repo demo/repo' "$LOG")" -eq 40 ]

RESULT=$(run_script discover-empty discover.sh --label easy --limit 1 --min-stars 1 --json)
echo "$RESULT" | jq -e '.total == 0 and .count == 0' >/dev/null
RESULT=$(run_script discover-empty discover.sh --label easy --limit 1 --summary --json)
echo "$RESULT" | jq -e '.total_issues == 0 and .languages == []' >/dev/null

if run_script discover-meta-fail discover.sh --label easy --limit 1 --min-stars 1 --json >"$TMP/meta.out" 2>"$TMP/meta.err"; then
  echo "discover star metadata failure must exit non-zero" >&2
  exit 1
fi
grep -q 'while resolving --min-stars' "$TMP/meta.err"

if run_script summary-meta-fail discover.sh --label easy --limit 1 --summary --json >"$TMP/summary.out" 2>"$TMP/summary.err"; then
  echo "discover language metadata failure must exit non-zero" >&2
  exit 1
fi
grep -q 'while generating --summary' "$TMP/summary.err"

: > "$LOG"
RESULT=$(run_script trending-issues-fail trending.sh --issues --json 2>"$TMP/trending.err")
echo "$RESULT" | jq -e '.issue_lookup_failures == 1 and .repos[0].gfi == null and .repos[0].hw == null' >/dev/null
grep -q 'Check gh auth status or gh api rate_limit' "$TMP/trending.err"
: > "$LOG"
RESULT=$(run_script trending-empty trending.sh --issues --json)
echo "$RESULT" | jq -e '.issue_lookup_failures == 0 and .repos == []' >/dev/null
! grep -q 'search issues' "$LOG"

: > "$LOG"
RESULT=$(run_script contributions contributions.sh me --limit 10 --json)
echo "$RESULT" | jq -e '
  .user == "Me"
  and .summary.merged_prs == 3
  and .summary.limit_reached == false
  and .summary.metadata_lookup_failures == 0
  and .external == [{repo:"outside/lib", prs:2, stars:42, description:"Library", url:"https://github.com/outside/lib"}]
  and .orgs[0].org == "myorg"
  and .orgs[0].prs == 1
' >/dev/null
echo "$RESULT" | jq '.summary.limit_reached = true' | python3 "$ROOT/scripts/render_html.py" | grep -q '검색 상한 10건'
grep -q -- '--visibility public' "$LOG"

RESULT=$(run_script contributions-meta-fail contributions.sh me --limit 10 --json 2>"$TMP/contributions-meta.err")
echo "$RESULT" | jq -e '
  .summary.metadata_lookup_failures == 1
  and .external[0].stars == null
  and .external[0].metadata_unavailable == true
' >/dev/null
grep -q 'repository metadata lookup failed for 1' "$TMP/contributions-meta.err"
echo "$RESULT" | python3 "$ROOT/scripts/render_html.py" | grep -q '★ ?'

if run_script org-fail contributions.sh @me --json >"$TMP/org.out" 2>"$TMP/org.err"; then
  echo "organization API failure must exit non-zero" >&2
  exit 1
fi
grep -q 'unable to load organization memberships' "$TMP/org.err"

: > "$LOG"
RESULT=$(run_script stats stats.sh me --limit 10 --json)
echo "$RESULT" | jq -e '
  .user == "Me"
  and .years == [{year:"2026", prs:1}]
  and .months == [{month:"08", prs:1}]
  and .summary.limit_reached == false
  and .summary.merge_rate == 100
  and .summary.language_lookup_failures == 0
' >/dev/null
[ "$(grep -c -- '--visibility public' "$LOG")" -eq 2 ]

RESULT=$(run_script stats-capped stats.sh me --limit 1 --json)
echo "$RESULT" | jq -e '.summary.limit_reached == true and .summary.merge_rate == null' >/dev/null
echo "$RESULT" | python3 "$ROOT/scripts/render_html.py" | grep -q '계산 불가'

RESULT=$(run_script stats-language-fail stats.sh me --limit 10 --json 2>"$TMP/stats-language.err")
echo "$RESULT" | jq -e '.summary.language_lookup_failures == 1 and .languages == []' >/dev/null
grep -q 'excluded from language distribution' "$TMP/stats-language.err"
echo "$RESULT" | python3 "$ROOT/scripts/render_html.py" | grep -q '언어 조회 실패 1건'

if "$ROOT/scripts/bootstrap.sh" badrepo --dry >"$TMP/bootstrap.out" 2>"$TMP/bootstrap.err"; then
  echo "invalid repo must fail" >&2
  exit 1
fi
if "$ROOT/scripts/bootstrap.sh" owner/repo branch extra --dry >"$TMP/bootstrap.out" 2>"$TMP/bootstrap.err"; then
  echo "extra positional argument must fail" >&2
  exit 1
fi
"$ROOT/scripts/bootstrap.sh" owner/repo contrib/test --dry >/dev/null

echo "test_operations: ok"
