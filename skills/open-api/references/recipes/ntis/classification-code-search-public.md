# 과학기술표준분류코드/국가중점기술코드 검색 서비스(전체용)

> provider: ntis.go.kr
> official: https://www.ntis.go.kr/rndopen/openApi/targetSearch
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

국가표준분류코드/국가중점기술코드를 검색할 수 있는 서비스 검색 키워드: 과학기술표준분류,국가R&D,국가중점기술. 이용대상: 대국민. 과학기술표준분류와 국가중점기술 코드 매핑, 추천 작업에 쓴다.

## Endpoint

- base: `https://www.ntis.go.kr/rndopen/openApi/targetSearch`
- operation: `/rndopen/openApi/targetSearch`
- method: `GET`
- format: `XML`
- apiSn: `6430`

## 키

- env: `NTIS_API_KEY`
- key parameter: `apprvKey`
- 주입 예: `agents-env run NTIS_API_KEY -- <명령>`
- recipe와 로그에는 실제 승인키를 남기지 않는다.

## 호출 예시

```bash
curl -sG "https://www.ntis.go.kr/rndopen/openApi/targetSearch" \
  --data-urlencode "apprvKey=$NTIS_API_KEY" \
  --data-urlencode "rqstSlctCd=NTIS001" \
  --data-urlencode "rqstSearchCd=NA0101"
```

## 필수/주요 파라미터

| 이름 | 필수 | 의미 | 예시 |
|---|---:|---|---|
| apprvKey | Y | 승인된 발급키 | `$NTIS_API_KEY` |
| rqstSlctCd | Y | 필드명필드 설명NTIS001 과학기술표준분류코드 NTIS002 국가중점기술코드사용 예) rqstSlctCd=NTIS001 | `NTIS001` |
| rqstSearchCd | N | 검색 코드 입력사용 예)“rqstSearchCd”=“060200” | `NA0101` |

## 응답 핵심 필드

| 필드 | 의미 |
|---|---|
| `ntis` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `status` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `recode` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `remsg` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `contents` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `dataset` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `cd` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `cdNm` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `cdExplan` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `cdNmEng` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `upperCd` | 공식 PDF XML 예시에서 확인된 응답 태그 |

공식 PDF 응답부 발췌:

```text
② 응답명세
- 요청구분코드 : NTIS001(국가표준분류코드)
Field

Attributes

Iteration

설명

ntis

결과문서의 최상위 필드

·status

상태
상태코드
필드명
100
101
200
300

··recode

400
··remsg

상태값

·contents
··dataset

num : dataset 인덱스

- 6 -

필드 설명
정상
요청데이터 미존재
요청 권한 없음
요청 파라미터 재확인
수행 중 오류
(관리자에게 문의)

국가과학기술지식정보서비스 (National Science & Technology Information Service)

Field

Attributes

Iteration

설명

···classCd

분야코드

···kindCd

연구분야코드

···kindCdNm

연구분야명

···classCdNm

분류코드명

···classCdNmEng

분류코드영문명

···classCdExplan

분류코드설명

···upperClassCd

상위분류코드

- 요청구분코드 : NTIS002(국가중점기술코드)
Field

Attributes

Iteration

설명

ntis

결과문서의 최상위 필드

·status

상태
상태코드
필드명
100
101
200
300

··recode

400
··remsg

필드 설명
정상
요청데이터 미존재
요청 권한 없음
요청 파라미터 재확인
수행 중 오류
(관리자에게 문의)

상태값

·contents
··dataset

num : dataset 인덱스

···cd

코드

···cdNm

코드명

···cdNmEng

코드영문명

···cdExplan

코드설명

···upperCd

상위코드

③ 요청/ 응답 메시지 예시
요청메세지

Request Header :
POST https://www.ntis.go.kr/rndopen/openApi/targetSearch HTTP/1.1
Host: www.ntis.go.kr
Content-Type: application/x-www-form-urlencoded;charset=UTF-8
Request Body :
apprvKey={{NTIS_API_KEY}}
&rqstSlctCd=NTIS002&rqstSearchCd=060200
응답메시지

Response Header:

- 7 -

국가과학기술지식정보서비스 (National Science & Technology Information Service)

Status Code: 200 OK
Connection: close
Content-Type: application/xml
Response Body :
<?xml version="1.0" encoding="utf-8" standalone="yes"?>
<ntis>
<status>
<recode>100</recode>
<re
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

- PDF: [`6430-classification-code-search-public.pdf`](../docs/ntis/6430-classification-code-search-public.pdf)
- TXT 추출본: [`6430-classification-code-search-public.txt`](../docs/ntis/6430-classification-code-search-public.txt)
- 원본 파일명: `14. 통합OpenAPI_과학기술표준분류코드_국가중점기술코드 검색(전체용)_메뉴얼_2024.pdf`
- PDF 원문과 전체 텍스트 추출본은 위 docs 경로에 그대로 보존했다.

## 함정

- NTIS 서비스별 활용신청/승인이 필요할 수 있다. 미승인 응답이면 이 recipe의 apiSn으로 신청 상태를 먼저 확인한다.
- 검색어, 기관명, 과제명 등 한글 값은 UTF-8 URL 인코딩을 전제로 호출한다.
- 저작권/이용허락: 제4유형:출처표시+상업적이용금지+출처표시.
