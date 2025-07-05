import asyncio
import os
from dotenv import load_dotenv
from src.main import DiscordMCPServer
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    # Load environment variables
    load_dotenv()
    
    # Get Discord bot token from environment
    discord_token = os.getenv("DISCORD_BOT_TOKEN")
    if not discord_token:
        raise ValueError("DISCORD_BOT_TOKEN environment variable is required")
    
    # Create and start the server
    server = DiscordMCPServer()
    try:
        await server.start(
            discord_token=discord_token,
            host=os.getenv("HOST", "localhost"),
            port=int(os.getenv("PORT", "8000"))
        )
    except KeyboardInterrupt:
        logger.info("Shutting down server...")
        await server.stop()
    except Exception as e:
        logger.error(f"Server error: {e}")
        await server.stop()
        raise

if __name__ == "__main__":
    asyncio.run(main()) 