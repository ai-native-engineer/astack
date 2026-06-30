---
name: goal-plan
description: "Create and maintain a lightweight /goal plan for long-running agent work: GOAL.md instructions plus progress.tsv plan/progress scoreboard. Use when the user asks for a goal plan, goal workspace, goal harness, /goal setup, durable progress tracking, completion conditions, or resumable long-running task state. Do NOT use for short one-shot tasks that do not need persistent state."
---

# Goal Plan

Set up a durable workspace for a long-running `/goal` loop, then track progress through it. This skill has two distinct phases:

- **Setup phase**: create `GOAL.md` and `progress.tsv`, commit the plan, then stop and tell the user the exact `/goal @GOAL.md` command. Do not start progress rows, edit target files, or run the Proof in setup phase.
- **Loop phase**: starts only after the user invokes `/goal @GOAL.md` or an active goal continuation is present. Then follow `progress.tsv`, work, verify, and commit each step.

The durable record is two files plus git:

- `GOAL.md`: the instructions and loop protocol the goal runs on. Start with `/goal @GOAL.md`.
- `progress.tsv`: the plan and progress table. Edit it only through `goal_log.py`, never by hand.
- git: each loop step ends in a commit, so the commit history is the durable, resumable record of what was tried and kept.

## Setup: interview, then scaffold, then stop

GOAL.md needs more than a one-line goal. Before scaffolding, inspect the repo enough to propose concrete defaults, then settle these with the user up front (1-2 tight rounds, not a long survey; in Claude Code, via AskUserQuestion). Ask only what changes the run, and fill the Context section from the repo, not the user:

- Goal -- one measurable end state
- Proof -- the command/check that proves it; propose it from the repo, then confirm. Make it self-contained: if a service must run, include start, readiness/wait, check, and cleanup.
- Acceptance Criteria -- add 2-5 checkable items when the request spans multiple systems, has vague words like "improve/features", or has several deliverables.
- Scope / Out of Scope -- what is included, what is excluded or deferred
- Constraints -- what must not change, required tools, paths git may touch
- Input Stability -- for mutable sources, define a snapshot path, cutoff timestamp, or explicit "current at proof time" caveat
- Target Change Tracking -- where target edits will be committed or snapshotted
- Bounds -- time/turn limit for unattended running (or none)

For broad requests, convert fuzzy language into acceptance criteria before writing GOAL.md. If "several features" could mean read-only status versus remote actions, ask one tight question; do not silently pick the more invasive scope.

For recommendation, audit, research, or synthesis goals, add one semantic quality acceptance item. Structural checks prove shape, not judgment. The quality item should say what a human-readable result must satisfy: evidence examples are relevant, ranking rationale is explainable, exclusions/gaps are named, and generic keyword matches are not enough.

Then scaffold into a git worktree, so the main tree stays free for other work and a failed goal leaves no trace on it:

```bash
python3 ~/.claude/skills/goal-plan/scripts/init_goal_plan.py --worktree <tag> --goal "<one measurable end state>"
```

This adds a `goal/<tag>` worktree under `.claude/worktrees/`, seeds the GOAL.md skeleton plus `progress.tsv` there, and prints the path. Replace every `TBD` from the interview, commit the plan, then stop. Tell the user to start the loop from that path with `/goal @GOAL.md` (in Claude Code, `EnterWorktree` switches the session into it). The ledger lives on the `goal/<tag>` branch, so removing the worktree later never loses it.

When a worktree can't apply -- the target's git must stay untouched (auditing a read-only repo, research over a corpus), or the target is not a git repo -- make a dedicated goal repo instead and init there:

```bash
mkdir <dir> && git -C <dir> init && python3 ~/.claude/skills/goal-plan/scripts/init_goal_plan.py <dir> --goal "<one measurable end state>"
```

`init_goal_plan.py` skips existing files and never overwrites a live workbench.

Dedicated goal repos track the goal ledger, not external target edits by magic. If target edits are in scope and the target is not a git repo, settle one tracking mode before the loop starts:

- user approves `git init` in the target, then target commits carry code diffs;
- target stays non-git, so each loop step commits patch/snapshot artifacts in the goal repo;
- target is read-only, so the goal can only produce reports or external artifacts.

