# Getting Started

Quick setup guide for the Discord-Telegram automation bridge.

## Prerequisites

- Python 3.10+
- A Discord bot token ([Developer Portal](https://discord.com/developers/applications))
- The @opxero Telegram bot token (from [@BotFather](https://t.me/BotFather))

## 1. Install

```bash
git clone https://github.com/Cybersoulja/Discord.git
cd Discord
pip install -r requirements.txt
```

## 2. Configure

```bash
cp .env.example .env
```

Open `.env` and fill in the **required** values:

```
DISCORD_BOT_TOKEN=your_discord_token
TELEGRAM_BOT_TOKEN=your_opxero_token
```

Then add any **optional** integrations you use:

```
DISCORD_CHANNEL_ID=123456789          # Bridge messages from this Discord channel
TELEGRAM_CHAT_ID=987654321            # Bridge messages to this Telegram chat
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...   # Hawk webhook for #taskade
PUSHCUT_API_KEY=your_key              # Pushcut widget updates
```

> **Tip:** Don't know your Telegram chat ID? Start the bot first, then send `/chatid` to @opxero.

## 3. Run

```bash
python bot.py
```

You should see:

```
Webhook server listening on port 8080
Telegram bot (@opxero) handlers registered
Starting Discord + Telegram (@opxero) bridge with automation hub...
Discord bot logged in as YourBot#1234
```

## 4. Test It

**From Telegram (@opxero):**

```
/status          → Check all connections
/hawk Hello!     → Posts "Hello!" to Discord #taskade
/notify Test     → Broadcasts to Discord + Pushcut
```

**From a Shortcut or curl:**

```bash
# Send a Drafts note
curl -X POST http://localhost:8080/webhook/drafts \
  -H "Content-Type: application/json" \
  -d '{"draft_metadata": {"title": "My Note", "tags": "idea", "folder": "Inbox"}}'

# Update Taskade agent widget
curl -X POST http://localhost:8080/webhook/taskade \
  -H "Content-Type: application/json" \
  -d '{"inputs": {"input0": "Status", "input1": "Active", "input2": "3 tasks"}}'

# Health check
curl http://localhost:8080/health
```

## 5. Connect Your iOS Automations

### Drafts App Action

In your Drafts action, POST the metadata dictionary to:
```
http://<your-server>:8080/webhook/drafts
```

### Pushcut / Shortcuts

Point your Shortcut's "Get Contents of URL" action to:
```
http://<your-server>:8080/webhook/taskade
```

With the JSON body:
```json
{"inputs": {"input0": "[[input0]]", "input1": "[[input1]]", "input2": "[[input2]]"}}
```

## Troubleshooting

| Problem | Fix |
|---|---|
| `DISCORD_BOT_TOKEN not set` | Check your `.env` file exists and has the token |
| Telegram not receiving messages | Run `/chatid`, then set `TELEGRAM_CHAT_ID` in `.env` |
| Hawk webhook not working | Verify `DISCORD_WEBHOOK_URL` matches your webhook settings |
| Pushcut not updating | Confirm `PUSHCUT_API_KEY` is valid in Pushcut app settings |
| Port 8080 in use | Set `WEBHOOK_SERVER_PORT=9090` in `.env` |
