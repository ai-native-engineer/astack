# Reply to the originating conversation

## Contract

The native conversation ID is the destination; workspace/tab/pane labels are location hints. Never infer the destination from the focused terminal or a similar title.

For an active originating Codex task, run the helper's `receive` in that task's tool call. It verifies `CODEX_THREAD_ID` against the registered conversation and returns one stored reply through the same tool call. This works when Herdr has no native session reference. Keep the yielded process observable and await it; a completed agent turn cannot be awakened by this callback alone.

For an identified terminal conversation, the helper resolves one native ID on an explicitly selected Herdr server and checks foreground ownership and an empty supported prompt. Codex and Claude Code use `herdr agent prompt`. GJC is a custom agent: its private `.gjc/state/sdk/<session-id>.json` descriptor must match the foreground GJC PID, then `herdr pane run` sends literal text and Enter together. Missing or duplicate identities stop delivery. Sending never changes focus or types into a shell. Ignore retained Devin IDs on GJC panes; they are not GJC conversation IDs.

Register a frozen HTML revision. Artifact identity hashes structured fields for the resolved path, revision, agent, native conversation ID, and exact Herdr endpoint. Replies identify the artifact, short revision, and reply ID. Full paths, hashes, question labels, and saved payloads remain available through `inspect <artifact-id> --reply <reply-id>`. Later edits receive a new revision and do not change what an older reply refers to.

Keep a distinctive artifact title and an optional `<meta name="html-reply-context" content="Purpose, prior decisions, current change">` in its source. The header's context view renders this bounded plain-text summary alongside the originating conversation and revision, not inferred chat history. Do not put secrets in the summary. The original-session button is a separate, deliberate navigation action: check the exact native identity and foreground owner twice, select it with `agent focus`, and verify the selected terminal. On macOS, use Swift/AppKit to activate only one existing GUI host found in the exact Herdr endpoint client's process ancestry; otherwise report selection separately from app activation. It may view a working conversation or existing draft, but never submits input, resumes a closed session, or creates a new conversation. A missing or ambiguous session shows an error without guessing. Preview mode blocks navigation. Navigation uses the same loopback Host/Origin/CSRF boundary as submission.

## Compact message

Keep the source reader full width and full height behind a floating bottom composer. Do not paint a full-width backing panel or shrink the source viewport. Empty space around the composer must pass pointer input through to the source. Add end-of-scroll clearance inside the source's document or internal scroll container so its final controls can scroll above the composer. Show the answered count in the dock; keep selections, item notes, quotations, and the read-only outgoing packet in its expandable summary. The user adds an optional overall memo and sends once. Keep per-item notes attached to their item IDs. A selection or keystroke updates the draft, not the agent's task. Preserve the draft when collapsing either the summary or the dock.

Collect visible source headings for the right-side outline rail. Reveal the outline on hover or keyboard focus, allow tap-to-open, and support Escape to close. Clicking an entry scrolls and focuses its source heading without changing the saved source revision. Track the active heading during document and internal-container scrolling. Keep large surfaces and the composer neutral; use a shared blue accent for sending and original-session navigation. Source diagrams may use restrained categorical accents with explicit labels and line styles. Use muted green for answered-question indicators and muted red for unanswered/choice-needed indicators in the outline, progress, and answer summary. Retain explicit state text and checkbox symbols so color is not the only signal; the colors indicate completion, not correctness or approval. Delivery states remain distinct text with gray backgrounds. Do not desaturate source media or evidence screenshots. Verify primary-action and state-label text contrast in both themes.

Use the source-owned question controls and semantics in the confirmation-sheet workflow. Show live question progress near the composer and within the outline, with per-question unanswered links, an unanswered-only filter, and deliberate next-question navigation. Do not mirror editable controls in the panel. Counts track the current draft, not delivery or approval. While a submission is pending, label its frozen preview separately from the next draft; refresh the preview after a terminal receipt. Preserve source focus and caret while updating progress.

For selection annotations, reuse the confirmation-sheet template rather than implementing a second reply panel. Its source-owned note carriers flow through ordinary per-item memos; hidden recovery state is excluded from answers and progress. The source hides its standalone copy/overall-memo controls when framed. Adding or editing a note updates the next draft only and cannot mutate a pending packet or trigger delivery.

Use a Markdown title followed by escaped XML data:

```xml
## Review feedback
<feedback artifact="artifact-id" rev="revision" id="reply-id">
  <answer id="R1">Use first</answer>
  <note for="R1">Keep the real input and output examples.</note>
  <unanswered>R2 R3</unanswered>
  <memo>Apply the structure to the next explanation.</memo>
</feedback>
```

Omit empty sections. Preserve unselected IDs explicitly; an absent choice is not approval. For multiple choices, keep distinct `value` children. Treat quotations and notes as text, escaping XML characters. Do not repeat full question labels, long paths, full hashes, and native conversation IDs in every prompt. Resolve unfamiliar IDs with `inspect` before acting instead of guessing their meanings. Legacy text-only sheets retain their complete answer text.

