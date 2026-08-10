#!/usr/bin/env bash
# oss-explore :: contributions
# 머지된 PR 기준으로 "본인 소유가 아닌" 레포 기여 내역을 정리한다.
# 소속 조직(팀 프로젝트) vs 순수 외부 OSS로 분류하고, 외부는 star 순으로 하이라이트.
#
# Usage: contributions.sh [username] [--json|--html] [--limit N]
#   username   생략 또는 @me 면 현재 gh 로그인 사용
#   --json           원시 JSON 출력 (render_html.py 입력 포맷)
#   --html           HTML 리포트 생성 후 open
#   --emit-markdown  순수 외부 OSS 기여를 shields.io 배지 테이블(마크다운)로 — 프로필 README/이력서용
#   --limit N        머지 PR 검색 상한 (기본 1000, gh search 최대 1000)
set -euo pipefail
command -v jq >/dev/null 2>&1 || { echo "error: jq is required; install jq and add it to PATH" >&2; exit 69; }

OUT=md
LIMIT=1000
USER_ARG=""
while [ $# -gt 0 ]; do
  case "$1" in
    --json) OUT=json ;;
    --html) OUT=html ;;
    --emit-markdown) OUT=markdown ;;
    --limit) shift; LIMIT="${1:?--limit needs a value}" ;;
    -*) echo "unknown option: $1" >&2; exit 1 ;;
    *) [ -z "$USER_ARG" ] || { echo "error: only one username is allowed" >&2; exit 1; }; USER_ARG="$1" ;;
  esac
  shift
done

case "$LIMIT" in ''|*[!0-9]*) echo "error: --limit must be an integer from 1 to 1000" >&2; exit 1 ;; esac
[ "$LIMIT" -ge 1 ] && [ "$LIMIT" -le 1000 ] || { echo "error: --limit must be an integer from 1 to 1000" >&2; exit 1; }

# username 해석: 조회 대상이 "현재 로그인 사용자"면 user/orgs(비공개 멤버십 포함),
# 다른 사람이면 users/<user>/orgs(공개 멤버십만 — GitHub API의 본질적 제약).
# username을 명시해도 본인이면 user/orgs를 쓰는 게 핵심(흔한 함정).
LOGIN=$(gh api user --jq .login)
if [ -z "$USER_ARG" ] || [ "$USER_ARG" = "@me" ]; then
  USER="$LOGIN"
else
  USER=$(gh api "users/$USER_ARG" --jq .login)
fi
if [ "$USER" = "$LOGIN" ]; then
  ORG_ENDPOINT="user/orgs"
else
  ORG_ENDPOINT="users/$USER/orgs"
fi

# 소속 조직 로그인 목록 (페이지네이션 대응). 실패를 빈 조직으로 오인하지 않는다.
if ! ORGS_JSON=$(gh api --paginate "$ORG_ENDPOINT" --jq '.[].login' | jq -R . | jq -s .); then
  echo "error: unable to load organization memberships for $USER" >&2
  exit 1
fi

