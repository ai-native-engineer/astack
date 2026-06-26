---
argument-hint: "[command]"
name: context7-cli
description: "Context7/ctx7 CLI workflow for fetching current library docs, finding/installing/generating AI coding skills, and configuring Context7 MCP. Use when user mentions ctx7/context7, needs up-to-date library documentation for coding, wants skill discovery via Context7, or needs Context7 MCP setup. Do NOT use for general web search, local repo grep, non-library research, or code changes that do not need external docs."
---

# ctx7 CLI

The Context7 CLI does three things: fetches up-to-date library documentation, manages AI coding skills, and sets up Context7 MCP for your editor.

Make sure the CLI is up to date before running commands:

```bash
npm install -g ctx7@latest
```

Or run directly without installing:

```bash
npx ctx7@latest <command>
```

## What this skill covers

- **[Documentation](references/docs.md)** — Fetch current docs for any library. Use when writing code, verifying API signatures, or when training data may be outdated.
- **[Skills management](references/skills.md)** — Install, search, suggest, list, remove, and generate AI coding skills.
- **[Setup](references/setup.md)** — Configure Context7 MCP for Claude Code / Cursor / OpenCode.

## Quick Reference

The core workflow is the two-step docs lookup:

```bash
ctx7 library <name> <query>     # Step 1: resolve library ID (e.g. /facebook/react)
ctx7 docs <libraryId> <query>  # Step 2: fetch docs with that ID
```

- Full docs flags, query-writing, version IDs → [references/docs.md](references/docs.md)
- Skills commands (install/search/suggest/list/remove/generate) → [references/skills.md](references/skills.md)
- MCP setup + authentication (login/logout/whoami, API key) → [references/setup.md](references/setup.md)

Run `ctx7 <command> --help` for the authoritative, installed-version flags.

## Common Mistakes

- Library IDs require a `/` prefix — `/facebook/react` not `facebook/react`
- Always run `ctx7 library` first — `ctx7 docs react "hooks"` will fail without a valid ID
- Repository format for skills is `/owner/repo` — e.g., `ctx7 skills install /anthropics/skills`
- `skills generate` requires login — run `ctx7 login` first
