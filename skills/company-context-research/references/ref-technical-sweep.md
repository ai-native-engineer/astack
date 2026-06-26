# Technical Data Collection & Crawl Guidelines

본 문서는 `company-context-research` 스킬에서 공공 웹 크롤링(crawl-first), 제3자 보도(Press), 그리고 국가별 관할 데이터(DART/KRX)를 전수 조사하고 예외 상황에 대처하기 위한 기술적인 통합 지침을 다룹니다.

---

## 0. 스크립트 실행 명령어 규약

수집 단계는 통합 크롤러 엔진 `research_crawler.py`와 보도 수집기 `research_press_tuner.py`로 제어합니다.

### research_crawler.py (모드별)

**1. 1차 재귀 크롤링 및 첨부파일 자동 다운로드** — 지정된 도메인 시드를 바탕으로 재귀 크롤을 수행하고, 감지된 첨부파일(JS 암호화 다운로드 주소 자동 복원 포함)을 함께 회수합니다.

```bash
python3 scripts/research_crawler.py --mode crawl <seed-url...> \
  --keyword <kw1> --keyword <kw2> \
  --out <recursive-crawl-dir> --download --download-limit 20
```

**2. 로컬 크롤 파일 복구 (rebuild)** — 작업이 도중에 중단됐어도 `pages/`에 로컬 캐시가 있으면 처음부터 다시 긁지 않고 원본 TSV 테이블들만 동적으로 재생성합니다.

```bash
python3 scripts/research_crawler.py --mode rebuild \
  --out <recursive-crawl-dir> --keyword <kw1>
```

**3. 오타 슬러그 및 저신호 페이지 삭제 (prune)**

```bash
python3 scripts/research_crawler.py --mode prune <recursive-crawl/pages>
```

**4. 고신호 우선 미러링 (mirror)** — 인용할 숏리스트 페이지들을 `public-mirror/` 디렉토리에 깔끔하게 이관하여 보고서 인용 근거로 씁니다.

```bash
python3 scripts/research_crawler.py --mode mirror <recursive-crawl/shortlist.tsv> --out <public-mirror-dir>
```

**5. 2차 패스 및 연관 도메인 확장 (second-pass)** — 1차 크롤링 결과에서 새로 드러난 연관 브랜드/도메인을 대상으로 타겟을 확장 수집합니다.

```bash
python3 scripts/research_crawler.py --mode second-pass <recursive-crawl/shortlist.tsv> --out <second-pass-dir> --download
```

**6. 재무 시각화 및 수출 물류 리스크 분석 자동 생성**

```bash
# 03-market-data.md에 3개년 매출 및 이익 █ 차트 자동 생성
python3 scripts/research_crawler.py --mode visualize --market-data-path <workspace>/03-market-data.md

# 05-company-brief.md에 초고비중 해외 수출 리스크 경고 자동 추가
python3 scripts/research_crawler.py --mode scan-risk --market-data-path <workspace>/03-market-data.md --brief-path <workspace>/05-company-brief.md
```

### research_press_tuner.py (외부 보도)

제3자 언론 보도 수집을 실행합니다.

```bash
python3 scripts/research_press_tuner.py "<회사명>" ["<회사명> <대표명>" ...] --out <workspace>/press
```

* **Timeout & Fallback 작동**: 네이버 API 통신 지연 시 15초 제한 후 1차 직접 curl 조회 ➔ 실패 시 2차 Tavily News Search API로 자동 전환되어 인벤토리를 확보합니다.

---

## 1. Crawl-First & Recursive Surface Crawl

표면이 분절된 기업(소비자 사이트, 법인 사이트, B2B 포털이 분리된 경우)은 홈페이지 하나로 끝내지 않고 **재귀 확장(Recursive Crawl)**을 통해 전체적인 인벤토리를 생성합니다.

### 📌 재귀 크롤 실행 가이드라인
* ** modes & actions**:
  - `crawl`: 시드 URL과 타깃 키워드를 받아 재귀 파싱 및 크롤 수행.
  - `rebuild`: 이미 받아진 `pages/` 아카이브가 존재하는 경우, 처음부터 크롤링하지 않고 인벤토리 데이터(TSV 5종)만 후처리 재생성.
  - `prune & rebuild`: 오타 슬러그나 저신호 페이지를 제거(`prune`)한 뒤 인벤토리 재구성.
* **생성되는 핵심 인벤토리 (5종)**:
  - `crawl-manifest.tsv`: 실제 저장된 페이지 목록
  - `link-inventory.tsv`: 발견된 모든 링크를 카테고리별로 매핑한 원장
  - `attachment-candidates.tsv`: PDF/DOC/PPT 등 수집용 첨부파일 후보
  - `keep-list-candidates.tsv`: 사람이 실제 정밀 판독하기 위해 거르는 필터 목록
  - `shortlist.tsv`: 바로 읽기 위해 순위를 정한 상위 20개 후보 (우선순위: 첨부 > B2B포털 > 로컬브랜드 > 브랜드관련 > 본사)
* **Commerce Noise Rule**:
  - Shopify/Commerce 기반 사이트는 상품 목록 및 장바구니 노이즈가 큽니다. `products/`, `collections/`, `cart`, `checkout`, `account` 계열은 수집에서 배제하고, `/pages/`, `/blogs/`, `/about-us` 계열만 읽기 대상으로 남깁니다.
