---
name: project-collect
description: "Collects project context from Slack, Notion, Google Workspace, Obsidian, voice notes, recordings, and local sources into per-source archives under the current project's context folder with attachments preserved. Use when user asks 프로젝트 맥락 모아줘, 맥락 가져와줘, context 수집, 자료 모아줘, collect project context, or project-collect. Do NOT use for project cleanup, stale-file review, AGENTS.md maintenance, external web/YouTube research, company public research, daily brief, or source-specific actions without archiving."
---

# Project Collect

주제(키워드)를 받아 등록된 도구들을 검색하고, **관련 맥락을 소스당 1개 통합 아카이브로 정리**해 `01-context/company/`에 저장한다. 원본 파일은 그대로 보존한다. 외부 웹/유튜브 리서치는 하지 않는다.

> **이름 기준**: 신규 호출과 문서에서는 `project-collect`를 쓴다.

> **출력 위치(하위호환)**: 신규 프로젝트는 `01-context/company/`. 기존 `context/`만 있는 레거시 프로젝트는 그대로 `context/`에 머지한다 — `01-context/company/`가 있으면 그걸, 없고 `context/`가 있으면 그걸 쓴다(`scripts/context_status.py`도 같은 순서로 해소). 신규 생성 시에만 `01-context/company/`.

## 출력 형태 (가장 중요)

목표는 "히트 전수 덤프"가 아니라 **사람이 바로 읽는 통합 맥락 아카이브**다.

항목 크기에 따라 두 방식으로 나눈다.

- **메신저류(Slack·카톡·짧은 메일 등)는 소스당 1개 `.md` 아카이브**로 합친다. 스레드별로 파일을 흩뿌리지 않는다.
  - 상단: 수집 계정/채널·범위·수집일, 핵심 인물 표, 주요 결정사항, **다른 소스와의 교차참조**.
  - 본문: 관련 항목의 **원문 전체를 시간순으로 빠짐없이**. 요약 아닌 원문. 정리는 구조(헤더·순서·표)로만.
- **대형 항목(미팅 전사본·녹취·긴 문서)은 항목당 1파일**로 둔다. 한 파일에 다 합치려 하지 않는다(컨텍스트·파일 크기 초과 방지).
  - 같은 소스의 대형 항목들은 인덱스 아카이브 1개(`...-아카이브.md`)에 목록·핵심 요지·각 파일 링크만 두고, 전문은 개별 파일에.
  - 파일명: `YYMMDD-<소스>-<제목>.md` (예: `260408-caret-구글-미팅.md`).
- **원본 파일(첨부·문서·녹음)은 `attachments/`에 사람이 읽는 이름으로 보존**한다. `260530-F0B5...-image.png` 같은 기계 이름 금지 → `1주차_강의자료.pdf`처럼. 같은 파일은 한 번만(해시로 dedupe). 추출 텍스트가 있으면 `.pdf`+`.txt` 함께.
- 아카이브 .md와 하위폴더 모두 파일명 앞에 날짜 `YYMMDD-`를 붙인다(아래 날짜 규칙).

## 재실행 머지 (upsert — 덮어쓰기·중복 파일 금지)

같은 소스 아카이브가 `01-context/company/`에 이미 있으면 새 파일을 만들거나 통째로 덮어쓰지 않는다. 기존 파일을 읽어 **증분 병합**한다(없을 때만 새로 생성). 같은 소스의 재실행이 항상 "처음부터 최신 상태로 쓴 한 파일"로 읽혀야 한다.

메타데이터는 아카이브 맨 위 **YAML frontmatter**가 단일 소스다 (스키마·소스별 anchor·머지 절차 전부: `references/archive-schema.md`).

- **증분 기준점(anchor)**: 재수집 전 기존 anchor를 읽어 그 이후만 검색 — `python3 scripts/context_status.py 01-context/company --source <소스>`. slack=마지막 ts(`--oldest`), gmail=마지막 날짜(`after:`) 등. anchor 없으면 본문 항목과 dedupe.
- **풀 리스캔 예외**: 사용자가 "처음부터 끝까지 수집해줘" 류로 명시 요청할 때만 anchor를 무시하고 전 범위 재검색. 이때도 새 파일을 만들지 않고 기존 항목과 dedupe하며 같은 아카이브에 머지한다.
- **본문 증분**: 기존 항목 보존, 직전 수집 이후 신규 항목만 시간순 제자리에 dedupe(같은 ts·내용 제외)해 끼워 넣는다.
- **frontmatter 갱신**: `collected_last`=오늘, `range_end`=새 최신 항목일, `anchor`=새 마지막 키, `items` 갱신. `collected_first`·`range_start`는 불변.
- **결정·인물**: 새 사실 추가, 기존 줄 보존, 충돌하는 옛 결정만 최신으로 교체(옛 값 `→ 변경`).
- 현황 한눈: `python3 scripts/context_status.py 01-context/company`.

