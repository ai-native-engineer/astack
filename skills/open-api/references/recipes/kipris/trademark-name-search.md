# KIPRIS 상표명 검색

> provider: plus.kipris.or.kr
> official: https://plus.kipris.or.kr/portal/popup/DBII_000000000000012/SC002/ADI_0000000000015174/apiDescriptionSearch.do
> checked: 2026-06-28 · 상태: 실제 호출 성공

## 언제 쓰나

브랜드명, 서비스명, 제품명 기준으로 상표 출원·등록 현황을 찾을 때 쓴다. 회사명 검색으로 누락될 수 있는 서비스 상표, 예를 들어 `채널톡`, `ALF`, `ZOYI` 같은 이름을 확인할 때 사용한다.

## Endpoint

- base: `http://plus.kipris.or.kr/openapi/rest`
- serviceId: `trademarkInfoSearchService`
- operation: `trademarkNameSearchInfo`
- method: `GET`
- detail id: `DBII_000000000000012` / `SC002` / `ADI_0000000000015174`

## 키

- env: `KIPRIS_API_KEY`
- query parameter: `accessKey`
- 주입 예: `agents-env run KIPRIS_API_KEY -- <명령>`

## 호출 예시

```bash
curl -sG "http://plus.kipris.or.kr/openapi/rest/trademarkInfoSearchService/trademarkNameSearchInfo" \
  --data-urlencode "trademarkName=채널톡" \
  --data-urlencode "docsStart=1" \
  --data-urlencode "docsCount=100" \
  --data-urlencode "accessKey=$KIPRIS_API_KEY"
```

## 필수/주요 파라미터

| 이름 | 의미 | 형식·예 |
|---|---|---|
| `trademarkName` | 상표명 검색어 | `채널톡` |
| `docsStart` | 페이지번호 | `1` |
| `docsCount` | 페이지당 건수 | `100` |
| `accessKey` | KIPRIS Plus 서비스키 | `$KIPRIS_API_KEY` |

## 응답 핵심 필드

| 필드 | 의미 |
|---|---|
| `TotalSearchCount` | 전체 검색 건수 |
| `ApplicationNumber` / `ApplicationDate` | 출원번호 / 출원일 |
| `Title` | 상표명 |
| `ApplicantName` | 출원인명 |
| `ApplicationStatus` | 출원/공고/등록/거절 등 상태 |
| `GoodClassificationCode` | 상품분류 코드 |
| `RegistrationNumber` / `RegistrationDate` | 등록번호 / 등록일 |
| `ViennaCode` | 도형분류 코드 |

## 페이징

`docsStart`가 페이지번호다. `docsCount`는 페이지당 건수이며 호출 전 전체 건수는 `TotalSearchCount`로 확인한다.

## 함정

- 이 operation은 `ServiceKey`가 아니라 `accessKey`를 쓴다.
- 상표명은 동음이의·타사 상표가 섞일 수 있다. 화면에 병합하기 전 `ApplicantName`을 대상 법인명으로 재확인한다.
