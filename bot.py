import asyncio
import logging
import os

import discord
from dotenv import load_dotenv

from bridge import Bridge
from telegram_bot import TelegramBot

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
)
logger = logging.getLogger(__name__)

# Configuration from environment
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
DISCORD_CHANNEL_ID = os.getenv("DISCORD_CHANNEL_ID")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


# --- Bridge setup ---
bridge = Bridge(
    discord_channel_id=int(DISCORD_CHANNEL_ID) if DISCORD_CHANNEL_ID else None,
    telegram_chat_id=int(TELEGRAM_CHAT_ID) if TELEGRAM_CHAT_ID else None,
)


# --- Discord client ---
class DiscordBot(discord.Client):
    async def on_ready(self):
        bridge.discord_ready = True
        logger.info(f"Discord bot logged in as {self.user}")

    async def on_message(self, message):
        # Ignore messages from this bot itself
        if message.author == self.user:
            return
        # Ignore bridged messages (sent by this bot)
        if message.author.bot:
            return

        logger.info(f"[Discord] {message.author}: {message.content}")
        await bridge.forward_to_telegram(
            sender=str(message.author.display_name),
            content=message.content,
            channel_id=message.channel.id,
        )


async def main():
    if not DISCORD_BOT_TOKEN:
        logger.error("DISCORD_BOT_TOKEN not set in environment")
        return
    if not TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN not set in environment")
        return

    # Build Telegram bot
    telegram = TelegramBot(token=TELEGRAM_BOT_TOKEN, bridge=bridge)
    app = telegram.build()
    bridge.set_telegram_bot(telegram)

    # Build Discord bot
    intents = discord.Intents.default()
    intents.message_content = True
    discord_client = DiscordBot(intents=intents)
    bridge.set_discord_client(discord_client)

    # Run both bots concurrently
    logger.info("Starting Discord + Telegram (@opxero) bridge...")

    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    try:
        await discord_client.start(DISCORD_BOT_TOKEN)
    finally:
        await app.updater.stop()
        await app.stop()
        await app.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
