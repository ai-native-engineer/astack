#!/bin/bash
# html-explainer 생성물 헤드리스 렌더 검증
# usage: verify.sh <file.html> | verify.sh --syntax <file.html>
# 확인: 콘솔 에러, Mermaid SVG 렌더, ECharts 캔버스, Iconify 아이콘, 전체 스크린샷
set -euo pipefail

if [ "${1:-}" = "--help" ] || [ "${1:-}" = "-h" ]; then
  echo "usage: verify.sh <file.html>                 # CDP render checks (explicit request only)"
  echo "       verify.sh --syntax <file.html>        # inline JavaScript syntax only; Python 3 + Node.js"
  exit 0
fi

if [ "${1:-}" = "--syntax" ]; then
  shift
  exec python3 - "$@" <<'PY'
import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from html.parser import HTMLParser
from pathlib import Path

class Scripts(HTMLParser):
    def __init__(self):
        super().__init__()
        self.scripts, self.active, self.unchecked = [], None, 0
    def handle_starttag(self, tag, attrs):
        if tag != "script":
            return
        attrs = dict(attrs)
        kind = (attrs.get("type") or "").strip().lower()
        self.active = None
        if kind in ("application/json", "application/ld+json"):
            return
        if "src" in attrs or kind not in ("", "text/javascript", "application/javascript", "module"):
            self.unchecked += 1
            return
        self.active = {"line": self.getpos()[0], "module": kind == "module", "parts": []}
        self.scripts.append(self.active)
    def handle_data(self, data):
        if self.active is not None:
            self.active["parts"].append(data)
    def handle_endtag(self, tag):
        if tag == "script":
            self.active = None

parser = argparse.ArgumentParser(description="Check final HTML inline JavaScript without running it or opening a browser.")
parser.add_argument("html_file", type=Path)
args = parser.parse_args()
result = {"ok": False, "scope": "inline-javascript-syntax", "runtime": "not-checked", "checked": 0, "errors": []}
code = 2
try:
    node = shutil.which("node")
    if not node:
        raise ValueError("Node.js is required; use an installed node or report syntax as unverified.")
    page = Scripts()
    page.feed(args.html_file.read_text(encoding="utf-8"))
    page.close()
    if not page.scripts or page.unchecked:
        raise ValueError("Inline JavaScript is missing or script dependencies/types remain unchecked; verify with the matching browser workflow.")
    with tempfile.TemporaryDirectory(prefix="html-inline-js-") as folder:
        for index, script in enumerate(page.scripts, 1):
            file = Path(folder) / (str(index) + (".mjs" if script["module"] else ".js"))
            file.write_text("".join(script["parts"]), encoding="utf-8")
            run = subprocess.run([node, "--check", str(file)], capture_output=True, text=True, check=False)
            result["checked"] += 1
            if run.returncode:
                # Report the error category, not source lines that may contain private values.
                error = next((line for line in run.stderr.splitlines() if line.startswith("SyntaxError:")), "Node.js syntax check failed")
                result["errors"].append({"script": index, "htmlLine": script["line"], "message": error})
    result["ok"] = not result["errors"]
    code = 0 if result["ok"] else 1
except (OSError, UnicodeError, ValueError) as exc:
    result["errors"].append({"message": str(exc)})
print(json.dumps(result, ensure_ascii=False))
sys.exit(code)
PY
fi

f="${1:?usage: verify.sh <file.html>}"
f="$(cd "$(dirname "$f")" && pwd)/$(basename "$f")"
[ -f "$f" ] || { echo "파일 없음: $f"; exit 1; }
url="file://$f"

command -v chrome-devtools >/dev/null || { echo "chrome-devtools CLI 없음 — chrome-devtools-cli 스킬 참조"; exit 1; }
chrome-devtools status >/dev/null 2>&1 || chrome-devtools start >/dev/null 2>&1

# 데몬은 여러 세션이 공유한다. 다른 세션이 선택한 페이지를 navigate로 덮지 말고
# 이 URL의 페이지를 따로 잡아 쓰고, 호출 직전마다 다시 선택한다 —
# 선택을 뺏긴 채 평가·촬영하면 남의 페이지 결과가 통과로 보고된다.
page_id() { chrome-devtools list_pages 2>/dev/null | grep -F "($url)" | tail -1 | cut -d: -f1 | tr -d ' '; }
select_target() {
  local pid
  pid="$(page_id)"
  [ -n "$pid" ] || { echo "대상 페이지를 찾지 못함: $url"; exit 1; }
  chrome-devtools select_page "$pid" >/dev/null 2>&1
}

if [ -n "$(page_id)" ]; then
  select_target
  chrome-devtools navigate_page reload >/dev/null 2>&1
else
  chrome-devtools new_page "$url" >/dev/null 2>&1
fi
sleep 5
select_target

echo "== 콘솔 메시지 (에러가 있으면 아래에 표시됨) =="
chrome-devtools list_console_messages 2>/dev/null | grep -v '^Update available' | grep -v '^Run `npm install' || true

echo
echo "== 렌더 체크 (href가 대상 파일과 다르면 결과를 믿지 말고 재실행) =="
select_target
chrome-devtools evaluate_script "() => ({
  href: location.href,
  mermaid_svg: !!document.querySelector('.diagram svg'),
  mermaid_error: document.querySelector('.diagram .err')?.textContent?.slice(0, 200) || null,
  echarts_canvas: document.querySelectorAll('.chart canvas').length,
  iconify_total: document.querySelectorAll('iconify-icon').length,
  iconify_rendered: [...document.querySelectorAll('iconify-icon')].filter(i => i.shadowRoot?.querySelector('svg')).length
})" 2>/dev/null | grep -v '^Update available' | grep -v '^Run `npm install'

# 등장 애니메이션(Motion)의 초기 opacity:0 상태를 해제 — 풀페이지 스크린샷이 빈 섹션으로 찍히는 것 방지
select_target
chrome-devtools evaluate_script "() => { document.querySelectorAll('.wrap > *').forEach(el => { el.style.opacity = ''; el.style.transform = ''; }); return true; }" >/dev/null 2>&1

shot="${TMPDIR:-/tmp}/$(basename "${f%.html}")-verify.png"
select_target
chrome-devtools take_screenshot --fullPage --filePath "$shot" >/dev/null 2>&1
echo
echo "== 스크린샷 (Read로 열어 겹침·잘림 육안 확인) =="
echo "$shot"

# CLI는 탭이 아니라 자동화 Chrome 프로세스 자체를 띄운다. 검증이 끝나면 프로세스를 내린다.
chrome-devtools stop >/dev/null 2>&1 || true
