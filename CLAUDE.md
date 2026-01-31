# CLAUDE.md - Discord Bot Project Context

## Project Overview

This is a feature-rich Discord bot built with Python using the discord.py library. The bot connects to Discord, handles commands, logs events, and provides useful functionality through event handlers and commands.

## Project Structure

- **bot.py** - Main bot implementation with commands, event handlers, and error handling
- **README.md** - User-facing documentation with setup and usage instructions
- **requirements.txt** - Python dependencies (discord.py, python-dotenv)
- **.env.example** - Example environment configuration file
- **.gitignore** - Git ignore rules for secrets and Python artifacts
- **CLAUDE.md** - This file - context for AI assistants

## Key Components

### bot.py
- **Environment Configuration**
  - Loads `.env` file with `load_dotenv()`
  - Validates BOT_TOKEN is set and not placeholder
  - Configurable logging level via LOG_LEVEL env variable

- **Bot Instance** (`bot = commands.Bot()`)
  - Uses `commands.Bot` for command handling
  - Command prefix: `!`
  - Intents: default + message_content + members + reactions

- **Event Handlers**
  - `on_ready()`: Logs successful login and guild count
  - `on_message()`: Logs all messages and processes commands
  - `on_member_join()`: Sends welcome message and logs member joins
  - `on_member_remove()`: Logs member departures
  - `on_reaction_add()`: Logs when users add reactions
  - `on_reaction_remove()`: Logs when users remove reactions
  - `on_command_error()`: Global error handler for invalid commands

- **Commands**
  - `!hello` - Responds with a greeting
  - `!ping` - Shows bot latency
  - `!help_custom` - Displays available commands with descriptions

- **Logging**
  - Configured with timestamps and log levels
  - All events and commands are logged
  - Errors are caught and logged gracefully

## Configuration

The bot uses environment variables loaded from `.env`:
- `BOT_TOKEN` (required) - Discord bot token from developer portal
- `LOG_LEVEL` (optional, default: INFO) - Controls logging verbosity

## Setup Context

To get this project running:
1. Run `pip install -r requirements.txt` to install discord.py and python-dotenv
2. Copy `.env.example` to `.env`
3. Add your Discord bot token to `.env`
4. Run `python bot.py`

## Features Implemented

- ✅ Command handling with prefix-based commands
- ✅ Environment variable configuration (no hardcoded secrets)
- ✅ Comprehensive logging framework
- ✅ Member join/leave event handlers
- ✅ Reaction tracking on messages
- ✅ Global error handling with user-friendly messages
- ✅ Multiple commands with help documentation
- ✅ Message content intent enabled for full message text

## Architecture Notes

- Uses discord.py's `commands.Bot` extension for cleaner command handling
- All event handlers are async functions using `@bot.event` decorator
- Commands are defined as async functions using `@bot.command()` decorator
- Error handling is centralized in `on_command_error()` handler
- Logging provides visibility into bot operations and user interactions

## Development Guidelines

- Keep changes focused and minimal
- Follow PEP 8 style guidelines for Python
- Document new features in README.md and CLAUDE.md
- Use async/await patterns for all Discord events and commands
- Add error handling for new event handlers
- Update this file when adding significant features or changing architecture
- Keep environment-specific configuration in `.env`, never hardcode secrets

## Future Enhancement Areas

- Database integration for data persistence
- Cog-based architecture for modular commands
- Command permissions and role-based access control
- Message embeds for richer command responses
- Automated task scheduling
- Rate limiting and spam detection
- User statistics and metrics tracking
