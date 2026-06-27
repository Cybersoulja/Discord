# CLAUDE.md

Guidance for Claude Code (and other AI assistants) working in this repository.

## Project Overview

This repo (`Discord`) is a small Python automation hub that bridges **Discord**,
**Telegram** (bot `@opxero`), the iOS **Drafts** app, **Pushcut**, and **Taskade**
into one process. It is a single long-running asyncio service, not a web app or
library — there is no package structure, build step, or test suite.

Core capabilities:
- Bi-directional message bridging between a Discord channel and a Telegram chat.
- A Telegram command interface (`/hawk`, `/taskade`, `/notify`, `/status`, `/chatid`) for
  triggering automations from mobile.
- An outbound Discord "Hawk" webhook client that posts plain messages/embeds to a
  `#taskade` channel.
- A Pushcut client that updates a widget (`taskade-agent`) and fires notifications.
- An inbound HTTP server (`aiohttp`) that accepts webhook payloads from iOS Shortcuts,
  Drafts actions, and other external automations, fanning them out to Discord/Telegram/Pushcut.

## Architecture

```
bot.py              Entry point. Loads .env, wires every module together, runs
                     the Discord client, Telegram polling, and the aiohttp
                     webhook server concurrently inside one asyncio event loop.
bridge.py           Bridge class — holds shared state (discord_client,
                     telegram_bot, configured channel/chat IDs) and the two
                     forward_to_* methods that move messages between platforms.
telegram_bot.py      TelegramBot class — builds the python-telegram-bot
                     Application, registers /start /status /chatid /hawk
                     /taskade /notify commands plus a catch-all text handler
                     that forwards to Discord via the bridge.
webhook.py           DiscordWebhook class — thin aiohttp client around a
                     Discord incoming webhook URL ("Hawk"). send(), plus
                     higher-level send_draft() and send_taskade_update()
                     helpers that build embeds.
pushcut_client.py    PushcutClient class — aiohttp client for the Pushcut API
                     (PUT widget inputs, POST notifications).
webhook_server.py    WebhookServer class — aiohttp.web app exposing
                     POST /webhook/drafts, POST /webhook/taskade,
                     POST /webhook/notify, GET /health. Each handler fans the
                     payload out to whichever of discord_webhook / pushcut /
                     bridge.telegram_bot are configured.
```

Everything is wired together in `bot.py:main()`:
1. Build `Bridge` with optional `DISCORD_CHANNEL_ID` / `TELEGRAM_CHAT_ID`.
2. Conditionally construct `DiscordWebhook` and `PushcutClient` only if their
   API keys/URLs are set in the environment (both are `None` otherwise).
3. Build `TelegramBot`, then the Discord `discord.Client` subclass, then
   `WebhookServer`, registering each with the shared `Bridge`.
4. Start the webhook server, start Telegram polling, then run the Discord
   client (`await discord_client.start(...)`) as the loop's main blocking call.
5. On shutdown (loop exit), stop the Telegram app and clean up the aiohttp
   runner in a `finally` block.

### Optional-integration pattern

`discord_webhook` and `pushcut` are **both optional** and are `None` when their
env vars aren't set. Every call site checks `if self.discord_webhook:` /
`if self.pushcut:` before using them — follow this pattern for any new
integration rather than assuming it's configured. `DISCORD_BOT_TOKEN` and
`TELEGRAM_BOT_TOKEN` are the only two genuinely required variables; `main()`
logs an error and returns early if either is missing.

### Bridge guard clauses

`Bridge.forward_to_discord` / `forward_to_telegram` both:
- No-op with a warning log if the destination client isn't ready/available.
- No-op (silently, by design) if the configured channel/chat ID doesn't match
  the incoming message's origin — this is how the bridge restricts itself to
  one Discord channel <-> one Telegram chat pair.
- No-op with a warning if the destination channel/chat ID was never configured.

Preserve this id-filtering behavior when touching bridge logic; it's what
prevents the bot from echoing messages into/from unintended channels.

## Running Locally

```bash
pip install -r requirements.txt
cp .env.example .env   # then fill in tokens
python bot.py
```

