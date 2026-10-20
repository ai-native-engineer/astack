# KIPRIS 권리자변동정보

> provider: plus.kipris.or.kr
> official: https://plus.kipris.or.kr/portal/popup/DBII_000000000000541/SC002/ADI_0000000000016528/apiDescriptionSearch.do
> checked: 2026-06-28 · 상태: 실제 호출 성공

## 언제 쓰나

등록번호로 현재·과거 권리자란, 발명자, 의무자 등 권리자 변동 관련자를 확인할 때 쓴다. 특허·실용뿐 아니라 KIPRIS 권리자 변동 이력 서비스의 기본 권리자 정보 확인에 쓴다.

## Endpoint

- base: `http://plus.kipris.or.kr/openapi/rest`
- serviceId: `RightHolderService`
- operation: `rightHolderInfo`
- method: `GET`
- detail id: `DBII_000000000000541` / `SC002` / `ADI_0000000000016528`

## 키

- env: `KIPRIS_API_KEY`
- query parameter: `accessKey`
- 주입 예: `agents-env run KIPRIS_API_KEY -- <명령>`

## 호출 예시

```bash
curl -sG "http://plus.kipris.or.kr/openapi/rest/RightHolderService/rightHolderInfo" \
  --data-urlencode "registrationNumber=2000642310000" \
  --data-urlencode "accessKey=$KIPRIS_API_KEY"
```

## 필수/주요 파라미터

| 이름 | 의미 | 형식·예 |
|---|---|---|
| `registrationNumber` | 등록번호 | `2000642310000` |
| `accessKey` | KIPRIS Plus 서비스키 | `$KIPRIS_API_KEY` |

## 응답 핵심 필드

| 필드 | 의미 |
|---|---|
| `rightHolderInfo` | 권리자 변동 관련자 1건 |
| `pertinentPartition` | 해당란. 예: 권리자란, 전용권자란 |
| `rankNumber` | 순위번호 |
| `registrationDate` | 등록일자, `YYYYMMDD` |
| `rankCorrelatorSerialNumber` | 순위관련자 일련번호 |
| `rankCorrelatorNumber` | 순위관련자 번호 또는 특허고객번호 |
| `rankCorrelatorType` | 관련자 종류. 예: 권리자, 발명자, 의무자 |
| `rankCorrelatorName` | 관련자 이름 |
| `rankCorrelatorAddress` | 관련자 주소. KIPRIS 응답에서 일부 마스킹될 수 있음 |
| `transferDate` | 이전일자. 항목에 따라 빈 값 가능 |

## 페이징

없음. 등록번호 단건 조회이며 `rightHolderInfo`가 여러 건 반복될 수 있다.

## 함정

- 이 operation은 `accessKey`를 쓴다.
- 2026-06-28 실호출 기준, 정상 콘텐츠가 있어도 `resultCode`와 `resultMsg`가 빈 값으로 내려올 수 있다. HTTP 200과 `rightHolderInfo` 반복 노드 존재 여부를 함께 본다.
- `registrationNumber`는 하이픈 없이 보낸다. 예: `10-1104063-0000`은 `1011040630000` 형식이다.
- 국내 특허·실용의 권리이전 사건 자체가 필요하면 같은 신청 묶음의 `RightTransferService/getRightTransferInfo`를 별도 recipe 후보로 본다.
- 권리자명·주소는 공개 응답이지만 개인정보/주소 노출을 최소화해서 필요한 필드만 보관한다.
