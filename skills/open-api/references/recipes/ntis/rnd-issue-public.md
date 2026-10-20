# 이슈로보는R&D 서비스(전체용)

> provider: ntis.go.kr
> official: https://www.ntis.go.kr/rndopen/openApi/issue
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

최신 과학기술 이슈와 관련된 국가R&D 현황, 키워드, 동향 정보를 제공 합니다. 검색 키워드: R&D현황,기술,이슈. 이용대상: 대국민.

## Endpoint

- base: `https://www.ntis.go.kr/rndopen/openApi/issue`
- operation: `/rndopen/openApi/issue`
- method: `GET`
- format: `XML`
- apiSn: `6429`

## 키

- env: `NTIS_API_KEY`
- key parameter: `apprvKey`
- 주입 예: `agents-env run NTIS_API_KEY -- <명령>`
- recipe와 로그에는 실제 승인키를 남기지 않는다.

## 호출 예시

```bash
curl -sG "https://www.ntis.go.kr/rndopen/openApi/issue" \
  --data-urlencode "apprvKey=$NTIS_API_KEY" \
  --data-urlencode "SRWR=나노"
```

## 필수/주요 파라미터

| 이름 | 필수 | 의미 | 예시 |
|---|---:|---|---|
| apprvKey | Y | 승인된 발급키 | `$NTIS_API_KEY` |
| SRWR | N | 검색하고자 하는 키워드(한글, 영문) 검색범위 : 주제키워드 + 연관키워드 ※검색키워드가 없는 경우 최신 이슈 5개 리턴 | `나노` |

## 응답 핵심 필드

| 필드 | 의미 |
|---|---|
| `img` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `NewestIssue` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `searchListCnt` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `list` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `topicNo` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `topicNm` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `extrDt` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `rltdPjtCnt` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `url01` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `url02` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `rltdKywdList` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `kywd` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `imgOfferYn` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `verifyFlag` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `resCd` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `resMsg` | 공식 PDF XML 예시에서 확인된 응답 태그 |

공식 PDF 응답부 발췌:

```text
② 응답명세
※정상 응답
Field

Attributes

Iteration

NewestIssue

결과문서의 최상위 필드

selectListCnt
list

설명

검색결과 건수
NO : 이슈 순서

Y

이슈 목록

topicNo

이슈고유번호

topicNm

이슈명

extrDt

추출일자

rltdPjtCnt

연관과제건수

url01

연구자맵 원문번호

url02

기관맵 원문번호

rltdKywdList

Y

kywd

관련키워드 목록
키워드

imgOfferYn

이슈 메인 이미지 제공 여부(Y,N)

- 6 -

국가과학기술지식정보서비스 (National Science & Technology Information Service)

Ÿ

이슈 바로가기 URL :
http://www.ntis.go.kr/issuernd/sns/{topicNo}
※ 예 : http://www.ntis.go.kr/issuernd/sns/201807020001

Ÿ

연구자맵 바로가기 URL :
http://www.ntis.go.kr/ecologymap/cmRschrMapView.do?nodeNo={url01}&chkYear=0000
※ 예 : http://www.ntis.go.kr/ecologymap/cmRschrMapView.do?nodeNo=1527561179057&chkYear=0000

Ÿ

기관맵 바로가기 URL :
http://www.ntis.go.kr/ecologymap/cmRschrOrgMapView.do?nodeNo={url02}&chkYear=0000
※ 예 : http://www.ntis.go.kr/ecologymap/cmRschrOrgMapView.do?nodeNo=1527561179057&chkYear=0000

Ÿ

이슈 메인 이미지 호출 URL : (imgOfferYn 필드 값이 ‘Y“인 경우만 이미지 제공)
http://www.ntis.go.kr/ppm/api/selectMainImgSrc.do?topicNo={topicNo}&imgType=main
※ 예 : <img src="http://www.ntis.go.kr/ppm/api/selectMainImgSrc.do?topicNo=201809100001&imgType=main">
※오류 응답
Field

Attributes

Iteration

RESULT

설명
결과문서의 최상위 필드

verifyFlag

검증결과(TRUE, FALSE)
응답코드(2 : API 내부 오류, 3 :

resCd

허용되지 않은 접근 또는 호출정보
오류)

resMsg

오류 응답 메세지

③ 요청/ 응답 메시지 예시
REST(URI)
https://www.ntis.go.kr/rndopen/openApi/issue?apprvKey={{NTIS_API_KEY}}&SRWR=smart
응답메시지(정상)

<
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

- PDF: [`6429-rnd-issue-public.pdf`](../docs/ntis/6429-rnd-issue-public.pdf)
- TXT 추출본: [`6429-rnd-issue-public.txt`](../docs/ntis/6429-rnd-issue-public.txt)
- 원본 파일명: `12. 통합OpenAPI_이슈로보는R&D(전체용)_매뉴얼_2024.pdf`
- PDF 원문과 전체 텍스트 추출본은 위 docs 경로에 그대로 보존했다.

## 함정

- NTIS 서비스별 활용신청/승인이 필요할 수 있다. 미승인 응답이면 이 recipe의 apiSn으로 신청 상태를 먼저 확인한다.
- 검색어, 기관명, 과제명 등 한글 값은 UTF-8 URL 인코딩을 전제로 호출한다.
- 저작권/이용허락: 제3유형:출처표시+변경금지.
