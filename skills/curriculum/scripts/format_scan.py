#!/usr/bin/env python3
"""교안 형식 스캐너: 본문 덩어리는 '순수 불렛 목록' 또는 '독립 줄글 1~2줄'만 허용.

규칙 (사용자 확정):
- 같은 run(구분자 사이 연속 구간)에 줄글과 불렛이 섞이면 위반 (리드문+불렛 하이브리드 포함)
- 줄글만 있는 run이 3줄 이상이면 위반
- 콜아웃 내부에도 동일 적용. 표/이미지/코드펜스/헤딩/북마크는 run 구분자
- 빈 줄은 투명(run을 끊지 않음. 노션 렌더링에는 빈 줄이 없음)

usage: python3 format_scan.py <draft.md> [...]  (위반 있으면 exit 1)
"""
import argparse
import re
import sys

SEP = re.compile(r"[#|<!>]|\[\[bookmark|```|---$|!\[")
BULLET = re.compile(r"(- |\d+\. )")

def classify(line):
    s = line.strip()
    if not s: return "blank"
    if s.startswith("```"): return "fence"
    if BULLET.match(s): return "b"
    if SEP.match(s): return "sep"
    return "p"

def scan(path):
    lines = open(path, encoding="utf-8").read().splitlines()
    in_code = False
    runs, cur = [], []  # cur: list of (lineno, kind)
    for i, ln in enumerate(lines, 1):
        k = classify(ln)
        if k == "fence": in_code = not in_code; k = "sep"
        elif in_code: continue
        if k == "blank": continue
        if k == "sep":
            if cur: runs.append(cur); cur = []
        else:
            cur.append((i, k))
    if cur: runs.append(cur)
    bad = []
    for run in runs:
        kinds = {k for _, k in run}
        first = run[0][0]
        if kinds == {"p", "b"}:
            bad.append((first, f"줄글+불렛 혼합 run ({len(run)}줄)"))
        elif kinds == {"p"} and len(run) >= 3:
            bad.append((first, f"줄글 {len(run)}줄 연속 (허용 1~2줄)"))
    return bad


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("drafts", nargs="+", help="검사할 교안 .md")
    args = ap.parse_args(argv)

    total = 0
    for path in args.drafts:
        try:
            bad = scan(path)
        except (FileNotFoundError, IsADirectoryError, UnicodeDecodeError, PermissionError) as e:
            print(f"입력 파일 오류: {path}: {e}", file=sys.stderr)
            return 2
        for ln, msg in bad:
            print(f"{path}:{ln}  {msg}")
        total += len(bad)
    print(f"위반 {total}건")
    return 1 if total else 0


if __name__ == "__main__":
    raise SystemExit(main())
