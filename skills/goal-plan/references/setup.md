# Goal Plan Setup

Read this when creating a goal plan.

## Setup Flow

1. Inspect the target enough to infer defaults: repo type, likely proof commands, mutable inputs, and change-tracking mode.
2. Give the user a compact overview of the inferred plan: goal, proof, scope, constraints, and open risks.
3. Ask 1-3 concrete interview questions before scaffolding. If a structured clarification UI is available, use it.
4. Scaffold only after the user answers, or after the user explicitly says to use defaults or skip questions.
5. Replace every `TBD`, add the initial progress rows, commit the plan, then stop.

## Workspace Choice

- If the target is a git repo and its git/worktree may be touched, scaffold into an external git worktree under `~/.agents/goals/<YYMMDD-HHMMSS-name>`.
- If the target is not a git repo, or target git must stay untouched, scaffold a dedicated goal repo under `~/.agents/goals/<YYMMDD-HHMMSS-name>`.
- Dedicated goal repos track the goal ledger, not external target edits by magic.

## Worktree Mode

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/goal-plan/scripts/init_goal_plan.py --worktree <tag> --goal "<one measurable end state>"
```

This adds a timestamped worktree under `~/.agents/goals/<YYMMDD-HHMMSS-tag>` on the target repo's `goal/<tag>` branch, extends `AGENTS.md`, writes `CLAUDE.md` as `@AGENTS.md`, seeds `progress.tsv`, and prints the path.

If `AGENTS.md` already exists, it is copied to `AGENTS.md.bak` before the goal block is appended or replaced. If `CLAUDE.md` already exists, it is copied to `CLAUDE.md.bak` before the thin `@AGENTS.md` entrypoint is written.

Replace every `TBD`, commit the plan, then stop. Hand off:

```bash
!cd <printed worktree path>
/goal @AGENTS.md
```

The ledger lives on the `goal/<tag>` branch, so removing the external worktree later does not lose it.

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
- the plan overview: acceptance criteria, proof commands/checks, and progress row summary;
- the workspace path, branch, and plan commit hash;
- the exact run commands:

```bash
!cd <printed workspace path>
/goal @AGENTS.md
```

Do not run the loop, proof, or target edits during setup.
