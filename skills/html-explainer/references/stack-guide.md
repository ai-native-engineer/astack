# 스택 가이드 — 기능별 함정·레시피

2026-06 멀티에이전트 리서치(공식 문서·릴리스·이슈 트래커 검증)로 선정한 스택의 사용 지침. 작성하려는 기능의 섹션만 읽으면 된다.

## CDN 로드 (템플릿에 포함됨)

```html
<script src="https://cdn.jsdelivr.net/npm/iconify-icon@3/dist/iconify-icon.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/echarts@6/dist/echarts.min.js"></script>
<script type="module">
import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';
// ELK는 동적 import + 실패 시 dagre 폴백 (템플릿의 renderDiagram 참조)
</script>
```

## 애니메이션 — 이해 보조 전용

**장식적 등장 효과(fade-in, 슬라이드인)는 금지** — "이해에 하나도 도움이 안 된다"는 사용자 피드백 실측. 애니메이션은 정보를 운반할 때만 넣는다. 검증된 패턴 3가지(추가 라이브러리 불필요):

1. **엣지 흐름 (데이터 방향)** — Mermaid 내장. 엣지에 ID를 달고 animate 지정:
   ```
   source e0@-->|"라벨"| target
   e0@{ animate: true }
   ```
   점선(`-.->`)도 동작. "이 구성에서 실제로 데이터가 흐르는 경로"만 animate하면 그 자체가 설명이 된다.
2. **상태 토글 (구성 A ↔ B)** — 모드 버튼 → 다이어그램 재렌더(모드별 animate 목록 교체) + SVG 후처리 dim + 차트 `setOption` 색 교체 + 표·트리 CSS 클래스 전환을 한 번에. 켜고 끌 때 무엇이 살아나는지가 직접 보인다. SVG 후처리 주의점:
   - mermaid `classDef opacity`는 도형(rect)에만 적용 — 텍스트까지 dim하려면 렌더 후 노드 그룹(`g[id*="flowchart-<id>-"]`)에 `style.opacity` 적용.
   - 엣지 path id에는 렌더 프리픽스가 붙음(`m3-e7`) — `[id$="-e7"]` ends-with로 매칭.
   - 엣지 라벨(`.edgeLabels .edgeLabel`)은 측정용 복제가 섞여 총개수가 엣지 수의 배수 — 배수를 계산해 묶음으로 dim.
3. **값 변화** — ECharts는 `setOption` 시 내장 전환 애니메이션이 자동.

위로 부족한 연출(스크롤 연동 등)이 꼭 필요할 때만 Motion: `https://cdn.jsdelivr.net/npm/motion@12/dist/motion.js` 로드 후 `const { animate, inView } = Motion`. ⚠️ AI 학습 데이터는 framer-motion(React `<motion.div>`) 위주 — vanilla 전역 `Motion`에서 구조분해하는 형태만 쓰고, `prefers-reduced-motion`을 존중한다.

## Mermaid (다이어그램)