## 관련성 게이트 (저장 전 필수)

검색은 부분일치로 무관한 걸 대량 긁는다. 저장 전에 **"이게 정말 이 프로젝트(예: A사) 맥락인가?"**를 판정한다.

- 키워드를 **정확 매칭** 우선으로 본다. 회사명이 흔한 일반어를 포함하면(예: "○○엔지니어링"), 그 일반어 단독 매칭(일반 프롬프트 엔지니어링 페이지, 타사명 등)은 버린다.
- 자동 알림(CRM 문의알림 등), 무관 채널, 일반 지식 페이지는 제외한다.
- 빈 export(블록 0·본문 0)는 저장하지 않고 manifest에 "빈 export"로 기록.
- 애매하면 버리지 말고 목록으로 사용자에게 확인받는다.

## 입력

- 인자에서 키워드를 추출한다. 모호하면 한 번 묻는다. 띄어쓰기 변형(예: `선 엔지니어링`)도 함께 검색한다.
- 파일명 맨 앞 `YYMMDD`는 **그 자료가 작성·발생한 날짜**(아카이브는 범위의 대표일 또는 최신일). 수집일이 아니다. 못 구하면 오늘로 폴백하고 수집일은 헤더에만.

## 사전 준비

1. 날짜 확보: `date +%y%m%d`, `date +%Y-%m-%d`.
2. `mkdir -p 01-context/company/attachments`.
3. **수집 의도 파악** — 구조화 질문 도구가 현재 런타임에서 가능하면 먼저 묻는다. 도구가 없거나 Default mode 제한으로 실패하면 같은 질문을 재시도하지 말고 `intent="포괄적 전수"`로 두고 진행한다. 이 의도가 관련성 판정의 기준이 되고, 그대로 서브에이전트에 전달된다. 의도는 "무엇이 관련 있나"(범위 축)만 정한다 — "언제부터 찾나"(시간 축)는 항상 anchor 이후 증분이 기본(재실행 머지 섹션).
   - 질문: "`<키워드>` 맥락, 어디까지 모을까요? (기존 아카이브가 있으면 지난 수집 이후 증분만 수집됩니다)"
   - 프리셋 옵션 2개(구조화 질문 도구의 옵션 스키마 대응): ① `전체 (프로젝트 전반 모두 수집)` ② `토픽 집중 — Other(자유입력)로 범위 지정`. ②를 자유입력 없이 그대로 고르면 범위를 되묻는다(빈 채로 넘어가는 사고 방지). 그 외 "특정/니치" 같은 프리셋은 만들지 않는다.
   - `전체` 선택 → intent="포괄적 전수". 자유입력 → intent=그 문구(예: "2회차 청주 운영만", "계약·정산만").
   - 자유입력으로 "처음부터 끝까지 수집해줘" 류(처음부터 다시/전 기간 재수집)가 오면 **풀 리스캔**: anchor를 무시하고 전 범위를 재검색하되, 기존 항목과 dedupe하며 같은 아카이브에 머지한다.
4. **소스 — 기본셋으로 바로 진행 + 한 줄 확인** (매번 묻지 않는다)
   - 기본 소스: **Slack, Notion, gog(Gmail·Calendar·Drive), Obsidian, 음성 4소스(음성메모·에이닷 통화녹음·Apple Notes·Caret)**.
   - 검색 시작 전 한 줄로 알린다: `기본 소스로 진행합니다 → Slack · Notion · gog · Obsidian · 음성4소스(음성메모·통화·Notes·Caret). 빠지거나 뺄 소스 있으면 알려주세요 (예: "카톡도", "Slack 빼고", 또는 아래 카탈로그 참고).` 그리고 **바로 진행한다**(블로킹 질문 X).
   - 사용자가 추가·제외를 말하면 그에 맞춰 소스 집합을 조정해 재진행한다.
   - 사용자가 명시적으로 "소스 고를래/선택지 보여줘"라고 할 때만 카탈로그를 펼쳐 고르게 한다.

### 소스 카탈로그 (누락 방지용 — 평소엔 한 줄 안내에 링크만)

내가 쓰는 도구뿐 아니라 **고객사가 쓸 법한 도구**까지 둬서 빠진 소스를 사용자가 잡게 한다. 기본셋 밖은 해당 도구 연동(스킬/CLI/MCP)이 있을 때만 실제 수집한다.

