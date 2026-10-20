# 국가R&D 용어사전 조회 서비스(전체용)

> provider: ntis.go.kr
> official: https://www.ntis.go.kr/rndopen/openApi/ntisDic
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

국가R&D 용어사전을 검색하는 서비스 검색 키워드: 관련어,대역어,용어사전. 이용대상: 대국민.

## Endpoint

- base: `https://www.ntis.go.kr/rndopen/openApi/ntisDic`
- operation: `/rndopen/openApi/ntisDic`
- method: `GET`
- format: `XML`
- apiSn: `6604`

## 키

- env: `NTIS_API_KEY`
- key parameter: `apprvKey`
- 주입 예: `agents-env run NTIS_API_KEY -- <명령>`
- recipe와 로그에는 실제 승인키를 남기지 않는다.

## 호출 예시

```bash
curl -sG "https://www.ntis.go.kr/rndopen/openApi/ntisDic" \
  --data-urlencode "apprvKey=$NTIS_API_KEY" \
  --data-urlencode "collection=bizinfo" \
  --data-urlencode "query=나노" \
  --data-urlencode "startPosition=1" \
  --data-urlencode "displayCount=1" \
  --data-urlencode "naviCount=30"
```

## 필수/주요 파라미터

| 이름 | 필수 | 의미 | 예시 |
|---|---:|---|---|
| apprvKey | Y | 승인된 발급키 | `$NTIS_API_KEY` |
| userId | N | 로그인한 경우에만 사용자 ID 기재 | `` |
| collection | N | 입력하지 않아도 과제만 검색됨사용 예) collection=project | `bizinfo` |
| query | Y | 검색 질의어 입력 연산자 필드 설명 AND 띄워쓰기로 구분query=나노 기술 OR \| 특수문자로 구분query=나노\|기술 NOT ! 특수문자로 구분query=!나노 “” 일치 문자열 검색query=“나노 기술" 사용 예) query=나노&searchField=BI* UTF-8 인코딩 필요 | `나노` |
| searchField | N | 필드명 필드 설명 BI 전체 (하위 모두 포함) TI 한글용어명,영문용어명 AB 주약어 사용 예) searchFd=BI* UTF-8 인코딩 필요 | `` |
| addQuery | N | 필드명 필드 설명 CN 용어사전키 PY(int) 용어사전 등록년 TI01 한글용어명 TI02 영문용어명 AB01 주약어명 사용 예)addQuery=CN=2020063972 int형필드 설명 2004/MORE,2009/UNDER 2004이상 2009이하 2006/MORE 2004이상 2002/UNDER 2002이하 2... | `` |
| sortby | N | 검색 결과에 대한 정렬 필드명 필드 설명 RANK/DESC 검색 랭킹 내림차순 RANK/ASC 검색 랭킹 오름차순 DATE/DESC 날자 내림차순 DATE/ASC 날자 오름차순 사용 예) searchRnkn=DATE/DESC* UTF-8 인코딩 필요 | `` |
| startPosition | N | 검색결과 시작위치를 지정사용 예) startPosition=1 | `1` |
| displayCount | N | 화면에 보여줄 검색 결과 수사용 예) displayCount=10 | `1\|2\|3` |
| naviCount | N | 네비게이션 카운트사용 예) naviCount=30 | `30` |

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
| `KorWord` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `EngWord` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `MainAbrv` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `SntStdCls` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `RelWord` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `TermDctn` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `TermCls` | 공식 PDF XML 예시에서 확인된 응답 태그 |

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

사용자 원래 질의어
NAME : 오퍼레이션명

O

NAME : 네비게이터필드명

O

검색 오퍼레이션

NAVIGATION

scienceclass: 과기표준분류
NAVIGATIONENTRY

year : 용어등록년도
termtypename : 용어구분명

NAVIGATIONELEMENTS

NAVIGATIONELEMENT

COUNT : 하위요소개수
NAME : 네비게이터이름

O

COUNT : 개수

- 7 -

국가과학기술지식정보서비스 (National Science & Technology Information Service)

Field

Attributes

Iteration

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
참고 : highlight tag 는
HITS

NO : 검색결과문서순서

O

<span class=search_word>
</span> 으로 리턴됨

TermSn

용어사전 고유번호

KorWord

한글용어명

EngWord

영문용어명

MainAbrv

주약어명

SntStdCls

과기표준분류

RelWord

연관어

TermDctn

용어설명

TermCls

용어구분명

- 8 -

국가과학기술지식정보서비스 (National Science & Technology Information Service)

③ 요청/ 응답 메시지 예시
REST(URI)

https://www.ntis.go.kr/rndopen/openApi/ntisDic?apprvKey={{NTIS_API_KEY}}&query=나노&userId=&
collection=&searchField=&displayCount=1&startPosition=1&naviCount=30&sortby=&boostquery=&addQu
ery=

응답메시지
<?xml version="1.0" encoding="UTF-8"?>
<RESULT
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xsi:noNamespaceSchemaLocation="https://www.ntis.go.kr/searchapi/schema/title.1.0.xsd">
<QUERYTRANSFORMS>
<ORIGINALQUERY>나노</ORIGINALQUERY>
</QUERYTRANSFORMS>
<COUNTLIST>
<COLCOUNT NAME="rpaperSR">649</COLCOUNT>
</COUNTLIST
```

## 페이징

`startPosition`은 검색 시작 위치다. `displayCount`는 반환 건수다. `naviCount`는 네비게이션 카운트다.

## 활용신청

- 신청 URL: `https://www.ntis.go.kr/rndopen/rqst/cmbn/cmbnPrctuseApplsInsertForm.do`
- 신청 상태: `submitted`
- 제출 확인: 2026-06-28 NTIS 활용신청이력에서 확인
- 승인키: 아직 `NTIS_API_KEY` 또는 상세 이력에서 확인되지 않음
- 호출 상태: 승인키 발급 전에는 공식 오류 `인증키 정보가 없습니다.` 반환

## 공식 PDF 원문

- PDF: [`6604-rnd-dictionary-public.pdf`](../docs/ntis/6604-rnd-dictionary-public.pdf)
- TXT 추출본: [`6604-rnd-dictionary-public.txt`](../docs/ntis/6604-rnd-dictionary-public.txt)
- 원본 파일명: `13. 통합OpenAPI_국가R&D용어사전(전체용)_메뉴얼_2024.pdf`
- PDF 원문과 전체 텍스트 추출본은 위 docs 경로에 그대로 보존했다.

## 함정

- NTIS 서비스별 활용신청/승인이 필요할 수 있다. 미승인 응답이면 이 recipe의 apiSn으로 신청 상태를 먼저 확인한다.
- 검색어, 기관명, 과제명 등 한글 값은 UTF-8 URL 인코딩을 전제로 호출한다.
- 저작권/이용허락: 제3유형:출처표시+변경금지.
- `userId`는 로그인한 경우에만 기재하는 선택 파라미터로 캡처됐다.
