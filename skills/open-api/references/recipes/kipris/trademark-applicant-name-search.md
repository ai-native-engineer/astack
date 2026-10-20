# KIPRIS 상표 출원인명 검색

> provider: plus.kipris.or.kr
> official: https://plus.kipris.or.kr/portal/popup/DBII_000000000000012/SC002/ADI_0000000000015186/apiDescriptionSearch.do
> checked: 2026-06-28 · 상태: 실제 호출 성공

## 언제 쓰나

상표 출원 속보에서 회사명, 출원인명, 특허고객번호 기준으로 상표 목록을 찾을 때 쓴다. SaaS·브랜드 기업의 제품명, 서비스명, 상표 상태, 상품분류 코드를 수집할 때 사용한다.

## Endpoint

- base: `http://plus.kipris.or.kr/openapi/rest`
- serviceId: `trademarkInfoSearchService`
- operation: `applicantNamesearchInfo`
- method: `GET`
- detail id: `DBII_000000000000012` / `SC002` / `ADI_0000000000015186`

## 키

- env: `KIPRIS_API_KEY`
- query parameter: `accessKey`
- 주입 예: `agents-env run KIPRIS_API_KEY -- <명령>`

## 호출 예시

```bash
curl -sG "http://plus.kipris.or.kr/openapi/rest/trademarkInfoSearchService/applicantNamesearchInfo" \
  --data-urlencode "applicantName=채널코퍼레이션" \
  --data-urlencode "docsStart=1" \
  --data-urlencode "docsCount=100" \
  --data-urlencode "accessKey=$KIPRIS_API_KEY"
```

## 필수/주요 파라미터

| 이름 | 의미 | 형식·예 |
|---|---|---|
| `applicantName` | 출원인명 또는 특허고객번호 검색어 | `채널코퍼레이션` |
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
- operation 이름은 공식 표기 그대로 `applicantNamesearchInfo`이며 `search`의 대소문자를 임의 수정하지 않는다.
- 출원인명 부분일치가 넓게 걸릴 수 있다. 정규화 단계에서 `ApplicantName` 기준으로 대상 법인명과 일치 여부를 다시 필터링한다.
