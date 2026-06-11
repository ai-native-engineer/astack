---
argument-hint: "[company or domain]"
name: company-context-research
description: "Gather all relevant public and internal context about a company before outreach or diligence. Use for sales call prep, prospect qualification, target account review, or '이 회사 맥락 다 훑어줘'. Default to account-first mode when existing project/context files already exist. Mandatory behavior: map fragmented public surfaces first (legal entity, parent site, local brand site, B2B portal, careers, IR, CDN attachments), then crawl those surfaces and collect first-party attachments, press coverage, and official market data by jurisdiction (Korean DART/KRX/public-data layers, SEC EDGAR for US-listed)."
---

# Company Context Research

## 목적

기업명(또는 도메인) 하나를 받아 **영업 전 사전조사**에 필요한 그 회사의 공개 맥락을 전수 수집한다. 목표는 "회사 소개 요약"이 아니라, 영업 대화·실사에서 바로 꺼내 쓸 수 있는 **근거 자료 패키지**다.

- 수집 축 4개: ① 계정/회사 리서치 절차(account-research + company-research 합성) ② 관할별 공식 데이터(한국: DART·KRX·공공데이터 / 미국 상장: SEC EDGAR) ③ 퍼블릭 웹 전수(표면 매핑 → crawl-first 재귀 크롤 → 모든 첨부파일) ④ 보도자료·언론
- 작동 원칙 2개: **crawl-first**(몇 페이지 훑고 요약하지 말고, 먼저 전부 로컬에 크롤한 뒤 그 사본에서 첨부와 근거를 발굴) / **재귀 확장**(본 사이트 → 발견된 연관 도메인 → 반복)
- 입력 = 회사명, 출력 = 크롤 원본 + 첨부 + DART/KRX + 보도자료가 담긴 로컬 맥락 패키지. 그 외의 자동화(스냅샷 동기화, 검증 리포트, 전달 패키징 등)는 이 스킬의 범위가 아니다 — 필요하면 작업 세션에서 모델이 인라인으로 한다.

## Output Contract

항상 회사별 작업 폴더를 먼저 만든다.

```bash
bash scripts/init_company_workspace.sh "<company-or-domain>" [base_dir]
```

파일 구조와 섹션 규약은 `references/report-schema.md`를 따른다. 최소 산출물:

- `00-surface-map.md` — 법인/브랜드/부모회사/IR/CDN/채용/포털 표면 맵
- `01-public-web.md` — public surface 웹/문서/첨부 조사
- `02-public-press.md` — 보도자료/뉴스/인터뷰/파트너십/채용 시그널
- `03-market-data.md` — 관할별 공식 데이터(한국: KRX·DART·공공데이터 / 미국 상장: EDGAR)
- `04-internal-context.md` — 기존 접점/사내 맥락(있을 때)
- `05-company-brief.md` — 한 화면 요약 + 영업 포인트
- `attachments/` — PDF/PPT/DOCX/XLS 등 원본
- `source-manifest.tsv` — 방문 URL, 파일, 저장 경로, 메모
- `recursive-crawl/` — 재귀 크롤 원본(분절 표면 회사에서는 선택이 아니라 기본)
- `press/press-inventory.tsv` — 외부 보도 인벤토리(네이버 + Google News RSS)

## Workflow

### 1. Resolve the target first

- 회사명, 대표 도메인, 국가, 상장 여부를 먼저 확정한다.
- 법인명이 모호하면 크롤링 전에 정확한 엔티티를 먼저 해결한다.
- 기본 의도는 `sales pre-call / prospect qualification` 이다. 사용자가 더 좁은 목적을 줬다면 모든 단계에서 그 목적을 유지한다.
- 한국 기업/수입사/브랜드 운영사처럼 공개 표면이 분절될 수 있으면 **홈페이지 하나로 끝내지 말고 surface map을 먼저 만든다**: 법인명, 이메일 도메인, 부모회사 corporate site, 한국 소비자용 brand/D2C site, B2B portal, careers, IR host, first-party attachment host(CDN, q4cdn, Shopify CDN 등).
- surface map은 `00-surface-map.md`에 먼저 적고 시작한다. surface map 없이 본문 조사로 바로 들어가지 않는다.

