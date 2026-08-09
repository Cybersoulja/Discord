import logging
import aiohttp

logger = logging.getLogger(__name__)


class GuildXyzClient:
    """Integration with Guild.xyz for role-gated guild membership checks."""

    def __init__(self, guild_id: str, api_key: str | None = None):
        self.guild_id = guild_id
        self.api_key = api_key
        self.base_url = "https://api.guild.xyz/v2"

    def _headers(self) -> dict:
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["X-Api-Key"] = self.api_key
        return headers

    async def get_guild(self) -> dict | None:
        """Fetch the configured Guild.xyz guild's public info."""
        url = f"{self.base_url}/guilds/{self.guild_id}"

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self._headers()) as resp:
                    if resp.status == 200:
                        return await resp.json()
                    body = await resp.text()
                    logger.error(f"Guild.xyz get_guild failed ({resp.status}): {body}")
                    return None
        except aiohttp.ClientError as e:
            logger.error(f"Guild.xyz get_guild network error: {e}")
            return None

    async def check_access(self, discord_user_id: str) -> list | None:
        """Check which roles a Discord user has been granted in the guild.

        Guild.xyz's member lookup is keyed by its own internal user ID, not a
        Discord snowflake, so this fetches the full member list and matches
        on each member's linked Discord platform account instead.
        """
        url = f"{self.base_url}/guilds/{self.guild_id}/members"

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self._headers()) as resp:
                    if resp.status != 200:
                        body = await resp.text()
                        logger.error(f"Guild.xyz check_access failed ({resp.status}): {body}")
                        return None
                    members = await resp.json()
        except aiohttp.ClientError as e:
            logger.error(f"Guild.xyz check_access network error: {e}")
            return None

        for member in members:
            for platform_user in member.get("platformUsers", []):
                platform_name = str(platform_user.get("platformName", "")).upper()
                platform_id = str(platform_user.get("platformUserId", ""))
                if platform_name == "DISCORD" and platform_id == str(discord_user_id):
                    return member.get("roleIds", [])

        return None
