# 국세청_사업자등록정보 진위확인 및 상태조회 서비스

> publicDataPk: 15081808 · 상세: https://www.data.go.kr/data/15081808/openapi.do
> checked: 2026-06-10 · 상태: 외부 문서 기반(실호출 미검증 — 키 발급 대기). 출처: NomaDamas/k-skill nts-business-registration

## 언제 쓰나

사업자등록번호 상태조회(계속사업자/휴업/폐업, 과세유형), 사업자 진위확인, 거래처·조사 대상 법인의 휴폐업 확인, 동명 법인 분리 검증.

## Endpoint (odcloud 신형)

- 상태조회: `POST https://api.odcloud.kr/api/nts-businessman/v1/status`
- 진위확인: `POST https://api.odcloud.kr/api/nts-businessman/v1/validate`

## 호출 예시

```bash
curl -s -X POST "https://api.odcloud.kr/api/nts-businessman/v1/status?serviceKey=$(python3 -c "import urllib.parse,os;print(urllib.parse.quote(os.environ['DATA_GO_KR_API_KEY'],safe=''))")" \
  -H "Content-Type: application/json" \
  -d '{"b_no": ["1234567890"]}'
```

## 파라미터

| 이름 | 의미 | 비고 |
|---|---|---|
| b_no | 사업자등록번호 배열 | 숫자 10자리(하이픈 제거), **한 요청 최대 100개** |
| (validate) start_dt, p_nm | 개업일자 `YYYYMMDD`, 대표자명 | 진위확인 필수. b_nm(상호)·corp_no(법인 13자리) 등 선택 |

## 응답 핵심 필드 (status)

| 필드 | 의미 |
|---|---|
| b_stt / b_stt_cd | 계속사업자·휴업자·폐업자 / 코드 |
| tax_type | 과세유형 (일반/간이/면세 등) |
| end_dt | 폐업일 (폐업 시) |

## 함정

- POST의 쿼리스트링 serviceKey는 `--data-urlencode`를 못 쓰므로 위처럼 **직접 URL-인코딩** 1회. 또는 헤더 `Authorization: Infuser $DATA_GO_KR_API_KEY`로 대체.
- 진위확인(validate)은 대표자명 등 개인정보를 보낸다 — 작업에 status로 충분하면 validate를 쓰지 않는다.