The read-only preview and actual delivery use the same serializer. Keep the exact submission ID and payload frozen across network retries.

## Operate

`python3 <skill-dir>/scripts/reply-bridge.py --help`를 먼저 실행한다. 구현을 읽지 말고 도구로 쓴다. 공용 상태 디렉터리는 `~/.agents/artifacts/.html-page-replies` 하나다. 격리 테스트는 임시 디렉터리를 쓴다.

1. 등록과 열기는 `publish <file>` 한 번이다. 문법·디자인 검사, 현재 Herdr 패널의 대화 식별, 서비스 기동, 등록, 브라우저 열기를 순서대로 하고 결과 JSON을 낸다. exit 3이면 파일만 열린 미연결 상태이므로 그렇게 보고한다. `--no-open`은 호출자가 브라우저를 직접 열 때만 쓴다.
2. GJC는 패널 cwd의 `.gjc/state/sdk/<session-id>.json` descriptor가 전면 PID를 가리켜야 식별된다. Herdr 라벨은 표시용이다.
3. 원래 Codex 작업이 사용자의 회신을 기다릴 때는 그 세션에서 `receive <artifact-id> --timeout <seconds>`를 실행하고 yielded 도구 프로세스를 기다린다. 돌아온 회신과 revision을 소비한다. 작업이 기다리는 동안에만 대기를 연장하고, 관찰하지 않는 프로세스를 남긴 채 전달됐다고 말하지 않는다.
4. 브라우저에서 렌더, 로컬 미디어, 인용 캡처, 선택, 메모 입력, 영수증을 확인한다. 패널에 상속된 변수는 낡았을 수 있다.
5. 사용자에게 로그(`<state-dir>/service.log`), `stop` 명령, 턴이 끝난 뒤에도 서비스가 남는다는 사실을 알린다. `stop`은 저장된 회신을 보존하고 기록된 프로세스 인스턴스를 확인한 뒤에만 신호를 보낸다. 훅, LaunchAgent, 부팅 등록은 설치하지 않는다.

서비스는 등록된 HTML 스냅샷, 명시적 로컬 미디어 허용 목록, 회신을 저장한다. 로컬 미디어 경로는 읽기 전용이며 range 요청을 지원한다. 큰 React/Babel 페이지와 로컬 영상은 호환된다고 말하기 전에 실제로 연다. 지원하지 않는 자원은 원본 파일로 연다.

## States

| State | Known fact | Next action |
|---|---|---|
| Browser draft | Unsent input exists only in this browser | Send or copy before losing browser state |
| Queued | Stored; waiting for an available agent or prior turn | Continue viewing without screen changes |
| Held | Stored; identity, foreground, or empty input unverified | Inspect the original conversation, then retry or cancel |
| Sent | Herdr accepted terminal input | Check the agent's answer for actual application |
| Received | The originating Codex tool call retrieved the reply | The calling agent handles the returned feedback |
| Uncertain | Input may have been sent before an error/restart | Inspect the conversation; never resend automatically |

Queued replies survive browser closure and service restart. Interrupted sends become uncertain. Repeated clicks reuse one ID. Ordering and active receiver exclusion use the exact Herdr endpoint, agent, and native conversation ID across all artifacts, not display labels. Replies are ordered by creation time, with insertion order breaking ties. An earlier queued, held, sending, or uncertain reply blocks a later callback even on another artifact; receiving a later artifact never consumes the earlier artifact's reply. Handle or cancel an earlier queued/held reply before waiting on a later artifact. Sending/uncertain replies cannot be consumed, cancelled, or automatically retried by the callback.

Only one active receiver may wait for a target, including calls in the same process. Its registration suppresses terminal delivery to that target. Expired or replaced receivers cannot resume consuming replies, and cleanup removes only the caller's own registration. Other endpoints, agents, and conversations remain independent. Terminal delivery also waits for an observed working-to-ready cycle; the callback does not use that gate. It returns one reply to its waiting tool, which must handle the result before starting another receive call.

Use the Herdr skill's inspection/recovery workflow when native identity is missing. Do not overwrite agent metadata, register hooks, start another conversation, or clear user drafts to make delivery succeed.

## Fallback and verification

Without the local service, copy self-contained Markdown with the artifact title/ID/revision, originating agent and full conversation ID plus its display label when present, reply ID, question labels and IDs, all selected values or explicit unanswered markers, item notes, source location, quotation, and overall memo. Copy the frozen pending packet when one exists, not the next draft; capture that packet before requesting the preview so a receipt cannot change it mid-copy. Preserve editor contents and saved form state even when clipboard access fails and manual copying is required. Preserve responses when destination checks fail. Browser storage, server persistence, terminal delivery, and agent application are separate claims.

Test duplicate sends, lost responses, restart, stale/duplicate identity, foreground shells, existing drafts, cross-artifact ordering and receiver ownership, independent targets, cancellation, offline context and frozen-packet copying, and media seeking. Use isolated targets for terminal-input tests.
