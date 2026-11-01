# GitHub Flow

Read this in setup when filling `GOAL.md` "GitHub Flow", and in loop phase before the finish row. When the target repo's `AGENTS.md` sets its own branch, commit, or PR rules, those win; the rules here fill the gaps.

## Branch, commit, cleanup rules

- Branch: `<type>/<issue>-<description>` with a lowercase kebab-case description and no `#` (GitHub does not read branch names; `#` becomes `%23` in URLs). Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`. Branch from `origin/<base>` after `git fetch`, in a worktree, never in a shared checkout that sits on `main`.
- Commit subject: `<type>(<scope>): <subject>`, imperative, lowercase first word, no trailing period, under 100 characters. A subject that opens with an uppercase word (`PR`, `README`) fails common commit linters; open with a lowercase word or Korean.
- Commit body: motivation and contrast with the previous behavior, wrapped before 100 characters per line. Reference issues in the footer or subject as `#N`.
- One logical change per commit, tests passing and lint clean at each commit. Structure-only changes (rename, move, extract) go in their own commit before behavior changes.
- Stage by path (`git add -- <paths>`), never `git add -A` or `git add .`, so another session's uncommitted files in the same checkout do not ride along.
- Before every push: `git fetch`, then `git log --oneline <remote>/<base>..HEAD` shows only this goal's commits.
- Cleanup: the goal never deletes branches or worktrees. After the user merges, they decide what to remove; the goal reports the branch names and the merge state instead.

## Shape

| stage | git | GitHub |
|---|---|---|
| setup | goal branch or dedicated goal repo, plan commit | tracking issue (optional) |
| loop | one commit per row, discards included | comment on the tracking issue when blocked or at a milestone |
| finish | result branch = goal branch minus scaffold files | one PR with the Proof output in the body |
| after | nothing | the user merges; the goal does not merge or delete branches |

## Tracking issue

- Create one when the goal spans more than one session or other people follow it. Check for an existing issue first (`gh issue list --search "<keywords>" --state all`) and reuse it. On a fork, pass `-R <owner/repo>` to every `gh` command so issues and the PR land upstream.
- Put the issue number in `GOAL.md` "GitHub Flow". `init_goal_plan.py --issue N` fills it at scaffold time.
- The issue is the human-readable record: a short comment when a row blocks (what input unblocks it) and when a milestone lands (checkpoint hash, what the Proof showed). The ledger of every row stays in `progress.tsv`; do not mirror it.
- Close the issue only after the result PR merges, which is the user's action, or write `Closes #N` in the PR body so the merge closes it.

## Sub-issues: one step, one page

- One tracking issue per goal. Each progress row that does real work gets a sub-issue under it, so the tracking issue page lists the steps with their state and progress, and each step's page collects its commits and outcome. Rows that are ledger ceremony (baseline record, finish row) get no sub-issue.
- Open the sub-issue when the row is added: `python3 <skill>/scripts/goal_issue.py open --parent <tracking> --title "<row task>"` prints the number; then `goal_log.py add --task "<row task>" --issue <number>` writes it as `#N` at the start of the task. When a backlog issue already covers the row, attach it instead: `goal_issue.py open --parent <tracking> --existing <N>`.
- Close the sub-issue when the row closes: `goal_issue.py close <N> --reason completed --comment "<artifact>"` for keep, `--reason not-planned --comment "<why, what to try instead>"` for discard, crash, or drop. The closing comment is the row's artifact or notes, so the issue page tells the same story as the ledger.
- `goal_issue.py list --parent <tracking>` shows the steps and states; paste it in the reply at milestones instead of describing progress in prose.
- The sub-issue API takes the child's database id, not its number, and the child must share the repository owner with the parent; `goal_issue.py` handles both.

## Linking issue, commit, PR

- Every commit subject carries a number: the row's sub-issue when it has one, else the tracking issue. GitHub lists the commit on that issue, so the issue timeline becomes the history of the work without extra comments. `goal_pr.py` warns about commits whose subject has no `#N`; fix the subject before pushing when the commit is still local to the goal branch, otherwise leave the warning in the reply.
- The result branch name starts with the tracking issue number (`feat/N-<description>`, as the branch rule above), and the PR body lists `Closes #N` for the tracking issue and every sub-issue still open, so the merge closes them and the PR links back to each. Sub-issues already closed by the loop are listed under "Steps" with their numbers, so a reader moves PR -> step -> commits.
- Check the chain before the finish row: `git log --oneline <base>..HEAD` shows a number on every subject, `goal_issue.py list --parent <tracking>` shows every step closed or listed in the PR body, and `gh issue view <n> --json state` is `OPEN` for every issue the PR will close.

## Loop commits

- Commit after every row on the goal branch: `<type>(<scope>): <what changed> (#<issue>, row <id> keep|discard|crash)`. The decision in the subject makes `git log --oneline` readable as the experiment log.
- Commit discarded attempts too. The PR reviewer sees the net diff, not every attempt, so the history costs nothing in review and keeps the dead ends findable.
- Target repos outside the goal repo (dedicated mode) follow `GOAL.md` Target Change Tracking.

## Result PR

Run from the goal workspace once the Proof passes:

```bash
python3 <skill>/scripts/goal_pr.py --branch <type>/<issue>-<description> --title "<type>(<scope>): <subject> (#<issue>)" --body-file <pr-body.md>
```

- The script branches from the goal branch, removes the scaffold files (`GOAL.md`, `progress.tsv`, `.claude/settings.json`, `.codex/hooks.json`) in one commit, pushes, and opens the PR against the base branch. Pass `--include <path>` to keep a scaffold file that the goal changed on purpose, `--base <branch>` to change the base, `--dry-run` to build the branch without pushing, `--no-pr` to push without opening a PR.
- Before running it: `git fetch` and `git log --oneline <remote>/<base>..HEAD` shows only this goal's commits, and the Proof passed on `HEAD`.
- The PR body carries what and why, the Proof command with its actual output, the Acceptance Criteria with how each was verified, `Closes #N` lines, the rows dropped with their reasons, follow-up issues found on the way, and review points. Draft it in a file; the script does not write prose.
- Separate PRs only when Scope names separate deliverables. A loose set of unrelated changes in one PR is as hard to review as a loose goal is to run.
- The last reply of the goal ends with the PR URL and `gh pr view <n> --json state` output. Merge is the user's choice; the loop stops there.

## Proof patterns

- PR open: `gh pr view <n> --json state,isDraft --jq '.state'` prints `OPEN`.
- CI on the PR: `gh pr checks <n> --watch --fail-fast` exits 0.
- After the user merges, a later goal that depends on it checks `gh pr view <n> --json state --jq '.state'` prints `MERGED` and `git log --oneline <remote>/<base>..HEAD` is empty after a fetch.
- Issue state when the goal must close it: `gh issue view <n> --json state --jq '.state'`.
