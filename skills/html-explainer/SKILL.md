---
name: html-explainer
description: "Local single-file HTML explainer in two types - visual (Mermaid/ELK diagrams, ECharts, Iconify; static, at-a-glance) and interactive walkthrough (React single-file; click-through steps, learner-driven). Both dark/light with headless render verification. Use when user asks HTML로 설명/정리, 시각화 자료, 구조도, 아키텍처 그림, flow diagram, comparison chart, 인터랙티브 튜토리얼, 단계별 설명, 클릭하며 보는 설명, step-through explainer, or complex explanation as a local HTML file. Do NOT use for production websites, Remotion/video motion graphics, Marp/PPT slide deck files, raw markdown docs, or frontend app implementation."
argument-hint: "[visual|interactive] [topic]"
---

# HTML Explainer

설명 자료를 단일 HTML로 만든다. **두 타입**이 있고, 시작 전에 먼저 고른다. 핵심 멘탈 모델: **수동으로 좌표를 계산하지 않는다** - 시각형은 배치를 레이아웃 엔진(Mermaid/ELK)에, 인터랙티브형은 상태를 React에 위임한다. 수동 SVG 좌표 계산은 요소 겹침·가림 사고의 근원이다(실측 실패 패턴).

## 두 가지 타입 - 먼저 고른다

| 타입 | 무엇 / 언제 | 스택 | 시작 템플릿 + 읽을 reference |
|---|---|---|---|
| **시각형** | 다이어그램·차트로 핵심을 한 화면에(정적). 구조·관계·수치를 한눈에, 참고·요약. | Mermaid v11+ELK, ECharts 6, Iconify | `assets/template.html` + `references/stack-guide.md` |
| **인터랙티브형** | 단계를 클릭하며 스스로 결론에 도달(단계 워크스루). 개념 체득, 비교·의사결정, 교육. | React 18 + Babel 단일 HTML | `assets/interactive-template.html` + `references/interactive-walkthrough.md` |

## 워크플로 (두 타입 공통)

1. **타입 선택 -> 템플릿 복사**: 위 표의 시작 템플릿을 출력 경로로 복사해 내용만 채운다. 테마·폰트·다크/라이트·네비 배선이 이미 들어 있다 - 골격을 재작성하지 않는다.
2. **내용 작성**: 작성 전 그 타입의 reference에서 쓸 기능의 함정·레시피를 읽는다.
3. **검증**: `scripts/verify.sh <파일>` - 콘솔 에러·렌더를 확인하고, 출력된 스크린샷을 Read로 열어 겹침·잘림을 육안 확인한다. 통과 전에는 사용자에게 열어주지 않는다.
4. **열기**: `open <파일>`.

출력 경로는 기본 `/tmp/<slug>.html`(1회성 열람). 보관·공유를 원하면 프로젝트 폴더에 둔다.

## 철칙 (두 타입 공통)

- 긴 한국어 라벨은 `<br/>`로 수동 분리 (CJK 무공백 장문 클리핑).
- 다크/라이트는 `matchMedia('(prefers-color-scheme: dark)')` 기준 - 양 템플릿에 배선돼 있다.
- CDN 라이브러리는 메이저 버전 고정(시각형 `@11`·`@6`·`@3`, 인터랙티브형 React `@18.3.1`·Babel `@7.26.4`). `@latest` 금지.
- **애니메이션은 이해 보조만** - 데이터 흐름·상태 전환·값 변화·단계 진행처럼 정보를 운반할 때만. 장식적 fade-in·슬라이드인 금지.

## 시각형 전용 철칙

- Mermaid **architecture-beta 금지** - 형제 노드 겹침(공식 한계). 아키텍처도 `flowchart`+`subgraph`로 그린다.
- 새 차트/다이어그램을 추가하면 다크/라이트 **재렌더 함수에 등록**한다(템플릿 배선).
- 스택 외 라이브러리가 필요해 보이면 먼저 `references/stack-guide.md`의 "케이스별 대안"·"피해야 할 것"을 확인한다(라이선스 함정·중단 프로젝트·AI 헛코드 패턴 정리됨).

## Resources

| 언제 | 무엇 |
|---|---|
| 타입 선택·라우팅 | 위 "두 가지 타입" 표 |
| 시각형 내용 작성 전 | `references/stack-guide.md` |
| 인터랙티브형 내용 작성 전 | `references/interactive-walkthrough.md` |
| 새 파일 시작 | `assets/template.html`(시각형) / `assets/interactive-template.html`(인터랙티브형) |
| 생성 후 검증 | `scripts/verify.sh <파일.html>` |
