---
argument-hint: "[설계|맥락수집|자료조사|자료생성|검수개선|노션반영]"
name: curriculum
description: "입문자/비개발자 대상 강의, 교육과정, 교안, 실습, 워크숍, B2B 기업교육 자료를 설계, 제작, 수정, 검수/개선, Notion 반영하는 전 주기 스킬. Use when user asks for 커리큘럼, 강의 설계, 차시 설계, 학습목표, 교안/강의안 작성, 실습 설계, 회차 자료, 교안 검수, 강의 자료 노션 반영. Do NOT use for 단순 Notion 검색/CRUD, 일반 문서 작성, Google Workspace 조작, 음성 전사, 또는 교육과 무관한 리서치."
---

# Curriculum - 강의/교육과정 전 주기 (설계 -> 맥락수집 -> 자료조사 -> 자료생성 -> 검수/개선 -> 노션반영)

Backward Design + ADDIE 하이브리드 기반. 맥락 수집부터 검수, 선택적 발행까지 한 흐름이다. 설계/맥락수집/자료생성/검수는 도구 비종속이고, 자료조사는 프로젝트가 선언한 소스만 쓴다. **Notion 반영은 프로젝트가 발행 채널로 Notion을 쓸 때만** `ntn`으로 실행한다. `[대괄호]`는 상황에 맞게 채운다.

## 라이프사이클 (6 Phase - 어느 단계부터든 진입 가능, 해당 작업에 들어가면 그 reference를 읽는다)

| Phase | 무엇 | 읽을 것 |
|---|---|---|
| 1. **설계** | 무엇을/왜 가르치나 - 목표, 차시 분해, 평가, 버전관리, B2B/B2C | [`references/design.md`](references/design.md) 1절 |
| 2. **맥락수집** | 고객/수강생/요구 context 수집 - `project-collect`에 위임 (다중소스 검색, 음성 전사, 아카이브) | [`references/design.md`](references/design.md) 2절 |
| 3. **자료조사** | 프로젝트가 선언한 기존 강의자료 소스 탐색 -> 후보 원문 비교 -> `gate-candidates` 통과 | [`authoring.md`](references/authoring.md) 3-0절 (+모듈 적재 module-bank.md) |
| 4. **자료생성** | 회차 페이지 작성 **+ 자기검수**(초안 != 완료) - 기존 자료 이식, 콘텐츠 원칙, 라이브 운영, 제작 직후 검수 루프 | [`authoring.md`](references/authoring.md) 3-1~3-6절 + [`review.md`](references/review.md) (+골격은 라이브냐 VOD냐로: 라이브 template.md / VOD vod-clip-template.md, 이미지 image-generation-notion-assets.md) |
| 5. **검수/개선** | 사용자 관점으로 비평하고 **실제로 고친다**(약점표 금지) - 제작 마무리 겸 단독 진입 | [`references/review.md`](references/review.md) |
| 6. **노션반영** | 프로젝트가 Notion 발행을 선언한 경우: 공통 쓰기 안전선 -> 베이스 선택 -> surgical 또는 전체교체 -> round-trip. `notion` 스킬/`ntn`이 없으면 실행하지 않는다. | `notion` 스킬의 `references/ntn-cli.md` + [`references/notion-sync.md`](references/notion-sync.md) |

## 불변 원칙 (모든 Phase 공통)

