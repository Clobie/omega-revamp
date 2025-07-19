"""
Core module for initializing and running the Discord bot and its utilities.
"""

import discord
from discord.ext import commands
import asyncio
import weakref
from utils.logger import Logger
from utils.config import Config
from utils.common import Common
from utils.database import Database
from utils.cog import CogLoader
from utils.personality import PersonalityManager
from utils.ai import AI
from utils.giphy import Giphy
from utils.rag import Rag

class Core:
	"""
	Core class to initialize and run the Discord bot along with its utilities.
	"""

	def __init__(self, config_path: str, personalities_path: str, cogs_path: str, cogs_config_path: str):
		self.bot = None
		self.personalities_path = personalities_path
		self.config_path = config_path
		self.logger = Logger()
		self.db = None
		self.common = None
		self.cog_loader = None
		self.personalities = None
		self.config = None
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
			self.personalities = PersonalityManager(self.personalities_path)  # load personalities
			self.giphy = Giphy()
			self.ai = AI()
			self.rag = Rag()
			self.cog_loader = CogLoader()
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
			intents = discord.Intents.all()
			self.bot = commands.Bot(
				command_prefix=self.config.COMMAND_PREFIX,
				intents=intents
			)
			self.bot.remove_command("help")
			self.bot.core = weakref.proxy(self)

			return True
		
		except Exception as e:
			self.logger.error(f"Bot setup failed: {e}")
			return False

	async def load_cogs(self):
		"""
		Async method to load all enabled cogs using CogLoader.
		Parallelizes cog loading for faster startup.
		"""
		cog_names = await self.cog_loader.get_enabled_cogs()
		await asyncio.gather(
			*(self.cog_loader.load_cog(self.bot, cog_name) for cog_name in cog_names)
		)

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
			token = getattr(self.config, "DISCORD_BOT_TOKEN", None)
			if not token or not isinstance(token, str) or not token.strip():
				self.logger.error("No valid Discord bot token found. Exiting.")
				if self.bot is not None:
					await self.bot.close()
				return False
			await self.bot.start(token)
		except Exception as e:
			self.logger.error(f"Failed to start bot: {e}")
			try:
				if self.bot is not None:
					await self.bot.close()
			except Exception as close_err:
				self.logger.error(f"Failed to close bot gracefully: {close_err}")
			return False