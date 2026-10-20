# 국가R&D 수행기관 R&D현황조회 서비스(전체용)

> provider: ntis.go.kr
> official: https://www.ntis.go.kr/rndopen/openApi/orgRndInfo
> checked: 2026-06-28 · 상태: 스키마/PDF 확보 · 활용신청 제출 확인 · 승인키 발급 대기

## 목차

- 언제 쓰나
- Endpoint
- 키
- 호출 예시
- 필수/주요 파라미터
- 응답 핵심 필드
- 페이징
- 활용신청
- 공식 PDF 원문
- 함정

## 언제 쓰나

수행기관 요청 내용에 대한 관련 정보를 제공하여 국가R&D 수행기관 정보를 공동 활용할 수 있도록 지원 검색 키워드: 과제,기관,표준분류. 이용대상: 대국민. 기관명 또는 사업자등록번호 기반 R&D 현황 조회에 쓴다.

## Endpoint

- base: `https://www.ntis.go.kr/rndopen/openApi/orgRndInfo`
- operation: `/rndopen/openApi/orgRndInfo`
- method: `GET`
- format: `XML`
- apiSn: `6609`

## 키

- env: `NTIS_API_KEY`
- key parameter: `apprvKey`
- 주입 예: `agents-env run NTIS_API_KEY -- <명령>`
- recipe와 로그에는 실제 승인키를 남기지 않는다.

## 호출 예시

```bash
curl -sG "https://www.ntis.go.kr/rndopen/openApi/orgRndInfo" \
  --data-urlencode "apprvKey=$NTIS_API_KEY" \
  --data-urlencode "reqOrgBno=205-82-04043" \
  --data-urlencode "reqOrgNm=한국과학기술정보연구원"
```

## 필수/주요 파라미터

| 이름 | 필수 | 의미 | 예시 |
|---|---:|---|---|
| apprvKey | Y | 승인된 발급키 | `$NTIS_API_KEY` |
| reqOrgBno | Y | R&D현황이 필요한 사업자등록번호xxx-xx-xxxxx 또는 숫자10자리로 입력사용 예) reqOrgBno=205-82-04043 | `205-82-04043` |
| reqOrgNm | N | 검색어 기반의 기관명 검색사용 예) reqOrgNm=한국과학기술정보연구원 | `한국과학기술정보연구원` |

## 응답 핵심 필드

| 필드 | 의미 |
|---|---|
| `response` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `header` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `resultCode` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `resultMsg` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `body` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `orgName` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `orgPageInfo` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `rndKorKeword` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `rndEngKeword` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `rndCategory` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `rndStatusList` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `year` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `pjtCnt` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `rndBudget` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `govBudget` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `paperCnt` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `patentCnt` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `reportCnt` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `numOfList` | 공식 PDF XML 예시에서 확인된 응답 태그 |

공식 PDF 응답부 발췌:

```text
② 응답명세
Parameter

Parameter

항목크기

(KOR)

항목구분

설명
결과

resultCode

결과코드

2

1

결과값
00 정상
01 비정상
02 비정상
03 비정상
04 비정상

설명

결과값
결과메시지
00 요청작업이 성공하였습니다
사업자등록번호 또는 기관명이
01
입력되지 않았습니다.
사업자등록번호 형식이 맞지
resultMsg

결과메시지

100

1

02

03
04

않습니다.(숫자 10자리, 또는
xxx-xx-xxxxx로 입력해야 합니다.)
요청하신 기관정보가 NTIS에
없습니다.
요청하신 사업자등록번호가
수행한 R&D과제정보가
없습니다.

orgName

기관명

100

1

사업자등록번호에 해당되는 기관명

orgPageInfo

NTIS 수행기관링크

50

1

기관상세정보를 볼 수 있는 링크

rndKorKeyword

국문연구키워드

50

0..5

기관이 수행한 과제들의 국문 연구키워드 Top5

rndEngKeyword

영문연구키워드

50

0..5

기관이 수행한 과제들의 영문 연구키워드 Top5

rndCategory

연구분야

50

0..3

기관이 수행한 과제들의 연구분야 Top3

rndStatusList

R&D현황리스트

array

0..n

기관이 수행한 과제를 연도별로 표기

year

연도

4

1

과제 기준년도

pjtCnt

과제건수

5

1

기관이 수행한 과제건수

rndBudget

연구비합계

16

1

기관이 수행한 과제의 연구비합계

govBudget

정부투자연구비합계

16

1

기관이 수행한 과제의 정부투자연구비합계

paperCnt

논문건수

5

1

기관이 수행한 과제에서 유발된 논문건수

patentCnt

특허건수

5

1

기관이 수행한 과제에서 유발된 특허건수

reportcnt

보고서건수

5

1

기관이 수행한 과제의 연구보고서건수
사업자등록번호로 검색 시

numOfList

R&D현황리스트갯수

2

1

특정 기관이 과제를 수행한 R&D현황리스트의 개수
기관명으로 검색 시
검색어와 매칭되는 기관의 개수

- 7 -

국가과학기술지식정보서비스 (National Science & Technology Information Service)

③ 요청/ 응답 메시지 예시
REST(URI)
https://www.ntis.go.kr/rndopen/openApi/orgRndInfo?apprvKey={{NTIS_API_KEY}}&reqOrgBno=205-82-04043&reqOrgN
m=한국과학기술정보연구원
https://www.ntis.go.kr/rndopen/openApi/orgRndInfo?apprvKey={{NTIS_API_KEY}}&reqOrgBno=205-82-04043

응답메시지 (resultCode가 00인 경우에
```

## 페이징

테스트 페이지 기준 별도 페이징 파라미터가 없다.

## 활용신청

- 신청 URL: `https://www.ntis.go.kr/rndopen/rqst/cmbn/cmbnPrctuseApplsInsertForm.do`
- 신청 상태: `submitted`
- 제출 확인: 2026-06-28 NTIS 활용신청이력에서 확인
- 승인키: 아직 `NTIS_API_KEY` 또는 상세 이력에서 확인되지 않음
- 호출 상태: 승인키 발급 전에는 공식 오류 `인증키 정보가 없습니다.` 반환

## 공식 PDF 원문

- PDF: [`6609-org-rnd-status-public.pdf`](../docs/ntis/6609-org-rnd-status-public.pdf)
- TXT 추출본: [`6609-org-rnd-status-public.txt`](../docs/ntis/6609-org-rnd-status-public.txt)
- 원본 파일명: `08. 통합OpenAPI_국가R&D수행기관 조회(전체용)_메뉴얼_2024.pdf`
- PDF 원문과 전체 텍스트 추출본은 위 docs 경로에 그대로 보존했다.

## 함정

- NTIS 서비스별 활용신청/승인이 필요할 수 있다. 미승인 응답이면 이 recipe의 apiSn으로 신청 상태를 먼저 확인한다.
- 검색어, 기관명, 과제명 등 한글 값은 UTF-8 URL 인코딩을 전제로 호출한다.
- 저작권/이용허락: 제1유형:출처표시.
