# 국가R&D 연구보고서 검색 서비스(전체용)

> provider: ntis.go.kr
> official: https://www.ntis.go.kr/rndopen/openApi/rresearchpdf
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

국가R&D 연구보고서 메타정보를 검색할 수 있는 서비스 검색 키워드: 목록검색,연구보고서. 이용대상: 대국민.

## Endpoint

- base: `https://www.ntis.go.kr/rndopen/openApi/rresearchpdf`
- operation: `/rndopen/openApi/rresearchpdf`
- method: `GET`
- format: `XML, JSON`
- apiSn: `6607`

## 키

- env: `NTIS_API_KEY`
- key parameter: `apprvKey`
- 주입 예: `agents-env run NTIS_API_KEY -- <명령>`
- recipe와 로그에는 실제 승인키를 남기지 않는다.

## 호출 예시

```bash
curl -sG "https://www.ntis.go.kr/rndopen/openApi/rresearchpdf" \
  --data-urlencode "apprvKey=$NTIS_API_KEY" \
  --data-urlencode "collection=researchpdf" \
  --data-urlencode "query=나노" \
  --data-urlencode "startPosition=1" \
  --data-urlencode "displayCount=1"
```

## 필수/주요 파라미터

| 이름 | 필수 | 의미 | 예시 |
|---|---:|---|---|
| apprvKey | Y | 승인된 발급키 | `$NTIS_API_KEY` |
| userId | N | 로그인한 경우에만 사용자 ID 기재 | `` |
| collection | Y | 입력하지 않아도 국가R&D 연구보고서만 검색됨사용 예) collection=researchpdf | `researchpdf` |
| query | Y | 검색 질의어 입력 연산자 필드 설명 AND 띄워쓰기로 구분query=나노 기술 OR \| 특수문자로 구분query=나노\|기술 NOT ! 특수문자로 구분query=!나노 “” 일치 문자열 검색query=“나노 기술" 사용 예) query=나노&searchField=BI* UTF-8 인코딩 필요 | `나노` |
| searchField | N | 필드명 필드 설명 BI 전체 (하위 모두 포함) TI 보고서명 한글 보고서명 영문 PB 발행기관명 KW 키워드 한글 키워드 영문 AB 초록 한글 초록 영문 목차 사용 예) searchFd=BI* UTF-8 인코딩 필요 | `` |
| addQuery | N | 필드명 필드 설명 CN 성과번호 PY(int) 발행년도 TI01 보고서명(한글) TI02 보고서명(영문) PB01 발행기관명 KW01 키워드(한글) KW02 키워드(영문) AB01 초록(한글) AB02 초록(영문) AB04 목차 사용 예)addQuery=CN=11110000 int형필드 설명 2004/MORE,200... | `` |
| sortBy | N | 검색 결과에 대한 정렬 필드명 필드 설명 RANK/DESC 검색 랭킹 내림차순 RANK/ASC 검색 랭킹 오름차순 DATE/DESC 날자 내림차순 DATE/ASC 날자 오름차순 사용 예) searchRnkn=DATE/DESC | `` |
| startPosition | N | 검색결과 시작위치를 지정사용 예) startPosition=10 | `1` |
| displayCount | N | 화면에 보여줄 검색 결과 수사용 예) displayCount=100 | `1\|2\|3` |
| returnType | N | 검색 양식 리턴 필드명 필드 설명 xml 출력 포맷을 xml로 제공(기본) json 출력 포맷을 json으로 제공 | `` |

## 응답 핵심 필드

| 필드 | 의미 |
|---|---|
| `span` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `QUERYTRANSFORMS` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `ORIGINALQUERY` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `COUNTLIST` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `COLCOUNT` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `TOTALHITS` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `STARTPOSITION` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `SEARCHTIME` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `TermSn` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `PublicationYm` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `ResearchPublicNo` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `PublicationAgency` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `ResultTitle` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `Korean` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `English` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `Abstract` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `Keyword` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `Contents` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `PublicationCountry` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `PublicationLanguage` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `DocUrl` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `NrmsUrl` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `ProjectNumber` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `ProjectTitle` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `ManageAgency` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `Manager` | 공식 PDF XML 예시에서 확인된 응답 태그 |