# 머지 PR → 외부 레포별 카운트 (본인 소유 제외) + 조직 여부 플래그
PRS=$(gh search prs --author="$USER" --merged --visibility public --limit "$LIMIT" --json repository)
SEARCHED=$(echo "$PRS" | jq 'length')
BASE=$(echo "$PRS" | jq --arg u "$USER" --argjson orgs "$ORGS_JSON" '
      ($orgs | map(ascii_downcase)) as $orgs_lower
      |
      [ .[].repository.nameWithOwner ]
      | map(select((ascii_downcase | startswith(($u | ascii_downcase) + "/")) | not))
      | group_by(.)
      | map({ repo: .[0], prs: length, owner: (.[0] | split("/")[0]) })
      | map(. + { is_org: ((.owner | ascii_downcase) as $o | ($orgs_lower | index($o)) != null) })
    ')

# 순수 외부 레포: star/description 보강 후 star 내림차순
EXTERNAL=$(echo "$BASE" | jq -r '.[] | select(.is_org==false) | .repo' | while read -r repo; do
  [ -z "$repo" ] && continue
  prs=$(echo "$BASE" | jq --arg r "$repo" '.[] | select(.repo==$r) | .prs')
  if meta=$(gh repo view "$repo" --json stargazerCount,description,url 2>/dev/null); then
    jq -c -n --arg r "$repo" --argjson m "$meta" --argjson prs "$prs" '
      { repo: $r, prs: $prs,
        stars: ($m.stargazerCount // 0),
        description: ($m.description // ""),
        url: ($m.url // ("https://github.com/" + $r)) }'
  else
    jq -c -n --arg r "$repo" --argjson prs "$prs" '
      { repo: $r, prs: $prs, stars: null, description: "",
        url: ("https://github.com/" + $r), metadata_unavailable: true }'
  fi
done | jq -s 'sort_by([if .metadata_unavailable then 1 else 0 end, -(.stars // 0)])')
[ -z "$EXTERNAL" ] && EXTERNAL='[]'
METADATA_FAILURES=$(echo "$EXTERNAL" | jq '[.[] | select(.metadata_unavailable == true)] | length')
[ "$METADATA_FAILURES" -eq 0 ] || echo "warning: repository metadata lookup failed for $METADATA_FAILURES external repository/repositories" >&2

# 소속 조직: org별 그룹 (조직 내 레포는 PR 순)
ORG_GROUPS=$(echo "$BASE" | jq '
  [ .[] | select(.is_org==true) ]
  | group_by(.owner)
  | map({ org: .[0].owner,
          prs: (map(.prs) | add),
          repos: (sort_by(-.prs) | map({repo, prs})) })
  | sort_by(-.prs)')

TOTAL_MERGED=$(echo "$BASE" | jq '(map(.prs) | add) // 0')
EXT_COUNT=$(echo "$EXTERNAL" | jq 'length')
ORG_COUNT=$(echo "$ORG_GROUPS" | jq 'length')

RESULT=$(jq -n \
  --arg user "$USER" \
  --arg gen "$(date '+%Y-%m-%d %H:%M')" \
  --argjson external "$EXTERNAL" \
  --argjson orgs "$ORG_GROUPS" \
  --argjson tm "$TOTAL_MERGED" \
  --argjson ec "$EXT_COUNT" \
  --argjson oc "$ORG_COUNT" \
  --argjson searched "$SEARCHED" \
  --argjson metadata_failures "$METADATA_FAILURES" \
  --argjson limit "$LIMIT" '
  { type: "contributions", user: $user, generated: $gen,
    summary: { merged_prs: $tm, external_repos: $ec, org_groups: $oc,
               search_limit: $limit, limit_reached: ($searched >= $limit),
               metadata_lookup_failures: $metadata_failures },
    external: $external, orgs: $orgs }')

case "$OUT" in
  json)
    echo "$RESULT"
    ;;
  markdown)
    # 프로필 README/이력서에 붙이는 포트폴리오 테이블 (순수 외부 OSS만, star순). 배지는 shields.io 실시간.
    echo "$RESULT" | jq -r '
      "## Open-source contributions — \(.user)\n",
      (if .summary.limit_reached then "_GitHub 검색 상한 \(.summary.search_limit)건에 도달해 일부 기여가 빠질 수 있습니다._\n" else empty end),
      (if .summary.metadata_lookup_failures > 0 then "_레포 메타데이터 조회 실패 \(.summary.metadata_lookup_failures)건: 별 수와 설명 일부를 확인할 수 없습니다._\n" else empty end),
      (if (.external | length) == 0 then "_순수 외부 OSS 기여 없음_" else
        ( "| Repository | Stars | Merged PRs |",
          "|---|---|---|",
          (.external[] | "| [\(.repo)](\(.url)) | " + (if .stars == null then "?" else "![stars](https://img.shields.io/github/stars/\(.repo)?style=flat&label=%E2%98%85)" end) + " | \(.prs) |") )
      end)'
    ;;
  html)
    SELF="$(cd "$(dirname "$0")" && pwd)"
    f="${TMPDIR:-/tmp}/oss-explore-${USER}.html"
    echo "$RESULT" | python3 "$SELF/render_html.py" > "$f"
    echo "HTML 리포트: $f"
    open "$f" 2>/dev/null || true
    ;;
  md)
    echo "$RESULT" | jq -r '
      "# \(.user) — 오픈소스 기여 내역\n",
      "머지 PR \(.summary.merged_prs)건 · 순수 외부 OSS \(.summary.external_repos)곳 · 소속 조직 \(.summary.org_groups)곳\n",
      (if .summary.limit_reached then "_GitHub 검색 상한 \(.summary.search_limit)건에 도달해 일부 기여가 빠질 수 있습니다._\n" else empty end),
      (if .summary.metadata_lookup_failures > 0 then "_레포 메타데이터 조회 실패 \(.summary.metadata_lookup_failures)건: 별 수와 설명 일부를 확인할 수 없습니다._\n" else empty end),
      "## 순수 외부 OSS 기여 (star 순)\n",
      (if (.external | length) == 0 then "_없음_\n" else
        ( "| 레포 | 머지 PR | ⭐ | 설명 |",
          "|---|---|---|---|",
          (.external[] | "| \(.repo) | \(.prs) | " + (if .stars == null then "?" else (.stars | tostring) end) + " | \((.description // "")[0:60]) |") )
      end),
      "\n## 소속 조직 (팀/회사 프로젝트)\n",
      (if (.orgs | length) == 0 then "_없음_" else
        (.orgs[] | "- **\(.org)** (\(.prs) PR): " +
          ([.repos[] | "\((.repo | split("/")[1]))(\(.prs))"] | join(", ")))
      end)
    '
    ;;
esac