### 2. Detect mode first

- 현재 작업 경로 또는 인접 프로젝트에 `context/` 폴더, 기존 영업 아카이브, 제안서/견적서 첨부, 프로젝트 문서가 이미 있고 회사명 키워드와 맞으면 **account-first mode** 로 간다.
- 아무 내부 흔적이 없고 회사만 처음 보는 상황이면 **cold research mode** 로 간다.
- `account-first` 에서는 공개 웹 조사가 내부 계정 맥락을 덮어쓰면 안 된다. 공개 웹은 현재 딜/챔피언/니즈를 보강하는 근거로만 쓴다.

### 3. Load the right references

- 시작 시 `references/source-patterns.md` 를 읽는다.
- `account-first` 이면 `references/account-priority.md` 를 읽는다.
- 엔티티가 분절돼 보이거나 브랜드/모회사/법인이 섞일 가능성이 있으면 `references/entity-resolution.md` 를 읽는다.
- 웹 수집 전 `references/public-sweep-checklist.md` 를 읽는다.
- 외부 보도 수집 전 `references/press-coverage.md` 를 읽는다.
- 분절 표면이 보이면 `references/recursive-crawl.md` 를 읽는다.
- 회사가 한국 법인이거나 한국 사업자등록/주소/법인 흔적이 보이면 `references/korean-market-data.md` 를 읽는다.

### 4. Recover internal context first when in account-first mode

- `account-first` 면 내부 맥락을 먼저 읽는다: 기존 `context/*.md`, 제안서/견적서/발송 이력, Slack / Gmail / Notion / Obsidian / 회의 메모 / 음성 메모.
- 먼저 답해야 할 질문: 지금 딜 단계가 어디인가, 내부 챔피언이 누구인가, 다음 미팅/다음 액션이 무엇인가, 참가자/이해관계자 니즈가 어떻게 나뉘는가, 리스크와 블로커가 무엇인가.
- 이 단계가 끝나기 전에는 generic company summary를 먼저 쓰지 않는다.

### 5. Sweep the public web thoroughly (crawl-first)

- 공개 웹 수집은 **`crawl` 스킬 또는 동급 로컬 크롤러를 우선 사용**한다. 몇 페이지를 브라우저/grep으로 훑고 요약만 남기는 식으로 끝내지 않는다.
- 표면이 분절돼 있으면 샘플링보다 먼저 재귀 크롤을 돈다:

```bash
python3 scripts/recursive_surface_crawl.py <seed-url...> --keyword <kw> --out <recursive-crawl-dir>
```

- 이 스크립트의 목적은 "바로 답을 쓰는 것"이 아니라 원본 5종을 먼저 만드는 것이다: `crawl-manifest.tsv`, `link-inventory.tsv`, `attachment-candidates.tsv`, `keep-list-candidates.tsv`, `shortlist.tsv`. 이후 `shortlist.tsv`를 1차 읽기 대상으로, `keep-list-candidates.tsv`를 2차 보강 대상으로 삼는다. `link-inventory.tsv` 전체를 다시 다 읽지 않는다.
- 첨부 후보는 본문 반영 전에 먼저 회수한다:

```bash
python3 scripts/download_attachment_candidates.py <attachment-candidates.tsv> --out <attachments-dir>
```

