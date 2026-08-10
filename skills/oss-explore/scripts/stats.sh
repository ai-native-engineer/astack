#!/usr/bin/env bash
# oss-explore :: stats
# PR 기준 기여 통계: 머지율, 연도별 추이, 언어별 분포(머지 PR이 닿은 레포의 주 언어).
#
# Usage: stats.sh [username] [--json|--html] [--limit N]
set -euo pipefail
command -v jq >/dev/null 2>&1 || { echo "error: jq is required; install jq and add it to PATH" >&2; exit 69; }

OUT=md
LIMIT=1000
USER_ARG=""
while [ $# -gt 0 ]; do
  case "$1" in
    --json) OUT=json ;;
    --html) OUT=html ;;
    --limit) shift; LIMIT="${1:?--limit needs a value}" ;;
    -*) echo "unknown option: $1" >&2; exit 1 ;;
    *) [ -z "$USER_ARG" ] || { echo "error: only one username is allowed" >&2; exit 1; }; USER_ARG="$1" ;;
  esac
  shift
done

case "$LIMIT" in ''|*[!0-9]*) echo "error: --limit must be an integer from 1 to 1000" >&2; exit 1 ;; esac
[ "$LIMIT" -ge 1 ] && [ "$LIMIT" -le 1000 ] || { echo "error: --limit must be an integer from 1 to 1000" >&2; exit 1; }

if [ -z "$USER_ARG" ] || [ "$USER_ARG" = "@me" ]; then
  USER=$(gh api user --jq .login)
else
  USER=$(gh api "users/$USER_ARG" --jq .login)
fi

ALL=$(gh search prs --author="$USER" --visibility public --limit "$LIMIT" --json createdAt)
MERGED=$(gh search prs --author="$USER" --merged --visibility public --limit "$LIMIT" --json repository,closedAt)

TOTAL=$(echo "$ALL" | jq 'length')
MERGED_N=$(echo "$MERGED" | jq 'length')

# 연도별 (머지 PR 기준)
YEARS=$(echo "$MERGED" | jq '
  [ .[].closedAt[0:4] ] | group_by(.)
  | map({ year: .[0], prs: length }) | sort_by(.year)')

# 월별 (1~12) — 문자열 슬라이스라 무위험
MONTHS=$(echo "$MERGED" | jq '
  [ .[].closedAt[5:7] ] | group_by(.)
  | map({ month: .[0], prs: length }) | sort_by(.month)')

# 요일별 — jq strptime/mktime/strftime(빌드 의존) 실패 시 빈 배열로 폴백
WEEKDAYS=$(echo "$MERGED" | jq '
  [ .[].closedAt | (strptime("%Y-%m-%dT%H:%M:%SZ") | mktime | strftime("%u %a")) ]
  | group_by(.) | map({ day: .[0], prs: length }) | sort_by(.day)' 2>/dev/null || echo '[]')
[ -z "$WEEKDAYS" ] && WEEKDAYS='[]'

# 언어별: 머지 PR이 닿은 unique 레포의 주 언어. 실패는 실제 Unknown과 구분해 제외한다.
LANG_RESULTS=$(echo "$MERGED" | jq -r '[ .[].repository.nameWithOwner ] | unique | .[]' | while read -r repo; do
  [ -z "$repo" ] && continue
  gh repo view "$repo" --json primaryLanguage --jq '.primaryLanguage.name // "Unknown"' 2>/dev/null || echo "__oss_explore_lookup_failed__"
done | jq -R . | jq -s .)
[ -z "$LANG_RESULTS" ] && LANG_RESULTS='[]'
LANGUAGE_FAILURES=$(echo "$LANG_RESULTS" | jq '[.[] | select(. == "__oss_explore_lookup_failed__")] | length')
[ "$LANGUAGE_FAILURES" -eq 0 ] || echo "warning: primary language lookup failed for $LANGUAGE_FAILURES repository/repositories; excluded from language distribution" >&2
LANGS=$(echo "$LANG_RESULTS" | jq '
  map(select(. != "__oss_explore_lookup_failed__"))
  | group_by(.) | map({ name: .[0], repos: length }) | sort_by(-.repos)')
[ -z "$LANGS" ] && LANGS='[]'

RESULT=$(jq -n \
  --arg user "$USER" \
  --arg gen "$(date '+%Y-%m-%d %H:%M')" \
  --argjson total "$TOTAL" \
  --argjson merged "$MERGED_N" \
  --argjson years "$YEARS" \
  --argjson months "$MONTHS" \
  --argjson weekdays "$WEEKDAYS" \
  --argjson langs "$LANGS" \
  --argjson language_failures "$LANGUAGE_FAILURES" \
  --argjson limit "$LIMIT" '
  { type: "stats", user: $user, generated: $gen,
    summary: { total_prs: $total, merged_prs: $merged,
               merge_rate: (if $total >= $limit or $merged >= $limit then null elif $total > 0 then (($merged * 1000 / $total) | floor) / 10 else 0 end),
               search_limit: $limit, limit_reached: ($total >= $limit or $merged >= $limit),
               language_lookup_failures: $language_failures },
    years: $years, months: $months, weekdays: $weekdays, languages: $langs }')

case "$OUT" in
  json)
    echo "$RESULT"
    ;;
  html)
    SELF="$(cd "$(dirname "$0")" && pwd)"
    f="${TMPDIR:-/tmp}/oss-explore-stats-${USER}.html"
    echo "$RESULT" | python3 "$SELF/render_html.py" > "$f"
    echo "HTML 리포트: $f"
    open "$f" 2>/dev/null || true
    ;;
  md)
    echo "$RESULT" | jq -r '
      "# \(.user) — 기여 통계\n",
      "전체 PR \(.summary.total_prs)건 · 머지 \(.summary.merged_prs)건 · 머지율 " + (if .summary.merge_rate == null then "계산 불가" else "\(.summary.merge_rate)%" end) + "\n",
      (if .summary.limit_reached then "_GitHub 검색 상한 \(.summary.search_limit)건에 도달해 통계가 일부 기간만 반영될 수 있습니다._\n" else empty end),
      (if .summary.language_lookup_failures > 0 then "_언어 조회 실패 \(.summary.language_lookup_failures)건은 언어별 분포에서 제외했습니다._\n" else empty end),
      "## 연도별 (머지 PR)\n",
      (.years[] | "- \(.year): \(.prs)"),
      "\n## 월별 (머지 PR)\n",
      (.months[] | "- \(.month)월: \(.prs)"),
      (if (.weekdays | length) > 0 then
        ( "\n## 요일별 (머지 PR)\n", (.weekdays[] | "- \(.day): \(.prs)") )
       else empty end),
      "\n## 언어별 (머지 PR이 닿은 레포 수)\n",
      (.languages[] | "- \(.name): \(.repos)")
    '
    ;;
esac
