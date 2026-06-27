# Setup

## Authentication

Most commands work without login. Exceptions: `ctx7 skills generate` always requires it; `ctx7 setup --cli` requires it unless `--api-key` is passed. Login also unlocks higher rate limits on docs commands.

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

## ctx7 setup --cli (install the skill)

One-time command that installs the upstream Context7 docs skill into an agent's skills directory, guiding it to use `ctx7 library` and `ctx7 docs`. Already installed here — only needed to set up a new agent/location.

```bash
ctx7 setup --cli               # Interactive — prompts for install target
ctx7 setup --cli --claude      # Claude Code (~/.claude/skills)
ctx7 setup --cli --cursor      # Cursor (~/.cursor/skills)
ctx7 setup --cli --universal   # Universal (~/.agents/skills)
ctx7 setup --cli --antigravity # Antigravity (~/.config/agent/skills)

ctx7 setup --cli --project     # Configure current project instead of globally
ctx7 setup --cli --api-key KEY # Use an existing API key instead of OAuth
ctx7 setup --cli --yes         # Skip confirmation prompts
```
