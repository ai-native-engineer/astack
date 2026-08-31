# HTML Explainer

로컬에서 바로 열 수 있는 단일 HTML 설명 자료를 만드는 shared skill이다. 실행 지침의 정본은 `SKILL.md`와 `references/`이며, 이 문서는 유지보수자를 위한 구조와 출처만 설명한다.

## 구조

- `SKILL.md`: 타입 선택, 생성, 사용자 브라우저로 열기. CDP 검수는 명시 요청만
- `references/`: 타입별 스택과 작성 규칙, 타입 공통 마감 규칙(`ui-polish.md`)
- `assets/template.html`: 시각형 기본 템플릿
- `assets/interactive-template.html`: 인터랙티브형 기본 템플릿
- `assets/01-*.html`부터 `assets/20-*.html`: 용도별 단일 HTML 예시 템플릿
- `assets/AGENTS.md`: 20개 예시 템플릿 카탈로그
- `scripts/verify.sh`: 사용자가 CDP 검수를 요청했을 때만. 끝나면 데몬을 내린다

## 참고 자료와 출처

20개 예시 템플릿은 Anthropic의 [The unreasonable effectiveness of HTML](https://github.com/anthropics/html-effectiveness) 저장소에서 가져왔다. 원본 파일명과 내용을 유지했으며, 가져온 revision은 `58c305be97f47b26b678f2c07dec01d4242268ec`이다.

원본은 MIT License로 배포된다. 저작권과 라이선스 전문은 `assets/html-effectiveness-LICENSE.txt`에 보존한다.

시각형 스택(Mermaid+ELK, ECharts, Iconify)은 2026-06 멀티에이전트 리서치에서 공식 문서·릴리스·이슈 트래커를 검증해 선정했다.

`references/ui-polish.md`의 마감 규칙은 [jakubkrehel/skills](https://github.com/jakubkrehel/skills)(MIT, revision `d01493b0a7b976a74bfcedc80c783d60c7995910`)의 `better-ui` 스킬 원칙에서 가져왔다. 원본은 React·Tailwind·Motion 기준이라 그대로 참조하지 않고, 단일 파일 HTML에서 성립하는 항목만 골라 다시 썼다.

- 내재화한 항목: 깊이는 그림자와 구조는 보더 분리, 동심 border radius, 이미지 아웃라인의 순수 흑/백 규칙, `transition` 속성 명시와 `will-change` 절제, `scale(0.96)` 누름 피드백, 반복 조작의 모션 절제와 `prefers-reduced-motion`, 아이콘의 광학 무게와 `currentColor` 상태 표현.
- 제외한 항목: `AnimatePresence`·`initial={false}`, Motion spring 설정, Tailwind 클래스 문법, RTL 아이콘 플립. 이 스킬 산출물에는 해당 스택이 없다.
- 규칙은 `interfaces` 플러그인 설치 여부와 무관하게 동작하도록 두 시작 템플릿에 CSS 토큰(`--shadow-border`, `--img-outline`)으로 배선했다.

## 유지보수

번호가 붙은 파일은 결과물 유형과 정보 구조를 참고하는 예시다. 실제 생성물은 `SKILL.md`의 타입별 규칙을 따른다. 업스트림을 갱신할 때는 20개 HTML과 라이선스 고지를 함께 교체하고 skill-manager 검증을 다시 실행한다.
