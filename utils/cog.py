import os
import json
from utils.logger import Logger

CONFIG_PATH = './config/cogs.json'
COGS_DIR = './cogs'

class CogLoader:
	"""
	Singleton Cog Loader for managing Discord bot cogs.
	Loads cog config from JSON, auto-imports new cogs, and handles enabling,
	disabling, loading, and reloading of cogs for the bot.

	Usage:
		from utils.cog import CogLoader
		cog_loader = CogLoader()
		await cog_loader.load_cogs(bot)
	"""

	_instance = None

	def __new__(cls, *args, **kwargs):
		if cls._instance is None:
			cls._instance = super().__new__(cls)
		return cls._instance

	def __init__(self, config_path=CONFIG_PATH, cogs_dir=COGS_DIR, logger=None):
		"""
		Initialize the CogLoader singleton.

		Args:
			config_path (str): Path to cogs config JSON file.
			cogs_dir (str): Directory containing cog files.
			logger (Logger): Optional logger instance; will create one if None.
		"""
		if getattr(self, '_initialized', False):
			return

		self.config_path = config_path
		self.cogs_dir = cogs_dir
		self.logger = logger or Logger()

		self.config = self._load_config()
		self._import_cogs()
		self._initialized = True

	def _load_config(self):
		"""Load the cog configuration from JSON file or return empty dict."""
		if os.path.exists(self.config_path):
			try:
				with open(self.config_path, 'r', encoding='utf-8') as f:
					return json.load(f)
			except (json.JSONDecodeError, IOError) as e:
				self.logger.error(f"Failed to load config: {e}")
		return {}

	def _save_config(self):
		"""Save the current cog config to JSON file."""
		try:
			os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
			with open(self.config_path, 'w', encoding='utf-8') as f:
				json.dump(self.config, f, indent=4)
		except IOError as e:
			self.logger.error(f"Failed to save config: {e}")

	def _import_cogs(self):
		"""
		Scan the cogs directory and add new cog filenames (without .py) to config as 'enabled'.
		Save the updated config file.
		"""
		try:
			for filename in os.listdir(self.cogs_dir):
				if filename.endswith('.py'):
					cog_name = filename[:-3]
					if cog_name not in self.config:
						self.config[cog_name] = 'enabled'
						self.logger.info(f"Imported new cog '{cog_name}' to config.")
			self._save_config()
		except FileNotFoundError:
			self.logger.error(f"Cogs directory not found: {self.cogs_dir}")

	async def enable_cog(self, bot, cog_name):
		"""
		Enable (load) a cog by name.

		Args:
			bot (discord.Client or commands.Bot): The Discord bot instance.
			cog_name (str): The cog name without prefix.
		"""
		full_name = f"cogs.{cog_name}"
		try:
			await bot.load_extension(full_name)
			self.config[cog_name] = 'enabled'
			self._save_config()
			self.logger.info(f"Enabled cog: {full_name}")
		except Exception as e:
			self.logger.error(f"Failed to enable cog {full_name}: {e}")

	async def disable_cog(self, bot, cog_name):
		"""
		Disable (unload) a cog by name.

		Args:
			bot (discord.Client or commands.Bot): The Discord bot instance.
			cog_name (str): The cog name without prefix.
		"""
		full_name = f"cogs.{cog_name}"
		try:
			await bot.unload_extension(full_name)
			self.config[cog_name] = 'disabled'
			self._save_config()
			self.logger.info(f"Disabled cog: {full_name}")
		except Exception as e:
			self.logger.error(f"Failed to disable cog {full_name}: {e}")

	async def load_cogs(self, bot):
		"""
		Load all enabled cogs into the bot.

		Args:
			bot (discord.Client or commands.Bot): The Discord bot instance.
		"""
		enabled_cogs = [cog for cog, status in self.config.items() if status == 'enabled']
		try:
			for cog_name in enabled_cogs:
				full_name = f"cogs.{cog_name}"
				await bot.load_extension(full_name)
				self.logger.info(f"Loaded cog: {full_name}")
		except Exception as e:
			self.logger.error(f"Failed to load cog {full_name}: {e}")

	async def reload_cog(self, bot, cog_name):
		"""
		Reload a single cog.

		Args:
			bot (discord.Client or commands.Bot): The Discord bot instance.
			cog_name (str): The cog name without prefix.
		"""
		full_name = f"cogs.{cog_name}"
		try:
			await bot.reload_extension(full_name)
			self.logger.info(f"Reloaded cog: {full_name}")
		except Exception as e:
			self.logger.error(f"Failed to reload cog {full_name}: {e}")
