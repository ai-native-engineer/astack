# 국가R&D 과제검색 서비스(기관용)

> provider: ntis.go.kr
> official: https://www.ntis.go.kr/rndopen/openApi/pjtSearch/
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

국가R&D 과제 메타정보를 검색할 수 있는 서비스 ※ 일반이용자는 대국민용을 신청하시기 바랍니다. 검색 키워드: 과제,국가R&D,목록검색. 이용대상: 전문기관 , 과제관리기관 , 연구성과전담기관 , 정부출연(연) , 대학연구자. 국가R&D 과제명, 과제고유번호, 부처, 수행기관, 연구책임자 축으로 찾을 때 우선 검토한다. 기관명 또는 사업자등록번호 기반 R&D 현황 조회에 쓴다.

## Endpoint

- base: `https://www.ntis.go.kr/rndopen/openApi/pjtSearch/`
- operation: `/rndopen/openApi/pjtSearch/`
- method: `GET`
- format: `XML`
- apiSn: `6427`

## 키

- env: `NTIS_API_KEY`
- key parameter: `apprvKey`
- 주입 예: `agents-env run NTIS_API_KEY -- <명령>`
- recipe와 로그에는 실제 승인키를 남기지 않는다.

## 호출 예시

```bash
curl -sG "https://www.ntis.go.kr/rndopen/openApi/pjtSearch/" \
  --data-urlencode "apprvKey=$NTIS_API_KEY" \
  --data-urlencode "collection=project" \
  --data-urlencode "SRWR=나노" \
  --data-urlencode "startPosition=1" \
  --data-urlencode "displayCnt=1"
```

## 필수/주요 파라미터

| 이름 | 필수 | 의미 | 예시 |
|---|---:|---|---|
| apprvKey | Y | 승인된 발급키 | `$NTIS_API_KEY` |
| userId | N | 로그인한 경우에만 사용자 ID 기재 | `` |
| collection | Y | 입력하지 않아도 과제만 검색됨 사용 예) collection=project | `project` |
| SRWR | Y | 검색 질의어 입력 연산자 필드 설명 AND 띄워쓰기로 구분query=나노 기술 OR \| 특수문자로 구분query=나노\|기술 NOT ! 특수문자로 구분query=!나노 “” 일치 문자열 검색query=“나노 기술" 사용 예) SRWR=나노&searchField=BI* UTF-8 인코딩 필요 | `나노` |
| searchFd | N | 필드명 필드 설명 BI 전체 (하위 모두 포함) TI 과제명 AU 연구책임자명 OG 과제관리기관명 PB 과제수행기관명 부처명 예산사업명 기관사업명 내역사업명 세부과제번호 과제고유번호 키워드 KW 키워드 AB 연구목표 연구내용 연구성과(기대효과) 사용 예) searchFd=BI* UTF-8 인코딩 필요 | `` |
| addQuery | N | 필드명 필드 설명 CN 과제고유번호 PY 기준년도 TI01 국문과제명 TI02 영문과제명 AU01 연구책임자명 OG01 과제관리기관명 PB01 과제수행기관명 PB02 사업부처명 PB03 사업명(프로그램) PB05 내역사업명 PB07 세부과제번호 KW01 한글키워드 KW02 영문키워드 AB01 연구목표요약 AB02 연... | `` |
| searchRnkn | N | 검색 결과에 대한 정렬 필드명 필드 설명 RANK/DESC 검색 랭킹 내림차순 RANK/ASC 검색 랭킹 오름차순 DATE/DESC 날짜 내림차순 DATE/ASC 날짜 오름차순 사용 예) searchRnkn=DATE/DESC | `` |
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
| `ProjectNumber` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `ProjectTitle` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `Korean` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `English` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `Manager` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `Name` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `HumanID` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `ResearcherNO` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `Researchers` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `ManCount` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `WomanCount` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `PrStRegistrationNumber` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `Goal` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `Full` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `Teaser` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `Abstract` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `Effect` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `Keyword` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `OrderAgency` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `Code` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `LeadAgency` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `ResearchAgency` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `BudgetProject` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `BusinessName` | 공식 PDF XML 예시에서 확인된 응답 태그 |

공식 PDF 응답부 발췌:

```text
② 응답명세
Iter
Field

Attributes

atio

길이

설명

n
RESULT

결과문서의 최상위 필드

QUERYTRANSFORMS
ORIGINALQUERY
COUNTLIST
NAVIGATION

4000
CLOB

NAME : 오퍼레이션명

사용자 원래 질의어
검색 오퍼레이션

leadagency : 과제수행기관명
orderagency : 전문기관명
projectyear : 기준년도
budgetprojectname : 사업명
scienceclass1 : 국가과학기술표준분류
NAVIGATIONENTRY

NAME : 네비게이터필드명

O

CLOB

commistionproject : 위탁과제유무
ministryname : 부처명
performagent : 연구수행주체
developmentphases : 연구개발단계
sixtechnology : 6T분류
strategictechique : 중점과학기술분류

NAVIGATIONELEMENTS

NAVIGATIONELEMENT

COUNT : 하위요소개수
NAME : 네비게이터이름
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

1base index, 현재 결과로 넘겨준 문서
의 시작위치

RESULTSET
참고 : highlight tag 는
HIT

NO : 검색결과문서순서

O

20

<span class=search_word>
</span> 으로 리턴됨

ProjectNumber

10

과제고유번호

Korean

512

국문과제명

English

512

영문과제명

ProjectTitle

Manager

- 8 -

국가과학기술지식정보서비스 (National Science & Technology Information Service)

Iter
Field

Attributes

atio

길이

설명

n
Name

110

연구책임자명

Name

4000

참여연구원 성명 (;로 나열)

ManCount

10

참여연구원 성별구분의 남성 합계

WomanCount

10

참여연구원 성별구분의 여성 합계

Researchers

Goal
Full

4000

Teaser

4000

연구목표요약
※ 성능 제약으로 요약으로 대체
연구목표요약
※ 약 250자 내외

Abstract
Full

4000

Teaser

4000

연구개발내용
※ 성능 제약으로 요약으로 대체
연구개발내용 요약
※ 약 250자 내외

Effect
Full

4000

Teaser

4000

기대효과요약
※ 성능 제약으로 요약으로 대체
기대효과 요약
※ 약 250자 내외

Keyword
Korean

1024

English

1024

한글 키워드
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

- PDF: [`6427-project-search-agency.pdf`](../docs/ntis/6427-project-search-agency.pdf)
- TXT 추출본: [`6427-project-search-agency.txt`](../docs/ntis/6427-project-search-agency.txt)
- 원본 파일명: `02.통합OpenAPI_국가R&D 과제검색(기관용)_매뉴얼_2025.pdf`
- PDF 원문과 전체 텍스트 추출본은 위 docs 경로에 그대로 보존했다.

## 함정

- NTIS 서비스별 활용신청/승인이 필요할 수 있다. 미승인 응답이면 이 recipe의 apiSn으로 신청 상태를 먼저 확인한다.
- 검색어, 기관명, 과제명 등 한글 값은 UTF-8 URL 인코딩을 전제로 호출한다.
- 기관용 API는 이용대상 제한이 있으므로 소속기관 권한과 신청 가능 범위를 먼저 확인한다.
- 저작권/이용허락: 제1유형:출처표시.
- `userId`는 로그인한 경우에만 기재하는 선택 파라미터로 캡처됐다.
