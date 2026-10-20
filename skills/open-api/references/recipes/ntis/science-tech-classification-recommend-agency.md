# 과학기술표준분류 추천 서비스(기관용)

> provider: ntis.go.kr
> official: https://www.ntis.go.kr/rndopen/openApi/rcmncls
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

요청정보(과제요약정보)에 적합한 국가과학기술표준분류 연구분야, 부처 분류(2개 시범)를 추천 검색 키워드: 과제참여,국가과학기술표준분류 연구분야,자동분류. 이용대상: 전문기관 , 과제관리기관 , 연구성과전담기관 , 정부출연(연) , 대학연구자. 기관명 또는 사업자등록번호 기반 R&D 현황 조회에 쓴다. 과학기술표준분류와 국가중점기술 코드 매핑, 추천 작업에 쓴다.

## Endpoint

- base: `https://www.ntis.go.kr/rndopen/openApi/rcmncls`
- operation: `/rndopen/openApi/rcmncls`
- method: `GET`
- format: `XML`
- apiSn: `6603`

## 키

- env: `NTIS_API_KEY`
- key parameter: `apprvKey`
- 주입 예: `agents-env run NTIS_API_KEY -- <명령>`
- recipe와 로그에는 실제 승인키를 남기지 않는다.

## 호출 예시

```bash
curl -sG "https://www.ntis.go.kr/rndopen/openApi/rcmncls" \
  --data-urlencode "apprvKey=$NTIS_API_KEY" \
  --data-urlencode "collection=rcmncls" \
  --data-urlencode "rqstDes=대용량 데이터 전송을 위한 replication기능 안정화AMGA 기술품질 향상 : LFC 기능 개발, GUI기반 서비스 관리 툴 개발사용자 활용지원 기술..."
```

## 필수/주요 파라미터

| 이름 | 필수 | 의미 | 예시 |
|---|---:|---|---|
| apprvKey | Y | 승인된 발급키 | `$NTIS_API_KEY` |
| collection | Y | collection=rcmncls | `rcmncls` |
| rqstDes | Y | 텍스트길이설명최소 300 byte 보다 커야 함최대 30K byte보다 작아야 함* UTF-8 인코딩 필요 | `대용량 데이터 전송을 위한 replication...` |

## 응답 핵심 필드

| 필드 | 의미 |
|---|---|
| `NTIS` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `auth` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `apprvKey` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `orgCD` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `userId` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `REQUEST` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `rqstDes` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `STATUS` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `ResultCode` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `ResultMsg` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `Result_1` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `Result_2` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `Result_3` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `Result_4` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `Result_5` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `rschGoalAbstract` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `rschAbstract` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `expEfctAbstract` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `korKywd` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `engKywd` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `MOHWD` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `MOHWR` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `MOTIE` | 공식 PDF XML 예시에서 확인된 응답 태그 |

공식 PDF 응답부 발췌:

```text
국가과학기술지식정보서비스 (National Science & Technology Information Service)

국가과학기술지식정보서비스
R&D데이터개방 오픈API 활용가이드

- 과학기술표준분류 추천 서비스(기관용) -

2024. 01. 03.

- 1 -

국가과학기술지식정보서비스 (National Science & Technology Information Service)

목

차

1. 서비스 활용 방법 ·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·3
2. 분류 추천 서비스 ·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·4
2.1 서비스 개요 ·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·4
2.2 상세기능 목록 ·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·5
2.3 상세기능 명세 ·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
·
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

- PDF: [`6603-science-tech-classification-recommend-agency.pdf`](../docs/ntis/6603-science-tech-classification-recommend-agency.pdf)
- TXT 추출본: [`6603-science-tech-classification-recommend-agency.txt`](../docs/ntis/6603-science-tech-classification-recommend-agency.txt)
- 원본 파일명: `11. 통합OpenAPI_과학기술표준분류 추천(기관용)_매뉴얼_2024.pdf`
- PDF 원문과 전체 텍스트 추출본은 위 docs 경로에 그대로 보존했다.

## 함정

- NTIS 서비스별 활용신청/승인이 필요할 수 있다. 미승인 응답이면 이 recipe의 apiSn으로 신청 상태를 먼저 확인한다.
- 검색어, 기관명, 과제명 등 한글 값은 UTF-8 URL 인코딩을 전제로 호출한다.
- 기관용 API는 이용대상 제한이 있으므로 소속기관 권한과 신청 가능 범위를 먼저 확인한다.
- 저작권/이용허락: 제4유형:출처표시+상업적이용금지+출처표시.
- `rqstDes`는 최소/최대 byte 조건이 있어 짧은 문장만 넣으면 오류가 날 수 있다.
