# chrome-devtools CLI 커맨드 맵

**권위 소스는 항상 `chrome-devtools --help` / `chrome-devtools <command> --help`.** 아래는 어떤 작업에 어떤 커맨드가 있고 무엇이 플래그를 요구하는지 빠르게 훑기 위한 **비권위 스냅샷**이다 — 플래그 상세는 버전에 따라 바뀌니 신뢰하지 말고 `--help`로 확인한다. `--output-format=json`은 모든 커맨드에 붙일 수 있다.

## 데몬 관리

| 커맨드 | 설명 |
|---|---|
| `start [플래그]` | 데몬 기동/재시작. `--headless`, `--userDataDir`, `--experimental*`, `--category*` 등 글로벌 설정 플래그를 여기에 전달 |
| `status` | 데몬 실행 여부 + pid/socket/version 출력 |
| `stop` | 데몬 정지 |

## 페이지 / 네비게이션

| 커맨드 | 설명 |
|---|---|
| `new_page <url> [--background] [--isolatedContext] [--timeout]` | 새 탭 열고 URL 로드 |
| `navigate_page [--url] [--type back\|forward\|reload] [--ignoreCache] [--handleBeforeUnload] [--initScript] [--timeout]` | 현재 탭 이동/뒤로/앞으로/리로드 |
| `list_pages` | 열린 탭 목록 + 선택 상태 |
| `select_page <pageId> [--bringToFront]` | 이후 명령의 대상 탭 전환 |
| `close_page <pageId>` | 탭 닫기 (마지막 탭은 못 닫음) |
| `resize_page <width> <height>` | 창 크기 조정 |

## 상호작용 (uid 기반 — take_snapshot으로 uid 획득)

| 커맨드 | 설명 |
|---|---|
| `take_snapshot [--verbose] [--filePath]` | a11y 트리 기반 텍스트 스냅샷 + 각 요소 uid. **스크린샷보다 우선** |
| `click <uid> [--dblClick] [--includeSnapshot]` | uid 요소 클릭 |
| `click_at <x> <y> [--dblClick]` | 좌표 클릭 (`--experimentalVision=true` 필요) |
| `fill <uid> <value> [--includeSnapshot]` | input/textarea 입력, select 옵션 선택 |
| `hover <uid> [--includeSnapshot]` | 호버 |
| `drag <from_uid> <to_uid> [--includeSnapshot]` | 드래그앤드롭 |
| `type_text <text> [--submitKey]` | 포커스된 입력에 키보드 타이핑 |
| `press_key <key> [--includeSnapshot]` | 키/조합키 입력 (단축키·특수키) |
| `upload_file <uid> <filePath> [--includeSnapshot]` | 파일 업로드 |
| `handle_dialog <action> [--promptText]` | alert/confirm/prompt 다이얼로그 처리 |

## 검사 / 평가

| 커맨드 | 설명 |
|---|---|
| `evaluate_script <function> [--args] [--filePath] [--dialogAction]` | JS 함수 평가. JSON 직렬화 가능 값만 반환 |
| `take_screenshot [--format] [--quality] [--uid] [--fullPage] [--filePath]` | 페이지/요소 스크린샷 |
| `list_console_messages [--types] [--pageSize] [--pageIdx] [--includePreservedMessages]` | 콘솔 메시지 목록 |
| `get_console_message <msgid>` | 콘솔 메시지 단건 |
| `list_network_requests [--resourceTypes] [--pageSize] [--pageIdx] [--includePreservedRequests]` | 네트워크 요청 목록 |
| `get_network_request [--reqid] [--requestFilePath] [--responseFilePath]` | 네트워크 요청 단건 상세 |

## 에뮬레이션

| 커맨드 | 설명 |
|---|---|
| `emulate [--networkConditions] [--cpuThrottlingRate] [--geolocation] [--userAgent] [--colorScheme] [--viewport] [--extraHttpHeaders]` | 네트워크/CPU 스로틀, 위치, UA, 다크모드, 뷰포트 등 에뮬레이션 |

## 감사 / 성능

| 커맨드 | 설명 |
|---|---|
| `lighthouse_audit [--mode snapshot] [--device mobile\|desktop] [--outputDirPath]` | Lighthouse(접근성/SEO/Best Practices/Agentic Browsing). **성능은 제외** → 트레이스 사용 |
| `performance_start_trace [--reload] [--autoStop] [--filePath]` | 성능 트레이스 시작. Core Web Vitals(LCP/INP/CLS), 로드 속도 |
| `performance_stop_trace [--filePath]` | 트레이스 종료 |
| `performance_analyze_insight <insightSetId> <insightName>` | 특정 인사이트 상세 분석 |

## 메모리 (`--experimentalMemory=true` 필요)

| 커맨드 | 설명 |
|---|---|
| `take_heapsnapshot <filePath>` | 힙 스냅샷 캡처 (메모리 누수 분석) |
| `get_heapsnapshot_summary <filePath>` | 스냅샷 요약 통계 |
| `get_heapsnapshot_details <filePath> [--pageIdx] [--pageSize]` | 전체 정보 + 집계 (페이지네이션) |
| `get_heapsnapshot_class_nodes <filePath> <id> [--pageIdx] [--pageSize]` | 특정 클래스 인스턴스 |
| `get_heapsnapshot_retainers <filePath> <nodeId> [--pageIdx] [--pageSize]` | 특정 노드 retainer |

## 기타 실험적 / 카테고리 기능

| 커맨드 | 필요 플래그 |
|---|---|
| `screencast_start [--filePath]` / `screencast_stop` | `--experimentalScreencast=true` |
| `install_extension` / `list_extensions` / `reload_extension` / `trigger_extension_action` / `uninstall_extension` | `--categoryExtensions=true` |
| `execute_3p_developer_tool` / `list_3p_developer_tools` | `--categoryExperimentalThirdParty=true` |
| `execute_webmcp_tool` / `list_webmcp_tools` | `--categoryExperimentalWebmcp=true` |

## 참고

- `(requires flag: ...)` 표시된 커맨드는 그 플래그로 **데몬을 기동**해야 한다: `chrome-devtools start --experimentalMemory=true` 후 해당 커맨드 실행.
- `--includeSnapshot`은 상호작용 직후 갱신된 페이지 스냅샷을 함께 받아 왕복을 줄인다.
