import logging

logger = logging.getLogger(__name__)


class Bridge:
    """Bridges messages between Discord and Telegram."""

    def __init__(self, discord_channel_id: int | None = None, telegram_chat_id: int | None = None):
        self.discord_channel_id = discord_channel_id
        self.telegram_chat_id = telegram_chat_id
        self.discord_client = None
        self.telegram_bot = None
        self.discord_ready = False

    def set_discord_client(self, client):
        self.discord_client = client

    def set_telegram_bot(self, bot):
        self.telegram_bot = bot

    async def forward_to_discord(self, sender: str, content: str, chat_id: int):
        """Forward a message from Telegram to Discord."""
        if not self.discord_client or not self.discord_ready:
            logger.warning("Discord client not ready, dropping message")
            return

        if self.telegram_chat_id and chat_id != self.telegram_chat_id:
            return

        if not self.discord_channel_id:
            logger.warning("DISCORD_CHANNEL_ID not configured, cannot forward to Discord")
            return

        channel = self.discord_client.get_channel(self.discord_channel_id)
        if channel is None:
            logger.error(f"Discord channel {self.discord_channel_id} not found")
            return

        formatted = f"**[Telegram] {sender}:** {content}"
        await channel.send(formatted)
        logger.info(f"Forwarded Telegram -> Discord: {sender}: {content[:50]}")

    async def forward_to_telegram(self, sender: str, content: str, channel_id: int):
        """Forward a message from Discord to Telegram."""
        if not self.telegram_bot:
            logger.warning("Telegram bot not available, dropping message")
            return

        if self.discord_channel_id and channel_id != self.discord_channel_id:
            return

        if not self.telegram_chat_id:
            logger.warning("TELEGRAM_CHAT_ID not configured, cannot forward to Telegram")
            return

        formatted = f"[Discord] {sender}: {content}"
        await self.telegram_bot.send_message(chat_id=self.telegram_chat_id, text=formatted)
        logger.info(f"Forwarded Discord -> Telegram: {sender}: {content[:50]}")
