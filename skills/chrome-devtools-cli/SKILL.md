---
argument-hint: "[subcommand]"
name: chrome-devtools-cli
description: "Use for: Use terminal-driven headless Chrome for navigation, screenshots, DOM/JS, console/network inspection, CDP, Lighthouse, Core Web Vitals, and performance traces. App QA/screen flows: browse; URL-to-Markdown: crawl. Not for ordinary web research."
compatibility: Requires the chrome-devtools CLI and a local Chrome install.
metadata:
  requires:
    - tool: chrome-devtools
      check: command -v chrome-devtools
      install: pnpm add -g chrome-devtools-mcp@latest
---

# chrome-devtools CLI

## Overview

`chrome-devtools`는 `chrome-devtools-mcp` 패키지가 제공하는 **전역 CLI 바이너리**다. MCP 서버 대신 on-demand로 Bash에서 호출해 헤드리스 Chrome을 제어한다(컨텍스트 비용 0, 풀 기능, Google 공식 유지보수). MCP의 모든 도구가 그대로 서브커맨드로 노출된다.

**권장**: 같은 패키지를 MCP 서버로도 등록할 수 있지만 도구가 컨텍스트에 상주한다. 기본은 이 CLI를 on-demand로 호출하고, MCP 도구가 없어도 정상으로 본다.

설치 확인: `command -v chrome-devtools` (없으면 `pnpm add -g chrome-devtools-mcp@latest`).

## 데몬 모델 (먼저 이해할 것)

CLI는 백그라운드 데몬(MCP 서버)의 클라이언트다. 데몬이 브라우저를 들고 있고, **페이지·쿠키·로그인 상태가 호출 간 유지**된다.

```sh
chrome-devtools status     # 데몬 상태 확인
chrome-devtools start      # 명시 기동/재시작 (보통 불필요. 첫 명령에 자동 기동)
chrome-devtools stop       # 데몬 정지. 아래 동시 세션 절을 먼저 본다
```

- 첫 브라우저 명령(예: `new_page`)을 던지면 데몬이 자동 기동된다. `start`를 따로 부를 필요는 보통 없다.
- 기본 **headless**이고 고정 프로필 `~/.cache/chrome-devtools-mcp-cli/chrome-profile`을 쓴다. headed로 보거나 다른 프로필을 쓰려면 `chrome-devtools start --userDataDir <경로>` 등으로 띄운다. 정확한 플래그는 `chrome-devtools start --help` 참고.

## 동시 세션

데몬은 OS 사용자당 하나다(`status`의 socket이 `/tmp/chrome-devtools-mcp-<uid>.sock`). Claude, Codex 등 이 계정의 모든 세션이 같은 브라우저와 탭을 함께 쓴다.

- 페이지 대상 명령은 `pageId`가 필수다(기본값 `--pageIdRouting`). 대부분 첫 위치 인자로 받고, `evaluate_script`만 `--pageId <id>`로 받는다. `select_page`로 바꾼 "현재 탭"에 기대지 않는다. 그사이 다른 세션이 다른 탭을 고를 수 있다.
- 자기 탭의 id는 `new_page` 출력에서 이번에 연 주소로 찾는다. `list_pages`의 다른 탭은 다른 세션의 것일 수 있다.
- 다 쓰면 자기가 연 탭만 `close_page <pageId>`로 닫는다. `stop`과 플래그를 바꾼 `start`는 데몬을 다시 띄워 다른 세션의 탭까지 닫으므로, `list_pages`에 자기 탭만 있을 때만 쓴다.
- 쿠키와 저장소를 다른 탭과 나누지 않으려면 `new_page <url> --isolatedContext <이름>`으로 연다.
- 페이지 명령이 `The browser is already running for <프로필>`로 실패하면 다른 chrome-devtools-mcp(다른 세션의 MCP 서버나 남은 옛 데몬)가 그 프로필을 잡고 있다. `ps -axo pid,ppid,lstart,command | grep chrome-devtools-mcp`로 주인과 시작 시각을 확인해 사용자에게 알리고, 그 프로세스를 직접 끄지 않는다. 오류 문구가 권하는 `--isolated`(임시 프로필)로 데몬을 다시 띄우는 것도 공유 데몬을 바꾸는 일이라 위 `stop` 기준을 따른다. 브라우저 한 번이면 되는 확인은 임시 `--user-data-dir`로 headless Chrome을 따로 띄워 데몬을 거치지 않는다.

