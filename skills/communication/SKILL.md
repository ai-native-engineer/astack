---
argument-hint: "[channel|recipient|message]"
name: communication
description: "Cross-channel work-message orchestrator and shared writing contract. Use when drafting, rewriting, sending, editing, or reviewing outbound messages for Slack, Discord, KakaoTalk, Gmail/Google Chat, iMessage/SMS, PR/issue comments, stakeholder handoffs, requests, status updates, or personal/team style matching. Do NOT use for long-form docs, curriculum content, blog posts, or channel mechanics without message composition; use the channel transport skill for execution details."
---

# Communication

Shared communication rules for work messages across channels. This is the orchestrator and the source of truth that direct channel skills load before drafting or sending.

## Workflow

1. Identify the job: read/search, draft, rewrite, reply, send, edit, summarize, or archive.
2. Identify the channel. If the user named a channel, use it. If only a recipient is named, infer from recent context only when there is evidence; otherwise ask or mark `확인 필요:`.
3. Load only the needed references:
   - `references/routing.md` when the channel, recipient, or action is not fully explicit
   - `references/work-message-contract.md` for common message quality rules
   - `references/style-profiles.md` when matching a person/team voice
   - `references/message-templates.md` when the message is a request, handoff, status update, proposal, correction, or attachment context
   - one file under `references/channel-overlays/` for channel-specific constraints
4. Delegate transport to the channel skill when it is installed. If it is absent, finish the draft and name the missing transport instead of pretending the send/read action ran:
   - Slack -> `agent-slack`
   - Discord -> `agent-discord`
   - KakaoTalk -> `kakaotalk`
   - Gmail or Google Chat -> `gog`
   - iMessage/SMS/RCS -> `imessage`
5. Before any external send/edit, show the recipient/channel and final body for confirmation unless the user has already explicitly approved the exact body.

## Direct Channel Entry

Users may invoke a transport skill directly, for example `kakaotalk` or `agent-slack`. Those skills must still load this skill's common references before composing outbound copy. This prevents channel-specific tools from drifting away from shared tone, structure, and safety rules.

Each direct channel skill should keep only:

- transport mechanics, auth, targeting, and platform constraints
- a pointer to this skill's common references
- a short fallback contract for cases where this skill is unavailable

Do not copy the full common communication rules into channel skills.

After adding or editing a channel skill, run `python3 scripts/check-channel-hooks.py` from this skill directory to verify every installed channel skill still points to the shared contract. A packaged plugin may omit optional transports; the shared source checkout still requires all five.

## Style Profiles

Reusable person/team voice belongs in the local profile directory, not in shared skill files or transport skills.

Read `references/style-profiles.md`. Use `templates/style.md` with `scripts/create-style-profile.py` to create `$HOME/.config/communication/styles/<slug>.md`.

Example:

```bash
python3 scripts/create-style-profile.py --name "Person or Team" --slug "person-or-team"
```
