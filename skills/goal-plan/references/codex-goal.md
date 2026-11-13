# Codex: /goal runtime notes

Applies only when running goal-plan in Codex. Official: https://developers.openai.com/codex/hooks and https://developers.openai.com/codex/use-cases/follow-goals/

- Enable: if goal commands are hidden, turn on `features.goals` in `config.toml` or run `codex features enable goals`.
- Condition: start with the line from `goal_log.py condition`; Codex needs the outcome, proof, boundaries, and iteration policy in the condition itself. Claude Code uses `/goal @GOAL.md` instead.
- Instructions: Codex concatenates `AGENTS.md` files from the repo root down and reads at most one per directory (`AGENTS.override.md` replaces `AGENTS.md`); `GOAL.md` is read because the condition says so.
- Trust: review and trust project hooks when Codex prompts. Do not bypass hook trust for ordinary goal runs.
