# Curriculum 스킬 (maintainer README)

> 대상 스킬 루트: `~/.agents/skills/shared/curriculum/` (source of truth). 심볼릭: `~/.claude/skills/curriculum/`, `~/.codex/skills/curriculum/`.
> 편집 착수 시 `skill-manager`(update 모드) + `authoring-principles.md` 선독 절차를 따른다.
> 이 파일은 사람(maintainer)용이다. 사고 기록, 설계 근거, 출처는 여기에 둔다 - SKILL.md와 코드는 AI가 읽는 파일이라 출처/사고 정보를 넣지 않는다(skill-manager 규칙).

## 설계 의도 (작성자)

강제하려는 것은 AI 산문 지침이 아니라 **스크립트/exit-code**다. 의도 전달만 지침으로 둔다. 근거: "지침이 비대할수록 실행률이 떨어진다." 산문으로 "잘 해라"라고 적으면 AI가 건너뛰지만, 게이트가 산출물과 exit-code를 요구하면 못 건너뛴다.

이 의도와 skill-manager의 "Claude는 이미 똑똑하다, 관찰된 실패에만 최소 추가" 원칙은 충돌하지 않는다. 아래 게이트는 모두 **문서화된 반복 실패**(다회 재발)에 대응하는 것이지 일반 모범을 기계화한 것이 아니다.

## 구조 개요

- **5 Phase**: 설계 -> 자료조사 -> 자료생성 -> 노션반영 -> 검수/개선 (어느 단계부터든 진입). 각 Phase 세부는 `references/`.
- **게이트 스크립트** `scripts/curriculum_gate.py`: 서브커맨드 `explore` / `gate-candidates` / `verify-pages` / `verify-media` / `review-draft` / `gate-review` / `status`.
- **반영 스크립트** `scripts/notion_reflect.py`: 노션 반영 재업로드 + 검수 게이트(gate-review) 내장.
- **외부 PreToolUse 훅** `~/.claude/hook-utils/curriculum-write-gate.py`: 충실도 게이트(net-new 발명 차단). 이 스킬 폴더 밖, `~/.claude`에 있다.
- **references** 15개 + `templates/` 1개.

## 게이트 원장 (왜 각 게이트가 있나)

SKILL.md 본문은 "이 단계가 강제된다"는 거시 라우팅만 둔다. 각 게이트가 막는 실패와 그 근거 사고는 여기에 둔다. 9개 게이트가 7개 독립 실패모드에 대응한다(과기계화 아님).

| 게이트 | 막는 실패모드 | 근거 사고 (다회 반복) |
|---|---|---|
| `explore` | 기존 검증 자료를 안 보고 새로 지어냄. 모듈 DB만 보고 "자료 없다"고 고착 | author-intent #1 "왜 기존 자료 안봤어". 3소스(모듈 DB + 강의자료/조직 노션 + 로컬) 전수, 최신순 10개 임계 |
| `gate-candidates` | 검색 파일만 만들고 원문(`ntn pages get`)은 안 본 채 제작 시작 | #3 딥탐색 건너뜀. `[x]` 체크 + 근거 + 최선 후보를 요구 |
| `verify-pages` | page-id를 환각해 단정/반영 | 한 회차에서 존재하지 않는 page-id 18개 환각. 404(환각) vs 401/403(미공유) 구분 |
| `verify-media` | 텍스트만 이식하고 이미지/첨부를 빠뜨림 | #7 이식 누락. 원본 작업본 vs 교안 미디어 ref 대조 |
| `review-draft` | 신호 없는 섹션, 이미지 없는 산출물 섹션, dense-prose, AI slop 표기 | 표기/구조 게이트 5종(frontmatter, aside, 비표준색, 소수 번호, 콜아웃 이모지) |
| `gate-review` | 검수가 약점표/분석에서 멈추고 실제로 안 고침 | author-intent #2 "왜 이미지 개선 안하냐". 검수 리포트 + 고신호 0을 반영 전제로 |
| `status` | 단계 전환을 산문 추론에 맡겨 1라운드로 끝내거나 건너뜀 | "검증 루프 안 돎". 어느 Phase까지 통과했는지 기계 판정(enforcement 아닌 가시성) |
| `notion_reflect` 내장 게이트 | 검수 리포트 없이, 고신호 교안인 채로 반영 | gate-review를 반영 진입부에서 재실행. `--skip-gate`는 의도적 우회만 |
| `curriculum-write-gate` 훅 | 소스에 없는 net-new(발명) 블록을 노션에 씀 | author-intent #1 서브타입. `.fidelity.json` sources 선언 + char-trigram 커버리지로 차단, 우회 불가 |

공통 규칙: 게이트 통과는 exit 0 + 응답에 (실행 명령, exit code, 핵심 출력 라인) 인용으로만 인정한다. 증거 없이 통과를 단정한 실패가 있었다(단정 후 누락/환각).

## 향후 스크립트화 후보 (산문인데 기계 강제 가능, 미구현)

> 2026-06-22 skill-manager 정합 감사에서 도출. review-draft/게이트로 흡수 가능하나 ROI와 난이도로 보류.

- **anti-patterns 5절 수동 rg 제거** (높음): "강의 본문 기호 rg 0"을 수동 명령으로 안내하나, review-draft가 `slop-symbol`/`source-inline`으로 이미 file:line 강제(fence 스킵으로 코드펜스 제외도 동등). 수동 rg를 "review-draft가 강제"로 대체.
- **빈 이미지/staging-link 검사** (중간): notion-sync 4-3 round-trip의 빈 이미지 `![]()`와 테스트 링크 `<page url=`를 review-draft 패턴으로 추가.
- **module-bank 적재 검증 게이트화** (중간): "적재했다 단정 금지, data-source query로 행 실재 + 속성값 확인" + "원본 미디어 ref 전수 보존"을 verify-media 재사용 또는 전용 게이트로.
- **코드펜스 한글 비-text 검출** (낮음, 추정): 복붙 펜스가 한글인데 언어가 text 아니면 노션이 오하이라이팅. 휴리스틱 가능성 검토.

## 미착수 설계 항목

- **리서치/검수 서브에이전트 역할 경계 명문화**: 스크립트(결정, 전수 대조) vs 서브에이전트(판단, 비평) 경계를 references에 더 구체화. 대부분 이미 분리됨(notion-explorer는 좌표, curriculum-reviewer는 검수).
- **노션 템플릿 감독 가드**: 템플릿 골격은 자동화하지 않고 사용자가 직접 감독한다. 유형은 고정 목록 없이 프로젝트별 사용자 지시로 받는다(AI 미감 재구성 금지).

## 변경 이력

- 2026-06-30: SKILL.md 본문 re-macro. run-on 불릿 분해, 본문의 incident 인용과 미시 어휘(서브커맨드, exit-code, 경로)를 README/references로 이동, 품질 게이트 섹션을 거시 라우팅으로 축약. 게이트 로직/훅은 불변.
- 2026-06-22: review-draft 표기 게이트 5종, status + 검수 루프 강제, skill-manager 원칙 정합화(P1 자기위반, P2 배선, P3 중복 축약).
