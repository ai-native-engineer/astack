---
name: goal-plan
description: "Create and maintain a lightweight /goal plan for long-running agent work: AGENTS.md goal instructions plus progress.tsv plan/progress scoreboard. Use when the user asks for a goal plan, goal workspace, goal harness, /goal setup, durable progress tracking, completion conditions, or resumable long-running task state. Do NOT use for short one-shot tasks that do not need persistent state."
---

# Goal Plan

Set up a durable workspace for a long-running `/goal` loop, then track progress through it. This skill has two distinct phases:

- **Setup phase**: create or extend `AGENTS.md`, create `CLAUDE.md` and `progress.tsv`, optionally add runtime Stop-hook configs, commit the plan, then stop and hand the user ready-to-run `!cd <workspace>` and `/goal @AGENTS.md` start commands. Do not start progress rows, edit target files, or run the Proof in setup phase.
- **Loop phase**: starts only after the user invokes `/goal @AGENTS.md` or an active goal continuation is present. Then follow `progress.tsv`, work, verify, and commit each step.

The durable record is two files plus git:

- `AGENTS.md`: the repo guidance plus the instructions and loop protocol the goal runs on. Start with `/goal @AGENTS.md`.
- `progress.tsv`: the plan and progress table. Edit it only through `goal_log.py`, never by hand.
- git: each loop step ends in a commit, so the commit history is the durable, resumable record of what was tried and kept.

`CLAUDE.md` is a thin Claude Code entrypoint that contains only `@AGENTS.md`.

Stop-hook configs enforce the Proof command; `AGENTS.md` remains the single source of truth for completion.

`templates/AGENTS.md.tmpl` is script input. Do not read it during ordinary setup; `init_goal_plan.py` copies and fills it. Open it only when changing or verifying the scaffold.

Read `references/setup.md` when creating a plan. Read `references/progress-ledger.md` in loop phase or when changing the ledger contract. Read the Claude Code or Codex runtime reference before installing Stop hooks.

## Setup: explore, interview, scaffold, then stop

AGENTS.md goal instructions need more than a one-line goal. Before scaffolding, inspect the repo enough to propose concrete defaults, then run at least one interview round with the user. Ask only what changes the run, use the host's structured clarification UI when available, and fill the Context section from the repo, not the user.

When the user asks to turn a rough operations/TODO list into a Codex `/goal`, especially with phrases like "until it works" or "isolated environment", do not hand off a vague goal. Convert the list into acceptance criteria, a deterministic proof command, explicit scope/out-of-scope boundaries, reversible-change constraints, and a progress row for each major subsystem. If the user chooses real infrastructure scope, keep the goal repo isolated but constrain real host changes to narrow, reversible user-level canaries unless they explicitly approve broader actions.

If the user later corrects the goal scope, rewrite both `AGENTS.md` and `progress.tsv` to match the corrected scope, remove stale acceptance criteria/rows/phrases from the prior scope, verify with a content search, and commit the rewrite. Do not leave old risky domains (for example security/network/production ops) as active proof requirements after the user moved them out of scope.

For service-boilerplate or harness goals where the user asks for spec-driven development, use the user's named spec system instead of inventing a generic `SPEC.md`. In particular, if they say GitHub Spec Kit, encode Spec Kit as the source of truth: `specify-cli` install/verification via `uv`, `specify init`, and the `constitution -> specify -> plan -> tasks -> implement` flow. Note command naming differences: most slash-command agents use `/speckit.*`, while Codex CLI in skills mode uses `$speckit-*`. A local `SPEC.md` may only be a thin compatibility note around Spec Kit outputs, not the primary spec system.

The interview round is required for broad or long-running requests. Present a short overview of the inferred goal, proof, scope, and risks, then ask 1-3 concrete questions. Do not scaffold in the first response unless the user explicitly says to use defaults, skip questions, or continue without interview.

Settle these fields before writing the goal instructions:

- Goal -- one measurable end state
- Proof -- the command/check that proves it; propose it from the repo, then confirm. Make it self-contained: if a service must run, include start, readiness/wait, check, and cleanup. Confirm the loop can execute it and read a clear pass/fail signal.
- Acceptance Criteria -- add 2-5 checkable items when the request spans multiple systems, has vague words like "improve/features", or has several deliverables.
- Scope / Out of Scope -- what is included, what is excluded or deferred
- Constraints -- what must not change, required tools, paths git may touch
- Input Stability -- for mutable sources, define a snapshot path, cutoff timestamp, or explicit "current at proof time" caveat
- Target Change Tracking -- where target edits will be committed or snapshotted
- Bounds -- time/turn limit for unattended running (or none)

