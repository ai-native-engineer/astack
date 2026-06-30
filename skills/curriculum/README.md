# Curriculum 스킬 수정 계획

> 작성: 2026-06-22, 작성자 의도 기록, 구현 중
> 대상 스킬 루트: `~/.agents/skills/shared/curriculum/` (심볼릭: `~/.claude/skills/curriculum/`)
> 스킬 편집 착수 시 `skill-manager`(update 모드) + 저작 원칙 선독 절차를 따른다.

현 구조: 5 Phase(설계 -> 자료조사 -> 자료생성 -> 노션반영 -> 검수/개선), 게이트 스크립트 `scripts/curriculum_gate.py`(서브커맨드 6개: `explore`/`verify-pages`/`verify-media`/`review-draft`/`gate-review`/`status`) + `scripts/notion_reflect.py`(노션 반영 재업로드 + 검수 게이트 내장), references 13개.

**핵심 원칙**: 강제하려는 것은 AI 산문 지침이 아니라 **스크립트/exit-code**로, 의도 전달만 지침으로. "지침이 비대할수록 실행률은 떨어진다."

---

## 진행 상황

- [x] **(B) review-draft 표기/구조 게이트 5종** (`3566b28`) - frontmatter, aside, nonstd-color(HIGH) + section-decimal, section-gap, callout-emoji(warn). authoring 3-1~3-3 산문 규칙을 기계 검출로 흡수.
- [x] **(A/1번) status 서브커맨드 + 검수 루프 강제** (`cf9a284`+) - `status`로 단계와 검수 통과와 다음 게이트를 기계 판정. `notion_reflect.py --report <검수.md>`가 gate-review를 다시 실행해 검수 리포트 없는 반영과 고신호 교안 반영을 거부(`--skip-gate` 우회). "검증 루프 안 돎" 처방.
- [x] **(감사) skill-manager 원칙 정합화** - P1 자기위반(notion-sync 동그라미숫자와 `[출처:]` 자기모순, authoring 가운뎃점), P2 배선 누락(status와 notion_reflect 게이트 문서화 + docstring 6개), P3 중복(이미지 우선순위, 미디어게이트, 보안콜아웃, 우회명령을 정본 포인터로 축약) 수정.
- [ ] (2번) 리서치/검수 서브에이전트 + 스크립트 역할 분리 - **다음**
- [ ] (3번) 노션 템플릿 감독 가드
- [ ] (P4) 향후 스크립트화 후보 - 아래 별도 섹션

---

## 1. 각 단계 명확화 ("검증 루프가 안 돈다" 처방, 완료)

게이트는 `curriculum_gate.py`로 강제됐으나 "단계 전환"과 "검수 루프 반복"이 강제되지 않아 AI가 1라운드로 끝내거나 건너뛰던 문제. 처방:
- [x] `curriculum_gate.py status <workspace> [--draft]` - 어느 Phase까지 통과했고 다음 필수 게이트가 무엇인지 기계 판정(탐색 산출물, 검수 리포트, 교안 고신호로).
- [x] **검수 루프 강제** - `notion_reflect.py --report <검수.md>` 반영 진입부가 gate-review를 실행해 검수 리포트 없는 반영과 고신호 교안 반영을 거부한다. 의도적이면 `--skip-gate`로만 우회.
- 상시 훅은 **쓰지 않음**(`status` on-demand로 충분, 상시 훅은 컨텍스트만 먹음, context-optimization-loop 원칙).

## 2. 리서치(Phase 2) + 검수(Phase 5) 서브에이전트 + 스크립트로 분리 (미착수)

무거운 원문 탐색/대조를 서브에이전트 안에서 처리, 메인엔 결과만.
- 리서치: `explore` 결과를 서브에이전트가 비판적 비교까지 후 "후보 비교표 + 추천"만 반환.
- 검수: 서브에이전트 fan-out로 review-draft 린트 / 페르소나 비평 / verify-media와 verify-pages 대조. codex `exec -s read-only` 교차검증 1개 병행.
- **핵심**: 스크립트(결정과 전수 대조) vs 서브에이전트(판단과 비평) 역할 경계를 references에 명문화. (대부분 이미 분리됨, 문서 정리 + 지침 구체화 수준)

## 3. 노션 템플릿 구성, 사용자 직접 감독 (미착수)

템플릿 골격 구성은 자동화하지 않고 작성자가 직접 감독. AI가 임의로 골격을 바꾸지 않는다는 가드를 SKILL.md/notion-sync.md에 명시. 템플릿 유형은 **고정 목록 없이 프로젝트별 사용자 지시로** 받는다(미감 재구성 금지).

---

## P4. 향후 스크립트화 후보 (산문인데 기계 강제 가능, 미구현)

> 2026-06-22 skill-manager 정합 감사에서 도출. review-draft/게이트로 흡수 가능하나 ROI와 난이도로 보류.

- [ ] **anti-patterns 5절 수동 rg 제거** (높음): "강의 본문 기호 rg 0"을 수동 명령으로 안내하나, review-draft가 `slop-symbol`/`source-inline`으로 이미 file:line 강제(fence 스킵으로 코드펜스 제외도 동등). 수동 rg를 "review-draft가 강제"로 대체.
- [ ] **빈 이미지와 staging-link 검사** (중간): notion-sync 4-3 round-trip의 빈 이미지 `![]()`와 테스트 링크 `<page url=`를 review-draft 패턴으로 추가.
- [ ] **module-bank 적재 검증 게이트화** (중간): "적재했다 단정 금지, data-source query로 행 실재 + 속성값 확인" + "원본 미디어 ref 전수 보존"을 verify-media 재사용 또는 전용 게이트로.
- [ ] **코드펜스 한글 비-text 검출** (낮음, 추정): 복붙 펜스가 한글인데 언어가 text 아니면 노션이 오하이라이팅. 휴리스틱 가능성 검토.

---

## 작업 순서

1. [x] (B) 게이트 5종, [x] (1번) status + 검수루프강제, [x] (감사) P1~P3 정합화
2. [ ] 검수 fan-out 래퍼 + 역할 경계 문서화 (2번)
3. [ ] 리서치 explore 서브에이전트 래퍼 (2번)
4. [ ] 템플릿 감독 가드 명문화 (3번)
5. [ ] P4 후보 중 높음(anti-patterns 5절)부터
