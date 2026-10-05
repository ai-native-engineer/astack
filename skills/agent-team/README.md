# Agent Team

Shared source for strong-coordinator and persistent-worker orchestration across Claude Code, Codex, and optional herdr panes.

## Sources

- YouTube: [Tmux + Fable = Cut 35% less token](https://www.youtube.com/watch?v=wCSPgHpcxdc) — coordinator/worker separation, persistent follow-up sessions, observable cross-harness panes.
- [AI Builder Club open-agent-teams](https://github.com/AI-Builder-Club/skills/tree/main/skills/open-agent-teams): result files and race-safe completion sentinels.
- [herdr](https://herdr.dev/llms.txt): agent-aware panes with lifecycle states (`idle`, `working`, `blocked`, `done`) and `agent prompt --wait`, which replace the earlier hand-rolled sentinel adapter.
- Anthropic [Optimizing for cost and intelligence](https://platform.claude.com/docs/en/about-claude/models/optimizing-for-cost-and-intelligence): delegation pays only when there is bulk independent work; for one dependent chain or work that fits one context, the coordinator alone came out ahead in every measured case.
- Anthropic [Prompting Claude Sonnet 5.5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5): the two paragraphs appended to Sonnet worker prompts (keep working until done, no unrequested additions).
- OpenAI [GPT-6.1 Sol](https://openai.com/index/introducing-gpt-6-1-sol/): near-Astra quality at one-fifth of Astra's price, which makes it the default Codex worker.

Runtime behavior lives in `SKILL.md` and `references/`. The Zellij adapter (`scripts/zdel`) was retired in favor of herdr's built-in agent control; it remains in git history.
