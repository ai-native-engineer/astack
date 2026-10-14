# Gmail / Google Chat Channel Overlay

Apply this after the common communication contract when the selected channel is Gmail or Google Chat through `gog`.

## Gmail

- Decide whether the task is a new email, reply, forward, or draft.
- Confirm sender account, recipient, subject, and body before sending.
- Prefer drafts for long, external, legal, billing, or high-stakes messages unless the user explicitly asks to send now.
- Use a subject that names the decision, request, or context packet.
- In replies, preserve the thread context and answer the latest actionable ask first.
- Include links/files only when the user approved the attachment or the source is safe to share.
- Do not include secrets, tokens, passwords, or unredacted private data.

## Draft to Sent

Applies when the user sends the message themselves: a draft-only account, or a draft the user wants to edit first.

1. Save the draft through `gog` and read it back (thread, sender, recipient, body). Report which parts were read back and which were not, such as whether the quoted original made it in.
2. When the user asks for a change, update that draft. A second draft of the same reply can be sent by mistake or left behind as a stale copy.
3. After the user says it was sent, find the message in the sent mail by recipient, not by draft ID, and read its body. Users often edit before sending.
4. Compare the sent body with the last draft and tell the user what differs.
5. Any project record (log, archive, summary) follows the sent text, not the draft. Fix earlier entries that were written from the draft.
6. Check that no draft for that thread is left over. If one is, tell the user it is stale and let them delete it.

## Email Shape

```text
안녕하세요, [이름/팀]님.

[결론/요청]입니다.

맥락
- [왜]
- [근거/파일/날짜]

요청
- [무엇을]
- [어떻게]
- [언제까지]

감사합니다.
[발신자 이름] 드림
```

Load a saved signature from the selected local style profile when present; otherwise use the sender name the user provided. Do not invent a name or signature.

For internal short replies, omit formal greeting/signoff when the thread already establishes context.

## Google Chat

- Treat Google Chat closer to Slack than email: shorter, action-first, fewer formal openings.
- If the message is long, split into a short ask plus a linked doc/email draft when appropriate.