Do not leave target code changes as the only uncommitted record unless the user explicitly chooses that risk.

For mutable data sources such as session logs, queues, feeds, calendars, live APIs, or changing folders, freeze the input before unattended work when repeatability matters:

- snapshot the input into the goal repo or target worktree;
- or record an `as_of` cutoff and make the parser ignore newer records;
- or state that the proof is intentionally "current at proof time" and expect counts to drift.

Do not call a proof deterministic if rerunning it can silently analyze a different input set.

## Progress: use goal_log.py, not hand edits

Use this section only in loop phase. Editing a TSV by hand breaks on tab matching across context resets. Drive every change through the helper, run from the workspace dir (full flags: `goal_log.py <cmd> --help`):

- `add --task ... [--done-when ...] [--next ...]` -> append a todo row, prints its id
- `start <id>` / `block <id>` / `drop <id>` -> status transitions
- `done <id> --decision keep|discard|crash --artifact "<proof>"` -> close a row, stamps the current `HEAD` checkpoint; artifact or notes evidence is required
- `set <id> --col <column> --value <v>` -> edit any field
- `show [--status doing]` -> read the table

The script auto-fills id and checkpoint, escapes tabs/newlines, and validates the status/decision enums.

## Each step is a commit

The loop is: take a row -> work -> record the outcome with `goal_log.py` -> commit. The commit captures the work plus the `progress.tsv` change, so even a non-code step has a real diff to commit (no empty commits). `goal_log.py done` stamps the current `HEAD` as the row's resume checkpoint; the commit you make immediately after is the durable ledger entry for that step. Commit discarded attempts too rather than `git reset` them away, or the record is lost.

Keep row granularity aligned with real work. If one script/report pass will produce coverage, parser, ranking, and validation together, make that one row with acceptance criteria instead of four rows that later become ledger-only closures. If a single artifact legitimately satisfies several existing rows, say that in each artifact field, then collapse future plans rather than repeating the pattern.

## Writing a good Goal + Proof

- Outcome-first: the Goal states what must be true, not every step to take.
- The Proof is deterministic, repeatable evidence: command output, tests, build status, file count, queue state, or a log path -- not a "looks good" judgment, because on an unattended run the agent is the only verifier.
- The Proof is self-contained: include service startup, readiness checks, cleanup, and required env where needed, so a future run can reproduce it without hidden terminal state.
- For report/recommendation goals, the Proof must include a semantic review gate in addition to schema/section validation. Inspect representative rows or examples before completion; a green validator that only checks headings is weak evidence.
- The `/goal` evaluator reads the conversation, not the filesystem -- surface the Proof output in your replies, not just in files.
- Completion is evidence, not confidence: the evaluator is tuned skeptical and rejects "probably done", and budget or turn exhaustion is not completion.

## progress.tsv schema

```tsv
id	status	decision	task	done_when	checkpoint	artifact	next	notes
```

- `status`: todo, doing, done, blocked, dropped.
- `decision`: n/a (open), keep (advanced the goal), discard (tried, no progress but no harm), crash (tried, caused a regression -- usually needs git revert).
- `checkpoint`: current `HEAD` commit hash when `goal_log.py done` ran; the following git commit records the row update.
- `artifact`: the proof -- every done row needs evidence here or in notes.
- `next`: the next action if the row is not complete.

The first row is the baseline/current state before changes.

## When to add more

Two files plus git is the floor, not a cap. Add subagents, workflows, or extra files only when the work needs them: real parallelism, adversarial verification, repeated triage, or scale. For a goal with many distinct acceptance tests, add an `## Acceptance Criteria` section to GOAL.md instead of overloading each `done_when`.

Use plain `/goal` for one-off long-running work with a single condition; pair with `/loop` for work that repeats (triage, periodic checks), and use a scheduled routine for work that must outlive the session. Avoid `/goal` for one-line edits, vague finish lines ("improve X"), or a condition gameable without real progress.

Runtime specifics -- pause/resume, headless runs, auto-stop, enabling goals -- differ by tool; read `references/claude-code-goal.md` or `references/codex-goal.md` for the one you run on.
