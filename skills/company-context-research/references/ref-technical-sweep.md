# Technical Data Collection & Web Package Guidelines

본 문서는 `company-context-research` 스킬에서 공공 웹 크롤링(crawl-first), 제3자 보도(Press), 관할 데이터(DART/KRX), 정적 웹 패키지 검증을 수행하는 기술 지침이다.

## 목차

- 0. 스크립트 실행 명령어 규약
- 1. Crawl-First & Recursive Surface Crawl
- 2. Public Sweep & Troubleshooting
- 3. Press Coverage
- 4. Korean Market Data
- 5. Web Package Handoff Gate

## 0. 스크립트 실행 명령어 규약

작업 폴더는 항상 먼저 만든다.

```bash
bash scripts/init_company_workspace.sh "<company-or-domain>" [base_dir]
```

출력 경로를 `$workspace`로 잡은 뒤 아래 명령을 실행한다.

### research_crawler.py

**1. 1차 재귀 크롤링 및 첨부파일 자동 다운로드**

```bash
python3 scripts/research_crawler.py --mode crawl <seed-url...> \
  --keyword <kw1> --keyword <kw2> \
  --out "$workspace/recursive-crawl" --download --download-limit 20
```

`--download`는 자동 첨부를 `$workspace/attachments/`에 저장하고, 다운로드 로그는 `$workspace/recursive-crawl/download-report.tsv`에 남긴다.

**2. 로컬 크롤 파일 복구**

```bash
python3 scripts/research_crawler.py --mode rebuild \
  --out "$workspace/recursive-crawl" --keyword <kw1>
```

**3. 오타 슬러그 및 저신호 페이지 삭제**

```bash
python3 scripts/research_crawler.py --mode prune "$workspace/recursive-crawl/pages"
```

**4. 고신호 우선 미러링**

```bash
python3 scripts/research_crawler.py --mode mirror \
  "$workspace/recursive-crawl/shortlist.tsv" --out "$workspace/public-mirror"
```

**5. 2차 패스 및 연관 도메인 확장**

```bash
python3 scripts/research_crawler.py --mode second-pass \
  "$workspace/recursive-crawl/shortlist.tsv" \
  --out "$workspace/recursive-crawl-v2" --download
```

### research_press_tuner.py

제3자 언론 보도 수집:

```bash
python3 scripts/research_press_tuner.py "<회사명>" ["<회사명> <대표명>" ...] --out "$workspace/press"
```

네이버 API가 지연되거나 키가 없으면 Tavily News Search로 폴백한다. 실패한 소스는 숨기지 말고 `data/research-status.json`의 해당 step notes에 남긴다.

### merge_official_data.py

공식 API 호출은 `$open-api`가 처리한다. 이 스크립트는 `$open-api` 또는 수동 정규화 단계가 만든 `official-data/<provider>/*.tsv`만 읽어 화면 데이터에 병합한다.

```bash
python3 scripts/merge_official_data.py "$workspace"
```

현재 병합 대상은 DART 재무·투자/자본 보조 신호, Naver DataLab 검색 관심도, data.go.kr 국민연금·사업자상태·조달/지원사업 검색, KIPRIS 특허/상표/키워드, NTIS 과제 TSV다. API 키, 엔드포인트, 페이징, raw 응답 저장 방식은 이 스킬에 두지 않고 `$open-api` 레시피가 관리한다.

### validate_company_workspace.py

전달 직전 화면 데이터 번들을 만든 뒤 검증한다.

```bash
python3 scripts/build_viewer_data.py "$workspace"
python3 scripts/validate_company_workspace.py "$workspace"
```

빌더는 최신 `templates/company-viewer.html`을 `index.html`로 동기화한 뒤 `data/company-profile.json`, `data/research-status.json`, `source-manifest.tsv`, 주요 정규화 TSV를 `data/viewer-data.json`으로 합친다. 검증기는 JSON/TSV 무결성, `source-manifest.tsv` 저장 경로, 필수 step 상태, 얕은 크롤 false-positive, 공식 데이터 보류 false-positive, 인증 파라미터 누출, React 차트/워드클라우드/정렬 테이블/7개 탭 뷰어 계약을 확인한다.

검증 후에는 `file://`가 아니라 로컬 정적 서버로 확인한다. `index.html`이 `fetch("./data/viewer-data.json")`를 쓰기 때문에 직접 파일 열기는 브라우저 보안 정책으로 실패한다.

```bash
python3 -m http.server 8766 -b 127.0.0.1 -d "$workspace"
open http://127.0.0.1:8766/
```

이미 포트가 사용 중이면 다른 빈 포트를 쓴다. 사용자에게는 파일 경로가 아니라 서버 URL을 준다.

## 1. Crawl-First & Recursive Surface Crawl

표면이 분절된 기업은 홈페이지 하나로 끝내지 않는다. 법인 사이트, 브랜드 사이트, B2B 포털, IR/CDN, 채용, 뉴스룸, 제품 문서, 파트너 포털을 seed 또는 second-pass로 확장한다.

