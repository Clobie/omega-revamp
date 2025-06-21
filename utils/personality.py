# utils/personality.py

import yaml
from typing import Dict

class Personality:
	"""
	Represents a single AI personality, including its system prompt,
	description, and optional metadata.

	Attributes:
		name (str): The unique name/identifier of the personality.
		system_prompt (str): The system prompt text defining the personality's behavior.
		description (str): A brief description of the personality.
		metadata (dict): Optional dictionary of additional personality attributes.
	"""

	def __init__(self, name: str, system_prompt: str, description: str = "", metadata: dict = None):
		"""
		Initialize a Personality instance.

		Args:
			name (str): Unique name for the personality.
			system_prompt (str): The system prompt text.
			description (str, optional): Description of the personality. Defaults to "".
			metadata (dict, optional): Additional metadata. Defaults to None.
		"""
		self.name = name
		self.system_prompt = system_prompt
		self.description = description
		self.metadata = metadata or {}

	def get_system_prompt(self) -> str:
		"""
		Retrieve the system prompt text of the personality.

		Returns:
			str: The system prompt string.
		"""
		return self.system_prompt


class PersonalityManager:
	"""
	Manages loading, storing, and retrieving multiple Personality instances from a YAML file.

	Attributes:
		yaml_filepath (str): Path to the YAML file containing personality definitions.
		personalities (Dict[str, Personality]): Dictionary mapping personality names to Personality instances.
	"""

	def __init__(self, yaml_filepath: str):
		"""
		Initialize the PersonalityManager and load personalities from the YAML file.

		Args:
			yaml_filepath (str): File path to the YAML personalities file.
		"""
		self.yaml_filepath = yaml_filepath
		self.personalities: Dict[str, Personality] = {}
		self.load_personalities()

	def load_personalities(self):
		"""
		Load personalities from the YAML file into the internal dictionary.

		Clears any previously loaded personalities before loading.
		Logs an error message on failure but does not raise.
		"""
		try:
			with open(self.yaml_filepath, "r", encoding="utf-8") as f:
				data = yaml.safe_load(f)
			self.personalities.clear()
			for name, details in data.items():
				self.personalities[name] = Personality(
					name=name,
					system_prompt=details.get("system_prompt", ""),
					description=details.get("description", ""),
					metadata=details.get("metadata", {})
				)
		except Exception as e:
			print(f"[PersonalityManager] Error loading personalities: {e}")

	def get(self, name: str) -> Personality | None:
		"""
		Retrieve a Personality instance by its name.

		Args:
			name (str): The name/key of the desired personality.

		Returns:
			Personality | None: The Personality instance if found, else None.
		"""
		return self.personalities.get(name)

	def reload(self):
		"""
		Reload personalities from the YAML file at runtime.

		Useful for hot-reloading personalities without restarting the app.
		"""
		self.load_personalities()
