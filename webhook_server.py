import json
import logging
from aiohttp import web

logger = logging.getLogger(__name__)


class WebhookServer:
    """HTTP server that receives automation payloads from Drafts, Pushcut, Shortcuts, etc.

    Endpoints:
        POST /webhook/drafts    - Receive Drafts App metadata dictionaries
        POST /webhook/taskade   - Receive Taskade agent input updates
        POST /webhook/notify    - Generic notification to Discord + Telegram
        GET  /health            - Health check
    """

    def __init__(self, port: int, discord_webhook=None, pushcut=None, bridge=None):
        self.port = port
        self.discord_webhook = discord_webhook
        self.pushcut = pushcut
        self.bridge = bridge
        self.app = web.Application()
        self._setup_routes()

    def _setup_routes(self):
        self.app.router.add_get("/health", self.health)
        self.app.router.add_post("/webhook/drafts", self.handle_drafts)
        self.app.router.add_post("/webhook/taskade", self.handle_taskade)
        self.app.router.add_post("/webhook/notify", self.handle_notify)

    async def health(self, request):
        return web.json_response({"status": "ok", "service": "opxero-bridge"})

    async def handle_drafts(self, request):
        """Receive a Drafts App metadata dictionary and forward to Discord + Telegram."""
        try:
            body = await request.json()
            metadata = body.get("draft_metadata", body)
            logger.info(f"Received draft: {metadata.get('title', 'untitled')}")

            # Forward to Discord via Hawk webhook
            if self.discord_webhook:
                await self.discord_webhook.send_draft(metadata)

            # Forward to Telegram
            if self.bridge and self.bridge.telegram_bot and self.bridge.telegram_chat_id:
                title = metadata.get("title", "Untitled")
                tags = metadata.get("tags", "")
                folder = metadata.get("folder", "")
                text = f"📝 *New Draft:* {title}\nFolder: {folder}\nTags: {tags}"
                await self.bridge.telegram_bot.send_message(
                    chat_id=self.bridge.telegram_chat_id, text=text
                )

            return web.json_response({"status": "ok", "received": "draft"})
        except (json.JSONDecodeError, Exception) as e:
            logger.error(f"Drafts webhook error: {e}")
            return web.json_response({"status": "error", "message": str(e)}, status=400)

    async def handle_taskade(self, request):
        """Receive Taskade agent inputs and update Pushcut widget + Discord."""
        try:
            body = await request.json()
            inputs = body.get("inputs", body)
            input0 = inputs.get("input0", "")
            input1 = inputs.get("input1", "")
            input2 = inputs.get("input2", "")

            logger.info(f"Received taskade update: {input0[:50]}")

            # Update Pushcut widget
            if self.pushcut:
                await self.pushcut.update_widget(input0=input0, input1=input1, input2=input2)

            # Send to Discord via Hawk webhook
            if self.discord_webhook:
                await self.discord_webhook.send_taskade_update(inputs)

            # Notify Telegram
            if self.bridge and self.bridge.telegram_bot and self.bridge.telegram_chat_id:
                text = f"🤖 *Taskade Agent Update*\n{input0}\n{input1}\n{input2}".strip()
                await self.bridge.telegram_bot.send_message(
                    chat_id=self.bridge.telegram_chat_id, text=text
                )

            return web.json_response({"status": "ok", "received": "taskade"})
        except (json.JSONDecodeError, Exception) as e:
            logger.error(f"Taskade webhook error: {e}")
            return web.json_response({"status": "error", "message": str(e)}, status=400)

    async def handle_notify(self, request):
        """Generic notification endpoint - sends to both Discord and Telegram."""
        try:
            body = await request.json()
            message = body.get("message", "")
            source = body.get("source", "Automation")

            if not message:
                return web.json_response({"status": "error", "message": "missing 'message'"}, status=400)

            logger.info(f"Notify from {source}: {message[:50]}")

            # Discord webhook
            if self.discord_webhook:
                await self.discord_webhook.send(content=f"**[{source}]** {message}", username=source)

            # Telegram
            if self.bridge and self.bridge.telegram_bot and self.bridge.telegram_chat_id:
                await self.bridge.telegram_bot.send_message(
                    chat_id=self.bridge.telegram_chat_id, text=f"[{source}] {message}"
                )

            # Pushcut notification
            if self.pushcut:
                await self.pushcut.trigger_notification(title=source, text=message)

            return web.json_response({"status": "ok"})
        except (json.JSONDecodeError, Exception) as e:
            logger.error(f"Notify webhook error: {e}")
            return web.json_response({"status": "error", "message": str(e)}, status=400)

    async def start(self):
        """Start the webhook server."""
        runner = web.AppRunner(self.app)
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", self.port)
        await site.start()
        logger.info(f"Webhook server listening on port {self.port}")
        return runner
