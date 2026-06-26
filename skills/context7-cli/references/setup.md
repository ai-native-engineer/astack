# Setup

## Authentication

Most commands work without login. Exceptions: `ctx7 skills generate` always requires it; `ctx7 setup` requires it unless `--api-key` or `--oauth` is passed. Login also unlocks higher rate limits on docs commands.

```bash
ctx7 login               # Opens browser for OAuth
ctx7 login --no-browser  # Prints URL instead of opening browser
ctx7 logout              # Clear stored tokens
ctx7 whoami              # Show current login status (name + email)
```

Set an API key via environment variable to skip interactive login entirely:

```bash
export CONTEXT7_API_KEY=your_key
```

## ctx7 setup

One-time command to configure Context7 for your AI coding agent. Prompts for mode on first run:
- **MCP server** — registers the Context7 MCP server so the agent can call tools natively
- **CLI + Skills** — installs a `find-docs` skill that guides the agent to use `ctx7` CLI commands (no MCP required)

```bash
ctx7 setup                     # Interactive — prompts for mode, then agent/install target
ctx7 setup --mcp               # Skip prompt, use MCP server mode
ctx7 setup --cli               # Skip prompt, use CLI + Skills mode

# MCP mode — target a specific agent
ctx7 setup --claude            # Claude Code only
ctx7 setup --cursor            # Cursor only
ctx7 setup --opencode          # OpenCode only

# CLI + Skills mode — target a specific install location
ctx7 setup --cli --claude      # Claude Code (~/.claude/skills)
ctx7 setup --cli --cursor      # Cursor (~/.cursor/skills)
ctx7 setup --cli --universal   # Universal (~/.agents/skills)
ctx7 setup --cli --antigravity # Antigravity (~/.config/agent/skills)

ctx7 setup --project           # Configure current project instead of globally
ctx7 setup --yes               # Skip confirmation prompts
```

**Authentication options:**
```bash
ctx7 setup --api-key YOUR_KEY  # Use an existing API key (both MCP and CLI + Skills mode)
ctx7 setup --oauth             # OAuth endpoint — MCP mode only (IDE handles the auth flow)
```

Without `--api-key` or `--oauth`, setup opens a browser for OAuth login. MCP mode additionally generates a new API key after login. `--oauth` is MCP-only.

**What gets written — MCP mode:**
- MCP server entry in the agent's config file (`.mcp.json` for Claude, `.cursor/mcp.json` for Cursor, `.opencode.json` for OpenCode)
- A Context7 rule file instructing the agent to use Context7 for library docs
- A `context7-mcp` skill in the agent's skills directory

**What gets written — CLI + Skills mode:**
- A `find-docs` skill in the chosen agent's skills directory, guiding the agent to use `ctx7 library` and `ctx7 docs` commands
