import unittest
from unittest.mock import mock_open, patch
from utils.personality import PersonalityManager, Personality

class TestPersonalityManager(unittest.TestCase):
	def setUp(self):
		# Example mock YAML content as a Python dict (what yaml.safe_load returns)
		self.mock_yaml_data = {
			"friendly": {
				"system_prompt": "You are a friendly AI assistant.",
				"description": "A kind and helpful personality.",
				"metadata": {"mood": "happy"}
			},
			"serious": {
				"system_prompt": "You are a serious AI assistant.",
				"description": "A no-nonsense personality.",
				"metadata": {"mood": "stern"}
			}
		}

	@patch("builtins.open", new_callable=mock_open, read_data="dummy data")
	@patch("yaml.safe_load")
	def test_load_personalities_and_get(self, mock_safe_load, mock_file):
		# Mock yaml.safe_load to return our mock data dict
		mock_safe_load.return_value = self.mock_yaml_data
		
		pm = PersonalityManager("fake_path.yaml")
		
		# Test that personalities were loaded correctly
		self.assertIn("friendly", pm.personalities)
		self.assertIn("serious", pm.personalities)
		
		friendly = pm.get("friendly")
		self.assertIsInstance(friendly, Personality)
		self.assertEqual(friendly.system_prompt, "You are a friendly AI assistant.")
		self.assertEqual(friendly.description, "A kind and helpful personality.")
		self.assertEqual(friendly.metadata, {"mood": "happy"})

		serious = pm.get("serious")
		self.assertEqual(serious.system_prompt, "You are a serious AI assistant.")
		self.assertEqual(serious.metadata["mood"], "stern")

		# Test get returns None for unknown personality
		self.assertIsNone(pm.get("unknown"))

	@patch("builtins.open", new_callable=mock_open, read_data="dummy data")
	@patch("yaml.safe_load")
	def test_reload_calls_load(self, mock_safe_load, mock_file):
		mock_safe_load.return_value = self.mock_yaml_data
		pm = PersonalityManager("fake_path.yaml")
		with patch.object(pm, 'load_personalities') as mock_load:
			pm.reload()
			mock_load.assert_called_once()

if __name__ == "__main__":
	unittest.main()
