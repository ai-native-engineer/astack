---
name: html-explainer
description: 설명·시각화 자료를 단일 HTML 파일로 생성해 브라우저로 여는 표준 스택 + 검증 루프. 아키텍처/플로 다이어그램은 Mermaid+ELK(좌표 계산 없는 자동 레이아웃), 차트·간단한 관계도는 ECharts, 아이콘은 Iconify, 다크/라이트 자동 대응, 생성 후 헤드리스 렌더 검증까지 포함. 사용자가 "HTML로 설명/정리해줘", "시각화 자료 만들어줘", "구조도/아키텍처 그림", "플로 다이어그램", "비교 차트", "html-explainer"를 요청하거나, 복잡한 설명(구조 비교·아키텍처·플로)을 HTML로 만들어 open할 때 항상 사용. (영상 설명은 remotion-explainer, 웹 배포용 프로덕션 HTML은 design-html — 이 스킬은 로컬 1회성 설명 자료 전용.)
argument-hint: "[topic]"
---

# HTML Explainer

설명 자료를 단일 HTML로 만들 때의 표준 스택과 절차. 핵심 멘탈 모델: **좌표를 직접 계산하지 않는다** — 배치는 레이아웃 엔진에 위임한다. 수동 SVG 좌표 계산은 요소 겹침·가림 사고의 근원이다(실측으로 확인된 실패 패턴).

## 표준 스택

| 용도 | 라이브러리 | 핵심 |
|---|---|---|
| 다이어그램 (아키텍처·플로·관계) | Mermaid v11 + ELK 플러그인 | 텍스트 DSL → 자동 레이아웃, 겹침 원천 차단 |
| 차트 + 간단한 네트워크/sankey/tree | Apache ECharts 6 | 선언적 option 객체, 다크 테마 내장 |
| 아이콘 | Iconify 웹 컴포넌트 | `<iconify-icon icon="lucide:이름">`, currentColor로 다크 자동 |
| 애니메이션 | Mermaid 엣지 흐름 + 상태 토글 + ECharts 내장 전환 | 추가 라이브러리 없음 — stack-guide "애니메이션" 섹션 |

## 워크플로

1. **템플릿에서 시작**: `assets/template.html`을 출력 경로로 복사해 내용만 채운다. CSS 변수 테마·폰트·다크/라이트 재렌더 배선(JS)이 이미 들어 있다 — 이 골격을 매번 재작성하지 않는다.
2. **내용 작성**: 작성 전 `references/stack-guide.md`에서 사용할 기능의 섹션(함정·레시피)을 읽는다.
3. **검증**: `scripts/verify.sh <파일>` 실행 — 콘솔 에러·렌더 여부를 확인하고, 출력된 스크린샷을 Read로 열어 겹침·잘림을 육안 확인한다. 통과 전에는 사용자에게 열어주지 않는다.
4. **열기**: `open <파일>`.

출력 경로는 기본 `/tmp/<slug>.html` (1회성 열람). 사용자가 보관·공유를 원하면 프로젝트 폴더에 두고 오프라인 인라인(stack-guide 참조)을 적용한다.

## 철칙 (모든 생성에 적용)

- Mermaid **architecture-beta 다이어그램 금지** — 형제 노드 겹침이 공식 문서에 명시된 한계. 아키텍처도 `flowchart` + `subgraph`로 그린다.
- 긴 한국어 라벨은 `<br/>`로 수동 분리 (CJK 무공백 장문 클리핑 이슈).
- 다크/라이트는 `matchMedia('(prefers-color-scheme: dark)')` 기준 초기 렌더 + change 리스너 재렌더 — 템플릿에 배선돼 있으니 새 차트/다이어그램을 추가하면 해당 재렌더 함수에 등록한다.
- CDN 라이브러리는 jsDelivr 기준, 메이저 버전 고정(`@11`, `@6`, `@3`). `@latest` 금지.
- 스택 외 라이브러리가 필요해 보이면 먼저 `references/stack-guide.md`의 "케이스별 대안"과 "피해야 할 것"을 확인한다 (라이선스 함정·중단 프로젝트·AI 헛코드 패턴 정리됨).
- **애니메이션은 이해 보조만** — 데이터 흐름 방향(엣지 애니메이션), 상태 전환(구성 토글), 값 변화처럼 정보를 운반할 때만. 장식적 fade-in·슬라이드인 등장 효과 금지.

## Resources

| 언제 | 무엇 |
|---|---|
| 내용 작성 전 — 기능별 함정·레시피, CDN 스니펫, 대안/금지 목록, 오프라인화 | `references/stack-guide.md` |
| 새 파일 시작 | `assets/template.html` (복사해서 사용) |
| 생성 후 검증 | `scripts/verify.sh <파일.html>` |
