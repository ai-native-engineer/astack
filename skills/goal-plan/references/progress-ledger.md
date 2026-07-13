# Progress Ledger

Read this in loop phase or when changing `progress.tsv` / `goal_log.py`.

## Commands

Run from the goal workspace. Full flags are in `goal_log.py <cmd> --help`.

- `add --task ... [--done-when ...] [--next ...]` appends a todo row and prints its id.
- `start <id>` marks a row doing.
- `block <id>` marks a row blocked.
- `drop <id> --notes "<reason>"` drops a row; dropped rows need a reason.
- `done <id> --decision keep|discard|crash --artifact "<proof>"` closes a row and stamps the current `HEAD` checkpoint.
- `set <id> --col <column> --value <v>` edits an open row field; use `done` or `drop` for terminal rows.
- `show [--status doing]` reads the table.

## Step Loop

The loop is: take a row -> work -> record the outcome with `goal_log.py` -> commit.

`goal_log.py done` stamps the current `HEAD` as the row's resume checkpoint. The commit immediately after records the row update. Commit discarded attempts too rather than `git reset` them away, or the record is lost.

Keep row granularity aligned with real work:

- If one script or report pass produces several outputs together, make one row with acceptance criteria.
- Do not split tightly coupled outputs into rows that become ledger-only closures.
- If one artifact legitimately satisfies several existing rows, say that in each artifact field.
- Collapse future rows after a multi-row artifact instead of repeating ledger-only closures.

## Schema

```tsv
id	status	decision	task	done_when	checkpoint	artifact	next	notes
```

- `status`: todo, doing, done, blocked, dropped.
- `decision`: n/a for open rows; keep advanced the goal; discard did not help but caused no harm; crash caused a regression.
- `checkpoint`: current `HEAD` commit hash when `goal_log.py done` ran.
- `artifact`: proof for done rows.
- `next`: next action if the row is not complete.
