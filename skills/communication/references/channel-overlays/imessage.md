# iMessage / SMS Channel Overlay

Apply this after the common communication contract when the selected channel is iMessage, SMS, or RCS.

## Shape

- Keep the message short and conversational.
- Use one or two paragraphs, not section-heavy formatting.
- Avoid long operational handoffs unless the user explicitly wants a long text.
- Do not add signatures unless the user asks.

## Recipient Safety

- Confirm the exact contact, phone number, or chat target before sending.
- If there are likely duplicates, use dry-run output and ask the user to confirm.
- Do not infer a phone number from a name without evidence.

## Send Limits

- Text only. Attachments, tapbacks, edits, and thread replies are not supported by the current channel skill.
- Always dry-run first; only run the actual send after explicit approval.

## Useful Shapes

```text
[핵심 내용]입니다.
[필요한 액션/시간]만 확인해주세요.
```
