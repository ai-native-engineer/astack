# 중소벤처기업부_중소기업 지원사업 공고 조회 서비스

> publicDataPk: 15157820 · 상세: https://www.data.go.kr/data/15157820/openapi.do
> checked: 2026-06-28 · 상태: **실호출 검증됨** (`/pblancBsnsService`, HTTP 200·resultCode 00·1479건 확인)
> 활용기간: 2026-06-28 ~ 2028-06-28 · 일일 10000건

## 언제 쓰나

기업마당 중소기업 지원사업 공고, 소상공인 지원사업, 정부지원사업, 중앙부처·지자체·유관기관 지원사업 공고 목록을 조회할 때 쓴다. 해시태그, 분야, 공고ID, 등록일, 수정일 기준 검색에 맞다.

## Endpoint

- host: `apis.data.go.kr/1421000/bizinfo`
- 주요 오퍼레이션: `/pblancBsnsService` — 중소기업 지원사업 공고 목록·상세성 필드 조회

## 키

- env: `DATA_GO_KR_API_KEY`
- query parameter: `serviceKey`
- 주입 예: `agents-env run DATA_GO_KR_API_KEY -- <명령>`

## 호출 예시

```bash
agents-env run DATA_GO_KR_API_KEY -- curl -sG \
  "https://apis.data.go.kr/1421000/bizinfo/pblancBsnsService" \
  --data-urlencode "serviceKey={{DATA_GO_KR_API_KEY}}" \
  --data-urlencode "dataType=json" \
  --data-urlencode "pageNo=1" \
  --data-urlencode "numOfRows=10"
```

## 필수/주요 파라미터

| 이름 | 의미 | 형식·예 |
|---|---|---|
| serviceKey | 인증키 | required, Decoding 키를 `--data-urlencode`로 전달 |
| dataType | 응답 형식 | `json` 지정 시 JSON |
| pageNo / numOfRows | 페이지 | `1` / `10` |
| searchLclasId | 분야 조회값 | 선택 |
| hashtags | 해시태그 조회값 | 예: `AI`, `수출`, `창업` |
| pblancId | 공고 고유 식별값 | 예: `PBLN_000000000123685` |
| registDe | 등록일자 | 공식 설명은 "공고를 등록한 일자"; 형식은 상세 페이지에 별도 표기 없음 |
| updtPnttm | 수정일자 | 공식 설명은 "공고를 수정한 일자"; 형식은 상세 페이지에 별도 표기 없음 |

## 응답 핵심 필드

| 필드 | 의미 |
|---|---|
| pblancNm / pblancUrl / pblancId | 공고명 / 기업마당 URL / 공고ID |
| jrsdInsttNm / excInsttNm | 소관기관명 / 수행기관명 |
| bsnsSumryCn | 사업개요내용, HTML 포함 가능 |
| pldirSportRealmLclasCodeNm | 정책디렉토리 지원분야 대분류명 |
| creatPnttm / updtPnttm | 등록일시 / 수정일시 |
| reqstBeginEndDe | 신청기간 |
| trgetNm | 지원대상 |
| inqireCo | 조회수 |
| flpthNm / fileNm | 첨부파일 경로 / 첨부파일명, 여러 건은 `@`로 연결 |
| printFlpthNm / printFileNm | 본문 출력 파일 경로 / 파일명 |
| hashtags | 해시태그 |
| reqstMthPapersCn | 사업신청방법내용 |
| refrncNm | 문의처 |
| rceptEngnHmpgUrl | 사업신청 URL |

## 페이징

- `pageNo`와 `numOfRows`를 사용한다.
- JSON 응답의 전체 건수 필드를 확인하고 결과 목록을 페이지별로 합친다.
- 공고 목록은 HTML·첨부파일 문자열이 길 수 있으므로 대량 수집 시 원문 응답을 함께 보존한다.

## 함정

- JSON 파라미터명은 `type=json`이 아니라 `dataType=json`이다.
- `bsnsSumryCn`은 HTML 문자열로 온다. 화면 표시·요약 전에 태그 처리한다.
- 파일 경로와 파일명은 여러 건이 `@`로 합쳐져 올 수 있다. 같은 인덱스끼리 매칭한다.
- 신청 직후 403 `Forbidden`이 나오면 키-서비스 동기화 지연일 수 있다. 2026-06-28 실측에서 재시도 후 같은 `https`+`--data-urlencode` 호출이 정상화됐다.
