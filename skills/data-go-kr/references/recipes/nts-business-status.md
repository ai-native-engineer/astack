# 국세청_사업자등록정보 진위확인 및 상태조회 서비스

> publicDataPk: 15081808 · 상세: https://www.data.go.kr/data/15081808/openapi.do
> Swagger: https://infuser.odcloud.kr/api/stages/28493/api-docs?1728017570963
> checked: 2026-06-28 · 상태: 상태조회 실호출 검증됨, 진위확인 실호출 형식 검증됨
> 심층 문서: docs/260628-nts-businessman-swagger-1.1.json

## 언제 쓰나

사업자등록번호 상태조회, 휴폐업 확인, 과세유형 확인, 거래처·조사 대상 법인의 현재 사업자 상태 확인에 쓴다. 대표자명·개업일자까지 알고 있을 때는 사업자등록정보 진위확인에도 쓴다.

## Endpoint

- host: `api.odcloud.kr/api/nts-businessman/v1`

| 오퍼레이션 | 용도 |
|---|---|
| `POST /status` | 사업자등록번호 배열로 계속/휴업/폐업 및 과세유형 조회 |
| `POST /validate` | 사업자번호, 대표자명, 개업일자 등 입력값의 진위 확인 |

## 키

- env: `DATA_GO_KR_API_KEY`
- query parameter: `serviceKey`
- 주입 예: `agents-env run DATA_GO_KR_API_KEY -- <명령>`

## 호출 예시

상태조회:

```bash
agents-env run DATA_GO_KR_API_KEY -- curl -sS -X POST "https://api.odcloud.kr/api/nts-businessman/v1/status" \
  --url-query "serviceKey={{DATA_GO_KR_API_KEY}}" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{"b_no":["0000000000"]}'
```

진위확인:

```bash
agents-env run DATA_GO_KR_API_KEY -- curl -sS -X POST "https://api.odcloud.kr/api/nts-businessman/v1/validate" \
  --url-query "serviceKey={{DATA_GO_KR_API_KEY}}" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{"businesses":[{"b_no":"3018136564","start_dt":"20000101","p_nm":"홍길동","p_nm2":"","b_nm":"","corp_no":"","b_sector":"","b_type":"","b_adr":""}]}'
```

## 필수/주요 파라미터

| 이름 | 의미 | 형식·예 |
|---|---|---|
| `serviceKey` | 공공데이터포털 일반 인증키 | Decoding 키를 환경변수에 두고 URL query로 전달 |
| `returnType` | 응답 형식 | JSON은 생략 권장, XML 필요 시 `XML` |
| `b_no` | 사업자등록번호 | 숫자 10자리, 하이픈 제거 |
| `businesses` | 진위확인 요청 배열 | 1회 최대 100개 |
| `start_dt` | 개업일자 | `YYYYMMDD`, 사업자등록증 기준 |
| `p_nm` | 대표자성명 | 필수 |
| `p_nm2` | 대표자성명2 | 외국인 사업자의 한글명 입력용. 필요 없으면 빈 문자열 |
| `b_nm` | 상호 | 선택 |
| `corp_no` | 법인등록번호 | 선택, 숫자 13자리 |
| `b_sector` | 주업태명 | 선택 |
| `b_type` | 주종목명 | 선택 |
| `b_adr` | 사업장주소 | 선택 |

## 응답 핵심 필드

| 필드 | 의미 |
|---|---|
| `status_code` | `OK`면 정상 |
| `request_cnt` | 요청 건수 |
| `match_cnt` | 상태조회 매칭 건수 |
| `valid_cnt` | 진위확인 valid 건수 |
| `data[].valid` | 진위확인 결과, `01`: Valid, `02`: Invalid |
| `data[].valid_msg` | 진위확인 실패 메시지 |
| `data[].b_stt` / `data[].b_stt_cd` | 납세자상태, `01`: 계속사업자, `02`: 휴업자, `03`: 폐업자 |
| `data[].tax_type` / `data[].tax_type_cd` | 과세유형 |
| `data[].end_dt` | 폐업일 |
| `data[].utcc_yn` | 단위과세전환폐업여부 |
| `data[].tax_type_change_dt` | 최근 과세유형 전환일자 |
| `data[].invoice_apply_dt` | 세금계산서 적용일자 |
| `data[].rbf_tax_type` / `data[].rbf_tax_type_cd` | 직전 과세유형 |

## 페이징

없음. POST batch API이며 `/status`와 `/validate` 모두 1회 최대 100건까지 보낸다.

## 함정

- GET이 아니라 POST 전용이다. `serviceKey`와 `returnType`만 querystring이고, `b_no`/`businesses`는 JSON body로 보낸다.
- JSON은 기본값이라 `returnType=JSON`을 생략하는 편이 안전하다. 2026-06-28 실측상 `serviceKey` query에 `returnType=JSON`을 함께 붙이면 HTTP 400 `{"code":-999,"msg":"UNKNOWN"}`가 났다.
- `--url-query "serviceKey=$DATA_GO_KR_API_KEY"`를 쓰면 Decoding 키를 직접 URL-인코딩하지 않아도 된다.
- `/validate`는 `0000000000`처럼 자리수만 맞춘 번호로 호출하면 HTTP 400 `{"code":-999,"msg":"UNKNOWN"}`가 날 수 있다. 도달성 테스트는 형식상 유효한 사업자번호와 불일치 대표자명·개업일자로 보내면 `valid=02` 정상 응답이 온다.
- 1회 호출은 최대 100개다. 초과하면 413 `TOO_LARGE_REQUEST`.
- 삭제된 사업자등록정보는 조회되지 않는다. 상태조회는 "국세청에 등록되지 않은 사업자등록번호입니다", 진위확인은 "확인할 수 없습니다" 성격의 응답을 돌려준다.
- 진위확인은 대표자명·개업일자 등 민감할 수 있는 값을 보낸다. 단순 휴폐업 확인이면 `/status`만 쓴다.
- 사업자등록번호, 법인등록번호, 개업일자는 하이픈 등 기호를 제거한다.
- 상호의 `(주)`, `주식회사`, 특수문자 괄호 `（주）`는 앞뒤에 붙어도 동일하게 검색 가능하다고 안내되어 있다.
- 주업태명, 주종목명, 사업장주소는 공백을 무시하고 검색된다.
