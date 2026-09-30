# 세션 소스와 adapter 동작

소스별 `--tool` 선택, `--cwd`/`--files` 해석, transcript 직접 읽기, 제한 환경 fallback이 필요할 때 읽는다.

## 목차

- [Capability](#capability)
- [Claude Code와 Desktop/Cowork](#claude-code와-desktopcowork)
- [Codex](#codex)
- [Grok](#grok)
- [Cursor](#cursor)
- [Gemini CLI와 Antigravity](#gemini-cli와-antigravity)
- [opencode](#opencode)
- [Aside](#aside)
- [OpenClaw / senpi / gjc](#openclaw--senpi--gjc)
- [GitHub Copilot](#github-copilot)
- [사용자 메시지 필터](#사용자-메시지-필터)
- [커버 범위 밖으로 확인한 저장소](#커버-범위-밖으로-확인한-저장소)
- [제한 환경 fallback](#제한-환경-fallback)

## Capability

| `--tool` | 제품 | 세션 명령 | `--cwd` | `show --files` | 안정적 토큰 |
|---|---|---|---|---|---|
| `claude` | Claude Code, Claude Desktop/Cowork | `list`, `timeline`, `rg`, `show` | 메타가 있으면 가능 | 지원 | 지원 |
| `codex` | Codex | `list`, `timeline`, `rg`, `show` | 지원 | 지원 | 지원 |
| `grok` | Grok | `list`, `timeline`, `rg`, `show` | 지원 | 지원 | 지원 |
| `cursor` | Cursor agent transcript, chats store | `list`, `timeline`, `rg`, `show` | 지원 | 지원 | 미지원 |
| `gemini` | Gemini CLI, Antigravity CLI/IDE | `list`, `timeline`, `rg`, `show` | 메타 의존 | 안정적 event 계약 없음 | 미지원 |
| `opencode` | opencode | `list`, `timeline`, `rg`, `show` | DB 세션만 | 지원 | 지원 |
| `aside` | Aside | `list`, `timeline`, `rg`, `show` | 지원 | 지원 | 지원 |
| `openclaw` | OpenClaw, senpi, gjc | `list`, `timeline`, `rg`, `show` | 지원 | 지원 | 지원 |
| `copilot` | GitHub Copilot CLI, VS Code Chat | `list`, `timeline`, `rg`, `show` | 지원 | 지원 | CLI만 |

`sources`는 위 adapter가 지원하는 저장소의 존재 여부와 인덱싱된 세션 수만 보고한다. adapter가 구조적으로 못 읽는 부분은 `source_notes()`로 함께 출력한다. 임의 형식 transcript를 발견하거나 해석하지 않는다.

## Claude Code와 Desktop/Cowork

- `~/.claude/history.jsonl`: 사용자 메시지 preview. 대화형 입력만 기록해 세션의 정본이 아니다.
- `~/.claude/projects/**/*.jsonl`: Claude Code 전체 대화. 정본이며 history에 없는 세션은 여기서 backfill한다.
- `~/.cache/claude-local/{config,cfg}/projects/**/*.jsonl`: `CLAUDE_CONFIG_DIR`을 옮겨 실행한 세션. 스키마 동일.
- `~/Library/Application Support/Claude/claude-code-sessions/**/local_*.json`: Desktop/Cowork 연결 메타
- `~/Library/Application Support/Claude/local-agent-mode-sessions/**/local_*.json`: 격리 세션 메타
- `~/Library/Application Support/Claude/local-agent-mode-sessions/**/.claude/projects/**/*.jsonl`: 격리된 전체 transcript
- Desktop/Cowork 메타의 `cliSessionId`로 UI 세션과 transcript를 연결한다.
- `sessionId`가 없는 history 줄은 버린다. 모으면 서로 다른 프로젝트의 프롬프트가 가짜 세션 하나로 합쳐진다.
- `sources`의 수치는 transcript 기준이라 `list`보다 작다. transcript가 정리된 세션은 `list`에만 남고 `show`는 실패한다.

## Codex

- `~/.codex/history.jsonl`: prompt preview
- `~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl`: 메타, 대화, tool record, patch event, token event
- `~/.codex/archived_sessions/rollout-*.jsonl`: 보관된 세션. 포맷이 같아 함께 인덱싱한다.
- 변경 파일은 `apply_patch`, `patch_apply_begin`, mutation 형태의 `shell` 호출에서 추출한다.
- 세션 이름과 `model_provider`는 `~/.codex/state_5.sqlite`에서 읽어 목록·검색에 보충한다. SQLite가 없거나 읽을 수 없으면 rollout 메타와 첫 사용자 메시지로 계속 표시한다.
- provider가 현재 Codex와 다르면 Codex 자체 `resume` 목록에서 숨을 수 있다. 확인한 provider/profile로 재개하고 rollout이나 SQLite를 직접 수정하지 않는다.
- 다른 앱이 codex를 감싸도 rollout은 `~/.codex/sessions`로 모인다. orca(`codex-runtime-home`)는 hardlink, AionUi는 `cwd=~/.aionui/...`로 나타나 이미 커버된다.

## Grok

- `~/.grok/sessions/<url-encoded-cwd>/<session-id>/summary.json`: 세션 메타
- `~/.grok/sessions/<url-encoded-cwd>/<session-id>/chat_history.jsonl`: 대화와 tool record
- `~/.grok/sessions/<url-encoded-cwd>/prompt_history.jsonl`: prompt preview
- `~/.grok/sessions/<url-encoded-cwd>/<session-id>/updates.jsonl`: token usage
- `~/.grok/sessions/session_search.sqlite`는 Grok 자체 검색 인덱스이며 이 도구의 정본이 아니다.

## Cursor

- `~/.cursor/projects/**/agent-transcripts/**/*.jsonl`: 대화와 tool record. 정본이다.
- `~/.cursor/chats/<workspace>/<agent-id>/store.db`: 같은 세션의 병렬 저장소. `meta` 키 `'0'`이 hex JSON(`agentId`, `name`, `createdAt`, `subagentInfo`, `latestRootBlobId`)이고 `blobs`는 content-addressed DAG다. 루트 블롭이 자식 blob id 32바이트를 대화 순서대로 품는다.
- transcript에 있는 세션은 store.db를 쓰지 않는다. store.db는 compaction 때 앞부분을 잃는다.
- `subagentInfo`가 있는 chats 세션은 subagent로 취급해 기본 제외한다.
- project는 주입된 `Workspace Path`, Cursor project slug, tool working directory 순으로 복원한다.
- timestamp tag가 없으면 파일 수정 시각(chats는 `createdAt`)을 fallback으로 쓴다.
- 변경 파일은 구조화된 편집 도구, `ApplyPatch`, mutation 형태의 shell 호출에서 추출한다. chats의 `tool-call`/`tool-result` part는 `tool_use`/`tool_result`로 정규화한다.

## Gemini CLI와 Antigravity

- `~/.gemini/tmp/*/chats/session-*.jsonl`: Gemini CLI 세션
- `~/.gemini/antigravity-cli/brain/*/.system_generated/logs/transcript_full.jsonl`: Antigravity CLI 전체 transcript
- `~/.gemini/antigravity-cli/cache/conversation_metadata.json`: Antigravity CLI workspace/title 메타
- `~/.gemini/antigravity/conversations/*.pb`: Antigravity IDE 대화 본문. OS 키체인 키로 암호화돼 복원할 수 없다.
- `~/.gemini/antigravity/agyhub_summaries_proto.pb`: 평문 protobuf. 제목·workspace URI·시각만 여기서 읽는다.
- IDE 세션의 `show`는 빈 결과 대신 "본문 암호화로 복원 불가" 표시와 제목을 돌려준다. 빈 목록은 "대화 없음"으로 오독된다.
- 세 형식 모두 stable token usage와 공통 changed-file event 계약은 제공하지 않는다.

## opencode

- `~/.local/share/opencode/opencode.db`: `session`/`message`/`part` 테이블. 본문은 `part.data.type=="text"`, 역할은 `message.data.role`이다.
- `~/.claude/transcripts/*.jsonl`: opencode가 남긴 사본. cwd가 없어 `--cwd` 필터에 걸리지 않고 assistant 답변도 없다.
- 변경 파일은 `edit`/`write`의 `filePath`, `apply_patch`의 `patchText`, `part.data.type=="patch"`의 `files`에서 모은다.

## Aside

- `~/.aside/u/<n>/state.db`: `sessions`(id, title, model, cwd, created_at **초**, parent_id), `session_runs`(token_usage JSON, files_changed)
- `~/.aside/u/<n>/sessions/<YYYY-MM-DD>_<sid>/messages.jsonl`: 대화. timestamp는 **ms**라 초 단위와 섞이지 않게 정규화한다.
- `parent_id`가 있으면 subagent다.

## OpenClaw / senpi / gjc

- `~/.openclaw/agents/main/sessions/*.jsonl`, `~/.senpi/agent/sessions/**/*.jsonl`, `~/.gjc/agent/sessions/**/*.jsonl`
- 세 도구가 같은 스키마를 쓴다. 첫 줄이 `{"type":"session","id","timestamp","cwd"}` 헤더이고 이후 `{"type":"message","message":{"role","content","model","usage"}}`가 이어진다.
- `.jsonl.reset.<ts>`는 같은 세션의 리셋 이전 회차라 `--include-subagents`에서만 보인다.
- `~/.omo/memory/agents/*/runtime/transcripts/*/transcript.jsonl`은 senpi와 세션 ID를 공유하는 사본이라 따로 읽지 않는다.

## GitHub Copilot

- `~/.copilot/session-state/<uuid>/workspace.yaml`: 평면 `key: value`. `id`, `cwd`, `created_at`이 인덱스 소스다.
- `~/.copilot/session-state/<uuid>/events.jsonl`: `user.message`, `assistant.message`, `tool.execution_start`, `session.shutdown`
- `optimistic-chat-*`처럼 UUID가 아닌 디렉토리는 임시 골격이라 세션으로 세지 않는다.
- 토큰은 `session.shutdown.data.modelMetrics[model].tokenDetails`만 쓴다. 같은 노드의 `usage.inputTokens`는 cache를 합산한 값이라 중복 계상된다.
- `~/Library/Application Support/Code/User/workspaceStorage/*/chatSessions/*.json`: VS Code Chat. `requests[].message.text`가 사용자 발화, `response[]`의 `value` part가 답변, `textEditGroup`/`codeblockUri`가 변경 파일이다. cwd는 형제 `workspace.json`의 `folder`에서 읽는다.
- VS Code Chat에는 token usage가 없어 비용 집계에서 빠진다.

## 사용자 메시지 필터

- runtime context, skill 목록, system reminder, synthetic user record는 사용자 의도가 아닌 메타로 처리한다.
- wrapped record는 앞쪽 주입 문맥 대신 마지막 명시적 request block을 쓴다.
- Grok/Cursor는 `<user_query>`를 인식한다.
- Gemini/Antigravity는 `<USER_REQUEST>`와 `<user_query>`를 인식한다.
- Claude는 `<system-reminder>` 블록을 지우고 `<command-args>`를 풀며, `<local-command-stdout>`·`<user-prompt-submit-hook>`·`Caveat:`로 시작하는 줄과 `tool_result` part를 버린다.
- OpenClaw 계열은 `A new session was started via`, `Conversation info (untrusted metadata):`, `[Queued messages while agent was busy]`, `<skill name=`, `<omo-senpi-task>` prefix를 버린다.
- Copilot은 `<skill-context`, `<function_results`, `<tool_result` prefix를 버린다.
- Grok의 `synthetic_reason` record와 알려진 주입 전용 prefix는 제외한다.
- subagent/internal session은 기본 제외하고 요청에 필요할 때만 `--include-subagents`로 포함한다.

## 커버 범위 밖으로 확인한 저장소

같은 대화가 이미 지원 adapter에 잡히거나 구조적으로 못 읽는 것들이다. 재감사 때 중복 조사를 피하려고 남긴다.

- `~/Library/Application Support/orca/codex-runtime-home/home/sessions`: `~/.codex/sessions`와 hardlink된 같은 파일이다.
- `~/Library/Application Support/AionUi/aionui/aionui-backend.db`: GUI 사본. 실제 세션은 codex rollout에 `cwd=~/.aionui/conversations/...`로 남는다.
- `~/.omo/memory/agents/*/runtime/transcripts/*/transcript.jsonl`: senpi와 세션 ID가 같은 사본이다.
- `~/.gemini/antigravity/conversations/*.pb`: 본문 암호화. 요약 인덱스로 메타만 복원한다.
- `~/.codex/state_5.sqlite`(`threads`), `~/.codex/thread_history_1.sqlite`: rollout의 파생 인덱스라 정본이 아니다. 후자는 전체 thread의 일부만 담는다.

## 제한 환경 fallback

스크립트 실행이 막히거나 `show`가 세션 상세를 찾지 못하면:

1. file read 도구로 indexed transcript를 직접 읽는다.
    - Claude: `~/.claude/projects/**/*.jsonl` 또는 연결된 Desktop/Cowork transcript
    - Codex: 해당 `rollout-*.jsonl`
    - Grok: 해당 `chat_history.jsonl`
    - Cursor: 해당 `agent-transcripts/**/*.jsonl`
    - Gemini CLI: 해당 `session-*.jsonl`
    - Antigravity CLI: 해당 `transcript_full.jsonl`
    - opencode: `opencode.db`의 `part` 행 또는 `~/.claude/transcripts/<id>.jsonl`
    - Aside: 해당 `sessions/<date>_<sid>/messages.jsonl`
    - OpenClaw 계열: 해당 `sessions/<id>.jsonl`
    - Copilot: 해당 `session-state/<uuid>/events.jsonl` 또는 `chatSessions/<sid>.json`
2. index ID와 transcript 이름이 다르면 cwd, timestamp, 첫 실제 사용자 요청으로 교차 확인한다.
3. 로컬 transcript가 없으면 그 한계를 밝히고 인접 세션은 보조 근거라고 명시한다.
4. Hermes 대화는 이 도구 대신 `session_search`로 찾는다.
