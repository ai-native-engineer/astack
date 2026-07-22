# goal-plan

Maintainer documentation for the shared `goal-plan` skill. Runtime behavior and
agent instructions live in `SKILL.md` and `references/`.

## Design

`goal-plan` keeps long-running work resumable with the smallest durable set that
works:

- `AGENTS.md` holds the objective, proof, constraints, and loop protocol.
- `CLAUDE.md` is a thin `@AGENTS.md` entrypoint for Claude Code.
- `progress.tsv` records plan state, evidence, checkpoints, and next actions.
- git commits preserve each accepted or discarded work pass.

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
- [Dynamic workflows in Claude Code](https://claude.com/blog/a-harness-for-every-task-dynamic-workflows-in-claude-code) — add orchestration only for real scale, parallelism, or adversarial verification.

Later refinements also used the following source packs:

- [Codex goals use case](https://developers.openai.com/codex/use-cases/follow-goals/) and [Using goals in Codex](https://developers.openai.com/cookbook/examples/codex/using_goals_in_codex/) — outcome, proof, boundaries, iteration policy, and blocked stop conditions.
- [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) — progress files, git checkpoints, and testable handoffs across context windows.
- [Harness design for long-running apps](https://www.anthropic.com/engineering/harness-design-long-running-apps) — planner, generator, and evaluator contracts.
- [Trustworthy third-party evaluations](https://openai.com/index/trustworthy-third-party-evaluations-foundations/) — explicit budgets, attempts, scoring, limitations, and comparable evidence.

These sources inform the design; `SKILL.md`, generated `AGENTS.md`, and the
helper scripts remain the operational source of truth.
