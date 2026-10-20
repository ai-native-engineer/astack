# KIPRIS 법적 상태 현재정보조회

> provider: plus.kipris.or.kr
> official: https://plus.kipris.or.kr/portal/popup/DBII_000000000000540/SC002/ADI_0000000000016533/apiDescriptionSearch.do
> checked: 2026-06-28 · 상태: 실제 호출 성공

## 언제 쓰나

특허·실용, 상표, 디자인의 출원번호로 현재 법적 상태를 확인할 때 쓴다. 등록, 심결, 연차료 미납, 권리 소멸 같은 상태 코드·상태명·상태일자가 필요할 때 먼저 조회한다.

## Endpoint

- base: `http://plus.kipris.or.kr/openapi/rest`
- serviceId: `legStatusInfoSearchService`
- operation: `legalStatusBasicInfo`
- method: `GET`
- detail id: `DBII_000000000000540` / `SC002` / `ADI_0000000000016533`

## 키

- env: `KIPRIS_API_KEY`
- query parameter: `accessKey`
- 주입 예: `agents-env run KIPRIS_API_KEY -- <명령>`

## 호출 예시

```bash
curl -sG "http://plus.kipris.or.kr/openapi/rest/legStatusInfoSearchService/legalStatusBasicInfo" \
  --data-urlencode "applicationNumber=1020080025578" \
  --data-urlencode "accessKey=$KIPRIS_API_KEY"
```

## 필수/주요 파라미터

| 이름 | 의미 | 형식·예 |
|---|---|---|
| `applicationNumber` | 출원번호 | `1020080025578` |
| `accessKey` | KIPRIS Plus 서비스키 | `$KIPRIS_API_KEY` |

## 응답 핵심 필드

| 필드 | 의미 |
|---|---|
| `resultCode` / `resultMsg` | 처리 결과. 검증 호출에서는 `00` / `success` |
| `appReferenceNumber` | 출원참조번호 |
| `applicationNumber` | 출원번호 |
| `legalStatusCode` | 법적 상태 코드 |
| `legalStatusName` / `legalStatusEngName` | 법적 상태명 한글 / 영문 |
| `legalStatusDate` | 법적 상태일자, `YYYYMMDD` |
| `legalStatusComment` / `legalStatusEngComment` | 상태 설명 한글 / 영문 |

## 페이징

없음. 출원번호 단건 현재 상태 조회다.

## 함정

- 이 operation은 `accessKey`를 쓴다. 같은 서비스 안의 `getLegStatusHistoryInfoSearch`는 `kipo-api/kipi` + `ServiceKey` 샘플이므로 패턴을 섞지 않는다.
- 팝업의 "요청 주소" 섹션은 `kipo-api/kipi`를 보이지만, 2026-06-28 실호출 성공 기준은 "입력값 예시(Request Sample)"의 `openapi/rest` URL이다.
- `applicationNumber`는 하이픈 없이 보낸다. 예: `10-2008-0025578`이 아니라 `1020080025578`.
- 법적 상태명은 최신 권리 상태만 요약한다. 변경 이력 전체가 필요하면 같은 서비스의 `getLegStatusHistoryInfoSearch` 또는 ST.27/ST.87 세부 operation을 검토한다.
