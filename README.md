# Discord Bot

A feature-rich Discord bot built with Python using discord.py.

## Features

- **Command handling** - Process Discord commands with `!` prefix
- **Event logging** - Track messages, member joins/leaves, and reactions
- **Member events** - Welcome messages when members join the server
- **Reaction tracking** - Log user reactions on messages
- **Error handling** - Comprehensive error handling and feedback
- **Configurable logging** - Adjustable log levels via environment variables

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment variables

Copy the example environment file:
```bash
cp .env.example .env
```

Edit `.env` and add your Discord bot token:
```
BOT_TOKEN=your_actual_bot_token_here
LOG_LEVEL=INFO
```

**Note:** Never commit the `.env` file to version control. It's in `.gitignore` by default.

### 3. Get your Discord Bot Token

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application"
3. Go to "Bot" section and click "Add Bot"
4. Under TOKEN section, click "Copy" to copy your bot token
5. Paste it in your `.env` file

## Running the Bot

Start the bot with:
```bash
python bot.py
```

You should see output like:
```
INFO:discord.client:Logging in as YourBotName#1234
INFO:__main__:Logged in as YourBotName#1234
INFO:__main__:Bot is in 1 guild(s)
```

## Available Commands

- `!hello` - Say hello to the bot
- `!ping` - Check bot latency
- `!help_custom` - Display all available commands

## Bot Events

The bot tracks and logs the following events:

- **Messages** - Logs all messages sent in servers where bot has access
- **Member Join** - Sends welcome message and logs when members join
- **Member Leave** - Logs when members leave the server
- **Reactions** - Logs when reactions are added or removed from messages
- **Errors** - Comprehensive error handling with user-friendly error messages

## Configuration

You can adjust the bot behavior through the `.env` file:

- `BOT_TOKEN` - Your Discord bot token (required)
- `LOG_LEVEL` - Logging verbosity (DEBUG, INFO, WARNING, ERROR, CRITICAL) - default: INFO

## Project Structure

- `bot.py` - Main bot implementation with all handlers and commands
- `requirements.txt` - Python dependencies
- `.env.example` - Example environment configuration
- `.gitignore` - Files to exclude from version control
- `README.md` - This file
- `CLAUDE.md` - Context for AI assistants working on this project

## Development

For more detailed information about the project structure and development guidelines, see `CLAUDE.md`.
