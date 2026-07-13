---
argument-hint: "[subcommand]"
name: chrome-devtools-cli
description: chrome-devtools CLI(chrome-devtools-mcp 패키지의 standalone CLI 모드)로 헤드리스 Chrome을 제어 — 페이지 이동, 클릭/입력, 스크린샷, 콘솔/네트워크 검사, JS 평가, Lighthouse 감사, 성능 트레이스(Core Web Vitals LCP/INP/CLS), 힙 스냅샷. Use when user says 'chrome-devtools', '브라우저 자동화', '헤드리스 브라우저', '스크린샷 찍어', 'Lighthouse', '성능 감사', '페이지 성능', 'Core Web Vitals', '콘솔 로그 확인', '네트워크 요청 확인', '웹페이지 클릭/입력 자동화', 'CDP', or needs CDP-level browser control from the terminal. chrome-devtools는 MCP 서버가 아니라 이 전역 CLI로 쓴다(MCP 재등록 금지). Do NOT use for 단순 URL/사이트의 마크다운 변환(crawl), React/Next E2E 테스트 코드 작성, or 브라우저 제어가 불필요한 일반 웹 리서치.
---

# chrome-devtools CLI

## Overview

`chrome-devtools`는 `chrome-devtools-mcp` 패키지가 제공하는 **전역 CLI 바이너리**다. MCP 서버 대신 on-demand로 Bash에서 호출해 헤드리스 Chrome을 제어한다(컨텍스트 비용 0, 풀 기능, Google 공식 유지보수). MCP의 모든 도구가 그대로 서브커맨드로 노출된다.

**권장**: 같은 패키지를 MCP 서버로도 등록할 수 있지만(도구 ~40개가 컨텍스트에 상주), 컨텍스트 절약을 위해 MCP 등록은 빼고 이 CLI로만 on-demand 호출하는 구성을 권장한다. `mcp__chrome-devtools__*` 도구가 안 보여도 정상이다.

설치 확인: `which chrome-devtools` (없으면 `pnpm add -g chrome-devtools-mcp@latest`).

## 데몬 모델 (먼저 이해할 것)

CLI는 백그라운드 데몬(MCP 서버)의 클라이언트다. 데몬이 브라우저를 들고 있고, **페이지·쿠키·로그인 상태가 호출 간 유지**된다.

```sh
chrome-devtools status     # 데몬 상태 확인
chrome-devtools start      # 명시 기동/재시작 (보통 불필요 — 첫 명령에 자동 기동)
chrome-devtools stop       # 작업 끝나면 정지 (잔여 프로세스 정리)
```

- 첫 브라우저 명령(예: `new_page`)을 던지면 데몬이 자동 기동된다. `start`를 따로 부를 필요는 보통 없다.
- 기본 **headless**. headed로 보거나 영속 프로필을 쓰려면 데몬을 직접 띄운다: `chrome-devtools start --userDataDir <경로>` 등. 정확한 플래그는 `chrome-devtools start --help` 참고.
- 작업이 끝나면 `chrome-devtools stop`으로 데몬을 내려 clean state 유지.

## 핵심 상호작용 모델: uid 기반

요소를 CSS 셀렉터가 아니라 **uid**로 가리킨다. `take_snapshot`으로 a11y 트리 + 각 요소의 uid를 받고, 그 uid로 click/fill/hover 한다. 스크린샷보다 snapshot을 우선(텍스트라 토큰 효율적이고 uid를 줌).

```sh
chrome-devtools take_snapshot              # 페이지 요소 + uid 목록
chrome-devtools click <uid>                # uid로 클릭
chrome-devtools fill <uid> "입력값"        # input/textarea/select 입력
# 상호작용 후 바뀐 DOM이 필요하면 --includeSnapshot 로 한 번에 받는다
chrome-devtools click <uid> --includeSnapshot
```

## 자주 쓰는 워크플로우

**페이지 열기/이동**
```sh
chrome-devtools new_page "https://example.com"     # 새 탭 + 로드
chrome-devtools navigate_page --url "https://..."  # 현재 탭 이동 (--type back|forward|reload 도 가능)
chrome-devtools list_pages                          # 열린 탭 목록 + 선택 상태
chrome-devtools select_page <pageId>                # 대상 탭 전환
```

**스크린샷 / JS 평가**
```sh
chrome-devtools take_screenshot --filePath out.png [--fullPage] [--uid <uid>]
chrome-devtools evaluate_script "() => ({ title: document.title })"   # JSON 직렬화 가능 값만 반환
```

**콘솔 / 네트워크 검사**
```sh
chrome-devtools list_console_messages [--types error,warning]
chrome-devtools list_network_requests [--resourceTypes fetch,xhr]
chrome-devtools get_network_request --reqid <id>     # 단일 요청 상세
```

**Lighthouse 감사** (cdp-cli엔 없는 핵심 기능 — 접근성/SEO/Best Practices/Agentic Browsing)
```sh
chrome-devtools lighthouse_audit --mode snapshot [--device mobile]
# 성능(perf)은 lighthouse에 포함 안 됨 → 아래 트레이스 사용
```

**성능 트레이스** (Core Web Vitals: LCP/INP/CLS, 로드 속도)
```sh
chrome-devtools performance_start_trace --reload --autoStop   # 페이지 리로드하며 측정
chrome-devtools performance_stop_trace                        # 수동 종료 시
chrome-devtools performance_analyze_insight <insightSetId> <insightName>   # 개별 인사이트 상세
```

## 출력 파싱

기본은 사람용 출력. 스크립트/jq로 파싱하려면 `--output-format=json`.
```sh
chrome-devtools list_pages --output-format=json | jq '.pages[] | select(.selected)'
```

## 실험적/카테고리 기능

일부 커맨드(메모리·좌표 클릭·화면 녹화·확장프로그램 등)는 데몬 기동 시 플래그가 필요하다 — 도움말에 `(requires flag: ...)`로 표기된다. 플래그는 글로벌 설정이라 `chrome-devtools start <플래그>`로 데몬을 띄운 뒤 해당 커맨드를 쓴다. 커맨드↔플래그 전체 매핑은 `references/commands.md`, 설치본 기준은 `chrome-devtools <command> --help`.

## 전체 커맨드 레퍼런스

모든 서브커맨드와 인자는 `references/commands.md` 참고. 설치본 기준은 언제든 `chrome-devtools --help` 또는 `chrome-devtools <command> --help`로 확인.

## 마무리 체크

- 작업 종료 시 `chrome-devtools stop` (데몬 정리)
- 임시 스크린샷/리포트 파일 정리
