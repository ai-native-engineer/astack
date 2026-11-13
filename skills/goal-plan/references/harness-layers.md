# Harness Layers

Read this when filling Verification Layers, when proposing defaults in the setup interview, and when a harness row installs a hook.

## Agent Hook Events

Exit 0 lets the action continue, exit 2 blocks it and returns stderr to the agent. Event names are in `goal_hooks.py`; the ones a goal loop uses:

| event | use in a goal loop |
|---|---|
| `SessionStart` | print the last `progress.tsv` row and its `next`, confirm the Environment services are up |
| `PreToolUse` | block edits to `.env`, lock files, and the `GOAL.md` Proof section; block `git push --force` and `git commit --no-verify`; pause on a command that needs the user |
| `PostToolUse` | after `Edit\|Write`: format, lint, type-check, run the tests that import the changed file |
| `PreCompact` | write a checkpoint row so the next context window resumes from it |

## Baseline by Repo Signal

Propose every matching line as a default. The user accepts or declines each line; declined lines go to Decisions with the reason.

| signal in the repo | agent hook | git hook | CI |
|---|---|---|---|
| formatter or linter config (`biome.json`, `.eslintrc`, `ruff.toml`, `.prettierrc`) | `PostToolUse` `Edit\|Write`: format and lint the changed file | `pre-commit`: lint the staged set | lint job |
| typed language config (`tsconfig.json`, `mypy.ini`, `pyrightconfig.json`) | `PostToolUse`: type-check the changed package when it finishes in seconds; otherwise `pre-commit` | `pre-commit` or `pre-push`: full type-check | type-check job |
| test directory or runner config (`tests/`, `vitest.config`, `pytest.ini`) | `PostToolUse`: run the tests related to the changed file | `pre-push`: the full suite | full suite on every push |
| committed fixtures for an e2e entry point | none (too slow) | `pre-push` when under a minute | e2e job; required check on the result PR |
| `.env`, `*.pem`, credentials files | `PreToolUse` `Edit\|Write`: block | `pre-commit`: refuse to stage them | secret scan |
| lock files (`pnpm-lock.yaml`, `uv.lock`, `Cargo.lock`) | `PreToolUse`: block direct edits; changes come from the package manager | none | install must be reproducible (`--frozen-lockfile`) |
| GitHub remote with a tracking issue | none | `commit-msg`: subject carries `#N` | required checks before merge |
| a goal with a fast deterministic Proof | `Stop`: Proof gate | none | the same command as a job |
| a goal expected to span context windows | `SessionStart` status, `PreCompact` checkpoint | none | none |

## Rules

- A check that runs on every edit finishes in about ten seconds; anything slower moves to `pre-commit`, `pre-push`, or CI.
- Every hook the goal adds is a harness row with a `done_when` that fires it on a sample: `goal_hooks.py fire` for agent hooks, a sample commit with a planted failure for git hooks, a green run on the goal branch for CI. "Config file exists" is not done.
- Use the repository's own tools. Git hooks go through the framework the repo already has (`lefthook`, `pre-commit`, `husky`); add one only when the repo has none, and record the choice in Decisions.
- The Stop gate (`init_goal_plan.py --proof-command`, `scripts/stop_gate.py`) blocks a Stop once with the Proof's failing output. Use it only for a fast, deterministic, bounded, non-interactive, non-destructive Proof; slow, flaky, costly, destructive, or human-only checks stay in the final Proof.
- Blocking hooks exit 2 with one line of stderr that names the file and the rule, so the agent can act on it instead of guessing.

## Installing and Proving Hooks

```bash
python3 <skill>/scripts/goal_hooks.py add --event PostToolUse --matcher 'Edit|Write' --command 'pnpm biome check --write "$(jq -r .tool_input.file_path)"' --timeout 20
```

A hook command reads the event JSON on stdin; `jq -r .tool_input.file_path` is the usual first line. `goal_hooks.py fire` proves it on a sample (the script docstring has the forms).
