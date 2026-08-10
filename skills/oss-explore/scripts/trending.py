#!/usr/bin/env python3
"""oss-explore :: trending fetcher
github.com/trending 페이지를 파싱해 레포 목록 JSON을 stdout으로 출력.
관심사/언어를 하드코딩하지 않는다 — 전부 인자로 받는다. 의존성 0(표준 라이브러리).
"""
import argparse
import datetime
import html
import json
import re
import sys
import urllib.parse
import urllib.request


def source_url(language, since):
    path = f"/trending/{urllib.parse.quote(language, safe='')}" if language else "/trending"
    return f"https://github.com{path}?since={since}"


def fetch(language, since):
    url = source_url(language, since)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (oss-explore)"})
    with urllib.request.urlopen(req, timeout=25) as response:
        return response.read().decode("utf-8", "replace")


def parse(doc, limit):
    out = []
    rows = re.findall(r'<article class="Box-row">(.*?)</article>', doc, re.S)
    if not rows:
        plain = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", doc)))
        if "It looks like we don’t have any trending repositories for your choices." in plain:
            return []
        raise ValueError("GitHub Trending markup changed or returned no recognizable rows")
    for row in rows:
        m = re.search(r'<h2[^>]*>\s*<a[^>]*href="/([^"]+)"', row)
        if not m:
            continue
        repo = re.sub(r"\s+", "", m.group(1))
        dm = re.search(r'<p[^>]*class="col-9[^"]*"[^>]*>(.*?)</p>', row, re.S)
        desc = html.unescape(re.sub(r"<[^>]+>", "", dm.group(1))).strip() if dm else ""
        lm = re.search(r'<span itemprop="programmingLanguage">([^<]+)</span>', row)
        lang = lm.group(1).strip() if lm else ""
        sm = re.search(r"([\d,]+)\s*stars?\s*(?:today|this week|this month)", row)
        if not sm:
            raise ValueError(f"could not parse period stars for {repo}")
        period = int(sm.group(1).replace(",", ""))
        tm = re.search(r'href="/[^"]+/stargazers"[^>]*>(?:\s*<svg.*?</svg>)?\s*([\d,]+)', row, re.S)
        if not tm:
            raise ValueError(f"could not parse total stars for {repo}")
        total = int(tm.group(1).replace(",", ""))
        out.append({
            "repo": repo, "period_stars": period, "total_stars": total,
            "language": lang, "description": desc,
        })
        if len(out) >= limit:
            break
    if not out:
        raise ValueError("GitHub Trending rows contained no recognizable repositories")
    return out


def positive_int(value):
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError("must be at least 1")
    return number


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("language", nargs="?", default="", help="trending 언어 (생략 시 전체)")
    ap.add_argument("--since", default="daily", choices=["daily", "weekly", "monthly"])
    ap.add_argument("--limit", type=positive_int, default=25)
    a = ap.parse_args()
    try:
        repos = parse(fetch(a.language, a.since), a.limit)
    except Exception as e:
        print(f'{{"type":"trending","error":{json.dumps(str(e))},"repos":[]}}')
        sys.exit(1)
    print(json.dumps(
        {"type": "trending", "language": a.language, "since": a.since,
         "generated": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
         "source_url": source_url(a.language, a.since), "repos": repos},
        ensure_ascii=False,
    ))


if __name__ == "__main__":
    main()
