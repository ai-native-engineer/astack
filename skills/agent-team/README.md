# Agent Team

Shared source for strong-coordinator and persistent-worker orchestration across Claude Code, Codex, and optional Zellij panes.

## Sources

- YouTube: [Tmux + Fable = Cut 35% less token](https://www.youtube.com/watch?v=wCSPgHpcxdc) — coordinator/worker separation, persistent follow-up sessions, observable cross-harness panes.
- [AI Builder Club open-agent-teams](https://github.com/AI-Builder-Club/skills/tree/main/skills/open-agent-teams): result files and race-safe completion sentinels.
- [Zellij CLI](https://zellij.dev/documentation/zellij-commands): pane creation and pane-ID actions.

Runtime behavior lives in `SKILL.md` and `references/`. `scripts/zdel` is the Zellij adapter and includes an in-session self-test; the notify sentinel scripts are covered by `tests/test-notify.sh`.
