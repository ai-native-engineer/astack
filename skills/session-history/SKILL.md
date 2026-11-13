---
argument-hint: "[query]"
name: session-history
description: "Use for: 로컬 AI 세션(Claude, Codex, Cursor 등)의 검색, 전사, 도구 호출, 변경 파일, 토큰과 비용 조회. 지금 세션의 진행 정리와 남은 일은 session-wrapup, 반복 작업에서 스킬 후보 발굴은 skill-harvest."
---

# Session History

Claude Code, Codex, OMP, Cursor와 다른 지원 런타임의 로컬 대화 로그를 조회한다. 제품을 지정하면 `--tool omp|claude|codex`처럼 출처를 고정한다. OMP는 native title 메타데이터 뒤의 session header를 읽으며 과거 파일을 변환하거나 옮기지 않는다.


Hermes Agent 자체 대화(Discord/Telegram/Gateway/CLI)는 이 스크립트 대상이 아니다. Hermes 대화는 `session_search` 도구가 `~/.hermes/state.db`를 검색한다.

## 빠른 사용

```bash
SH="scripts/session_history.py"
python3 $SH sources
python3 $SH list --cwd
python3 $SH rg gcloud "cloud run" --since <YYYY-MM-DD> --sort relevance --limit 5
python3 $SH show <session-id> --grep gcloud
python3 $SH show --last --full
python3 $SH show <session-id> --files
python3 $SH redact
```

서브커맨드는 `sources`, `list`, `timeline`, `rg`/`grep`, `show`, `redact`다. `--tool`의 기본값은 `all`이다. 전체 도구와 옵션은 `python3 $SH <subcommand> -h`를 먼저 본다.


## 워크플로

1. **현재 프로젝트 복원**: `list --cwd`로 후보를 좁히고 `show <session-id>`로 대화를 읽는다. 남은 작업을 복원할 때는 `references/session-sources.md`의 "작업 상태 복원"을 따른다.
2. **특정 작업이나 주제의 맥락 모으기**:
    1. 이전 세션이 남긴 결론(메모리, 보고서)이 있으면 먼저 읽는다. 위치는 전역 지침(AGENTS.md, rules)에 적힌 메모리와 산출물 경로를 따른다. 산출물 파일명에 세션 ID가 있으면 그 ID로 바로 `show`한다.
    2. 동의어를 `rg` 한 번에 모두 넘긴다(`rg A B C`, OR). 키워드마다 `rg`를 반복 호출하지 않는다. 호출마다 전체 로그를 다시 읽는다.
    3. 기간은 "최근 N일"이면 `--days N`, 시작일이 정해져 있으면 `--since`로 준다. 세션이 많으면 `--sort relevance`로 주제를 실제로 다룬 세션을 위로 올린다.
    4. 고른 세션은 `show <id> --grep <키워드>`로 일치한 곳과 앞뒤만 읽는다. 출력 끝의 이어 읽기 명령을 그대로 쓰면 번호 기준이 맞는다.
    5. Codex 세션 이름과 provider는 `list --search`로 찾는다.
3. **오늘 작업 정리**: `timeline`을 시간순 데일리 노트 초안으로 쓴다.
4. **장기 현황**: `list --days 30 --summary`로 범위를 좁힌 뒤 필요한 날짜·프로젝트만 `list`로 확인

## 핵심 동작

