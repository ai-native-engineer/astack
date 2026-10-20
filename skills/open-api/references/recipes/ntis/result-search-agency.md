# 국가R&D 성과검색 서비스(기관용)

> provider: ntis.go.kr
> official: https://www.ntis.go.kr/rndopen/openApi/natRnDSearch
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

국가R&D 성과(논문, 특허, 연구보고서, 연구시설장비) 메타정보를 검색할 수 있는 서비스 ※ 일반이용자는 대국민용을 신청하시기 바랍니다. 검색 키워드: R&D,성과. 이용대상: 전문기관 , 과제관리기관 , 연구성과전담기관 , 정부출연(연) , 대학연구자. 논문, 특허, 연구보고서, 장비 등 성과 메타데이터를 과제와 연결할 때 쓴다. 기관명 또는 사업자등록번호 기반 R&D 현황 조회에 쓴다.

## Endpoint

- base: `https://www.ntis.go.kr/rndopen/openApi/natRnDSearch`
- operation: `/rndopen/openApi/natRnDSearch`
- method: `GET`
- format: `XML`
- apiSn: `161`

## 키

- env: `NTIS_API_KEY`
- key parameter: `apprvKey`
- 주입 예: `agents-env run NTIS_API_KEY -- <명령>`
- recipe와 로그에는 실제 승인키를 남기지 않는다.

## 호출 예시

```bash
curl -sG "https://www.ntis.go.kr/rndopen/openApi/natRnDSearch" \
  --data-urlencode "apprvKey=$NTIS_API_KEY" \
  --data-urlencode "collection=rpaper" \
  --data-urlencode "SRWR=나노" \
  --data-urlencode "startPosition=1" \
  --data-urlencode "displayCnt=1"
```

## 필수/주요 파라미터

| 이름 | 필수 | 의미 | 예시 |
|---|---:|---|---|
| apprvKey | Y | 발급된 인증키 | `$NTIS_API_KEY` |
| userId | N | 로그인한 경우에만 사용자 ID 기재 | `` |
| collection | Y | 논문 오퍼레이션 지정사용 예) collection=rpaper | `rpaper` |
| SRWR | Y | 검색 질의어 입력 연산자 필드 설명 AND 띄워쓰기로 구분query=나노 기술 OR \| 특수문자로 구분query=나노\|기술 NOT ! 특수문자로 구분query=!나노 “” 일치 문자열 검색query=“나노 기술" 사용 예) SRWR=나노&searchFd=BI* UTF-8 인코딩 필요 | `나노` |
| searchFd | N | 필드 필드 설명 BI 전체 (하위 모두 포함) TI 논문명, 저널명, 과제고유번호 AU 저자명 OG ISSN번호 PB 학술지명 KW 키워드 AB 초록 사용 예) searchFd=BI* UTF-8 인코딩 필요 | `` |
| addQuery | N | 필드명필드 설명 CN 성과번호 UF 원문유무(Y/N) PY(int) 성과연도 DBT PAP (반드시 DBT값 입력) TI01 논문명 TI02 저널명 TI03 과제고유번호 AU01 저자명 OG01 ISSN번호 PB01 학술지명 KW01 국문키워드 KW02 영문키워드 AB01 초록 사용 예)addQuery=CN=1111... | `` |
| searchRnkn | N | 검색 결과에 대한 정렬 필드명 필드 설명 RANK/DESC 검색 랭킹 내림차순 RANK/ASC 검색 랭킹 오름차순 DATE/DESC 날자 내림차순 DATE/ASC 날자 오름차순 사용 예) searchRnkn=DATE/DESC* UTF-8 인코딩 필요 | `` |
| startPosition | N | 검색결과 시작위치를 지정사용 예) startPosition=1 | `1` |
| displayCnt | N | 화면에 보여줄 검색 결과 수사용 예) displayCnt=10 | `1\|2\|3` |

## 응답 핵심 필드

| 필드 | 의미 |
|---|---|
| `span` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `QUERYTRANSFORMS` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `ORIGINALQUERY` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `COUNTLIST` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `COLCOUNT` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `TOTALHITS` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `SECRETPROJECTHITS` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `PROJECTRHITS` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `PROJECTCHITS` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `PROJECTCRHITS` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `STARTPOSITION` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `SEARCHTIME` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `ResultID` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `ResultTitle` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `JournalName` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `IssnNumber` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `Author` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `Abstract` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `Full` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `Teaser` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `Keyword` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `Korean` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `English` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `PubYear` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `ProjectID` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `PaperType` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `SciType` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `NationType` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `JCType` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `SourceFlag` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `KeywordFlag` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `TechnologylinkFlag` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `ProjectYear` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `BudgetProjectNumber` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `BudgetProject` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `MinistryName` | 공식 PDF XML 예시에서 확인된 응답 태그 |

