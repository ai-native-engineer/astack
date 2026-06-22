#!/usr/bin/env -S uv run --with crawl4ai --quiet python
"""문서 섹션을 deep-crawl해 각 페이지를 URL 경로에 대응하는 .md 파일로 저장.

URL `https://host/a/b` → `<out>/host/a/b.md` (URL 경로 = 파일 경로).
crwl CLI(`crwl -O`)는 전체를 한 파일에 `# <URL>` 구분선으로 이어 붙이지만, 이 스크립트는
페이지별 파일로 미러링한다. 문서 사이트(특히 Google devsite)에서 겪은 함정을 기본값에 박아둠:

- 로케일 폭발: devsite 페이지는 footer에 `?hl=<lang>` 링크가 있어 deep-crawl이 ~20배로 불어난다.
  → 기본으로 `*hl=*` 링크를 따라가지 않고(--block), 언어는 Accept-Language(--lang)로 고정한다.
- 보일러플레이트: full markdown은 nav/footer가 반복된다. → target_elements로 본문 컨테이너만 마크다운 생성
  (--selector, 후보 리스트). nav/footer는 본문 밖이라 자동 제외(excluded_tags로 nav를 지우면 그 안 링크까지
  사라져 발견이 다시 막히므로 쓰지 않는다).
- 발견과 추출 분리(핵심): css_selector는 "entire extraction process"에 영향 → 셀렉터 밖 nav 링크가 잘려
  deep-crawl이 못 따라간다(실측: docs.crawl4ai.com css_selector='main' 24개 vs target_elements 118개 발견).
  target_elements는 추출만 본문에 한정하고 링크 발견은 전체 DOM 유지, List[str]라 후보를 한 번에 넘기고
  미매칭 시 전체 페이지로 graceful degrade → 셀렉터 자동승격·폴백 복구가 불필요(사이트 구조 무관).
- 끊긴/오타 링크(404): deep-crawl에 스퓨리어스 URL이 섞인다. → 본문 길이 게이트(--min-len)로 버린다.
- Mintlify 크롬: 헤딩이 `## `+`[​](anchor)`+텍스트 3줄로 쪼개지고, `Copy page` 버튼·`Was this page helpful?` 푸터·제목 위 eyebrow가 박힌다.
  → 저장 전 strip_chrome()으로 재결합·제거(패턴 없으면 no-op이라 사이트 무관).
- 이미지: raw_markdown은 원격 URL 참조만 남긴다. 로컬 보존(상대경로 치환)은 --assets로 페이지 옆 <page>.assets/에 받는다.

사용:
  crawl-mirror.py https://developers.google.com/search/docs \
      --pattern "*developers.google.com/search/docs*" --lang en --out .
전체 옵션: --help
"""
import argparse
import asyncio
import hashlib
import os
import re
import urllib.request
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


def save(out, url, md, assets=False):
    fp, clean = dest(out, url)
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    body = strip_chrome(md).strip()
    if assets:
        body = fetch_assets(body, fp)
    with open(fp, "w", encoding="utf-8") as f:
        f.write(f"<!-- source: {clean} -->\n\n{body}\n")


async def main(a):
    filters = [URLPatternFilter(patterns=a.pattern)]
    if a.block:
        filters.append(URLPatternFilter(patterns=a.block, reverse=True))
    strat = BFSDeepCrawlStrategy(
        max_depth=a.max_depth, max_pages=a.max_pages, filter_chain=FilterChain(filters)
    )
    headers = {"Accept-Language": f"{a.lang},{a.lang};q=0.9"} if a.lang else {}
    bc = BrowserConfig(headless=True, headers=headers)
    # target_elements: 마크다운 추출만 본문 컨테이너로 한정하고 링크 발견은 전체 DOM에서 유지한다.
    # css_selector는 "entire extraction process"에 영향 → 셀렉터 밖 nav 링크가 잘려 deep-crawl이 못 따라간다
    # (실측: docs.crawl4ai.com css_selector='main' 24개 vs target_elements 118개 발견). target_elements는
    # List[str]라 후보를 한 번에 넘기고 미매칭 시 전체 페이지로 graceful degrade → 셀렉터 자동승격·폴백 복구가 불필요.
    # excluded_tags는 안 쓴다: nav 태그를 제거하면 그 안 링크까지 사라져 deep-crawl 발견이 다시 막힌다
    # (css_selector와 같은 함정). target_elements가 추출을 본문으로 한정하므로 nav/footer는 어차피 추출에서 빠진다.
    deep = CrawlerRunConfig(
        deep_crawl_strategy=strat,
        target_elements=a.selector,
        cache_mode=CacheMode.BYPASS,
    )

    written, spurious = set(), []
    async with AsyncWebCrawler(config=bc) as c:
        for r in await c.arun(a.seed, config=deep):
            if not r.success:
                continue
            key = urlsplit(r.url).path
            md = (r.markdown.raw_markdown or "").strip()
            if len(md) >= a.min_len and key not in written:
                save(a.out, r.url, md, a.assets)
                written.add(key)
            elif len(md) < a.min_len:
                spurious.append(r.url)

    print(f"written  : {len(written)}")
    print(f"spurious : {len(spurious)} (min-len 미달/404, skipped)")
    for u in spurious:
        print("  skip:", u)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="URL 경로 미러링 문서 크롤러")
    p.add_argument("seed", help="시작 URL")
    p.add_argument("--pattern", action="append", required=True, help="따라갈 URL glob(반복). 예: '*host/docs*'")
    p.add_argument("--out", default=".", help="출력 루트 (기본 현재 디렉토리)")
    p.add_argument("--lang", default=None, help="Accept-Language로 로케일 고정 (예: en, ko)")
    p.add_argument("--selector", action="append", help="본문 CSS 셀렉터(반복=폴백 체인). 기본: .devsite-article-body(devsite), #content-area(Mintlify), main, article")
    p.add_argument("--block", action="append", default=None, help="따라가지 않을 URL glob(반복). 기본: *hl=* (로케일 폭발 방지)")
    p.add_argument("--max-pages", type=int, default=500)
    p.add_argument("--max-depth", type=int, default=6)
    p.add_argument("--min-len", type=int, default=400, help="본문이 이보다 짧으면 스퓨리어스로 제외")
    p.add_argument("--assets", action="store_true", help="원격 이미지를 페이지 옆 <page>.assets/로 다운로드 (기본: 원격 URL 참조만)")
    a = p.parse_args()
    a.selector = a.selector or [".devsite-article-body", "#content-area", "main", "article"]
    a.block = a.block if a.block is not None else ["*hl=*"]
    asyncio.run(main(a))
