# Codex: /goal runtime notes

Applies only when running goal-plan in Codex. Official: https://developers.openai.com/codex/hooks

- Enable: if goal commands are hidden, turn on `features.goals` in `config.toml` or run `codex features enable goals`.
- Pause: unlike Claude's `clear`-only model, Codex supports `/goal pause` and `/goal resume` to stop and continue mid-run.
- Shape the goal first: if the completion condition is fuzzy, draft it in `/plan`, then hand it to `/goal`.
- Stop gate: `init_goal_plan.py --proof-command '<command>'` writes `.codex/hooks.json`. On failure `scripts/stop_gate.py` exits `2`, so Codex creates a continuation prompt from the error; `stop_hook_active` bounds the hook-only retry while `/goal` owns continued work and Bounds.
- Trust: review and trust project hooks when Codex prompts. Do not bypass hook trust for ordinary goal runs.
- Headless / CI: use Codex Exec for one-off automated runs that complete on their own.
