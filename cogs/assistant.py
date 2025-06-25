# cogs/template_simple.py

import discord
from discord.ext import commands, tasks
import os

class TemplateSimple(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
		self.logger = self.bot.core.logger
		self.config = self.bot.core.config
		self.ai = self.bot.core.ai
	
async def setup(bot: commands.Bot):
	cog = TemplateSimple(bot)
	await bot.add_cog(cog)