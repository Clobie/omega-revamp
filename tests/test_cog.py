import unittest
from unittest import mock
import asyncio
import os
import json
import builtins

from utils.cog import CogLoader

class TestCogLoader(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        # Patch os.listdir to simulate cogs directory
        self.patcher_listdir = mock.patch('os.listdir', return_value=['testcog.py', 'anothercog.py'])
        self.mock_listdir = self.patcher_listdir.start()

        # Patch open to simulate config file reading/writing
        self.mock_open = mock.mock_open(read_data=json.dumps({'testcog': 'enabled'}))
        self.patcher_open = mock.patch('builtins.open', self.mock_open)
        self.patcher_open.start()

        # Patch os.path.exists to simulate config file presence
        self.patcher_exists = mock.patch('os.path.exists', return_value=True)
        self.patcher_exists.start()

        # Patch os.makedirs to do nothing
        self.patcher_makedirs = mock.patch('os.makedirs')
        self.patcher_makedirs.start()

        # Create CogLoader instance (singleton)
        self.cog_loader = CogLoader()

        # Create a mock bot with async mocks for extension methods
        self.mock_bot = mock.Mock()
        self.mock_bot.load_extension = mock.AsyncMock()
        self.mock_bot.unload_extension = mock.AsyncMock()
        self.mock_bot.reload_extension = mock.AsyncMock()

        # Patch logger methods to avoid actual logging output
        self.cog_loader.logger.info = mock.Mock()
        self.cog_loader.logger.error = mock.Mock()

    def tearDown(self):
        self.patcher_listdir.stop()
        self.patcher_open.stop()
        self.patcher_exists.stop()
        self.patcher_makedirs.stop()

    async def test_import_cogs_adds_new_cogs_to_config(self):
        # Initially 'anothercog' is not in config, should get added as enabled
        self.cog_loader.config = {'testcog': 'enabled'}
        self.cog_loader._import_cogs()

        self.assertIn('anothercog', self.cog_loader.config)
        self.assertEqual(self.cog_loader.config['anothercog'], 'enabled')

        # Check if save_config is called by checking if open was called for write
        self.mock_open.assert_called_with(self.cog_loader.config_path, 'w', encoding='utf-8')

    async def test_enable_cog_loads_and_updates_config(self):
        await self.cog_loader.enable_cog(self.mock_bot, 'testcog')

        self.mock_bot.load_extension.assert_awaited_with('cogs.testcog')
        self.assertEqual(self.cog_loader.config['testcog'], 'enabled')
        self.cog_loader.logger.info.assert_called_with('Enabled cog: cogs.testcog')

    async def test_disable_cog_unloads_and_updates_config(self):
        self.cog_loader.config['testcog'] = 'enabled'

        await self.cog_loader.disable_cog(self.mock_bot, 'testcog')

        self.mock_bot.unload_extension.assert_awaited_with('cogs.testcog')
        self.assertEqual(self.cog_loader.config['testcog'], 'disabled')
        self.cog_loader.logger.info.assert_called_with('Disabled cog: cogs.testcog')

    async def test_load_cogs_loads_only_enabled_cogs(self):
        self.cog_loader.config = {
            'testcog': 'enabled',
            'anothercog': 'disabled'
        }
        await self.cog_loader.load_cogs(self.mock_bot)

        self.mock_bot.load_extension.assert_awaited_once_with('cogs.testcog')
        self.cog_loader.logger.info.assert_called_with('Loaded cog: cogs.testcog')

    async def test_reload_cog_reloads_cog(self):
        await self.cog_loader.reload_cog(self.mock_bot, 'testcog')

        self.mock_bot.reload_extension.assert_awaited_with('cogs.testcog')
        self.cog_loader.logger.info.assert_called_with('Reloaded cog: cogs.testcog')

    async def test_load_config_fails_gracefully(self):
        # Patch open to raise JSONDecodeError
        with mock.patch('builtins.open', mock.mock_open()) as mock_file:
            mock_file.side_effect = json.JSONDecodeError("msg", "doc", 0)
            config = self.cog_loader._load_config()
            self.assertEqual(config, {})
            self.cog_loader.logger.error.assert_called()

    async def test_save_config_fails_gracefully(self):
        # Patch open to raise IOError on write
        with mock.patch('builtins.open', mock.mock_open()) as mock_file:
            mock_file.side_effect = IOError("fail")
            self.cog_loader.config = {'test': 'enabled'}
            self.cog_loader._save_config()
            self.cog_loader.logger.error.assert_called()

if __name__ == '__main__':
    unittest.main()
