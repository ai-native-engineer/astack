---
name: goal-plan
description: "Use for: Set up/maintain resumable /goal work: interview the user, write GOAL.md (goal, proof, environment, verification layers, GitHub flow), track progress.tsv, loop with a commit per row, finish with a result PR. Not for short one-shot tasks."
---

# Goal Plan

Set up a durable workspace for a long-running `/goal` loop, then track progress through it. Two phases:

- **Setup phase**: inspect the target, interview the user, scaffold `GOAL.md` and `progress.tsv` (plus `AGENTS.md` when absent), fill every TBD, add the initial rows, commit the plan, then stop and hand the user the `!cd <workspace>` and `/goal` lines.
- **Loop phase**: starts only after the user runs the `/goal` line or an active goal continuation is present. Then follow `progress.tsv`, work, verify, commit each row, and finish with the result PR.

The durable record is two files plus git:

- `GOAL.md`: the objective, Proof, acceptance criteria, environment, verification layers, GitHub flow, boundaries, and loop protocol. The whole harness for one goal lives in this file.
- `progress.tsv`: the plan and progress table. Edit it only through `goal_log.py`, never by hand; only the orchestrator writes it.
- git: each loop row ends in a commit on the goal branch, so the commit history is the record of what was tried and kept. The result PR is built from that branch.

`AGENTS.md` is the repository's own instruction file: preserve existing content, never duplicate the goal there. The scaffold never creates a project `CLAUDE.md` (Claude Code reads `AGENTS.md` directly, and a `CLAUDE.md` would shadow it); an existing one is left alone with a warning. `templates/*.tmpl` are script inputs; open them only when changing the scaffold.

## References

- `references/setup.md` when creating a plan: interview, defaults, special cases, scaffold commands.
- `references/progress-ledger.md` in loop phase or when changing the ledger contract.
- `references/github-flow.md` when filling GitHub Flow, opening or closing a sub-issue (`scripts/goal_issue.py`), and before the finish row.
- `references/worker-protocol.md` before assigning workers or integrating a worker PR (`scripts/goal_worker.py`).
- `references/harness-layers.md` when filling Verification Layers or installing a hook (`scripts/goal_hooks.py`).
- `references/claude-code-goal.md` or `references/codex-goal.md` before installing Stop hooks or starting the loop.

## Setup: inspect, interview, scaffold, then stop

Setup is terminal for this invocation. After the plan commit, print `!cd <workspace>` and `/goal @GOAL.md`, then end the response. Do not enter the goal worktree, run `/goal`, run the Proof, edit target files, assign workers, or start orchestration in the setup turn. The next user-run `/goal` command is the only transition into loop phase.

A one-line goal cannot run unattended. Inspect the repo, interview with the question set in `references/setup.md`, and apply its defaults silently. Every answer lands in a `GOAL.md` section, and the interview ends when no TBD remains. Scaffold only after the user approves the final overview in words, or says to use defaults or skip questions.

## Loop: each row is a commit; the goal is a PR

The main agent schedules rows, a worker executes each independent row, the main agent reviews and integrates the result, `goal_log.py` records the outcome, and the goal branch receives one commit per row that holds the work plus the `progress.tsv` change (no empty commits). `goal_worker.py start` and `integrate` handle worker branches, merging, issue closing, and cleanup. Commit discarded attempts too rather than `git reset` them away, or the record is lost.

One row per real work pass, not per ledger ceremony. A worker that needs user action records `deferred`; other independent rows continue. A deferred user-only row never idles the loop: while it waits, keep working (todo rows, then new rows from the goal's own gaps, see `references/worker-protocol.md`). Commit subjects are `<type>(<scope>): <what changed> (#<issue>)`.

When the Goal holds, `goal_pr.py` builds the result branch without the scaffold files, pushes it, and opens one final PR with the Proof output in the body. Details in `references/github-flow.md` and `references/worker-protocol.md`.

## Writing a good Goal + Proof

- Outcome-first: the Goal states what must be true, not every step to take.
- The Proof is deterministic, repeatable evidence: command output, tests, build status, file count, queue state, or a log path -- not a "looks good" judgment, because on an unattended run the agent is the only verifier.
- The Proof is self-contained: include service startup, readiness checks, cleanup, and required env where needed, so a future run can reproduce it without hidden terminal state. The Environment section holds those commands once; the Proof calls them.
- The Proof closes the loop only when the agent can run it, read the result, and iterate on the root cause. Artifact existence alone is not proof; visual or semantic work needs an explicit comparison or review criterion.
- The Proof must verify every Acceptance Criteria item, including any semantic review item.
- The `/goal` evaluator reads the conversation, not the filesystem -- surface the Proof output in your replies. Completion is evidence, not confidence; budget or turn exhaustion is not completion.

The first `progress.tsv` row is the baseline before changes; harness rows for missing verification layers come next. Column meanings are in `references/progress-ledger.md`.

## When to use /goal

Use plain `/goal` for one-off long-running work with a single condition, `/loop` for work that repeats, and a scheduled routine for work that must outlive the session. Avoid `/goal` for one-line edits, vague finish lines, or a condition gameable without real progress.