- 메신저: Slack(기본) · 카카오톡 · Teams · Discord · 라인
- 문서/지식: Notion(기본) · Obsidian(기본) · Confluence · Google Docs(gog) · 사내 위키
- 메일/일정/드라이브: Gmail·Calendar·Drive(gog, 기본) · Outlook/M365
- 개인: 음성메모 · 에이닷 통화녹음 · Apple Notes · Caret (모두 기본 — voice-memos 스킬 `search.py`가 앞 3개를 통합, Caret은 MCP 병렬)
- 녹화: OBS 미팅·강의 녹화(`~/Movies/`·`~/Movies/obs/*.mp4`·화면녹화 mp4/vtt) — apple-stt/mlx_whisper로 전사. 강의 녹화면 학습자 막힘 포인트를 뽑아 차기 회차 교안/과제에 반영(→ `curriculum`)
- 이슈/PM: Jira · Linear · Asana · GitHub Issues
- 저장소: Google Drive(기본) · Dropbox · 로컬 폴더

## 실행 모드 (서브에이전트 / 메인)

두 모드가 있다. 별도 질문 없이 **인자·한마디로 선택**하고, 없으면 **의도 기반 기본값**을 쓴다. 소스 안내 줄 옆에 현재 모드를 한 줄로 표시한다.

- **서브에이전트 모드**(`--sub`): 소스별 병렬, 메인 컨텍스트 보호, 대량·다소스에 강함. 품질·일관성은 다소 낮음.
- **메인 모드**(`--main`): 메인이 모든 소스를 직접 처리. 품질·소스 간 교차참조 최상, 단 컨텍스트 무겁고 순차라 느림.
- 오버라이드: `--main`/`--sub` 인자 또는 "메인으로"/"서브로" 한마디.
- **기본값**: 니치 의도 → 메인 모드 / 포괄적 의도 → 서브에이전트 모드.

## 수집 메커니즘

검색은 발견 단계일 뿐, 관련 항목은 원문 전체를 끌어온다. 무거운 원문은 메인 컨텍스트에 적재하지 않는다. 어느 모드든 **intent 기준 관련성 게이트 → 소스당 통합 아카이브 1개 + attachments 원본**은 동일하다.

**서브에이전트 모드**
- 소스당 `source-collector` 서브에이전트에 위임(`subagent_type: source-collector`). 선택된 소스를 병렬로 띄운다.
- 위임 프롬프트에 전달: `source`, `keyword`(+변형), **`intent`(그대로 전달)**, `out_dir`(`01-context/company`), `today`(YYMMDD), 계정/워크스페이스/채널 범위.
- 에이전트는 manifest(아카이브 경로·hits/kept/excluded·uncertain·첨부)만 반환. 메인은 `uncertain`을 모아 사용자 확인, `hits/kept/excluded`로 과수집·누락 점검.

**메인 모드**
- 메인이 소스를 순차로 직접 검색·정리한다. CLI는 대용량 원본을 `>` 리다이렉트로 파일 직행(검증 `head`/`wc`만), 한 소스를 아카이브로 저장한 뒤 다음 소스로 넘어가 컨텍스트를 비운다.
- 관련성 게이트·아카이브 형식·manifest 점검은 동일하게 메인이 수행한다.

## 소스별 검색법

소스별 명령 레시피와 로컬 설정 조회법은 컨텍스트가 무거우니 본문에 두지 않는다. 검색 실행 단계에서 `references/source-search.md`를 읽고 해당 소스 절차를 따른다.

대상 소스(상세는 `references/source-search.md`):

- Obsidian
- 음성 4소스 (음성메모·에이닷 통화녹음·Apple Notes·Caret — voice-memos 스킬로 빠짐없이)
- Notion (등록 workspace/alias 조회)
- Slack (`agent-slack`)
- Google Workspace (gog — Gmail·Calendar·Drive, 등록 계정 전수)
- 미팅/강의 녹화 (OBS·화면녹화)

## 아카이브 형식

맨 위 **YAML frontmatter**(메타 단일 소스) + 본문(핵심 인물 표·주요 결정사항·교차참조·시간순 원문 전체). 새 아카이브는 `templates/archive-template.md`를 복사해 시작하고, 전체 필드·anchor·머지 규칙은 `references/archive-schema.md`를 따른다.

## 마무리 요약

저장된 아카이브·attachments 목록, 소스별 관련 항목 수 / 제외 수(사유), 검색 못 한 소스 사유를 출력한다. 파일 작성 후 `file -I`로 UTF-8 확인.
