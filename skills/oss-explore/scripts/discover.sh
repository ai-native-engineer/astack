#!/usr/bin/env bash
# oss-explore :: discover
# 기여 진입점 발굴: 비기너 친화 라벨이 붙은 "지금 잡을 수 있는" 열린 이슈를 찾는다.
# 기본 동작(기여자 관점): (1) 이미 PR이 연결된 이슈 제외 (2) max-age(기본 1년) 넘거나 blocked/wontfix/stale 제외
# (3) 비기너 라벨 동의어 ~10종을 OR로 검색. 결과는 최근 업데이트 순(또는 --sort).
#
# Usage: discover.sh [--language L] [--label L].. [--topic KW] [--limit N] [--min-stars N]
#                    [--max-age DAYS] [--stale-ok] [--include-linked] [--sort recent|comments-asc] [--json]
#   --language L      레포 주 언어 (python, typescript, rust, go ...)
#   --label L         검색 라벨 (반복). 미지정 시 비기너 라벨 동의어 사전 전체를 OR
#   --topic KW        이슈 제목/본문 키워드
#   --limit N         라벨당 검색 상한 (기본 30)
#   --min-stars N     레포 star 하한 (줄 때만 star 보강 → 양산/이벤트성 레포 제거, star순 정렬)
#   --max-age DAYS    이 일수보다 오래 전 생성된 이슈 제외 (기본 365)
#   --stale-ok        오래된/blocked/wontfix/stale 이슈도 포함 (max-age 해제)
#   --include-linked  이미 PR이 연결된 이슈도 포함 (기본은 제외)
#   --sort S          recent(기본) | comments-asc(미선점=댓글 적은 순 우선)
#   --curated         awesome-for-beginners(검증된 ~229 레포)만 시드로, 레포별 등재 라벨로 발굴 (--limit=레포수, 최대 40)
#   --top N           출력할 이슈 상한 (기본 20). 초과분은 푸터로 안내
#   --hot             이슈 대신 "good first issue ≥5개인 활성 레포"를 star순으로 (핫스팟 발굴)
#   --summary         발굴 결과를 언어별(레포수/이슈수)로 집계 (이슈 목록 대신)
#   --json            원시 JSON 출력
set -euo pipefail
command -v jq >/dev/null 2>&1 || { echo "error: jq is required; install jq and add it to PATH" >&2; exit 69; }

LANG_FILTER=""
TOPIC=""
LIMIT=30
MIN_STARS=0
MAX_AGE=365
STALE_OK=0
INCLUDE_LINKED=0
SORT=recent
CURATED=0
TOP=20
HOT=0
HOT_MIN=5
SUMMARY=0
OUT=md
LABELS=()
while [ $# -gt 0 ]; do
  case "$1" in
    --language) shift; LANG_FILTER="${1:?--language needs a value}" ;;
    --label) shift; LABELS+=("${1:?--label needs a value}") ;;
    --topic) shift; TOPIC="${1:?--topic needs a value}" ;;
    --limit) shift; LIMIT="${1:?--limit needs a value}" ;;
    --min-stars) shift; MIN_STARS="${1:?--min-stars needs a value}" ;;
    --max-age) shift; MAX_AGE="${1:?--max-age needs a value}" ;;
    --stale-ok) STALE_OK=1 ;;
    --include-linked) INCLUDE_LINKED=1 ;;
    --sort) shift; SORT="${1:?--sort needs a value}" ;;
    --curated) CURATED=1 ;;
    --top) shift; TOP="${1:?--top needs a value}" ;;
    --hot) HOT=1 ;;
    --summary) SUMMARY=1 ;;
    --json) OUT=json ;;
    -*) echo "unknown option: $1" >&2; exit 1 ;;
    *) TOPIC="$1" ;;
  esac
  shift
done

case "$LIMIT" in ''|*[!0-9]*) echo "error: --limit must be an integer from 1 to 1000" >&2; exit 1 ;; esac
[ "$LIMIT" -ge 1 ] && [ "$LIMIT" -le 1000 ] || { echo "error: --limit must be an integer from 1 to 1000" >&2; exit 1; }
case "$MIN_STARS" in ''|*[!0-9]*) echo "error: --min-stars must be a non-negative integer" >&2; exit 1 ;; esac
case "$MAX_AGE" in ''|*[!0-9]*) echo "error: --max-age must be a non-negative integer" >&2; exit 1 ;; esac
case "$TOP" in ''|*[!0-9]*) echo "error: --top must be a positive integer" >&2; exit 1 ;; esac
[ "$TOP" -ge 1 ] || { echo "error: --top must be a positive integer" >&2; exit 1; }
case "$SORT" in recent|comments-asc) ;; *) echo "error: --sort must be recent or comments-asc" >&2; exit 1 ;; esac

