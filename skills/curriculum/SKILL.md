---
argument-hint: "[설계|자료조사|자료생성|노션반영|검수개선]"
name: curriculum
description: "입문자/비개발자 대상 강의, 교육과정, 교안, 실습, 워크숍, B2B 기업교육 자료를 설계, 제작, 수정, Notion 반영, 검수/개선하는 전 주기 스킬. Use when user asks for 커리큘럼, 강의 설계, 차시 설계, 학습목표, 교안/강의안 작성, 실습 설계, 회차 자료, 강의 자료 노션 반영, 교안 검수. Do NOT use for 단순 Notion 검색/CRUD, 일반 문서 작성, Google Workspace 조작, 음성 전사, 또는 교육과 무관한 리서치."
---

# Curriculum - 강의/교육과정 전 주기 (설계 -> 자료조사 -> 제작 -> 수정/노션 반영)

Backward Design + ADDIE 하이브리드 기반. context 수집부터 노션 회차 페이지 반영, 검증까지 한 흐름. **Phase 1~3은 도구 비종속, Phase 4 반영은 ntn 전용.** `[대괄호]`는 상황에 맞게 채운다. 워크스페이스 경로 예: `~/Playground/projects/curriculum-workspace/`.

## 라이프사이클 (5 Phase - 어느 단계부터든 진입 가능, 해당 작업에 들어가면 그 reference를 읽는다)

| Phase | 무엇 | 읽을 것 |
|---|---|---|
| 1. **설계** | 무엇을/왜 가르치나 - 목표, 차시 분해, 평가, 버전관리, B2B/B2C | [`references/design.md`](references/design.md) 1절 |
| 2. **자료조사** | `project-context-gather`에 위임 (다중소스 검색, 음성 전사, 아카이브) | [`references/design.md`](references/design.md) 2절 |
| 3. **자료생성** | 회차 페이지 작성 **+ 자기검수**(초안 != 완료) - 기존 자료 이식, 콘텐츠 원칙, 라이브 운영, 제작 직후 검수 루프 | [`authoring.md`](references/authoring.md)(3-6 자기검수) + [`review.md`](references/review.md) (+골격은 라이브냐 VOD냐로: 라이브 template.md / VOD vod-clip-template.md, 이미지 image-generation-notion-assets.md) |
| 4. **노션반영** | 베이스 선택 라우터(로컬/노션 어디가 최신) -> surgical 부분 반영 또는 전체교체 -> round-trip 검증 | [`references/notion-sync.md`](references/notion-sync.md) (+이미지 삽입 image-generation-notion-assets.md 2절) |
| 5. **검수/개선** | 사용자 관점으로 비평하고 **실제로 고친다**(약점표 금지) - 제작 마무리 겸 단독 진입 | [`references/review.md`](references/review.md) |

## 불변 원칙 (모든 Phase 공통)

- **AI 창작이 아니라 사람의 검증 자료가 기본값, 약간의 개선만** - 모든 Phase의 헌법. 기존 검증 자료를 베이스로 최소 개선하고, AI 자율 미감으로 새로 짓거나(특히 이미지) 멀쩡한 걸 방치 판단하지 않는다. 왜, 3대 실패패턴, 판단원칙은 [`references/author-intent.md`](references/author-intent.md)(제작/검수 시작 전 1회 읽기).
- **핵심만, 신호 우선, 개념은 명료하게** - 모든 블록은 수강생이 *뭘 보고/칠지*(명령어, 출처, 실제 화면 같은 신호)만 담는다. 개념은 **한 줄 정의 -> 직관적 단계 -> 복붙 프롬프트**로 또렷하게(잡설 제거와 개념 흐리기는 다르다). **산문 최소, 불렛/넘버링/표 우선**(세 문장 넘는 줄글은 쪼갠다). 검수 때 전체 줄 수/이미지 수가 아니라 **문단 밀도**를 본다. 블록 테스트, 콜아웃 용도/이모지, 표기 규칙 상세는 품질 게이트 / authoring 3-3절 / anti-patterns.md.
- **논리 구조는 항상 고객, 수강생 중심** - 사고 사슬은 1. 수강생 피드백/설문 -> 2. 만들고 싶다고 한 주제 -> 3. 그래서 이번 회차에 만드는 것 -> 4. 만들기 위해 가르칠 개념(기존 자료 이식). 개념->실습 순으로 정리하지 않는다.
- **입문자, 비개발자 전제** - 존댓말, 부담 낮게, 용어 첫 등장 1줄 풀이(괄호 인라인 풀이는 금지).
- **딥 탐색 -> 최선 선택 -> 비판적 검토 후 이식** (무비판 복붙 금지) - 1. 참고 자료를 최신순 10개 이상 탐색(`curriculum_gate.py explore`, 기본 임계 10 - 지정 소스 하나만 보고 시작 금지, 이 산출물 없이 제작/검수 시작 금지) 2. 비판적으로 비교해 최선 선택 3. 약점(낡음, 잡설, 이미지 부실, 도메인 불일치)을 검토한 뒤 이식. 통째 이식 범위는 검증된 설명/프롬프트/이미지 ref, 도메인(고객사, 팀, 예시)만 치환한다. 구체를 일반 라벨로 희석하지 않는다. **원본 밀도가 상한선**(불리면 비대). 상세는 review.md(검수)/authoring.md 3-0절(제작).
- **안전선**: 위험/보안 우회 명령(인증서 검증 끄기 등)은 학습자 본문, 강사 메모 어디에도 금지. 내부 모순 금지(저장 안 되면 "시제품", 되면 "도구"). 시간 현실성(한 블록에 풀코스 금지).

