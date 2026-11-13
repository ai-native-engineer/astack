# Goal Plan Setup

Read this when creating a goal plan.

## Setup Flow

1. Inspect the target to infer everything the repo can answer: repo type, test and lint commands, services the Proof needs and how they start, secrets it needs, and change-tracking mode. Match the signals against the baseline table in `harness-layers.md`.
2. Interview the user (below), 1-3 questions per round, using the host's structured clarification UI when available.
3. Show the final overview (goal, proof, scope, environment, verification layers, constraints, open risks) and wait for the user to approve it in words. Having seen the overview is not approval. Scaffold only after approval, or after the user explicitly says to use defaults or skip questions.
4. Scaffold, replace every `TBD`, add the initial progress rows (baseline first, then harness rows, then feature rows), commit the plan, print the handoff, and stop. Do not enter the goal worktree or start the loop in this invocation.

## Interview

Ask only what the repo cannot answer:

- Intent and premise, asked open, one question at a time, each building on the last answer: why this goal now and what happens if it is not done; what is true when it is done, and for whom; what is the simplest thing that would also satisfy the intent and why it is not enough; what would make a reviewer reject the result even if every check passed. A proposed default here anchors the user to the agent's guess, which is the thing the interview exists to avoid.
- Scope and Out of Scope.
- Proof: propose it from the repo ("Proof A: `./run test` exit 0. Proof B: A plus the e2e lane. Which?"), then confirm. It must be self-contained: service start, readiness wait, check, cleanup.
- Missing secrets or user-only access (credentials, hardware, a human login), which become `cannot start here` in Environment.
- Approval to `git init` when the target is not a git repo and target edits are in scope. Otherwise commit patch/snapshot artifacts in the goal repo, or make the goal read-only.

Rules:

- Follow up on each answer until it is observable by a command, output, count, or artifact. Convert vague words ("improve", "features", "works") the same way. If "several features" could mean read-only status versus remote actions, ask one tight question; do not silently pick the more invasive scope.
- Record each answer in `GOAL.md` Decisions with the user's words quoted. Do not record defaults.
- Stop when no TBD remains and the user approved the overview.

## Defaults

Apply silently and write them into `GOAL.md`; change one only when the user says so.

- Loop unit: one row per real work pass. Ask only when Scope names several deliverables.
- Acceptance Criteria: "Covered by Proof." For goals spanning several systems or deliverables, write 2-5 items instead, `- AC-n: WHEN <trigger> THE SYSTEM SHALL <observable result>. Proof: <command>`, each decidable by a command; the Proof must verify every item.
- Verification layers and Environment commands: inferred from the repo, using the `harness-layers.md` baseline. A layer the Proof needs but the repo lacks becomes a harness row before any feature row.
- Branches and PR bases: `goal/<tag>`, worker PRs into the goal branch, result PR into the repository default branch. Merge policy `pr-only`; `autonomous` only when the user asks.
- Tracking issue: a new one, with a sub-issue per working row. Search first (`gh issue list --search "<keywords>" --state all`) and reuse an existing issue. No remote: `none`.
- Bounds: none. Input stability: stable inputs; for a mutable source (feeds, logs, live APIs) edit Input Stability in `GOAL.md`.
- Deferred actions: the list in `GOAL.md` Deferred Actions. Reversible file, Git, issue, PR, and worker operations are never per-step questions.
- Merged worker branches and worktrees are deleted automatically by `goal_worker.py integrate`.

## Special Cases

