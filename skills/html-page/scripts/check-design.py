#!/usr/bin/env python3
"""Check that a final html-page page follows the skill's design contract.

Run it: python3 check-design.py <file.html> [...]. Exit 0 when every file passes.
It reads the HTML as text and does not open a browser. publish runs it before
registering a page, so a page that fails here is never sent.
"""
import json
import re
import sys
from pathlib import Path

# Tokens every page must define, because the panel, completion colors and
# dark mode read them. They come from assets/design.css.
REQUIRED_TOKENS = ("--bg", "--paper", "--ink", "--muted", "--line", "--action", "--complete", "--pending")
# CDN scripts must name an exact version, otherwise a page that worked today
# breaks when the package publishes a new major.
UNPINNED_CDN = re.compile(r'<script[^>]+src="https?://[^"]*(?:@latest|/npm/[^@"/]+/|@\d+(?:\.\d+)?/)[^"]*"', re.I)
ANY_CDN = re.compile(r'<script[^>]+src="(https?://[^"]+)"', re.I)
PINNED = re.compile(r"@\d+\.\d+\.\d+")


def check(path):
    text = Path(path).read_text(encoding="utf-8")
    head = text[: text.lower().find("</head>")] if "</head>" in text.lower() else text
    errors = []
    if 'name="darkreader-lock"' not in head:
        errors.append('<meta name="darkreader-lock">가 없습니다. 확장이 색을 덮어쓰지 않게 head에 넣으세요.')
    if 'name="color-scheme"' not in head and "color-scheme:" not in text:
        errors.append('color-scheme 선언이 없습니다. <meta name="color-scheme" content="light dark"> 또는 :root { color-scheme }를 넣으세요.')
    if "prefers-color-scheme: dark" not in text:
        errors.append("다크 모드 블록(@media (prefers-color-scheme: dark))이 없습니다. assets/design.css 블록을 인라인하세요.")
    missing = [token for token in REQUIRED_TOKENS if not re.search(re.escape(token) + r"\s*:", text)]
    if missing:
        errors.append("디자인 토큰이 정의되지 않았습니다: " + ", ".join(missing) + ". assets/design.css 블록을 인라인하세요.")
    for src in ANY_CDN.findall(text):
        if not PINNED.search(src):
            errors.append(f"버전이 고정되지 않은 외부 스크립트: {src}. name@x.y.z 형식으로 고정하세요.")
    if re.search(r"(?m)^\s*architecture-beta\b", text):
        errors.append("Mermaid architecture-beta는 렌더가 불안정합니다. flowchart를 쓰세요.")
    return errors


def main(argv):
    if not argv or argv[0] in {"-h", "--help"}:
        print(__doc__.strip())
        return 0 if argv else 2
    result = {"ok": True, "files": {}}
    for path in argv:
        try:
            errors = check(path)
        except (OSError, UnicodeError) as exc:
            errors = [str(exc)]
        result["files"][path] = errors
        if errors:
            result["ok"] = False
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
