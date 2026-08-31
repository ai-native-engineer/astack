#!/bin/bash
# html-explainer 생성물 헤드리스 렌더 검증
# usage: verify.sh <file.html>
# 확인: 콘솔 에러, Mermaid SVG 렌더, ECharts 캔버스, Iconify 아이콘, 전체 스크린샷
set -euo pipefail

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

shot="/tmp/$(basename "${f%.html}")-verify.png"
select_target
chrome-devtools take_screenshot --fullPage --filePath "$shot" >/dev/null 2>&1
echo
echo "== 스크린샷 (Read로 열어 겹침·잘림 육안 확인) =="
echo "$shot"

# CLI는 탭이 아니라 자동화 Chrome 프로세스 자체를 띄운다. 검증이 끝나면 프로세스를 내린다.
chrome-devtools stop >/dev/null 2>&1 || true
