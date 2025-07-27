# utils/encoder.py

import binascii
import base64
from utils.logger import Logger


class Encoder:

	_instance = None

	def __new__(cls, *args, **kwargs):
		if cls._instance is None:
			cls._instance = super().__new__(cls)
		return cls._instance

	def __init__(self):
		if hasattr(self, "_initialized") and self._initialized:
			return

		self.logger = Logger()
		self._initialized = True

	def encode_hex(self, data: str) -> str:
		self.logger.info("Encoding data to hex")
		return binascii.hexlify(data.encode()).decode()

	def decode_hex(self, data: str) -> str:
		self.logger.info("Decoding data from hex")
		try:
			return binascii.unhexlify(data.encode()).decode()
		except (binascii.Error, UnicodeDecodeError) as e:
			self.logger.error(f"Hex decoding error: {e}")
			raise ValueError(f"Error decoding hex: {e}")

	def encode_base64(self, data: str) -> str:
		self.logger.info("Encoding data to base64")
		return base64.b64encode(data.encode()).decode()

	def decode_base64(self, data: str) -> str:
		self.logger.info("Decoding data from base64")
		try:
			return base64.b64decode(data.encode()).decode()
		except (binascii.Error, UnicodeDecodeError) as e:
			self.logger.error(f"Base64 decoding error: {e}")
			raise ValueError(f"Error decoding base64: {e}")
