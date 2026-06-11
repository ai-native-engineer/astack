#!/usr/bin/env python3
"""외부 보도 수집: 네이버 뉴스 검색 API + Google News RSS 검색 → press-inventory.tsv

사용:
  python3 search_press.py "쿼리1" ["쿼리2" ...] --out <dir> [옵션]

네이버는 NAVER_CLIENT_ID / NAVER_CLIENT_SECRET 환경변수가 필요하다 (agents-env run으로 주입).
Google News RSS는 키가 필요 없다. 기사 링크는 인코딩돼 있어 batchexecute 방식으로
원문 URL을 디코딩하며, 실패하면 인코딩 URL을 그대로 보존한다(decoded=no).

출력: <out>/press-inventory.tsv
컬럼: source  date  outlet  title  url  decoded  queries
"""

import argparse
import email.utils
import html
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import date, timedelta

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
GNEWS_LOCALES = {
    "ko": "hl=ko&gl=KR&ceid=KR:ko",
    "en": "hl=en-US&gl=US&ceid=US:en",
}


def fetch(url, headers=None, data=None, timeout=15):
    req = urllib.request.Request(url, data=data, headers={"User-Agent": UA, **(headers or {})})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


def clean_text(s):
    s = html.unescape(html.unescape(s or ""))
    s = re.sub(r"</?b>", "", s)
    return re.sub(r"\s+", " ", s).strip()


def parse_pubdate(s):
    try:
        return email.utils.parsedate_to_datetime(s).date().isoformat()
    except Exception:
        return ""


def outlet_from_url(url):
    try:
        host = urllib.parse.urlparse(url).netloc.lower()
        return host[4:] if host.startswith("www.") else host
    except Exception:
        return ""


# ---------- 네이버 뉴스 검색 API ----------

def search_naver(query, delay=0.15):
    """sort=date로 페이징 전수 회수. start<=1000 제한이라 쿼리당 최대 ~1,100건."""
    cid = os.environ.get("NAVER_CLIENT_ID")
    csec = os.environ.get("NAVER_CLIENT_SECRET")
    if not (cid and csec):
        print("  ! NAVER_CLIENT_ID/NAVER_CLIENT_SECRET 없음 — naver 스킵 "
              "(agents-env run NAVER_CLIENT_ID NAVER_CLIENT_SECRET -- ... 로 실행)", file=sys.stderr)
        return [], None
    headers = {"X-Naver-Client-Id": cid, "X-Naver-Client-Secret": csec}
    items, total = [], None
    starts = list(range(1, 1000, 100)) + [1000]
    for start in starts:
        url = ("https://openapi.naver.com/v1/search/news.json?"
               + urllib.parse.urlencode({"query": query, "display": 100, "start": start, "sort": "date"}))
        try:
            body = json.loads(fetch(url, headers=headers))
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", errors="replace")[:200]
            hint = " (403이면 개발자센터 앱 'API 설정'에서 '검색' 체크 확인)" if e.code == 403 else ""
            print(f"  ! naver HTTP {e.code}{hint}: {detail}", file=sys.stderr)
            break
        total = body.get("total", total)
        page = body.get("items", [])
        if not page:
            break
        for it in page:
            orig = it.get("originallink") or it.get("link") or ""
            items.append({
                "source": "naver",
                "date": parse_pubdate(it.get("pubDate", "")),
                "outlet": outlet_from_url(orig),
                "title": clean_text(it.get("title", "")),
                "url": orig,
                "decoded": "-",
            })
        if start + len(page) > min(total or 0, 1000):
            break
        time.sleep(delay)
    return items, total


# ---------- Google News RSS 검색 ----------

def gnews_feed_queries(query, years_back):
    """기본(최근) 쿼리 + 연 단위 after:/before: 윈도우 (피드당 ~100건 캡 우회)."""
    qs = [query]
    today = date.today()
    for i in range(years_back):
        end = today - timedelta(days=365 * i)
        start = today - timedelta(days=365 * (i + 1))
        qs.append(f"{query} after:{start.isoformat()} before:{end.isoformat()}")
    return qs


def search_gnews(query, locale, years_back):
    items = []
    for q in gnews_feed_queries(query, years_back):
        url = ("https://news.google.com/rss/search?q=" + urllib.parse.quote(q)
               + "&" + GNEWS_LOCALES[locale])
        try:
            root = ET.fromstring(fetch(url))
        except Exception as e:
            print(f"  ! gnews fetch 실패 ({q!r}): {e}", file=sys.stderr)
            continue
        for item in root.iter("item"):
            link = (item.findtext("link") or "").strip()
            src = item.find("source")
            items.append({
                "source": f"gnews-{locale}",
                "date": parse_pubdate(item.findtext("pubDate") or ""),
                "outlet": clean_text(src.text if src is not None else ""),
                "title": clean_text(item.findtext("title") or ""),
                "url": link,
                "decoded": "no" if "news.google.com" in link else "-",
            })
        time.sleep(0.3)
    return items


