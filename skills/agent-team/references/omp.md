# OMP

Read only when OMP is the coordinator or selected worker. The common scope and result contract stays in the parent skill.

OMP reads shared `.agents/skills` and `.agents/rules` natively. Read the current installed tool schemas before spawning workers; model names and tool arguments belong to that runtime. `scripts/pick_worker_model.py --harness omp` reads the cached native model catalog and requires `OMP_WORKER_PROVIDER` naming the existing configured provider to avoid selecting an unrelated route. Availability in the catalog does not prove credentials or model execution.

Use the existing CLIProxyAPI provider. Claude Code and Codex keep native subscription authentication. Keep secrets in native secure configuration and agents-env; never transfer another harness's auth files or token values.

For a visible pane, inspect `herdr integration --help` and installed native OMP support. Do not relabel it as another runtime. The shared Herdr worker helper supports only Codex/Claude; unsupported OMP paths stay blocked until native tooling is verified. Resume uses the exact original file/cwd and OMP's installed `--resume` contract. `resume-audit` is read-only and does not prove a restarted conversation.

The skill-manager OMP extension connects shared explicit-path edit checks, pre-read recording, post-edit checks, bounded memory-index injection and shutdown logging. Native loading/event behavior and activation are separate checks. Shell/eval and opaque extension mutations have no shared safety parity; unsupported glob/implicit ast_edit and protocol writes are held. Read the local-installation OMP section before setup.
