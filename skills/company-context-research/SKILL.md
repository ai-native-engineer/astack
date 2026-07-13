---
argument-hint: "[company or domain]"
name: company-context-research
description: "Company context research before outreach, sales prep, diligence, or account review using public surfaces, first-party pages, attachments, press, and official data such as DART/KRX/data.go.kr/Naver DataLab/KIPRIS/NTIS. Use when user asks 이 회사 맥락, company research, sales call prep, prospect qualification, target account review, or fragmented brand/legal/entity mapping. Do NOT use for standalone data.go.kr API calls, personal career research, generic web browsing, internal project context gathering, SimilarWeb-only traffic checks, or non-company topics."
---

# Company Context Research

## 멘탈 모델

기업명(또는 도메인) 하나를 받아 **영업 전 사전조사**에 필요한 공개/내부 맥락을 전수 수집하고, 웹에서 바로 탐색 가능한 **정규화 데이터 패키지 + HTML 뷰어**를 구축한다.

- **수집 축 4개**: ① 계정/회사 리서치 전략 ② 관할별 공식 데이터(DART / KRX / 공공데이터 / EDGAR) ③ 퍼블릭 웹 전수(재귀 크롤 및 첨부파일) ④ 보도자료 및 언론 분석
- **작동 원칙 2개**: **crawl-first**(로컬에 원본 페이지를 크롤하여 백업한 뒤 첨부 및 근거를 발굴) / **재귀 확장**(도메인 분석 후 연관 도메인 순차 조회)

## 작업 시작 전

리서치를 수행할 때 항상 회사별 작업 폴더를 먼저 생성한다.

```bash
bash scripts/init_company_workspace.sh "<company-or-domain>" [base_dir]
```

*(루트에 `01-context` 디렉토리가 존재하면 수동 이동 없이 자동으로 `01-context/company/` 하위로 대상 폴더가 리다이렉트되어 구축된다.)*

초기화 스크립트는 `templates/company-viewer.html`을 `index.html`로 복사한다. 별도 요청이 없으면 이 뷰어를 새로 만들지 말고 데이터만 채운다.

파일 구조와 데이터 규약, `source-manifest.tsv` 헤더는 `references/report-schema.md`를 따른다. 최소 산출물:

- `index.html` — 정적 HTML 데이터 탐색 뷰어
- `data/company-profile.json` — 기업개요/성장분석/방문자·소비자/R&D·특허/투자/조직·재무/뉴스/내부맥락의 canonical 데이터
- `data/viewer-data.json` — `index.html`이 읽는 단일 화면 데이터 번들
- `data/research-status.json` — 단계별 수집 상태와 evidence 체크리스트
- `source-manifest.tsv` — 방문 URL, 파일, 저장 경로, 메모 일지
- `attachments/` — PDF/PPT/DOCX/XLS 등 수집된 실물 원본 파일 폴더
- `press/press-inventory.tsv` — 보도/뉴스 인벤토리
- `recursive-crawl/` — 통합 재귀 크롤러 실행 사본 및 분석 인벤토리 TSV
- `public-mirror/` — 인용용 읽기 사본

Markdown 보고서는 canonical 산출물이 아니다. 필요한 경우에만 임시 판독 노트를 만들고, 최종 전달 전 `data/company-profile.json`에 반영한다.

## 라우팅 — 언제 무엇을 읽나

| 상황 | 읽을 것 |
|---|---|
| 영업 계정 판단, 법인 구조 분할 매핑, DART 중복명 해결 | `references/ref-strategic-resolution.md` |
| 재귀 크롤 제어·스크립트 명령어, JS 암호화 첨부 복원, 뉴스 API 폴백, DART 013 웹 보강 | `references/ref-technical-sweep.md` |
| Naver DataLab 또는 `$open-api` 정규화 산출물로 탭 데이터를 보강 | `references/ref-official-api-enrichment.md` |
| 최종 웹 패키지 포맷·디렉토리 구조 | `references/report-schema.md` |

크롤러(`research_crawler.py`), 보도 수집기(`research_press_tuner.py`), 공식 데이터 병합기(`merge_official_data.py`), 화면 번들 빌더(`build_viewer_data.py`), 전달 전 검증기(`validate_company_workspace.py`)의 실제 실행 명령어는 전부 `references/ref-technical-sweep.md`에 있다. 본문에서 명령어를 추측하지 말고 그 파일을 읽고 따른다.

