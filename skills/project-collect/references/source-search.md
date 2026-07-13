# 소스별 검색법 + workspace-id·account-email 테이블

소스별 명령 레시피와 하드코딩된 식별자(Notion workspace-id, gog 계정 이메일)를 모은 단일 소스. 검색 실행 단계에서 이 파일을 읽고 해당 소스 절차를 따른다. SKILL.md 본문에는 소스 목록만 둔다.

## 목차

- Obsidian
- 음성 4소스 (voice-memos 스킬로 빠짐없이)
- Notion (workspace-id 매핑)
- Slack
- Google Workspace (gog 계정 후보)
- 미팅/강의 녹화 (OBS·화면녹화)

## Obsidian

- `rg -l -i "키워드" "$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/<your-vault>"` → 관련 노트 원문을 아카이브에 통합. 앱 미실행이어도 rg 동작.

## 음성 4소스 (voice-memos 스킬로 빠짐없이)

- 검색 진입점: `python3 ~/.claude/skills/voice-memos/scripts/search.py --keyword <키워드>`가 `[음성 메모]`·`[에이닷]`(통화녹음)·`[메모]`(Apple Notes) **3소스를 한 번에** 인덱싱한다.
- 같은 단계에서 Caret MCP(`caret_search_notes`+`caret_search_knowledge` 병렬)로 `[Caret]`까지 더해 **4소스**를 모은다.
- 검색어는 **키워드 단독이 아니라 도메인 인접어도 함께** 넣는다 (예: 'A사'뿐 아니라 그 회사 제품명·관련 약어).
- **동음이의 주의** — 본문으로 관련성을 확정한다 (예: 'A사'=이커머스 SaaS vs 같은 이름의 다른 행사).
- **manifest에 4라벨별 hits/kept를 각각 보고**한다. 0건이어도 라벨마다 '0건'을 명시한다 (라벨 통째 누락 금지).
- 저장: 전사본은 대형이라 **항목당 1파일**로 둔다.
- **파일명 prefix는 실제 출처로** 한다 — 음성메모 `YYMMDD-voice-<제목>.md`, 통화녹음 `YYMMDD-call-<상대>.md`, Apple Notes `YYMMDD-note-<제목>.md`, Caret `YYMMDD-caret-<제목>.md` (출처를 caret로 뭉뚱그리지 말 것).
- 각 파일 헤더에 출처·원본파일(m4a/통화 txt/노트 ID)·일시를 명기한다.
- 혼합 인덱스는 `YYMMDD-voice-<키워드>-아카이브.md`에 라벨별 목록·요지·링크만 둔다.
- 한 건씩 가져와 즉시 파일로 쓰고 컨텍스트에서 비운다.
- 원본 m4a/통화 txt는 `attachments/`에 보존한다.
- 우선순위: 음성메모 > 통화 > Notes > Caret. 전사 불가는 무시한다.
- **키워드 0건이어도 끝내지 말 것** — 미팅 녹음은 발화에 회사명·키워드가 아예 안 나오는 경우가 흔하다 (실측 2026-06-10 아머스포츠: 관련 2건 모두 키워드 검색 누락). 0건 시 폴백:
  - ① 프로젝트 활동 기간(최소 최근 1~2주)을 `search.py --date`로 훑어 제목·미리보기로 관련성 판정.
  - ② Recordings 원본 폴더(`~/Library/Group Containers/group.com.apple.VoiceMemos.shared/Recordings/*.{m4a,qta}`)와 전사본 날짜 목록(`~/.voice-memos/transcripts/`)을 대조해 **미전사 원본**을 찾아 `extract.py`(무출력 스킵 시 apple-stt 직접)로 전사 후 재판정.

## Notion (workspace-id 매핑)

- 모든 호출에 `NOTION_WORKSPACE_ID=<workspace-id>`를 붙인다.
- 매핑:
  - 워크스페이스명=ID로 매핑한다. 예: `<팀A>=<workspace-id>`, `<팀B>=<workspace-id>`, `<개인>=<workspace-id>` (`ntn api /v1/users/me`의 `workspace_name`으로 ID 확인)
- 검색: `NOTION_WORKSPACE_ID=<workspace-id> ntn api /v1/search -d '{"query":"키워드","page_size":10,"sort":{"direction":"descending","timestamp":"last_edited_time"}}'`
- 관련 페이지 원문 전체 수집: `NOTION_WORKSPACE_ID=<workspace-id> ntn pages get <id>`
- 검증: `NOTION_WORKSPACE_ID=<workspace-id> ntn api /v1/users/me`의 응답 `workspace_name`으로.

## Slack

- `agent-slack`로 채널·스레드 검색 → 관련 채널의 전체 메시지(루트+답글)를 1개 아카이브로, 첨부는 `attachments/`.

## Google Workspace (gog 계정 후보)

- 먼저 `gog auth list`로 등록 계정 전수를 뽑고, **각 계정을 `gog -a <email>`로 직접 검색**한다 (예 `gog -a <work-account@example.com> gmail search "키워드"`).
- **OAuth refresh token이 없어도 `service_account`로 등록된 계정은 `-a`로 Gmail/Calendar/Drive가 그대로 검색된다** (도메인 와이드 위임, 실측 2026-06-08) — "OAuth 없음"으로 미리 스킵하지 말 것.
- 계정 후보: `gog auth list`에 나오는 모든 계정(개인 Gmail + 회사 Workspace 이메일).
- Gmail=관련 메일 본문 전문을 이메일 아카이브 1개로+첨부, Calendar=관련 이벤트 상세, Drive=관련 파일 원본을 `attachments/`로.
- 실제 호출해 **에러나 No results인 계정만** 스킵·사유 기록.

## 미팅/강의 녹화 (OBS·화면녹화)

- `~/Movies` 등에서 `*.mp4`/`*.vtt`를 찾아 `apple-stt`(또는 `mlx_whisper`)로 전사 → 전사본은 대형이므로 **녹화당 1파일**(`YYMMDD-<제목>-전사.md`), 원본 mp4는 `attachments/`.
- 강의 녹화면 전사 인용으로 **학습자 막힘 포인트 표**를 만들어 차기 회차 교안/과제 반영의 입력으로 둔다.
- 사용자가 녹화 경로를 주거나 미팅·회차 직후 맥락 수집일 때만 포함.