- `rg`는 전사의 대화와 도구 기록을 검색한다. Codex는 연결된 분할 전사와 누락된 사용자 입력을 함께 읽으며, 입력 기록에서 보충한 항목은 출처를 표시한다. 키워드는 대소문자를 무시한 고정 문자열이고, `-E`를 붙이면 정규식이 된다.
- `rg`는 기본으로 최근 세션 순이며 `--limit`은 그 순서로 자른다. `--sort relevance`는 맞힌 키워드 종류 수, 대화(사용자, 어시스턴트) hit 수, 전체 hit 수 순이다. 흔한 키워드 하나는 그 말이 든 파일을 여러 번 읽은 세션에 도구 출력 hit로 쌓이기 때문이다.
- 현재 세션과 이 스크립트를 부른 도구 기록(지난 검색의 메아리)은 `rg`에서 빠진다. `--include-self`를 붙이면 포함된다.
- `rg --format json`의 세션 행 키는 `sid`, `tool`, `project`, `start`, `first_ts_ms`, `hit_count`, `talk_count`, `terms`, `fpath`, `hits`이고, `hits` 항목 키는 `role`, `time`, `ts`, `term`, `excerpt`다. `start`와 `time`은 로컬 시각이다.
- `show`의 `#번호`는 세션 안 위치다. 대화만 볼 때와 도구 기록을 포함할 때(`--full`, `--grep`) 기준이 달라서 `--offset`도 같은 모드로 준다.
- `show`는 도구 출력을 텍스트에서 300자, JSON에서 500자로 줄인다. `--grep`을 쓰면 일치한 위치 주변을 남기고, `--full` 없이도 도구 기록까지 찾는다.
- 복원 경고가 있으면 전사 마지막 답변을 마지막 작업으로 단정하지 않는다. `history` 출처는 사용자 입력만 복원한 것이며, 빠진 답변이나 실행 완료를 증명하지 않는다. JSON에서도 행의 `source`와 stderr 경고를 함께 확인한다.
- 모든 출력은 시크릿을 가린 뒤 나간다. JSON은 직렬화 전에 문자열 값만 가려 키와 숫자, 참/거짓, null의 구조를 보존한다. 원문이 필요하면 `--raw`를 붙인다. 로그에는 사용자가 붙여넣은 키가 그대로 있어, 무심코 검색하면 그 값이 다시 컨텍스트와 새 로그로 번진다.
- 세션 ID는 prefix 매칭한다. 충돌을 피하려면 목록의 12자리 이상을 그대로 쓴다.
- 모든 도구의 주입 컨텍스트는 사용자 의도가 아니다. `<user_query>`·`<USER_REQUEST>` 블록을 우선하고 Claude의 `<system-reminder>`, `<command-args>`, hook 출력은 걷어낸다.
- Claude 압축 컨텍스트는 `summary`로 구분하고, 작업 완료 알림은 일반 검색에서 제외하며 `show --full`에서 길이를 제한한 도구 결과로만 표시한다.
- subagent/internal은 지원되는 native 식별자에 한해 기본 제외한다. Claude/ Cursor `subagents/`, Cursor chats `subagentInfo`, OpenClaw reset archives와 Codex exec 세션은 `--include-subagents`로 포함한다. OMP `parentSession`만으로 worker를 추정하지 않으며 ordinary fork/continuation은 보존한다.
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
- 백업에는 지운 키가 원문으로 남는다. 백업은 소유자만 읽게 만들고 기존 백업은 덮어쓰지 않지만, 치환을 확인한 뒤 백업까지 지워야 키가 디스크에서 사라진다. 백업을 남긴 채 회수가 끝났다고 보고하지 않는다.
- 지울 때는 `sk-`·`ntn_`·`AIza`처럼 **모양이 확실한 키만** 건드린다. 화면 마스킹이 함께 쓰는 `token=...` 이름 기반 휴리스틱은 `token=3` 같은 멀쩡한 기록까지 덮어써, 되돌릴 수 없는 쪽에서는 놓치는 것보다 부수는 것이 비싸다.
- 살아 있는 세션의 파일은 `--exclude`로 빼고 그 세션이 끝난 뒤 돌린다. 자기 세션만이 아니라 **동시에 떠 있는 다른 세션도** 해당한다. 그 세션은 자기가 들고 있는 상태로 로그를 다시 쓰므로, 치환해도 그 위에 덮여 사라진다.
- `--apply` 뒤에 인자를 그대로 두고 한 번 더 세어 0인지 확인한다. 남아 있으면 그 파일을 누가 다시 쓰고 있다는 신호다.
- 텍스트 로그만 고친다. sqlite처럼 바이너리로 저장하는 소스는 건너뛰므로 그쪽 키는 이 명령으로 사라지지 않는다.
- Codex paginated rollout이 치환 대상이면 `--apply` 전체를 중단한다. 원본 길이를 바꾸면 분할 기록의 byte offset이 어긋나므로 조회 마스킹을 사용한다.
- 파일을 지워도 그 키가 외부로 나간 사실은 남는다. 회수는 교체를 대신하지 못한다.

## 토큰·비용

토큰/비용만 필요하면 `python3 scripts/token_usage.py`를 실행한다. 제품별 조회는 세션 명령과 동일한 `--tool`을 지정한다.

```bash
python3 scripts/token_usage.py --days 7 --cost --by-model
python3 scripts/token_usage.py --month --cost --quota
```

Cursor, Gemini, VS Code Copilot Chat transcript에는 안정적인 token usage가 없어 토큰·비용 집계에서 제외한다. 단가, 모델 해석, cache, quota 세부와 전사 파일을 직접 집계할 때의 함정은 `references/cost-measurement.md`를 읽는다.

## 대화 맥락 교정 대응

사용자가 “이전에 이 내용으로 대화했어”, “전에 확인했잖아”, “면밀하게 확인해봐”처럼 과거 대화 기반으로 교정하면 추측보다 세션 검색을 먼저 수행한다.

1. 이 스킬의 `rg` 또는 Hermes의 `session_search`로 과거 발화와 키워드를 찾는다.
2. 찾은 메시지와 현재 live config/state를 각각 확인한다.
3. 답변에서 과거 합의와 현재 상태를 짧게 구분한다.
