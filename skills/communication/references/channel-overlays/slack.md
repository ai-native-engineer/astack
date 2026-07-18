# Slack Channel Overlay

Apply this after the common communication contract when the selected channel is Slack.

## Structure

- Main channel message should usually be a one-line headline.
- Put details, context, links, and evidence in the thread.
- Label the message by function, such as `[질문]`, `[공유]`, or `[요청]`.
- Headline format: `[성격] 핵심 내용` or `[성격] <@USER_ID> 핵심 내용`.
- Exception: short one-line answers or reactions can stay directly in the channel.
- If a long message is already approved by the user, do not split or rewrite it unless asked.

## Mentions

- Mention only people who need to act, decide, or know.
- Use Slack user IDs for mentions when known: `<@U...>`.
- Use `@channel` only when the whole channel needs timely attention; otherwise use direct mentions.
- Avoid repeating a mentioned person's name with honorifics if the user asked for mention-only.
- If the recipient must act, the first visible line should make that action clear.

## Channel vs DM

- Put searchable team information, decisions, and reusable context in a public channel.
- Use DM for private or sensitive context, including personal feedback about improvement or mistakes.
- Do not move general work context into DM when the team will need to find or reuse it.

## Status Reactions

- Use 👀 for acknowledged or in progress and ✅ for complete when a reaction is enough.
- Do not add a separate text reply only to report those states.
- Treat reactions as external writes: add one only when the user asked for or approved it.

## Formatting

- Avoid Markdown tables unless the user explicitly asks; they are hard to read and often render poorly.
- Avoid fragile Markdown when sending through CLI: nested lists, heavy bolding, table-like pipes, and long continuation blocks can render differently in Slack than in the command text.
- Prefer plain section labels (`전제`, `핵심 판단`, `체크할 포인트`, `요청`, `막히면`) plus short bullets.
- Use backticks for file paths, parameters, functions, commands, and literal labels.

## Send / Edit

- Preserve user-approved wording while sending or editing.
- If editing an existing Slack message, scope the change first: length, structure, facts, tone, typo, attachment, mention, or thread placement.
- After sending/editing, verify with `agent-slack message get` or `agent-slack message list` when feasible.
- If formatting breaks, edit in place with simpler plain text instead of adding a corrective reply.

## Channel Main + Thread Template

Main message:

```text
[요청] <@USER_ID> [핵심 요청] ([기한/긴급도])
```

Thread:

```text
<@USER_ID> [상황/목적] 전에 이것만 먼저 봐주세요.

첨부한 [파일명]은 [기준/용도]입니다. 이번에는 [이전과 다른 점] 때문에 [가장 중요한 운영 변수]가 핵심입니다.

전제
- [팩트 1]
- [팩트 2]
- 그래서 [운영 기준]

핵심 판단
- [결론]
- 근거: [숫자/사례/관찰]

체크할 포인트
1. [항목]
- 변수: [현장에서 생길 수 있는 일]
- 대응: [어떻게 처리할지]

막히면
- [막히는 조건]이면 [대안]으로 빼면 됩니다.

정리하면 [핵심 흐름]이 끊기지 않게 보면 됩니다.
```
