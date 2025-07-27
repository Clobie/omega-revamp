import os
import yaml
from utils.logger import Logger

CONFIG_PATH = './config/cogs.yaml'
COGS_DIR = './cogs'

class CogLoader:

	_instance = None

	def __new__(cls, *args, **kwargs):
		if cls._instance is None:
			cls._instance = super().__new__(cls)
		return cls._instance

	def __init__(self, config_path=CONFIG_PATH, cogs_dir=COGS_DIR, logger=None):
		if hasattr(self, "_initialized") and self._initialized:
			return

		self.config_path = config_path
		self.cogs_dir = cogs_dir
		self.logger = logger or Logger()

		self.config = self._load_config()
		self._import_cogs()
		self._initialized = True

	def _load_config(self):
		"""Load the cog configuration from YAML file or return empty dict."""
		if os.path.exists(self.config_path):
			try:
				with open(self.config_path, 'r', encoding='utf-8') as f:
					data = yaml.safe_load(f)
					return data if isinstance(data, dict) else {}
			except (yaml.YAMLError, IOError) as e:
				self.logger.error(f"Failed to load YAML config: {e}")
		return {}

	def _save_config(self):
		"""Save the current cog config to YAML file."""
		try:
			os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
			with open(self.config_path, 'w', encoding='utf-8') as f:
				yaml.dump(self.config, f, default_flow_style=False, sort_keys=True)
		except IOError as e:
			self.logger.error(f"Failed to save YAML config: {e}")

	def _import_cogs(self):
		"""Scan cogs directory and add new cogs as 'enabled' in the config."""
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
		full_name = f"cogs.{cog_name}"
		try:
			await bot.load_extension(full_name)
			self.config[cog_name] = 'enabled'
			self._save_config()
			self.logger.info(f"Enabled cog: {full_name}")
		except Exception as e:
			self.logger.error(f"Failed to enable cog {full_name}: {e}")

	async def disable_cog(self, bot, cog_name):
		full_name = f"cogs.{cog_name}"
		try:
			await bot.unload_extension(full_name)
			self.config[cog_name] = 'disabled'
			self._save_config()
			self.logger.info(f"Disabled cog: {full_name}")
		except Exception as e:
			self.logger.error(f"Failed to disable cog {full_name}: {e}")

	async def load_cogs(self, bot):
		enabled_cogs = [cog for cog, status in self.config.items() if status == 'enabled']
		try:
			for cog_name in enabled_cogs:
				full_name = f"cogs.{cog_name}"
				await bot.load_extension(full_name)
				self.logger.info(f"Loaded cog: {full_name}")
		except Exception as e:
			self.logger.error(f"Failed to load cog {full_name}: {e}")
	
	async def load_cog(self, bot, cog_name):
		full_name = f"cogs.{cog_name}"
		try:
			await bot.load_extension(full_name)
			self.config[cog_name] = 'enabled'
			self._save_config()
			self.logger.info(f"Loaded cog: {full_name}")
		except Exception as e:
			self.logger.error(f"Failed to load cog {full_name}: {e}")

	async def reload_cog(self, bot, cog_name):
		full_name = f"cogs.{cog_name}"
		try:
			await bot.reload_extension(full_name)
			self.logger.info(f"Reloaded cog: {full_name}")
		except Exception as e:
			self.logger.error(f"Failed to reload cog {full_name}: {e}")

	async def get_enabled_cogs(self):
		"""Return a list of enabled cogs."""
		return [cog for cog, status in self.config.items() if status == 'enabled']