## 핵심 상호작용 모델: uid 기반

요소를 CSS 셀렉터가 아니라 **uid**로 가리킨다. `take_snapshot`으로 a11y 트리 + 각 요소의 uid를 받고, 그 uid로 click/fill/hover 한다. 스크린샷보다 snapshot을 우선(텍스트라 토큰 효율적이고 uid를 줌).

```sh
chrome-devtools take_snapshot <pageId>              # 페이지 요소 + uid 목록
chrome-devtools click <pageId> <uid>                # uid로 클릭
chrome-devtools fill <pageId> <uid> "입력값"        # input/textarea/select 입력
# 상호작용 후 바뀐 DOM이 필요하면 --includeSnapshot 로 한 번에 받는다
chrome-devtools click <pageId> <uid> --includeSnapshot
```

## 자주 쓰는 워크플로우

**페이지 열기/이동**
```sh
chrome-devtools new_page "https://example.com" --background   # 새 탭 + 로드. 출력에서 이 주소의 id를 쓴다
chrome-devtools navigate_page <pageId> --url "https://..."    # 탭 이동 (--type back|forward|reload 도 가능)
chrome-devtools list_pages                                     # 열린 탭 목록. 다른 세션의 탭도 보인다
chrome-devtools close_page <pageId>                            # 자기가 연 탭 닫기
```

**스크린샷 / JS 평가**
```sh
chrome-devtools take_screenshot <pageId> --filePath out.png [--fullPage] [--uid <uid>]
chrome-devtools evaluate_script "() => ({ title: document.title })" --pageId <pageId>   # JSON 직렬화 가능 값만 반환
```

**콘솔 / 네트워크 검사**
```sh
chrome-devtools list_console_messages <pageId> [--types error,warning]
chrome-devtools list_network_requests <pageId> [--resourceTypes fetch,xhr]
chrome-devtools get_network_request <pageId> --reqid <id>     # 단일 요청 상세
```

**Lighthouse 감사** (cdp-cli엔 없는 핵심 기능 — 접근성/SEO/Best Practices/Agentic Browsing)
```sh
chrome-devtools lighthouse_audit <pageId> --mode snapshot [--device mobile]
# 성능(perf)은 lighthouse에 포함 안 됨 → 아래 트레이스 사용
```

**성능 트레이스** (Core Web Vitals: LCP/INP/CLS, 로드 속도)
```sh
chrome-devtools performance_start_trace <pageId> --reload --autoStop   # 페이지 리로드하며 측정
chrome-devtools performance_stop_trace <pageId>                        # 수동 종료 시
chrome-devtools performance_analyze_insight <pageId> <insightSetId> <insightName>   # 개별 인사이트 상세
```

## 출력 파싱

기본은 사람용 출력. 스크립트/jq로 파싱하려면 `--output-format=json`.
```sh
chrome-devtools list_pages --output-format=json | jq -r '.pages[] | select(.url == "<연 주소>") | .id'
```

## 실험적/카테고리 기능

일부 커맨드(메모리·좌표 클릭·화면 녹화·확장프로그램 등)는 데몬 기동 시 플래그가 필요하다 — 도움말에 `(requires flag: ...)`로 표기된다. 플래그는 글로벌 설정이라 `chrome-devtools start <플래그>`로 데몬을 띄운 뒤 해당 커맨드를 쓴다. 다시 띄우면 다른 세션의 탭도 닫히므로 동시 세션 절의 `stop` 기준을 따른다. 커맨드↔플래그 전체 매핑은 `references/commands.md`, 설치본 기준은 `chrome-devtools <command> --help`.

## 전체 커맨드 레퍼런스

모든 서브커맨드와 인자는 `references/commands.md` 참고. 설치본 기준은 언제든 `chrome-devtools --help` 또는 `chrome-devtools <command> --help`로 확인.

## 마무리 체크

- 자기가 연 탭을 `close_page <pageId>`로 닫는다. `chrome-devtools stop`은 `list_pages`에 자기 탭만 남았을 때만 (동시 세션 절)
- 임시 스크린샷/리포트 파일 정리
