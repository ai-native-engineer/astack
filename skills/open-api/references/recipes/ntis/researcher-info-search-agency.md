# 출연(연) 연구자정보검색 서비스(기관용)

> provider: ntis.go.kr
> official: https://www.ntis.go.kr/rndopen/openApi/rsrcInfo
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

출연(연) 연구자정보검색 서비스(기관용) 검색 키워드: 국가R&D,연구자,출연(연). 이용대상: 정부출연(연). 기관명 또는 사업자등록번호 기반 R&D 현황 조회에 쓴다. 출연연 연구자 정보 조회용이며 개인정보 최소 처리 원칙을 적용한다.

## Endpoint

- base: `https://www.ntis.go.kr/rndopen/openApi/rsrcInfo`
- operation: `/rndopen/openApi/rsrcInfo`
- method: `GET`
- format: `XML`
- apiSn: `6618`

## 키

- env: `NTIS_API_KEY`
- key parameter: 테스트 페이지 기준 별도 `apprvKey` 파라미터 없음
- 주입 예: `agents-env run NTIS_API_KEY -- <명령>`
- recipe와 로그에는 실제 승인키를 남기지 않는다.

## 호출 예시

```bash
curl -sG "https://www.ntis.go.kr/rndopen/openApi/rsrcInfo" \
  --data-urlencode "nm=<연구자명>" \
  --data-urlencode "rrno=<국가연구자번호>" \
  --data-urlencode "brthdt=YYYYMMDD" \
  --data-urlencode "blngorgnm=<소속기관명>"
```

## 필수/주요 파라미터

| 이름 | 필수 | 의미 | 예시 |
|---|---:|---|---|
| nm | Y | 연구자명 | `<연구자명>` |
| rrno | Y | 국가연구자번호(과학기술인등록번호) | `<국가연구자번호>` |
| brthdt | N | 생년월일 | `YYYYMMDD` |
| blngorgnm | N | 소속기관명 | `<소속기관명>` |

## 응답 핵심 필드

| 필드 | 의미 |
|---|---|
| `ResultList` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `Result` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `Nm` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `Rrno` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `BlngorNm` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `Keyword` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `PjtList` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `Pjt` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `KorPjtNm` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `PjtId` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `StanYr` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `ProgNm` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `RschMngrNm` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `MainRschOrgNm` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `DeptNm` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `TotRndco` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `PaperList` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `Paper` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `PaperNm` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `PubYr` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `JrnlSlct` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `AuthorSlct` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `AuthorNm` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `JrnlNm` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `Volume` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `Number` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `StartPage` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `EndPage` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `TrnswrtList` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `Trnswrt` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `TrnswrtSlct` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `TrnswrtNm` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `PblctnNm` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `Isbn` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `IprList` | 공식 PDF XML 예시에서 확인된 응답 태그 |
| `Ipr` | 공식 PDF XML 예시에서 확인된 응답 태그 |

공식 PDF 응답부 발췌:

```text
② 응답명세
Field
ResultList

Attributes
Count : 결과문서건수

설명
결과문서 리스트

Result

결과문서

Nm

이름

Rrno

국가연구자번호(과학기술인등
록번호)

BlngorNm

소속기관명

Keyword

키워드

PjtList

Count : 과제건수

과제 리스트

KorPjtNm : 과제명
PjtId : 과제고유번호
Pjt

StanYr : 기준년도

과제 정보

ProgNm : 예산사업명
RschMngrNm : 연구책임자
MainRschOrgNm : 과제수행기관

- 6 -

국가과학기술지식정보서비스 (National Science & Technology Information Service)

Field

Attributes

설명

DeptNm : 부처명
TotRndco : 정부투자연구비
PapertList

Count : 논문건수

논문 리스트

PaperNm : 논문명
PubYr: 발행년도
JrnlSlct : 학술지구분
AuthorSlct : 저자구분
Paper

AuthorNm : 저자명

논문 정보

JrnlNm : 저널(프로시딩)
Volume : 개재권,집
Number : 개재호
StartPage : 시작페이지
EndPage : 종료페이지

TrnswrtList

Count : 저역서건수

저역서리스트

TrnswrtSlct : 저역서구분
TrnswrtNm : 저역서명
Trnswrt

PblctnNm : 저역서발행처명

저역서 정보

Isbn : ISBN번호
PubYr : 발행년도
IprList

Count : 지식재산권건수

지식재산권리스트

IprNm : 지적재산권(발명)명칭
Yr : 연도
Ipr

IprSlct : 지재권구분

지적재산권 정보

AcqSlct : 출원등록구분
AplyRegistHm : 출원(등록)인
AplyRegistNo : 출원(등록)번호

ActList

Count : 주요활동건수

주요활동리스트

ActRelOrgNm : 관계기관명
ActNm : 활동명
Act

ActSlct : 활동구분

주요활동 정보

ActStartDt : 활동시작년월
ActEndDt : 활동종료년월
QualList

Count : 자격사항건수

자격사항리스트

QualPblctnNm : 자격증발행처명
Qual

QualNm : 자격증명

자격사항 정보

QualAcqDt : 자격취득일자
MdrwList

Count : 훈포장상건수

훈포장상리스트

CnfOrgNm : 수여기관명
Mdrw

AwardedNm : 수상명

훈포장상 정보

AwardeYm : 수상년월

- 7 -

국가과학기술지식정보서비스 (National Science & Technology Information Service)

③ 요청/ 응답 메시지 예시
REST(URI)
https://www.ntis.go.kr/rndopen/o
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

- PDF: [`6618-researcher-info-search-agency.pdf`](../docs/ntis/6618-researcher-info-search-agency.pdf)
- TXT 추출본: [`6618-researcher-info-search-agency.txt`](../docs/ntis/6618-researcher-info-search-agency.txt)
- 원본 파일명: `25.출연(연)연구자정보 검색(기관용)_매뉴얼_2025.pdf`
- PDF 원문과 전체 텍스트 추출본은 위 docs 경로에 그대로 보존했다.

## 함정

- NTIS 서비스별 활용신청/승인이 필요할 수 있다. 미승인 응답이면 이 recipe의 apiSn으로 신청 상태를 먼저 확인한다.
- 검색어, 기관명, 과제명 등 한글 값은 UTF-8 URL 인코딩을 전제로 호출한다.
- 기관용 API는 이용대상 제한이 있으므로 소속기관 권한과 신청 가능 범위를 먼저 확인한다.
- 저작권/이용허락: 제3유형:출처표시+변경금지.
- 연구자명, 국가연구자번호, 생년월일은 개인정보 성격이 있으므로 목적에 필요한 최소값만 처리한다.
