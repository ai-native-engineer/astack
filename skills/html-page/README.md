# HTML Page

로컬에서 바로 열 수 있는 단일 HTML 페이지를 만들고 원래 대화의 Herdr 패널로 회신받는 shared skill이다. 실행 지침의 정본은 `SKILL.md`와 `references/`이며, 이 문서는 유지보수자를 위한 구조와 출처만 설명한다.

## 구조

- `SKILL.md`: 사용자 반응을 근거로 구조 선택, 생성, 회신 연결, 사용자 브라우저 검증
- `references/`: 타입별 스택과 작성 규칙, 타입 공통 마감 규칙(`ui-polish.md`)
- `references/reference-selection.md`: 피드백 범위와 사례 선택 기준
- `references/reply-delivery.md`: 세션 연결, 저장과 전달 상태, 복구 절차
- `assets/template.html`: Mermaid/ECharts 시각형의 선택 가능한 시작점
- `assets/interactive-template.html`: 순서대로 진행하는 학습 자료의 선택 가능한 시작점
- `assets/review-template.html`: 실제 체크 항목, 드래그 선택 주석, 항목별 메모와 초안 복원을 재사용하는 오프라인 시작점
- `assets/reply-panel.html`, `reply-panel.js`, `reply-content.js`: 넓은 원본 리더와 하단 회신 입력창, 접이식 선택 요약과 문맥 수집
- `scripts/reply-bridge.py`: 로컬 HTML 스냅샷, SQLite 응답 보관, 명시적 Herdr 세션 전달
- Codex/Claude Code는 native ID와 foreground 프로세스를 확인한 뒤 `agent prompt`로 전달한다. GJC는 private SDK descriptor의 native ID/PID를 확인한 뒤 `pane run`으로 한 번 제출한다. Herdr에 남은 Devin ID를 GJC ID로 쓰지 않는다.
- `receive`: 실행 중인 원본 Codex 도구 호출로 응답 반환. 완료된 턴을 자동으로 깨우지는 않는다
- 선택은 응답에 자동 포함하며, 항목별 메모와 전체 메모를 분리한다. 전송 미리보기와 실제 메시지는 같은 Markdown/XML 생성기를 사용한다
- 긴 경로와 전체 해시, 질문 라벨은 보관하고 `inspect`로 조회한다. 프롬프트에는 자료 식별자, 짧은 버전, 선택값, 메모를 담는다
- `assets/01-*.html`부터 `assets/20-*.html`: 용도별 단일 HTML 예시 템플릿
- `assets/AGENTS.md`: 20개 예시 템플릿 카탈로그
- `scripts/verify.sh`: `--syntax`는 브라우저 없이 실행. CDP 모드는 명시 요청일 때만 쓰고 끝나면 데몬을 내린다

## 저장 경로와 정리

| 수명 | 경로 | 정리 |
|---|---|---|
| 이번 답이나 선택으로 끝나는 페이지 | `$TMPDIR/html-pages/` | macOS가 3일 이상 접근하지 않은 파일을 매일 지운다 |
| `$TMPDIR`이 없는 환경의 대체 경로 | `~/.cache/html-pages/` | OS가 지우지 않는다. 쌓이면 손으로 비운다 |
| 다시 볼 내용 | `~/.agents/artifacts/` | 지우지 않는다 |

회신 서비스는 등록 시점의 페이지 스냅샷을 `~/.agents/artifacts/.html-page-replies/`에 따로 보관한다. 임시 파일이 지워져도 보낸 응답과 그 페이지는 남는다. Stop 훅은 두 경로 모두 내 소유이고 group/other 쓰기가 없을 때만 본다.

## 참고 자료와 출처

