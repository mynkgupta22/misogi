import logging
import asyncio
from fastmcp import FastMCP
from .discord_bot import DiscordBot
from .tools.message_tools import MessageTools
from .tools.channel_tools import ChannelTools
from .tools.moderation_tools import ModerationTools
from .auth.api_key_auth import APIKeyAuth
from .inspector.debug import MCPInspector

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DiscordMCPServer(FastMCP):
    def __init__(self):
        super().__init__(name="Discord MCP Server")
        self.discord_bot = DiscordBot()
        self.auth = APIKeyAuth()
        self.inspector = MCPInspector()
        
        # Initialize tools
        self.message_tools = MessageTools(self.discord_bot)
        self.channel_tools = ChannelTools(self.discord_bot)
        self.moderation_tools = ModerationTools(self.discord_bot)
        
        self.register_tools()

    def register_tools(self):
        """Register all tools with the MCP server."""
        # Message tools
        @self.tool(name="send_message", description="Send a message to a Discord channel")
        async def send_message(channel_id: str, content: str):
            return await self.message_tools.send_message(channel_id, content)

        @self.tool(name="get_messages", description="Get recent messages from a Discord channel")
        async def get_messages(channel_id: str, limit: int = 100):
            return await self.message_tools.get_messages(channel_id, limit)

        @self.tool(name="search_messages", description="Search for messages in a Discord channel")
        async def search_messages(channel_id: str, query: str, limit: int = 100):
            return await self.message_tools.search_messages(channel_id, query, limit)
        
        # Channel tools
        @self.tool(name="get_channel_info", description="Get information about a Discord channel")
        async def get_channel_info(channel_id: str):
            return await self.channel_tools.get_channel_info(channel_id)
        
        # Moderation tools
        @self.tool(name="moderate_content", description="Moderate content in a Discord channel")
        async def moderate_content(channel_id: str, message_id: str, action: str):
            return await self.moderation_tools.moderate_content(channel_id, message_id, action)

    async def authenticate_request(self, api_key: str) -> bool:
        """Authenticate incoming requests."""
        is_valid = self.auth.validate_key(api_key)
        if not is_valid:
            logger.warning(f"Invalid API key attempt")
        return is_valid

    async def initialize(self, protocol_version: str, capabilities: dict = None, client_info: dict = None):
        """Handle initialize request from the client."""
        logger.info(f"Initializing with protocol version: {protocol_version}")
        return {
            "serverInfo": {
                "name": "Discord MCP Server",
                "version": "1.0.0"
            },
            "capabilities": {}
        }

    async def start(self, discord_token: str, host: str = "localhost", port: int = 8000):
        """Start the MCP server and Discord bot."""
        try:
            # Start Discord bot
            logger.info("Starting Discord bot...")
            await self.discord_bot.start_bot(discord_token)
            
            # Start MCP server
            logger.info(f"Starting MCP server on {host}:{port}...")
            await self.run_http_async(host=host, port=port)
            
        except Exception as e:
            logger.error(f"Failed to start server: {e}")
            raise

    async def stop(self):
        """Stop the MCP server and Discord bot."""
        try:
            await self.discord_bot.stop_bot()
        except Exception as e:
            logger.error(f"Failed to stop server: {e}")
            raise 