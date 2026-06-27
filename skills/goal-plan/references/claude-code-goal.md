# Claude Code: /goal runtime notes

Applies only when running goal-plan in Claude Code. Official: https://code.claude.com/docs/en/goal

- Auto-stop: Claude Code force-ends the loop after the evaluator returns "not met" 8 times in a row, so the session can end before the condition holds. Resume with `--resume` in a new session to continue; the turn count, timer, and token budget reset on resume.
- Headless / CI: `claude -p "/goal @GOAL.md"` runs the loop to completion in one invocation; Ctrl+C interrupts it.
- Evaluator: after each turn a small fast model (Haiku by default) judges from the conversation only -- it cannot read files or run commands, so the Proof output must be surfaced in your replies (same rule as the main skill).
