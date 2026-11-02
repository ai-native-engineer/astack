# Codex: /goal runtime notes

Applies only when running goal-plan in Codex. Official: https://developers.openai.com/codex/hooks and https://developers.openai.com/codex/use-cases/follow-goals/

- Enable: if goal commands are hidden, turn on `features.goals` in `config.toml` or run `codex features enable goals`.
- Condition: start with the line from `goal_log.py condition`; it carries outcome, proof, and the instruction to follow `GOAL.md`, which is the shape Codex goals expect (outcome, proof, boundaries, iteration policy).
- Pause: unlike Claude's `clear`-only model, Codex supports `/goal pause` and `/goal resume` to stop and continue mid-run.
- Shape the goal first: if the completion condition is fuzzy, draft it in `/plan`, then hand it to `/goal`.
- Stop gate: `init_goal_plan.py --proof-command '<command>'` writes `.codex/hooks.json`. On failure `scripts/stop_gate.py` exits `2`, so Codex creates a continuation prompt from the error; `stop_hook_active` bounds the hook-only retry while `/goal` owns continued work and Bounds.
- Instructions: Codex concatenates `AGENTS.md` files from the repo root down and reads at most one per directory (`AGENTS.override.md` replaces `AGENTS.md`); `GOAL.md` is read because the condition says so.
- Trust: review and trust project hooks when Codex prompts. Do not bypass hook trust for ordinary goal runs.
- Headless / CI: use Codex Exec for one-off automated runs that complete on their own.
