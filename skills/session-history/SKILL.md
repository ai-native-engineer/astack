---
argument-hint: "[query]"
name: session-history
description: "Claude Code and Codex local JSONL session history lookup: lists, timelines, full conversation details, tool calls, grep/search, and token usage. Use for Claude/Codex 작업 내역, 오늘 한 일, 뭐 했더라, history. Do NOT use for Hermes Agent/Discord/Gateway conversations in ~/.hermes/state.db — use session_search instead. Do NOT use for personal reflection synthesis, automation packaging, memory updates, or searching current repo files."
---

# Session History

Claude Code (`~/.claude/`) + Codex (`~/.codex/`) 통합 세션 히스토리.

Hermes Agent 자체 대화(Discord/Telegram/Gateway/CLI)는 이 스크립트 대상이 아니다. Hermes 대화는 `session_search` 도구가 `~/.hermes/state.db`를 검색한다.

토큰 사용량만 필요하면 설치된 `session-history` 스킬 루트에서 `python3 scripts/token_usage.py`를 실행해 로컬 JSONL의 Claude `usage`와 Codex `token_count`를 파싱한다(`--all-time` 지원).

## 사용법

네 서브커맨드: `list`(목록)·`timeline`(시간순, 데일리 노트용)·`rg`(세션 전문 검색)·`show`(대화 보기). `grep`도 같은 검색의 호환 alias다. 대표 호출:

```bash
SH="scripts/session_history.py"  # 설치된 session-history 스킬 루트에서 실행
python3 $SH list --cwd                # 현재 프로젝트 오늘 세션 (절대 경로 포함)
python3 $SH rg "gcloud" --days 30     # 30일간 세션 JSONL 전문 검색 (맥락 발췌)
python3 $SH rg "error" --days 30 --limit 5  # 실패 신호가 있는 세션 5개만 보기
python3 $SH show --last --files       # 가장 최근 세션의 수정 파일 목록
```

서브커맨드별 옵션은 다르다. 특히 `--limit`은 `show`·`rg`에만 있고 `list`엔 없다(목록 범위는 `--days`/`--date`로 조절). 출력 형식은 `--format text|json`만 받는다(`compact` 값 없음 — 압축 출력은 `timeline --compact` 전용 플래그). 페이지네이션용 `--offset`은 없다. 그 밖의 플래그는 실행 전 `python3 $SH <subcommand> -h`로 확인한다.

비자명한 동작:

- `rg`는 `list --search`(history.jsonl preview)와 달리 **실제 세션 JSONL의 대화·도구 호출·도구 결과**를 검색한다.
- `rg --limit N`은 매칭 세션 수를 제한한다. 세션 안에서는 앞 3개 매칭만 요약하고, 전체 맥락은 `show <ID> --full`로 본다.
- 세션 ID는 prefix 매칭. 목록의 12자리를 그대로 붙여넣는 것을 권장 (UUID v7 특성상 앞 8자리는 동시 생성 세션끼리 충돌 가능).
- `--files`는 두 섹션을 출력한다:
  - **구조화된 파일 변경** — `Edit`/`Write`/`MultiEdit`/`NotebookEdit` + Codex `apply_patch`/`patch_apply_begin`에서 경로 추출.
  - **Bash/shell 변경 의심** — `rm`/`mv`/`cp`/`sed -i`/`tee`/`>` 등 파일 변경 패턴이 든 `Bash` 호출 및 Codex `shell` call.

## 워크플로우

1. **현재 프로젝트 맥락 복원**: `list --cwd` → `show <ID>` 또는 `show --last`
2. **특정 작업 찾기**: `rg "키워드"` (7일 기본) → `show <ID>`
3. **오늘 데일리 노트**: `timeline` → 출력 복사 붙여넣기
4. **전체 목록**: `list --days 7` → 세션 ID와 파일 경로 확인

## 대화 맥락 교정 대응

사용자가 “이전에 이 내용으로 대화했어”, “전에 확인했잖아”, “면밀하게 확인해봐”처럼 과거 대화 기반으로 교정하면, 바로 추측성 답을 고치지 말고 **세션 검색을 먼저 수행**한다. 특히 Hermes 설정/모드/게이트웨이 상태처럼 현재값과 과거 합의가 함께 중요한 질문은:

1. `session_search` 또는 이 스킬의 `rg`로 과거 발화/키워드를 찾는다.
2. 찾은 세션의 핵심 메시지와 현재 live config/state를 각각 확인한다.
3. 답변은 “과거 대화에서 무엇을 확인했는지”와 “현재 상태가 그와 일치하는지”를 짧게 구분해 말한다.

이 패턴은 사용자의 교정 신호가 강한 경우 우선 적용한다. 단순히 현재 컨텍스트에 플래그가 안 보인다는 이유로 “확인 불가”라고 끝내면 안 된다.

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
