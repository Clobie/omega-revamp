# utils/giphy.py

import random
import requests
from utils.ai import AI
from utils.config import Config
from utils.logger import Logger

class Giphy:
	"""
	Singleton utility class for retrieving reaction GIF URLs from the Giphy API
	based on a concise search string generated from analyzing input text.

	The class uses an AI completion to generate relevant search keywords,
	queries the Giphy API for GIFs matching those keywords, and returns a GIF URL.

	Attributes:
		respond_chance (int): Chance (percentage) to respond with a GIF (default: 10).
		api_url (str): Base URL for Giphy search API.
		logger (Logger): Logger instance for logging info and errors.
	"""

	_instance = None

	def __new__(cls, *args, **kwargs):
		if cls._instance is None:
			cls._instance = super().__new__(cls)
		return cls._instance

	def __init__(self):
		"""
		Initialize the Giphy singleton utility.
		Ensures logger and API settings are initialized only once.
		"""
		if getattr(self, '_initialized', False):
			return

		self.logger = Logger()
		self.ai = AI()
		self.cfg = Config()
		self.api_url = "https://api.giphy.com/v1/gifs/search"
		self._initialized = True

	async def get_react_gif_url(self, message: str) -> str | None:
		"""
		Analyze a message to generate a relevant search string for a reaction GIF,
		query the Giphy API with that string, and return a GIF URL if available.

		Args:
			message (str): The input text message to analyze for GIF reaction.

		Returns:
			str | None: URL of a relevant reaction GIF, or None if none found or on error.
		"""
		try:
			search_string = self.ai.openai_chat_completion(
				'gpt-4.1-mini',
				(
					'Analyze the text and suggest a concise search string for finding a relevant REACTION GIF. '
					'Your search string should be short and relevant. For example: '
					'If a user says something sus like "I put 5 markers in my butt" then the search string could be "sus", "sharpies", "gross". '
					'If a user says something funny, the search string could be something like "laughing". '
					'If a user says "where is everyone?" the search string could be "john travolta" because of the popular gif. '
					'When possible, try to use known, popular or funny search strings to find the best response.'
				),
				message
			)
			params = {
				"api_key": self.cfg.GIPHY_API_KEY,
				"q": search_string,
				"limit": 25,
				"offset": random.randint(0, 24),
				"rating": "r",
				"lang": "en",
				"bundle": "messaging_non_clips"
			}
			response = requests.get(self.api_url, params=params)
			response.raise_for_status()
			data = response.json()
			if data.get('data'):
				react_gif_url = data['data'][0].get('url')
				self.logger.info(f"Found GIF URL: {react_gif_url} for search '{search_string}'")
				return react_gif_url
			else:
				self.logger.warning(f"No GIFs found for search '{search_string}'")
		except Exception as e:
			self.logger.error(f"Error getting reaction GIF: {e}")
		return None

gfy = Giphy()
