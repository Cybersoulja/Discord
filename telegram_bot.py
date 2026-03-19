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

    def __init__(self, token: str, bridge=None, discord_webhook=None, pushcut=None):
        self.token = token
        self.bridge = bridge
        self.discord_webhook = discord_webhook
        self.pushcut = pushcut
        self.application = None

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /start command."""
        await update.message.reply_text(
            "Hello! I'm @opxero bot.\n\n"
            "Bridge Commands:\n"
            "/status - Check bridge status\n"
            "/chatid - Get this chat's ID\n\n"
            "Automation Commands:\n"
            "/hawk <message> - Send via Hawk webhook to #taskade\n"
            "/taskade <input0> | <input1> | <input2> - Update Taskade agent widget\n"
            "/notify <message> - Send to all channels"
        )

    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /status command."""
        discord_status = "Connected" if self.bridge and self.bridge.discord_ready else "Disconnected"
        webhook_status = "Configured" if self.discord_webhook else "Not configured"
        pushcut_status = "Configured" if self.pushcut else "Not configured"
        await update.message.reply_text(
            f"Bridge Status:\n"
            f"  Telegram: Connected\n"
            f"  Discord: {discord_status}\n"
            f"  Hawk Webhook: {webhook_status}\n"
            f"  Pushcut: {pushcut_status}"
        )

    async def chatid_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the /chatid command to get the current chat ID."""
        await update.message.reply_text(
            f"Chat ID: `{update.effective_chat.id}`", parse_mode="Markdown"
        )

    async def hawk_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Send a message to Discord #taskade via the Hawk webhook."""
        if not context.args:
            await update.message.reply_text("Usage: /hawk <message>")
            return
        message = " ".join(context.args)
        if self.discord_webhook:
            await self.discord_webhook.send(content=message, username="Hawk (via @opxero)")
            await update.message.reply_text("Sent to #taskade via Hawk.")
        else:
            await update.message.reply_text("Hawk webhook not configured.")

    async def taskade_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Update the Taskade agent Pushcut widget. Inputs separated by |."""
        if not context.args:
            await update.message.reply_text("Usage: /taskade <input0> | <input1> | <input2>")
            return
        raw = " ".join(context.args)
        parts = [p.strip() for p in raw.split("|")]
        input0 = parts[0] if len(parts) > 0 else ""
        input1 = parts[1] if len(parts) > 1 else ""
        input2 = parts[2] if len(parts) > 2 else ""

        results = []
        if self.pushcut:
            ok = await self.pushcut.update_widget(input0=input0, input1=input1, input2=input2)
            results.append("Pushcut widget updated." if ok else "Pushcut update failed.")
        if self.discord_webhook:
            await self.discord_webhook.send_taskade_update(
                {"input0": input0, "input1": input1, "input2": input2}
            )
            results.append("Sent to #taskade.")

        await update.message.reply_text("\n".join(results) if results else "No integrations configured.")

    async def notify_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Send a notification to all connected channels."""
        if not context.args:
            await update.message.reply_text("Usage: /notify <message>")
            return
        message = " ".join(context.args)
        sender = update.message.from_user.first_name or "opxero"

        if self.discord_webhook:
            await self.discord_webhook.send(content=f"**[{sender}]** {message}", username=sender)
        if self.pushcut:
            await self.pushcut.trigger_notification(title="opxero", text=message)

        await update.message.reply_text("Notification sent.")

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
        self.application.add_handler(CommandHandler("hawk", self.hawk_command))
        self.application.add_handler(CommandHandler("taskade", self.taskade_command))
        self.application.add_handler(CommandHandler("notify", self.notify_command))
        self.application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message)
        )

        logger.info("Telegram bot (@opxero) handlers registered")
        return self.application

    async def send_message(self, chat_id: int, text: str):
        """Send a message to a Telegram chat."""
        if self.application and self.application.bot:
            await self.application.bot.send_message(chat_id=chat_id, text=text)
