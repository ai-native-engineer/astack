# DART 단일회사 주요계정 재무 조회

> provider: opendart.fss.or.kr
> official: https://opendart.fss.or.kr/api/fnlttSinglAcnt.json
> checked: 2026-06-28 · 상태: 실호출 검증됨

## 언제 쓰나

사업보고서·반기보고서·분기보고서 기준 단일회사의 주요 재무계정, 연결/별도 재무제표 금액을 조회할 때 쓴다. 매출액, 영업이익, 당기순이익, 자산총계 같은 DART 재무제표 요약 확인용이다.

## Endpoint

- base: `https://opendart.fss.or.kr`
- operation: `/api/fnlttSinglAcnt.json`
- method: `GET`

## 키

- env: `API_K_DART`
- 주입 예: `agents-env run API_K_DART -- <명령>`

## 호출 예시

```bash
agents-env run API_K_DART -- curl -sG "https://opendart.fss.or.kr/api/fnlttSinglAcnt.json" \
  --data-urlencode "crtfc_key=$API_K_DART" \
  --data-urlencode "corp_code=00126380" \
  --data-urlencode "bsns_year=2025" \
  --data-urlencode "reprt_code=11011" \
  --data-urlencode "fs_div=CFS"
```

## 필수/주요 파라미터

| 이름 | 의미 | 형식·예 |
|---|---|---|
| `crtfc_key` | DART 인증키 | `$API_K_DART` |
| `corp_code` | DART 고유번호 | `00126380` |
| `bsns_year` | 사업연도 | `2025` |
| `reprt_code` | 보고서 코드 | `11011` 사업보고서, `11012` 반기보고서, `11013` 1분기보고서, `11014` 3분기보고서 |
| `fs_div` | 재무제표 구분 | `CFS` 연결, `OFS` 별도 |

## 응답 핵심 필드

| 필드 | 의미 |
|---|---|
| `status`, `message` | 처리 상태. 정상은 `000` |
| `list[].bsns_year` | 사업연도 |
| `list[].sj_nm` | 재무제표명 |
| `list[].account_nm` | 계정명 |
| `list[].thstrm_amount` | 당기 금액 |
| `list[].frmtrm_amount` | 전기 금액 |

## 페이징

없음.

## 함정

- 재무제표 조회 전 `list.json`에서 해당 사업연도/보고서 존재를 먼저 확인한다.
- DART `013` 또는 `조회된 데이타가 없습니다.`는 키 실패가 아니라 조건 0건일 수 있다.
- 2026-06-28 삼성전자 `00126380`, `2025`, `11011`, `CFS` 테스트 결과 `status=000`, 30개 계정을 확인했다.
- 같은 조건에서 `bsns_year=1999`는 `status=013`으로 확인했다.
