# core/core.py

import discord
from discord.ext import commands
from utils.logger import Logger
from utils.config import Config
from utils.common import Common
from utils.database import Database
from utils.token import Token
from utils.cog import CogLoader
from utils.personality import PersonalityManager  # import PersonalityManager
from utils.ai import AI
from utils.giphy import Giphy
from utils.rag import Rag

class Core:
	"""
	Core class to initialize and run the Discord bot along with its utilities.
	"""

	def __init__(self, config_path: str, personalities_path: str = "./config/personalities.yaml"):
		self.logger = None
		self.db = None
		self.common = None
		self.token = None
		self.bot = None
		self.cog_loader = None
		self.personalities_path = personalities_path
		self.personalities = None
		self.config_path = config_path
		self.config = None
		self.logger = Logger()
		self.ai = None
		self.giphy = None
		self.rag = None

	def load_utils(self) -> bool:
		"""
		Initialize and validate all utility singletons with required dependencies.

		Returns:
			bool: True if all utils initialized successfully, False otherwise.
		"""

		try:
			self.config = Config(self.config_path)
			self.db = Database(self.config)
			self.common = Common()
			self.token = Token()
			self.personalities = PersonalityManager(self.personalities_path)  # load personalities
			self.ai = AI()
			self.rag = Rag()
			return True
		except Exception as e:
			self.logger.error(f"Utility initialization failed: {e}")
			return False

	def setup_bot(self) -> bool:
		"""
		Set up the Discord bot with intents and command prefix.

		Returns:
			bool: True if setup succeeded.
		"""
		try:
			intents = discord.Intents.default()
			intents.message_content = True
			self.bot = commands.Bot(
				command_prefix=self.config.COMMAND_PREFIX,
				intents=intents
			)
			self.bot.remove_command("help")
			self.bot.core = self
			return True
		except Exception as e:
			self.logger.error(f"Bot setup failed: {e}")
			return False

	async def load_cogs(self):
		"""
		Async method to load all enabled cogs using CogLoader.
		"""
		self.cog_loader = CogLoader()
		await self.cog_loader.load_cogs(self.bot)

	async def run(self):
		"""
		Main entrypoint to run the bot.
		"""

		try:
			self.logger.info("Loading utilities...")
			if not self.load_utils():
				self.logger.error("Exiting due to utility load failure.")
				return False
		except Exception as e:
			self.logger.error(f"Exception during utility loading: {e}")
			return False

		try:
			self.logger.info("Setting up bot...")
			if not self.setup_bot():
				self.logger.error("Exiting due to bot setup failure.")
				return False
		except Exception as e:
			self.logger.error(f"Exception during bot setup: {e}")
			return False

		try:
			self.logger.info("Loading cogs...")
			await self.load_cogs()
		except Exception as e:
			self.logger.error(f"Exception during cog loading: {e}")
			return False

		try:
			self.logger.info("Starting bot...")
			await self.bot.start(self.config.DISCORD_BOT_TOKEN)
			self.logger.info("Bot started successfully.")
		except Exception as e:
			self.logger.error(f"Failed to start bot: {e}")
			try:
				await self.bot.close()
			except Exception as close_err:
				self.logger.error(f"Failed to close bot gracefully: {close_err}")
			return False
