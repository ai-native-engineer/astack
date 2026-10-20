# KIPRIS 특허·실용 출원번호 검색

> provider: plus.kipris.or.kr
> official: https://plus.kipris.or.kr/portal/popup/DBII_000000000000001/SC002/ADI_0000000000010163/apiDescriptionSearch.do
> checked: 2026-06-28 · 상태: 실제 호출 성공

## 언제 쓰나

특허·실용신안 출원번호로 검색 결과 1건 이상을 조회할 때 쓴다. 상세 전체 필드가 필요하면 결과의 출원번호로 `getBibliographyDetailInfoSearch`를 이어서 호출한다.

## Endpoint

- base: `http://plus.kipris.or.kr/openapi/rest`
- serviceId: `patUtiModInfoSearchSevice`
- operation: `applicationNumberSearchInfo`
- method: `GET`
- detail id: `DBII_000000000000001` / `SC002` / `ADI_0000000000010163`

## 키

- env: `KIPRIS_API_KEY`
- query parameter: `accessKey`
- 주입 예: `agents-env run KIPRIS_API_KEY -- <명령>`

## 호출 예시

```bash
curl -sG "http://plus.kipris.or.kr/openapi/rest/patUtiModInfoSearchSevice/applicationNumberSearchInfo" \
  --data-urlencode "applicationNumber=1020050050026" \
  --data-urlencode "docsStart=1" \
  --data-urlencode "accessKey=$KIPRIS_API_KEY"
```

## 필수/주요 파라미터

| 이름 | 의미 | 형식·예 |
|---|---|---|
| `applicationNumber` | 출원번호 | `1020050050026` |
| `docsStart` | 페이지번호 | `1` |
| `accessKey` | KIPRIS Plus 서비스키 | `$KIPRIS_API_KEY` |

## 응답 핵심 필드

| 필드 | 의미 |
|---|---|
| `TotalSearchCount` | 전체 건수 |
| `SearchStartNumber` | 페이지번호 |
| `ApplicationNumber` / `ApplicationDate` | 출원번호 / 출원일 |
| `OpeningNumber` / `OpeningDate` | 공개번호 / 공개일 |
| `RegistrationNumber` / `RegistrationDate` / `RegistrationStatus` | 등록번호 / 등록일 / 등록상태 |
| `InventionName` | 발명의 명칭 |
| `Applicant` | 출원인 |
| `InternationalpatentclassificationNumber` | IPC 코드 |

## 페이징

`docsStart`가 페이지번호다. `docsCount`는 페이지당 건수이며 기본 30, 최대 500이다.

## 함정

- 이 operation은 `ServiceKey`가 아니라 `accessKey`를 쓴다.
- base도 `kipo-api/kipi`가 아니라 `openapi/rest`다. 팝업의 Request Sample을 기준으로 호출한다.
