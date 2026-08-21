import logging
import aiohttp

logger = logging.getLogger(__name__)


class DiscordWebhook:
    """Send messages to Discord via the Hawk webhook in #taskade channel."""

    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    async def send(self, content: str, username: str = "Hawk", embed: dict | None = None):
        """Send a message or embed to the Discord webhook."""
        payload = {"username": username}
        if content:
            payload["content"] = content
        if embed:
            payload["embeds"] = [embed]

        async with aiohttp.ClientSession() as session:
            async with session.post(self.webhook_url, json=payload) as resp:
                if resp.status == 204:
                    logger.info(f"Webhook sent: {content[:50] if content else 'embed'}")
                else:
                    body = await resp.text()
                    logger.error(f"Webhook failed ({resp.status}): {body}")

    async def send_draft(self, draft_metadata: dict):
        """Send a Drafts App note as a formatted Discord embed."""
        embed = {
            "title": draft_metadata.get("title", "Untitled Draft"),
            "color": 0x5865F2,
            "fields": [],
        }
        field_map = {
            "uuid": "UUID",
            "folder": "Folder",
            "tags": "Tags",
            "created": "Created",
            "modified": "Modified",
            "flagged": "Flagged",
            "language": "Language",
        }
        for key, label in field_map.items():
            value = draft_metadata.get(key)
            if value:
                embed["fields"].append({"name": label, "value": str(value), "inline": True})

        lat = draft_metadata.get("latitude")
        lon = draft_metadata.get("longitude")
        if lat and lon and lat != "0" and lon != "0":
            embed["fields"].append({"name": "Location", "value": f"{lat}, {lon}", "inline": True})

        await self.send(content=None, username="Drafts", embed=embed)

    async def send_taskade_update(self, inputs: dict):
        """Send a Taskade agent update as a Discord embed."""
        embed = {
            "title": "Taskade Agent Update",
            "color": 0xE040FB,
            "fields": [
                {"name": f"Input {i}", "value": str(v) or "-", "inline": False}
                for i, v in enumerate(inputs.values())
            ],
        }
        await self.send(content=None, username="Taskade Agent", embed=embed)
