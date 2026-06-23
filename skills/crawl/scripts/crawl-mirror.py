#!/usr/bin/env -S uv run --with crawl4ai --quiet python
"""단일 페이지(--single) 또는 문서 섹션 전체(deep-crawl)를 크롤해 URL 경로에 대응하는 .md로 저장.

URL `https://host/a/b` -> `<out>/host/a/b.md` (URL 경로 = 파일 경로).
crwl CLI(`crwl -O`)는 전체를 한 파일에 `# <URL>` 구분선으로 이어 붙이지만, 이 스크립트는
페이지별 파일로 미러링한다. 문서 사이트(특히 Google devsite)에서 겪은 함정을 기본값에 박아둠:

- 로케일 폭발: devsite 페이지는 footer에 `?hl=<lang>` 링크가 있어 deep-crawl이 ~20배로 불어난다.
  -> 기본으로 `*hl=*` 링크를 따라가지 않고(--block), 언어는 Accept-Language(--lang)로 고정한다.
- 발견과 추출 분리(핵심): css_selector는 "entire extraction process"에 영향 -> 셀렉터 밖 nav 링크가 잘려
  deep-crawl이 못 따라간다(실측: docs.crawl4ai.com css_selector='main' 24개 vs target_elements 118개).
  target_elements는 추출만 본문에 한정하고 링크 발견은 전체 DOM 유지, 미매칭 시 전체로 graceful degrade.
- 보일러플레이트 제거 + 이미지 보존: target_elements로 본문 위주 추출 -> 전체 크롤이면 cross-page 반복 제거
  (3장 이상 페이지에 공통으로 나오는 줄 = nav/footer/사이드바, 이미지 줄은 페이지 고유라 보존, --boiler-threshold)
  -> strip_chrome. excluded_tags로 nav를 지우면 그 안 링크까지 사라져 발견이 막히므로 안 쓴다.
  Pruning(fit_markdown)은 이미지를 죽이므로 안 쓰고 raw_markdown을 쓴다(실측).
- 끊긴/오타 링크(404): deep-crawl에 스퓨리어스 URL이 섞인다. -> 본문 길이 게이트(--min-len)로 버린다.
- Mintlify 크롬: 헤딩이 `## `+제로폭 앵커+텍스트 3줄로 쪼개지고, `Copy page`/`Was this page helpful?` 푸터/eyebrow가 박힌다.
  -> 저장 전 strip_chrome()으로 재결합/제거(패턴 없으면 no-op이라 사이트 무관).
- 이미지: raw_markdown은 원격 URL 참조만 남긴다. 로컬 보존(상대경로 치환)은 --assets로 페이지 옆 <page>.assets/에 받는다.

사용:
  # 전체 크롤(섹션): --pattern이 따라갈 URL 범위
  crawl-mirror.py https://host/docs --pattern "*host/docs*" --lang en --assets
  # 단일 페이지
  crawl-mirror.py https://host/docs/page --single --assets
전체 옵션: --help
"""
import argparse
import asyncio
import hashlib
import os
import re
import urllib.request
from collections import Counter
from urllib.parse import urlsplit

from crawl4ai import AsyncWebCrawler, BrowserConfig, CacheMode, CrawlerRunConfig
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy
from crawl4ai.deep_crawling.filters import FilterChain, URLPatternFilter

# Mintlify 마크다운 크롬 제거 — 패턴이 없으면 no-op이라 어떤 사이트에도 안전.
_ZW = "​"  # Mintlify가 헤딩 앵커 링크 텍스트로 넣는 제로폭 공백
_H_ANCHOR = re.compile(r"^(#{1,6})[ \t]*\n\[" + _ZW + r"\]\([^)]*\)\n(.+)$", re.M)  # 3줄로 쪼개진 헤딩 재결합
_ZW_LINK = re.compile(r"\[" + _ZW + r"\]\([^)]*\)")  # 헤딩 외 제로폭 앵커 링크
_COPY = re.compile(r"^Copy page$", re.M)  # 복사 버튼
_FOOTER = re.compile(r"\n*Was this page helpful\?.*\Z", re.S)  # Mintlify 피드백 위젯 + 이전/다음 nav (본문 맨 끝)
_EYEBROW = re.compile(r"\A[^\n#][^\n]*\n+(?=# )")  # 제목 위 카테고리 eyebrow (첫 H1 앞 비헤딩 한 줄)


