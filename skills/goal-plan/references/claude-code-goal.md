# Claude Code: /goal runtime notes

Applies only when running goal-plan in Claude Code. Official: https://code.claude.com/docs/en/goal and https://code.claude.com/docs/en/hooks

- Condition: `/goal @GOAL.md` starts the loop from the saved goal contract in a fresh context. The `@GOAL.md` mention supplies the file contents to the evaluator; keep the Proof and Loop Protocol in `GOAL.md` so the condition stays self-contained.
- Evaluator: after each turn a small fast model judges from the conversation only; it cannot read files or run commands, so surface the Proof output in your replies. Several turns without tool use stop the loop.
- Instructions: Claude loads the project `AGENTS.md` every turn (v2.1.277+, only when no project `CLAUDE.md` exists); `GOAL.md` is read because the condition says so.
- Worktree entry: after setup, you may `EnterWorktree` into the printed worktree path on the user's go instead of pasting `!cd <path>`.
- Compaction: Claude Code auto-compacts on long runs; do not run `/compact` yourself. The condition survives compaction; re-read `GOAL.md` after a compaction notice.