## 핵심 체크리스트 (전달 전 자기검증)

- **시작 전 모드 판정**: 대상이 관계사인지 판별하여 `account-first` 인 경우 `summary.deal_status`, `summary.champion_buying_center`, `summary.participant_needs`를 먼저 채운다.
- **표면 매핑**: single-domain 가정을 깨고 IR 호스트, ATS 채용, CDN 등 분절된 Surface Map을 `data/company-profile.json.surface_map`에 먼저 명세한다.
- **DART 013(데이터 없음) 감지 시**: 단순 스킵하지 말고, 실적 공시 매핑 지연으로 판명되면 즉시 웹 쿼리로 최근 1분기/결산 매출액·영업이익·당기순이익 실적을 보강한다.
- **공식 API 위임**: `$open-api`가 설치돼 있으면 레시피 검색 → 호출 → 정규화 파일 병합 흐름을 따른다. 없으면 포함된 `data-go-kr` 절차로 접근 가능한 공식 데이터를 수집하고, 지원하지 않는 공급자는 관측 공백으로 남긴다.
- **Naver 구분**: Naver News는 보도 인벤토리이고, Naver DataLab은 검색 관심도 프록시다. 둘을 같은 데이터로 취급하지 않는다.
- **재무 손익 정규화**: DART 재무는 `operating_result_krw`, `net_result_krw`처럼 흑자 양수·적자 음수의 signed 값을 canonical로 쓴다. 손실 전용 컬럼만 있을 때만 하위호환 변환한다.
- **고용 프록시 명칭**: data.go.kr NPS workplace 값은 `국민연금 가입자수`로 표기한다. 고용보험 가입자수와 섞지 않는다.
- **상태 강제**: 전달 전 `data/research-status.json`의 모든 필수 step은 `done`, `partial`, 근거 있는 `skipped` 중 하나여야 한다. `done`은 실제 row/evidence가 있을 때만 쓴다.
- **인증 파라미터 경계**: canonical JSON, normalized TSV, manifest, viewer에는 `accessKey`, `serviceKey`, `crtfc_key` 같은 인증 파라미터 URL을 남기지 않는다. raw 호출 흔적은 `official-data/<provider>/raw/`에만 둔다.
- **산출물 무결성**: 인용한 자명하지 않은 모든 팩트는 `source-manifest.tsv`, `public-mirror/`, `attachments/`, 또는 원본 URL에 근거를 남긴다.
- **화면 데이터 번들**: `index.html`은 raw/TSV/API 파일을 직접 조합하지 않고 `data/viewer-data.json`만 읽는다.
- **뷰어 템플릿 유지**: 탭, 차트, 워드클라우드, 검색/정렬/페이지네이션 테이블은 `templates/company-viewer.html` 계약을 따른다.
- **최종 게이트**: 전달 직전 반드시 `python3 scripts/build_viewer_data.py <workspace>`를 실행한 뒤 `python3 scripts/validate_company_workspace.py <workspace>`를 통과시킨다.
- **브라우저 확인**: `index.html`은 `fetch()`를 쓰므로 `file://`로 열지 않는다. 전달 시 로컬 정적 서버를 켜고 `http://127.0.0.1:<port>/` URL을 연다.

## 안전선 (항상 — 추정 금지)

- 디자인이나 트렌디한 문구만 보고 회사의 실제 비즈니스 모델이나 ICP를 넘겨짚지 않는다.
- 모회사와 자회사를 명시적 근거 없이 묶어 취급하지 않는다.
- 오래된 주가 시세나 과거 공시를 현재 기업 가치인 것처럼 설명하지 않는다.
- "못 찾았다"를 "없다"로 바꾸지 않는다. 막힌 소스는 숨기지 말고 관측 공백으로 적는다.

## References

- `references/ref-strategic-resolution.md` — 영업 계정 판단, 법인 구조 분할 매핑 및 DART 중복명 해결 규칙
- `references/ref-technical-sweep.md` — 재귀 크롤 테이블 제어, 스크립트 명령어 규약, JS 암호화 첨부파일 다운로드 복원, 뉴스 API 폴백, DART 013 웹 보강, 최종 검증 지침
- `references/ref-official-api-enrichment.md` — Naver DataLab 및 `$open-api` 정규화 산출물 병합 규칙
- `references/report-schema.md` — 최종 웹 패키지 JSON/HTML 포맷 및 디렉토리 구조 명세