# --hot: 이슈가 아니라 "기여 기회(good first issue)가 많은 활성 레포"를 star순으로.
# gh search repos 의 네이티브 qualifier(--good-first-issues)를 쓴다 — 이슈를 다 긁어 세는 것보다 가볍다.
if [ "$HOT" = 1 ]; then
  hargs=(--good-first-issues ">=$HOT_MIN" --archived=false --visibility public --include-forks false --sort stars --limit "$LIMIT" --json fullName,stargazersCount,description,url,updatedAt)
  [ -n "$LANG_FILTER" ] && hargs+=(--language "$LANG_FILTER")
  [ "$MIN_STARS" -gt 0 ] && hargs+=(--stars ">=$MIN_STARS")
  HRESULT=$(gh search repos "${hargs[@]}" | jq --arg lang "$LANG_FILTER" --argjson min "$HOT_MIN" '
    { type: "discover-hot", query: { language: $lang, min_good_first_issues: $min },
      count: length,
      repos: [ .[] | { repo: .fullName, stars: .stargazersCount, description: (.description // ""), url, updated: (.updatedAt[0:10]) } ] }')
  if [ "$OUT" = json ]; then
    echo "$HRESULT"
  else
    echo "$HRESULT" | jq -r '
      "# 핫스팟 레포 \(.count)곳 · good first issue ≥\(.query.min_good_first_issues)"
        + (if .query.language != "" then " · lang=\(.query.language)" else "" end) + "\n",
      (if .count == 0 then "_조건에 맞는 레포가 없습니다._" else
        ( "| 레포 | ★ | 업데이트 | 설명 |", "|---|---|---|---|",
          (.repos[] | "| [\(.repo)](\(.url)) | \(.stars) | \(.updated) | \((.description)[0:50]) |") )
      end)'
  fi
  exit 0
fi

# 비기너 친화 라벨 동의어 사전 (난이도용 일반 라벨 — 특정 분야 하드코딩 아님)
[ ${#LABELS[@]} -eq 0 ] && LABELS=(
  "good first issue" "good-first-issue" "help wanted" "first-timers-only"
  "easy" "low-hanging-fruit" "beginner" "beginner-friendly" "starter" "contributor-friendly"
)

if [ "$STALE_OK" = 1 ]; then
  SINCE="2008-01-01"   # GitHub 창립 무렵 = 사실상 전체 (created:>= 토큰은 유지해 leading-dash 방지; 비현실적 과거 날짜는 GitHub이 0건 반환)
else
  SINCE=$(date -v-"${MAX_AGE}"d +%Y-%m-%d 2>/dev/null || date -d "-${MAX_AGE} days" +%Y-%m-%d)
fi

# query 조립: created:>= 를 항상 맨 앞에 둔다.
# (gh search 는 query가 '-'로 시작하면 플래그로 오인 → created: 로 시작해 leading-dash를 원천 차단)
build_query() {
  local q="created:>=$SINCE"
  [ -n "$TOPIC" ] && q="$q $TOPIC"
  [ "$INCLUDE_LINKED" = 0 ] && q="$q -linked:pr"
  [ "$STALE_OK" = 0 ] && q="$q -label:blocked -label:wontfix -label:stale"
  printf '%s' "$q"
}
QUERY=$(build_query)

search_label() {
  local label="$1"
  local args=(--state open --archived=false --visibility public --limit "$LIMIT" --json repository,title,url,labels,updatedAt,commentsCount)
  [ -n "$LANG_FILTER" ] && args+=(--language "$LANG_FILTER")
  gh search issues "$QUERY" --label "$label" "${args[@]}"
}

# 발굴: --curated 면 awesome-for-beginners 검증 레포 시드(레포별 등재 라벨), 아니면 비기너 라벨 사전 검색
ALL='[]'
if [ "$CURATED" = 1 ]; then
  CACHE_DIR="${XDG_CACHE_HOME:-$HOME/.cache}/oss-explore"
  mkdir -p "$CACHE_DIR"
  DATA="$CACHE_DIR/awesome-for-beginners.json"
  cache_valid() {
    jq -e '(.repositories | type) == "array"' "$1" >/dev/null 2>&1
  }
  refresh_cache() {
    local tmp
    tmp=$(mktemp "$CACHE_DIR/awesome-for-beginners.json.XXXXXX")
    if curl -fsSL https://raw.githubusercontent.com/MunGell/awesome-for-beginners/main/data.json -o "$tmp" 2>/dev/null \
      && cache_valid "$tmp"; then
      mv "$tmp" "$DATA"
      return
    fi
    if gh api repos/MunGell/awesome-for-beginners/contents/data.json --jq '.content' 2>/dev/null | base64 -d > "$tmp" \
      && cache_valid "$tmp"; then
      mv "$tmp" "$DATA"
      return
    fi
    rm -f "$tmp"
    return 1
  }
  # 6시간 캐시. 새 데이터는 검증한 뒤에만 원자적으로 교체한다.
  NEEDS_REFRESH=0
  cache_valid "$DATA" || NEEDS_REFRESH=1
  if [ "$NEEDS_REFRESH" = 0 ] && find "$DATA" -mmin +360 -print -quit 2>/dev/null | grep -q .; then
    NEEDS_REFRESH=1
  fi
  if [ "$NEEDS_REFRESH" = 1 ] && ! refresh_cache; then
    if cache_valid "$DATA"; then
      echo "warning: awesome-for-beginners cache refresh failed; using the existing valid cache" >&2
    else
      echo "error: could not refresh a valid awesome-for-beginners cache; check network access and GitHub authentication, then rerun" >&2
      exit 1
    fi
  fi
  REPO_LIMIT="$LIMIT"; [ "$REPO_LIMIT" -gt 40 ] && REPO_LIMIT=40
  # --language 로 technologies[] 필터 → "owner/repo<TAB>레포별 등재 라벨"
  REPOS_TSV=$(jq -r --arg lang "$LANG_FILTER" --argjson limit "$REPO_LIMIT" '
    [ .repositories[]
      | select(($lang == "") or ((.technologies // []) | map(ascii_downcase) | index($lang | ascii_downcase) != null))
      | "\((.link | sub("https?://github.com/"; "") | sub("/$"; "")))\t\(.label)" ]
    | .[:$limit][]' "$DATA")
  while IFS=$'\t' read -r repo label; do
    [ -n "$repo" ] && [ -n "$label" ] || continue
    part=$(gh search issues "$QUERY" --repo "$repo" --label "$label" --state open --archived=false --visibility public --limit 5 \
      --json repository,title,url,labels,updatedAt,commentsCount)
    ALL=$(jq -c -n --argjson a "$ALL" --argjson b "${part:-[]}" '$a + $b')
  done <<< "$REPOS_TSV"
else
  for label in "${LABELS[@]}"; do
    part=$(search_label "$label")
    ALL=$(jq -c -n --argjson a "$ALL" --argjson b "${part:-[]}" '$a + $b')
  done
fi

ISSUES=$(echo "$ALL" | jq '
  unique_by(.url)
  | map({ repo: .repository.nameWithOwner,
          title: .title,
          url: .url,
          labels: [ .labels[].name ],
          updated: (.updatedAt[0:10]),
          comments: (.commentsCount // 0) })')

# 정렬
case "$SORT" in
  comments-asc) ISSUES=$(echo "$ISSUES" | jq 'sort_by(.comments, .updated)') ;;
  *)            ISSUES=$(echo "$ISSUES" | jq 'sort_by(.updated) | reverse') ;;
esac

# star 하한이 주어지면: unique 레포 star 병렬 보강 → 필터 → star 내림차순
if [ "$MIN_STARS" -gt 0 ] && jq -e 'length > 0' <<<"$ISSUES" >/dev/null; then
  STARTSV=$(echo "$ISSUES" | jq -r '[.[].repo] | unique | .[]' | xargs -P 10 -n 1 sh -c '
    if ! gh repo view "$1" --json stargazerCount --jq "[\"$1\", (.stargazerCount|tostring)] | @tsv"; then
      echo "error: gh repo view failed for $1 while resolving --min-stars; check repository access and GitHub authentication" >&2
      exit 1
    fi' _)
  STARMAP=$(echo "$STARTSV" | jq -R 'split("\t") | select(length==2) | {(.[0]): (.[1]|tonumber)}' | jq -s 'add // {}')
  ISSUES=$(echo "$ISSUES" | jq --argjson m "$STARMAP" --argjson min "$MIN_STARS" '
    map(.stars = ($m[.repo] // 0)) | map(select(.stars >= $min)) | sort_by(-.stars)')
fi

# --summary: 이슈 목록 대신 "언어별(레포수/이슈수)" 집계로 — repo primaryLanguage 보강 후 group
if [ "$SUMMARY" = 1 ]; then
  LANGMAP='{}'
  if jq -e 'length > 0' <<<"$ISSUES" >/dev/null; then
    LANGTSV=$(echo "$ISSUES" | jq -r '[.[].repo] | unique | .[]' | xargs -P 10 -n 1 sh -c '
      if ! gh repo view "$1" --json primaryLanguage --jq "[\"$1\", (.primaryLanguage.name // \"Unknown\")] | @tsv"; then
        echo "error: gh repo view failed for $1 while generating --summary; check repository access and GitHub authentication" >&2
        exit 1
      fi' _)
    LANGMAP=$(echo "$LANGTSV" | jq -R 'split("\t") | select(length==2) | {(.[0]): .[1]}' | jq -s 'add // {}')
  fi
  SUMRESULT=$(echo "$ISSUES" | jq --argjson m "$LANGMAP" '
    map(.lang = ($m[.repo] // "Unknown"))
    | { type: "discover-summary", total_issues: length,
        languages: ( group_by(.lang)
          | map({ language: .[0].lang, repos: ([.[].repo] | unique | length), issues: length })
          | sort_by(-.issues) ) }')
  if [ "$OUT" = json ]; then
    echo "$SUMRESULT"
  else
    echo "$SUMRESULT" | jq -r '
      "# 발굴 언어별 집계 · 총 \(.total_issues) 이슈\n",
      "| 언어 | 레포 | 이슈 |", "|---|---|---|",
      (.languages[] | "| \(.language) | \(.repos) | \(.issues) |")'
  fi
  exit 0
fi

# 출력 상한 — 총 발견 수(TOTAL_FOUND)는 보존하고 상위 TOP건만 표시
TOTAL_FOUND=$(echo "$ISSUES" | jq 'length')
ISSUES=$(echo "$ISSUES" | jq --argjson n "$TOP" '.[0:$n]')

RESULT=$(jq -n \
  --argjson issues "$ISSUES" \
  --arg lang "$LANG_FILTER" \
  --arg topic "$TOPIC" \
  --argjson min "$MIN_STARS" \
  --arg since "$SINCE" \
  --argjson stale "$STALE_OK" \
  --argjson linked "$INCLUDE_LINKED" \
  --argjson curated "$CURATED" \
  --argjson total "$TOTAL_FOUND" \
  --argjson labels "$(printf '%s\n' "${LABELS[@]}" | jq -R . | jq -s .)" '
  { type: "discover",
    query: { language: $lang, topic: $topic, labels: $labels, min_stars: $min,
             since: $since, exclude_linked: ($linked == 0), exclude_stale: ($stale == 0),
             curated: ($curated == 1) },
    total: $total,
    count: ($issues | length),
    issues: $issues }')

case "$OUT" in
  json) echo "$RESULT" ;;
  md)
    echo "$RESULT" | jq -r '
      "# 기여 진입점 \(.count)건  "
        + (if .query.curated then "· 큐레이션(awesome-for-beginners) " else "" end)
        + (if .query.language != "" then "· lang=\(.query.language) " else "" end)
        + (if .query.topic != "" then "· \"\(.query.topic)\" " else "" end)
        + (if .query.min_stars > 0 then "· ★≥\(.query.min_stars) " else "" end)
        + (if .query.exclude_linked then "· PR미연결 " else "" end)
        + (if .query.exclude_stale then "· \(.query.since) 이후" else "" end) + "\n",
      "_💬=댓글수(🆕0=아직 아무도 안 집은 이슈)_\n",
      (if .count == 0 then "_조건에 맞는 열린 이슈가 없습니다._"
       elif .query.min_stars > 0 then
        ( "| 레포 | ★ | 💬 | 이슈 | 라벨 | 업데이트 |",
          "|---|---|---|---|---|---|",
          (.issues[] | "| \(.repo) | \(.stars) | \(if .comments==0 then "🆕0" else (.comments|tostring) end) | [\((.title)[0:44])](\(.url)) | \(.labels | join(", ")) | \(.updated) |") )
       else
        ( "| 레포 | 💬 | 이슈 | 라벨 | 업데이트 |",
          "|---|---|---|---|---|",
          (.issues[] | "| \(.repo) | \(if .comments==0 then "🆕0" else (.comments|tostring) end) | [\((.title)[0:50])](\(.url)) | \(.labels | join(", ")) | \(.updated) |") )
      end),
      (if (.total // .count) > .count then "\n_총 \(.total)건 중 상위 \(.count) — 더 보려면 `--top \(.total)`_" else empty end)
    '
    ;;
esac