- Rough operations/TODO list ("until it works", "isolated environment"): do not hand off a vague goal. Convert the list into acceptance criteria, a deterministic Proof, Scope and Out of Scope, reversible-change constraints, and a progress row per major subsystem. If the user chooses real infrastructure scope, keep the goal repo isolated and limit real host changes to narrow, reversible user-level canaries unless they approve more.
- The user corrects the scope later: rewrite both `GOAL.md` and `progress.tsv`, remove stale acceptance criteria, rows, and phrases of the old scope, verify with a content search, and commit. Do not leave moved-out domains (security, network, production ops) as active Proof requirements.
- Spec-driven development: use the spec system the user names instead of inventing `SPEC.md`. For GitHub Spec Kit that means `specify-cli` installed and verified through `uv`, `specify init`, and the `constitution -> specify -> plan -> tasks -> implement` flow (`/speckit.*` in slash-command agents, `$speckit-*` in Codex skills mode). A local `SPEC.md` may only be a thin note around Spec Kit outputs.
- Recommendation, audit, research, or synthesis goals: add one semantic review item to Acceptance Criteria stating what a human-readable result must satisfy. Check that evidence examples are relevant, ranking rationale is explainable, and exclusions and gaps are named. Generic keyword matches and heading-only validators are weak evidence.
- Behavior-changing code goals: reproduce or add a failing check first. If no suitable check exists, the first row creates the smallest test, fixture diff, or screenshot comparison.

## Harness Rows

A verification layer with status `build in row N` becomes a progress row before any feature row that depends on it. Give each harness row a `done_when` that fires the layer on a sample, not one that checks a config file exists (rules in `harness-layers.md`). The Proof may only rely on a layer whose row is `done`. Prefer the repo's existing tools; record a new tool in Decisions.

## Choosing e2e Means

| entry point | means | pass signal |
|---|---|---|
| CLI | run the command on committed fixtures | exit code plus expected stdout or output file hash |
| HTTP API | start the service, call endpoints with a script | status codes and response fields |
| web UI | browser automation against the started service | DOM text assertions, screenshot diff within a measured tolerance |
| native GUI | accessibility-tree or screen driver script | element states, screenshot diff |
| media or render output | render on fixtures, compare to a reference | decode succeeds, dimensions and duration match, frame or audio diff within a measured tolerance |

- Use the repo's existing runner when there is one. Otherwise create the smallest runner for the entry point the goal changes, and commit its fixtures.
- Measure a tolerance before setting it: run the same input twice, record the difference, and confirm a deliberately broken control is rejected at that tolerance.
- Visual or semantic checks no script can decide get a review checklist in the repo, and the loop pastes the filled checklist as evidence.

## Scaffold

Worktree mode (the target is a git repo whose worktree may be touched) adds a worktree under `~/.agents/goals/<YYMMDD-HHMMSS-tag>` on the target's `goal/<tag>` branch. Dedicated-repo mode (the target is not git, or its git must stay untouched) creates `~/.agents/goals/<YYMMDD-HHMMSS-name>` as its own repo; the repo itself is the ledger.

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/goal-plan/scripts/init_goal_plan.py --worktree <tag> --goal "<one measurable end state>" [--issue N] [--proof-command '<exact command>']
python3 ${CLAUDE_PLUGIN_ROOT}/skills/goal-plan/scripts/init_goal_plan.py --dedicated <name> --goal "<one measurable end state>" [--issue N] [--proof-command '<exact command>']
```

- Pass `--proof-command` only for a Proof that fits the Stop gate rule in `harness-layers.md`; it fills the Proof and installs the gate in `.claude/settings.json` and `.codex/hooks.json`.
- An existing `AGENTS.md` is preserved. A changed `GOAL.md` is copied to `.bak` first. No project `CLAUDE.md` is created, because Claude Code reads `AGENTS.md` directly; an existing `CLAUDE.md` is left untouched and reported, since it makes Claude skip `AGENTS.md`.
- The ledger lives on the `goal/<tag>` branch, so removing the external worktree later loses nothing.

## Handoff Response

After the plan commit, answer with the goal in one sentence; the plan overview (acceptance criteria, Proof, environment, verification layers with status, progress rows); the workspace path, branch, and plan commit hash; and the handoff commands `!cd <workspace>` and `/goal @GOAL.md`. Do not execute either. `python3 <skill>/scripts/goal_log.py condition` is an optional readiness check before handing off.
