import tempfile
import configparser
import pytest
from unittest import mock
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.config import Config

@pytest.fixture
def temp_config_file():
	with tempfile.NamedTemporaryFile(mode='w+', delete=False) as f:
		f.write("[general]\ntoken = testtoken\ncolor = 0xFF5733\nenv_var = ENV\n")
		f.flush()
		yield f.name
	os.unlink(f.name)

@mock.patch.dict(os.environ, {"ENV_VAR": "env_value"})
def test_config_loading(temp_config_file):
	cfg = Config(temp_config_file)
	assert cfg.TOKEN == "testtoken"
	assert isinstance(cfg.COLOR, object)
	assert cfg.ENV_VAR == "env_value"

def test_set_and_get_variable(temp_config_file):
	cfg = Config(temp_config_file)
	cfg.set_variable("custom_key", 1234)
	assert cfg.get_variable("custom_key") == 1234
	assert cfg.variable_exists("custom_key")

def test_get_variable_default(temp_config_file):
	cfg = Config(temp_config_file)
	assert cfg.get_variable("nonexistent", "default") == "default"

def test_get_all_variables(temp_config_file):
	cfg = Config(temp_config_file)
	vars = cfg.get_all_variables()
	assert isinstance(vars, dict)
	assert "TOKEN" in vars

@mock.patch("builtins.open", new_callable=mock.mock_open)
def test_save_config(mock_open_file, temp_config_file):
	cfg = Config(temp_config_file)
	cfg.set_variable("newkey", "newval")
	cfg.save_config()
	mock_open_file.assert_called_with(temp_config_file, 'w')
	assert cfg.get_variable("newkey") == "newval"
