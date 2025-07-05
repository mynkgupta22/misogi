import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class MessageTools:
    def __init__(self, discord_bot):
        self.bot = discord_bot

    async def send_message(self, channel_id: str, content: str) -> Dict[str, Any]:
        """Send a message to a specific channel."""
        try:
            channel = await self.bot.bot.fetch_channel(int(channel_id))
            message = await channel.send(content)
            return {
                "success": True,
                "message_id": str(message.id),
                "content": message.content,
                "timestamp": message.created_at.isoformat()
            }
        except Exception as e:
            logger.error(f"Failed to send message: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    async def get_messages(self, channel_id: str, limit: int = 100) -> Dict[str, Any]:
        """Get recent messages from a channel."""
        try:
            channel = await self.bot.bot.fetch_channel(int(channel_id))
            messages = []
            async for message in channel.history(limit=limit):
                messages.append({
                    "id": str(message.id),
                    "content": message.content,
                    "author": str(message.author),
                    "timestamp": message.created_at.isoformat()
                })
            return {
                "success": True,
                "messages": messages
            }
        except Exception as e:
            logger.error(f"Failed to get messages: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    async def search_messages(self, channel_id: str, query: str, limit: int = 100) -> Dict[str, Any]:
        """Search for messages containing specific text."""
        try:
            channel = await self.bot.bot.fetch_channel(int(channel_id))
            messages = []
            async for message in channel.history(limit=limit):
                if query.lower() in message.content.lower():
                    messages.append({
                        "id": str(message.id),
                        "content": message.content,
                        "author": str(message.author),
                        "timestamp": message.created_at.isoformat()
                    })
            return {
                "success": True,
                "messages": messages
            }
        except Exception as e:
            logger.error(f"Failed to search messages: {e}")
            return {
                "success": False,
                "error": str(e)
            } 