- 크롤이 중단됐어도 `recursive-crawl/pages/`가 있으면 `scripts/postprocess_recursive_crawl.py <dir>`로 인벤토리를 복구한다. broken slug/중복 경로가 보이면 `scripts/prune_recursive_crawl_pages.py <pages-dir>` 후 postprocess를 다시 돈다.
- 1차에서 `brand-related`/`local-brand` 도메인이 새로 나오면 `scripts/second_pass_from_shortlist.py <shortlist.tsv> --out <dir> --mirror-out-root <public-mirror-dir>`로 2차 패스를 돈다. 그 뒤에도 팔 가치가 있는 host가 남으면 **그 host의 URL을 시드로 `recursive_surface_crawl.py`를 다시 돌리는 방식으로 재귀를 반복**한다. 더 갈지/멈출지는 모델이 link-inventory의 신호(법인·브랜드 콘텐츠 표면이 계속 열리는가)로 직접 판단한다.
- 보고서에서 인용할 페이지는 raw `pages/`가 아니라 `scripts/mirror_selected_pages.py <shortlist.tsv> --out <public-mirror-dir>`로 만든 `public-mirror/` 경로를 쓴다.
- 재귀 크롤은 특히 Shopify/commerce 호스트에서 유용하지만 위험하다. 상품/컬렉션/계정/장바구니 노이즈가 커서 keep-list 후처리를 전제로 쓴다 (`references/recursive-crawl.md`).
- 홈페이지, sitemap, robots, 메인 내비게이션부터 시작하고, surface map에 잡힌 각 공개 표면의 고신호 섹션(about / product / solutions / industries / customers / docs / blog / newsroom / careers / IR / governance / pricing / partners)을 빠짐없이 훑는다.
- 첨부파일은 **same-domain만 보지 않는다**. first-party가 링크한 cross-domain 첨부(IR 호스트, CDN, q4cdn, Shopify CDN, media kit)도 포함한다. 수집 확장자: `.pdf`, `.docx`, `.pptx`, `.xlsx`, `.csv`. `attachments/`에 읽기 쉬운 이름으로 저장하고 `source-manifest.tsv`에 기록한다.
- 사이트가 매우 크더라도 무한 크롤은 하지 않는다. "모조리"의 뜻은 "고신호 페이지와 관련 첨부를 빠짐없이"이지, 저가치 반복 페이지까지 끝없이 긁는 것이 아니다.
- 회사가 반복해서 쓰는 단어, 전략 문장, 고객 언어, proof point, 수치 주장을 반드시 남긴다.
- 실제로 읽은 페이지/미러 파일 경로를 `01-public-web.md`에 남긴다. "봤다"고만 쓰지 않는다. 재귀 크롤을 썼다면 저장 페이지 수, 인벤토리 링크 수, 카테고리별 개수, 새로 발견된 연관 도메인, 새로 확보한 첨부, 노이즈가 큰 표면과 그 이유를 적는다.

### 6. Check external coverage

- 제3자 보도 수집은 스크립트로 시작한다 (`references/press-coverage.md` 참조):

```bash
agents-env run NAVER_CLIENT_ID NAVER_CLIENT_SECRET -- \
  python3 scripts/search_press.py "<회사명>" --out <workspace>/press
```

- 네이버 뉴스 API(한국 본진) + Google News RSS(연 윈도우·글로벌)가 `press/press-inventory.tsv`로 합쳐진다. 영문/글로벌 보도는 `tvly search --topic news`로 보강한다.
- 최근 보도자료, 뉴스룸 포스트, 인터뷰, 펀딩, 파트너십, 소송, 채용/성장 시그널, M&A, 주요 출시를 모은다.
- 회사가 직접 쓴 주장과 제3자 보도를 구분한다. 인용할 기사는 원문 URL을 미러해 근거로 남긴다.
- 회사 전용 newsroom이 없으면 브랜드 사이트, IR 릴리스, 외부 업계지, 채용 플랫폼으로 대체하고, 공식 newsroom 부재를 공백으로 남긴다.

### 7. Add official market data when relevant

