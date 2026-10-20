# KIPRIS 특허·실용 출원인명 검색

> provider: plus.kipris.or.kr
> official: https://plus.kipris.or.kr/portal/popup/DBII_000000000000001/SC002/ADI_0000000000015118/apiDescriptionSearch.do
> checked: 2026-06-28 · 상태: 실제 호출 성공

## 언제 쓰나

특허·실용신안 공개·등록공보에서 회사명, 출원인명, 권리 후보명으로 특허 목록을 찾을 때 쓴다. 기업 리서치에서 KIPRIS 특허 원장, 출원번호, 등록상태, IPC, 초록을 수집할 때 우선 사용한다.

## Endpoint

- base: `http://plus.kipris.or.kr/openapi/rest`
- serviceId: `patUtiModInfoSearchSevice`
- operation: `applicantNameSearchInfo`
- method: `GET`
- detail id: `DBII_000000000000001` / `SC002` / `ADI_0000000000015118`

## 키

- env: `KIPRIS_API_KEY`
- query parameter: `accessKey`
- 주입 예: `agents-env run KIPRIS_API_KEY -- <명령>`

## 호출 예시

```bash
curl -sG "http://plus.kipris.or.kr/openapi/rest/patUtiModInfoSearchSevice/applicantNameSearchInfo" \
  --data-urlencode "applicant=채널코퍼레이션" \
  --data-urlencode "docsStart=1" \
  --data-urlencode "docsCount=100" \
  --data-urlencode "accessKey=$KIPRIS_API_KEY"
```

## 필수/주요 파라미터

| 이름 | 의미 | 형식·예 |
|---|---|---|
| `applicant` | 출원인명 검색어 | `채널코퍼레이션` |
| `docsStart` | 페이지번호 | `1` |
| `docsCount` | 페이지당 건수 | `100` |
| `accessKey` | KIPRIS Plus 서비스키 | `$KIPRIS_API_KEY` |

## 응답 핵심 필드

| 필드 | 의미 |
|---|---|
| `TotalSearchCount` | 전체 검색 건수 |
| `ApplicationNumber` / `ApplicationDate` | 출원번호 / 출원일 |
| `InventionName` | 발명의 명칭 |
| `Applicant` | 출원인 |
| `RegistrationNumber` / `RegistrationDate` / `RegistrationStatus` | 등록번호 / 등록일 / 등록상태 |
| `InternationalpatentclassificationNumber` | IPC 코드 |
| `Abstract` | 초록 |

## 페이징

`docsStart`가 페이지번호다. `docsCount`는 페이지당 건수이며 호출 전 전체 건수는 `TotalSearchCount`로 확인한다.

## 함정

- 이 operation은 `ServiceKey`가 아니라 `accessKey`를 쓴다.
- base는 `kipo-api/kipi`가 아니라 `openapi/rest`다. 팝업의 Request Sample을 기준으로 호출한다.
- 회사명 부분일치가 넓게 걸릴 수 있다. 정규화 단계에서 `Applicant`가 대상 법인명 또는 확인된 과거 법인명과 맞는지 필터링한다.
