import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class ChannelTools:
    def __init__(self, discord_bot):
        self.bot = discord_bot

    async def get_channel_info(self, channel_id: str) -> Dict[str, Any]:
        """Get information about a specific channel."""
        try:
            channel = await self.bot.bot.fetch_channel(int(channel_id))
            return {
                "success": True,
                "channel_info": {
                    "id": str(channel.id),
                    "name": channel.name,
                    "type": str(channel.type),
                    "position": channel.position,
                    "category": str(channel.category.name) if channel.category else None,
                    "created_at": channel.created_at.isoformat()
                }
            }
        except Exception as e:
            logger.error(f"Failed to get channel info: {e}")
            return {
                "success": False,
                "error": str(e)
            } 