- **architecture-beta 금지** (SKILL.md 철칙). flowchart + subgraph로 그룹을 표현한다.
- 레이아웃: ELK 등록 성공 시 `initialize({ layout: 'elk' })`. 복잡한 그래프에서 기본 dagre보다 엣지 교차가 훨씬 적다.
- 노드 안 텍스트는 `<br/>`로 줄 분리. 한 줄 ~20자 이내 권장 (CJK 클리핑 이슈 mermaid#7354).
- 색 구분은 `classDef` + `class`로. **fill을 칠하지 말고 stroke 색만** 지정하면 다크/라이트 양쪽에서 테마 기본 fill과 자연스럽게 어울린다. 점선 구분: `stroke-dasharray:6 4`.
- 테마는 initialize의 `theme: 'dark' | 'default'`로만 — 라이브 전환은 재렌더 필요(템플릿에 배선됨). `fontFamily`는 initialize에서 지정해야 라벨 폭 측정과 실제 렌더 폰트가 일치한다.
- 손그림 스타일이 필요하면 `look: 'handDrawn'` (rough.js 내장) — Excalidraw 임베드 불필요.
- 다이어그램 소스는 `<script type="text/plain" id="...">`에 두고 `mermaid.render()`로 수동 렌더 — startOnLoad 자동 처리보다 에러 표시·재렌더 제어가 쉽다. render id는 호출마다 유니크하게.

## ECharts (차트·관계도)

- 다크 모드: `echarts.init(el, isDark() ? 'dark' : null)` + 테마 전환 시 dispose 후 재init (템플릿 패턴). option에 `backgroundColor: 'transparent'`를 넣어 카드 배경과 융합.
- **로그 축 range bar는 stacked bar로 만들지 말 것** (로그축+스택 부정확) — `type: 'custom'`의 renderItem에서 `api.coord([값, 카테고리])`로 rect를 그린다 (공식 Profile/Gantt 패턴, rect shape의 `r`로 라운드 코너).
- 간단한 네트워크는 `series: { type: 'graph', layout: 'force' }`, sankey/tree/treemap/chord도 풀 번들에 포함 — 별도 라이브러리 불필요.
- 컨테이너에 명시적 height 필수 + `window.resize`에서 `chart.resize()`.
- 한국어 라벨: `axisLabel`에 `\n` 줄바꿈 동작, overflow는 `'break'`/`'breakAll'`.

## Iconify (아이콘)

- `<iconify-icon icon="lucide:database"></iconify-icon>`. 크기는 `font-size`, 색은 `color`로 제어 (currentColor 상속 → 다크 자동).
- ⚠️ **존재하지 않는 이름은 에러 없이 빈 칸** — 흔한 lucide 아이콘만 쓰고, verify 단계에서 `iconify-icon`의 shadowRoot에 svg가 생겼는지 확인한다 (verify.sh가 체크).
- lucide 이름은 현행 canonical 기준 (예: `triangle-alert`, `alert-triangle` 아님).
- Mermaid 노드 내부에는 아이콘을 넣지 않는다 — 섹션 헤더·경고 박스 등 HTML 영역에만.

## 오프라인화 (보관·공유용 자료)

기본 구성은 CDN 4개 의존 — 오프라인에서 다이어그램·차트·아이콘이 안 뜬다. 보관용은:

1. 아이콘: 생성 시점에 `curl -s https://api.iconify.design/lucide/<이름>.svg`로 받아 인라인 SVG로 박는다 (stroke="currentColor" 유지됨 → 다크 자동 유지).
2. 라이브러리: CDN URL의 파일을 받아 `<script>` 인라인 또는 파일 옆에 두고 상대 경로 로드.
3. Mermaid는 렌더 결과 SVG를 추출해 정적으로 박는 방법도 있다 (테마 고정됨 — 다크/라이트 중 하나 포기).

## 케이스별 대안 (스택으로 부족할 때)

| 케이스 | 대안 | 주의 |
|---|---|---|
| 엣지 수십 개의 조밀한 의존/계층 그래프 | Graphviz WASM (`@viz-js/viz@3`, viz-standalone.js) | 한글 라벨 폭 오추정 → 노드에 `margin="0.3,0.15"` 방어 필수. 다크는 `bgcolor="transparent"` + 출력 SVG에 CSS 오버라이드 |
| 픽셀 단위 의도된 배치 (레인 구조 등) | elkjs(레이아웃만) + HTML/CSS 카드 직접 렌더 | 보일러플레이트 50~100줄 — 즉석 생성 말고 템플릿화가 전제. 노드 크기는 임시 DOM 실측으로 |
| 데이터 차트만 + 스펙 재사용 | Vega-Lite 6 + vega-embed (`{theme:'dark'}` 한 줄) | 스크립트 3개 로드, theme 옵션은 experimental |
| 마크다운 → 마인드맵 | markmap (autoloader CDN) | 2024-12 이후 릴리스 정체 |

## 피해야 할 것 (검증된 함정)

- **ApexCharts**: 2025년 말 MIT → 듀얼 라이선스 전환 (연매출 $2M 미만만 무료 + 경쟁 제품 금지 조항). AI 학습 데이터엔 "MIT"로 남아 있어 오안내되기 쉬움.
- **leader-line**(2025-04 아카이브)·**jsPlumb community**(업데이트 종료 명시)·**perfect-arrows**(2023 이후 휴면): "DOM 박스 + 자동 화살표" 카테고리 전체가 사실상 죽음 — 화살표가 필요하면 Mermaid로 그린다.
- **Plotly.js의 `template:'plotly_dark'`**: Python 전용 — JS에서는 조용히 무시된다. Plotly 자체가 4.8MB라 이 용도에 부적합.
- **anime.js**: v3→v4 API 전면 개편으로 AI가 구문법을 섞기 쉬움 — 애니메이션은 Motion 사용.
- **Chart.js**: 다크 테마 없음(수동 갈아끼우기) + sankey/graph는 별도 플러그인 — ECharts가 상위 호환.
- **Excalidraw 임베드**: 자동 레이아웃이 없어 좌표 수동 계산으로 회귀 — 손그림은 Mermaid `look: 'handDrawn'`으로.
