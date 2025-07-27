# utils/personality.py

import yaml
from typing import Dict

class Personality:
	def __init__(self, name: str, system_prompt: str, description: str = "", metadata: dict = None):
		self.name = name
		self.system_prompt = system_prompt
		self.description = description
		self.metadata = metadata or {}

	def get_system_prompt(self) -> str:
		return self.system_prompt


class PersonalityManager:

	def __init__(self, yaml_filepath: str):
		self.yaml_filepath = yaml_filepath
		self.personalities: Dict[str, Personality] = {}
		self.load_personalities()

	def load_personalities(self):
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
			print(f"Error loading personalities: {e}")

	def get(self, name: str) -> Personality | None:
		return self.personalities.get(name)

	def reload(self):
		self.load_personalities()
