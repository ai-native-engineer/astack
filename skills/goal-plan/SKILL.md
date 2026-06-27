---
name: goal-plan
description: "Create and maintain a lightweight /goal plan for long-running agent work: GOAL.md instructions plus progress.tsv plan/progress scoreboard. Use when the user asks for a goal plan, goal workspace, goal harness, /goal setup, durable progress tracking, completion conditions, or resumable long-running task state. Do NOT use for short one-shot tasks that do not need persistent state."
---

# Goal Plan

Set up a durable workspace for a long-running `/goal` loop, then track progress through it. Two files plus git:

- `GOAL.md`: the instructions and loop protocol the goal runs on. Start with `/goal @GOAL.md`.
- `progress.tsv`: the plan and progress table. Edit it only through `goal_log.py`, never by hand.
- git: each loop step ends in a commit, so the commit history is the durable, resumable record of what was tried and kept.

## Setup: interview, then scaffold

GOAL.md needs more than a one-line goal. Before scaffolding, settle these with the user up front (1-2 tight rounds, not a long survey; in Claude Code, via AskUserQuestion) -- they fill the GOAL.md sections (the Context section you fill from the repo, not the user):

- Goal -- one measurable end state
- Proof -- the command/check that proves it; read the repo and PROPOSE it ("done = `pytest -q` green"), then confirm, do not ask cold
- Scope / Out of Scope -- what is included, what is excluded or deferred
- Constraints -- what must not change, required tools, paths git may touch
- Bounds -- time/turn limit for unattended running (or none)

Ask only what you cannot infer from the repo. Then scaffold into a git worktree, so the main tree stays free for other work and a failed goal leaves no trace on it:

```bash
python3 ~/.claude/skills/goal-plan/scripts/init_goal_plan.py --worktree <tag> --goal "<one measurable end state>"
```

This adds a `goal/<tag>` worktree under `.claude/worktrees/`, seeds the GOAL.md skeleton (the sections above as `TBD` placeholders) plus `progress.tsv` there, and prints the path. Replace every `TBD` from the interview, then start the loop from that path with `/goal @GOAL.md` (in Claude Code, `EnterWorktree` switches the session into it). The ledger lives on the `goal/<tag>` branch, so removing the worktree later never loses it.

When a worktree can't apply -- the target's git must stay untouched (auditing a read-only repo, research over a corpus), or the target is not a git repo -- make a dedicated goal repo instead and init there:

```bash
mkdir <dir> && git -C <dir> init && python3 ~/.claude/skills/goal-plan/scripts/init_goal_plan.py <dir> --goal "<one measurable end state>"
```

`init_goal_plan.py` skips existing files and never overwrites a live workbench.

## Progress: use goal_log.py, not hand edits

Editing a TSV by hand breaks on tab matching across context resets. Drive every change through the helper, run from the workspace dir (full flags: `goal_log.py <cmd> --help`):

- `add --task ... [--done-when ...] [--next ...]` -> append a todo row, prints its id
- `start <id>` / `block <id>` / `drop <id>` -> status transitions
- `done <id> --decision keep|discard|crash --artifact "<proof>"` -> close a row, stamps the current `HEAD` checkpoint; artifact or notes evidence is required
- `set <id> --col <column> --value <v>` -> edit any field
- `show [--status doing]` -> read the table

The script auto-fills id and checkpoint, escapes tabs/newlines, and validates the status/decision enums.

## Each step is a commit

The loop is: take a row -> work -> record the outcome with `goal_log.py` -> commit. The commit captures the work plus the `progress.tsv` change, so even a non-code step has a real diff to commit (no empty commits). `goal_log.py done` stamps the current `HEAD` as the row's resume checkpoint; the commit you make immediately after is the durable ledger entry for that step. Commit discarded attempts too rather than `git reset` them away, or the record is lost.

## Writing a good Goal + Proof

- Outcome-first: the Goal states what must be true, not every step to take.
- The Proof is deterministic, repeatable evidence: command output, tests, build status, file count, queue state, or a log path -- not a "looks good" judgment, because on an unattended run the agent is the only verifier.
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

Two files plus git is the floor, not a cap. Add subagents, workflows, or extra files only when the work needs them: real parallelism, adversarial verification, repeated triage, or scale. For a goal with many distinct acceptance tests, add an `## Acceptance Criteria` section to GOAL.md (2-4 checkable items) instead of overloading each `done_when`.

Use plain `/goal` for one-off long-running work with a single condition; pair with `/loop` for work that repeats (triage, periodic checks), and use a scheduled routine for work that must outlive the session. Avoid `/goal` for one-line edits, vague finish lines ("improve X"), or a condition gameable without real progress.

Runtime specifics -- pause/resume, headless runs, auto-stop, enabling goals -- differ by tool; read `references/claude-code-goal.md` or `references/codex-goal.md` for the one you run on.
