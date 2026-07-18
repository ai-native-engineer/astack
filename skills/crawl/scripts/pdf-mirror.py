#!/usr/bin/env python3
"""미러에 링크된 PDF(eBook·가이드 등)를 원본 그대로 다운로드해 도메인 트리에 저장.

크롤은 HTML 텍스트만 받으므로 페이지에 [Download now](.../x.pdf)로 박힌 PDF 본문이 통째로 빠진다.
youtube-transcripts 패턴과 동일하게 미러 전체 .md를 스캔해 PDF URL을 모으고, 각 원본을 받아 <out>/<host>/<path>에 저장한다.
PDF는 자체 텍스트 레이어가 있어 필요 시 추출이 쉬우므로 .md로 변환하지 않고 원본만 보존한다.

대상 호스트는 --host로 지정한다(필수, 반복). 미러 소유 도메인만 넣어 외부 인용 PDF(arxiv·대학·정부 등)를 받지 않게 한다 -- 두 미러 공용 도구라 어느 미러의 도메인도 하드코딩하지 않는다.
증분·멱등: 기존 파일은 skip(--force로 재다운로드). HTML 에러페이지를 PDF로 오인 저장하지 않도록 %PDF- 매직바이트를 검증한다.
--max-mb(기본 100) 초과 PDF는 미러하지 않는다 -- GitHub 파일 하드 리밋이라, 받아두면 git push가 통째로 거부된다(소스 링크는 .md에 남는다).

Usage: pdf-mirror.py <out_dir> --host <substr> [--host <substr>]... [--force]
  anthropic: --host anthropic.com --host claude.com
  openai:    --host openai.com --host d2xo500swnpgl1.cloudfront.net --host openaiassets.blob.core.windows.net --host downloads.ctfassets.net
"""
import argparse
import os
import re
import urllib.request
from urllib.parse import urlsplit

PDF_RE = re.compile(r'https?://[^\s)"\'<>]+\.pdf(?:\?[^\s)"\'<>]*)?', re.I)


def scan(out, hosts):
    """미러 전체 .md에서 대상 호스트의 PDF URL 수집. (PDF는 .md가 아니라 재스캔되지 않는다.)"""
    urls = set()
    for root, _, files in os.walk(out):
        for fn in files:
            if not fn.endswith(".md"):
                continue
            try:
                with open(os.path.join(root, fn), encoding="utf-8") as f:
                    txt = f.read()
            except Exception:
                continue
            for u in PDF_RE.findall(txt):
                if any(h in urlsplit(u).netloc for h in hosts):
                    urls.add(u)
    return sorted(urls)


def dest(out, url):
    """URL 경로 = 파일 경로. 쿼리는 떼고 원본 확장자(.pdf) 유지."""
    sp = urlsplit(url)
    return os.path.join(out, sp.netloc, sp.path.lstrip("/"))


def _get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})  # CDN 기본 UA 차단 회피
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def fetch(url):
    try:
        return _get(url)
    except Exception:
        if url.startswith("http://"):  # 자산 CDN은 https 전용 -- http 링크는 https로 승격 재시도
            return _get("https://" + url[7:])
        raise


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--force", action="store_true", help="기존 파일도 다시 다운로드")
    ap.add_argument("--host", action="append", default=[], help="대상 호스트 substring(필수, 반복). 미러 소유 도메인만 -- 외부 인용 PDF 제외.")
    ap.add_argument("--max-mb", type=int, default=100, help="이 크기(MB) 초과 PDF는 미러 안 함(기본 100=GitHub 파일 하드 리밋). 0이면 무제한.")
    a = ap.parse_args()
    if not a.host:
        ap.error("--host 최소 1개 필요(미러 소유 도메인). 예: --host anthropic.com --host claude.com / --host openai.com")
    hosts = tuple(a.host)

    urls = scan(a.out, hosts)
    print(f"PDF 링크 {len(urls)}개 발견", flush=True)
    saved = skipped = failed = 0
    for u in urls:
        fp = dest(a.out, u)
        if os.path.exists(fp) and not a.force:
            skipped += 1
            continue
        try:
            data = fetch(u)
        except Exception as e:
            print(f"  FAIL {u} [{str(e)[:80]}]", flush=True)
            failed += 1
            continue
        if data[:5] != b"%PDF-":
            # 비-PDF 응답 = 업스트림이 자산을 회수(홈으로 redirect)했거나 에러페이지 -> 실패가 아니라 skip.
            # 저장하지 않으므로 매 실행 재확인되고, 자산이 복구되면 자동 수집된다.
            print(f"  SKIP(비-PDF 응답, 업스트림 회수/에러) {u}", flush=True)
            skipped += 1
            continue
        if a.max_mb and len(data) > a.max_mb * 1024 * 1024:  # GitHub 하드 리밋 초과 -> 미러 안 함(소스 링크만, git push 거부 방지)
            print(f"  SKIP(>{a.max_mb}MB, GitHub 리밋) {u}", flush=True)
            skipped += 1
            continue
        os.makedirs(os.path.dirname(fp), exist_ok=True)
        with open(fp, "wb") as f:
            f.write(data)
        saved += 1
        print(f"  saved {fp} ({len(data) // 1024}KB)", flush=True)
    print(f"저장 {saved} / skip {skipped} / 실패 {failed}", flush=True)


if __name__ == "__main__":
    main()