def strip_chrome(md):
    md = _H_ANCHOR.sub(r"\1 \2", md)
    md = _ZW_LINK.sub("", md)
    md = _COPY.sub("", md)
    md = _FOOTER.sub("", md)
    md = _EYEBROW.sub("", md)
    return re.sub(r"\n{3,}", "\n\n", md)


def dest(out, url):
    sp = urlsplit(url)
    rel = f"{sp.netloc}/{sp.path.strip('/')}" if sp.path.strip("/") else sp.netloc
    return os.path.join(out, rel + ".md"), f"{sp.scheme}://{sp.netloc}{sp.path}"


_IMG = re.compile(r"(!\[[^\]]*\]\()(https?://[^)\s]+)(\))")  # 원격 이미지 참조만


def fetch_assets(md, fp):
    """원격 이미지를 페이지 옆 <page>.assets/로 받아 상대경로로 치환. 실패 시 원격 URL 유지."""
    adir = fp[:-3] + ".assets"  # foo.md → foo.assets/
    rel = os.path.basename(adir)

    def repl(m):
        url = m.group(2)
        h = hashlib.md5(url.encode()).hexdigest()[:6]  # url당 고유 → 파일명 충돌 방지 + 재실행 캐시
        name = f"{h}-{os.path.basename(urlsplit(url).path) or 'img'}"
        dst = os.path.join(adir, name)
        try:
            if not os.path.exists(dst):
                os.makedirs(adir, exist_ok=True)
                # CDN(mintcdn 등)은 기본 UA를 차단 → 브라우저 UA. timeout 30s: 큰 이미지 여유
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=30) as r, open(dst, "wb") as f:
                    f.write(r.read())
            return f"{m.group(1)}{rel}/{name}{m.group(3)}"
        except Exception:
            return m.group(0)  # solve-don't-punt: 다운로드 실패해도 원격 참조는 살린다

    return _IMG.sub(repl, md)


def find_boilerplate(mds, threshold):
    """여러 페이지에 반복되는 줄(nav/footer/사이드바)을 식별. 이미지 줄(![)은 페이지 고유라 제외해 보존.
    셀렉터로 본문을 추측하는 대신, 전체로 받은 뒤 '모든 페이지에 같은 줄=보일러플레이트'로 후처리 제거한다."""
    mds = list(mds)
    n = len(mds)
    cnt = Counter()
    for md in mds:
        for line in {x.strip() for x in md.split("\n") if x.strip()}:
            cnt[line] += 1
    return {line for line, c in cnt.items() if c >= n * threshold and not line.lstrip().startswith("![")}


def strip_boilerplate(md, boiler):
    out = "\n".join(line for line in md.split("\n") if line.strip() not in boiler)
    return re.sub(r"\n{3,}", "\n\n", out)


def save(out, url, md, assets=False):
    fp, clean = dest(out, url)
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    body = strip_chrome(md).strip()
    if assets:
        body = fetch_assets(body, fp)
    with open(fp, "w", encoding="utf-8") as f:
        f.write(f"<!-- source: {clean} -->\n\n{body}\n")


