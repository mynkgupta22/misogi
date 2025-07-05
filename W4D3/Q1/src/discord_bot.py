import discord
from discord.ext import commands
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DiscordBot:
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        
        self.bot = commands.Bot(command_prefix="!", intents=intents)
        self.setup_events()

    def setup_events(self):
        @self.bot.event
        async def on_ready():
            logger.info(f"Bot is ready as {self.bot.user}")

        @self.bot.event
        async def on_message(message):
            if message.author == self.bot.user:
                return
            logger.info(f"Message received: {message.content} from {message.author}")
            await self.bot.process_commands(message)

    async def start_bot(self, token):
        try:
            await self.bot.start(token)
        except Exception as e:
            logger.error(f"Failed to start bot: {e}")
            raise

    async def stop_bot(self):
        try:
            await self.bot.close()
        except Exception as e:
            logger.error(f"Failed to stop bot: {e}")
            raise 