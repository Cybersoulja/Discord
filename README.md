# Discord-Telegram Automation Bridge

A Python bot bridging Discord, Telegram (@opxero), Drafts App, Pushcut, and Taskade into a unified automation hub.

## Features

- **Bi-directional bridge** between Discord and Telegram (@opxero)
- **Hawk webhook** posts to Discord #taskade channel
- **Drafts App integration** receives draft metadata dictionaries via webhook
- **Pushcut widget updates** for the taskade-agent widget (`[[input0]]`, `[[input1]]`, `[[input2]]`)
- **HTTP webhook server** receives payloads from iOS Shortcuts, Drafts actions, and other automations
- **Telegram commands** to trigger automations from mobile
- **Guild.xyz integration** checks role-gated guild access and relays membership events
- **Bot/agent chat support** lets allowlisted Discord bots and Telegram `/agent` messages bridge as agents instead of being dropped

## Architecture

```
bot.py              - Main entry point, runs all services concurrently
telegram_bot.py     - Telegram bot (@opxero) with automation commands
bridge.py           - Discord <-> Telegram message forwarding
webhook.py          - Discord webhook client (Hawk -> #taskade)
pushcut_client.py   - Pushcut API client (widget + notification)
guildxyz_client.py  - Guild.xyz API client (guild info + member access)
webhook_server.py   - HTTP server receiving external automation payloads
```

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
```

| Variable | Description |
|---|---|
| `DISCORD_BOT_TOKEN` | Discord bot token |
| `TELEGRAM_BOT_TOKEN` | @opxero token from @BotFather |
| `DISCORD_CHANNEL_ID` | Discord channel ID to bridge |
| `TELEGRAM_CHAT_ID` | Telegram chat ID to bridge |
| `DISCORD_WEBHOOK_URL` | Hawk webhook URL for #taskade |
| `PUSHCUT_API_KEY` | Pushcut API key for widget updates |
| `PUSHCUT_WIDGET_ID` | Pushcut widget ID (default: `taskade-agent`) |
| `GUILDXYZ_GUILD_ID` | Guild.xyz guild ID to check role access against |
| `GUILDXYZ_API_KEY` | Guild.xyz API key |
| `DISCORD_AGENT_BOT_IDS` | Comma-separated Discord bot/application IDs allowed to bridge as agents |
| `WEBHOOK_SERVER_PORT` | HTTP server port (default: `8080`) |

### 3. Run

```bash
python bot.py
```

## Telegram Commands (@opxero)

| Command | Description |
|---|---|
| `/start` | Show help |
| `/status` | Bridge + integration status |
| `/chatid` | Get chat ID for config |
| `/hawk <msg>` | Send message to #taskade via Hawk webhook |
| `/taskade <in0> \| <in1> \| <in2>` | Update Taskade agent Pushcut widget |
| `/notify <msg>` | Send to all channels (Discord, Telegram, Pushcut) |
| `/agent <msg>` | Send a bot/agent chat message to Discord |
| `/guild <discord_user_id>` | Check a user's Guild.xyz role access |

## Webhook Endpoints

The HTTP server (default port 8080) accepts automation payloads:

### `POST /webhook/drafts`

Receives Drafts App metadata dictionaries:

```json
{
  "draft_metadata": {
    "uuid": "...",
    "title": "...",
    "created": "...",
    "modified": "...",
    "tags": "...",
    "folder": "...",
    "flagged": "...",
    "language": "..."
  }
}
```

### `POST /webhook/taskade`

Updates Taskade agent widget and posts to Discord:

```json
{
  "inputs": {
    "input0": "...",
    "input1": "...",
    "input2": "..."
  }
}
```

### `POST /webhook/notify`

Generic notification to all channels:

```json
{
  "source": "AutomationLab",
  "message": "Build completed successfully"
}
```

### `POST /webhook/guildxyz`

Receives a Guild.xyz role/membership event and posts it to Discord + Telegram:

```json
{
  "event": "role_granted",
  "userId": "discord-user-id",
  "guildId": "guildxyz-guild-id",
  "roleIds": ["role-id-1"]
}
```

### `GET /webhook/guildxyz/{user_id}`

Looks up a Discord user's Guild.xyz role access:

```json
{
  "status": "ok",
  "userId": "discord-user-id",
  "roleIds": ["role-id-1"]
}
```

Returns `404` if the user has no Guild.xyz access, or `503` if Guild.xyz isn't configured.

### `GET /status`

Bridge and integration status:

```json
{
  "discord": "connected",
  "hawk_webhook": true,
  "pushcut": true,
  "guildxyz": true
}
```

### `GET /health`

Health check endpoint.

## iOS Shortcuts Integration

Use these URL patterns in your Shortcuts:

- **Drafts action**: POST draft metadata JSON to `http://<server>:8080/webhook/drafts`
- **Taskade update**: POST inputs to `http://<server>:8080/webhook/taskade`
- **Notify**: POST `{"source": "Shortcuts", "message": "..."}` to `http://<server>:8080/webhook/notify`
- **Guild.xyz role lookup**: GET `http://<server>:8080/webhook/guildxyz/<discord_user_id>`
- **Bridge status**: GET `http://<server>:8080/status`
