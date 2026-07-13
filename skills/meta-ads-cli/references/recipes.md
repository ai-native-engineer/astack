# Meta Ads CLI — 실전 워크플로

명령 카탈로그는 `commands.md`. 여기는 "어떻게 엮는가"와 스크립트 함정.

## 목차

- 1. 필요한 ID 찾기
- 2. 캠페인 end-to-end 생성
- 3. 전환 추적 셋업 (픽셀)
- 4. 성과 분석 (insights)
- 5. 스크립트 자동화
- 6. 정리 (cleanup)

## 1. 필요한 ID 찾기

```bash
meta ads adaccount list   # ad account id → AD_ACCOUNT_ID
meta ads page list        # 비즈니스 페이지 id → creative의 --page-id
# BUSINESS_ID는 보통 ad account에서 자동 해결, 필요 시 export BUSINESS_ID=...
```

## 2. 캠페인 end-to-end 생성

생성 순서는 **campaign → adset → creative → ad**, 전부 PAUSED로 만들어진다. 마지막에 ACTIVE로 게시(=과금 시작).

```bash
# 1) 캠페인 (예산=통화 minor unit; USD 5000=$50, KRW 5000=5,000원)
meta ads campaign create --name "My Campaign" --objective OUTCOME_TRAFFIC --daily-budget 5000
# 2) 광고세트 — 캠페인에 예산 있으면 여기 예산 생략(CBO)
meta ads adset create <CAMPAIGN_ID> --name "US Audience" \
  --optimization-goal LINK_CLICKS --billing-event IMPRESSIONS --targeting-countries US
# 3) 크리에이티브 — --page-id 필수
meta ads creative create --name "Hero" --page-id <PAGE_ID> --image ./banner.jpg \
  --body "Check our deals!" --title "Shop Now" --link-url https://example.com --call-to-action SHOP_NOW
# 4) 광고 — adset에 creative 연결
meta ads ad create <ADSET_ID> --name "Hero Ad" --creative-id <CREATIVE_ID>
# 5) 게시 (비용 발생 — 사용자 승인 후)
meta ads campaign update <CAMPAIGN_ID> --status ACTIVE
meta ads adset update <ADSET_ID> --status ACTIVE
meta ads ad update <AD_ID> --status ACTIVE
```

크리에이티브 포맷은 플래그로 자동 결정: `--video`→비디오, `--link-url`만→링크, 둘 다 없으면→페이지 포토포스트. 인스타 노출은 `--instagram-actor-id`. 여러 소재 A/B는 DCO(복수형 `--images/--titles/--bodies`).

## 3. 전환 추적 셋업 (픽셀)

```bash
meta ads dataset create --name "Website Pixel"          # 픽셀 생성
meta ads dataset connect <PIXEL_ID> --ad-account-id <AD_ACCOUNT_ID>   # 계정에 연결
# (선택) 카탈로그 제품 전환: --catalog-id <CATALOG_ID>
meta ads campaign create --name "Sales" --objective OUTCOME_SALES
meta ads adset create <CAMPAIGN_ID> --name "Purchases" \
  --optimization-goal OFFSITE_CONVERSIONS --billing-event IMPRESSIONS \
  --pixel-id <PIXEL_ID> --custom-event-type PURCHASE --targeting-countries US
meta ads ad create <ADSET_ID> --name "Conv Ad" --creative-id <CREATIVE_ID> --pixel-id <PIXEL_ID>
```

전환 캠페인 공식: objective `OUTCOME_SALES` + optimization-goal `OFFSITE_CONVERSIONS` + adset/ad에 `--pixel-id`.

## 4. 성과 분석 (insights)

기본 기간 `last_30d`, 기본 지표 `spend,impressions,clicks,ctr,cpc,reach`.

```bash
meta ads insights get --campaign-id <ID> --date-preset last_7d
meta ads insights get --breakdown publisher_platform --breakdown age   # 분해(반복 가능)
meta ads insights get --campaign-id <ID> --fields spend,conversions,purchase_roas --sort spend_descending
meta ads insights get --date-preset last_30d --time-increment daily --fields spend   # 일별 추이
```

- **`ACTIVE`인데 `{"data":[]}`**: 캠페인이 켜져 있어도 집행 기간이 조회 범위(기본 `last_30d`) 밖이면 빈 결과다. 시작일이 오래된 캠페인은 `--since/--until`로 전체 기간을 재조회하고, `--time-increment daily`로 실제 집행일을 확인.
- **종료된/과거 캠페인**: `--date-preset`엔 `maximum`이 없다. 임의 기간은 `--since YYYY-MM-DD --until YYYY-MM-DD`(둘이 함께 쓰여 date-preset을 덮어씀).
- breakdown: `age` `gender` `country` `publisher_platform` `device_platform` `platform_position` `impression_device`.
- 자주 쓰는 지표: `spend impressions reach clicks ctr cpc cpm frequency conversions cost_per_conversion purchase_roas`.

## 5. 스크립트 자동화

```bash
# JSON + jq로 ID 추출해 반복
CAMPAIGN_IDS=$(meta --output json ads campaign list | jq -r '.[].id')
for id in $CAMPAIGN_IDS; do
  meta ads insights get --campaign-id "$id" --fields spend,purchase_roas
done

# 비대화형: 프롬프트 전면 억제
meta --no-input ads campaign delete <CAMPAIGN_ID> --force

# exit code로 분기
meta auth status >/dev/null 2>&1 || echo "토큰 없음/만료"
```

**exit code**: `0` 성공 · `1` 일반 오류 · `2` 사용법/인자 오류 · `3` 인증 오류 · `4` API 오류 · `5` 리소스 없음.

### ⚠️ 자동화 핵심 함정 — 변경 명령 출력은 순수 JSON이 아님
`-o json`이어도 `create/update/delete`는 앞에 `Created campaign 'X' (ID: ...)` 같은 사람용 메시지 줄을 먼저 찍는다 → `json.load`/`jq`가 깨진다. 조회(`list`/`get`)는 깨끗한 JSON. 생성물 ID는 둘 중 하나로 잡는다:

```bash
OUT=$(meta ads campaign create --name X --objective OUTCOME_TRAFFIC)
CID=$(printf '%s' "$OUT" | grep -oE '[0-9]{15,}' | head -1)   # 메시지에서 ID 추출
# 또는: 생성 후 list로 이름 매칭해 id 재조회 (list는 순수 json)
```

## 6. 정리 (cleanup)

```bash
meta ads campaign delete <CAMPAIGN_ID> --force   # 하위 adset·ad까지 cascade 삭제
meta ads adset delete <ADSET_ID> --force         # 하위 ad까지
meta ads creative delete <CREATIVE_ID> --force   # 단, active 광고가 쓰는 creative는 삭제 불가
meta ads dataset disconnect <PIXEL_ID> --ad-account-id <AD_ACCOUNT_ID> --force
```

동작만 검증하려면: `create`(기본 PAUSED) → `get`/`list`로 확인 → `delete --force`. PAUSED라 노출·과금 없음.
