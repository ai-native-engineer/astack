# Claude Code: /goal runtime notes

Applies only when running goal-plan in Claude Code. Official: https://code.claude.com/docs/en/goal and https://code.claude.com/docs/en/hooks

- Headless / CI: `claude -p "/goal @GOAL.md"` runs the loop to completion in one invocation; Ctrl+C interrupts it.
- Evaluator: after each turn a small fast model (Haiku by default) judges from the conversation only -- it cannot read files or run commands, so the Proof output must be surfaced in your replies (same rule as the main skill).
- Stop gate: `init_goal_plan.py --proof-command '<command>'` writes a project `Stop` command hook. `scripts/stop_gate.py` exits `2` with failing output to continue once, then honors `stop_hook_active` so `/goal`, not the hook alone, owns further retries and Bounds.
- Worktree entry: after setup, you may `EnterWorktree` into the printed worktree path on the user's go instead of pasting `!cd <path>`. The generated `CLAUDE.md` imports `AGENTS.md`; `/goal @GOAL.md` loads the separate goal contract.
- Compaction: on a long run the context window fills and Claude Code auto-compacts old turns on its own; do not run `/compact` yourself because it is an interactive command, not a turn action.
