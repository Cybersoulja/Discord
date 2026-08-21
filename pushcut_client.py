import logging
import aiohttp

logger = logging.getLogger(__name__)


class PushcutClient:
    """Integration with Pushcut for taskade-agent widget updates."""

    def __init__(self, api_key: str, widget_id: str = "taskade-agent"):
        self.api_key = api_key
        self.widget_id = widget_id
        self.base_url = "https://api.pushcut.io"

    async def update_widget(self, input0: str = "", input1: str = "", input2: str = ""):
        """Update the taskade-agent Pushcut widget with new input values."""
        url = f"{self.base_url}/v1/widgets/{self.widget_id}"
        headers = {"API-Key": self.api_key, "Content-Type": "application/json"}
        payload = {
            "inputs": {
                "input0": input0,
                "input1": input1,
                "input2": input2,
            }
        }

        async with aiohttp.ClientSession() as session:
            async with session.put(url, json=payload, headers=headers) as resp:
                if resp.status == 200:
                    logger.info(f"Pushcut widget '{self.widget_id}' updated")
                    return True
                else:
                    body = await resp.text()
                    logger.error(f"Pushcut update failed ({resp.status}): {body}")
                    return False

    async def trigger_notification(self, title: str, text: str = ""):
        """Send a Pushcut notification."""
        url = f"{self.base_url}/v1/notifications/{title}"
        headers = {"API-Key": self.api_key, "Content-Type": "application/json"}
        payload = {}
        if text:
            payload["text"] = text

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload, headers=headers) as resp:
                if resp.status == 200:
                    logger.info(f"Pushcut notification '{title}' sent")
                    return True
                else:
                    body = await resp.text()
                    logger.error(f"Pushcut notification failed ({resp.status}): {body}")
                    return False
