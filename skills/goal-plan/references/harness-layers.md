# Harness Layers

Read this when filling Verification Layers, when proposing defaults in the setup interview, and when a harness row installs a hook.

## 목차

- Four Layers
- Agent Hook Events
- Baseline by Repo Signal
- Rules
- Installing and Proving Hooks

## Four Layers

A harness is not one hook. Checks fire at four different moments, and each layer catches what the others cannot, so a goal stacks them rather than picking one.

| layer | fires | runs where | catches | misses |
|---|---|---|---|---|
| agent hooks (`.claude/settings.json`, `.codex/hooks.json`) | around tool calls, on session start, prompt submit, stop, compaction | inside that runtime only | format and lint right after an edit, forbidden edits, stopping before the Proof passes | edits made by hand or by another runtime |
| git hooks (`pre-commit`, `commit-msg`, `pre-push`) | at commit and push | any committer's machine | lint and tests on the staged set, commit subject rules (`#N`), full suite before push | `--no-verify`, clones that never installed them |
| CI (GitHub Actions) | on push and PR | a clean remote runner | the full suite, e2e on committed fixtures, the build | too slow to gate a loop row |
| branch protection (required checks, review) | at merge | GitHub | merging a PR whose checks failed | the content itself |

Agent hooks and git hooks overlap on purpose: a hand edit skips the agent hooks and is caught at commit; `git commit --no-verify` skips the git hooks and can be refused by a `PreToolUse` hook on Bash; a false pass in both is caught by CI and the Proof.

## Agent Hook Events

Claude Code and Codex use the same event names and the same JSON on stdin, so one group installed in both files behaves the same under either runtime. Exit 0 lets the action continue, exit 2 blocks it and returns stderr to the agent.

| event | use in a goal loop |
|---|---|
| `SessionStart` | print the last `progress.tsv` row and its `next`, confirm the Environment services are up |
| `UserPromptSubmit` | append a standing rule or the current row to the prompt |
| `PreToolUse` | block edits to `.env`, lock files, and the `GOAL.md` Proof section; block `git push --force` and `git commit --no-verify`; pause on a command that needs the user |
| `PostToolUse` | after `Edit|Write`: format, lint, type-check, run the tests that import the changed file |
| `SubagentStop` | check that a subagent that reports "tests pass" left a test log |
| `PreCompact` | write a checkpoint row so the next context window resumes from it |
| `Stop` | run the Proof; a failure blocks once with the output (`scripts/stop_gate.py`) |

## Baseline by Repo Signal

Inspect the target in Setup Flow step 1 and propose every matching line as a default in the verification-layers question. The user accepts or declines each line; declined lines go to Decisions with the reason.

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

- A check that runs on every edit finishes in about ten seconds; anything slower moves to `pre-commit`, `pre-push`, or CI. A slow `PostToolUse` hook stalls every row.
- Every hook the goal adds is a harness row with a `done_when` that fires it on a sample: `goal_hooks.py fire` for agent hooks, a sample commit or `git hook run` for git hooks, a green run on the goal branch for CI. "Config file exists" is not done.
- Never loosen, skip, or delete a layer to make a row pass; a row that must change a hook, timeout, snapshot, or rule says why in `notes` and in the commit message.
- Use the repository's own tools. Git hooks go through the framework the repo already has (`lefthook`, `pre-commit`, `husky`); add one only when the repo has none, and record the choice in Decisions. Agent hooks go into the project's own `.agents/hooks/` source when the repo keeps one, followed by the repo's sync command as the harness row.
- Blocking hooks exit 2 with one line of stderr that names the file and the rule, so the agent can act on it instead of guessing.

## Installing and Proving Hooks

`scripts/goal_hooks.py` writes one command hook into both runtime files, dedupes by (event, matcher, command), and refuses when `.claude` or `.codex` is a symlink out of the workspace.

```bash
python3 <skill>/scripts/goal_hooks.py add --event PostToolUse --matcher 'Edit|Write' --command 'pnpm biome check --write "$(jq -r .tool_input.file_path)"' --timeout 20
python3 <skill>/scripts/goal_hooks.py add --event PreToolUse --matcher 'Edit|Write' --command 'tools/block-protected.sh'   # a repo script: reads the JSON, exits 2 for .env and lock files
python3 <skill>/scripts/goal_hooks.py list
python3 <skill>/scripts/goal_hooks.py fire PostToolUse --tool Edit --file src/x.ts        # lists the commands that would run, runs nothing
python3 <skill>/scripts/goal_hooks.py fire PostToolUse --tool Edit --file src/x.ts --trust-workspace   # exit 0: every matching hook ran clean
python3 <skill>/scripts/goal_hooks.py fire PreToolUse --tool Edit --file .env --expect-block --trust-workspace   # exit 0 only when the hook blocked (exit 2)
python3 <skill>/scripts/goal_hooks.py remove <id>
```

`fire` runs shell lines from the workspace config, so like the runtimes it first lists them and runs only with `--trust-workspace`, with a minimal environment (`PATH`, `HOME`, `CLAUDE_PROJECT_DIR`). It feeds the same JSON the runtimes send (`hook_event_name`, `tool_name`, `tool_input.file_path`, `stop_hook_active`) to each matching command with `CLAUDE_PROJECT_DIR` set, prints each exit code, and fails when a hook crashes or blocks unexpectedly. A hook command reads that JSON on stdin; `jq -r .tool_input.file_path` is the usual first line. The Stop gate installed by `init_goal_plan.py --proof-command` is listed but managed by that script.

Harness row examples:

| task | done_when |
|---|---|
| install PostToolUse lint on changed files | `goal_hooks.py fire PostToolUse --file <sample> --trust-workspace` exits 0 on a clean file and 1 on a file with a planted lint error |
| block `.env` and lock-file edits | `goal_hooks.py fire PreToolUse --file .env --expect-block --trust-workspace` exits 0; same for `pnpm-lock.yaml` |
| pre-commit lint and unit tests via lefthook | `lefthook install` done; a sample commit with a planted failing test is refused and the next clean commit passes |
| CI on the goal branch | the workflow run for the latest goal-branch push is green and listed as a required check |

The e2e means table and the fixture rules stay in `setup.md`; this file covers when and where checks fire.
