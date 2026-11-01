# Progress Ledger

Read this in loop phase or when changing `progress.tsv` / `goal_log.py`.

## Commands

Run from the goal workspace. Full flags are in `goal_log.py <cmd> --help`.

- `add --task ... [--issue N] [--done-when ...] [--next ...]` appends a todo row and prints its id; `--issue` prefixes the task with `#N` so commits and the PR can link to it.
- `start <id>` marks a row doing.
- `block <id>` marks a row blocked.
- `drop <id> --notes "<reason>"` drops a row; dropped rows need a reason.
- `done <id> --decision keep|discard|crash --artifact "<proof>"` closes a row and stamps the current `HEAD` checkpoint.
- `set <id> --col <column> --value <v>` edits an open row field; use `done` or `drop` for terminal rows.
- `show [--status doing]` reads the table.
- `condition [--goal-file GOAL.md]` prints the `/goal` line built from the Goal, Proof, and Bounds sections. It refuses while the contract is incomplete: any `TBD` left in `GOAL.md`, no recorded Decisions, an `AC-n` item without `Proof:`, or a line over the runtime limit. It checks emptiness only; "none", "n/a", and "Covered by Proof." are complete answers.

Sub-issues live in `goal_issue.py` (see `github-flow.md`): `open --parent <tracking> --title "<row task>"` prints the new number for `add --issue`, `close <n> --reason completed|not-planned --comment "<artifact or reason>"` records the row's outcome on its page, `list --parent <tracking>` shows the steps.

## Step Loop

The loop is: take a row -> work -> record the outcome with `goal_log.py` -> commit.

`goal_log.py done` stamps the current `HEAD` as the row's resume checkpoint. The commit immediately after records the row update, with the decision in the subject: `<type>(<scope>): <what changed> (#<issue>, row <id> keep|discard|crash)`, where the issue is the row's own or the tracking issue. Commit discarded attempts too rather than `git reset` them away, or the record is lost.

Keep row granularity aligned with real work:

- If one script or report pass produces several outputs together, make one row with acceptance criteria.
- Do not split tightly coupled outputs into rows that become ledger-only closures.
- If one artifact legitimately satisfies several existing rows, say that in each artifact field.
- Collapse future rows after a multi-row artifact instead of repeating ledger-only closures.

Row order: the baseline row first, harness rows (verification layers marked `build in row N` in `GOAL.md`) next, feature rows after the layers they depend on, and the finish row (result PR) last.

A harness row's `done_when` fires the layer on a sample rather than checking that a config file exists: `goal_hooks.py fire PostToolUse --file <sample> --trust-workspace` exits 0 for an agent hook, `goal_hooks.py fire PreToolUse --file .env --expect-block --trust-workspace` exits 0 for a blocking hook (without the flag `fire` only lists the commands it would run), a sample commit with a planted failing test is refused for a git hook, the latest goal-branch run is green for CI. `goal_hooks.py add|list|remove` manages the agent hooks in both runtime files; see `harness-layers.md`.

## Schema

```tsv
id	status	decision	task	done_when	checkpoint	artifact	next	notes
```

- `status`: todo, doing, done, blocked, dropped.
- `decision`: n/a for open rows; keep advanced the goal; discard did not help but caused no harm; crash caused a regression.
- `checkpoint`: current `HEAD` commit hash when `goal_log.py done` ran.
- `artifact`: proof for done rows; the finish row's artifact is the PR URL.
- `next`: next action if the row is not complete.
