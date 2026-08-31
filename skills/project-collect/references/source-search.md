# 소스별 검색법과 로컬 설정 조회

소스별 명령 레시피와 로컬 설정 조회법을 모은 단일 소스. 검색 실행 단계에서 이 파일을 읽고 해당 소스 절차를 따른다. SKILL.md 본문에는 소스 목록만 둔다.

`../<skill>/...` 형태의 sibling 명령은 이 `project-collect` 스킬 디렉터리에서 실행한다.

## 목차

- Obsidian
- 음성 4소스 (voice-memos 스킬로 빠짐없이)
- Notion (workspace/alias 조회)
- Slack
- 카카오톡
- Google Workspace (gog 등록 계정)
- 미팅/강의 녹화 (OBS·화면녹화)

## Obsidian

- `rg -l -i "키워드" "$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/llm-wiki"` → 관련 노트 원문을 아카이브에 통합. 앱 미실행이어도 rg 동작.

## 음성 4소스 (voice-memos 스킬로 빠짐없이)

- 이 스킬 디렉터리에서 `python3 ../voice-memos/scripts/search.py --keyword <키워드>`를 실행하면 `[음성 메모]`·`[에이닷]`(통화녹음)·`[메모]`(Apple Notes) **3소스를 한 번에** 인덱싱한다.
- 같은 단계에서 Caret MCP(`caret_search_notes`+`caret_search_knowledge` 병렬)로 `[Caret]`까지 더해 **4소스**를 모은다.
- 검색어는 **키워드 단독이 아니라 도메인 인접어도 함께** 넣는다 (예: '그랜터'뿐 아니라 '셀러 OS'·'셀러').
- **동음이의 주의** — 본문으로 관련성을 확정한다 (예: '그랜터'=이커머스 SaaS vs 프라이머 액셀러레이팅 발표).
- **manifest에 4라벨별 hits/kept를 각각 보고**한다. 0건이어도 라벨마다 '0건'을 명시한다 (라벨 통째 누락 금지).
- 저장: 전사본은 대형이라 **항목당 1파일**로 둔다.
- **파일명 prefix는 실제 출처로** 한다 — 음성메모 `YYMMDD-voice-<제목>.md`, 통화녹음 `YYMMDD-call-<상대>.md`, Apple Notes `YYMMDD-note-<제목>.md`, Caret `YYMMDD-caret-<제목>.md` (출처를 caret로 뭉뚱그리지 말 것).
- 각 파일 헤더에 출처·원본파일(m4a/통화 txt/노트 ID)·일시를 명기한다.
- 혼합 인덱스는 `YYMMDD-voice-<키워드>-아카이브.md`에 라벨별 목록·요지·링크만 둔다.
- 한 건씩 가져와 즉시 파일로 쓰고 컨텍스트에서 비운다.
- 원본 m4a/통화 txt는 `attachments/`에 보존한다.
- 우선순위: 음성메모 > 통화 > Notes > Caret. 전사 불가는 무시한다.
- **키워드 0건이어도 끝내지 말 것** — 미팅 녹음은 발화에 회사명·키워드가 나오지 않을 수 있다. 0건이면 날짜 범위와 미전사 원본으로 폴백한다.
  - ① 프로젝트 활동 기간(최소 최근 1~2주)을 `search.py --date`로 훑어 제목·미리보기로 관련성 판정.
  - ② Recordings 원본 폴더(`~/Library/Group Containers/group.com.apple.VoiceMemos.shared/Recordings/*.{m4a,qta}`)와 전사본 날짜 목록(`~/.voice-memos/transcripts/`)을 대조해 **미전사 원본**을 찾아 `extract.py`(무출력 스킵 시 apple-stt 직접)로 전사 후 재판정.

## Notion (workspace/alias 조회)

- workspace ID는 `ntn`의 `~/.config/notion/workspaces.json`, alias는 `~/.config/notion/aliases.json`이 정본이다.
- 등록 대상 확인: `python3 ../notion/scripts/ntn-ws.py --list`.
- 검색: `python3 ../notion/scripts/ntn-ws.py <workspace-or-alias> api /v1/search -d '{"query":"키워드","page_size":10,"sort":{"direction":"descending","timestamp":"last_edited_time"}}'`.
- 관련 페이지 원문 전체 수집: `python3 ../notion/scripts/ntn-ws.py <workspace-or-alias> pages get <page-id>`.
- 검증: `python3 ../notion/scripts/ntn-ws.py <workspace-or-alias> api /v1/users/me`의 `workspace_name`을 확인한다.

## Slack

- `agent-slack`로 채널·스레드 검색 → 관련 채널의 전체 메시지(루트+답글)를 1개 아카이브로, 첨부는 `attachments/`.

## 카카오톡

- `kakaotalk` 스킬로 채팅방·대화 검색 → 관련 대화(기간·방 이름을 헤더에 기록)를 1개 아카이브로, 첨부는 `attachments/`.

## Google Workspace (gog 등록 계정)

- `gog auth list -j`와 `gog auth alias list`로 등록 계정 전수를 확인하고, 각 계정을 `-a <account-or-alias>`로 직접 검색한다.
- OAuth refresh token이 없어도 `service_account`로 등록된 계정은 도메인 위임으로 검색될 수 있으므로 인증 유형만 보고 미리 제외하지 않는다.
- Gmail=관련 메일 본문 전문을 이메일 아카이브 1개로+첨부, Calendar=관련 이벤트 상세, Drive=관련 파일 원본을 `attachments/`로.
- 실제 호출해 **에러나 No results인 계정만** 스킵·사유 기록.

## 미팅/강의 녹화 (OBS·화면녹화)

- `~/Movies` 등에서 `*.mp4`/`*.vtt`를 찾아 `apple-stt`(또는 `mlx_whisper`)로 전사 → 전사본은 대형이므로 **녹화당 1파일**(`YYMMDD-<제목>-전사.md`), 원본 mp4는 `attachments/`.
- 강의 녹화면 전사 인용으로 **학습자 막힘 포인트 표**를 만들어 차기 회차 교안/과제 반영의 입력으로 둔다.
- 사용자가 녹화 경로를 주거나 미팅·회차 직후 맥락 수집일 때만 포함.
