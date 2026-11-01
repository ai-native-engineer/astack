# Claude Code: /goal runtime notes

Applies only when running goal-plan in Claude Code. Official: https://code.claude.com/docs/en/goal and https://code.claude.com/docs/en/hooks

- Condition: `/goal <text>` registers the text verbatim as the condition (up to 4,000 characters) and does not expand an `@file`, so `/goal @GOAL.md` leaves the evaluator judging against the literal string. Start with the line from `goal_log.py condition`, which names the goal, the Proof command, and the instruction to follow `GOAL.md`.
- Headless / CI: `claude -p "<the /goal line>"` runs the loop to completion in one invocation; add `--output-format stream-json --verbose` to watch turns. Ctrl+C interrupts it.
- Evaluator: after each turn a small fast model (Haiku by default) judges from the conversation only -- it cannot read files or run commands, so the Proof output must be surfaced in your replies (same rule as the main skill). Several turns without tool use stop the loop.
- Stop gate: `init_goal_plan.py --proof-command '<command>'` writes a project `Stop` command hook. `scripts/stop_gate.py` exits `2` with failing output to continue once, then honors `stop_hook_active` so `/goal`, not the hook alone, owns further retries and Bounds.
- Instructions: Claude loads `CLAUDE.md` (`@AGENTS.md` or the symlink) every turn; `GOAL.md` is read because the condition says so and the Loop Protocol starts with it.
- Worktree entry: after setup, you may `EnterWorktree` into the printed worktree path on the user's go instead of pasting `!cd <path>`.
- Compaction: on a long run the context window fills and Claude Code auto-compacts old turns on its own; do not run `/compact` yourself because it is an interactive command, not a turn action. The condition survives compaction; re-read `GOAL.md` after a compaction notice.
