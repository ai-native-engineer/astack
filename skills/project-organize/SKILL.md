---
argument-hint: "[project-root]"
name: project-organize
description: "Organizes a project workspace by identifying current truth, stale drafts, legacy outputs, archive or backup candidates, AGENTS.md drift, and context README drift. Use when user asks 프로젝트 정리, 레거시 확인, 정본 찾기, stale 파일, cleanup candidates, AGENTS.md 인덱스 정리, context README 갱신, or project-organize. Do NOT use for collecting new context from external tools; use project-collect."
---

# Project Organize

Keep a project folder readable by separating current truth from old drafts, backups, stale outputs, and index drift. This skill does not collect new context from external tools.

## When To Use

- The user asks whether a project has legacy, stale, duplicate, or confusing files.
- The user asks to find the current source of truth for a project.
- The user asks to update `AGENTS.md`, `README.md`, or `context/README.md` indexes after a project changed.
- The user asks for cleanup candidates, archive candidates, or a project hygiene pass.

Use `project-collect` instead when the job is to gather new context from Slack, Notion, Google Workspace, Obsidian, voice notes, recordings, or other sources.

## Workflow

1. **Select the root**
   - Use the provided path if the user gave one.
   - Otherwise use the current working directory.
   - Confirm the real path with `pwd` and, if relevant, `git rev-parse --show-toplevel`.

2. **Read project instructions first**
   - Read `AGENTS.md` if present.
   - Then read `README.md`, `context/README.md`, or `01-context/README.md` if present.
   - Treat these as indexes, not proof. Verify important claims against files.

3. **Build a truth map**
   - Identify the current canonical materials, source-of-truth pages, output files, and transcript/source paths.
   - Mark explicit supersession notes such as "stale", "backup", "do not revert", "Notion is truth", or "local is truth".
   - Check recent file timestamps and content headers, but do not trust filenames alone.

4. **Classify project files**
   - `current`: directly used or named as the current truth.
   - `reference/archive`: old but intentionally retained for provenance.
   - `stale-risk`: likely superseded and dangerous to reuse.
   - `cleanup-candidate`: empty, duplicate, temporary, or confirmed junk.
   - `unknown`: unclear without user decision.

5. **Check index drift**
   - Compare `AGENTS.md` and context README indexes against actual files.
   - Flag missing current files, stale "current" claims, misleading names, and unindexed transcripts or source materials.
   - If asked to edit, keep indexes short and factual. Put long chronology in logs, not the working index.

6. **Propose before changing**
   - First tell the user, briefly, how you will organize the project.
   - Include the intended moves, deletes, index edits, and commit scope.
   - Stop and wait for explicit approval before moving, deleting, editing indexes, or committing.

7. **Act conservatively after approval**
   - Do not delete files without explicit user approval.
   - Prefer a review list, archive move, or note before deletion.
   - Preserve attachments, source exports, and backups unless they are confirmed junk.
   - If external systems such as Notion are involved, state whether the check is local-only or live-verified.
   - In a git repo, commit the approved cleanup after verification.
   - Stage only approved/touched paths. Leave unrelated dirty worktree changes out of the commit and mention them.
   - If there are no file changes after approval, skip the commit and say why.

## Output Format

Use this shape unless the user asks for a different format:

```markdown
## Current Truth
- <path or source> — <why it is current>

## Stale Risks
- <path> — <why reuse is risky>

## Cleanup Candidates
- <path> — <evidence and suggested action>

## Index Drift
- <file> — <missing or misleading entry>

## Proposed Actions
- <move/delete/edit/commit scope>

## Actions Taken
- <edit or move performed>

## Needs Decision
- <question or candidate requiring user approval>
```

For small tasks, collapse empty sections instead of padding the answer.
