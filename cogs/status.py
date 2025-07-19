# cogs/template_simple.py

import discord
from discord.ext import commands, tasks
import os

class Status(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
	
	@commands.Cog.listener()
	async def on_ready(self):
		await self.bot.change_presence(activity=discord.Game(name="with cogs"))
		self.bot.core.logger.info(f"Logged in as {self.bot.user}!")

async def setup(bot: commands.Bot):
	cog = Status(bot)
	await bot.add_cog(cog)
