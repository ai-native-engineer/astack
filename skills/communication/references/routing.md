# Communication Routing

Use this when the user asks for communication but the channel, recipient, or action is not fully explicit.

## Intent

- Read/search: gather context only; do not draft unless asked.
- Draft/rewrite: produce copy, do not send.
- Reply/send/edit: draft, show target and body, confirm, then use the channel skill.
- Summarize/archive: preserve source links, timestamps, and unknowns.

## Channel Selection

Use the explicit channel first:

- Slack words: Slack, 슬랙, channel, thread, DM, mention -> `agent-slack`
- Discord words: Discord, 디스코드, server, guild, channel, thread -> `agent-discord`
- KakaoTalk words: 카톡, 카카오톡, 오픈채팅, 채팅방 -> `kakaotalk`
- Gmail/email words: 메일, 이메일, Gmail, 답장, 초안 -> `gog`
- iMessage/SMS words: 아이메시지, 문자, SMS, RCS -> `imessage`

If only a recipient is named:

1. Check the current project/thread context for a recently used channel.
2. If there is clear evidence, state `추정: [channel]로 진행합니다` before drafting.
3. If the action would send externally and the channel is not clear, ask for confirmation.

## Direct Invocation Invariant

The user may bypass this router by naming a transport skill directly. That is valid. The transport skill must still load the shared communication references before writing outbound copy.

## Safety

- Never send externally without an explicit final-body approval unless the user already provided both target and exact body.
- Never infer a recipient identity from a common name when there are likely duplicates. Confirm the handle, email, room, channel, or phone number.
- If the content may include confidential data, call out the risk and ask whether to redact or use sample data.
