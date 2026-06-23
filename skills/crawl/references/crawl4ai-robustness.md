# crawl4ai 견고성 레퍼런스 — 안 되는 사이트를 되게

봇 차단·동적 로딩·Web Component·로그인·지역 게이트로 막힌 사이트를 미러링할 때 본다.
코어(CLI·발견/추출·deep-crawl·seeding·마크다운·캡처)는 `crawl4ai-api.md`. 전체는 공식 문서(https://docs.crawl4ai.com).

## 목차
- 동적·lazy·무한스크롤 로딩
- Shadow DOM · iframe · 동의 팝업
- 봇 차단 우회 (단계적 에스컬레이션)
- 지역·언어 위장
- 성능·경량 크롤
- 다중 URL·동시성·rate limit

## 동적·lazy·무한스크롤 로딩

JS 실행 순서(고정): `goto → js_code_before_wait → wait_for → delay_before_return_html → js_code → flatten_shadow_dom → content`.
로딩을 **트리거하고 기다려야** 하면 `js_code_before_wait`로 트리거 + `wait_for`로 대기(`js_code`는 wait_for 이후라 늦음).

- `wait_for="css:.sel"`(출현) 또는 `"js:() => 조건"`(폴링). `nth-child(N)`으로 N개 이상 로드 보장
- `wait_until="domcontentloaded"`(기본)|`"networkidle"`|`"load"`. `page_timeout=60000`(ms), `delay_before_return_html=0.1`(초)
- lazy 이미지/콘텐츠(append형 무한스크롤): `scan_full_page=True` + `scroll_delay=0.5` + `wait_for_images=True` → `result.media["images"]`. 무거우니 `max_scroll_steps`로 상한. ⚠ cache 켜지면 새 이미지 fetch 스킵 → `CacheMode.BYPASS`. placeholder→실이미지는 `wait_for="css:img.loaded"`
- 교체형 가상 스크롤(트위터/인스타): `from crawl4ai import VirtualScrollConfig` → `CrawlerRunConfig(virtual_scroll_config=VirtualScrollConfig(container_selector=필수, scroll_count=10, scroll_by="container_height"|"page_height"|px, wait_after_scroll=0.5))`
- 동적 페이지네이션(같은 탭 multi-step): `session_id="s"` 유지, 첫 호출 뒤 `js_code=<다음버튼 클릭>` + `js_only=True`(재내비 없이 JS만), `wait_for`로 새 콘텐츠 대기. 끝나면 `await c.crawler_strategy.kill_session(session_id)`. `cache_mode=CacheMode.BYPASS`
- JS 없이 인터랙션: `c4a_script`(C4A DSL → JS 컴파일)

## Shadow DOM · iframe · 동의 팝업

본문이 비어 나오는 흔한 원인 3종.
- **Shadow DOM**(Web Component 빈 결과): `flatten_shadow_dom=True`(shadow tree 평탄화·`<slot>` 해석·closed root 강제 오픈). Stencil/Lit/Shoelace 필수. **실측 1KB→33KB**. hydration 대기: `wait_until="load"` + `delay_before_return_html=2~5`
- iframe 병합: `process_iframes=True`
- 팝업: `remove_overlay_elements=True`, `remove_consent_popups=True`(OneTrust/Cookiebot/TrustArc)

## 봇 차단 우회 (단계적 에스컬레이션)

regular+stealth → 차단 시 undetected → 여전히 차단 시 둘 결합.

**1단계 — stealth(가볍게)**: `BrowserConfig(enable_stealth=True)`(playwright-stealth로 `navigator.webdriver` 제거·fingerprint 변조) + `CrawlerRunConfig(magic=True, simulate_user=True, override_navigator=True)`. 안티봇 사이트는 `wait_until="load"`(기본 `domcontentloaded`는 센서 완료 전 반환). `headless=False`가 탐지 회피에 유리. ⚠ `enable_stealth`는 `browser_mode="builtin"`과 병용 불가.
- UA 랜덤: `BrowserConfig(user_agent_mode="random", user_agent_generator_config={...})`

**로그인 세션 보존**: `use_persistent_context=True`(자동 managed) + `user_data_dir="..."`(쿠키/로컬스토리지 영속). 또는 `storage_state=dict|"파일.json"`(`{cookies:[...], origins:[{origin, localStorage:[...]}]}`), `cookies=[{name,value,url}]` 사전 주입. 프로필 생성: CLI `crwl profiles` 또는 `from crawl4ai import BrowserProfiler`(`create_profile`/`list_profiles`/`delete_profile`·반환 경로를 `user_data_dir`로). config는 `wait_for="css:.logged-in"`으로 로그인 확인.

**managed/CDP**(기존 브라우저 세션 재사용): `use_managed_browser=True` + `cdp_url="ws://localhost:9222/..."` 또는 `debugging_port=9222`. `browser_mode`: `dedicated`(기본·매번 새)|`builtin`(백그라운드 CDP 재사용)|`custom`|`docker`.

**재시도/프록시/폴백**: `CrawlerRunConfig(max_retries=N`(차단 감지 시 라운드·매 라운드 모든 프록시 시도)`, proxy_config=list[ProxyConfig]`(순차 시도, `ProxyConfig.DIRECT`로 '프록시 없이 먼저')`, fallback_fetch_function=async(url)->html`(최후)`)`. `ignore_https_errors=True`(기본)로 자체서명 인증서 통과.
- 프록시: `BrowserConfig.proxy_config=ProxyConfig|dict({server,username,password})`. `ProxyConfig.from_string("ip:port:user:pass"`등 5형식`)` / `from_env()`. `proxy_rotation_strategy=RoundRobinProxyStrategy(proxies)`(요청 i → `proxies[i % len]`)

**2단계 — undetected(최강)**: `from crawl4ai import UndetectedAdapter, PlaywrightAdapter`; `from crawl4ai.async_crawler_strategy import AsyncPlaywrightCrawlerStrategy`. `strategy=AsyncPlaywrightCrawlerStrategy(browser_config=cfg, browser_adapter=UndetectedAdapter())` → `AsyncWebCrawler(crawler_strategy=strategy, config=cfg)`. 기본 어댑터는 `PlaywrightAdapter()`. 사이트별 선택: `UndetectedAdapter() if is_protected(url) else PlaywrightAdapter()`(성능 손실 최소화).

## 지역·언어 위장 (지역 게이트 우회)

`CrawlerRunConfig(locale="fr-FR"`(언어·날짜·숫자 포맷)`, timezone_id="Europe/Paris"`(JS Date)`, geolocation=GeolocationConfig(latitude=, longitude=, accuracy=)`(`from crawl4ai import GeolocationConfig`; 위치 권한 자동 부여)`)`. 세 값을 일관되게 맞춰야 완전한 위치 프로필. managed browser와 조합 가능.

## 성능·경량 크롤

- `BrowserConfig`: `text_mode=True`(이미지 끔·텍스트 전용 가속), `avoid_ads=True`(GA/DoubleClick/Facebook/Hotjar 등 트래커 도메인 차단), `avoid_css=True`(.css/.less/.scss 차단), `light_mode=True`(백그라운드 기능 끔), `extra_args=["--disable-extensions"]`(브라우저 플래그 직접), `device_scale_factor=2.0`(Retina 스크린샷)
- 스크래퍼: 기본 `LXMLWebScrapingStrategy`(>100KB 문서에서 BS4 대비 10-20x). 커스텀은 `ContentScrapingStrategy` 상속

## 다중 URL·동시성·rate limit

- `arun_many(urls, config, dispatcher)`. 기본 `MemoryAdaptiveDispatcher`(`from crawl4ai.async_dispatcher import ...`): `memory_threshold_percent=90`(초과 시 일시정지), `max_session_permit=10`(최대 동시), `memory_wait_timeout=600`(초과 지속 시 `MemoryError`), `check_interval=1`. `SemaphoreDispatcher`(고정 동시성).
- `stream=True`(run config) → async generator: `async for r in await c.arun_many(...)`(완료순). `result.dispatch_result`(task_id, memory_usage, peak_memory, start/end_time)
- `RateLimiter`(`from crawl4ai`): `base_delay=(1.0,3.0)`(요청 간 랜덤 지연), `max_delay=60`(백오프 상한), `max_retries=3`, `rate_limit_codes=[429,503]`. dispatcher에 `rate_limiter=`로 주입
- 진행 모니터: `CrawlerMonitor(max_visible_rows=15, display_mode=DisplayMode.DETAILED|AGGREGATED)`
- **URL별 config 라우팅**: `arun_many(config=[CrawlerRunConfig(url_matcher=...), ...])`. `url_matcher`=glob(`"*.pdf"`)·람다(`lambda u: 'api' in u`)·리스트+`match_mode=MatchMode.OR|AND`(`from crawl4ai import MatchMode`). ⚠ `url_matcher` 없는 fallback config를 **마지막**에 둘 것(없으면 미매칭 URL "No matching configuration found"로 실패). 순서대로 평가·구체 패턴 먼저. `config.is_match(url)`로 테스트
- robots: `check_robots_txt=True`(SQLite 캐시 `~/.crawl4ai/robots/`, TTL 7일, fail-open). 차단 시 `success=False` + `status_code==403` → 빈 파일 저장 회피
- 헤더: `arun(url, headers={...})` 또는 `CrawlerRunConfig(headers=...)`. UA 갱신 `crawler.crawler_strategy.update_user_agent("UA/1.0")`
