# 연관콘텐츠 추천 서비스(전체용)

> provider: ntis.go.kr
> official: https://www.ntis.go.kr/rndopen/openApi/ConnectionContent
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

인공지능 기술을 활용하여 특정 과제정보와 유사도가 높은 과제정보, 논문정보, 특허정보, 연구보고서 정보를 제공함 검색 키워드: 과제,성과,인공지능. 이용대상: 대국민.

## Endpoint

- base: `https://www.ntis.go.kr/rndopen/openApi/ConnectionContent`
- operation: `/rndopen/openApi/ConnectionContent`
- method: `GET`
- format: `XML`
- apiSn: `6613`

## 키

- env: `NTIS_API_KEY`
- key parameter: `apprvKey`
- 주입 예: `agents-env run NTIS_API_KEY -- <명령>`
- recipe와 로그에는 실제 승인키를 남기지 않는다.

## 호출 예시

```bash
curl -sG "https://www.ntis.go.kr/rndopen/openApi/ConnectionContent" \
  --data-urlencode "apprvKey=$NTIS_API_KEY" \
  --data-urlencode "pjtId=1425118980" \
  --data-urlencode "collection=project"
```

## 필수/주요 파라미터

| 이름 | 필수 | 의미 | 예시 |
|---|---:|---|---|
| apprvKey | Y | 승인된 발급키 | `$NTIS_API_KEY` |
| pjtId | Y | 과제고유번호(10자리) | `1425118980` |
| collection | Y | 검색할 컬렉션명을 입력사용 예)collection=project | `project` |

## 응답 핵심 필드

PDF 원문 TXT에서 자동 추출 가능한 XML 필드를 찾지 못했다. 원문 TXT를 확인한다.

공식 PDF 응답부 발췌:

```text
② 응답명세

Field

Attributes

설명

PJT_ID

String

요청한 과제 고유번호

KOR_PJT_NM

String

요청한 Item Title Text

exist

String

유사 데이터 존재여부

items

String

출력결과

count

String

결과 개수

RST_ID

String

고유번호

similarity_score

float

유사도

creat_dt

String

데이터 등록일

KOR_PJT_NM

String

과제명

RANK

Int

유사도에 따른 과제 순위

- 7 -

국가과학기술지식정보서비스 (National Science & Technology Information Service)

③ 요청/ 응답 메시지 예시
REST(URI)

https://www.ntis.go.kr/rndopen/openApi/ConnectionContent.do?apprvKey={{NTIS_API_KEY}}&pjtId=142511898
0&collection=project

응답메시지

{
"PJT_ID": "1425118980",
"KOR_PJT_NM": "안내 서비스를 위한 클라우드 IoT 인공지능 로봇 시나리오 저작 환경 구현",
"exist": true,
"items": [
{
"PJT_ID": "1711193709",
"similarity_score": 0.7264716811909956,
"rank": 1,
"creat_dt": "2023-03-21 11:39:34",
"KOR_PJT_NM": "IoT 및 지능정보 기반 동남권 제조 IT 기술 혁신 및 인재양성"
},
{
"PJT_ID": "1711193762",
"similarity_score": 0.7222462311397535,
"rank": 2,
"creat_dt": "2023-03-21 11:39:35",
"KOR_PJT_NM": "다수 로봇의 지능을 통합 고도화하는 클라우드 로봇 지능 증강·공유 및 프레임워크 기술 개발"
},
{
"PJT_ID": "1711193899",
"similarity_score": 0.7192183842019017,
"rank": 3,
"creat_dt": "2023-04-24 12:28:26",
"KOR_PJT_NM": "클라우드 엣지 전주기 데이터 안정성을 위한 추적성 보장 기술 개발"
},
{
"PJT_ID": "1711193388",
"similarity_score": 0.7171209557401704,
"rank": 4,
"creat_dt": "2023-04-24 12:28:11",
"KOR_PJT_NM": "디바이스 성능에 따라 변화하는 클라우드 기반 XR 콘텐츠 변환 및 서비스 기술 개발"
},
{
"PJT_ID": "1425179901",

- 8 -

국가과학기술지식정보서비스 (National
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

- PDF: [`6613-related-content-recommend-public.pdf`](../docs/ntis/6613-related-content-recommend-public.pdf)
- TXT 추출본: [`6613-related-content-recommend-public.txt`](../docs/ntis/6613-related-content-recommend-public.txt)
- 원본 파일명: `15.통합OpenAPI_연관컨텐츠 조회 서비스(전체용)_메뉴얼_2024.pdf`
- PDF 원문과 전체 텍스트 추출본은 위 docs 경로에 그대로 보존했다.

## 함정

- NTIS 서비스별 활용신청/승인이 필요할 수 있다. 미승인 응답이면 이 recipe의 apiSn으로 신청 상태를 먼저 확인한다.
- 검색어, 기관명, 과제명 등 한글 값은 UTF-8 URL 인코딩을 전제로 호출한다.
- 저작권/이용허락: 제1유형:출처표시.