생성되는 핵심 인벤토리:

- `crawl-manifest.tsv`
- `link-inventory.tsv`
- `attachment-candidates.tsv`
- `download-report.tsv`
- `keep-list-candidates.tsv`
- `shortlist.tsv`
- `pages/`

`link-inventory.tsv`와 `shortlist.tsv`가 모두 헤더뿐이면 재귀 확장이 완료된 것이 아니다. 이 경우 `public_web_crawl`은 `partial`로 두고, 막힌 URL/host와 다음 확장 후보를 notes에 적는다.

Commerce 노이즈 규칙:

- Shopify/Commerce 기반 사이트는 `products/`, `collections/`, `cart`, `checkout`, `account` 계열을 낮은 신호로 본다.
- `/pages/`, `/blogs/`, `/about-us`, `newsroom`, `press`, `careers`, `IR` 계열을 우선 판독한다.

## 2. Public Sweep & Troubleshooting

High-signal 우선순위:

- `about`
- `product`
- `solutions`
- `case studies`
- `docs`
- `blog`
- `newsroom/press`
- `careers`
- `IR`
- `pricing`
- `partners`

예외 처리:

- `<meta http-equiv="refresh">`만 남아있고 본문이 없으면 redirect 대상 URL로 다시 크롤한다.
- 403이나 빈 본문이면 `Mozilla/5.0` 헤더 curl 또는 브라우저 기반 조회로 보강한다.
- JS 암호화 다운로드는 페이지 내 `fnDownload`, `downloadFile`, `fnDownloadFile` 계열 함수와 실제 servlet 경로를 역추적한다.
- 막힌 표면은 `없음`으로 쓰지 말고 `gaps`와 `research-status` notes에 관측 공백으로 남긴다.

## 3. Press Coverage

뉴스 수집은 자사 발표와 제3자 보도를 구분한다.

- Layer 1: Naver News API + Google News RSS
- Layer 2: Tavily News Search
- Layer 3: 빅카인즈 수동 확인은 최근 3년 이내 보도로 충분하지 않을 때만 사용

중요 기사는 스니펫에 의존하지 않고 원문 URL 또는 `public-mirror/` 경로를 `source-manifest.tsv`와 `data/company-profile.json.sources`에 남긴다.

## 4. Korean Market Data

한국 법인 흔적이 있으면 DART/KRX/공공데이터를 확인한다.

- 상장 여부: KRX, 주식 시세, stock code
- DART: `corp_code`, `corp_cls`, 최근 공시, 기업 개황, 최근 결산 재무제표
- 비상장/소규모 법인: 국민연금 사업장 가입자 추이, 사업자등록 상태, 정부 지원사업

Naver DataLab 또는 DART/data.go.kr/KIPRIS/NTIS 정규화 산출물로 탭 데이터를 보강할 때는 `references/ref-official-api-enrichment.md`를 읽는다. DART/data.go.kr/KIPRIS/NTIS 호출은 `$open-api` 레시피 검색·호출·적립 흐름을 우선한다.

DART 013 처리:

- 단순 데이터 없음으로 끝내지 않는다.
- 공시 의무 부재, 합병/분할, 회사명 중복, 최근 실적 공시 지연 중 무엇인지 기록한다.
- 필요한 경우 웹 보도/감사보고서/공공데이터로 최근 매출액, 영업이익, 당기순이익을 보강한다.

## 5. Web Package Handoff Gate

최종 전달 기준:

1. `data/company-profile.json`의 `summary.one_screen`이 비어 있지 않다.
2. `surface_map.surfaces` 또는 `surface_map.contradictions_unresolved_edges`에 single-domain 가정을 검증한 흔적이 있다.
3. `sections`의 웹 노출 7개 탭과 내부맥락 섹션이 모두 존재한다.
4. `data/research-status.json` 필수 step이 전부 `done`, `partial`, 근거 있는 `skipped` 중 하나이며, `done`은 실제 evidence가 있을 때만 쓴다.
5. `source-manifest.tsv`의 `saved_path`는 실제 파일/폴더만 가리킨다.
6. Naver DataLab, NTIS, 조달/계약, 지원사업, 재귀 크롤 확장을 보류했으면 상태가 `partial` 또는 `skipped`로 드러난다.
7. normalized TSV와 canonical JSON에 인증 파라미터가 포함된 API 호출 URL이 없다.
8. `python3 scripts/build_viewer_data.py "$workspace"`와 `python3 scripts/validate_company_workspace.py "$workspace"`가 통과한다.

로컬 확인은 정적 서버로 한다.

```bash
python3 -m http.server 8766 -b 127.0.0.1 -d "$workspace"
open http://127.0.0.1:8766/
```

브라우저에는 파일 경로가 아니라 서버 URL을 전달한다.