공식 PDF 응답부 발췌:

```text
② 응답명세
Field

Attributes

Iteration

RESULT

설명
결과문서의 최상위 필드

QUERYTRANSFORMS
ORIGINALQUERY
COUNTLIST

사용자 질의어
NAME : 오퍼레이션명

검색 오퍼레이션

TOTALHITS

검색건수(전체)
1base index, 현재 결과로 넘겨준

STARTPOSITION

문서의 시작위치

HITS

검색건수(출력건수)

SEARCHTIME

검색시간

RESULTSET
참고 : highlight tag 는
HIT

NO : 검색결과문서순서

O

<span class=search_word>
</span> 으로 리턴됨

TermSn

성과번호

PublicationYear

발행년도

ResearchPublicNo

보고서등록번호

PublicationAgency
ResultTitle
Abstract
Keyword

발행기관명
Korean : 한글
English : 영어
Korean : 한글
English : 영어
Korean : 한글
English : 영어

보고서명(한, 영)

키워드(한, 영)

Contents

목차

PublicationCountry

발행국가명

PublicationLanguage

사용언어

DocUrl

원문정보 URL

ProjectNumber

과제 고유번호

ProjectTitle

과제명

LeadAgency

과제 수행기관명

ManagerName

과제 연구책임자명

SpecializedAgency

전문기관

AgencyDetailProjectNumber

세부과제번호(기관)

- 8 -

국가과학기술지식정보서비스 (National Science & Technology Information Service)

③ 요청/ 응답 메시지 예시 (xml)
REST(URI)

https://www.ntis.go.kr/rndopen/openApi/rresearchpdf?apprvKey={{NTIS_API_KEY}}&query=나노&use
rId=&collection=rresearchpdf&searchField=&displayCount=10&startPosition=1&naviCount=30&sortby=
&boostquery=&addQuery=&returnType=

응답메시지

<?xml version="1.0" encoding="UTF-8"?>
<RESULT
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xsi:noNamespaceSchemaLocation="https://www.ntis.go.kr/searchapi/schema/title.1.0.xsd"
>
<QUERYTRANSFORMS>
<ORIGINALQUERY>나노</ORIGINALQUERY>
</QUERYTRANSFORMS>
<COUNTLIST
```

## 페이징

`startPosition`은 검색 시작 위치다. `displayCount`는 반환 건수다.

## 활용신청

- 신청 URL: `https://www.ntis.go.kr/rndopen/rqst/cmbn/cmbnPrctuseApplsInsertForm.do`
- 신청 상태: `submitted`
- 제출 확인: 2026-06-28 NTIS 활용신청이력에서 확인
- 승인키: 아직 `NTIS_API_KEY` 또는 상세 이력에서 확인되지 않음
- 호출 상태: 승인키 발급 전에는 공식 오류 `인증키 정보가 없습니다.` 반환

## 공식 PDF 원문

- PDF: [`6607-research-report-search-public.pdf`](../docs/ntis/6607-research-report-search-public.pdf)
- TXT 추출본: [`6607-research-report-search-public.txt`](../docs/ntis/6607-research-report-search-public.txt)
- 원본 파일명: `10. 통합OpenAPI_국가R&D연구보고서 검색(전체용)_매뉴얼_2024.pdf`
- PDF 원문과 전체 텍스트 추출본은 위 docs 경로에 그대로 보존했다.

## 함정

- NTIS 서비스별 활용신청/승인이 필요할 수 있다. 미승인 응답이면 이 recipe의 apiSn으로 신청 상태를 먼저 확인한다.
- 검색어, 기관명, 과제명 등 한글 값은 UTF-8 URL 인코딩을 전제로 호출한다.
- 저작권/이용허락: 제1유형:출처표시.
- `userId`는 로그인한 경우에만 기재하는 선택 파라미터로 캡처됐다.
