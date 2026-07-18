# KakaoTalk Channel Overlay

Apply this after the common communication contract when the selected channel is KakaoTalk.

## Shape

- Keep messages shorter than Slack/email by default.
- Use one compact paragraph for simple replies.
- Use bullets only when the recipient needs multiple actions or a handoff.
- Avoid heavy sectioning unless the message is an operational handoff.

## Context

- Read recent room messages before drafting when replying into an existing conversation.
- Match the room's current topic and level of formality.
- If the room is an open chat or group room, avoid exposing private context unless the user explicitly approved it.

## Sending

- Show the room name and final body before sending.
- Do not add an assistant signature to the body.
- Use the channel skill's own send options for signatures or no-signature behavior.
- If the target room is ambiguous, search/list rooms and confirm the exact room before sending.

## Useful Shapes

Simple reply:

```text
[핵심 답변]. [필요한 액션/다음 단계]로 보면 됩니다.
```

Compact request:

```text
[무엇] 먼저 확인해주세요.
이유는 [왜]입니다.
[방식/기한] 기준으로 보면 됩니다.
```
