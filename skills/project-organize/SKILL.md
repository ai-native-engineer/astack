---
argument-hint: "[project-root]"
name: project-organize
description: "프로젝트 폴더를 읽히게 유지한다 - 정본/낡은 파일 가리기(hygiene), nn- 번호 루트 재편(layout), AGENTS.md와 context README 인덱스 맞춤(index). Use when user asks 프로젝트 정리, 루트 재편, 번호 폴더, nn-폴더, 레거시 확인, 정본 찾기, stale 파일, cleanup candidates, AGENTS.md 인덱스, or project-organize. Do NOT use for collecting new context from Slack, Notion, Google Workspace, or other external sources (project-collect), or for rule sentences in AGENTS.md - stale, duplicate, oversized 지침 (update-agents-md)."
---

# Project Organize

프로젝트 안에 쌓인 것을 읽히게 유지한다. 밖에서 새 맥락을 들여오는 짝은 `project-collect`다(Slack·Notion·Google Workspace·Obsidian·음성 메모 등에서의 수집은 그쪽). 모드는 셋이다 - hygiene(정본/낡음 가리기), layout(루트 폴더 이름·순서), index(인덱스 맞춤).

## 모드 먼저 고른다

사용자가 루트 폴더 이름/번호 재편을 요청했으면 hygiene으로 시작하지 않는다.

| 모드 | 요청 신호 | 추가로 읽을 것 |
|---|---|---|
| `hygiene` | 정본, stale, 지울 것, 레거시 | 없음 |
| `layout` | `nn-` 폴더, 루트 재편, 번호로 구분 | `references/layout-renumber.md` |
| `index` | 표/README/인덱스만 맞추기 | 없음 |

요청이 모호하면 어느 모드인지 묻는다. `hygiene`이 기본값인 경우는 정리·정본 찾기를 요청했을 때뿐이고, 구조 요청이면 아니다.

## 공통 워크플로

1. **루트 선정.** 주어진 경로, 없으면 cwd. `pwd -P`와 필요시 `git rev-parse --show-toplevel`로 확정한다.
2. **인덱스는 주장으로 읽는다, 증거로 읽지 않는다.** `AGENTS.md`, 그다음 `README.md`, `context/README.md` 또는 `01-context/README.md`. 중요한 주장은 실제 파일과 대조한다.
3. **`layout`이면:** `references/layout-renumber.md`를 읽고 그 절차를 따른다. 출력도 그 파일의 템플릿을 쓴다.
4. **`hygiene`/`index`면:** truth map을 만들고, 분류하고, 인덱스 drift를 점검한 뒤 제안한다.

## Hygiene: truth map과 분류

정본 자료, source-of-truth 페이지, 산출물, 전사/소스 경로를 식별한다. 명시적 대체 선언("stale", "backup", "do not revert", "Notion is truth")을 표시하고 타임스탬프와 헤더를 확인한다. 파일명만 믿지 않는다.

| 분류 | 의미 |
|---|---|
| `current` | 실제 사용 중이거나 현행 정본으로 지목됨. 인덱스가 이미 정본으로 취급하는 미추적 파일 포함 |
| `reference/archive` | 낡았지만 의도적으로 보존 |
| `stale-risk` | 대체됐을 가능성이 높아 재사용이 위험 |
| `cleanup-candidate` | 아래 빈 폴더 점검을 통과한, 확인된 잡동사니 |
| `unknown` | 사용자 결정 필요 |

**빈 폴더 점검(`cleanup-candidate` 판정 전 필수).** 일반 파일, **숨김 파일**(`.claude/`, 설정, plugin state), 최근 mtime을 본다. 오타처럼 보이는 이름이라도 plugin 설정이 있거나 mtime이 최근이면 에이전트 세션이 작업 디렉터리(cwd)로 쓰고 있는 실험 폴더지 잡동사니가 아니다. `AGENTS.md`가 미래 슬롯으로 지목한 빈 폴더는 예약된 자리다 - 지우지 않는다.

**인덱스 drift**에는 누락 파일, 낡은 "current" 라벨, 오해를 부르는 이름, 미등재 소스, **그리고 파일이 반박하는 인덱스의 상태 주장**(예: 초안 폴더에 발행 기록이 있는데 "발행 0"이라고 적힘)이 들어간다. 경로 갱신과 상태 주장 정정은 사용자가 합치라고 하지 않는 한 별도 커밋이다.

**update-agents-md와의 경계.** 경계는 파일이 아니라 단위다. 경로·id·상태를 주장하는 표 행/목록 항목은 인덱스(이 스킬), 에이전트의 행동을 지시하는 문장은 규칙(`update-agents-md`) - 낡은·중복·분량 초과 지침은 그쪽이다. 한 행에 둘이 섞였으면 행의 소유자는 이 스킬이고, 규칙 문장은 그 자리에서 고치지 말고 `update-agents-md`로 뽑아내는 제안만 낸다.

인덱스 편집을 요청받으면 짧고 사실만 남긴다. 긴 연대기는 로그에 두고 작업 인덱스에 두지 않는다.

## 제안 후 실행

어떻게 정리할지 간단히 알린다: 이동, 삭제, 인덱스 편집, 커밋 단위. 거기서 멈추고, 이동·삭제·인덱스 편집·커밋 전에 명시적 승인을 기다린다.

승인 후:

- 명시적 승인 없이 삭제하지 않는다. 검토 목록이나 archive 이동을 우선한다.
- 첨부, 소스 export, 백업은 잡동사니로 확인되기 전까지 보존한다.
- Notion 등 외부 시스템이 걸려 있으면 점검이 로컬 한정인지 라이브 검증인지 밝힌다.
- git repo면 검증 후 승인된 작업을 커밋한다. 승인되고 손댄 경로만 stage한다.
- 이름을 바꿀 대상에 다른 세션의 미커밋 편집이 이미 있으면 커밋 전에 알린다. 기다리거나, 포함한다면 그 편집을 명시한다. rename 속에 숨기지 않는다.
- 승인 후 파일 변경이 없으면 커밋을 생략하고 이유를 말한다.

## 출력 (hygiene / index)

사용자가 다른 형식을 요구하지 않으면 이 형태를 쓴다. 빈 섹션은 접는다. `layout`은 `references/layout-renumber.md`의 템플릿을 쓴다.

```markdown
## Current Truth
- <경로 또는 소스> - <왜 현행 정본인가>

## Stale Risks
- <경로> - <왜 재사용이 위험한가>

## Cleanup Candidates
- <경로> - <근거와 제안 조치>

## Index Drift
- <파일> - <누락, 오해 소지, 반박된 주장>

## Proposed Actions
- <이동/삭제/편집/커밋 범위>

## Actions Taken
- <승인 후 수행한 편집·이동>

## Needs Decision
- <사용자 승인이 필요한 질문>
```
