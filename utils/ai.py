# utils/ai.py

from openai import OpenAI
import tiktoken
import requests
from utils.logger import Logger
from utils.personality import Personality
from utils.rag import Rag

class AI:

	_instance = None

	def __new__(cls, *args, **kwargs):
		if cls._instance is None:
			cls._instance = super().__new__(cls)
		return cls._instance

	def __init__(self):
		if hasattr(self, "_initialized") and self._initialized:
			return

		self.client = OpenAI()
		self.logger = Logger()
		self.rag = Rag()
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

	def openai_summarize_conversation(self, model: str, context: list) -> str:
		"""Summarize a conversation using OpenAI."""
		try:
			summary = self.client.chat.completions.create(
				model=model,
				messages=context + [{"role": "user", "content": "Please summarize our conversation with detail.  It will be used to update my user document (memory)."}]
			)
			response = summary.choices[0].message.content.strip()
			self.logger.debug(f"OpenAI summarize success (model={model}): {response}")
			return response
		except Exception as e:
			self.logger.error(f"OpenAI summarize error (model={model}): {e}\nContext: {context}")
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
		encoding = tiktoken.encoding_for_model(model)
		t_context = len(encoding.encode(context))
		t_result = len(encoding.encode(result))
		cost = ((cpm_context * t_context) + (cpm_result * t_result)) / 1_000_000.0
		return round(cost, 8)

	def count_tokens(model, text) -> int:
		encoding = tiktoken.encoding_for_model(model)
		return len(encoding.encode(text))

	def build_context(self, personality: Personality, rag_data: str = None, previous_context: list = []) -> list:
		"""
		Build the context for the chat completion request.

		Parameters:
			personality (Personality): The personality to use for the chat.
			rag_data (str): The RAG data to include in the context.
			previous_context (list): The previous context messages.

		Returns:
			list: The constructed context for the chat completion request.
		"""

		context = previous_context.copy()

		if context and context[0].get("role") == "system":
			context.pop(0)
		
		system_prompt = personality.get_system_prompt()

		if rag_data:
			system_prompt += f"\n\n{rag_data}"

		context.insert(0, {"role": "system", "content": system_prompt})

		return context
	
	def append_context(self, context: list, role: str, content: str) -> list:
		context.append({"role": role, "content": content})

		if not isinstance(role, str) or not isinstance(content, str):
			self.logger.error("Invalid role or content type in append_context")
			return None
		return context