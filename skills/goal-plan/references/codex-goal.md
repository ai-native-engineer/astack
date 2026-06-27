# Codex: /goal runtime notes

Applies only when running goal-plan in Codex. Official: https://developers.openai.com/codex

- Enable: if goal commands are hidden, turn on `features.goals` in `config.toml` or run `codex features enable goals`.
- Pause: unlike Claude's `clear`-only model, Codex supports `/goal pause` and `/goal resume` to stop and continue mid-run.
- Shape the goal first: if the completion condition is fuzzy, draft it in `/plan`, then hand it to `/goal`.
- Headless / CI: use Codex Exec for one-off automated runs that complete on their own.
