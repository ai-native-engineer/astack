#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["requests"]
# ///
"""
similar.py — SimilarWeb 무료 데이터 엔드포인트 클라이언트

SimilarWeb 크롬 확장이 쓰는 비공개 엔드포인트
(data.similarweb.com/api/v1/data)를 호출해 트래픽·순위·유입 데이터를
API 키 없이 가져온다.

원본(DaWe35/Similarweb-free-API) 대비 개선:
  - 브라우저 User-Agent 헤더            → 봇 차단(1차 403) 회피
  - 디스크 캐시(TTL)                    → 반복 호출 자체를 제거
  - 호출 간 스로틀 + 지수 백오프 재시도 → CloudFront rate limit(2차 403) 방어
  - 응답 정규화(문자열→숫자, 비율→%, 결측/IsSmall 처리)
  - 여러 도메인 비교, 월별 추이, JSON/CSV 내보내기, CLI

실행:
  uv run similar.py github.com
  uv run similar.py github.com stripe.com vercel.com   # 비교 표
  uv run similar.py openai.com --ai                     # AI 챗봇 유입 분석
  uv run similar.py wikipedia.org --keywords           # 키워드 SEO 가치
  uv run similar.py github.com --history               # 월별 방문 추이
  (또는 `pip install requests` 후 `python3 similar.py ...`)

라이브러리로:
  import similar
  s = similar.get("github.com")          # 정규화된 SiteData
  raw = similar.similarGet("github.com")  # 원본 호환(원본 JSON dict)
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse

import requests

ENDPOINT = "https://data.similarweb.com/api/v1/data?domain={}"
CACHE_DIR = Path.home() / ".cache" / "similarweb"
LAST_REQUEST_FILE = CACHE_DIR / ".last_request"
DEFAULT_TTL = 86_400          # 캐시 유효기간(초) — 24시간
DEFAULT_INTERVAL = 2.0        # 호출 간 최소 간격(초)
DEFAULT_RETRIES = 4           # 백오프 재시도 횟수
RETRY_CODES = {403, 429, 500, 502, 503, 504}

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
}


class RateLimited(Exception):
    """재시도를 소진하고도 403/429 차단이 풀리지 않은 경우."""


_SESSION = requests.Session()
_SESSION.headers.update(HEADERS)


# ── 도메인 정규화 ──────────────────────────────────────────────
def normalize_domain(raw: str) -> str:
    """URL 또는 호스트 문자열에서 등록 도메인만 추출.

    원본의 `replace("www.", "")`는 문자열 어디서나 치환돼 깨질 수 있어
    (예: "wwww.x.com"), 여기선 www. prefix만 제거한다.
    """
    netloc = urlparse(raw if "//" in raw else "//" + raw).netloc
    host = (netloc or raw).split("@")[-1].split(":")[0].strip().lower()
    return host[4:] if host.startswith("www.") else host


# ── 캐시 ───────────────────────────────────────────────────────
def _cache_file(domain: str) -> Path:
    return CACHE_DIR / f"{domain}.json"


def _read_cache(domain: str, ttl: int):
    f = _cache_file(domain)
    if f.exists() and time.time() - f.stat().st_mtime <= ttl:
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return None
        return data if isinstance(data, dict) else None
    return None


def _write_cache(domain: str, data: dict) -> None:
    """캐시 저장은 best-effort: temp 파일에 쓰고 원자적으로 교체한다.

    쓰기 실패(디스크 풀·권한 등)는 이미 받은 데이터 반환을 막지 않도록 무시한다.
    """
    target = _cache_file(domain)
    tmp = target.with_name(target.name + ".tmp")
    try:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        tmp.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        tmp.replace(target)  # 같은 파일시스템에서 원자적 교체
    except OSError:
        pass


# ── 스로틀 ─────────────────────────────────────────────────────
def _throttle(min_interval: float) -> None:
    """직전 요청과 min_interval 이상 간격 확보(프로세스 재실행 간에도 유지).

    마지막 요청 시각을 파일에 남겨, 스크립트를 짧게 여러 번 돌려도
    rate limit 임계에 도달하지 않게 한다. 캐시 적중 시엔 호출되지 않는다.
    """
    try:
        last = float(LAST_REQUEST_FILE.read_text())
    except (OSError, ValueError):
        last = 0.0
    wait = min_interval - (time.time() - last)
    if wait > 0:
        time.sleep(wait)
    try:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        LAST_REQUEST_FILE.write_text(str(time.time()))
    except OSError:
        pass  # 스로틀 기록 실패는 무시(best-effort) — 정상 요청을 막지 않는다


# ── HTTP (캐시 → 스로틀 → 백오프 재시도) ───────────────────────
def fetch_raw(
    domain: str,
    *,
    ttl: int = DEFAULT_TTL,
    use_cache: bool = True,
    retries: int = DEFAULT_RETRIES,
    min_interval: float = DEFAULT_INTERVAL,
    proxy: str | None = None,
) -> tuple[dict, bool]:
    """원본 JSON을 가져온다. 반환: (data, from_cache)."""
    if use_cache:
        cached = _read_cache(domain, ttl)
        if cached is not None:
            return cached, True

    url = ENDPOINT.format(domain)
    proxies = {"http": proxy, "https": proxy} if proxy else None
    delay = 5.0
    for attempt in range(1, retries + 1):
        _throttle(min_interval)
        try:
            resp = _SESSION.get(url, timeout=30, proxies=proxies)
        except requests.RequestException as e:
            if attempt < retries:
                time.sleep(delay)
                delay *= 2
                continue
            raise RateLimited(f"{domain}: 네트워크 오류 {e}") from e

        if resp.status_code == 200:
            try:
                data = resp.json()
            except ValueError as e:
                raise RateLimited(f"{domain}: 응답이 JSON이 아님 (차단 가능성)") from e
            if not isinstance(data, dict):
                # 200인데 dict가 아닌 본문(문자열·리스트·null 등)은 차단/오류 신호.
                # 캐시에 쓰지 않고 이미 처리되는 RateLimited 경로로 보낸다.
                raise RateLimited(f"{domain}: 예상치 못한 응답 형식 (차단 가능성)")
            _write_cache(domain, data)
            return data, False

        if resp.status_code in RETRY_CODES and attempt < retries:
            sys.stderr.write(
                f"  [{domain}] HTTP {resp.status_code} — {delay:.0f}s 후 재시도 "
                f"({attempt}/{retries})\n"
            )
            time.sleep(delay)
            delay *= 2
            continue

        if resp.status_code in (403, 429):
            raise RateLimited(
                f"{domain}: {resp.status_code} 차단. 수 분 뒤 재시도하거나 "
                f"--interval 을 늘리세요."
            )
        resp.raise_for_status()

    raise RateLimited(f"{domain}: 재시도 소진")


def similarGet(website: str):
    """원본 호환 함수: 도메인/URL → 원본 JSON(dict).

    캐시·백오프가 적용된다(원본은 단순 GET, 실패 시 False 반환).
    """
    data, _ = fetch_raw(normalize_domain(website))
    return data


# ── 정규화 ─────────────────────────────────────────────────────
def _f(v):
    """문자열/숫자 → float, 변환 불가 시 None. (Engagments 값이 문자열로 옴)"""
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def _i(v):
    f = _f(v)
    return int(f) if f is not None else None


@dataclass
class SiteData:
    domain: str
    name: str | None
    description: str | None
    global_rank: int | None
    country_rank: int | None
    country_code: str | None
    category: str | None
    category_rank: int | None
    is_small: bool
    monthly_visits: int | None
    bounce_rate: float | None        # 0~1
    pages_per_visit: float | None
    time_on_site: float | None       # 초
    top_countries: list              # [(country_code, share)]
    traffic_sources: dict            # {source: share(0~1)}
    monthly_history: dict            # {YYYY-MM-DD: visits}
    keywords: list                   # [{name, volume, cpc, value}]
    competitors: list                # [domain, ...]
    ai_visits: float | None          # AI 챗봇에서 온 월 추정 방문
    ai_share: float | None           # 전체 트래픽 중 AI 유입 비율(0~1)
    ai_chatbots: list                # [(name, share%)] — LLM별 점유율
    ai_prompts: list                 # [prompt, ...] — 유입 프롬프트
    screenshot: str | None
    snapshot_date: str | None
    from_cache: bool = False

    @classmethod
    def parse(cls, raw: dict, domain: str, from_cache: bool = False) -> "SiteData":
        eng = raw.get("Engagments") or {}
        gr = raw.get("GlobalRank") or {}
        cr = raw.get("CountryRank") or {}
        catr = raw.get("CategoryRank") or {}
        ai = raw.get("AiTrafficDetails") or {}
        ai_dist = ((ai.get("Traffic") or {}).get("Distribution")) or {}
        comp = (raw.get("Competitors") or {}).get("TopSimilarityCompetitors") or []
        return cls(
            domain=domain,
            name=raw.get("SiteName"),
            description=(raw.get("Description") or "").strip() or None,
            global_rank=_i(gr.get("Rank")),
            country_rank=_i(cr.get("Rank")),
            country_code=cr.get("CountryCode"),
            category=(catr.get("Category") or raw.get("Category") or "").strip() or None,
            category_rank=_i(catr.get("Rank")),
            is_small=bool(raw.get("IsSmall")),
            monthly_visits=_i(eng.get("Visits")),
            bounce_rate=_f(eng.get("BounceRate")),
            pages_per_visit=_f(eng.get("PagePerVisit")),
            time_on_site=_f(eng.get("TimeOnSite")),
            top_countries=[
                (c.get("CountryCode"), c.get("Value"))
                for c in (raw.get("TopCountryShares") or [])
                if c.get("CountryCode")
            ],
            traffic_sources={
                k: v
                for k, v in (raw.get("TrafficSources") or {}).items()
                if isinstance(v, (int, float)) and v > 0
            },
            monthly_history=raw.get("EstimatedMonthlyVisits") or {},
            keywords=[
                {"name": k.get("Name"), "volume": _i(k.get("Volume")),
                 "cpc": _f(k.get("Cpc")), "value": _i(k.get("EstimatedValue"))}
                for k in (raw.get("TopKeywords") or [])
                if k.get("Name")
            ],
            competitors=[
                c.get("Domain") for c in comp
                if isinstance(c, dict) and c.get("Domain")
            ],
            ai_visits=_f(ai.get("TotalVisits")),
            ai_share=_f(ai.get("ReferralTraffic")),
            ai_chatbots=[
                (c.get("Name"), _f(c.get("Value")))
                for c in (ai_dist.get("Chatbots") or [])
                if c.get("Name") and _f(c.get("Value")) is not None
            ],
            ai_prompts=[
                p for p in ((ai.get("TopPrompts") or {}).get("Prompts") or []) if p
            ],
            screenshot=raw.get("LargeScreenshot") or None,
            snapshot_date=raw.get("SnapshotDate"),
            from_cache=from_cache,
        )


def get(domain_or_url: str, **kw) -> SiteData:
    """편의 함수: 도메인/URL → 정규화된 SiteData."""
    d = normalize_domain(domain_or_url)
    raw, cached = fetch_raw(d, **kw)
    return SiteData.parse(raw, d, from_cache=cached)


def to_dict(s: SiteData) -> dict:
    return {
        "domain": s.domain,
        "name": s.name,
        "description": s.description,
        "global_rank": s.global_rank,
        "country_rank": s.country_rank,
        "country_code": s.country_code,
        "category": s.category,
        "category_rank": s.category_rank,
        "is_small": s.is_small,
        "monthly_visits": s.monthly_visits,
        "bounce_rate": s.bounce_rate,
        "pages_per_visit": s.pages_per_visit,
        "time_on_site": s.time_on_site,
        "top_countries": s.top_countries,
        "traffic_sources": s.traffic_sources,
        "keywords": s.keywords,
        "competitors": s.competitors,
        "ai_visits": s.ai_visits,
        "ai_share": s.ai_share,
        "ai_chatbots": s.ai_chatbots,
        "ai_prompts": s.ai_prompts,
        "screenshot": s.screenshot,
        "snapshot_date": s.snapshot_date,
    }


# ── 포맷팅 ─────────────────────────────────────────────────────
def _num(n):
    return f"{n:,}" if isinstance(n, (int, float)) else "—"


def _pct(v):
    return f"{v * 100:.1f}%" if isinstance(v, (int, float)) else "—"


def _dur(sec):
    if not isinstance(sec, (int, float)):
        return "—"
    m, s = divmod(int(sec), 60)
    return f"{m}m {s}s" if m else f"{s}s"


def render_detail(s: SiteData) -> str:
    L = [f"■ {s.domain}" + ("  (cache)" if s.from_cache else "")]
    if s.is_small:
        L.append("  ⚠ IsSmall: SimilarWeb이 '트래픽 적음'으로 표시 — 추정치 신뢰도 낮음")
    ppv = f"{s.pages_per_visit:.2f}" if s.pages_per_visit is not None else "—"
    rank = _num(s.country_rank)
    if s.country_code and s.country_rank is not None:
        rank = f"{rank} ({s.country_code})"  # 국가코드는 값쪽에 붙여 라벨 정렬 유지
    cat = s.category or "—"
    if s.category and s.category_rank is not None:
        cat = f"{s.category} (#{s.category_rank})"
    if s.description:
        L.append(f"  설명         : {s.description[:70]}")
    L.append(f"  사이트명     : {s.name or '—'}")
    L.append(f"  카테고리     : {cat}")
    L.append(f"  글로벌 순위  : {_num(s.global_rank)}")
    L.append(f"  국가 순위    : {rank}")
    L.append(f"  월 추정 방문 : {_num(s.monthly_visits)}")
    L.append(f"  평균 체류    : {_dur(s.time_on_site)}")
    L.append(f"  페이지/방문  : {ppv}")
    L.append(f"  이탈률       : {_pct(s.bounce_rate)}")
    if s.top_countries:
        cs = "  ".join(f"{c}:{_pct(v)}" for c, v in s.top_countries[:5])
        L.append(f"  유입 국가    : {cs}")
    if s.traffic_sources:
        srcs = sorted(s.traffic_sources.items(), key=lambda x: -x[1])
        ss = "  ".join(f"{k}:{_pct(v)}" for k, v in srcs)
        L.append(f"  트래픽 소스  : {ss}")
    if s.ai_share is not None or s.ai_chatbots:
        bots = "  ".join(f"{n}:{v:.0f}%" for n, v in s.ai_chatbots[:3])
        L.append(f"  AI 유입      : {_pct(s.ai_share)} of traffic  ({bots})")
    if s.keywords:
        L.append(f"  상위 키워드  : {', '.join(k['name'] for k in s.keywords[:5])}")
    if s.competitors:
        L.append(f"  경쟁사       : {', '.join(s.competitors[:5])}")
    return "\n".join(L)


def render_compare(sites: list) -> str:
    head = ["Domain", "Global", "Country", "Visits/mo", "Bounce", "Pages", "Time"]
    rows = [head]
    for s in sites:
        country = _num(s.country_rank)
        if s.country_code and s.country_rank is not None:
            country = f"{country} {s.country_code}"
        rows.append([
            s.domain,
            _num(s.global_rank),
            country,
            _num(s.monthly_visits),
            _pct(s.bounce_rate),
            f"{s.pages_per_visit:.2f}" if s.pages_per_visit is not None else "—",
            _dur(s.time_on_site),
        ])
    widths = [max(len(r[i]) for r in rows) for i in range(len(head))]
    out = []
    for ri, r in enumerate(rows):
        out.append("  ".join(c.ljust(widths[i]) for i, c in enumerate(r)))
        if ri == 0:
            out.append("  ".join("-" * widths[i] for i in range(len(head))))
    return "\n".join(out)


def render_history(s: SiteData) -> str:
    # 월별 값은 raw 그대로 저장되므로(문자열/None 가능) 여기서 숫자로 변환·필터한다.
    hist = sorted((d, _i(v)) for d, v in s.monthly_history.items())
    hist = [(d, v) for d, v in hist if v is not None]
    if not hist:
        return f"■ {s.domain}: 월별 추이 데이터 없음"
    peak = max((v for _, v in hist), default=0) or 1
    L = [f"■ {s.domain} — 월별 추정 방문 추이"]
    prev = None
    for date, v in hist:
        bar = "█" * round(40 * v / peak)
        chg = ""
        if prev:
            d = (v - prev) / prev * 100
            chg = f"  ({'+' if d >= 0 else ''}{d:.0f}%)"
        L.append(f"  {date[:7]}  {_num(v):>14}  {bar}{chg}")
        prev = v
    return "\n".join(L)


def render_ai(s: SiteData) -> str:
    if not (s.ai_chatbots or s.ai_visits):
        return f"■ {s.domain}: AI 트래픽 데이터 없음"
    L = [f"■ {s.domain} — AI 챗봇 유입 분석"]
    if s.ai_visits is not None:
        L.append(f"  AI 월 유입 방문 : {_num(int(s.ai_visits))}")
    if s.ai_share is not None:
        L.append(f"  전체 대비 AI 비율: {_pct(s.ai_share)}")
    if s.ai_chatbots:
        L.append("  챗봇별 점유율:")
        peak = max((v for _, v in s.ai_chatbots), default=0) or 1
        for name, v in s.ai_chatbots:
            bar = "█" * round(30 * v / peak)
            L.append(f"    {name:<22} {v:5.1f}%  {bar}")
    if s.ai_prompts:
        L.append("  유입 프롬프트(top):")
        for p in s.ai_prompts[:5]:
            L.append(f"    - {p}")
    return "\n".join(L)


def render_keywords(s: SiteData) -> str:
    if not s.keywords:
        return f"■ {s.domain}: 키워드 데이터 없음"
    L = [f"■ {s.domain} — 상위 키워드 (SEO 가치)"]
    for k in s.keywords:
        cpc = f"${k['cpc']:.2f}" if k["cpc"] is not None else "—"
        L.append(
            f"  {k['name']}  ·  검색량 {_num(k['volume'])}"
            f"  ·  CPC {cpc}  ·  추정가치 {_num(k['value'])}"
        )
    return "\n".join(L)


def write_csv(sites: list, path: str | None) -> None:
    cols = ["domain", "name", "category", "category_rank", "global_rank",
            "country_rank", "country_code", "is_small", "monthly_visits",
            "bounce_rate", "pages_per_visit", "time_on_site",
            "ai_visits", "ai_share", "snapshot_date"]
    f = open(path, "w", newline="", encoding="utf-8") if path else sys.stdout
    try:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for s in sites:
            w.writerow(to_dict(s))
    finally:
        if path:
            f.close()


# ── CLI ────────────────────────────────────────────────────────
def main(argv=None) -> int:
    p = argparse.ArgumentParser(
        description="SimilarWeb 무료 엔드포인트 클라이언트 (캐시·스로틀·백오프 내장)"
    )
    p.add_argument("domains", nargs="+", help="도메인 또는 URL (여러 개 가능)")
    p.add_argument("-c", "--compare", action="store_true", help="비교 표로 출력")
    # 출력 모드는 상호 배타 — 충돌 시 argparse가 명확히 거부(silent 무시 방지)
    mode = p.add_mutually_exclusive_group()
    mode.add_argument("--ai", action="store_true", help="AI 챗봇 유입 분석")
    mode.add_argument("--keywords", "--kw", action="store_true",
                      dest="keywords", help="상위 키워드 SEO 가치")
    mode.add_argument("--history", action="store_true", help="월별 방문 추이")
    mode.add_argument("--json", action="store_true", help="정규화 결과를 JSON으로")
    mode.add_argument("--raw", action="store_true", help="원본 응답 JSON 그대로")
    mode.add_argument("--csv", nargs="?", const="", metavar="PATH",
                      help="CSV로 출력 (경로 생략 시 stdout)")
    p.add_argument("--no-cache", action="store_true", help="캐시 무시하고 새로 요청")
    p.add_argument("--ttl", type=int, default=DEFAULT_TTL,
                   help=f"캐시 TTL(초), 기본 {DEFAULT_TTL}")
    p.add_argument("--interval", type=float, default=DEFAULT_INTERVAL,
                   help=f"호출 간 최소 간격(초), 기본 {DEFAULT_INTERVAL}")
    p.add_argument("--retries", type=int, default=DEFAULT_RETRIES,
                   help=f"백오프 재시도 횟수, 기본 {DEFAULT_RETRIES}")
    p.add_argument("--proxy", help="프록시 URL (예: socks5h://localhost:9050)")
    args = p.parse_args(argv)
    if args.ttl < 0:
        p.error("--ttl 은 0 이상이어야 합니다 (캐시를 끄려면 --no-cache)")
    if args.retries < 1:
        p.error("--retries 는 1 이상이어야 합니다")
    if args.interval < 0:
        p.error("--interval 은 0 이상이어야 합니다")

    fetch_kw = dict(ttl=args.ttl, use_cache=not args.no_cache,
                    retries=args.retries, min_interval=args.interval,
                    proxy=args.proxy)

    # 중복 제거하며 입력 순서 유지
    domains = []
    for d in args.domains:
        nd = normalize_domain(d)
        if nd and nd not in domains:
            domains.append(nd)

    sites, raws, errors = [], {}, []
    for d in domains:
        try:
            raw, cached = fetch_raw(d, **fetch_kw)
            raws[d] = raw
            sites.append(SiteData.parse(raw, d, from_cache=cached))
        except (RateLimited, requests.HTTPError) as e:
            errors.append(str(e))

    if not sites:
        sys.stderr.write("모든 요청 실패:\n" + "\n".join(errors) + "\n")
        return 1

    if args.raw:
        payload = raws if len(raws) > 1 else next(iter(raws.values()))
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    elif args.json:
        out = [to_dict(s) for s in sites]
        print(json.dumps(out if len(out) > 1 else out[0], indent=2, ensure_ascii=False))
    elif args.csv is not None:
        write_csv(sites, args.csv or None)
    elif args.ai:
        print("\n\n".join(render_ai(s) for s in sites))
    elif args.keywords:
        print("\n\n".join(render_keywords(s) for s in sites))
    elif args.history:
        print("\n\n".join(render_history(s) for s in sites))
    elif args.compare or len(sites) > 1:
        print(render_compare(sites))
    else:
        print(render_detail(sites[0]))

    if errors:
        sys.stderr.write("\n[일부 실패]\n" + "\n".join(errors) + "\n")
        return 2  # 부분 실패: 0(전체 성공)·1(전체 실패)과 구분
    return 0


if __name__ == "__main__":
    sys.exit(main())
