# astack

**Aiden's Stack** — a small, curated set of [Claude Code](https://docs.claude.com/en/docs/claude-code) skills I actually use every day, packaged as a plugin.

> The skills respond in Korean by default (they grew out of Korean voice/notes workflows), but the mechanics work in any language.

## Install

```text
/plugin marketplace add ai-native-engineer/astack
/plugin install astack@astack
```

Then invoke a skill with the `astack:` prefix, e.g. `astack:session-history`.

## Skills

| Skill | What it does | External deps |
|-------|--------------|---------------|
| `session-history` | Unified view & search of Claude Code (`~/.claude`) + Codex (`~/.codex`) sessions — list, timeline, full-text grep, show, token usage summary. | Python 3 |
| `voice-memos` | Apple Voice Memos / call recordings / Apple Notes / Caret MCP → transcribe, correct, search, summarize, notify. Includes a launchd watcher pipeline (auto transcribe → summarize → notify on new recordings, incl. call `.m4a`) with FDA diagnostics. | macOS, Python 3, `apple-stt`, `ffmpeg`, (optional) Caret MCP, Telegram/Discord |
| `imessage` | Read & search macOS Messages (iMessage/SMS/RCS) via readonly SQLite (decodes `attributedBody`); send via `osascript`. MCP-free, on-demand. | macOS, Python 3 (stdlib only), Full Disk Access |
| `chrome-devtools-cli` | Drive headless Chrome from the terminal via `chrome-devtools-mcp`'s standalone CLI — navigate, click/fill, screenshot, console/network inspect, JS eval, Lighthouse audit, performance trace (Core Web Vitals), heap snapshot. On-demand alternative to the MCP server. | Node.js, `chrome-devtools-mcp` (`npm i -g chrome-devtools-mcp@latest`), Chrome/Chromium |
| `meta-ads-cli` | Manage Meta (Facebook/Instagram) ads from the shell via the `meta` CLI — campaign/adset/ad/creative CRUD, performance insights (spend/CTR/CPC/ROAS, breakdowns), pixel conversion tracking, catalogs. Mental model + setup/commands/recipes references; full options delegated to `meta --help`. | PyPI `meta-ads` (`uv tool install meta-ads --python 3.13`), a Meta system-user access token |
| `crawl` | Crawl web pages & doc sites to clean markdown, fully local with no API key — single page, deep-crawl to one file, or mirror a whole doc tree to per-page files (URL path = file path). Built-in traps for locale explosion, boilerplate, and broken links. | Python 3, crawl4ai `crwl` CLI (`uv tool install crawl4ai && crawl4ai-setup`), headless browser |
| `oss-explore` | Discover-first GitHub toolkit (`gh` CLI): **find open-source projects by topic** (merged keyword+topic search, star/activity/language, with per-repo good-first-issue/help-wanted counts auto-shown), then drill into issue-level entry points (beginner-label synonyms, excludes already-PR'd/stale), browse trending ∩ contributable, bootstrap fork→clone→branch, and retrospect merged-PR contributions (org vs external OSS, star-ranked, badges) + stats (merge-rate, year/month/weekday, language). Terminal tables or dark/light HTML. Topic/language/filters are all user args — no hardcoded domain. | `gh` (authenticated), `jq` |
| `project-context-gather` | Topic-keyword sweep across your personal/collab tools (Obsidian, voice memos / call recordings / Apple Notes / Caret, Notion, Slack, Google Workspace) → one consolidated, relevance-gated context archive **per source** under `./context/`, with originals preserved in `attachments/`. Re-runs upsert into the existing per-source archive via YAML frontmatter `anchor` (incremental merge, dedup, date bump) instead of overwriting; `scripts/context_status.py` lists collection status. Subagent or main-thread modes; no web research. | `rg`, plus whichever per-source tools you use (`agent-slack`, Notion `ntn` CLI, `gog`, `voice-memos` skill, Caret MCP) |
| `html-explainer` | Single-file HTML explainers with a verified visualization stack: Mermaid v11 + ELK auto-layout diagrams (text DSL, no manual coordinates → no overlaps), Apache ECharts 6 charts (built-in dark theme, log-axis range bars via custom series), Iconify icons, auto dark/light re-render. Animations are comprehension-only (edge-flow, state toggles — no decorative fade-ins). Ships a wired template, a curated pitfall guide (license traps, dead libs, AI-hallucination patterns), and a headless render-verify script run before opening. | `chrome-devtools-cli` skill's CLI (for `verify.sh`), internet for CDNs (jsDelivr) |
| `data-go-kr` | Work-unit access to any Korean public-data API (data.go.kr): search the catalog → application guide → call, caching each successful call as a recipe (NTS business status, G2B bid/award info, …) with official reference docs preserved alongside. Calls hit the API directly with your own key — no proxy. | `DATA_GO_KR_API_KEY` (free data.go.kr account; per-API 활용신청), `curl`, Python 3 |
| `company-context-research` | Pre-outreach / diligence company research → a per-company evidence package: fragmented public-surface map (legal entity / parent / brand / B2B / careers / IR / CDN), crawl-first recursive crawl with full first-party attachment recovery, external press inventory (Naver News API + Google News RSS yearly windows with original-URL decoding; Tavily supplement), and jurisdiction-aware official data (Korean DART called directly + listing/public-data via `data-go-kr`; SEC EDGAR for US-listed). | Python 3, `crawl` skill (`crwl` CLI), `data-go-kr` skill, Naver Developers app keys (`NAVER_CLIENT_ID`/`NAVER_CLIENT_SECRET`), (optional) DART key `API_K_DART`, (optional) Tavily CLI `tvly` |

## voice-memos setup

`voice-memos` is macOS-only and needs a few extras:

- `apple-stt` (macOS SpeechAnalyzer) for transcription; `ffmpeg` for `.qta` files
- Python deps: `cd skills/voice-memos && uv sync`
- **Optional notifications**: copy `skills/voice-memos/.env.example` → `skills/voice-memos/.env` and fill in your Telegram/Discord values. Everything else works without it; only sending is skipped.
- **Optional automation**: register a launchd LaunchAgent that runs `scripts/run.sh` on new recordings — setup, log reading, and Full Disk Access diagnostics in `skills/voice-memos/references/watcher.md`.

## Notes

- Early cut (`v0.1.0`). Some `voice-memos` docs reference `~/.claude/skills/voice-memos/...` paths that assume a symlinked install; running purely as a plugin may need path tweaks for the helper scripts.
- More skills will be added after this MVP.

## License

MIT © Seungwon An (Aiden) — see [LICENSE](LICENSE).
