#!/usr/bin/env bash
# oss-explore :: trending
# github.com/trending 을 파싱해 보여준다. 언어·기간·강조 키워드는 전부 인자(하드코딩 없음).
#
# Usage: trending.sh [language] [--since daily|weekly|monthly] [--limit N] [--highlight a,b,c] [--issues] [--json]
#   language     trending 언어 (생략 시 전체). 예: python, typescript, rust, go
#   --since      집계 기간 (기본 daily)
#   --limit      개수 (기본 25)
#   --highlight  쉼표 구분 키워드 — 레포명/설명에 매치되면 🔖 표시 (없으면 강조 안 함)
#   --issues     각 레포의 good first issue / help wanted 수를 병렬 조회해 컬럼 추가
#   --json       원시 JSON 출력
set -euo pipefail
command -v jq >/dev/null 2>&1 || { echo "error: jq is required; install jq and add it to PATH" >&2; exit 69; }

LANGUAGE=""
SINCE=daily
LIMIT=25
HIGHLIGHT=""
ISSUES=0
ISSUE_LOOKUP_FAILURES=0
OUT=md
while [ $# -gt 0 ]; do
  case "$1" in
    --since) shift; SINCE="${1:?--since needs a value}" ;;
    --limit) shift; LIMIT="${1:?--limit needs a value}" ;;
    --highlight) shift; HIGHLIGHT="${1:?--highlight needs a value}" ;;
    --issues) ISSUES=1 ;;
    --json) OUT=json ;;
    -*) echo "unknown option: $1" >&2; exit 1 ;;
    *) [ -z "$LANGUAGE" ] || { echo "error: only one language is allowed" >&2; exit 1; }; LANGUAGE="$1" ;;
  esac
  shift
done

SELF="$(cd "$(dirname "$0")" && pwd)"
args=(--since "$SINCE" --limit "$LIMIT")
[ -n "$LANGUAGE" ] && args=("$LANGUAGE" "${args[@]}")
if ! DATA=$(python3 "$SELF/trending.py" "${args[@]}"); then
  printf '%s\n' "$DATA" >&2
  exit 1
fi
DATA=$(echo "$DATA" | jq '.issue_lookup_failures = 0')

# good first issue / help wanted 보강 (옵션)
if [ "$ISSUES" = 1 ] && [ "$(echo "$DATA" | jq '.repos | length')" -gt 0 ]; then
  TSV=$(echo "$DATA" | jq -r '.repos[].repo' | xargs -P 10 -n 1 sh -c '
    repo="$1"
    failed=0
    if result=$(gh search issues --repo "$repo" --visibility public --label "good first issue" --state open --limit 50 --json url 2>/dev/null) && gfi=$(printf "%s" "$result" | jq -er length 2>/dev/null); then :; else gfi=null; failed=1; fi
    if result=$(gh search issues --repo "$repo" --visibility public --label "help wanted" --state open --limit 50 --json url 2>/dev/null) && hw=$(printf "%s" "$result" | jq -er length 2>/dev/null); then :; else hw=null; failed=1; fi
    printf "%s\t%s\t%s\t%s\n" "$repo" "$gfi" "$hw" "$failed"' _)
  ISSUE_LOOKUP_FAILURES=$(printf '%s\n' "$TSV" | awk -F '\t' '$4 == 1 { n++ } END { print n + 0 }')
  MAP=$(echo "$TSV" | jq -R 'split("\t") | select(length==4) | {(.[0]): {gfi:(if .[1] == "null" then null else .[1]|tonumber end), hw:(if .[2] == "null" then null else .[2]|tonumber end)}}' | jq -s 'add // {}')
  DATA=$(echo "$DATA" | jq --argjson m "$MAP" --argjson failures "$ISSUE_LOOKUP_FAILURES" '.issue_lookup_failures = $failures | .repos |= map(. + ($m[.repo] // {gfi:null, hw:null}))')
  [ "$ISSUE_LOOKUP_FAILURES" -eq 0 ] || printf 'warning: issue lookup failed for %s repository(s); GFI/HW are shown as ?. Check gh auth status or gh api rate_limit.\n' "$ISSUE_LOOKUP_FAILURES" >&2
fi

# highlight 키워드 플래그 부여 (빈 입력도 [] 로 안전하게)
KWARR=$(printf '%s' "$HIGHLIGHT" | jq -Rs 'split(",") | map(gsub("^\\s+|\\s+$";"") | select(length>0) | ascii_downcase)')
DATA=$(echo "$DATA" | jq --argjson kws "$KWARR" '
  .repos |= map(.hl = ([ $kws[] as $k | ((.repo + " " + (.description // "")) | ascii_downcase | contains($k)) ] | any))')

case "$OUT" in
  json)
    echo "$DATA"
    ;;
  md)
    echo "$DATA" | jq -r '
      "# GitHub 트렌딩 — \(if .language == "" then "전체" else .language end) · \(.since)\n",
      (if (.repos | length) == 0 then "_조건에 맞는 트렌딩 레포가 없습니다._" else
        (if (.repos[0] | has("gfi")) then
          ( "| 레포 | ★/기간 | 총★ | 언어 | GFI | HW | 설명 |",
            "|---|---|---|---|---|---|---|",
            (.repos[] | "| \(if .hl then "🔖 " else "" end)\(.repo) | +\(.period_stars) | \(.total_stars) | \(.language) | \(.gfi // "?") | \(.hw // "?") | \((.description // "")[0:55]) |") )
         else
          ( "| 레포 | ★/기간 | 총★ | 언어 | 설명 |",
            "|---|---|---|---|---|",
            (.repos[] | "| \(if .hl then "🔖 " else "" end)\(.repo) | +\(.period_stars) | \(.total_stars) | \(.language) | \((.description // "")[0:60]) |") )
         end)
      end)
    '
    ;;
esac
