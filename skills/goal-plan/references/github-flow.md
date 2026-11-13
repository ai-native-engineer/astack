# GitHub Flow

Read this in setup when filling `GOAL.md` "GitHub Flow", and in loop phase before the finish row. When the target repo's `AGENTS.md` sets its own branch, commit, or PR rules, those win; the rules here fill the gaps.

## Branch and commit rules

- Branch: `<type>/<issue>-<description>` with a lowercase kebab-case description and no `#` (GitHub does not read branch names). Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`. Branch from `origin/<base>` after `git fetch`, in a worktree, never in a shared checkout that sits on `main`.
- Commit subject: `<type>(<scope>): <what changed> (#<issue>)`, imperative, lowercase first word, no trailing period, under 100 characters. Body: motivation and contrast with the previous behavior.
- One logical change per commit, tests passing and lint clean at each commit except discarded attempts, which are committed as they are. Structure-only changes (rename, move, extract) go in their own commit before behavior changes.
- Stage by path (`git add -- <paths>`), never `git add -A` or `git add .`, so another session's uncommitted files do not ride along.
- The goal branch and goal worktree are removed after the final PR merges, once the worktree is clean and the branch is merged. Worker branches and worktrees are removed by `goal_worker.py integrate`; do not ask again for either.

## Shape

| stage | git | GitHub |
|---|---|---|
| setup | create `goal/<tag>` from the repository base and commit the plan | tracking issue |
| loop | one worker branch/worktree per independent row; `goal_worker.py` integrates worker PRs into the goal branch | worker PR targets the goal branch; its sub-issue closes on integrate |
| finish | result branch = goal branch minus scaffold files | one final PR from the result branch to the repository base |
| after | sync the base, remove the goal branch and worktree | `pr-only` waits for a human merge; an explicitly selected autonomous policy may merge |

## Tracking issue and sub-issues

- One tracking issue per goal, created in setup unless an existing issue covers it (`gh issue list --search "<keywords>" --state all`). Pass `-R <owner/repo>` to `gh`, `--repo` to `goal_issue.py`, `goal_worker.py`, and `goal_pr.py` on a fork so everything lands upstream. The number goes in `GOAL.md` (`init_goal_plan.py --issue N`).
- Blockers and milestones go on the tracking issue as short comments (what input unblocks a row; checkpoint hash and what the Proof showed). The ledger of every row stays in `progress.tsv`; do not mirror it.
- Each row that does real work gets a sub-issue: `goal_issue.py open` prints its number for `goal_log.py add --issue`. Rows that are ledger ceremony (baseline, finish) get none. `goal_worker.py integrate` closes the sub-issue of a worker row.
- Close the tracking issue through `Closes #N` in the result PR body, not by hand.

## Linking issue, commit, PR

- Every commit subject carries a number: the row's sub-issue, else the tracking issue. GitHub lists the commit on that issue, so its timeline becomes the history of the work. `goal_pr.py` warns about subjects with no `#N`; fix a local one before pushing, otherwise leave the warning in the reply.
- The result branch name starts with the tracking issue number (`feat/N-<description>`). The PR body lists `Closes #N` for the tracking issue and every sub-issue still open, and lists already-closed sub-issues under "Steps" with their numbers.
- Before the finish row, `git log --oneline <base>..HEAD` shows only this goal's commits and `gh issue view <n> --json state` is `OPEN` for every issue the PR will close.

## Loop commits

- One commit per row on the goal branch: `<type>(<scope>): <what changed> (#<issue>)`. The keep/discard/crash decision lives in `progress.tsv`.
- Commit discarded attempts too. The PR reviewer sees the net diff, so the history costs nothing in review and keeps the dead ends findable.
- Target repos outside the goal repo (dedicated mode) follow `GOAL.md` Target Change Tracking.

## Result PR

Run from the goal workspace once the Proof passes, after `git fetch`:

```bash
python3 <skill>/scripts/goal_pr.py --branch <type>/<issue>-<description> --title "<type>(<scope>): <subject> (#<issue>)" --body-file <pr-body.md>
```

- The script builds the result branch from the goal branch without the scaffold files, pushes, and opens the PR (`goal_pr.py --help` has the flags).
- The PR body carries what and why, the Proof command with its actual output, the Acceptance Criteria with how each was verified, `Closes #N` lines, rows dropped with their reasons, follow-up issues found on the way, and review points. Draft it in a file; the script does not write prose.
- Separate PRs only when Scope names separate deliverables.
- The last reply of the goal ends with the PR URL and `gh pr view <n> --json state` output. The recorded merge policy decides whether the loop waits for a human merge or performs the allowed merge.
- After a final PR merge, the continuation checks `gh pr view <n> --json state --jq '.state'` prints `MERGED`, synchronizes the base, and removes the goal branch and worktree.

## Proof patterns

- PR open: `gh pr view <n> --json state,isDraft --jq '.state'` prints `OPEN`.
- CI on the PR: `gh pr checks <n> --watch --fail-fast` exits 0.
