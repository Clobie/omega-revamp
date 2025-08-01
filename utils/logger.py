# utils/logger.py

import logging
import os

class Logger:

	_instance = None

	def __new__(cls, *args, **kwargs):
		if cls._instance is None:
			cls._instance = super().__new__(cls)
		return cls._instance

	def __init__(self, log_dir='./logs'):
		if hasattr(self, "_initialized") and self._initialized:
			return

		self.logger = logging.getLogger("app_logger")
		self.logger.setLevel(logging.DEBUG)

		if not self.logger.handlers:
			os.makedirs(log_dir, exist_ok=True)

			# Create and add file handlers
			self.logger.addHandler(self._create_handler(logging.DEBUG, os.path.join(log_dir, 'debug.log')))
			self.logger.addHandler(self._create_handler(logging.INFO, os.path.join(log_dir, 'info.log')))
			self.logger.addHandler(self._create_handler(logging.WARNING, os.path.join(log_dir, 'warning.log')))
			self.logger.addHandler(self._create_handler(logging.ERROR, os.path.join(log_dir, 'error.log')))

			# Create and add console handler with formatter
			console_handler = logging.StreamHandler()
			console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - [%(filename)s] %(message)s'))
			self.logger.addHandler(console_handler)

			self.logger.info("Logger initialized.")

		self._initialized = True

	def _create_handler(self, level, filepath):
		handler = logging.FileHandler(filepath, 'a', 'utf-8')
		handler.setLevel(level)
		handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - [%(filename)s] %(message)s'))
		return handler

	def debug(self, msg):
		self.logger.debug(msg, stacklevel=2)

	def info(self, msg):
		self.logger.info(msg, stacklevel=2)

	def warning(self, msg):
		self.logger.warning(msg, stacklevel=2)

	def error(self, msg):
		self.logger.error(msg, stacklevel=2)

	def critical(self, msg):
		self.logger.critical(msg, stacklevel=2)
