# DART 기업 개황 조회

> provider: opendart.fss.or.kr
> official: https://opendart.fss.or.kr/api/company.json
> checked: 2026-06-28 · 상태: 실호출 검증됨

## 언제 쓰나

기업의 DART 등록 개황, `corp_cls`, 사업자번호, 종목코드, 법인구분을 빠르게 확인할 때 쓴다. 공시 목록이나 재무제표를 부르기 전 `corp_code`가 맞는지 검증하는 용도다.

## Endpoint

- base: `https://opendart.fss.or.kr`
- operation: `/api/company.json`
- method: `GET`

## 키

- env: `API_K_DART`
- 주입 예: `agents-env run API_K_DART -- <명령>`

## 호출 예시

```bash
agents-env run API_K_DART -- curl -sG "https://opendart.fss.or.kr/api/company.json" \
  --data-urlencode "crtfc_key=$API_K_DART" \
  --data-urlencode "corp_code=00126380"
```

## 필수/주요 파라미터

| 이름 | 의미 | 형식·예 |
|---|---|---|
| `crtfc_key` | DART 인증키 | `$API_K_DART` |
| `corp_code` | DART 고유번호 | `00126380` |

## 응답 핵심 필드

| 필드 | 의미 |
|---|---|
| `status`, `message` | 처리 상태. 정상은 `000` |
| `corp_name` | 회사명 |
| `corp_cls` | 법인구분. `Y` 유가, `K` 코스닥, `N` 코넥스, `E` 기타 |
| `stock_code` | 종목코드 |
| `bizr_no` | 사업자등록번호 |

## 페이징

없음.

## 함정

- 2026-06-28 삼성전자 `00126380` 테스트 결과 `status=000`, `corp_cls=Y`, `stock_code=005930`을 확인했다.
- `corp_cls=E`나 `stock_code` 공란은 비상장 기타법인일 수 있으며 공시 조회 대상에서 바로 제외하지 않는다.
