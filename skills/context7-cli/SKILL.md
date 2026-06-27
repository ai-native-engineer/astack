---
argument-hint: "[command]"
name: context7-cli
description: "Context7/ctx7 CLI for up-to-date library documentation, API references, and code examples for any library, framework, SDK, CLI tool, or cloud service, plus finding, installing, and generating AI coding skills via Context7. Triggers: API syntax, configuration options, version migration, 'how do I' questions naming a library, library-specific debugging, setup instructions, CLI usage - even well-known ones like React, Next.js, Prisma, Express, Tailwind, Django, Spring Boot; or user mentions ctx7/context7. Prefer this over training memory for API details, signatures, and config options, which are frequently outdated. Do NOT use for general web search, local repo grep, non-library research, discovering Claude agent skills (use find-skills), or code changes that do not need external docs."
---

# ctx7 CLI

The Context7 CLI does two things: fetches up-to-date library documentation and manages AI coding skills.

Use this even when you think you know the answer — training data for API details, signatures, and configuration options is frequently outdated. Verify against current docs, and prefer this over web search for library documentation.

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
- **[Setup](references/setup.md)** — Authentication (login for higher rate limits) and CLI skill install.

## Quick Reference

The core workflow is the two-step docs lookup:

```bash
ctx7 library <name> <query>     # Step 1: resolve library ID (e.g. /facebook/react)
ctx7 docs <libraryId> <query>  # Step 2: fetch docs with that ID
```

- Full docs flags, query-writing, version IDs → [references/docs.md](references/docs.md)
- Skills commands (install/search/suggest/list/remove/generate) → [references/skills.md](references/skills.md)
- Authentication (login/logout/whoami, API key) + CLI skill install → [references/setup.md](references/setup.md)

Run `ctx7 <command> --help` for the authoritative, installed-version flags.

## Common Mistakes

- Library IDs require a `/` prefix — `/facebook/react` not `facebook/react`
- Always run `ctx7 library` first — `ctx7 docs react "hooks"` will fail without a valid ID
- Repository format for skills is `/owner/repo` — e.g., `ctx7 skills install /anthropics/skills`
- `skills generate` requires login — run `ctx7 login` first