- 회사 관할의 공식 공시·등기·공공 데이터를 1차 근거로 쓴다. 회사가 스스로 말하는 것보다 우선하는 근거 레이어다.
- 한국 법인 흔적이 있으면 `references/korean-market-data.md`를 따른다 — KRX 상장 확인, DART 공시(상장 여부와 무관하게 시도), 비상장·소규모 법인은 공공데이터 보강까지.
- 다른 시장의 상장사는 해당 시장 공시 시스템을 쓴다. 미국 상장이면 SEC EDGAR — 무키로 full-text search와 submissions/companyfacts JSON API를 쓸 수 있다(User-Agent에 연락처 필요).
- 접근 수단(키·계정·승인)이 없는 레이어는 꾸며내지 않고 `03-market-data.md`에 관측 공백으로 명시한다.
- 일별 시세 snapshot은 실시간 가격처럼 말하지 않는다.

### 8. Write the brief

- `05-company-brief.md`에 정리한다: 현재 딜 상태/다음 액션, 내부 챔피언/buying center, 참가자별 니즈, 회사가 실제로 하는 일, 왜 지금 봐야 하는가, 근거 기반 buying signal, 반복적으로 쓰는 언어, 리스크/red flag, 아웃리치 각도.
- 자명하지 않은 주장에는 항상 작업 폴더 안 근거가 남아 있어야 한다.
- `account-first` 에서는 브리프 상단을 **generic company overview가 아니라 deal context**로 시작한다.
- parent company 정보는 예산/의사결정 구조를 바꾸거나, 브랜드/운영 범위를 규정하거나, local entity만으로 설명이 안 될 때만 전면에 올린다. 그 외에는 supporting context로 내린다.

## Mandatory Checks

- surface map을 먼저 만들었는가
- `account-first` 여부를 먼저 판정했는가
- corporate / brand / portal / careers / IR / attachment host 중 무엇이 실제로 존재하는지 분리했는가
- 분절 표면 회사에서 recursive crawl 원본을 먼저 만들었는가
- shortlist 상위 링크를 먼저 읽고, keep-list 기준으로 후속 읽기 대상을 좁혔는가
- same-domain이 아니라 **first-party linked attachment** 까지 수집했는가
- 회사 뉴스룸 + 외부 보도를 둘 다 봤는가
- 관할별 공식 데이터를 시도했는가 — 한국 법인 흔적이면 DART(+비상장이면 공공데이터), 한국 상장 가능성이면 KRX, 해외 상장이면 해당 시장 공시(미국: EDGAR)
- 기존 프로젝트 context가 있으면 먼저 읽었는가
- 브리프가 `현재 딜 상태 / 챔피언 / 다음 액션` 으로 시작하는가
- `source-manifest.tsv`의 saved_path가 전부 실존하는지 확인했는가
- API 차단, 파일 누락, entity ambiguity, paywall 등 관측 공백을 명시했는가

## Anti-Hallucination Rules

- 디자인, 폰트, 프레임워크만 보고 사업 모델이나 ICP를 추정하지 않는다.
- 모회사, 자회사, 브랜드, 계열사를 명시적 근거 없이 합치지 않는다.
- 회사 공식 홈페이지가 없다고 해서 public web 조사를 끝내지 않는다. 브랜드 사이트, B2B 포털, 채용 표면, CDN 첨부, IR 호스트를 계속 추적한다.
- 기존 계정 맥락이 있는데 generic global parent 설명으로 브리프를 시작하지 않는다.
- 오래된 보도자료나 일별 시세 snapshot을 현재 상태처럼 말하지 않는다.
- "못 찾았다"를 "없다"로 바꾸지 않는다. 막힌 소스는 숨기지 말고 공백으로 적는다.

## References

- `references/source-patterns.md` — account research / company research 합성 패턴
- `references/account-priority.md` — account-first sales prep 우선순위
- `references/entity-resolution.md` — 분절된 공개 표면 해상도 규칙
- `references/public-sweep-checklist.md` — 사이트/첨부/뉴스룸 점검표
- `references/recursive-crawl.md` — 재귀 크롤 + 인벤토리 후처리 규칙
- `references/press-coverage.md` — 외부 보도 수집(네이버 API·Google News RSS·tavily) 규칙
- `references/korean-market-data.md` — KRX + DART 사용 규칙
- `references/report-schema.md` — 작업 폴더와 최종 보고 형식
