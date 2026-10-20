# 위탁/공동연구 과제검색 서비스(기관용)

> provider: ntis.go.kr
> official: https://www.ntis.go.kr/rndopen/openApi/projectuOrg
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

위탁/공동연구 과제 메타 데이터 제공 검색 키워드: 과제,국가R&D,목록검색. 이용대상: 전문기관 , 과제관리기관 , 연구성과전담기관 , 정부출연(연) , 대학연구자. 국가R&D 과제명, 과제고유번호, 부처, 수행기관, 연구책임자 축으로 찾을 때 우선 검토한다. 기관명 또는 사업자등록번호 기반 R&D 현황 조회에 쓴다.

## Endpoint

- base: `https://www.ntis.go.kr/rndopen/openApi/projectuOrg`
- operation: `/rndopen/openApi/projectuOrg`
- method: `GET`
- format: `XML`
- apiSn: `6614`

## 키

- env: `NTIS_API_KEY`
- key parameter: `apprvKey`
- 주입 예: `agents-env run NTIS_API_KEY -- <명령>`
- recipe와 로그에는 실제 승인키를 남기지 않는다.

## 호출 예시

```bash
curl -sG "https://www.ntis.go.kr/rndopen/openApi/projectuOrg" \
  --data-urlencode "apprvKey=$NTIS_API_KEY" \
  --data-urlencode "pjtId=1425072712"
```

## 필수/주요 파라미터

| 이름 | 필수 | 의미 | 예시 |
|---|---:|---|---|
| apprvKey | Y | 승인된 발급키 | `$NTIS_API_KEY` |
| pjtId | Y | 검색할 위탁/공동 연구 과제 데이터의 주관과제 고유번호 또는 위탁과제번호를 입력 | `1425072712` |

## 응답 핵심 필드

| 필드 | 의미 |
|---|---|
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
| `CommissionNumber` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `ProjectYear` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `ProjectTitle` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `Korean` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `English` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `Commission` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `Manager` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `Name` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `CommissionManager` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `OrderAgency` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `LeadAgency` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `CommissionLeadAgency` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `CommissionType` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `PerformAgent` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `Country` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `ProjectPeriod` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `Start` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `End` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `Total` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `CorporateRegistrationNumber` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `ResearcherCount` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `ProjectOrderAgency` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `ProjectResearchManagerName` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `CollaborativeResearchFunds` | 공식 PDF XML 예시에서 확인된 응답 태그 |

공식 PDF 응답부 발췌:

```text
② 응답명세

Field

Attributes

RESULT

설명

결과문서의 최상위 필드

QUERYTRANSFORMS
ORIGINALQUERY
COUNTLIST

사용자 원래 질의어
NAME : 오퍼레이션명

검색 오퍼레이션

NAVIGATION
Description

과제수행기관명+코드
전문기관명+코드
연구책임자명
기준년도
사업명+코드
국가과학기술표준분류(연구분야) +코드

6T분류명+코드
위탁과제존재유무
부처명
연구수행주체
연구개발단계
참여연구원수
국가전략기술+코드
최종과제여부
국가과학기술표준분류(1번) 대
국가과학기술표준분류(2번) 중
국가과학기술표준분류(3번) 소
중점과학기술분류-대
중점과학기술분류-중
중점과학기술분류-소
국가과학기술표준분류(대,대,대)
국가과학기술표준분류(중,중,중)
국가과학기술표준분류(소,소,소)
과제별 연구비 총액 구간
과학기술표준분류(대, 매핑)
6T관련기술 대+코드
6T관련기술 증+코드
6T관련기술 소+코드
지역분류

NAVIGATIONENTRY

NAVIGATIONELEMENTS

NAVIGATIONELEMENT

COUNT : 하위요소개수
NAME : 네비게이터이름
COUNT : 개수

- 6 -

국가과학기술지식정보서비스 (National Science & Technology Information Service)

Field

Attributes

TOTALHITS

설명

검색건수(전체)
1base index, 현재 결과로 넘겨준

STARTPOSITION

문서의 시작위치

HITS

검색건수(가져온 건수)

SEARCHTIME

검색시간

RESULTSET
NO="1" //순서번호
NO : 검색결과문서 순서
HIT

SITENAME : 오퍼레이션구분
SITEID : 오퍼레이션ID

"1-1" //"1"번의 하위 과제
"1"번
SITENAME="project" // 과제
"subproject" // 하위과제
SITEID="1" //ID

ProjectNumber

주관/협동 고유번호 or 위탁/공동 고유번호

CommissionNumber

위탁 과제번호

ProjectYear

기준년도

ProjectTitle

과제명

Korean

한글 과제명

English

영문 과제명

Manager

과제 책임자

Name

과제 책임자명

CommissionManager

위탁연구 책임자명

OrderAgency

위탁 과제 책임자명

LeadAgency

과제관리(전문)기관명

CommissionLeadAgency

위탁수행기관명

CommissionType

위탁/공동연구 구분

PerformAgent

code : 연구수행주체 코드

연구수행 주체명

Country

code : 연구수행 국가코드

연구수행 국가명

ProjectPeriod

참여기간

Start

참여기간 시작일

End

참여기간 종료일
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

- PDF: [`6614-consortium-project-search-agency.pdf`](../docs/ntis/6614-consortium-project-search-agency.pdf)
- TXT 추출본: [`6614-consortium-project-search-agency.txt`](../docs/ntis/6614-consortium-project-search-agency.txt)
- 원본 파일명: `04. 위탁공동연구 과제 정보 제공 API(기관용)_메뉴얼_2024.pdf`
- PDF 원문과 전체 텍스트 추출본은 위 docs 경로에 그대로 보존했다.

## 함정

- NTIS 서비스별 활용신청/승인이 필요할 수 있다. 미승인 응답이면 이 recipe의 apiSn으로 신청 상태를 먼저 확인한다.
- 검색어, 기관명, 과제명 등 한글 값은 UTF-8 URL 인코딩을 전제로 호출한다.
- 기관용 API는 이용대상 제한이 있으므로 소속기관 권한과 신청 가능 범위를 먼저 확인한다.
- 저작권/이용허락: 제1유형:출처표시.
