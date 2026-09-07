---
argument-hint: "[query]"
name: find-skills
description: 'Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express interest in extending capabilities. This skill should be used when the user is looking for functionality that might exist as an installable skill. Do NOT use for looking up API/library documentation - use context7-cli instead.'
---


# Find Skills

This skill helps you discover skills - first among the ones already installed locally, then in the open agent skills ecosystem - and route installation through the local skill policy.

## When to Use This Skill

Use this skill when the user:

- Asks "how do I do X" where X might be a common task with an existing skill
- Says "find a skill for X" or "is there a skill for X"
- Asks "can you do X" where X is a specialized capability
- Expresses interest in extending agent capabilities
- Wants to search for tools, templates, or workflows
- Mentions they wish they had help with a specific domain (design, testing, deployment, etc.)

## Step 1: Check Installed Skills First

Most requests are already covered locally. List what is installed and match by name and description before searching outside:

```bash
ls ~/.agents/skills/shared   # shared originals (Claude, Codex, Grok, Cursor)
claude plugin list           # installed plugins and the skills they carry
```

If a local skill fits, use it and stop here. Continue to external search only when nothing local matches.

## Step 2: Search the Skills Ecosystem

The Skills CLI (`bunx skills`) searches the open agent skills ecosystem. Browse the same catalog at https://skills.sh/.

```bash
bunx skills find [query]
```

For example:

- User asks "how do I make my React app faster?" -> `bunx skills find react performance`
- User asks "can you help me with PR reviews?" -> `bunx skills find pr review`
- User asks "I need to create a changelog" -> `bunx skills find changelog`

The command returns matching skills with their source (`owner/repo@skill`) and a skills.sh link. Identify the domain and the specific task first so the query is specific ("react testing" beats "testing"); try alternative terms ("deployment", "ci-cd") when the first query misses.

## Step 3: Present Options to the User

When you find relevant skills, present them with:

1. The skill name and what it does
2. The source repository (`owner/repo@skill`)
3. A link to learn more at skills.sh

Example response:

```
I found a skill that might help! The "vercel-react-best-practices" skill provides
React and Next.js performance optimization guidelines from Vercel Engineering.

Source: vercel-labs/agent-skills@vercel-react-best-practices
Learn more: https://skills.sh/vercel-labs/agent-skills/vercel-react-best-practices

Want me to install it?
```

## Step 4: Install Through the Local Policy

External skills are installed as plugins, never copied into `~/.claude/skills/` by hand - the plugin structure is what gives a skill its source prefix (`name:skill`) and lets it be removed as a unit.

1. If the source publishes a Claude Code plugin or marketplace, run `claude plugin install <plugin>` after the user approves.
2. Otherwise hand the repository to the `skill-manager` skill: it reviews the external code with `references/security-review.md` and installs the reviewed copy with `install-skill.sh`.
3. Do not run `bunx skills add`; it writes straight into agent skill directories and bypasses both steps above.

## Common Skill Categories

When searching, consider these common categories:

| Category        | Example Queries                          |
| --------------- | ---------------------------------------- |
| Web Development | react, nextjs, typescript, css, tailwind |
| Testing         | testing, jest, playwright, e2e           |
| DevOps          | deploy, docker, kubernetes, ci-cd        |
| Documentation   | docs, readme, changelog, api-docs        |
| Code Quality    | review, lint, refactor, best-practices   |
| Design          | ui, ux, design-system, accessibility     |
| Productivity    | workflow, automation, git                |

## When No Skills Are Found

If no relevant skill exists locally or in the ecosystem:

1. Acknowledge that no existing skill was found
2. Offer to help with the task directly using your general capabilities
3. If the task recurs, create a skill with the `skill-manager` skill (create mode) instead of an external scaffold

Example:

```
I searched the installed skills and skills.sh for "xyz" but didn't find a match.
I can still help you with this task directly! Would you like me to proceed?

If this is something you do often, I can capture it as a skill with skill-manager.
```
