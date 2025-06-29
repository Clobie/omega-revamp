import os
import yaml
import discord
from utils.logger import Logger

class Config:
	"""Singleton YAML configuration loader with ENV support, runtime access, and save capability."""

	_instance = None

	def __new__(cls, *args, **kwargs):
		if cls._instance is None:
			cls._instance = super().__new__(cls)
		return cls._instance

	def __init__(self, config=None, logger=None):
		if hasattr(self, "_initialized") and self._initialized:
			return

		self.config_path = config or './config/bot.yaml'
		self.logger = logger or Logger()
		self._missing_vars = set()

		try:
			self._load_config()
			self.logger.debug(f"Config initialized with path: {self.config_path}")
		except Exception as e:
			self.logger.error(f"Failed to initialize config: {e}")

		self._initialized = True

	def __getattribute__(self, name):
		try:
			value = object.__getattribute__(self, name)
			if name.isupper():
				object.__getattribute__(self, 'logger').debug(f"Accessed config variable: {name}")
			return value
		except AttributeError:
			logger = object.__getattribute__(self, 'logger')
			logger.error(f"Accessed missing config variable: {name}")

			missing_vars = object.__getattribute__(self, '_missing_vars')
			missing_vars.add(name)
			raise

	def _load_config(self):
		if not os.path.exists(self.config_path):
			self.logger.warning(f"Config file not found: {self.config_path}")
			return

		with open(self.config_path, 'r', encoding='utf-8') as f:
			raw = yaml.safe_load(f) or {}

		for key, value in raw.items():
			key_upper = key.upper()
			try:
				if value == 'ENV':
					env_value = os.getenv(key_upper)
					if env_value is None:
						self.logger.error(f"Environment variable {key_upper} not found.")
					else:
						self.logger.info(f"Environment variable {key_upper} loaded.")
						setattr(self, key_upper, env_value)
				elif isinstance(value, str) and value.startswith('0x') and len(value) == 8:
					try:
						setattr(self, key_upper, discord.Color(int(value, 16)))
					except Exception as e:
						self.logger.error(f"Failed to convert {key_upper} to Color: {e}")
				else:
					setattr(self, key_upper, value)
			except Exception as e:
				self.logger.error(f"Error setting config variable {key_upper}: {e}")

	def save_config(self):
		try:
			os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
			data = {k.lower(): v.value if isinstance(v, discord.Color) else v
					for k, v in vars(self).items() if k.isupper()}
			with open(self.config_path, 'w', encoding='utf-8') as f:
				yaml.dump(data, f, sort_keys=True, default_flow_style=False)
			self.logger.info(f"Config saved to: {self.config_path}")
		except Exception as e:
			self.logger.error(f"Error saving config: {e}")
			raise

	def set_variable(self, key, value):
		try:
			if not key.isidentifier():
				raise ValueError("Invalid key format.")
			if not isinstance(value, (str, int, float, bool, discord.Color)):
				raise ValueError("Invalid value type.")
			setattr(self, key.upper(), value)
			self.logger.info(f"Variable {key.upper()} set to: {value}")
			self.save_config()
		except Exception as e:
			self.logger.error(f"Error setting variable {key}: {e}")
			raise

	def get_variable(self, key, default=None):
		try:
			value = getattr(self, key.upper(), default)
			self.logger.debug(f"Retrieved {key.upper()}: {value}")
			return value
		except Exception as e:
			self.logger.error(f"Error retrieving variable {key}: {e}")
			return default

	def variable_exists(self, key):
		try:
			exists = hasattr(self, key.upper())
			self.logger.debug(f"Checked existence of {key.upper()}: {exists}")
			return exists
		except Exception as e:
			self.logger.error(f"Error checking existence of {key}: {e}")
			return False

	def get_all_variables(self):
		try:
			return {k: v for k, v in vars(self).items() if k.isupper()}
		except Exception as e:
			self.logger.error(f"Error getting all config variables: {e}")
			return {}

	def print_config(self):
		try:
			for k, v in self.get_all_variables().items():
				print(f"{k} = {v}")
		except Exception as e:
			self.logger.error(f"Error printing config: {e}")

	def get_missing_variables(self):
		return getattr(self, '_missing_vars', set())