Required env vars: `DISCORD_BOT_TOKEN`, `TELEGRAM_BOT_TOKEN`.
Optional env vars (enable bridging/integrations when set): `DISCORD_CHANNEL_ID`,
`TELEGRAM_CHAT_ID`, `DISCORD_WEBHOOK_URL`, `PUSHCUT_API_KEY`, `PUSHCUT_WIDGET_ID`
(default `taskade-agent`), `WEBHOOK_SERVER_PORT` (default `8080`).

There is no test suite, linter config, or type-checker config in this repo —
there's nothing to run beyond `python bot.py` to sanity-check changes. Manually
exercise changes via the Telegram commands or `curl` against the webhook
endpoints (see `GETTING_STARTED.md` for example payloads) before considering
a change done.

## Conventions

- **Async everywhere.** All I/O (Discord, Telegram, aiohttp HTTP calls) is
  `async`/`await`. New integrations should follow the existing client pattern:
  a small class wrapping `aiohttp.ClientSession()` per-request (see
  `pushcut_client.py` / `webhook.py`), not a shared/global session.
  No threads.
  - Note: `aiohttp.ClientSession()` is currently created fresh per request in
    `webhook.py` and `pushcut_client.py` rather than reused — keep this in
    mind if you're chasing performance, but match existing style unless asked
    to refactor it.
- **Logging, not printing.** Every module does
  `logger = logging.getLogger(__name__)` and logs via `logger.info/.warning/.error`.
  `bot.py` configures the root logger format once; don't add print statements
  or per-module `basicConfig` calls.
- **Config via environment only.** All secrets/IDs come from `os.getenv(...)`
  in `bot.py`, loaded from `.env` via `python-dotenv`. Never hardcode tokens,
  webhook URLs, or chat/channel IDs — thread new config through `bot.py` and
  `.env.example` (with a placeholder value) the same way.
- **Dependency injection over globals.** Modules take their collaborators
  (`bridge`, `discord_webhook`, `pushcut`) as constructor args rather than
  importing singletons. Follow this when adding a new client/handler.
- **Docstrings on every public method**, one line, imperative ("Send a message
  to Discord via the Hawk webhook."). Keep this style for new methods.
- **No type-checked schemas for webhook payloads.** Inbound JSON is read with
  `body.get(...)` defensively (e.g. `inputs.get("input0", "")`) rather than
  validated against a schema — match that style rather than introducing a new
  validation library for a one-off field.

## Webhook Server API (`webhook_server.py`)

| Method | Path | Purpose |
|---|---|---|
| GET | `/health` | Health check, returns `{"status": "ok", "service": "opxero-bridge"}` |
| POST | `/webhook/drafts` | Drafts App metadata dict (`{"draft_metadata": {...}}` or bare dict) → Discord embed + Telegram message |
| POST | `/webhook/taskade` | Taskade agent inputs (`{"inputs": {"input0":..., "input1":..., "input2":...}}`) → Pushcut widget update + Discord embed + Telegram message |
| POST | `/webhook/notify` | Generic `{"source": ..., "message": ...}` → Discord webhook + Telegram + Pushcut notification |

This server has no authentication — it's designed to be reachable only from a
trusted LAN/Shortcuts context. Don't add destructive or sensitive operations
to it without first raising the auth question.

## Telegram Commands (`telegram_bot.py`, bot `@opxero`)

`/start`, `/status`, `/chatid`, `/hawk <msg>`, `/taskade <in0> | <in1> | <in2>`,
`/notify <msg>`. Any non-command text message is forwarded to Discord through
`Bridge.forward_to_discord`. When adding a command, register it in
`TelegramBot.build()` alongside the existing `CommandHandler` list.

## CI

`.github/workflows/jekyll-gh-pages.yml` builds/deploys a Jekyll site to GitHub
Pages on push to `main`. This is unrelated to the Python bot (there's no
Jekyll content — `_config.yml`, `_posts/`, etc. — in the repo); GitHub Pages
will simply render `README.md` as the site's homepage. There is no CI that
runs the Python code (no lint/test workflow exists).

## Secrets Handling

`.env` is gitignored. `.env.example` holds placeholder values only — keep it
that way, and never commit real tokens, webhook URLs, or chat/channel IDs.