공식 PDF 응답부 발췌:

```text
② 응답명세
Field

Attributes

Itera
tion

길이

RESULT

설명
결과문서의 최상위 필드

QUERYTRANSFORMS
ORIGINALQUERY
COUNTLIST

NAME : 오퍼레이션명

O

4000

사용자 원래 질의어

CLOB

검색 오퍼레이션

NAVIGATION
journalname : 저널명
NAVIGATIONENTRY

NAME : 네비게이터필드명

O

CLOB

year : 성과연도
nationtype : 국내외구분명
papertype : 국내외학술지구분명(코드)

- 7 -

국가과학기술지식정보서비스 (National Science & Technology Information Service)

Field

Attributes

Itera
tion

길이

설명
ministryname : 부처명(코드)
performagency : 수행기관명(코드)
performagent : 연구수행주체(코드)
sixtechnology : 6T분류명(코드)
textcheckyn : 원문유무 (Y/N)
scienceclass1 : 표준분류명(코드)
authorname : 저자명
scitype : SCI구분
● 구분값 예 : (명칭▦코드)

NAVIGATIONELEMENTS
NAVIGATIONELEMENT

COUNT : 하위요소개수
NAME : 값
COUNT : 개수

O

CLOB

TOTALHITS

20

검색건수(전체)

STARTPOSITION

20

HITS

20

검색건수(가져온 건수)

SEARCHTIME

21

검색시간

1base index, 현재 결과로 넘겨준
문서의 시작위치

RESULTSET

HIT

NO : 검색결과문서순서
SITID : 데이터구분

O

20,20
20

참고 : highlight tag 는
<span class=search_word>
</span> 으로 리턴됨

Year

4

성과연도

ResultID

20

성과ID

ResultTitle

880

논문명

JournalName

880

학술지명

IssnNumber

200

ISSN or ISBN

Author
Abstract
Keyword

저자명
Full : 초록 전체
Teaser : 초록 일부
Korean : 국문키워드
English : 영문키워드

O

초록

300

(Teaser는 250자 내외)

0

PubYear
PaperType

4000

키워드
4

code : 논문구분 코드

0

4(170)

학술지출판연도 or 학술대회발표연도
논문구분

SciType

10

SCI구분(01:SCI, 02:비SCI)

NationType

170

국내외구분

JCType

170

학술지 or 학술대회 구분

SourceFlag

1

원문유무(Y/N)

KeywordFlag

4

키워드유무(Y/N)
```

## 페이징

`startPosition`은 검색 시작 위치다. `displayCnt`는 반환 건수다.

## 활용신청

- 신청 URL: `https://www.ntis.go.kr/rndopen/rqst/cmbn/cmbnPrctuseApplsInsertForm.do`
- 신청 상태: `submitted`
- 제출 확인: 2026-06-28 NTIS 활용신청이력에서 확인
- 승인키: 아직 `NTIS_API_KEY` 또는 상세 이력에서 확인되지 않음
- 호출 상태: 승인키 발급 전에는 공식 오류 `인증키 정보가 없습니다.` 반환

## 공식 PDF 원문

- PDF: [`161-result-search-agency.pdf`](../docs/ntis/161-result-search-agency.pdf)
- TXT 추출본: [`161-result-search-agency.txt`](../docs/ntis/161-result-search-agency.txt)
- 원본 파일명: `06. 통합OpenAPI_국가R&D 성과검색(기관용)_매뉴얼_2024.pdf`
- PDF 원문과 전체 텍스트 추출본은 위 docs 경로에 그대로 보존했다.

## 함정

- NTIS 서비스별 활용신청/승인이 필요할 수 있다. 미승인 응답이면 이 recipe의 apiSn으로 신청 상태를 먼저 확인한다.
- 검색어, 기관명, 과제명 등 한글 값은 UTF-8 URL 인코딩을 전제로 호출한다.
- 기관용 API는 이용대상 제한이 있으므로 소속기관 권한과 신청 가능 범위를 먼저 확인한다.
- 저작권/이용허락: 제1유형:출처표시.
- `userId`는 로그인한 경우에만 기재하는 선택 파라미터로 캡처됐다.