* **1차 / 2차 패스 재귀 확장**:
  - 1차 패스에서 새로운 로컬 도메인이나 브랜드 도메인이 감지되면 이를 시드로 삼아 2차 수집 패스를 반복 수행합니다.

---

## 2. Public Sweep & Troubleshooting

### 💡 High-Signal Page 우선순위
* `about`, `product`, `solutions`, `case studies`, `docs`, `blog`, `newsroom/press`, `careers`, `IR`, `pricing`, `partners`.
* same-domain에 국한하지 않고, 연동된 q4cdn, Shopify CDN, 미디어 키트 CDN 등 cross-domain 경로의 first-party attachment(`.pdf`, `.docx`, `.xlsx`, `.pptx`)를 모두 모읍니다.

### 🛠️ 수집 예외 상황 트러블슈팅
1. **Client-Side Redirect 감지**:
   - `<meta http-equiv="refresh">`만 남아있고 본문이 없으면 client-side redirect이므로 지시된 대상 URL로 다시 크롤링을 요청합니다.
2. **User-Agent 차단 및 403**:
   - `crawl` 스킬로 수집된 결과가 비정상적으로 부실하면, `Mozilla/5.0` 브라우저 헤더를 curl에 명시적으로 주입하여 재조회합니다.
3. **JS 암호화 다운로드 역추적 (국내 기업 특화)**:
   - `<a href="...">` 태그 대신 `onclick="fnDownloadFile(encData)"` 형태로 첨부파일을 암호화하는 경우, 페이지 내 JS에서 `fnDownload` 함수의 실제 서블릿 매핑 경로를 역추적(예: `/api/common/files/download?encData=`)한 뒤, 원래 페이지 주소를 `Referer` 헤더에 실어 curl 다운로드 루프를 돌립니다.

---

## 3. Press Coverage (제3자 보도)

뉴스 수집은 자사 발표(보도자료)와 제3자 보도(언론사 분석)를 완벽히 구분해야 하며, 다음의 3개 레이어를 거칩니다.

* **Layer 1: search_press.py (Naver API + Google News RSS)**:
  - 쿼리는 회사명으로 시작하고, 검색 결과(`total`)가 1,100건을 상회하여 경고가 뜨면 `회사명+대표명`, `회사명+브랜드`로 쿼리를 분할 쿼리하여 API 한계를 우회합니다.
  - **Hang/Timeout 발생 시**: 네이버 OpenAPI 직접 curl 호출(15초 타임아웃) ➔ 실패 시 Tavily News Search (`tvly search --topic news`) API로 순차 자동 폴백을 가동합니다.
* **Layer 2: Tavily Search (글로벌 보강)**:
  - 글로벌 외신 보도, 해외 시장 리뷰, 영어 실적 보도 자료를 잡는 보완책으로 사용합니다.
* **Layer 3: 빅카인즈 (3년 이상 과거 폴백)**:
  - 최근 3년 이내 뉴스로 분석이 충분한 경우는 빅카인즈 웹 UI 수동 조회를 skip하고 기록에 남깁니다.
* **인용 기사의 Mirroring**:
  - 보고서에 인용하거나 팩트로 제시할 중요 기사는 스니펫에 의존하지 않고 원문 주소를 미러하여 `public-mirror/` 디렉토리에 보존합니다.

---

## 4. Korean Market Data (DART/KRX)

한국 법인 흔적(사업자등록번호, 주소 등)이 있는 타깃은 반드시 DART/KRX 조회를 진행합니다.

* **Layer 1: 상장 여부 및 주가 시세**:
  - `data-go-kr` 스킬로 주식 시세를 확인하되, API 승인 제약이 있으면 즉시 StockAnalysis나 Google Finance 웹 쿼리로 대체하고 Gap으로 남기지 않습니다.
* **Layer 2: DART 공시 조회**:
  - `API_K_DART` 키를 사용하여 `corp_code`를 찾고 최근 공시, 기업 개황, 최근 결산 재무제표를 수집합니다.
  - **중복 법인명 판별**: 상장법인은 `stock_code`가 존재하고 `corp_cls`가 `Y` 또는 `K`이므로 비상장/기타법인(`E`)과 혼동하지 않도록 확실히 대조합니다.
  - **DART 013 (데이터 없음) 처리**:
    - 등기상 존재하나 공시 의무가 없는 경우, 혹은 최근 합병/분할 개편 이력이 있는지 footer와 보도를 조회합니다.
    - 단일회사 주요재무사항 계정 조회 지연으로 인해 013이 발생한 경우, 지체 없이 **Web Financial Fallback**을 통해 네이버 금융, 언론 실적 보도로부터 3개년 매출액/영업이익/당기순이익 실적 데이터를 보완하여 채웁니다.
* **Layer 3: 공공데이터 보강 (비상장사 전용)**:
  - DART 공시 의무가 없는 비상장/소규모 법인은 공공데이터 API를 통해 **국민연금 사업장 가입자 추이**(인원 증감) 및 **사업자등록 상태**(휴폐업)를 활용해 성장 시그널을 보강합니다.
