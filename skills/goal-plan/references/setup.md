# Goal Plan Setup

Read this when creating a goal plan.

## 목차

- Setup Flow
- Interview
- Harness Rows
- Choosing e2e Means
- Optional Stop Gate
- Workspace Choice
- Worktree Mode
- Dedicated-Repo Mode
- Mutable Inputs
- Handoff Response

## Setup Flow

1. Inspect the target enough to infer defaults: repo type, test and lint commands, services the Proof needs and how they start, mutable inputs, and change-tracking mode. Match what you find against the baseline table in `harness-layers.md` so each repo signal (formatter config, test runner, `.env`, lock files, GitHub remote) yields the hooks, git hooks, and CI the goal should have.
2. Give the user a compact overview of the inferred plan: goal, proof, scope, environment, verification layers, GitHub flow, constraints, and open risks.
3. Interview with the question set below, 1-3 questions per round, until every section has an answer. If a structured clarification UI is available, use it.
4. Show the final overview and wait for the user to approve it in words. Scaffold only after that approval, or after the user explicitly says to use defaults or skip questions. Having seen the overview is not approval.
5. Replace every `TBD`, add the initial progress rows (baseline first, then harness rows, then feature rows), commit the plan, then stop.

## Interview

The interview has two jobs: pull out what the user actually wants, then pin it to defaults the repo supports. Open questions first for intent, proposed defaults afterwards for everything the repo can answer. Each answer has one home in `GOAL.md`.

| topic | ask | lands in |
|---|---|---|
| intent | Why this goal now, and what happens if it is not done? What is true when this is done, and for whom? What must not happen on the way? | Goal, Out of Scope, Decisions |
| premise | What is the simplest thing that would also satisfy the intent, and why is that not enough? What would make a reviewer reject the result even if every check passed? | Goal, Acceptance Criteria, Constraints |
| loop unit | What is one progress row: one issue, one feature, one file, one e2e cell? What does one row show before it counts as done? | row granularity, row `done_when` convention |
| success criteria | What check proves the goal (command, exit code, count, artifact)? When several deliverables exist, what proves each? | Proof, Acceptance Criteria |
| verification layers | Which of lint, unit tests, integration/e2e, agent hooks, git hooks, CI, scripts/tools exist with a working command? Propose every matching line of the `harness-layers.md` baseline as a default; which does the user accept, decline, or defer? Which missing layer must be built before feature work? Which checks run every edit, every commit, or only in the final Proof? | Verification Layers, harness rows, Decisions |
| environment | From a fresh checkout, what installs, starts, waits for readiness, and cleans up? Which tools and secrets are required, and where do secrets come from? | Environment |
| GitHub flow | Tracking issue: existing, new, or none? Result PR base branch, one PR or one per deliverable? The user merges unless they say otherwise. | GitHub Flow |
| bounds and approvals | Turn or time limit? Which irreversible actions (delete, network send, publish, pay) are pre-approved and which pause for the user? | Bounds, Constraints |
| inputs and tracking | Does any input change while the goal runs? Where do target edits get committed? | Input Stability, Target Change Tracking |

Rules for the interview:

- Intent and premise are asked open, one question at a time, and each next question builds on the last answer. A proposed default here anchors the user to the agent's guess, which is the thing the interview exists to avoid.
- Everything else is asked with the default inferred from the repo, so the user confirms or corrects instead of composing. Prefer concrete options once a default exists: "Proof A: `./run test` exit 0. Proof B: A plus the e2e lane. Which?"
- Follow up on every answer once: ask how that answer would be observed (which command, output, count, or artifact) until it is a checkable sentence. An answer that cannot be observed is not settled yet.
- Convert vague words ("improve", "features", "works") into a checkable sentence before moving on; the follow-up above is how.
- Round 1 settles the finish line (intent, premise, loop unit, success criteria, scope). Round 2 settles how the loop runs (verification layers, environment, GitHub flow, bounds and approvals, inputs and tracking). Extra rounds only for answers that opened a new question; do not re-ask a settled topic.
- Record every answer in `GOAL.md` Decisions as the interview goes, with the user's words quoted. Defaults the user accepted without comment are `accepted default`.
- When a layer is missing, ask whether to build it in this goal or leave it out of the Proof. Do not silently assume either.
- Baseline lines the user declines are recorded in Decisions with the reason, so the loop does not re-propose them and a later goal can pick them up from Out of Scope.
- When the answer is irreversible or costly (uploads, payments, deletions, paid APIs), write the exact pre-approval into Constraints; "approved" without the target and scope is not an approval.
- Stop interviewing when no TBD remains and the user has approved the final overview in words.

## Harness Rows

A verification layer with status `build in row N` becomes a progress row before any feature row that depends on it. Give each harness row its own `done_when` that proves the layer works on the current code: the lint runs clean or reports known findings, the test runner executes at least one test, the e2e script passes on a fixture, an agent hook passes `goal_hooks.py fire` on a sample file, a git hook refuses a sample commit with a planted failure, the environment script succeeds twice in a row. Layer-by-layer examples are in `harness-layers.md`. The Proof may only rely on a layer whose row is `done`. Prefer the repo's existing tools; add a new tool only when the repo has none for that job, and record the choice in Decisions.

