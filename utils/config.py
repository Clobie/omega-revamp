import configparser
import os
import discord
from utils.logger import Logger

class Config:
	"""Singleton configuration loader with ENV support, runtime access, and save capability."""

	_instance = None

	def __new__(cls, *args, **kwargs):
		"""Ensure only one Config instance exists."""
		if cls._instance is None:
			cls._instance = super().__new__(cls)
		return cls._instance

	def __init__(self, config=None, logger=None):
		"""Initialize Config instance and load configuration from file."""
		if hasattr(self, "_initialized") and self._initialized:
			return

		self.config_path = config
		self.logger = Logger()
		self._missing_vars = set()
		try:
			self._load_config()
			if self.logger:
				self.logger.debug(f"Config initialized with path: {self.config_path}")
		except Exception as e:
			if self.logger:
				self.logger.error(f"Failed to initialize config: {e}")
		self._initialized = True

	def __getattribute__(self, name):
		try:
			value = object.__getattribute__(self, name)  # avoid recursion by bypassing __getattribute__
			if name.isupper():
				try:
					logger = object.__getattribute__(self, 'logger')
					if logger:
						logger.info(f"Accessed config variable: {name}")
				except AttributeError:
					pass
			return value
		except AttributeError:
			try:
				logger = object.__getattribute__(self, 'logger')
				if logger:
					logger.error(f"Accessed missing config variable: {name}")
			except AttributeError:
				pass
			# Track missing variables internally
			try:
				missing_vars = object.__getattribute__(self, '_missing_vars')
			except AttributeError:
				missing_vars = set()
				object.__setattr__(self, '_missing_vars', missing_vars)
			missing_vars.add(name)
			raise


	def _load_config(self):
		"""Load configuration from INI file and apply ENV overrides or hex color conversions."""
		config = configparser.ConfigParser()
		try:
			config.read(self.config_path)
		except Exception as e:
			if self.logger:
				self.logger.error(f"Failed to read config file {self.config_path}: {e}")
			return

		for section in config.sections():
			for key, value in config[section].items():
				key_upper = key.upper()
				try:
					if value == 'ENV':
						env_value = os.getenv(key_upper)
						if env_value is None:
							if self.logger:
								self.logger.error(f"Environment variable {key_upper} not found.")
						else:
							if self.logger:
								self.logger.info(f"Environment variable {key_upper} found.")
							setattr(self, key_upper, env_value)
					else:
						if value.startswith('0x') and len(value) == 8:
							try:
								value = discord.Color(int(value, 16))
							except Exception as e:
								if self.logger:
									self.logger.error(f"Error converting {key_upper} value '{value}' to discord.Color: {e}")
						setattr(self, key_upper, value)
				except Exception as e:
					if self.logger:
						self.logger.error(f"Error setting attribute {key_upper}: {e}")

	def save_config(self):
		"""Write current config variables to the config file."""
		try:
			config = configparser.ConfigParser()
			config['DEFAULT'] = {k.lower(): str(v) for k, v in vars(self).items() if k.isupper()}
			with open(self.config_path, 'w') as configfile:
				config.write(configfile)
			if self.logger:
				self.logger.info(f"Config saved to path: {self.config_path}")
		except Exception as e:
			if self.logger:
				self.logger.error(f"Error saving config: {e}")
			raise

	def set_variable(self, key, value):
		"""Set a config variable and save the config file."""
		try:
			if not key.isidentifier():
				raise ValueError("Invalid key format.")
			if not isinstance(value, (str, int, float, bool)):
				raise ValueError("Invalid value type.")
			setattr(self, key.upper(), value)
			if self.logger:
				self.logger.info(f"Variable {key.upper()} set with value: {value}")
			self.save_config()
		except Exception as e:
			if self.logger:
				self.logger.error(f"Error setting variable {key}: {e}")
			raise

	def get_variable(self, key, default=None):
		"""Return value of config variable, or default if not found."""
		try:
			value = getattr(self, key.upper(), default)
			if self.logger:
				self.logger.debug(f"Retrieved variable {key.upper()}: {value}")
			return value
		except Exception as e:
			if self.logger:
				self.logger.error(f"Error retrieving variable {key}: {e}")
			return default

	def variable_exists(self, key):
		"""Return True if config variable exists."""
		try:
			exists = hasattr(self, key.upper())
			if self.logger:
				self.logger.debug(f"Variable exists check for {key.upper()}: {exists}")
			return exists
		except Exception as e:
			if self.logger:
				self.logger.error(f"Error checking existence of variable {key}: {e}")
			return False

	def get_all_variables(self):
		"""Return dict of all config variables."""
		try:
			return {k: v for k, v in vars(self).items() if k.isupper()}
		except Exception as e:
			if self.logger:
				self.logger.error(f"Error getting all variables: {e}")
			return {}

	def print_config(self):
		"""Print all config variables to console."""
		try:
			for key, value in self.get_all_variables().items():
				print(f"{key} = {value}")
		except Exception as e:
			if self.logger:
				self.logger.error(f"Error printing config: {e}")

	def get_missing_variables(self):
		"""Return a set of all accessed but missing config variables."""
		return getattr(self, '_missing_vars', set())
