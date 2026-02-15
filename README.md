# Discord-Telegram Bridge Bot

A Python bot that bridges messages between Discord and Telegram (@opxero).

Messages sent in a configured Discord channel are forwarded to a Telegram chat and vice versa.

## Features

- Bi-directional message forwarding between Discord and Telegram
- Configurable channel/chat mapping
- Telegram commands: `/start`, `/status`, `/chatid`
- Runs both bots concurrently in a single process

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment variables

Copy the example env file and fill in your values:

```bash
cp .env.example .env
```

Edit `.env` with your tokens and channel IDs:

| Variable | Description |
|---|---|
| `DISCORD_BOT_TOKEN` | Your Discord bot token (from [Discord Developer Portal](https://discord.com/developers/applications)) |
| `TELEGRAM_BOT_TOKEN` | Your Telegram bot token (from [@BotFather](https://t.me/BotFather) for @opxero) |
| `DISCORD_CHANNEL_ID` | The Discord channel ID to bridge |
| `TELEGRAM_CHAT_ID` | The Telegram chat ID to bridge (use `/chatid` command in Telegram to find it) |

### 3. Get your Telegram Chat ID

1. Start the bot without `TELEGRAM_CHAT_ID` set
2. Send `/chatid` to @opxero on Telegram
3. Copy the returned chat ID into your `.env` file

## Running the Bot

```bash
python bot.py
```

Both the Discord and Telegram bots will start concurrently.

## Telegram Commands

| Command | Description |
|---|---|
| `/start` | Show welcome message and available commands |
| `/status` | Check bridge connection status |
| `/chatid` | Get the current chat's ID for configuration |

## Architecture

```
bot.py            - Main entry point, runs both bots concurrently
telegram_bot.py   - Telegram bot (@opxero) handlers and setup
bridge.py         - Message forwarding logic between platforms
```
