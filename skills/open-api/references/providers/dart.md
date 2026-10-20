# Provider: opendart.fss.or.kr (DART)

전자공시·회사 공시·재무제표 조회가 목적이면 opendart.fss.or.kr(DART)를 쓴다.

- checked: 2026-06-28
- domain: `opendart.fss.or.kr`
- alias: DART/다트
- key env: `API_K_DART`
- recipes: `references/recipes/dart/*.md`

## 언제 쓰나

- 사업보고서, 반기보고서, 분기보고서, 감사보고서
- 단일회사 주요계정, 재무제표
- 공시 목록, 접수번호, 보고서 원문
- 상장사뿐 아니라 DART에 공시가 있는 비상장·기타법인 확인

## 키

- 기본 키 이름: `API_K_DART`
- `agents-env run API_K_DART -- <명령>`을 우선한다.

## 흐름

1. 회사명으로 corp code를 먼저 확보한다.
2. 동명이인·계열사·옛 이름을 확인해 corp code를 고른다.
3. 공시 목록으로 기간, 보고서 종류, 접수번호 존재를 확인한다.
4. 재무 API는 공시 목록에서 보고서 존재를 확인한 뒤 호출한다.
5. 재무 API가 0건이면 감사보고서·사업보고서 원문 공시 여부를 별도로 본다.

## 검증된 기본 레시피

| 작업 | recipe |
|---|---|
| DART 고유번호 목록 다운로드 | [corp-code-list](../recipes/dart/corp-code-list.md) |
| 기업 개황 조회 | [company-overview](../recipes/dart/company-overview.md) |
| 공시 목록 조회 | [disclosure-list](../recipes/dart/disclosure-list.md) |
| 단일회사 주요계정 재무 조회 | [single-company-financial-account](../recipes/dart/single-company-financial-account.md) |

## corp code 선택

- `corpCode.xml`에서 회사명이 중복되면 `stock_code`, `corp_cls`, `bizr_no`, `est_dt`를 같이 본다.
- `stock_code`가 있으면 상장 법인 판별에 강한 단서지만, 공란이어도 DART 대상이 아닐 수는 없다.
- `corp_cls`는 `Y` 유가, `K` 코스닥, `N` 코넥스, `E` 기타다. 상장사를 찾는 작업이면 `Y`/`K`를 우선한다.
- 분할, 합병, 사명 변경이 의심되면 사업자번호와 설립일로 대조한다.

## 함정

- "조회된 데이타가 없습니다" 또는 DART `013`은 키 실패가 아니라 조건 0건일 수 있다.
- `013`이면 corp code 오선택, 보고서 미존재, 공시 매핑 지연, 합병/분할/상장폐지, 공시 의무 부재를 분리해서 확인한다.
- 회사명 검색 실패 시 법인명 표기, 영문명, 옛 이름을 바꿔 본다.
- 재무제표 API 미조회와 DART 공시 부재는 다르다.
- `corpCode.xml`은 XML 본문이 아니라 zip이며 내부 `CORPCODE.xml`을 풀어 파싱한다.
- 실적 공시 매핑 지연이면 웹 공시/감사보고서/보도자료로 매출액·영업이익·당기순이익을 보강하고, API 관측 공백은 그대로 남긴다.
- 키 없음으로 단정하기 전 `agents-env run API_K_DART -- <명령>`로 실제 키 주입 경로를 확인한다.
