# core/omega.py

import discord
from discord.ext import commands

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.log import Logger
#from utils.cog import Cog
from utils.config import Config
#from utils.status import Status
from utils.common import Common
#from utils.credit import Credit
#from utils.role import Role
from utils.database import Database
#from utils.ai import AI
#from utils.embed import Embed
#from utils.giphy import Giphy

CONFIG_PATH = "./config/bot.conf"

class Omega:
    def __init__(self):
        pass
    
    def load_utils(self):

        try:
            self.logger = Logger()
        except Exception as e:
            print(f"Error loading logger: {e}")
            return False

        try:
            self.cfg = Config(CONFIG_PATH, self.logger)
        except Exception as e:
            print(f"Error loading config: {e}")
            self.cfg = None
            return False

        try:
            self.db = Database(self.cfg, self.logger)
        except Exception as e:
            print(f"Error initializing database: {e}")
            self.db = None

        try:
            self.common = Common()
        except Exception as e:
            print(f"Error loading common utilities: {e}")
            self.common = None


    def setup_bot(self):
        intents = discord.Intents.default()
        intents.message_content = True
        self.bot = commands.Bot(command_prefix=self.cfg.COMMAND_PREFIX, intents=intents)
        self.bot.remove_command("help")
        self.bot.config = self.cfg
        self.bot.omega = self
    
    def load_cogs(self):
        pass

    async def run(self):
        if not self.load_utils():
            print("Failed to load utilities. Exiting.")
            return
        #self.setup_bot()
        #self.load_cogs()
        #self.bot.run(self.cfg.TOKEN)