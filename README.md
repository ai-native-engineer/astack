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
| `session-history` | Unified view & search of Claude Code (`~/.claude`) + Codex (`~/.codex`) sessions — list, timeline, full-text search across messages and tool calls (`rg`/`grep`, `--limit`), show, token usage summary. | Python 3 |
| `voice-memos` | Apple Voice Memos / call recordings / Apple Notes / Caret MCP → transcribe, correct, search, summarize, notify. Includes a launchd watcher pipeline (auto transcribe → summarize → notify on new recordings, incl. call `.m4a`) with FDA diagnostics. | macOS, Python 3, `apple-stt`, `ffmpeg`, (optional) `stt` skill for speaker diarization, (optional) Caret MCP, Telegram/Discord |
| `imessage` | Read & search macOS Messages (iMessage/SMS/RCS) via readonly SQLite (decodes `attributedBody`); send via `osascript`. MCP-free, on-demand. | macOS, Python 3 (stdlib only), Full Disk Access |
| `chrome-devtools-cli` | Drive headless Chrome from the terminal via `chrome-devtools-mcp`'s standalone CLI — navigate, click/fill, screenshot, console/network inspect, JS eval, Lighthouse audit, performance trace (Core Web Vitals), heap snapshot. On-demand alternative to the MCP server. | Node.js, `chrome-devtools-mcp` (`npm i -g chrome-devtools-mcp@latest`), Chrome/Chromium |
| `meta-ads-cli` | Manage Meta (Facebook/Instagram) ads from the shell via the `meta` CLI — campaign/adset/ad/creative CRUD, performance insights (spend/CTR/CPC/ROAS, breakdowns), pixel conversion tracking, catalogs. Mental model + setup/commands/recipes references; full options delegated to `meta --help`. | PyPI `meta-ads` (`uv tool install meta-ads --python 3.13`), a Meta system-user access token |
| `crawl` | Crawl web pages & doc sites to clean markdown, fully local with no API key — single page, deep-crawl to one file, or mirror a whole doc tree to per-page files (URL path = file path) with optional image download (`--assets`). Built-in traps for locale explosion, boilerplate, broken links, and discovery-vs-extraction selector scoping (`target_elements`, not `css_selector`); bundled crawl4ai API reference for custom scripts (bot-evasion, dynamic/infinite-scroll, Shadow DOM, capture/download). | Python 3, crawl4ai `crwl` CLI (`uv tool install crawl4ai && crawl4ai-setup`), headless browser |
| `oss-explore` | Discover-first GitHub toolkit (`gh` CLI): **find open-source projects by topic** (merged keyword+topic search, star/activity/language, with per-repo good-first-issue/help-wanted counts auto-shown), then drill into issue-level entry points (beginner-label synonyms, excludes already-PR'd/stale), browse trending ∩ contributable, bootstrap fork→clone→branch, and retrospect merged-PR contributions (org vs external OSS, star-ranked, badges) + stats (merge-rate, year/month/weekday, language). Terminal tables or dark/light HTML. Topic/language/filters are all user args — no hardcoded domain. | `gh` (authenticated), `jq` |
| `project-context-gather` | Topic-keyword sweep across your personal/collab tools (Obsidian, voice memos / call recordings / Apple Notes / Caret, Notion, Slack, Google Workspace) → one consolidated, relevance-gated context archive **per source** under `./context/`, with originals preserved in `attachments/`. Re-runs upsert into the existing per-source archive via YAML frontmatter `anchor` (incremental merge, dedup, date bump) instead of overwriting; `scripts/context_status.py` lists collection status. Subagent or main-thread modes; no web research. | `rg`, plus whichever per-source tools you use (`agent-slack`, Notion `ntn` CLI, `gog`, `voice-memos` skill, Caret MCP) |
| `html-explainer` | Single-file HTML explainers with a verified visualization stack: Mermaid v11 + ELK auto-layout diagrams (text DSL, no manual coordinates → no overlaps), Apache ECharts 6 charts (built-in dark theme, log-axis range bars via custom series), Iconify icons, auto dark/light re-render. Animations are comprehension-only (edge-flow, state toggles — no decorative fade-ins). Ships a wired template, a curated pitfall guide (license traps, dead libs, AI-hallucination patterns), and a headless render-verify script run before opening. | `chrome-devtools-cli` skill's CLI (for `verify.sh`), internet for CDNs (jsDelivr) |
| `data-go-kr` | Work-unit access to any Korean public-data API (data.go.kr): search the catalog → application guide → call, caching each successful call as a recipe (NTS business status, G2B bid/award info, …) with official reference docs preserved alongside. Calls hit the API directly with your own key — no proxy. | `DATA_GO_KR_API_KEY` (free data.go.kr account; per-API 활용신청), `curl`, Python 3 |
| `company-context-research` | Pre-outreach / diligence company research → a per-company evidence package: fragmented public-surface map (legal entity / parent / brand / B2B / careers / IR / CDN), crawl-first recursive crawl with full first-party attachment recovery, external press inventory (Naver News API + Google News RSS yearly windows with original-URL decoding; Tavily supplement), and jurisdiction-aware official data (Korean DART called directly + listing/public-data via `data-go-kr`; SEC EDGAR for US-listed). | Python 3, `crawl` skill (`crwl` CLI), `data-go-kr` skill, Naver Developers app keys (`NAVER_CLIENT_ID`/`NAVER_CLIENT_SECRET`), (optional) DART key `API_K_DART`, (optional) Tavily CLI `tvly` |
| `tts` | Local text-to-speech & voice cloning (Qwen3-TTS via mlx-audio, fully offline) — register a reference voice once from any audio clip, then synthesize long narration in `full` (one-pass) or `chunk` (per-sentence, individually regenerable) mode with tail-fade/pad, end-cutoff `audit`+`regen`, and a loudness-normalized edit track for video. macOS `say` fallback for quick non-cloned speech. | macOS (Apple Silicon), `mlx-audio` (`uv tool install mlx-audio`), `huggingface_hub` (`hf`, model weights), `ffmpeg` |
| `stt` | Local speech-to-text + optional speaker diarization — transcribe audio/video (full or time-range) with macOS `apple-stt` (Vision, fast) or `argmax-cli` (WhisperKit), then build speaker-labeled transcripts by aligning text with a diarization timeline. Optional OpenAI/ElevenLabs cloud for sensitive-free audio. | macOS (`apple-stt` 26+ Vision binary on PATH), `ffmpeg`, (optional) `argmax-cli` (argmax-oss-swift), (optional) OpenAI/ElevenLabs API keys |
| `podcast` | End-to-end podcast production & publishing orchestrator: a news recap (or any script) becomes a spoken-style script (with a show-notes convention), then AI voice (`tts`), then a free public RSS feed via GitHub Releases + Pages (Spotify/Apple auto-pull). Bundles the publish scripts (`publish.sh`, `gen_feed.py`), title/show-notes conventions, loudness-normalized output, and a publish-only mode for existing mp3s. | `gh` (authenticated), `ffprobe`, Python 3, `tts` skill (for voice) |
| `ffmpeg` | Local `ffmpeg`/`ffprobe` (+ macOS `sips`) media operations — cut/join/compress/convert, extract tracks, resize, FPS, rotate, GIFs, subtitles, thumbnails, audio normalization, HDR-to-SDR, HEIC. Stream-copy vs re-encode decision model plus a recipe guide for the tricky cuts/joins. | `ffmpeg`/`ffprobe` (macOS `sips` for HEIC) |
| `ocr` | Local OCR for images and scanned PDFs via macOS Vision (`ocrmypdf` + AppleOCR plugin) — fully on-device, no cloud upload. | macOS, `ocrmypdf` (`uv tool install ocrmypdf --with ocrmypdf-appleocr`) |
| `similarweb` | SimilarWeb free-endpoint domain analytics — traffic, rank, visitor estimates, traffic sources, AI/LLM referrals, SEO keyword value, competitor comparison. No API key. | Python 3 / `uv` (auto-installs `requests`) |
| `humanize-korean` | Detect and rewrite AI-ish Korean — translationese, mechanical parallelism, passive overuse, citation clutter, uniform rhythm — while preserving meaning. 40+ tell-patterns with a scholarship reference. | none (prompt/reference skill) |
| `find-skills` | Discover and install agent skills from the open skills ecosystem via the Skills CLI. | Node.js, `skills` CLI (`npx skills`) |
| `context7-cli` | Context7 `ctx7` CLI — fetch up-to-date library/framework/SDK docs and code examples on demand, plus find/install/generate AI coding skills. | Node.js, `ctx7` (`npm i -g ctx7@latest`) |
| `kakaotalk` | macOS KakaoTalk read/search/send via the Accessibility API (atomacos) — list/search chatrooms, read history, send messages, all without stealing the mouse cursor (keyboard + AX actions only). Self-contained minimal message contract before sending. | macOS, KakaoTalk app, Python 3 (`atomacos`) |
| `goal-plan` | Durable `/goal` harness for long-running agent work: GOAL.md instructions plus a `progress.tsv` scoreboard (edited only via `goal_log.py`), scaffolded into a git worktree so the main tree stays free and each loop step is a resumable commit. Vendor-neutral core with per-runtime notes for Claude Code and Codex. | git, Python 3 (stdlib only) |

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
