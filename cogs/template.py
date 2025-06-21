# cogs/template_simple.py

import discord
from discord.ext import commands, tasks
import os

class TemplateSimple(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
		self.logger = self.bot.core.logger

	@commands.command(name='test')
	async def test_command(self, ctx: commands.Context):
		"""A simple test command."""
		await ctx.send("This is a test command!")
	
	@commands.Cog.listener()
	async def on_ready(self):
		self.logger.info(f"{self.bot.user.name} is online.")
		await self.bot.change_presence(activity=discord.Game(name="Template Bot"))
	
	@commands.Cog.listener()
	async def on_command(self, ctx: commands.Context):
		self.logger.info(f"Command '{ctx.command}' invoked by {ctx.author} in {ctx.channel} in {ctx.guild} server.")
	
async def setup(bot: commands.Bot):
	cog = TemplateSimple(bot)
	await bot.add_cog(cog)