def gnews_decode(link, timeout=15):
    """인코딩 링크 → 원문 URL. 페이지에서 서명/타임스탬프 추출 후 batchexecute POST."""
    m = re.search(r"/articles/([^/?]+)", link)
    if not m:
        return None
    art_id = m.group(1)
    page = fetch(f"https://news.google.com/rss/articles/{art_id}", timeout=timeout)
    sg = re.search(r'data-n-a-sg="([^"]+)"', page)
    ts = re.search(r'data-n-a-ts="([^"]+)"', page)
    if not (sg and ts):
        return None
    inner = ('["garturlreq",[["X","X",["X","X"],null,null,1,1,"US:en",null,1,null,null,null,null,null,0,1],'
             f'"X","X",1,[1,1,1],1,1,null,0,0,null,0],"{art_id}",{ts.group(1)},"{sg.group(1)}"]')
    body = "f.req=" + urllib.parse.quote(json.dumps([[["Fbv4je", inner, None, "generic"]]]))
    resp = fetch("https://news.google.com/_/DotsSplashUi/data/batchexecute",
                 headers={"content-type": "application/x-www-form-urlencoded;charset=UTF-8"},
                 data=body.encode(), timeout=timeout)
    chunk = resp.split("\n\n")[1]
    return json.loads(json.loads(chunk)[0][2])[1]


# ---------- 병합·중복 제거·출력 ----------

def norm_title(t):
    return re.sub(r"[\s\W]+", "", t).lower()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("queries", nargs="+", help="검색 쿼리 (회사명, 회사명+대표명 등 변형을 여러 개)")
    ap.add_argument("--out", required=True, help="출력 디렉토리")
    ap.add_argument("--sources", default="naver,gnews", help="naver,gnews 중 선택 (기본 둘 다)")
    ap.add_argument("--gnews-locales", default="ko,en", help="ko,en (기본 둘 다)")
    ap.add_argument("--years-back", type=int, default=3, help="gnews 연 단위 윈도우 수 (기본 3)")
    ap.add_argument("--decode-limit", type=int, default=250, help="gnews 원문 URL 디코딩 상한 (기본 250, 0=안 함)")
    ap.add_argument("--decode-interval", type=float, default=0.7, help="디코딩 호출 간격 초 (기본 0.7)")
    args = ap.parse_args()
    sources = {s.strip() for s in args.sources.split(",")}

    rows = []
    if "naver" in sources:
        for q in args.queries:
            print(f"[naver] {q!r}")
            items, total = search_naver(q)
            for it in items:
                it["query"] = q
            rows += items
            if total is not None:
                print(f"  total={total}, 회수={len(items)}" + (" — 1,000건 벽: 쿼리 분할 권장" if total > 1100 else ""))

    if "gnews" in sources:
        for locale in [l.strip() for l in args.gnews_locales.split(",")]:
            for q in args.queries:
                print(f"[gnews-{locale}] {q!r} (+{args.years_back}개 연 윈도우)")
                items = search_gnews(q, locale, args.years_back)
                for it in items:
                    it["query"] = q
                rows += items
                print(f"  회수={len(items)}")

    # 1차 dedupe: URL 기준 + (outlet, 제목) 기준
    seen_url, seen_key, merged = {}, {}, []
    for it in rows:
        key_u, key_t = it["url"], (it["outlet"], norm_title(it["title"]))
        dup = seen_url.get(key_u) or (seen_key.get(key_t) if it["title"] else None)
        if dup:
            if it["query"] not in dup["queries"]:
                dup["queries"] += f",{it['query']}"
            continue
        it["queries"] = it.pop("query")
        seen_url[key_u] = it
        if it["title"]:
            seen_key[key_t] = it
        merged.append(it)

    # gnews 원문 URL 디코딩 (최신순 우선, 실패 시 인코딩 URL 보존)
    todo = [it for it in sorted(merged, key=lambda x: x["date"], reverse=True) if it["decoded"] == "no"]
    skipped = max(0, len(todo) - args.decode_limit)
    ok = fail = 0
    for it in todo[: args.decode_limit]:
        try:
            url = gnews_decode(it["url"])
        except Exception:
            url = None
        if url:
            it["url"], it["outlet"], it["decoded"] = url, outlet_from_url(url), "yes"
            ok += 1
        else:
            fail += 1
        time.sleep(args.decode_interval)
    if todo:
        print(f"[decode] 성공={ok} 실패={fail}" + (f" 미시도={skipped} (--decode-limit 상향 가능)" if skipped else ""))

    # 2차 dedupe: 디코딩으로 naver와 URL이 겹친 항목 제거
    final, seen = [], set()
    for it in sorted(merged, key=lambda x: x["date"], reverse=True):
        if it["url"] in seen:
            continue
        seen.add(it["url"])
        final.append(it)

    os.makedirs(args.out, exist_ok=True)
    out_path = os.path.join(args.out, "press-inventory.tsv")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("source\tdate\toutlet\ttitle\turl\tdecoded\tqueries\n")
        for it in final:
            f.write("\t".join(
                (it[c] or "").replace("\t", " ").replace("\n", " ")
                for c in ("source", "date", "outlet", "title", "url", "decoded", "queries")) + "\n")

    by_src = {}
    for it in final:
        by_src[it["source"]] = by_src.get(it["source"], 0) + 1
    print(f"\n저장: {out_path}")
    print(f"총 {len(final)}건 (중복 제거 전 {len(rows)}건) — " + ", ".join(f"{k} {v}" for k, v in sorted(by_src.items())))


if __name__ == "__main__":
    main()
