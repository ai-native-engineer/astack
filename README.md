# astack

**Aiden's Stack** — a small, curated set of skills for [Claude Code](https://docs.claude.com/en/docs/claude-code) and Codex, packaged as a plugin.

> The skills respond in Korean by default (they grew out of Korean voice/notes workflows), but the mechanics work in any language.

## Install

### Claude Code

```text
/plugin marketplace add ai-native-engineer/astack
/plugin install astack@astack
```

### Codex

```bash
codex plugin marketplace add ai-native-engineer/astack
codex plugin add astack@astack
```

Then invoke a skill with the `astack:` prefix, e.g. `astack:session-history`.

## Skills

| Skill | What it does | External deps |
|-------|--------------|---------------|
| `agent-team` | Coordinate independent work across Claude Code, Codex, or persistent Zellij panes with a strong lead and reliable completion signaling. | None; optional Zellij and worker CLIs for cross-harness panes |
| `session-history` | Unified view & search of Claude Code (`~/.claude`) + Codex (`~/.codex`) sessions — list, timeline, full-text search across messages and tool calls (`rg`/`grep`, `--limit`), show, token usage summary. | Python 3 |
| `voice-memos` | Apple Voice Memos / call recordings / Apple Notes / Caret MCP → transcribe, correct, search, summarize, notify. Includes a launchd watcher pipeline (auto transcribe → summarize → notify on new recordings, incl. call `.m4a`) with FDA diagnostics. | macOS, Python 3, `apple-stt`, `ffmpeg`, (optional) `stt` skill for speaker diarization, (optional) Caret MCP, Telegram/Discord |
| `imessage` | Read & search macOS Messages (iMessage/SMS/RCS) via readonly SQLite (decodes `attributedBody`); send via `osascript`. MCP-free, on-demand. | macOS, Python 3 (stdlib only), Full Disk Access |
| `chrome-devtools-cli` | Drive headless Chrome from the terminal via `chrome-devtools-mcp`'s standalone CLI — navigate, click/fill, screenshot, console/network inspect, JS eval, Lighthouse audit, performance trace (Core Web Vitals), heap snapshot. On-demand alternative to the MCP server. | Node.js, `chrome-devtools-mcp` (`npm i -g chrome-devtools-mcp@latest`), Chrome/Chromium |
| `meta-ads-cli` | Manage Meta (Facebook/Instagram) ads from the shell via the `meta` CLI — campaign/adset/ad/creative CRUD, performance insights (spend/CTR/CPC/ROAS, breakdowns), pixel conversion tracking, catalogs. Mental model + setup/commands/recipes references; full options delegated to `meta --help`. | PyPI `meta-ads` (`uv tool install meta-ads --python 3.13`), a Meta system-user access token |
| `crawl` | Crawl web pages & doc sites to clean markdown, fully local with no API key — single page, deep-crawl to one file, or mirror a whole doc tree to per-page files (URL path = file path) with optional image download (`--assets`). Built-in traps for locale explosion, boilerplate, broken links, and discovery-vs-extraction selector scoping (`target_elements`, not `css_selector`); bundled crawl4ai API reference for custom scripts (bot-evasion, dynamic/infinite-scroll, Shadow DOM, capture/download). | Python 3, crawl4ai `crwl` CLI (`uv tool install crawl4ai && crawl4ai-setup`), headless browser |
| `oss-explore` | Discover-first GitHub toolkit (`gh` CLI): **find open-source projects by topic** (merged keyword+topic search, star/activity/language, with per-repo good-first-issue/help-wanted counts auto-shown), then drill into issue-level entry points (beginner-label synonyms, excludes already-PR'd/stale), browse trending ∩ contributable, bootstrap fork→clone→branch, and retrospect merged-PR contributions (org vs external OSS, star-ranked, badges) + stats (merge-rate, year/month/weekday, language). Terminal tables or dark/light HTML. Topic/language/filters are all user args — no hardcoded domain. | `gh` (authenticated), `jq` |
| `project-collect` | Collect relevant project context from local and collaboration sources into per-source archives under `01-context/company/` (or a legacy `context/` tree), preserving attachments and incrementally merging reruns. | `rg`, plus whichever source tools you use: Slack, Notion `ntn`, `gog`, Obsidian, voice notes/recordings |
| `html-explainer` | Single-file HTML explainers in two types, chosen up front: **visual** (static, at-a-glance) builds on a verified stack — Mermaid v11 + ELK auto-layout diagrams (text DSL, no manual coordinates → no overlaps), Apache ECharts 6 (built-in dark theme), Iconify icons; **interactive** (learner-driven walkthrough) is a build-less React 18 + Babel single file with click-through steps, a state machine, keyboard nav, and per-step demos. Both auto dark/light, animations comprehension-only (no decorative fade-ins). Ships a wired template per type, two completed interactive examples, curated pitfall guides (license traps, dead libs, AI-hallucination patterns; interactive-specific gotchas), and a headless render-verify script run before opening. | `chrome-devtools-cli` skill's CLI (for `verify.sh`), internet for CDNs (jsDelivr/unpkg) |
| `data-go-kr` | Work-unit access to any Korean public-data API (data.go.kr): search the catalog → application guide → call, caching each successful call as a recipe (NTS business status, G2B bid/award info, …) with official reference docs preserved alongside. Calls hit the API directly with your own key — no proxy. | `DATA_GO_KR_API_KEY` (free data.go.kr account; per-API 활용신청), `curl`, Python 3 |
| `company-context-research` | Pre-outreach / diligence company research → a per-company evidence package with public-surface mapping, recursive crawl and attachments, press inventory, normalized official data, canonical JSON, and a validated local HTML viewer. | Python 3, `crawl` and `data-go-kr` skills, Naver Developers app keys, (optional) `open-api`, DART key, Tavily CLI |
| `communication` | Shared work-message contract and channel-specific writing overlays used by transport skills. | None |
| `tts` | Local text-to-speech & voice cloning (Qwen3-TTS via mlx-audio; offline after model download) — keeps personal voice references in a local data directory outside the plugin and supports `full`/`chunk` generation, partial regeneration, cutoff audit, and edit-ready loudness normalization. | macOS (Apple Silicon), `mlx-audio`, `ffmpeg`, (optional) `apple-stt` for automatic reference transcription |
| `stt` | Local speech-to-text + optional speaker diarization — transcribe audio/video (full or time-range) with macOS `apple-stt` (Vision, fast) or `argmax-cli` (WhisperKit), then build speaker-labeled transcripts by aligning text with a diarization timeline. Optional OpenAI/ElevenLabs cloud for sensitive-free audio. | macOS (`apple-stt` 26+ Vision binary on PATH), `ffmpeg`, (optional) `argmax-cli` (argmax-oss-swift), (optional) OpenAI/ElevenLabs API keys |
| `podcast` | Draft, render, or explicitly publish a podcast episode from a news recap or script. Includes spoken-script and show-notes conventions, TTS routing, Apple/Spotify-compatible HTML show notes, validated RSS date ordering, dry-run preflight, and GitHub Releases + Pages publishing. | `gh` (authenticated), `ffmpeg`/`ffprobe`, Python 3, `tts` skill (for voice) |
| `ffmpeg` | Standalone `ffmpeg`/`ffprobe` (+ macOS `sips`) operations — explicit cuts/joins, compress/convert, extract tracks, resize, FPS, rotate, GIFs, subtitles, thumbnails, normalization, HDR-to-SDR, and HEIC. | `ffmpeg`/`ffprobe` (macOS `sips` for HEIC) |
| `video-cut-editor` | Evidence-driven video cleanup for silence removal, retake markers, VAD/STT-assisted cut plans, one-pass rendering from the original timeline, and waveform/decode QA. | Python 3, `ffmpeg`/`ffprobe`; optional STT/VAD tools |
| `ocr` | Local OCR for images and scanned PDFs via macOS Vision, plus table extraction to Markdown/HTML/CSV — fully on-device, no cloud upload. | macOS, `ocrmypdf` + AppleOCR plugin; `uv` for table extraction dependencies |
| `similarweb` | SimilarWeb free-endpoint domain analytics — traffic, rank, visitor estimates, traffic sources, AI/LLM referrals, SEO keyword value, competitor comparison. No API key. | Python 3 / `uv` (auto-installs `requests`) |
| `humanize-korean` | Detect and rewrite AI-ish Korean — translationese, mechanical parallelism, passive overuse, citation clutter, uniform rhythm — while preserving meaning. 40+ tell-patterns with a scholarship reference. | none (prompt/reference skill) |
| `find-skills` | Discover and install agent skills from the open skills ecosystem via the Skills CLI. | Node.js, `skills` CLI (`npx skills`) |
| `context7-cli` | Context7 `ctx7` CLI — fetch up-to-date library/framework/SDK docs and code examples on demand, plus find/install/generate AI coding skills. | Node.js, `ctx7` (`npm i -g ctx7@latest`) |
| `kakaotalk` | macOS KakaoTalk read/search/send via the Accessibility API (atomacos) — list/search chatrooms, read history, send messages, all without stealing the mouse cursor (keyboard + AX actions only). Self-contained minimal message contract before sending. | macOS, KakaoTalk app, Python 3 (`atomacos`) |
| `goal-plan` | Durable `/goal` harness for long-running agent work: `AGENTS.md` instructions plus a `progress.tsv` scoreboard, scaffolded into an external worktree or dedicated goal repo so every loop step is resumable through git. | git, Python 3 (stdlib only) |
| `project-organize` | Audit a project workspace for current truth, stale drafts, legacy outputs, cleanup/archive candidates, and AGENTS/README index drift; proposes changes before acting. | `rg`, git (optional) |

## voice-memos setup

`voice-memos` is macOS-only and needs a few extras:

- `apple-stt` (macOS SpeechAnalyzer) for transcription; `ffmpeg` for `.qta` files
- Python deps: `cd skills/voice-memos && uv sync`
- **Optional notifications**: place Telegram/Discord values in `~/.config/voice-memos/.env` (or set `VOICE_MEMOS_CONFIG_FILE`). Everything else works without it; only sending is skipped.
- **Optional automation**: register a launchd LaunchAgent that runs `scripts/run.sh` on new recordings — setup, log reading, and Full Disk Access diagnostics in `skills/voice-memos/references/watcher.md`.

## Maintainer

The source of truth is `~/.agents/skills/shared/`. This repository's `skills/` directory is generated; do not edit it directly. Run `scripts/sync.sh` after validating the shared skills, then validate both plugin manifests before committing.

## Test

```bash
python3 tests/test_repository.py
claude plugin validate .claude-plugin/plugin.json --strict
claude plugin validate .claude-plugin/marketplace.json --strict
```

## License

MIT © Seungwon An (Aiden) — see [LICENSE](LICENSE).
