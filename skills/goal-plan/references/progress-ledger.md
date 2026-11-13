# Progress Ledger

Read this in loop phase or when changing `progress.tsv` / `goal_log.py`.

Only the orchestrator writes the ledger, one update at a time, through `goal_log.py` (`goal_log.py --help` lists the commands). `assign` and `start` make no commit; the ledger rides in the row's commit.

- `defer` holds a row for a user action or an external condition, and other rows continue; `resume` returns it to todo. `block` is for a technical dependency or missing access, not an approval wait.

## Step Loop

Select runnable rows -> start workers -> review and integrate worker PRs -> record the outcome -> one commit per row.

`goal_log.py done` stamps the current `HEAD` as the row's resume checkpoint. The commit immediately after records the row update: `<type>(<scope>): <what changed> (#<issue>)`, where the issue is the row's own or the tracking issue. A deferred row keeps its issue, worker branch, and worktree open. Commit discarded attempts too rather than `git reset` them away.

Keep row granularity aligned with real work:

- If one script or report pass produces several outputs together, make one row with acceptance criteria.
- Do not split tightly coupled outputs into rows that become ledger-only closures.
- If one artifact legitimately satisfies several existing rows, say that in each artifact field.
- Collapse future rows after a multi-row artifact instead of repeating ledger-only closures.

Row order: the baseline row first, harness rows (layers marked `build in row N` in `GOAL.md`) next, feature rows after the layers they depend on, and the finish row (result PR) last.

## Columns

- `decision`: n/a for open rows; keep advanced the goal; discard did not help but caused no harm; crash caused a regression.
- `checkpoint`: current `HEAD` commit hash when `goal_log.py done` ran.
- `artifact`: proof for done rows; the finish row's artifact is the PR URL.
- `next`: next action if the row is not complete.