async def main(a):
    headers = {"Accept-Language": f"{a.lang},{a.lang};q=0.9"} if a.lang else {}
    bc = BrowserConfig(headless=True, headers=headers)
    # target_elements: 마크다운 추출만 본문 컨테이너로 한정하되 링크 발견은 전체 DOM에서 유지한다.
    # css_selector는 "entire extraction process"에 영향 -> 셀렉터 밖 nav 링크가 잘려 deep-crawl이 못 따라간다
    # (실측: docs.crawl4ai.com css_selector='main' 24개 vs target_elements 118개 발견). 미매칭 시 전체로 graceful degrade.

    # 1) 수집: --single이면 시드 1장, 아니면 deep-crawl 전체
    pages, spurious = {}, []
    async with AsyncWebCrawler(config=bc) as c:
        if a.single:
            run = CrawlerRunConfig(target_elements=a.selector, cache_mode=CacheMode.BYPASS)
            results = [await c.arun(a.seed, config=run)]
        else:
            filters = [URLPatternFilter(patterns=a.pattern)]
            if a.block:
                filters.append(URLPatternFilter(patterns=a.block, reverse=True))
            strat = BFSDeepCrawlStrategy(
                max_depth=a.max_depth, max_pages=a.max_pages, filter_chain=FilterChain(filters)
            )
            run = CrawlerRunConfig(
                target_elements=a.selector, cache_mode=CacheMode.BYPASS, deep_crawl_strategy=strat
            )
            results = await c.arun(a.seed, config=run)
        for r in results:
            if not r.success:
                continue
            md = (r.markdown.raw_markdown or "").strip()
            if len(md) >= a.min_len:
                pages[r.url] = md
            else:
                spurious.append(r.url)

    # 2) cross-page 정제: 3장 이상에서 반복되는 줄(nav/footer/사이드바)을 제거, 이미지 줄은 보존.
    #    셀렉터로 본문을 추측하는 대신 '모든 페이지 공통 줄=보일러플레이트'로 후처리 -> 구조에 안 의존.
    removed = 0
    if not a.no_boiler and len(pages) >= 3:
        boiler = find_boilerplate(pages.values(), a.boiler_threshold)
        if boiler:
            pages = {u: strip_boilerplate(md, boiler) for u, md in pages.items()}
            removed = len(boiler)

    # 3) 저장 (strip_chrome + 선택적 이미지 다운로드)
    written = set()
    for u, md in pages.items():
        save(a.out, u, md, a.assets)
        written.add(urlsplit(u).path)

    print(f"written    : {len(written)}")
    print(f"boilerplate: {removed} lines removed (cross-page)")
    print(f"spurious   : {len(spurious)} (min-len 미달/404)")
    for u in spurious:
        print("  skip:", u)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="URL 경로 미러링 문서 크롤러")
    p.add_argument("seed", help="시작 URL")
    p.add_argument("--pattern", action="append", help="따라갈 URL glob(전체 크롤 시 필요, 반복). 예: '*host/docs*'")
    p.add_argument("--single", action="store_true", help="단일 페이지만 (deep-crawl·cross-page 정제 없음, --pattern 불필요)")
    p.add_argument("--out", default=".", help="출력 루트 (기본 현재 디렉토리)")
    p.add_argument("--lang", default=None, help="Accept-Language로 로케일 고정 (예: en, ko)")
    p.add_argument("--selector", action="append", help="본문 CSS 셀렉터(반복=폴백 체인). 기본: .devsite-article-body(devsite), #content-area(Mintlify), main, article")
    p.add_argument("--block", action="append", default=None, help="따라가지 않을 URL glob(반복). 기본: *hl=* (로케일 폭발 방지)")
    p.add_argument("--boiler-threshold", type=float, default=0.4, help="이 비율 이상 페이지에 반복되는 줄을 nav/footer로 보고 제거(이미지 줄 제외). 기본 0.4")
    p.add_argument("--no-boiler", action="store_true", help="cross-page 반복 제거 끄기")
    p.add_argument("--max-pages", type=int, default=500)
    p.add_argument("--max-depth", type=int, default=6)
    p.add_argument("--min-len", type=int, default=400, help="본문이 이보다 짧으면 스퓨리어스로 제외")
    p.add_argument("--assets", action="store_true", help="원격 이미지를 페이지 옆 <page>.assets/로 다운로드 (기본: 원격 URL 참조만)")
    a = p.parse_args()
    if not a.single and not a.pattern:
        p.error("전체 크롤은 --pattern 필요 (단일 페이지는 --single)")
    a.selector = a.selector or [".devsite-article-body", "#content-area", "main", "article"]
    a.block = a.block if a.block is not None else ["*hl=*"]
    asyncio.run(main(a))
