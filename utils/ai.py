# utils/ai.py

from openai import OpenAI
import tiktoken
import requests
from utils.logger import Logger

class AI:
	"""Singleton wrapper for OpenAI and Ollama chat completions."""

	_instance = None

	def __new__(cls, *args, **kwargs):
		"""Ensure only one instance of AI exists."""
		if cls._instance is None:
			cls._instance = super().__new__(cls)
		return cls._instance

	def __init__(self):
		"""Initialize OpenAI client and logger (once)."""
		if hasattr(self, "_initialized") and self._initialized:
			return

		self.client = OpenAI()
		self.logger = Logger()
		self.ollama_url = "http://localhost:11434/api/chat"
		self._initialized = True

	def openai_chat_completion(self, model: str, system_prompt: str, user_prompt: str) -> str:
		try:
			completion = self.client.chat.completions.create(
				model=model,
				messages=[
					{"role": "system", "content": system_prompt},
					{"role": "user", "content": user_prompt}
				]
			)
			response = completion.choices[0].message.content
			# Safe strip: only if it exists and callable
			if hasattr(response, "strip") and callable(response.strip):
				response = response.strip()
			return response
		except Exception as e:
			self.logger.error(f"OpenAI completion error (model={model}): {e}")
			return f"Error: {str(e)}"


	def openai_chat_completion_with_context(self, model: str, context: list) -> str:
		"""Get OpenAI response from full conversation context."""
		try:
			completion = self.client.chat.completions.create(model=model, messages=context)
			response = completion.choices[0].message.content.strip()
			self.logger.debug(f"OpenAI completion with context success (model={model}): {response}")
			return response
		except Exception as e:
			self.logger.error(f"Chat completion context error (model={model}): {e}\nContext: {context}")
			return f"Error: {str(e)}"

	def ollama_chat_completion(self, model: str, system_prompt: str, user_prompt: str) -> str:
		"""Get Ollama response from system and user prompt."""
		payload = {
			"model": model,
			"messages": [
				{"role": "system", "content": system_prompt},
				{"role": "user", "content": user_prompt}
			]
		}
		try:
			resp = requests.post(self.ollama_url, json=payload)
			resp.raise_for_status()
			data = resp.json()
			response = data["message"]["content"].strip()
			self.logger.debug(f"Ollama completion success (model={model}): {response}")
			return response
		except Exception as e:
			self.logger.error(f"Ollama completion error (model={model}): {e}")
			return f"Error: {str(e)}"

	def ollama_chat_completion_with_context(self, model: str, context: list) -> str:
		"""Get Ollama response from full conversation context."""
		payload = {
			"model": model,
			"messages": context
		}
		try:
			resp = requests.post(self.ollama_url, json=payload)
			resp.raise_for_status()
			data = resp.json()
			response = data["message"]["content"].strip()
			self.logger.debug(f"Ollama completion with context success (model={model}): {response}")
			return response
		except Exception as e:
			self.logger.error(f"Ollama chat context error (model={model}): {e}\nContext: {context}")
			return f"Error: {str(e)}"

	def tokens_to_usd(model, context, result, cpm_context, cpm_result) -> float:
		"""
		Calculate cost in USD for tokens consumed by a given model.

		Parameters:
			model (str): Model name for tokenizer (e.g., "gpt-4", "gpt-3.5-turbo").
			context (str): Input text to encode (prompt tokens).
			result (str): Output text to encode (completion tokens).
			cpm_context (float): Cost per million tokens for context tokens.
			cpm_result (float): Cost per million tokens for result tokens.

		Returns:
			float: Estimated cost in USD rounded to 8 decimal places.
		"""
		encoding = tiktoken.encoding_for_model(model)
		t_context = len(encoding.encode(context))
		t_result = len(encoding.encode(result))
		cost = ((cpm_context * t_context) + (cpm_result * t_result)) / 1_000_000.0
		return round(cost, 8)

	def count_tokens(model, text) -> int:
		"""
		Count the number of tokens in a given text for a specific model.

		Parameters:
			model (str): Model name for tokenizer.
			text (str): Text to tokenize.

		Returns:
			int: Number of tokens.
		"""
		encoding = tiktoken.encoding_for_model(model)
		return len(encoding.encode(text))
