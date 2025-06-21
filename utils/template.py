import os
from utils.logger import Logger

class SingletonUtility:
	"""
	Singleton Utility base template.

	Usage:
		from utils.singleton_utility import SingletonUtility
		util = SingletonUtility()
		util.do_something()
	"""

	_instance = None

	def __new__(cls, *args, **kwargs):
		if cls._instance is None:
			cls._instance = super().__new__(cls)
		return cls._instance

	def __init__(self, some_param=None):
		if getattr(self, '_initialized', False):
			return
		
		# Initialize logger
		self.logger = Logger()

		# Initialize only once
		self.some_param = some_param
		# Add your initialization code here

		self._initialized = True

	def do_something(self, data):
		# Replace with your utility method
		self.logger.info(f"Doing something with {data}")
