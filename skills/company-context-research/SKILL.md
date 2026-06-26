---
argument-hint: "[company or domain]"
name: company-context-research
description: "Company context research before outreach, sales prep, diligence, or account review using public surfaces, first-party pages, attachments, press, and official market data. Use when user asks 이 회사 맥락, company research, sales call prep, prospect qualification, target account review, or fragmented brand/legal/entity mapping. Do NOT use for personal career research, generic web browsing, internal project context gathering, SimilarWeb-only traffic checks, or non-company topics."
---

# Company Context Research

## 멘탈 모델

기업명(또는 도메인) 하나를 받아 **영업 전 사전조사**에 필요한 그 회사의 공개 맥락을 전수 수집하고, 영업 포인트가 도출된 **근거 자료 패키지**를 구축한다.

- **수집 축 4개**: ① 계정/회사 리서치 전략 ② 관할별 공식 데이터(DART / KRX / 공공데이터 / EDGAR) ③ 퍼블릭 웹 전수(재귀 크롤 및 첨부파일) ④ 보도자료 및 언론 분석
- **작동 원칙 2개**: **crawl-first**(로컬에 원본 페이지를 크롤하여 백업한 뒤 첨부 및 근거를 발굴) / **재귀 확장**(도메인 분석 후 연관 도메인 순차 조회)

## 작업 시작 전

리서치를 수행할 때 항상 회사별 작업 폴더를 먼저 생성한다.

```bash
bash scripts/init_company_workspace.sh "<company-or-domain>" [base_dir]
```

*(루트에 `01-context` 디렉토리가 존재하면 수동 이동 없이 자동으로 `01-context/company/` 하위로 대상 폴더가 리다이렉트되어 구축된다.)*

파일 구조와 섹션 규약, `source-manifest.tsv` 헤더는 `references/report-schema.md`를 따른다. 최소 산출물:

- `00-surface-map.md` — 법인/브랜드/부모회사/IR/CDN/채용/B2B포털 표면 맵
- `00-target.md` — 조사 대상 법인 기본 정보 및 인스턴스 정보
- `01-public-web.md` — public surface 웹/문서/첨부 조사 결과
- `02-public-press.md` — 보도자료/뉴스/인터뷰/파트너십 타임라인 및 분석
- `03-market-data.md` — 관할별 공식 데이터 및 3개년 재무 트렌드 시각화 차트
- `04-internal-context.md` — Monday.com, CRM 등 사내 접점 및 내부 맥락
- `05-company-brief.md` — 원스크린 요약, 딜 상황, 부서별 니즈, 수출 물류/환 리스크 경고
- `attachments/` — PDF/PPT/DOCX/XLS 등 수집된 실물 원본 파일 폴더
- `source-manifest.tsv` — 방문 URL, 파일, 저장 경로, 메모 일지
- `recursive-crawl/` — 통합 재귀 크롤러 실행 사본 및 분석 인벤토리 TSV 5종

## 라우팅 — 언제 무엇을 읽나

| 상황 | 읽을 것 |
|---|---|
| 영업 계정 판단, 법인 구조 분할 매핑, DART 중복명 해결 | `references/ref-strategic-resolution.md` |
| 재귀 크롤 제어·스크립트 명령어, JS 암호화 첨부 복원, 뉴스 API 폴백, DART 013 웹 보강 | `references/ref-technical-sweep.md` |
| 최종 보고서 마크다운 포맷·디렉토리 구조 | `references/report-schema.md` |

스크립트 6모드(`crawl`/`rebuild`/`prune`/`mirror`/`second-pass`/`visualize`·`scan-risk`)와 보도 수집기(`research_press_tuner.py`)의 실제 실행 명령어는 전부 `references/ref-technical-sweep.md`에 있다. 본문에서 명령어를 추측하지 말고 그 파일을 읽고 따른다.

## 핵심 체크리스트 (전달 전 자기검증)

- **시작 전 모드 판정**: 대상이 관계사인지 판별하여 `account-first` 인 경우 브리프 상단을 글로벌 소개가 아닌 **딜(Deal) 상태와 부서별 실무 니즈**로 시작한다.
- **표면 매핑**: single-domain 가정을 깨고 IR 호스트, ATS 채용, CDN 등 분절된 Surface Map을 `00-surface-map.md`에 먼저 명세한다.
- **DART 013(데이터 없음) 감지 시**: 단순 스킵하지 말고, 실적 공시 매핑 지연으로 판명되면 즉시 웹 쿼리로 최근 1분기/결산 매출액·영업이익·당기순이익 실적을 보강한다.
- **산출물 무결성**: 인용한 자명하지 않은 모든 팩트는 `source-manifest.tsv` 및 `public-mirror/` 내의 클릭 가능한 실물 `file://` 링크로 근거를 남긴다.

## 안전선 (항상 — 추정 금지)

- 디자인이나 트렌디한 문구만 보고 회사의 실제 비즈니스 모델이나 ICP를 넘겨짚지 않는다.
- 모회사와 자회사를 명시적 근거 없이 묶어 취급하지 않는다.
- 오래된 주가 시세나 과거 공시를 현재 기업 가치인 것처럼 설명하지 않는다.
- "못 찾았다"를 "없다"로 바꾸지 않는다. 막힌 소스는 숨기지 말고 관측 공백으로 적는다.

## References

- `references/ref-strategic-resolution.md` — 영업 계정 판단, 법인 구조 분할 매핑 및 DART 중복명 해결 규칙
- `references/ref-technical-sweep.md` — 재귀 크롤 5종 테이블 제어, 스크립트 명령어 규약, JS 암호화 첨부파일 다운로드 복원, 뉴스 API 폴백 및 DART 013 웹 보강 기술 지침
- `references/report-schema.md` — 최종 결과 보고서의 마크다운 포맷 및 디렉토리 구조 명세
