# 호출 패턴 — 인코딩 · 페이징 · 에러

## upstream은 두 형태다 (같은 키 사용)

| 형태 | base | 특징 |
|---|---|---|
| 전통형 | `https://apis.data.go.kr/<기관코드>/<서비스>/<오퍼레이션>` | GET + 쿼리 파라미터. 응답 기본 XML, JSON은 별도 파라미터 |
| 신형(odcloud) | `https://api.odcloud.kr/api/...` | REST/JSON 네이티브. 국세청 사업자 등 표준화 API |

상세 페이지 인라인 Swagger의 `host`로 어느 쪽인지 판별한다.

## serviceKey 인코딩 — 최다 빈도 함정

키는 **Decoding(원문) 키**를 환경변수에 두고, 인코딩은 curl에 맡긴다:

```bash
curl -sG "https://apis.data.go.kr/<host path>/<operation>" \
  --data-urlencode "serviceKey=$DATA_GO_KR_API_KEY" \
  --data-urlencode "pageNo=1" --data-urlencode "numOfRows=100" \
  --data-urlencode "type=json"
```

- Encoding 키(이미 `%2B` 등 포함)를 `--data-urlencode`에 넣으면 **이중 인코딩** → `SERVICE_KEY_IS_NOT_REGISTERED`. 키가 어느 쪽인지 모르면: `%`가 포함돼 있으면 Encoding 키다.
- odcloud는 쿼리 `serviceKey=` 또는 헤더 `Authorization: Infuser $KEY` 둘 다 허용.

## JSON 응답 파라미터가 제각각

기관마다 `type=json` / `_type=json` / `resultType=json` / `returnType=JSON` 으로 다르다. 상세 페이지 요청변수 표에서 확인하고 레시피에 기록한다. 파라미터가 없으면 XML만 제공 — 그대로 파싱한다.

## 페이징

전통형 공통: `pageNo`(1부터) + `numOfRows`. 응답 `totalCount`로 전수 여부를 판단하고, **첫 페이지만 보고 "전부"라고 말하지 않는다.** 대량 조회는 기간 파라미터(예: `inqryBgnDt`/`inqryEndDt`)로 쪼개서 순회한다.

## 에러 — 두 층을 구분해서 읽는다

**층 1: 게이트웨이 에러** (미신청·키오류 — HTTP 200으로 오는 경우가 많아 코드만 보면 놓친다). 바디가 정상 응답이 아니라 이 구조다:

```xml
<OpenAPI_ServiceResponse>
  <cmmMsgHeader>
    <returnReasonCode>30</returnReasonCode>
    <returnAuthMsg>SERVICE_KEY_IS_NOT_REGISTERED_ERROR</returnAuthMsg>
  </cmmMsgHeader>
</OpenAPI_ServiceResponse>
```

판별: 바디에서 `returnReasonCode`/`returnAuthMsg`를 grep (정상 응답의 `resultCode`와 **다른 필드**다).

| returnReasonCode | 의미 | 행동 |
|---|---|---|
| 20 (SERVICE_ACCESS_DENIED) | **활용신청 안 됨** | 활용신청 딥링크 전달 (search-and-apply.md §3) |
| 30 (SERVICE_KEY_IS_NOT_REGISTERED) | 키 오류 (오타·이중 인코딩·미동기화) | 인코딩 확인 → 신청 직후면 최대 1시간 대기 |
| 22 (LIMITED_NUMBER_OF_SERVICE_REQUESTS_EXCEEDS) | 일일 쿼터 초과 | 운영계정 전환 또는 내일 재시도 안내 |
| 31 (DEADLINE_HAS_EXPIRED) | 활용기간 만료 | 연장신청 딥링크 전달 |

**층 0: HTTP 403 + 평문 "Forbidden"** (XML조차 아님) — 신청 승인 직후 **키-서비스 동기화 전** 상태에서 관측됨(2026-06-10 실측, 나라장터 낙찰). UA를 바꿔도 동일하면 WAF가 아니라 미활성이다. 행동: 즉시~1시간 대기 후 재시도, 그래도 403이면 활용신청이 그 publicDataPk에 됐는지 확인.

**층 2: 서비스 정상 응답의 결과 코드** — `<header><resultCode>00</resultCode>`(또는 JSON 동일 필드)가 정상. `00`이 아니면 해당 API의 자체 에러(파라미터 형식 등) — 상세 페이지의 에러코드 표 확인.

**odcloud(신형)는 HTTP 코드가 정직하다** — 401 키 누락/오류, 500 파라미터 오류. JSON 에러 바디 그대로 읽으면 된다.

## 레시피 갱신 트리거

호출이 레시피대로 안 되면(파라미터 변경·서비스 개편) 상세 페이지를 다시 떠서 레시피를 고치고 `checked` 날짜를 갱신한다 — 깨진 레시피를 두는 것이 레시피 없는 것보다 나쁘다.
