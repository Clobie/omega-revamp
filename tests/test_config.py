import unittest
import tempfile
from unittest import mock
import os
import sys
import yaml

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.config import Config

class TestConfig(unittest.TestCase):

	def setUp(self):
		# Create a temporary YAML config file
		self.config_data = {
			"token": "testtoken",
			"color": "0xFF5733",
			"env_var": "ENV"
		}
		self.temp_file = tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.yaml')
		yaml.dump(self.config_data, self.temp_file)
		self.temp_file.flush()
		self.temp_file.close()

		# Create mock logger
		self.mock_logger = mock.Mock()

		# Patch environment variable for ENV resolution
		self.env_patcher = mock.patch.dict(os.environ, {"ENV_VAR": "env_value"})
		self.env_patcher.start()

	def tearDown(self):
		os.unlink(self.temp_file.name)
		self.env_patcher.stop()

	def test_config_loading(self):
		cfg = Config(self.temp_file.name, logger=self.mock_logger)
		self.assertEqual(cfg.TOKEN, "testtoken")
		self.assertTrue(hasattr(cfg, "COLOR"))
		self.assertEqual(cfg.ENV_VAR, "env_value")

	def test_set_and_get_variable(self):
		cfg = Config(self.temp_file.name, logger=self.mock_logger)
		cfg.set_variable("custom_key", 1234)
		self.assertEqual(cfg.get_variable("custom_key"), 1234)
		self.assertTrue(cfg.variable_exists("custom_key"))

	def test_get_variable_default(self):
		cfg = Config(self.temp_file.name, logger=self.mock_logger)
		self.assertEqual(cfg.get_variable("nonexistent", "default"), "default")

	def test_get_all_variables(self):
		cfg = Config(self.temp_file.name, logger=self.mock_logger)
		vars = cfg.get_all_variables()
		self.assertIsInstance(vars, dict)
		self.assertIn("TOKEN", vars)
		self.assertEqual(vars["TOKEN"], "testtoken")

	@mock.patch("builtins.open", new_callable=mock.mock_open)
	def test_save_config(self, mock_open_file):
		cfg = Config(self.temp_file.name, logger=self.mock_logger)
		cfg.set_variable("newkey", "newval")
		cfg.save_config()
		mock_open_file.assert_any_call(cfg.config_path, 'w', encoding='utf-8')
		self.assertEqual(cfg.get_variable("newkey"), "newval")


if __name__ == "__main__":
	unittest.main()
