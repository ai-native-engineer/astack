---
argument-hint: "[query]"
name: session-history
description: Claude Code + Codex 통합 세션 히스토리 조회. 세션 목록, 전체 대화 내역, 도구 호출 포함 상세 보기를 지원. Use when user says "오늘 뭐 했지", "세션 히스토리", "session history", "작업 내역", "오늘 한 일", "뭐 했더라", "history", "대화 내역", or wants to review past Claude Code/Codex sessions.
---

# Session History

Claude Code (`~/.claude/`) + Codex (`~/.codex/`) 통합 세션 히스토리.

토큰 사용량만 필요하면 `python3 ~/.claude/skills/session-history/scripts/token_usage.py`로 로컬 JSONL의 Claude `usage`와 Codex `token_count`를 파싱한다(`--all-time` 지원).

## 사용법

### 세션 목록 (list)

```bash
python3 ~/.claude/skills/session-history/scripts/session_history.py                          # 오늘 세션 목록 (파일 경로 포함)
python3 ~/.claude/skills/session-history/scripts/session_history.py list --cwd               # 현재 디렉토리 프로젝트만
python3 ~/.claude/skills/session-history/scripts/session_history.py list --date 2026-03-17
python3 ~/.claude/skills/session-history/scripts/session_history.py list --days 7
python3 ~/.claude/skills/session-history/scripts/session_history.py list --search pytest     # 키워드 검색 (preview 기준)
```

목록에 각 세션의 절대 파일 경로가 기본으로 표시된다.

### 타임라인 (timeline) — 데일리 노트용

```bash
python3 ~/.claude/skills/session-history/scripts/session_history.py timeline                 # 오늘 시간순 타임라인
python3 ~/.claude/skills/session-history/scripts/session_history.py timeline --days 3        # 최근 3일
python3 ~/.claude/skills/session-history/scripts/session_history.py timeline --cwd           # 현재 프로젝트만
python3 ~/.claude/skills/session-history/scripts/session_history.py timeline --compact       # 중간 스냅샷 생략
```

모든 세션을 시간순으로 나열. 데일리 노트 붙여넣기에 바로 쓸 수 있는 형태.

### 전문 검색 (grep) — 실제 대화 내용 검색

```bash
python3 ~/.claude/skills/session-history/scripts/session_history.py grep "gcloud"            # 기본 7일간 전문 검색
python3 ~/.claude/skills/session-history/scripts/session_history.py grep "gcloud" --days 30  # 30일간
python3 ~/.claude/skills/session-history/scripts/session_history.py grep "gcloud" --cwd      # 현재 프로젝트만
```

`list --search`와 달리 history.jsonl preview가 아닌 **실제 세션 JSONL 파일 전문**을 검색. 키워드 주변 맥락 발췌 포함.

### 세션 대화 보기 (show)

```bash
python3 ~/.claude/skills/session-history/scripts/session_history.py show --last              # 가장 최근 세션
python3 ~/.claude/skills/session-history/scripts/session_history.py show <세션ID>            # 대화만
python3 ~/.claude/skills/session-history/scripts/session_history.py show <세션ID> --full     # 도구 호출 포함
python3 ~/.claude/skills/session-history/scripts/session_history.py show <세션ID> --files    # 수정된 파일 목록만
python3 ~/.claude/skills/session-history/scripts/session_history.py show <세션ID> --limit 20 # 앞 20개만
python3 ~/.claude/skills/session-history/scripts/session_history.py show <세션ID> --format json
```

`show` 결과 헤더에 세션 파일 절대 경로가 표시된다.

세션 ID는 prefix 매칭. 목록에 표시되는 12자리를 그대로 붙여넣는 것을 권장 (UUID v7 특성상 앞 8자리는 동시 생성 세션끼리 충돌 가능).

`--files`는 두 섹션을 출력한다:
- **구조화된 파일 변경** — Claude Code의 `Edit`/`Write`/`MultiEdit`/`NotebookEdit`와 Codex의 `apply_patch`/`patch_apply_begin`에서 경로를 직접 추출해 집계.
- **Bash/shell 변경 의심** — `rm`/`mv`/`cp`/`sed -i`/`tee`/`>` 등 파일 변경 패턴이 포함된 Claude `Bash` 호출 및 Codex `shell` function call.

## 공통 옵션

| 옵션 | 값 | 설명 |
|------|-----|------|
| `--tool` | `all`, `claude`, `codex` | 조회할 도구 (기본: all) |
| `--format` | `text`, `json` | 출력 형식 (기본: text) |
| `--cwd` | flag | 현재 작업 디렉토리 기준 프로젝트 필터 (list/timeline/grep 공통) |
| `--include-subagents` | flag | Claude Code(`/subagents/`)·Codex(`exec`/swarm) 세션 포함. 기본은 제외 |

## 워크플로우

1. **현재 프로젝트 맥락 복원**: `list --cwd` → `show <ID>` 또는 `show --last`
2. **특정 작업 찾기**: `grep "키워드"` (7일 기본) → `show <ID>`
3. **오늘 데일리 노트**: `timeline` → 출력 복사 붙여넣기
4. **전체 목록**: `list --days 7` → 세션 ID와 파일 경로 확인

## 데이터 소스

### Claude Code
- `~/.claude/history.jsonl`: user 메시지 인덱스 (display, timestamp(ms), sessionId, project)
- `~/.claude/projects/{path}/{sessionId}.jsonl`: 전체 대화 (user/assistant/tool_result)

### Codex
- `~/.codex/history.jsonl`: user 메시지 인덱스 (text, ts(sec), session_id)
- `~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl`: 전체 대화 (event_msg/response_item)

## 제한 환경 fallback (Restricted environment)

서브에이전트·샌드박스에서 `session_history.py`/`claude` CLI가 Bash 권한으로 막히거나, `show <ID> --full`이 세션 상세 대신 날짜 목록만 반환할 때:

1. **JSONL 직접 Read**: 스크립트 대신 `~/.claude/projects/<cwd-매핑-디렉토리>/<sessionId>.jsonl`을 Read 도구로 직접 읽는다. cwd의 `/`는 `-`로 치환되어 디렉토리명이 됨 (예: cwd `/` → `-` 디렉토리).
2. **ID 형식 불일치**: `history.jsonl`의 sessionId는 uuid-v4, transcript 파일명은 `ses_*` 형식이라 직접 매칭이 안 될 수 있다. 안 맞으면 **timestamp + cwd**로 교차 탐색해 같은 세션을 찾는다.
3. **세션 파일 부재**: 요청한 session_id가 `projects/`에 아예 없으면, 같은 cwd에서 나온 형제 세션·회고(`~/.agents/memory/retros/`)를 timestamp 기준으로 교차 참조해 맥락을 복원하고, 로컬에 파일이 없다는 한계를 명시한다.