- **AI 창작이 아니라 사람의 검증 자료가 기본값, 약간의 개선만** - 모든 Phase의 헌법. 기존 검증 자료를 베이스로 최소 개선하고, AI 자율 미감으로 새로 짓거나(특히 이미지) 멀쩡한 걸 방치 판단하지 않는다. 왜, 3대 실패패턴, 판단원칙은 [`references/author-intent.md`](references/author-intent.md)(제작/검수 시작 전 1회 읽기).
- **핵심만, 신호 우선** - 모든 블록은 수강생이 *뭘 보고/칠지*(명령어, 출처, 실제 화면)만 담는다. 빼도 할 일이 안 줄면 삭제.
- **개념은 명료하게** - 한 줄 정의 -> 직관적 단계 -> 복붙 프롬프트. 잡설 제거와 개념 흐리기는 다르다.
- **산문 최소, 불렛/넘버링/표 우선** - 세 문장 넘는 줄글은 쪼갠다. 검수는 전체 줄 수가 아니라 문단 밀도로 본다. 블록 테스트/콜아웃/표기 규칙 상세는 authoring 3-3절, anti-patterns.md.
- **논리 구조는 항상 고객, 수강생 중심** - 사고 사슬은 1. 수강생 피드백/설문 -> 2. 만들고 싶다고 한 주제 -> 3. 그래서 이번 회차에 만드는 것 -> 4. 만들기 위해 가르칠 개념(기존 자료 이식). 개념->실습 순으로 정리하지 않는다.
- **입문자, 비개발자 전제** - 존댓말, 부담 낮게.
- **용어 첫 등장 1줄 풀이** - 괄호 인라인 풀이는 금지(자연스러운 문장으로 녹인다).
- **딥 탐색 -> 최선 선택 -> 비판적 검토 후 이식** (무비판 복붙 금지):
  1. 프로젝트가 선언한 소스를 함께 탐색한다. 기본 후보 수는 10개이며, 범위가 작거나 소스가 적으면 근거를 남기고 낮춘다.
  2. 비판적으로 비교해 최선을 고른다.
  3. 약점(낡음, 잡설, 이미지 부실, 도메인 불일치)을 검토한 뒤 이식한다.
  - 통째 이식하되 도메인(고객사, 팀, 예시)만 치환한다. 구체를 일반 라벨로 희석하지 않는다.
  - 원본 밀도가 상한선이다(불리면 비대). 이 단계는 딥 탐색 게이트가 강제한다 - 상세는 authoring 3-0절(제작) / review.md(검수).
- **안전선**: 위험/보안 우회 명령(인증서 검증 끄기 등)은 학습자 본문, 강사 메모 어디에도 금지. 내부 모순 금지(저장 안 되면 "시제품", 되면 "도구"). 시간 현실성(한 블록에 풀코스 금지).

## 품질 게이트 (작성/반영 시 필수 - 상세는 각 reference)

깨지기 쉬운 단계는 산문이 아니라 게이트 스크립트가 산출물/exit-code로 강제한다. **게이트 통과는 응답에 (실행 명령, 통과 여부, 핵심 출력 라인)을 인용해야 인정**한다 - 증거 없이 단정하지 않는다. 각 게이트의 명령과 근거 사고는 [`README.md`](README.md) 게이트 원장 + 해당 reference.

- **딥 탐색 게이트** - 프로젝트가 선언한 기존 자료를 충분히 봤고 후보 원문을 비교했는지 강제한다. 상세 authoring 3-0절 / review.md 0절.
- **미디어 게이트** - 원본의 이미지/첨부가 교안에 다 이식됐는지 대조한다(누락 차단). 상세 authoring 3-0절.
- **환각 차단 게이트** - 단정/반영에 적은 page-id의 실존/접근을 검증한다(이미지 누락은 미디어 게이트가 대조). 상세 review.md 3절.
- **검수 게이트** - **초안 != 완료**. 검수가 약점표에서 멈추지 않고 실제 개선(텍스트 + 이미지)까지 갔는지 강제한다(반영 전제). 상세 authoring 3-6절 / review.md.
- **블록 테스트** - 모든 블록은 신호만, 빼도 할 일이 안 줄면 삭제, 원본 밀도 이내. 정본 authoring 3-3절.
- **정본 보호 게이트** - Notion 공통 쓰기 안전선은 `notion` 스킬이 정본이다. 프로젝트가 Notion published pages를 정본으로 선언한 경우에만 성숙 페이지 surgical 반영과 자산 보존 규칙을 추가한다.
- **충실도 쓰기 게이트** - 반영 전 사이드카로 기존 자료 소스를 선언한다. 지원하는 호스트 훅이 없으면 같은 검사를 수동 실행한다.
- **베이스 선택 라우터 + 발산 게이트** - 반영 시작 시 노션 최신본 신호로 베이스(로컬/노션)와 방식(surgical/전체교체)을 정한다. 기본 surgical, 갈라져 애매하면 멈추고 사용자에게 묻는다. 상세 notion-sync 4-R/4-1절.
- **round-trip 검증** - 반영 직후 페이지를 떠서 콜아웃/표/토글/이미지 보존을 확인한다. 상세 notion-sync 4-3절.

