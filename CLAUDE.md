# CLAUDE.md - Discord Bot Project Context

## Project Overview

This is a simple Discord bot built with Python using the discord.py library. The bot currently connects to Discord and logs messages sent in servers where it has access.

## Project Structure

- **bot.py** - Main bot entry point containing the bot client implementation
- **README.md** - User-facing documentation with setup instructions
- **requirements.txt** - Python dependencies (discord.py)

## Key Components

### bot.py
- `MyClient`: Custom Discord client class extending `discord.Client`
  - `on_ready()`: Handler called when bot successfully logs in
  - `on_message()`: Handler called when bot receives a message
- `BOT_TOKEN`: Configuration variable for Discord bot token (requires user to set)
- `intents`: Discord intents configuration enabling message content reading

## Setup Context

To get this project running:
1. Ensure requirements.txt lists discord.py
2. Users must set BOT_TOKEN with their actual Discord bot token
3. Run with: `python bot.py`

## Current Limitations

- Bot only logs messages, no actual command handling implemented
- Bot token is hardcoded as a string constant (should be environment variable)
- No error handling or logging framework
- No database or persistent storage
- Limited event handlers

## Development Guidelines

- Keep changes focused and minimal
- Follow PEP 8 style guidelines for Python
- Document new features in README.md
- Update this file when adding significant features or changing architecture

## Future Enhancement Areas

- Command handling and parsing
- Database integration for data persistence
- Better configuration management (environment variables)
- More event handlers (reactions, member joins, etc.)
- Error handling and logging
- Help commands and command documentation