20개 예시 템플릿은 Anthropic의 [The unreasonable effectiveness of HTML](https://github.com/anthropics/html-effectiveness) 저장소에서 가져왔다. 원본 파일명과 내용을 유지했으며, 가져온 revision은 `58c305be97f47b26b678f2c07dec01d4242268ec`이다.

원본은 MIT License로 배포된다. 저작권과 라이선스 전문은 `assets/html-effectiveness-LICENSE.txt`에 보존한다.

시각형 스택(Mermaid+ELK, ECharts, Iconify)은 2026-06 멀티에이전트 리서치에서 공식 문서·릴리스·이슈 트래커를 검증해 선정했다.

`references/ui-polish.md`의 마감 규칙은 [jakubkrehel/skills](https://github.com/jakubkrehel/skills)(MIT, revision `d01493b0a7b976a74bfcedc80c783d60c7995910`)의 `better-ui` 스킬 원칙에서 가져왔다. 원본은 React·Tailwind·Motion 기준이라 그대로 참조하지 않고, 단일 파일 HTML에서 성립하는 항목만 골라 다시 썼다.

- 내재화한 항목: 깊이는 그림자와 구조는 보더 분리, 동심 border radius, 이미지 아웃라인의 순수 흑/백 규칙, `transition` 속성 명시와 `will-change` 절제, `scale(0.96)` 누름 피드백, 반복 조작의 모션 절제와 `prefers-reduced-motion`, 아이콘의 광학 무게와 `currentColor` 상태 표현.
- 제외한 항목: `AnimatePresence`·`initial={false}`, Motion spring 설정, Tailwind 클래스 문법, RTL 아이콘 플립. 이 스킬 산출물에는 해당 스택이 없다.
- 규칙은 `interfaces` 플러그인 설치 여부와 무관하게 동작하도록 두 시작 템플릿에 CSS 토큰(`--shadow-border`, `--img-outline`)으로 배선했다.

## 유지보수

번호가 붙은 파일은 정보 구조를 참고하는 예시다. 사용자 지정 사례와 피드백 근거가 우선이며, 파일이 보관돼 있다는 이유만으로 선호 사례로 분류하지 않는다. 실제 피드백과 원본 경로는 로컬 artifact catalog에 둔다. 업스트림을 갱신할 때는 20개 HTML과 라이선스 고지를 함께 검토한다.

직접 작성용 두 시작 템플릿은 무채색 다크/라이트 토큰을 사용한다. Mermaid와 ECharts도 같은 회색 계열과 텍스트/축 색을 읽으며, 클래스별 라벨/선 굵기/점선으로 차이를 표현한다. 출처 원본을 유지하는 번호형 예시와 보관 자료, 증거 스크린샷은 일괄 재색상화하지 않는다.

검토용 `review-template.html`은 사용자 확인을 거친 체크와 드래그 주석 화면을 범용화한 별도 시작점이다. 완료 초록/미응답 빨강, 선택 영역 우측 상단의 주석 아이콘, 입력 즉시 회신 초안에 반영되는 작은 편집창을 제공한다. 상시 주석 도구막대나 별도 담기 단계는 없다. 항목 ID와 설명 내용은 바꿀 수 있고, 주석의 원문 위치와 조건은 작성 시점에 고정된다. 길이 제한을 넘은 편집도 복구용 초안으로 보존하되 해당 주석은 전송에서 제외한다. 작성 계약은 `references/confirm-sheet.md`에 있다.

템플릿은 직접 열면 전체 질문을 포함한 복사 경로를, 기존 회신 패널 안에서 열면 원래 대화로 보내는 경로를 사용한다. 연결 상태에서는 본문의 전체 메모/복사 UI를 숨겨 오른쪽 목차와 하단 입력창을 중복하지 않는다. 원본 연구 자료와 미리보기, 사용자 답변은 템플릿에 복제하지 않는다.

회신 동작의 참고 자료는 [Herdr agent automation](https://herdr.dev/docs/agent-automation/), [Herdr Web UI](https://github.com/devswha/herdr-web-ui), [Plannotator](https://github.com/backnotprop/plannotator)다. 기존 Herdr CLI를 전달 수단으로 쓰며 Web UI 코드를 복사하거나 설치본을 수정하지 않는다. 별도 브라우저 연결과 무관한 보관이 필요해 artifact별 응답 큐를 둔다. `sent`는 터미널 입력 전달을 뜻하며 에이전트의 처리 완료를 뜻하지 않는다.

회신 UI는 [Aside](https://aside.com)의 얇은 구분선과 둥근 입력창을 참고했다. 원본은 화면 아래까지 이어지고 회신 입력창만 그 위에 뜬다. 독 전체를 채우는 배경이나 iframe 높이 축소는 없으며, 입력창 밖의 빈 영역은 원문을 그대로 보여 주고 클릭도 통과시킨다. 문서 또는 내부 스크롤 영역의 끝에만 여유 공간을 추가해 마지막 항목을 입력창 위로 올려 읽을 수 있다. 선택 결과, 인용, 전송 미리보기는 ‘선택한 내용’에서 펼친다. 요약과 입력창을 접어도 초안은 유지하며, 펼침 상태도 새로고침 후 복원한다.

상단의 ‘맥락’은 자료 목적, 이전 결정과 이번 변경을 짧게 보여 준다. 요약은 원본의 `html-reply-context` 메타데이터에서 읽으며 자동으로 대화 이력을 추측하지 않는다. 자료 제목/버전과 원래 대화를 함께 표시해 여러 HTML을 구분한다. 바로 옆의 세션 이동 버튼은 정확한 native ID와 foreground 소유를 재확인한 뒤 원래 Herdr 세션만 선택한다. 전송이나 새 세션 생성은 하지 않고, 닫힌 세션이나 중복 대상은 오류를 표시한다. 작업 중인 대화나 작성 중인 초안도 지우지 않고 볼 수 있다. 미리보기에서는 실제 이동하지 않는다.

오른쪽의 짧은 줄에 마우스를 올리면 Notion 방식의 목차가 펼쳐지고, 제목을 누르면 해당 문단으로 이동한다. 현재 위치는 진한 줄과 목차 강조로 표시한다. 터치/키보드로도 접근하며 Escape로 닫는다. 넓은 배경과 입력창은 중립색, 보내기와 원래 세션 이동은 파랑으로 강조한다. 원문 시각화는 경로와 범주에 필요한 색을 라벨/선 모양과 함께 사용한다. 응답 완료는 초록, 미응답과 선택 필요는 빨강이며 정답이나 승인을 뜻하지 않는다. 전송 대기/도착/오류는 문구와 회색 배경으로 구분한다. 다크/라이트를 지원하며 원문 이미지나 증거 스크린샷은 흑백으로 바꾸지 않는다. 시스템 서체와 기존 저장/전달 계약을 유지한다.

실제 질문이 있는 자료는 하단에 응답 진행과 ‘미응답 보기’를 표시한다. 목차에는 질문별 완료/미응답, 상위 문단의 미응답 개수, ‘미응답만’ 필터가 붙는다. 질문을 누르면 원문의 선택칸으로 이동하고 접힌 질문도 열린다. 선택 질문의 메모만으로 완료 처리하지 않으며 직접 글로 답하는 질문은 `data-reply-answer`로 구분한다. 작성 규약은 확인 시트 reference가 정본이다. 미응답을 남긴 부분 전송, 체크 해제, 복수 선택과 메모의 새로고침 복원을 지원한다. 입력 중 자동 화면 이동은 하지 않는다.

브리지는 macOS/Linux, Python 표준 라이브러리와 Herdr CLI를 사용한다. 원본 HTML의 외부 CDN은 기존 의존성으로 남는다. 네트워크 리스너는 loopback 전용이고, POST는 정확한 Host/Origin과 CSRF 값을 확인한다. 등록한 HTML이 명시적으로 가리킨 미디어만 제공한다. 전송 여부가 불확실한 응답은 자동 재시도하지 않는다.

회신 UI 회귀 검증은 `python3 <skill-dir>/tests/reply-panel-browser.py`로 실행한다. Aside에서 실제 HTTP/SQLite/`Store.receive` 왕복, 초안 복원, 대기 응답 고정/취소, 복사 실패 대체 경로, 모바일/짧은 화면, 목차 이동과 입력창 밖 클릭 통과를 확인한다. 다크/라이트에서 질문 상태색, 주요 동작의 파란 강조색, 최소 4.5:1 텍스트 대비와 나머지 표면의 중립색을 검사한다. 시작 템플릿은 중립적인 기초 견본으로 유지하며 Mermaid/ECharts 렌더링과 React 위젯 조작을 확인한다. 임시 서비스와 탭은 종료한다. 격리된 테스트 ID를 사용하므로 실제 모델 응답이나 native 대화 자동 재개 검증은 아니다.

검토 템플릿 회귀 검증은 `python3 <skill-dir>/tests/review-template-browser.py`다. 일반화된 항목 ID로 실제 드래그, 주석 자동 수집과 편집/삭제, 새로고침과 제한 초과 초안 복구, 라이트/다크 및 좁은 화면, 독립 화면의 복사 처리와 격리된 회신 수신을 확인한다. 독립 화면은 loopback HTTP로 열고 클립보드 API의 인자를 검사하므로 `file://` 권한이나 실제 클립보드 읽기 검증은 아니다. 기존 패널과 native transport는 재사용하며 사용자의 대화에 시험 입력을 보내지 않는다.
