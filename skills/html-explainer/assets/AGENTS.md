# HTML 예시 템플릿 카탈로그

이 폴더의 번호형 HTML 20개는 [Anthropic html-effectiveness](https://github.com/anthropics/html-effectiveness)의 단일 파일 예시다. 각 파일은 빌드 없이 브라우저에서 열리며, 결과물의 용도와 정보 구조를 고를 때 참고한다.

실제 산출물을 만들 때는 상위 `SKILL.md`의 타입 선택, 다크/라이트, 자동 레이아웃, 한국어 라벨, 렌더 검증 규칙을 적용한다. 번호형 파일은 그 규칙을 대체하지 않는다.

## 기본 템플릿

| 파일 | 용도 |
|---|---|
| `template.html` | Mermaid/ELK 다이어그램과 ECharts를 쓰는 정적 시각형 설명 자료 |
| `interactive-template.html` | React 상태와 단계 이동을 쓰는 인터랙티브 워크스루 |

## Exploration & Planning

| 파일 | 템플릿 |
|---|---|
| `01-exploration-code-approaches.html` | 같은 문제를 푸는 세 가지 코드 접근법과 장단점을 나란히 비교 |
| `02-exploration-visual-designs.html` | 여러 레이아웃과 색상 방향을 실제 화면으로 비교 |
| `16-implementation-plan.html` | 마일스톤, 데이터 흐름, 인라인 목업, 위험 코드와 리스크 표를 묶은 구현 계획 |

## Code Review & Understanding

| 파일 | 템플릿 |
|---|---|
| `03-code-review-pr.html` | diff에 주석, 심각도 태그, 이동 링크를 붙인 PR 코드 리뷰 |
| `04-code-understanding.html` | 낯선 패키지의 모듈, 호출 흐름, 진입점을 상자와 연결선으로 정리 |
| `17-pr-writeup.html` | 변경 동기, 전후 비교, 파일별 이유, 집중 검토 지점을 담은 PR 설명 |

## Design

| 파일 | 템플릿 |
|---|---|
| `05-design-system.html` | 색상, 타입 스케일, 간격 토큰을 복사 가능한 견본으로 정리한 디자인 시스템 |
| `06-component-variants.html` | 한 컴포넌트의 크기, 상태, 의도 변형을 한 화면에서 비교 |

## Prototyping

| 파일 | 템플릿 |
|---|---|
| `07-prototype-animation.html` | duration과 easing을 조절하며 전환을 확인하는 애니메이션 샌드박스 |
| `08-prototype-interaction.html` | 네 화면을 연결해 실제 클릭 흐름을 확인하는 인터랙션 프로토타입 |

## Illustrations & Diagrams

| 파일 | 템플릿 |
|---|---|
| `10-svg-illustrations.html` | 글에 들어갈 여러 SVG 도해를 한 장에서 확인하고 개별 복사 |
| `13-flowchart-diagram.html` | 단계별 실행 내용, 시간, 실패 경로를 클릭해 보는 배포 플로차트 |

## Decks

| 파일 | 템플릿 |
|---|---|
| `09-slide-deck.html` | 좌우 방향키로 이동하는 빌드 없는 단일 HTML 발표 자료 |

## Research & Learning

| 파일 | 템플릿 |
|---|---|
| `14-research-feature-explainer.html` | TL;DR, 접이식 요청 경로, 설정 탭, FAQ로 기능 동작을 설명 |
| `15-research-concept-explainer.html` | 직접 조작하는 시뮬레이션, 비교표, 연동 용어집으로 개념을 설명 |

## Reports

| 파일 | 템플릿 |
|---|---|
| `11-status-report.html` | 완료, 지연, 핵심 지표를 빠르게 훑는 주간 상태 보고서 |
| `12-incident-report.html` | 분 단위 타임라인, 로그 발췌, 후속 조치 체크리스트를 담은 장애 보고서 |

## Custom Editing Interfaces

| 파일 | 템플릿 |
|---|---|
| `18-editor-triage-board.html` | 티켓을 Now, Next, Later, Cut으로 옮기고 Markdown 순서를 내보내는 보드 |
| `19-editor-feature-flags.html` | 영역별 토글, 선행 조건 경고, 변경 키 diff 복사를 제공하는 기능 플래그 편집기 |
| `20-editor-prompt-tuner.html` | 변수 슬롯이 있는 프롬프트를 편집하고 여러 입력 결과를 실시간 비교하는 튜너 |
