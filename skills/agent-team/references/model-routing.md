# Worker Model Routing

Read this before selecting a worker model. Model targets are role intents, not IDs that can be copied between harnesses.

## Role defaults

| role | normal target | fallback target |
|---|---|---|
| `orchestrator` | current lead session model | current lead model |
| `implementation` | Sonnet | Opus, then current lead model |
| `implementation-complex` | Opus | current lead model |
| `research` | the harness's same-generation cheapest capable model | current lead model |

The orchestrator role is documented for worker contracts and run records, but the lead normally already runs with the intended model. Use `implementation-complex` when the task requires architectural judgment, broad cross-file changes, difficult debugging, or adversarial verification. Use `implementation` for bounded code changes with a known design.

## Resolve for the current harness

1. Classify the worker by role before spawning it.
2. Read the current tool schema or harness catalog for the allowed model values.
3. Translate the role target into that harness's native alias or model ID.
4. Pass the translated value explicitly when the harness accepts it.
5. Never pass a model ID from another harness just because the provider name looks compatible.

Claude Code accepts Claude model aliases such as `opus`, `sonnet`, and `haiku` when those aliases appear in the current Agent/Workflow tool contract. Codex accepts only the model IDs listed by its current `spawn_agent` contract or catalog. AGY, OMP, and other runtimes use their own current model lists. The orchestrator normally does not need a worker model conversion because it is the lead session.

For `research`, use:

```bash
python3 -I <skill-root>/scripts/pick_worker_model.py --harness <harness>
```

The picker chooses the cheapest capable model within the current generation for that harness. It does not choose the orchestrator or implementation tier.

## Rejection and fallback

If an explicitly translated model is rejected before the worker starts because the provider or catalog does not accept it:

1. Record the requested role and rejected value.
2. Resolve the next target for the same role using the current harness contract.
3. Retry that worker once with the compatible value.
4. If no compatible override exists, omit `model` once so the worker inherits the lead model.
5. Record the actual model, provider if known, requested role, rejected value, and fallback reason in the run record.

If it is unclear whether the first worker started, observe its run/session and result before retrying. Do not execute the same task twice with another model.

A missing model is therefore a compatibility fallback, not the model-selection policy. Workers that need the lead's judgment may intentionally inherit it; ordinary workers should receive an explicit, harness-native model whenever one is available.
