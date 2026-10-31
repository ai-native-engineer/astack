#!/usr/bin/env python3
"""check-design.py 회귀 검사: 템플릿은 통과하고, 계약을 하나씩 깨면 그 항목으로 실패한다."""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
CHECK = SKILL / "scripts" / "check-design.py"


def run(path):
    result = subprocess.run([sys.executable, "-I", str(CHECK), str(path)], capture_output=True, text=True, check=False)
    return result.returncode, json.loads(result.stdout)["files"][str(path)]


def demo():
    for name in ("template.html", "review-template.html"):
        code, errors = run(SKILL / "assets" / name)
        assert code == 0 and not errors, (name, errors)
    source = (SKILL / "assets" / "template.html").read_text(encoding="utf-8")
    cases = {
        "darkreader": (source.replace('<meta name="darkreader-lock">', ""), "darkreader-lock"),
        "tokens": (source.replace("--action:", "--acton:"), "--action"),
        "unpinned": (source.replace("echarts@6.0.0/", "echarts@6/"), "고정되지 않은"),
        "mermaid": (source.replace("<body", "<pre class=\"mermaid\">\narchitecture-beta\n</pre><body", 1), "architecture-beta"),
        "dark": (source.replace("prefers-color-scheme: dark", "prefers-color-scheme: light"), "다크 모드"),
    }
    with tempfile.TemporaryDirectory(prefix="check-design-") as folder:
        for name, (text, needle) in cases.items():
            page = Path(folder) / f"{name}.html"
            page.write_text(text, encoding="utf-8")
            code, errors = run(page)
            assert code == 1 and any(needle in e for e in errors), (name, errors)
    print("ok: check-design")


if __name__ == "__main__":
    demo()
