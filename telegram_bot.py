import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

logger = logging.getLogger(__name__)


class TelegramBot:
    """Telegram bot integration for @opxero."""

    def __init__(self, token: str, bridge=None):
        self.token = token
        self.bridge = bridge
        self.application = None

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /start command."""
        await update.message.reply_text(
            "Hello! I'm @opxero bot. I'm bridged with Discord.\n\n"
            "Commands:\n"
            "/start - Show this message\n"
            "/status - Check bridge status\n"
            "/chatid - Get this chat's ID"
        )

    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /status command."""
        discord_status = "Connected" if self.bridge and self.bridge.discord_ready else "Disconnected"
        await update.message.reply_text(
            f"Bridge Status:\n"
            f"  Telegram: Connected\n"
            f"  Discord: {discord_status}"
        )

    async def chatid_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /chatid command to get the current chat ID."""
        await update.message.reply_text(f"Chat ID: `{update.effective_chat.id}`", parse_mode="Markdown")

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Forward incoming Telegram messages to Discord via the bridge."""
        if update.message is None or update.message.text is None:
            return

        if self.bridge:
            sender = update.message.from_user
            display_name = sender.first_name or sender.username or "Unknown"
            await self.bridge.forward_to_discord(
                sender=display_name,
                content=update.message.text,
                chat_id=update.effective_chat.id,
            )

    def build(self) -> Application:
        """Build the Telegram application with handlers."""
        self.application = Application.builder().token(self.token).build()

        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("status", self.status_command))
        self.application.add_handler(CommandHandler("chatid", self.chatid_command))
        self.application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message)
        )

        logger.info("Telegram bot (@opxero) handlers registered")
        return self.application

    async def send_message(self, chat_id: int, text: str):
        """Send a message to a Telegram chat."""
        if self.application and self.application.bot:
            await self.application.bot.send_message(chat_id=chat_id, text=text)
