# Select references from demonstrated use

## Evidence before preference

Use the artifact named in the request first. For previous favorites, use `session-history` to find its filename, topic, and surrounding feedback. Read the original user message and the artifact. Compaction summaries and assistant praise do not establish approval.

The optional local catalog is `~/.agents/artifacts/html-page-reference-catalog.json`. Read it when present. Records contain the original source path, purpose, useful interactions, feedback scope, and session pointer. Verify that a source still exists before selecting it. Private IDs and paths belong in this local catalog, not distributed instructions.

Distinguish evidence scopes:

- **Explicit design preference:** the user chose or praised the page's presentation or interaction.
- **Positive reaction in context:** praise follows the page but also concerns the project. Reuse the successful explanation pattern without claiming approval of every visual choice.
- **Used successfully:** the user completed selections or returned the response. This supports the interaction, not a preferred palette.
- **Stored example:** useful material without recovered preference evidence.
- **Correction requested:** retain the failure and requested change for comparison; check the corrected result before promoting it.

If evidence is limited, say so and continue with the best-supported example. Ask for another remembered topic only when it would change selection.

## Match the job

| Need | Pattern | Preserve |
|---|---|---|
| Understand how a real result was produced | Overview plus step explorer | One concrete case, input files, actual command, output, result image, and where edits restart the process |
| Understand state changes | Interactive lab | Before/after state, manipulable input, explanation tied to each action |
| Find a file, setting, or concept | Tree/search plus detail pane | Stable selection, linked sections, readable detail without repeated backtracking |
| Choose media or alternatives | Evidence-led sheet | Real media, item IDs, choices, notes, preview, and response destination |

Retained examples: [context lab](../examples/chat-context-composition-lab.html), [context timeline](../examples/claude-code-context-timeline.html), [directory explorer](../examples/claude-directory-explorer.html). Inspect the relevant example, not all three every time. Their presence alone does not prove user approval.

## Adaptation

Preserve the structural reason an example worked. A pipeline explanation follows a real case through inputs and outputs; it does not force every topic into the same cards or colors. A directory explorer keeps navigation beside detail; it need not become a slide deck.

Replace data and controls together. Verify paths, media, code, dates, and response destination. Keep the previous file when making a comparison. Upstream starters under `assets/` remain fallbacks beneath demonstrated user preferences.
