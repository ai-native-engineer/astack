#!/bin/bash
# html-explainer 생성물 헤드리스 렌더 검증
# usage: verify.sh <file.html>
# 확인: 콘솔 에러, Mermaid SVG 렌더, ECharts 캔버스, Iconify 아이콘, 전체 스크린샷
set -euo pipefail

f="${1:?usage: verify.sh <file.html>}"
f="$(cd "$(dirname "$f")" && pwd)/$(basename "$f")"
[ -f "$f" ] || { echo "파일 없음: $f"; exit 1; }

command -v chrome-devtools >/dev/null || { echo "chrome-devtools CLI 없음 — chrome-devtools-cli 스킬 참조"; exit 1; }
chrome-devtools status >/dev/null 2>&1 || chrome-devtools start >/dev/null 2>&1

chrome-devtools navigate_page url "file://$f" >/dev/null
sleep 5

echo "== 콘솔 메시지 (에러가 있으면 아래에 표시됨) =="
chrome-devtools list_console_messages 2>/dev/null | grep -v '^Update available' | grep -v '^Run `npm install' || true

echo
echo "== 렌더 체크 =="
chrome-devtools evaluate_script "() => ({
  mermaid_svg: !!document.querySelector('.diagram svg'),
  mermaid_error: document.querySelector('.diagram .err')?.textContent?.slice(0, 200) || null,
  echarts_canvas: document.querySelectorAll('.chart canvas').length,
  iconify_total: document.querySelectorAll('iconify-icon').length,
  iconify_rendered: [...document.querySelectorAll('iconify-icon')].filter(i => i.shadowRoot?.querySelector('svg')).length
})" 2>/dev/null | grep -v '^Update available' | grep -v '^Run `npm install'

# 등장 애니메이션(Motion)의 초기 opacity:0 상태를 해제 — 풀페이지 스크린샷이 빈 섹션으로 찍히는 것 방지
chrome-devtools evaluate_script "() => { document.querySelectorAll('.wrap > *').forEach(el => { el.style.opacity = ''; el.style.transform = ''; }); return true; }" >/dev/null 2>&1

shot="/tmp/$(basename "${f%.html}")-verify.png"
chrome-devtools take_screenshot --fullPage --filePath "$shot" >/dev/null 2>&1
echo
echo "== 스크린샷 (Read로 열어 겹침·잘림 육안 확인) =="
echo "$shot"