For behavior-changing code goals, use a verification-driven order: reproduce or add a failing check, make the minimum implementation change, then rerun until it passes. If no suitable check exists, make the first progress row create the smallest test, fixture diff, or screenshot comparison.

For broad requests, convert fuzzy language into acceptance criteria before writing the goal instructions. If "several features" could mean read-only status versus remote actions, ask one tight question; do not silently pick the more invasive scope.

For recommendation, audit, research, or synthesis goals:

- Add one semantic review item to Acceptance Criteria.
- Make the item say what a human-readable result must satisfy.
- Check that evidence examples are relevant.
- Check that ranking rationale is explainable.
- Check that exclusions and gaps are named.
- Treat generic keyword matches and heading-only validators as weak evidence.

Choose the goal workspace from the target's git boundary:

- If the target git/worktree may be touched, use a repo worktree.
- If the target is not a git repo, or target git must stay untouched, use a dedicated goal repo.

Use `init_goal_plan.py --help` and `references/setup.md` for exact commands. Pass `--proof-command` only for a fast, deterministic, bounded, non-interactive, non-destructive check; it fills the Proof and installs the same Stop gate for Claude Code and Codex. Replace every `TBD`, commit the plan, then stop. Hand off with a plan overview plus ready-to-run entry and start commands.

Dedicated goal repos track the goal ledger, not external target edits by magic. If target edits are in scope and the target is not a git repo, settle one tracking mode before the loop starts:

- user approves `git init` in the target, then target commits carry code diffs;
- target stays non-git, so each loop step commits patch/snapshot artifacts in the goal repo;
- target is read-only, so the goal can only produce reports or external artifacts.

Do not leave target code changes as the only uncommitted record unless the user explicitly chooses that risk.

For mutable data sources such as session logs, queues, feeds, calendars, live APIs, or changing folders, freeze the input or record the proof as current-at-proof-time. Do not call a proof deterministic if rerunning it can silently analyze a different input set.

## Progress: use goal_log.py, not hand edits

Use this section only in loop phase. Editing a TSV by hand breaks on tab matching across context resets. Drive every change through `goal_log.py` from the workspace dir. Use `goal_log.py <cmd> --help` and `references/progress-ledger.md` for command details.

The script auto-fills id and checkpoint, escapes tabs/newlines, validates the status/decision enums, and rejects status/decision/proof mismatches.

## Each step is a commit

The loop is: take a row -> work -> record the outcome with `goal_log.py` -> commit. The commit captures the work plus the `progress.tsv` change, so even a non-code step has a real diff to commit (no empty commits). `goal_log.py done` stamps the current `HEAD` as the row's resume checkpoint; the commit you make immediately after is the durable ledger entry for that step. Commit discarded attempts too rather than `git reset` them away, or the record is lost.

Keep row granularity aligned with real work: one row per real work pass, not one row per ledger ceremony.

## Writing a good Goal + Proof

- Outcome-first: the Goal states what must be true, not every step to take.
- The Proof is deterministic, repeatable evidence: command output, tests, build status, file count, queue state, or a log path -- not a "looks good" judgment, because on an unattended run the agent is the only verifier.
- The Proof is self-contained: include service startup, readiness checks, cleanup, and required env where needed, so a future run can reproduce it without hidden terminal state.
- The Proof closes the loop only when the agent can run it, read the result, and iterate on the root cause. Artifact existence alone is not proof; visual or semantic work needs an explicit comparison or review criterion.
- The Proof must verify every Acceptance Criteria item, including any semantic review item.
- The `/goal` evaluator reads the conversation, not the filesystem -- surface the Proof output in your replies, not just in files.
- Completion is evidence, not confidence: the evaluator is tuned skeptical and rejects "probably done", and budget or turn exhaustion is not completion.

The `progress.tsv` schema is documented in `references/progress-ledger.md`. The first row is the baseline/current state before changes.

## When to add more

Two files plus git is the floor, not a cap. Add Stop hooks, subagents, workflows, or extra files only when the work needs them: executable fast checks, real parallelism, adversarial verification, repeated triage, or scale. Keep slow, flaky, costly, destructive, or human-only checks in the final Proof instead of a Stop hook. For a goal with many distinct acceptance tests, add an `## Acceptance Criteria` section to `AGENTS.md` instead of overloading each `done_when`.

Use plain `/goal` for one-off long-running work with a single condition; pair with `/loop` for work that repeats (triage, periodic checks), and use a scheduled routine for work that must outlive the session. Avoid `/goal` for one-line edits, vague finish lines ("improve X"), or a condition gameable without real progress.

Runtime specifics -- pause/resume, headless runs, auto-stop, enabling goals -- differ by tool; read `references/claude-code-goal.md` or `references/codex-goal.md` for the one you run on.
