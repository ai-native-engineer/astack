---
argument-hint: "[query]"
name: session-history
description: "Claude, Codex, Cursor 등 로컬 AI 에이전트 세션의 목록·전사·도구 호출·변경 파일·토큰·비용을 검색하고 로그의 키를 마스킹한다. Use for 과거 작업·세션·사용량 조회. Do not use for Hermes state.db, 현재 저장소 검색, 회고 작성, 메모리 갱신."
---

# Session History

Claude Code/Desktop Cowork, Codex, Grok, Cursor, Gemini CLI/Antigravity, opencode, Aside, OpenClaw/senpi/gjc, GitHub Copilot(CLI/VS Code)의 로컬 대화 로그를 하나의 CLI로 조회한다.

Hermes Agent 자체 대화(Discord/Telegram/Gateway/CLI)는 이 스크립트 대상이 아니다. Hermes 대화는 `session_search` 도구가 `~/.hermes/state.db`를 검색한다.

## 빠른 사용

```bash
SH="scripts/session_history.py"
python3 $SH sources
python3 $SH list --cwd
python3 $SH rg "gcloud" --days 30 --limit 5
python3 $SH show --last --full
python3 $SH show <session-id> --files
python3 $SH redact
```

서브커맨드는 `sources`, `list`, `timeline`, `rg`/`grep`, `show`, `redact`다. `--tool`은 `all|claude|codex|grok|cursor|gemini|opencode|aside|openclaw|copilot`을 받으며 기본값은 `all`이다. 전체 옵션은 `python3 $SH <subcommand> -h`를 먼저 본다.

## 워크플로

1. **현재 프로젝트 복원**: `list --cwd`로 후보를 좁히고 `show <session-id>`로 대화를 읽는다.
2. **특정 작업 검색**: `rg "키워드"`로 실제 대화와 도구 기록을 검색하고 필요하면 `show --full`로 확장한다.
   Codex 세션 이름과 provider도 `list --search` 검색 대상이며 목록에 함께 표시된다.
3. **오늘 작업 정리**: `timeline`을 시간순 데일리 노트 초안으로 쓴다.
4. **장기 현황**: `list --days 30 --summary`로 범위를 좁힌 뒤 필요한 날짜·프로젝트만 `list`로 확인

## 핵심 동작

- `rg`는 preview가 아니라 실제 transcript의 대화·도구 호출·도구 결과를 검색한다.
- 모든 출력은 시크릿을 가린 뒤 나간다. 원문이 필요하면 `--raw`를 붙인다. 로그에는 사용자가 붙여넣은 키가 그대로 있어, 무심코 검색하면 그 값이 다시 컨텍스트와 새 로그로 번진다.
- 세션 ID는 prefix 매칭한다. 충돌을 피하려면 목록의 12자리 이상을 그대로 쓴다.
- 모든 도구의 주입 컨텍스트는 사용자 의도가 아니다. `<user_query>`·`<USER_REQUEST>` 블록을 우선하고 Claude의 `<system-reminder>`, `<command-args>`, hook 출력은 걷어낸다.
- subagent/internal 세션은 기본 제외한다. Claude `subagents/`, Cursor `subagents/`와 chats의 `subagentInfo`, OpenClaw `.jsonl.reset.*`, Codex `exec` 세션이 모두 여기 해당하며 `--include-subagents`로 켠다.
- `show --files`는 구조화된 편집 호출과 mutation 형태의 shell 호출을 모은다. Gemini는 안정적인 changed-file event 계약이 없어 빈 결과가 무변경을 보장하지 않는다.
- `sources`는 지원 adapter의 저장소와 인덱싱 수를 보여준다. adapter가 못 읽는 부분은 `·` 주석으로 함께 밝힌다(Claude의 transcript 없는 세션, Antigravity IDE 암호화 본문 등). 임의 형식 로그를 자동 해석하지는 않는다.
- Codex의 세션 이름과 provider는 보조 SQLite 인덱스에서 읽어 보충한다. 이 값은 검색·표시용이며 transcript를 대체하지 않는다.
- Codex provider가 `myproxy` 등으로 표시된 세션은 일반 `codex resume` 목록에서 숨을 수 있다. 목록의 세션 ID와 provider를 확인한 뒤 같은 profile/실행 래퍼로 재개한다.
- `sources`의 Claude 수치는 transcript 기준이라 `list` 결과보다 작다. 프롬프트 기록만 남은 세션은 `list`에 나오지만 `show`는 실패한다.

소스별 경로, capability, project 복원, 제한 환경 fallback이 필요하면 `references/session-sources.md`를 읽는다.

## 로그에 남은 키 지우기

마스킹은 화면만 가리고 파일에는 원문이 남는다. 키가 실제로 노출돼 회수해야 하면 `redact`가 로그 파일 자체를 고친다.

```bash
python3 $SH redact                                  # 세기만 한다
python3 $SH redact --path ~/proj --exclude <live>   # 대상 추가, 특정 경로 제외
python3 $SH redact --apply                          # 백업 후 치환
```

- 기본은 세기만 한다. `--apply`가 있어야 파일을 고치고, 고치기 전에 대상 전체를 `tar.gz`로 백업한 뒤 되돌리는 명령을 찍는다.
- 지울 때는 `sk-`·`ntn_`·`AIza`처럼 **모양이 확실한 키만** 건드린다. 화면 마스킹이 함께 쓰는 `token=...` 이름 기반 휴리스틱은 `token=3` 같은 멀쩡한 기록까지 덮어써, 되돌릴 수 없는 쪽에서는 놓치는 것보다 부수는 것이 비싸다.
- 살아 있는 세션의 파일은 `--exclude`로 빼고 그 세션이 끝난 뒤 돌린다. 자기 세션만이 아니라 **동시에 떠 있는 다른 세션도** 해당한다. 그 세션은 자기가 들고 있는 상태로 로그를 다시 쓰므로, 치환해도 그 위에 덮여 사라진다.
- `--apply` 뒤에 인자를 그대로 두고 한 번 더 세어 0인지 확인한다. 남아 있으면 그 파일을 누가 다시 쓰고 있다는 신호다.
- 텍스트 로그만 고친다. sqlite처럼 바이너리로 저장하는 소스는 건너뛰므로 그쪽 키는 이 명령으로 사라지지 않는다.
- 파일을 지워도 그 키가 외부로 나간 사실은 남는다. 회수는 교체를 대신하지 못한다.

## 토큰·비용

토큰/비용만 필요하면 `python3 scripts/token_usage.py`를 실행한다.

```bash
python3 scripts/token_usage.py --days 7 --cost --by-model
python3 scripts/token_usage.py --month --cost --quota
```

Cursor, Gemini, VS Code Copilot Chat transcript에는 안정적인 token usage가 없어 토큰·비용 집계에서 제외한다. 단가, 모델 해석, cache, quota 세부는 `references/cost-measurement.md`를 읽는다.

## 대화 맥락 교정 대응

사용자가 “이전에 이 내용으로 대화했어”, “전에 확인했잖아”, “면밀하게 확인해봐”처럼 과거 대화 기반으로 교정하면 추측보다 세션 검색을 먼저 수행한다.

1. 이 스킬의 `rg` 또는 Hermes의 `session_search`로 과거 발화와 키워드를 찾는다.
2. 찾은 메시지와 현재 live config/state를 각각 확인한다.
3. 답변에서 과거 합의와 현재 상태를 짧게 구분한다.