## 품질 게이트 (작성/반영 시 필수 - 상세는 각 reference)

깨지기 쉬운 3단계는 산문이 아니라 게이트 스크립트 `curriculum_gate.py`(`~/.agents/skills/shared/curriculum/scripts/`)가 산출물/exit-code로 강제한다. **게이트 통과 = exit 0 + 응답에 (실행 명령, exit code, 핵심 출력 라인) 인용** - 증거 없이 통과 단정 금지(이전 실패: 단정 후 누락/환각).

- **딥 탐색 게이트** (authoring 3-0절 / review 0절) - `explore`로 **강의 모듈 DB + 강의자료 워크스페이스/조직 노션 전수 + 로컬 교안** 셋 다 전수해 **참고 자료 최신순 10개 이상**(기본 임계 10) 후보 산출물(후보 <10/DB 미탐색/노션 미탐색이면 비0; 후보는 최신순 정렬+수정일 표기). 이후 `gate-candidates`로 `[x]` 후보, `근거:`, `최선 후보:`를 확인한다. 검색 파일만 만들고 원문을 안 본 상태로 제작/검수 시작 금지(#3 처방).
- **미디어 게이트** (authoring 3-0절) - `verify-media`로 로컬 원본 작업본 vs 교안의 미디어 ref를 대조(누락 0) + 섹션 분포 + 시각자료 출처 우선순위(정본 image-generation-notion-assets.md intro). live Notion 반영 검증은 notion-sync/notion_reflect round-trip이 맡는다.
- **환각 차단 게이트** (review 3절) - page-id 실존은 `verify-pages`(직접 REST, 404 환각 vs 401/403 미공유)로, 이미지 실존은 페이지를 떠서 image 블록을 본 것만 단정(고객사 A 신종 처방).
- **검수 게이트** (제작 필수 마무리, authoring 3-6 / review.md) - **초안 != 완료, 초안 띡 금지**. `review-draft`(신호 없는 섹션/이미지 없는 산출물 섹션/slop 고신호 0) + 사용자 관점 페르소나 비평(인용 게이트) + 개선=실행(이미지 생성, 약점표 금지). 반영 전제 `gate-review --candidates curriculum-candidates-*.md --report 검수-<회차>.md <교안>` exit 0("왜 이미지 개선 안하냐" 처방).
- **블록 테스트** - 모든 블록은 신호(수강생이 뭘 보고/칠지)만, 빼도 할 일이 안 줄면 삭제, 텍스트/콜아웃량은 원본 밀도 이내 (정본 authoring 3-3절).
- **정본 보호 게이트** (notion-sync 4-0절) - 노션이 정본. 파괴적 쓰기 전 직접 API로 상태/페이지 정체성 확인, 성숙 페이지는 surgical+사전 diff.
- **충실도 쓰기 게이트** (외부 훅, 우회 불가) - `notion_reflect.py` 쓰기는 PreToolUse 훅 `~/.claude/hook-utils/curriculum-write-gate.py`가 가로채 본문 옆 `<본문>.fidelity.json`(이식 원본 `sources` 선언)을 요구하고, 소스에 없는 net-new(발명) 블록 비율이 한도를 넘으면 쓰기를 차단한다(`--skip-gate`로 못 뚫음). 반영 전에 사이드카로 기존 자료 소스를 선언하고 본문을 그 흐름/구조 그대로 이식하라.
- **베이스 선택 라우터 + 발산 게이트** (notion-sync 4-R/4-1절) - 반영 시작 시 노션 `last_edited`로 베이스(로컬/노션)와 방식(surgical 부분 반영/전체교체)을 정한다. 기본 surgical, 전체교체는 신규/의도적 재작성만. 노션 직접 편집(케이스 3)이면 노션을 베이스로 변경만 재적용, 갈라져 애매하면 멈추고 사용자에게 묻는다.
- **round-trip 검증** (notion-sync 4-3절) - 반영 직후 떠서 callout/table/toggle/이미지 보존 확인.

## 실행 순서 (전 주기)

설계(design.md 1절) -> 자료조사(design.md 2절) -> 고객 리뷰(피드백 -> `curriculum-v{N}` 변경이력 헤더) -> 생성(authoring.md, 딥 탐색/미디어 게이트) -> 반영(notion-sync.md, 발산 게이트/round-trip) -> 표기 점검(강의 본문 anti-patterns 기호 rg 0, 코드펜스/URL 제외).

**단계 현황**: `curriculum_gate.py status <워크스페이스> [--draft 교안]`로 어느 Phase까지 통과했는지, 검수 리포트 유무, 다음 필수 게이트를 기계 판정(단계 전환을 산문 추론에 맡기지 않음). 반영 시 `notion_reflect.py --report <검수.md>`가 gate-review를 다시 실행해 검수 루프를 강제한다(`--skip-gate` 우회).

## 관련 지식

- `references/anti-patterns.md` - 강의 자료/스킬 문서에서 피해야 할 AI 티 표기(화살표, em dash, 가운뎃점, 동그라미 숫자, 섹션기호)와 어휘 클리셰
- `project-context-gather` - 다중 소스(Obsidian/Notion/Slack/GWS) context 수집(Phase 2 위임)
- `voice-memos` - 음성 메모 전사(Phase 2)
- `humanize-korean` - AI 티/번역투 탐지/윤문(authoring.md 3-3절 톤 게이트)
- `~/.agents/memory/feedback_avoid_ai_cliche_phrasing.md` - 클리셰 라벨, 추상/비유/얼버무림 금지, 담백/구체
- `notion/SKILL.md` - ntn 명령 레퍼런스, 콜아웃 문법
- `notion-explorer` 서브에이전트(정본 조직 플러그인 `agents/`, 전역 `~/.claude/agents/`는 심링크; 절차 정본 `references/notion-exploration.md`로 Codex 공유) - 노션에서 페이지/DB 좌표, 구조, 반영 베이스 신호(`last_edited`)를 ad-hoc로 찾을 때 위임하는 읽기 전용 haiku 탐색기(본문 덤프 없이 page-id, 경로만 반환 - 인증/워크스페이스/`--limit`/`datasources resolve` 함정 내장). 4-R 베이스 라우터 진입 전 page-id 정체성, `last_edited` 신호 수집에 쓴다. 딥 탐색 explore 게이트(3-0)의 노션 전수는 raw search JSON(`--notion-hits`)이 필요하니 그대로 `ntn /search`로 떠 넘긴다 - 거기엔 쓰지 않는다.
- `curriculum-reviewer` 서브에이전트(정본 조직 플러그인 `agents/`, 전역 `~/.claude/agents/`는 심링크) - 강의 자료를 fresh-context로 검수해 약점+인용+개선안 **리포트만** 반환하는 읽기 전용 검수기(sonnet). review.md 1-3절(린트/페르소나 비평/환각 차단)을 담당하고 개선 실행, iterate, 반영은 메인(4-6절)이 한다. 검수는 이쪽, 좌표 찾기는 notion-explorer - 검수를 탐색기에 보내지 않는다(정본 위임 지정은 review.md 2절).
- `references/image-generation-notion-assets.md` - 새 이미지 생성, 로컬 이미지 노션 삽입, Notion Doc Template 기본 톤
- **골격은 먼저 "라이브냐 VOD냐"로 고른다**:
  - **라이브**(실시간 빌드얼롱) -> `references/template.md`(복붙 프롬프트/단계 중심), 자료 많으면 `references/notion-session-page-template.md`(child_page 분리 변형)
  - **VOD**(녹화 클립) -> `references/vod-clip-template.md`(매뉴얼형 큰 틀: 학습목표/십진헤딩/이미지+표,코드/미션,요약, 개념형,실습형, 설명충 차단)
  - **VOD 녹화 대본**(완성 클립 -> 강사 음성 원고) -> `references/vod-script-generation.md`(인트로/아웃트로 고정 멘트, 자료를 말로 푸는 변환 규칙)
- `references/module-bank.md` - 기존 회차 자료를 모듈로 분해, 적재해 `강의 모듈` DB(재사용 뱅크)를 채우는 절차 + 속성 계약(반대 방향 모듈->회차 조립은 authoring.md 3-0절). DB 좌표는 프로젝트 AGENTS.md.
- `references/live-lecture-operations-tips.md`(운영), `references/live-lecture-delivery-tips.md`(설명/전달) - 라이브 회차 살아있는 문서 2종(상세는 authoring.md 3-5절)
- `~/.agents/memory/feedback_ntn_workspace_switch.md` - Notion 워크스페이스, 이미지/limit/STEP토글 실증
- 프로젝트별 동기화 로그, page id 매핑은 각 프로젝트 `AGENTS.md`에(결정 원장, notion-sync.md 4-2절)
