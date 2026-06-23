# crawl4ai / crwl 코어 레퍼런스 (작업 관점 큐레이션)

크롤 메커니즘의 핵심 + 실측 함정. **봇 차단·동적/무한스크롤 로딩·Shadow DOM·세션·프록시·지역위장·동시성은 `crawl4ai-robustness.md`**.
전체 API·옵션은 `crwl crawl --help`와 공식 문서(https://docs.crawl4ai.com)가 권위 소스 — 여기엔 작업 패턴·함정·정확한 파라미터명만 둔다. LLM 추출·임베딩 등 범위 밖은 맨 끝에 존재만 기록.

## 목차
- crwl CLI 핵심 패턴
- Python API 골격
- 발견 vs 추출 분리 (가장 중요)
- deep-crawl (전략·필터·prefetch·상태재개)
- URL seeding / sitemap / DomainMapper
- 보일러플레이트 제거 (fit_markdown)
- 마크다운 생성 제어
- 캡처·다운로드·로컬 입력
- 콘텐츠·링크·미디어 정제
- 실측 함정
- 범위 밖 (존재만)

## crwl CLI 핵심 패턴

`crwl <url> [옵션]`. 기본 출력은 마크다운이 **아니다** — `-o`로 명시.

| 옵션 | 용도 |
|---|---|
| `-o md` / `md-fit` | 마크다운 / content filter 적용된 본문 마크다운 |
| `-o json` / `all` | 구조화 추출 데이터 / 전체(메타 포함) |
| `-O f.md` | 파일 저장(기본 stdout) |
| `-b "k=v,…"` / `-B browser.yml` | 브라우저(headless, viewport_width, user_agent_mode, enable_stealth) |
| `-c "k=v,…"` / `-C crawler.yml` | 크롤러(cache_mode, scan_full_page, magic, wait_until, page_timeout) |
| `--deep-crawl bfs` `--max-pages N` | deep-crawl(bfs/dfs/best-first). URL 범위 제한은 `-C` config로만 |
| `-e cfg.yml -s schema.json` | 구조화 추출(json-css 또는 llm) |
| `-f filter.yml` | content filter(`type: bm25\|pruning`) → `-o md-fit` |
| `-q "질문"` | 크롤 내용에 LLM Q&A |
| `--bypass-cache` `-v` | 캐시 우회 / verbose |
| `crwl profiles` | 로그인 프로필 대화형 생성 |

설치/진단: `crawl4ai-setup`(브라우저 설치), `crawl4ai-doctor`(환경 점검). 예시 `crwl --example`, 전체 `crwl crawl --help`.

## Python API 골격 (스크립트 작성용)

```python
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
async with AsyncWebCrawler(config=BrowserConfig(headless=True)) as c:
    r = await c.arun(url, config=CrawlerRunConfig(...))       # 단일
    results = await c.arun_many(urls, config=cfg)             # 다중(동시성은 robustness.md)
# r.markdown.raw_markdown / r.markdown.fit_markdown / r.links['internal'] / r.media['images']
# r.success / r.status_code / r.redirected_url / r.downloaded_files / r.tables
```

`arun`은 `stream=False`(기본)면 deep-crawl 전체 완료 후 리스트, `stream=True`면 `async for r in await c.arun(...)`로 도착순.
**전략(deep_crawl·scraping·markdown_generator·extraction)은 `arun()`이 아니라 `CrawlerRunConfig`에 넣는다**(구버전 API 함정). `CacheMode`: `ENABLED`/`BYPASS`/`READ_ONLY`/`WRITE_ONLY`/`DISABLED`.

## 발견 vs 추출 분리 (가장 중요 — 실측 교훈)

deep-crawl에서 **본문 한정은 `css_selector`가 아니라 `target_elements`로**. 발견에 미치는 영향이 정반대.

| 파라미터 | 효과 | deep-crawl 발견 |
|---|---|---|
| `css_selector="…"` | 매칭 영역만 남기고 나머지 DOM 제거 — *"Affects the entire extraction process"* | ❌ 셀렉터 밖 nav 링크 소멸 → 못 따라감 |
| `target_elements=[…]` | 마크다운·데이터 추출만 한정 — *"still processing the entire page for links"* | ✅ 발견은 전체 DOM. List[str], 미매칭 시 전체로 graceful degrade |
| `excluded_tags=["nav",…]` | 태그 통째 제거 | ❌ nav 제거 시 링크도 소멸 — deep-crawl엔 쓰지 말 것 |

**실측**(docs.crawl4ai.com, MkDocs): `css_selector='main'` 24개 vs `target_elements=['main','article']` **118개** 발견.

## deep-crawl

```python
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy  # DFSDeepCrawlStrategy, BestFirstCrawlingStrategy
from crawl4ai.deep_crawling.filters import FilterChain, URLPatternFilter  # ContentTypeFilter, DomainFilter, SEOFilter
strat = BFSDeepCrawlStrategy(max_depth=6, max_pages=120,
    filter_chain=FilterChain([URLPatternFilter(patterns=["*host/docs/*"])]))
cfg = CrawlerRunConfig(deep_crawl_strategy=strat, target_elements=[".devsite-article-body", "#content-area", "main", "article"])
```

- 전략: BFS / DFS / `BestFirstCrawlingStrategy(url_scorer=KeywordRelevanceScorer(keywords, weight))`(점수순·`stream=True` 권장)
- 파라미터: `max_depth`, `max_pages`(하드캡 — depth>3 폭증 주의), `score_threshold`, `include_external=False`. `result.metadata['depth']/['score']`
- 필터(`crawl4ai.deep_crawling.filters`): `URLPatternFilter`, `ContentTypeFilter(allowed_types=["text/html"])`, `DomainFilter(allowed_domains, blocked_domains)`, `SEOFilter`, `ContentRelevanceFilter`(BM25·범위 경계). `FilterChain([...])`로 결합. 따라갈 링크 선별은 셀렉터가 아니라 이 필터/스코어로
- **prefetch 2단계**(대규모 미러 계획): `prefetch=True`면 markdown/scraping/media 스킵, HTML+링크만(페이지당 ~200-500ms, 5-10x). Phase1 prefetch로 `result.links['internal']` 수집 → 패턴 필터 → Phase2 일반 config로 선별 arun
- **상태 저장/재개**(장시간 크래시 복구): 모든 deep 전략 `resume_state=dict`(체크포인트), `on_state_change=async콜백`(URL마다, state는 JSON 직렬화 `{visited,pending,depths,pages_crawled}`), `should_cancel=async콜백` 또는 `strategy.cancel()`. `export_state()`는 on_state_change 설정 시만
- 한계: nav 링크만 따라가므로 orphan은 못 봄 → seeding으로 우회

## URL seeding / sitemap / DomainMapper

deep-crawl이 nav를 못 보는 사이트(MkDocs 등)는 sitemap에서 URL 직접 수신.

```python
from crawl4ai import AsyncUrlSeeder, SeedingConfig
async with AsyncUrlSeeder() as seeder:
    urls = await seeder.urls("example.com",
        SeedingConfig(source="sitemap+cc", pattern="*/docs/*", max_urls=-1,
                      live_check=True, filter_nonsense_urls=True))
seed_urls = [u["url"] for u in urls if u["status"] != "not_valid"]
results = await c.arun_many(seed_urls, config=cfg)
```

- `source`: `sitemap` | `cc`(Common Crawl) | `sitemap+cc`(기본)
- `live_check=True`(HEAD로 접근성 → `u['status']` valid/not_valid), `filter_nonsense_urls=True`(robots/sitemap/미디어/admin 자동 제외), `extract_head`(메타 사전필터), `concurrency`/`hits_per_sec`(레이트)
- 여러 도메인: `seeder.many_urls(domains)` → `{domain: [urls]}`
- 더 강하게: `crawler.amap_domain(domain, DomainMapperConfig(source="sitemap+cc+crt+probe", soft_404_detection=True))` — 8소스 결합. `soft_404_detection`은 SPA가 모든 URL에 200 반환하는 함정 검출

## 보일러플레이트 제거 (fit_markdown)

사이트별 CSS 셀렉터 대신 content filter 휴리스틱. (Shadow DOM·iframe·동의팝업은 robustness.md.)

```python
from crawl4ai import DefaultMarkdownGenerator
from crawl4ai.content_filter_strategy import PruningContentFilter  # BM25ContentFilter
cfg = CrawlerRunConfig(markdown_generator=DefaultMarkdownGenerator(
    content_filter=PruningContentFilter(threshold=0.48, threshold_type="dynamic")))
# → r.markdown.fit_markdown (raw_markdown은 항상 함께 보존)
```

- `PruningContentFilter(threshold=0.48, threshold_type="fixed"`(score≥threshold)`|"dynamic"`(밀도 따라 조정)`, min_word_threshold=N)`: 텍스트/링크 밀도 + "nav/footer" 패턴 휴리스틱 → 쿼리 없이 구조 무관
- `BM25ContentFilter(user_query=, bm25_threshold=1.0, language="english", use_stemming=True)`: 특정 주제일 때만. `filter_content(html)`로 2-pass 체이닝 가능(Pruning→BM25)
- 과공격적이면 footer/sidebar 핵심 손실 → threshold↓ 또는 raw 폴백

## 마크다운 생성 제어

```python
DefaultMarkdownGenerator(
    options={"ignore_links": False, "ignore_images": False, "body_width": 0,  # 0=무줄바꿈
             "skip_internal_links": True, "citations": True},
    content_source="cleaned_html")  # "raw_html"(정리 전 원본·콘텐츠 보존) | "fit_html"
```

- `content_source="raw_html"`: 정리가 본문을 지울 때 복구
- `citations=True` → `result.markdown.markdown_with_citations` + `references_markdown`

## 캡처·다운로드·로컬 입력

- 스크린샷/PDF/MHTML: `CrawlerRunConfig(screenshot=True`→`result.screenshot`[base64, **b64decode 후** 저장]`, pdf=True`→`result.pdf`[**bytes 그대로 write — 디코딩 X, 함정**]`, capture_mhtml=True`→`result.mhtml`[CSS/이미지 포함 단일파일, utf-8 저장]`)`. `force_viewport_screenshot=True`(전체 대신 뷰포트만·빠름), `wait_for_images=True`. 긴 페이지는 pdf가 풀페이지 스크린샷보다 안정
- 파일 다운로드(zip/PDF 첨부): `BrowserConfig(accept_downloads=True, downloads_path=...)` → `result.downloaded_files`. 보통 클릭 트리거(`js_code` + `wait_for`)
- 네트워크 없이 처리: `url="raw://<html_string>"`(메모리 HTML 직접) / `file://`(로컬 파일)
- PDF 미러: `from crawl4ai.processors.pdf import PDFCrawlerStrategy, PDFContentScrapingStrategy`. `AsyncWebCrawler(crawler_strategy=PDFCrawlerStrategy())` + `CrawlerRunConfig(scraping_strategy=PDFContentScrapingStrategy(extract_images=False, save_images_locally=False, image_save_dir=None, batch_size=4))`. 원격 PDF 자동 다운로드. ⚠ 스캔(이미지) PDF는 OCR 미포함이라 텍스트 안 나옴
- 디버그: `capture_network_requests=True`→`result.network_requests`(숨은 API 발견), `capture_console_messages=True`, `fetch_ssl_certificate=True`

## 콘텐츠·링크·미디어 정제

- 본문: `excluded_tags=["nav","footer"]`, `excluded_selector="#ads, .tracker"`, `remove_forms=True`, `keep_attrs=[...]`, `word_count_threshold`(기본 ~200 — 짧은 본문 누락 시 낮춤)
- 링크: `exclude_external_links`, `exclude_internal_links`, `exclude_social_media_links`, `exclude_domains=[...]`, `score_links=True`(URL구조·텍스트 품질 점수), `preserve_https_for_internal_links`
- 이미지: `exclude_all_images=True`(파이프라인 초기 제거·메모리↑), `exclude_external_images=True`, `image_score_threshold`, `save_images_locally=True` + `image_save_dir`
- 테이블(LLM 없이): `result.tables=[{headers, rows, caption, summary}]`. `table_score_threshold=7`(기본; 낮추면 더 탐지, 레이아웃 테이블은 제외)

## 실측 함정
- `crwl crawl` 기본 출력은 마크다운 아님 → `-o md` 필수(`crawl-mirror.py`는 자체 처리)
- `css_selector`를 deep-crawl에 넘기면 발견 붕괴(24 vs 118) → 본문 한정은 `target_elements`
- `excluded_tags=["nav"]`도 발견 막음 — target_elements 밖은 추출에서 어차피 빠짐
- deep-crawl `for r in await arun(...)`(stream=False)는 전체 완료 후 일괄 → 점진은 `stream=True` + `async for`
- `pdf=True`는 bytes 직접 저장(스크린샷 base64와 디코딩 방식 다름)
- SPA가 모든 URL 200 반환 → `DomainMapper(soft_404_detection=True)`
- 기본 스크래퍼는 `LXMLWebScrapingStrategy`(>100KB에서 BS4 대비 10-20x)

## 범위 밖 (존재만 — 필요 시 공식 문서)

이 스킬(크롤→마크다운 미러) 밖이지만 crawl4ai에 있음: LLM 추출(`LLMExtractionStrategy`/`LLMContentFilter`/`LLMConfig`), CSS·XPath 구조화 추출(`JsonCssExtractionStrategy`), 정규식 추출(`RegexExtractionStrategy`, 이메일/전화/URL), 임베딩·클러스터링(`CosineStrategy`), 청킹(RAG용), 적응형 크롤(`AdaptiveCrawler.digest` + `AdaptiveConfig` — 쿼리 충분성 정지·`statistical`은 무료지만 페이지별 전체 미러와 목적 불일치). `torch`/transformer extra 필요한 것들.
