#!/usr/bin/env python3
"""context/ 소스 아카이브 현황 뷰어.

각 .md의 YAML frontmatter(없으면 파일명·본문 헤더에서 best-effort)를 읽어
소스별 수집 현황을 표로 출력한다. --source 로 특정 소스의 anchor(증분 기준점)만 조회.
표준 라이브러리만 사용 (의존성 0).

  python3 context_status.py [dir]            # 기본 ./context, 현황 표
  python3 context_status.py ./context --source slack   # slack anchor만 출력
"""
import argparse
import glob
import os
import re
import sys


def parse_frontmatter(text):
    """맨 위 --- ~ --- 블록을 flat key:value dict로. 없으면 None."""
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    meta = {}
    for line in text[3:end].splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        k, v = line.split(":", 1)
        meta[k.strip()] = v.strip().strip('"').strip("'")
    return meta


def fallback_meta(text, path):
    """frontmatter 없는 기존 아카이브: 파일명·본문 헤더에서 best-effort."""
    meta = {"_nometa": "1"}
    base = os.path.basename(path)
    m = re.match(r"\d{6}-([0-9a-zA-Z가-힣]+)-", base)
    if m:
        meta["source"] = m.group(1)
    mc = re.search(r"수집일[:：]\s*([0-9]{4}-[0-9]{2}-[0-9]{2})", text)
    if mc:
        meta["collected_last"] = mc.group(1)
    mf = re.search(r"초수집[:：]\s*([0-9]{4}-[0-9]{2}-[0-9]{2})", text)
    meta["collected_first"] = mf.group(1) if mf else meta.get("collected_last", "")
    mr = re.search(
        r"범위[:：]\s*([0-9]{4}-[0-9]{2}-[0-9]{2})\s*~\s*([0-9]{4}-[0-9]{2}-[0-9]{2})", text
    )
    if mr:
        meta["range_start"], meta["range_end"] = mr.group(1), mr.group(2)
    return meta


def load(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    meta = parse_frontmatter(text)
    if meta is None:
        meta = fallback_meta(text, path)
    meta.setdefault("source", "?")
    meta["_file"] = os.path.basename(path)
    return meta


def main():
    ap = argparse.ArgumentParser(description="context/ 아카이브 수집 현황 뷰어")
    ap.add_argument("dir", nargs="?", default="./context", help="아카이브 폴더 (기본 ./context)")
    ap.add_argument("--source", help="이 소스의 anchor(증분 기준점)만 출력")
    args = ap.parse_args()

    files = sorted(glob.glob(os.path.join(args.dir, "*.md")))
    if not files:
        print(f"(no .md in {args.dir})", file=sys.stderr)
        sys.exit(1)
    rows = [load(f) for f in files]

    # --source: 해당 소스의 anchor만 (가장 최근 수집본 기준). 재수집 증분에 사용.
    if args.source:
        cand = [r for r in rows if r.get("source") == args.source and r.get("anchor")]
        cand.sort(key=lambda r: r.get("collected_last", ""), reverse=True)
        print(cand[0]["anchor"] if cand else "")
        return

    for r in rows:
        rs, re_ = r.get("range_start", ""), r.get("range_end", "")
        r["_range"] = f"{rs} ~ {re_}" if (rs or re_) else ""

    cols = [
        ("SOURCE", "source", 10),
        ("FIRST", "collected_first", 11),
        ("LAST", "collected_last", 11),
        ("RANGE", "_range", 25),
        ("ITEMS", "items", 6),
        ("ANCHOR", "anchor", 22),
        ("FILE", "_file", 40),
    ]
    hdr = " ".join(name.ljust(w) for name, _, w in cols)
    print(hdr)
    print("-" * len(hdr))
    for r in sorted(rows, key=lambda r: (r.get("source", ""), r.get("_file", ""))):
        flag = "*" if r.get("_nometa") else " "
        line = " ".join(str(r.get(key, "") or "").ljust(w)[:w] for _, key, w in cols)
        print(flag + line)
    if any(r.get("_nometa") for r in rows):
        print("\n* = frontmatter 없음 (본문 best-effort). 다음 머지 때 frontmatter가 얹힘.")


if __name__ == "__main__":
    main()
