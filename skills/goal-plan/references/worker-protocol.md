# Worker Protocol

Read this in loop phase before starting a worker or integrating a worker PR.

## Roles

- The main agent is the goal orchestrator and single writer of `progress.tsv`. Workers never edit it.
- A worker owns one assigned row and works only in its recorded worktree.
- A worker does not ask the user questions. It returns `deferred` when a user-only action is needed.

## Start

`python3 <skill>/scripts/goal_worker.py start <row> --worker <name> --type <type> --desc <kebab-description>` creates the worker branch `<type>/<issue>-<description>` and a sibling worktree from the goal branch, and records the assignment and `doing`. It makes no commit. The worker commits there, pushes, and opens a PR against the goal branch titled `<type>(<scope>): <what changed> (#<issue>)`; the title becomes the integration commit subject.

Run workers in parallel only when their dependencies, target files, external resources, and integration order do not overlap. Run dependent or overlapping rows serially.

## Worker result

The worker returns this exact shape to the orchestrator:

```text
row: <id>
status: done | deferred | blocked | crashed
decision: keep | discard | crash | n/a
commit: <sha or ->
proof: <actual command output or artifact path>
changed_files: <repo-relative paths>
deferred_reason: <required for deferred>
resume_when: <condition that resumes the row, if known>
next: <follow-up action>
```

A `done` result includes a commit and proof. A `deferred` result includes the prepared artifact and the reason. A `blocked` result is for a technical dependency or missing access, not ordinary approval waiting.

## Integration

The orchestrator reviews the PR diff and runs the row's proof and verification layers, then runs `python3 <skill>/scripts/goal_worker.py integrate <row> --pr <n> --head <reviewed-sha> --artifact "<proof>" [--keep-issue]`. The script owns the checks, the merge, the ledger update, the issue close, and the removal of the worker branch and worktree; read its error output if it refuses. Never run raw `git merge` or `gh pr merge` for a worker PR. Use `--keep-issue` when several rows share one issue.

Do not integrate a deferred row; keep its PR, issue, branch, and worktree for the next continuation. A discarded or crashed attempt is not merged: record it with `goal_log.py done --decision discard|crash` (or `drop`), close its issue with `goal_issue.py close --reason not-planned`, and remove its worktree and branch.

## While a user-only row waits

- The orchestrator keeps working: remaining todo rows first; when none are left, it opens new rows from the goal's own gaps (a QA pass on the integrated result, polish found by its own run, known issues), integrates them, and keeps the result PR updated.
- User feedback that arrives during the wait (complaint, bug, preference) becomes a sub-issue and a row right away and goes to a worker; do not ask the user to wait.
- Only when nothing verifiable remains, reply briefly that the goal is waiting and name the exact user action. Do not repeat long instructions on each Stop-hook turn.
