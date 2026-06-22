# crawl4ai / crwl 레퍼런스 (작업 관점 큐레이션)

`crwl` CLI와 crawl4ai Python API에서 이 스킬 작업(웹/문서 → 마크다운 미러)에 필요한 핵심 + 실측 함정만 추린다.
전체 API·옵션은 `crwl crawl --help`와 공식 문서(https://docs.crawl4ai.com)가 권위 소스 — 여기엔 작업 패턴·함정·정확한 파라미터명만 둔다. LLM 추출·임베딩 등 범위 밖은 맨 끝에 존재만 기록.

## 목차
- crwl CLI 핵심 패턴
- Python API 골격
- 발견 vs 추출 분리 (가장 중요)
- deep-crawl (BFS/DFS/BestFirst · prefetch · 필터)
- URL seeding / sitemap / DomainMapper
- 동적·lazy·무한스크롤 로딩
- 봇 차단 우회
- 보일러플레이트 · Shadow DOM · iframe 정리
- 마크다운 생성 제어
- 캡처 · 다운로드 · 로컬 입력 (PDF/스크린샷/raw)
- 다중 URL · 동시성
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
| `-c "k=v,…"` / `-C crawler.yml` | 크롤러(cache_mode, scan_full_page, magic, word_count_threshold, page_timeout, wait_for) |
| `--deep-crawl bfs` `--max-pages N` | deep-crawl(bfs/dfs/best-first). URL 범위 제한은 `-C` config로만 |
| `-e cfg.yml -s schema.json` | 구조화 추출(json-css 또는 llm) |
| `-f filter.yml` | content filter(`type: bm25\|pruning`) → `-o md-fit` |
| `-q "질문"` | 크롤 내용에 LLM Q&A |
| `--bypass-cache` `-v` | 캐시 우회 / verbose |
| `crwl profiles` | 로그인 프로필 대화형 생성(Create→로그인→q 저장) |

설치/진단: `crawl4ai-setup`(브라우저 설치), `crawl4ai-doctor`(환경 점검). 예시 `crwl --example`, 전체 `crwl crawl --help`.

## Python API 골격 (스크립트 작성용)

```python
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
async with AsyncWebCrawler(config=BrowserConfig(headless=True)) as c:
    r = await c.arun(url, config=CrawlerRunConfig(...))       # 단일
    results = await c.arun_many(urls, config=cfg)             # 다중(MemoryAdaptiveDispatcher 자동)
# r.markdown.raw_markdown / r.markdown.fit_markdown / r.links['internal'] / r.media['images']
# r.success / r.status_code / r.redirected_url / r.downloaded_files / r.tables
```

`arun`은 `stream=False`(기본)면 deep-crawl 전체 완료 후 리스트, `stream=True`면 `async for r in await c.arun(...)`로 도착순.
**전략(deep_crawl·scraping·markdown_generator·extraction)은 `arun()`이 아니라 `CrawlerRunConfig`에 넣는다**(구버전 API 함정).

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
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy  # DFSDeepCrawlStrategy, BestFirstCrawlingStrategy도
from crawl4ai.deep_crawling.filters import FilterChain, URLPatternFilter  # ContentTypeFilter, DomainFilter, SEOFilter
strat = BFSDeepCrawlStrategy(max_depth=6, max_pages=120,
    filter_chain=FilterChain([URLPatternFilter(patterns=["*host/docs/*"])]))
cfg = CrawlerRunConfig(deep_crawl_strategy=strat, target_elements=[".devsite-article-body", "#content-area", "main", "article"])
```

- 전략: BFS / DFS / `BestFirstCrawlingStrategy(url_scorer=KeywordRelevanceScorer(keywords, weight))`(점수순 처리·`stream=True` 권장)
- 파라미터: `max_depth`, `max_pages`(하드캡 — depth>3 폭증 주의), `score_threshold`, `include_external=False`. `result.metadata['depth']/['score']`
- 필터(`crawl4ai.deep_crawling.filters`): `URLPatternFilter`, `ContentTypeFilter(["text/html"])`, `DomainFilter(allowed_domains, blocked_domains)`, `SEOFilter`. `FilterChain([...])`로 결합
- 따라갈 링크 선별은 셀렉터가 아니라 이 필터/스코어로 (위 표)
- **prefetch 2단계**(대규모 미러 계획): `prefetch=True`면 markdown/scraping/media 전부 스킵, HTML+링크만(페이지당 ~200-500ms, 풀 파이프라인 대비 5-10x). Phase1 prefetch로 `result.links['internal']` 수집 → 패턴 필터 → Phase2 일반 config로 선별 arun
- 한계: nav 안 링크만 따라가므로 orphan은 못 봄 → seeding으로 우회

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
- `live_check=True`(HEAD로 접근성 검증 → `u['status']` valid/not_valid), `filter_nonsense_urls=True`(robots/sitemap/미디어/admin 자동 제외), `extract_head`(메타 사전필터), `concurrency`/`hits_per_sec`(레이트)
- 여러 도메인: `seeder.many_urls(domains)` → `{domain: [urls]}`
- 더 강하게: `crawler.amap_domain(domain, DomainMapperConfig(source="sitemap+cc+crt+probe", soft_404_detection=True))` — 8소스(sitemap/cc/wayback/crt/probe/robots/feed/homepage) 결합. `soft_404_detection`은 SPA가 모든 URL에 200 반환하는 함정 검출

## 동적·lazy·무한스크롤 로딩

JS 실행 순서(고정): `goto → js_code_before_wait → wait_for → delay_before_return_html → js_code → flatten_shadow_dom → content`.
로딩을 **트리거하고 기다려야** 하면 `js_code_before_wait`로 트리거 + `wait_for`로 대기(`js_code`는 wait_for 이후라 늦음).

- `wait_for="css:.sel"`(출현 대기) 또는 `"js:() => 조건"`(폴링). `nth-child(30)`으로 N개 이상 로드 보장 트릭
- `wait_until="domcontentloaded"`(기본) | `"networkidle"` | `"load"`. `page_timeout=60000`(ms), `delay_before_return_html=0.1`(초)
- lazy 이미지/콘텐츠(append형 무한스크롤): `scan_full_page=True` + `scroll_delay=0.2` + `wait_for_images=True`. 무거우니 `max_scroll_steps`로 상한
- 교체형 가상 스크롤(Twitter/Instagram): `from crawl4ai import VirtualScrollConfig` → `CrawlerRunConfig(virtual_scroll_config=VirtualScrollConfig(container_selector=필수, scroll_count=10, scroll_by="container_height"|"page_height"|px, wait_after_scroll=0.5))`
- 동적 페이지네이션(같은 탭 multi-step): `session_id="s"` 유지, 첫 호출 뒤 `js_code=<다음버튼 클릭>` + `js_only=True`(재내비 없이 JS만), `wait_for`로 새 콘텐츠 대기. 끝나면 `await c.crawler_strategy.kill_session(session_id)`. `cache_mode=CacheMode.BYPASS`
- JS 없이 인터랙션: `c4a_script`(C4A DSL → JS 컴파일)

## 봇 차단 우회

1순위(가볍게): `BrowserConfig(enable_stealth=True)`(playwright-stealth로 `navigator.webdriver` 제거·fingerprint 변조) + `CrawlerRunConfig(magic=True, simulate_user=True, override_navigator=True)`. 안티봇 사이트는 `wait_until="load"`(기본 `domcontentloaded`는 센서 완료 전 반환).

- UA 랜덤: `BrowserConfig(user_agent_mode="random")`. `avoid_ads=True`(GA/DoubleClick/Hotjar 등 트래커 차단), `text_mode=True`(이미지 끔·가속)
- 로그인 세션 보존: `use_persistent_context=True` + `user_data_dir="..."`(쿠키/로컬스토리지 런간 유지·자동 managed). 또는 `storage_state=dict|"파일.json"`(`{cookies:[...], origins:[{origin, localStorage:[...]}]}`). 프로필은 CLI `crwl profiles`
- 재시도/폴백: `CrawlerRunConfig(max_retries=N`(차단 감지 시 라운드)`, proxy_config=list[ProxyConfig]`(라운드마다 순차 시도, `ProxyConfig.DIRECT`로 '프록시 없이 먼저')`, fallback_fetch_function=async(url)->html`(최후)`)`
- 프록시: `ProxyConfig.from_string("ip:port:user:pass"`등 5형식`)` / `from_env()`. `proxy_rotation_strategy=RoundRobinProxyStrategy(proxies)`(arun_many에서 요청 i가 `proxies[i % len]`)
- 최강: `from crawl4ai import UndetectedAdapter` → `AsyncPlaywrightCrawlerStrategy(browser_adapter=UndetectedAdapter())`. ⚠ `enable_stealth`는 `browser_mode="builtin"`과 병용 불가

## 보일러플레이트 · Shadow DOM · iframe 정리

사이트별 CSS 셀렉터 대신 휴리스틱·평탄화로.

```python
from crawl4ai import DefaultMarkdownGenerator
from crawl4ai.content_filter_strategy import PruningContentFilter  # BM25ContentFilter도
cfg = CrawlerRunConfig(markdown_generator=DefaultMarkdownGenerator(
    content_filter=PruningContentFilter(threshold=0.48, threshold_type="dynamic")))
# → r.markdown.fit_markdown (raw_markdown은 항상 함께 보존)
```

- `PruningContentFilter`: 텍스트/링크 밀도 + "nav/footer" 패턴 휴리스틱 → 쿼리 없이 구조 무관. `BM25ContentFilter(user_query=...)`는 특정 주제일 때만. 과공격적이면 footer/sidebar 핵심 손실 → threshold↓ 또는 raw 폴백
- **Shadow DOM**(Web Component 빈 결과 함정): `flatten_shadow_dom=True`(shadow tree 평탄화·`<slot>` 해석·closed root 강제 오픈). Stencil/Lit/Shoelace 필수. **실측 1KB→33KB**. hydration 대기: `wait_until="load"` + `delay_before_return_html=2~5`
- iframe 병합: `process_iframes=True`. 팝업: `remove_overlay_elements=True`, `remove_consent_popups=True`(OneTrust/Cookiebot)
- 추가 정리: `remove_forms=True`, `keep_data_attributes=False`, `word_count_threshold`, `exclude_external_links`, `only_text`

## 마크다운 생성 제어

```python
DefaultMarkdownGenerator(
    options={"ignore_links": False, "ignore_images": False, "body_width": 0,  # 0=무줄바꿈
             "skip_internal_links": True, "citations": True},
    content_source="cleaned_html")  # "raw_html"(정리 전 원본·콘텐츠 보존) | "fit_html"
```

- `content_source="raw_html"`: 정리가 본문을 지울 때 복구
- `citations=True` → `result.markdown.markdown_with_citations` + `references_markdown`

## 캡처 · 다운로드 · 로컬 입력

- 스크린샷/PDF/MHTML: `CrawlerRunConfig(screenshot=True`→`result.screenshot`[base64, **b64decode 후** 저장]`, pdf=True`→`result.pdf`[**bytes 그대로 write — 디코딩 X, 함정**]`, capture_mhtml=True`→`result.mhtml`[CSS/이미지 포함 단일파일]`)`. 긴 페이지는 pdf가 풀페이지 스크린샷보다 안정. `wait_for_images=True`
- 파일 다운로드(zip/PDF 첨부): `BrowserConfig(accept_downloads=True, downloads_path=...)` → `result.downloaded_files`. 보통 클릭 트리거(`js_code` + `wait_for`)
- 네트워크 없이 처리: `url="raw://<html_string>"`(메모리 HTML 직접) / `file://`(로컬 파일)
- PDF 미러: `from crawl4ai.processors.pdf import PDFCrawlerStrategy, PDFContentScrapingStrategy` (crawler_strategy + scraping_strategy)
- 디버그: `capture_network_requests=True`→`result.network_requests`(숨은 API 발견), `capture_console_messages=True`, `fetch_ssl_certificate=True`

## 다중 URL · 동시성

- `arun_many(urls, config, dispatcher)`: 기본 `MemoryAdaptiveDispatcher(memory_threshold_percent=70, max_session_permit=10)`(메모리 기반 자동조절). `SemaphoreDispatcher`(고정 동시성). `stream=True`면 async generator
- `RateLimiter`(서버 보호·백오프), `check_robots_txt=True`(robots 준수)
- URL별 다른 설정: `url_matcher` + `MatchMode`
- `CacheMode`: `ENABLED` / `BYPASS` / `READ_ONLY` / `WRITE_ONLY` / `DISABLED`
- hooks 8단계(`set_hook` 또는 0.9.0 declarative): on_browser_created/on_page_context_created/before_goto/after_goto/… — 인증 주입·리소스 차단 위치

## 실측 함정
- `crwl crawl` 기본 출력은 마크다운 아님 → `-o md` 필수(`crawl-mirror.py`는 자체 처리)
- `css_selector`를 deep-crawl에 넘기면 발견 붕괴(24 vs 118) → 본문 한정은 `target_elements`
- `excluded_tags=["nav"]`도 발견 막음 — target_elements 밖은 추출에서 어차피 빠짐
- deep-crawl `for r in await arun(...)`(stream=False)는 전체 완료 후 일괄 → 점진은 `stream=True` + `async for`
- Web Component 사이트 빈 결과 → `flatten_shadow_dom=True` + hydration 대기
- `pdf=True`는 bytes 직접 저장(스크린샷 base64와 디코딩 방식 다름)
- SPA가 모든 URL 200 반환 → `DomainMapper(soft_404_detection=True)`
- `enable_stealth`는 `browser_mode="builtin"`과 병용 불가
- 동적 콘텐츠가 빈 결과 → js 실행 순서(트리거는 `js_code_before_wait`, `js_code`는 wait_for 이후)

## 범위 밖 (존재만 — 필요 시 공식 문서)

이 스킬(크롤→마크다운 미러) 밖이지만 crawl4ai에 있음: LLM 추출(`LLMExtractionStrategy`/`LLMContentFilter`/`LLMConfig`), CSS·XPath 구조화 추출(`JsonCssExtractionStrategy`), 정규식 추출(`RegexExtractionStrategy`, 이메일/전화/URL), 임베딩·클러스터링(`CosineStrategy`), 청킹(RAG용), 적응형 크롤(`AdaptiveCrawler.digest` — 쿼리 충분성 정지). `torch`/transformer extra 설치 필요한 것들.