## Choosing e2e Means

| entry point | means | pass signal |
|---|---|---|
| CLI | run the command on committed fixtures | exit code plus expected stdout or output file hash |
| HTTP API | start the service, call endpoints with a script | status codes and response fields |
| web UI | browser automation against the started service | DOM text assertions, screenshot diff within a measured tolerance |
| native GUI | accessibility-tree or screen driver script | element states, screenshot diff |
| media or render output | render on fixtures, compare to a reference | decode succeeds, dimensions and duration match, frame or audio diff within a measured tolerance |

- Use the repo's existing runner when there is one. Otherwise create the smallest runner for the entry point the goal changes, and commit its fixtures.
- Measure a tolerance before setting it: run the same input twice, record the difference, and confirm a deliberately broken control (wrong caption, missing frame) is rejected at that tolerance.
- Visual or semantic checks no script can decide get a review checklist in the repo, and the loop pastes the filled checklist as evidence.

## Optional Stop Gate

When the Proof is fast, deterministic, bounded, non-interactive, and non-destructive, pass it during scaffolding:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/goal-plan/scripts/init_goal_plan.py --dedicated <name> --goal "<one measurable end state>" --proof-command '<exact command>'
```

This fills the generated Proof and installs the same `scripts/stop_gate.py` command hook in `.claude/settings.json` and `.codex/hooks.json`. The gate translates a failed Proof into a blocking Stop response once; `stop_hook_active` prevents an unbounded hook-only loop while `/goal` remains responsible for continued work and Bounds. Review and trust project hooks when the runtime prompts. Omit `--proof-command` for slow, flaky, costly, destructive, or human-only checks and keep them in the final Proof.

## Workspace Choice

- If the target is a git repo and its git/worktree may be touched, scaffold into an external git worktree under `~/.agents/goals/<YYMMDD-HHMMSS-name>`.
- If the target is not a git repo, or target git must stay untouched, scaffold a dedicated goal repo under `~/.agents/goals/<YYMMDD-HHMMSS-name>`.
- Dedicated goal repos track the goal ledger, not external target edits by magic.

## Worktree Mode

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/goal-plan/scripts/init_goal_plan.py --worktree <tag> --goal "<one measurable end state>" [--issue N]
```

This adds a timestamped worktree under `~/.agents/goals/<YYMMDD-HHMMSS-tag>` on the target repo's `goal/<tag>` branch, preserves the repo's `AGENTS.md`, writes the goal contract to `GOAL.md`, writes `CLAUDE.md` as `@AGENTS.md`, seeds `progress.tsv`, and prints the path.

If `AGENTS.md` does not exist, the generator creates a minimal file for repo-wide rules. If `GOAL.md` or a regular `CLAUDE.md` already exists and changes, it is copied to a `.bak` file before replacement. An existing relative or absolute `CLAUDE.md` symlink to the sibling `AGENTS.md` is kept unchanged. Foreign, dangling, or cyclic links fail before scaffold writes rather than overwriting their targets.

The ledger lives on the `goal/<tag>` branch, so removing the external worktree later does not lose it. The result PR is built from that branch without the scaffold files; see `github-flow.md`.

## Dedicated-Repo Mode

Use a short kebab-case name:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/goal-plan/scripts/init_goal_plan.py --dedicated <name> --goal "<one measurable end state>"
```

Example path: `~/.agents/goals/260629-151845-llm-wiki-link-audit`.

If target edits are in scope and the target is not a git repo, settle one tracking mode before the loop starts:

- user approves `git init` in the target, then target commits carry code diffs;
- target stays non-git, so each loop step commits patch/snapshot artifacts in the goal repo;
- target is read-only, so the goal can only produce reports or external artifacts.

Do not leave target code changes as the only uncommitted record unless the user explicitly chooses that risk.

## Mutable Inputs

For session logs, queues, feeds, calendars, live APIs, or changing folders, choose one:

- snapshot the input into the goal repo or target worktree;
- record an `as_of` cutoff and make the parser ignore newer records;
- state that the proof is intentionally "current at proof time" and expect counts to drift.

## Handoff Response

After the plan commit, answer with:

- the goal in one sentence;
- the plan overview: acceptance criteria, proof commands/checks, environment, verification layers with their status, GitHub flow, and the progress row summary;
- the workspace path, branch, and plan commit hash;
- the exact run commands: `!cd <workspace>` and the line printed by `python3 <skill>/scripts/goal_log.py condition`, which names the goal and Proof because `/goal` registers its argument verbatim. The command refuses while any `TBD`, an empty Decisions section, or an `AC-n` without `Proof:` remains, so a refusal means the interview is not finished.

Do not run the loop, proof, or target edits during setup.
