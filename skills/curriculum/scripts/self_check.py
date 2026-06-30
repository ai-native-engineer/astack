#!/usr/bin/env python3
"""curriculum scripts self-check.

실행 목적: 게이트 스크립트의 핵심 실패 모드가 회귀하지 않았는지 확인한다.
"""
import os
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(__file__)
GATE = os.path.join(ROOT, "curriculum_gate.py")
REFLECT = os.path.join(ROOT, "notion_reflect.py")


def write(path, text):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def run(*args):
    return subprocess.run([sys.executable, *args], text=True, capture_output=True)


def expect(label, rc, *args):
    p = run(*args)
    if p.returncode != rc:
        print(f"FAIL {label}: expected rc={rc}, got {p.returncode}")
        print((p.stdout + p.stderr)[-1200:])
        return False
    print(f"OK {label}")
    return True


def main():
    ok = True
    with tempfile.TemporaryDirectory() as td:
        empty = os.path.join(td, "empty.md")
        orig = os.path.join(td, "orig.md")
        prod_missing = os.path.join(td, "prod-missing.md")
        prod_ok = os.path.join(td, "prod-ok.md")
        bad = os.path.join(td, "bad.md")
        good = os.path.join(td, "good.md")
        report = os.path.join(td, "report.md")
        cand_unchecked = os.path.join(td, "curriculum-candidates-unchecked.md")
        cand_blank = os.path.join(td, "curriculum-candidates-blank.md")
        cand_ok = os.path.join(td, "curriculum-candidates-ok.md")

        write(empty, "# text only\n")
        write(orig, "![a](file:///asset/a.png)\n")
        write(prod_missing, "# output\n")
        write(prod_ok, "![a](file:///asset/a.png)\n")
        write(bad, "# 1. 결과 화면\n설명만 있습니다.\n")
        write(good, "# 1. 실습\n아래 프롬프트를 복사합니다.\n\n```text\nhello\n```\n")
        write(report, "# 검수\n\nreview-draft before -> after: 고신호 1 -> 0\n")
        write(cand_unchecked, "# Curriculum 딥 탐색 후보\n\n> 게이트 상태: **OK**\n\n- [ ] 원본 A - id `a` | 근거: \n\n최선 후보: 원본 A\n")
        write(cand_blank, "# Curriculum 딥 탐색 후보\n\n> 게이트 상태: **OK**\n\n- [x] 원본 A - id `a` | 근거: \n\n최선 후보: 원본 A\n")
        write(cand_ok, "# Curriculum 딥 탐색 후보\n\n> 게이트 상태: **OK**\n\n- [x] 원본 A - id `a` | 근거: 프롬프트 3개와 결과 이미지 확인\n\n최선 후보: 원본 A\n")

        ok &= expect("verify-media rejects zero-media source", 1, GATE, "verify-media", empty, empty)
        ok &= expect("verify-media catches missing ref", 1, GATE, "verify-media", orig, prod_missing)
        ok &= expect("verify-media accepts preserved ref", 0, GATE, "verify-media", orig, prod_ok)
        ok &= expect("gate-candidates rejects unchecked source", 1, GATE, "gate-candidates", cand_unchecked)
        ok &= expect("gate-candidates rejects blank evidence", 1, GATE, "gate-candidates", cand_blank)
        ok &= expect("gate-candidates accepts checked evidence", 0, GATE, "gate-candidates", cand_ok)
        ok &= expect("review-draft catches weak draft", 1, GATE, "review-draft", bad)
        ok &= expect("review-draft accepts signal draft", 0, GATE, "review-draft", good)
        ok &= expect("gate-review accepts report plus clean draft", 0, GATE, "gate-review", "--report", report, good)
        ok &= expect("gate-review accepts candidates plus report", 0, GATE, "gate-review", "--candidates", cand_ok, "--report", report, good)
        ok &= expect("notion_reflect requires report before env/ntn", 2, REFLECT, "page-id", good)

    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
