# DART 공시 목록 조회

> provider: opendart.fss.or.kr
> official: https://opendart.fss.or.kr/api/list.json
> checked: 2026-06-28 · 상태: 실호출 검증됨

## 언제 쓰나

회사별 DART 공시 목록, 접수번호, 보고서명, 공시일자를 조회할 때 쓴다. 재무제표 API 호출 전 해당 기간에 사업보고서·반기보고서·분기보고서가 있는지 확인한다.

## Endpoint

- base: `https://opendart.fss.or.kr`
- operation: `/api/list.json`
- method: `GET`

## 키

- env: `API_K_DART`
- 주입 예: `agents-env run API_K_DART -- <명령>`

## 호출 예시

```bash
agents-env run API_K_DART -- curl -sG "https://opendart.fss.or.kr/api/list.json" \
  --data-urlencode "crtfc_key=$API_K_DART" \
  --data-urlencode "corp_code=00126380" \
  --data-urlencode "bgn_de=20260101" \
  --data-urlencode "end_de=20260628" \
  --data-urlencode "page_no=1" \
  --data-urlencode "page_count=10"
```

## 필수/주요 파라미터

| 이름 | 의미 | 형식·예 |
|---|---|---|
| `crtfc_key` | DART 인증키 | `$API_K_DART` |
| `corp_code` | DART 고유번호 | `00126380` |
| `bgn_de` | 시작일 | `YYYYMMDD` |
| `end_de` | 종료일 | `YYYYMMDD` |
| `page_no` | 페이지 번호 | `1` |
| `page_count` | 페이지당 건수 | `10` |

## 응답 핵심 필드

| 필드 | 의미 |
|---|---|
| `status`, `message` | 처리 상태. 정상은 `000` |
| `total_count`, `page_no` | 전체 건수와 현재 페이지 |
| `list[].rcept_dt` | 접수일 |
| `list[].report_nm` | 보고서명 |
| `list[].rcept_no` | 접수번호 |
| `list[].corp_name` | 회사명 |

## 페이징

`page_no`, `page_count`, `total_count`로 처리한다.

## 함정

- 첫 페이지만 보고 전체 공시라고 말하지 않는다.
- 보고서명은 공백이 붙을 수 있으므로 표시 전 trim한다.
- 2026-06-28 삼성전자 `00126380`, `20260101`~`20260628` 테스트 결과 `status=000`, `total_count=1917`을 확인했다.