## 실행 순서 (전 주기)

설계(design.md 1절) -> 맥락수집(design.md 2절) -> 고객 리뷰(피드백 -> `curriculum-v{N}` 변경이력 헤더) -> 자료조사(authoring.md 3-0) -> 자료생성(authoring.md 3-1~3-6) -> 검수/개선(review.md) -> 표기 점검 -> 프로젝트가 Notion 발행을 쓰면 반영(notion-sync.md, 발산 게이트/round-trip).

**단계 현황**: `status`는 archives를 제외한 후보/검수/교안 산출물과 다음 실행할 게이트를 보여주는 가시성 도구다. 파일 존재만으로 Phase 통과를 판정하지 않는다. 실제 통과는 해당 게이트 명령의 exit 0과 핵심 출력으로 확인한다. 명령은 README.md / notion-sync.md.

## 관련 지식

- `references/anti-patterns.md` - 강의 자료/스킬 문서에서 피해야 할 AI 티 표기(화살표, em dash, 가운뎃점, 동그라미 숫자, 섹션기호)와 어휘 클리셰
- `project-collect` - 다중 소스(Obsidian/Notion/Slack/GWS) context 수집(Phase 2 위임)
- `voice-memos` - 음성 메모 전사(Phase 2)
- `humanize-korean` - AI 티/번역투 탐지/윤문(authoring.md 3-3절 톤 게이트)
- `notion/references/ntn-cli.md` - Notion 공통 쓰기 안전선, ntn CLI, 워크스페이스 전환
- `notion-explorer` - Notion 좌표와 `last_edited` 신호만 찾는 읽기 전용 탐색기. 딥 탐색용 raw search JSON은 직접 `ntn /search`로 만든다.
- `curriculum-reviewer` - fresh-context 검수 리포트만 반환한다. 실제 개선, iterate, 반영은 메인이 한다.
- `references/image-generation-notion-assets.md` - 새 이미지 생성, 로컬 이미지 노션 삽입, Notion Doc Template 기본 톤
- **골격은 먼저 "라이브냐 VOD냐"로 고른다**:
  - **라이브**(실시간 빌드얼롱) -> `references/template.md`(복붙 프롬프트/단계 중심), 자료 많으면 `references/notion-session-page-template.md`(child_page 분리 변형)
  - **VOD**(녹화 클립) -> `references/vod-clip-template.md`(매뉴얼형 큰 틀: 학습목표/십진헤딩/이미지+표,코드/미션,요약, 개념형,실습형, 설명충 차단)
  - **VOD 녹화 대본**(완성 클립 -> 강사 음성 원고) -> `references/vod-script-generation.md`(기본 인트로/아웃트로, 자료를 말로 푸는 변환 규칙)
- `references/module-bank.md` - 기존 회차 자료를 모듈로 분해, 적재해 `강의 모듈` DB(재사용 뱅크)를 채우는 절차 + 속성 계약(반대 방향 모듈->회차 조립은 authoring.md 3-0절). DB 좌표는 프로젝트 AGENTS.md.
- `references/live-lecture-operations-tips.md`(운영), `references/live-lecture-delivery-tips.md`(설명/전달) - 공통 라이브 원칙. 회차별 로그는 프로젝트 로컬에 둔다.
- 프로젝트별 동기화 로그, page id 매핑은 각 프로젝트 `AGENTS.md`에(결정 원장, notion-sync.md 4-2절)
