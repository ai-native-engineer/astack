# goal-plan

Maintainer documentation for the shared `goal-plan` skill. Runtime behavior and
agent instructions live in `SKILL.md` and `references/`.

## Design

`goal-plan` keeps long-running work resumable with the smallest durable set that
works:

- `AGENTS.md` holds repository rules that remain active throughout the workspace.
- `GOAL.md` holds the objective, proof, environment, verification layers, GitHub flow, constraints, and loop protocol. The setup interview (`references/setup.md`) fills it.
- `CLAUDE.md` is a thin `@AGENTS.md` entrypoint for Claude Code.
- `progress.tsv` records plan state, evidence, checkpoints, and next actions.
- git commits preserve each accepted or discarded work pass; `scripts/goal_pr.py` turns the goal branch into the result PR without the scaffold files.
- `goal_log.py condition` prints the `/goal` line, because `/goal` registers its argument verbatim and does not expand `@GOAL.md`.

## Sources

The original `goal-workbench`, later renamed and evolved into `goal-plan`, drew
its structure from these sources:

- [Karpathy autoresearch `program.md`](https://github.com/karpathy/autoresearch/blob/master/program.md) — a fixed objective, constrained loop, and experiment ledger.
- [Codex Exec Plans](https://developers.openai.com/cookbook/articles/codex_exec_plans/) — self-contained living plans, milestones, progress, and decision logs.
- [Run long-horizon tasks with Codex](https://developers.openai.com/blog/run-long-horizon-tasks-with-codex/) — iterative long-running work with explicit verification.
- [Harness engineering](https://openai.com/index/harness-engineering/) — repository-local instructions, plans, logs, and feedback loops as the system of record.
- [Claude Code goals](https://code.claude.com/docs/en/goal) — measurable completion conditions and proof surfaced in the conversation for evaluation.
- [Claude Code best practices](https://code.claude.com/docs/en/best-practices) — explicit verification signals and context management.
- [Codex hooks](https://developers.openai.com/codex/hooks) — deterministic Stop gates, continuation feedback, and bounded `stop_hook_active` retries.
- [Claude Code hooks](https://code.claude.com/docs/en/hooks) — the event list (`SessionStart`, `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `SubagentStop`, `PreCompact`, `Stop`), the stdin JSON, and exit 2 as a block; Codex reads the same format, which is why `goal_hooks.py` writes one group to both files.
- [git hooks](https://git-scm.com/docs/githooks) — `pre-commit`, `commit-msg`, `pre-push` as the layer that fires for any committer, independent of the agent runtime; `harness-layers.md` stacks it with agent hooks and CI.
- [Dynamic workflows in Claude Code](https://claude.com/blog/a-harness-for-every-task-dynamic-workflows-in-claude-code) — add orchestration only for real scale, parallelism, or adversarial verification.

Later refinements also used the following source packs:

- [Codex goals use case](https://developers.openai.com/codex/use-cases/follow-goals/) and [Using goals in Codex](https://developers.openai.com/cookbook/examples/codex/using_goals_in_codex/) — outcome, proof, boundaries, iteration policy, and blocked stop conditions.
- [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) — progress files, git checkpoints, and testable handoffs across context windows.
- [Harness design for long-running apps](https://www.anthropic.com/engineering/harness-design-long-running-apps) — planner, generator, and evaluator contracts.
- [Trustworthy third-party evaluations](https://openai.com/index/trustworthy-third-party-evaluations-foundations/) — explicit budgets, attempts, scoring, limitations, and comparable evidence.
- [Claude Code memory and AGENTS.md](https://code.claude.com/docs/en/memory) and [Codex AGENTS.md discovery](https://developers.openai.com/codex/guides/agents-md) — which instruction files each runtime loads, which is why the harness lives in `GOAL.md` rather than a local instruction file.
- [superpowers brainstorming](https://github.com/obra/superpowers/blob/main/skills/brainstorming/SKILL.md) — one open question per message that builds on the last answer, and no building until the design is approved; the interview's intent and premise questions and the approval gate follow this.
- [Kiro specs](https://kiro.dev) EARS requirements (`WHEN <condition> THE SYSTEM SHALL <result>`, one id per requirement) — the Acceptance Criteria format, with a Proof per item added.
- [GitHub sub-issues REST API](https://docs.github.com/en/rest/issues/sub-issues) — `POST /repos/{owner}/{repo}/issues/{parent}/sub_issues` with the child's database id; one step of a goal is one sub-issue so the tracking issue page shows the steps and the PR links back to each.
- [Karpathy autoresearch](https://github.com/karpathy/autoresearch) preconditions (one metric, fixed eval, fixed budget, one editable file, cheap revert) compared with coding-agent loops (SWE-agent, OpenHands, Ralph loop) — why the ledger keeps keep/discard/crash but the Proof is an oracle check and the loop unit is a row, not a timed experiment.

These sources inform the design; `SKILL.md`, generated `AGENTS.md`/`GOAL.md`, and the
helper scripts remain the operational source of truth.
