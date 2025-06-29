# cogs/template_simple.py

import discord
from discord.ext import commands, tasks
import os

class TemplateSimple(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
		self.logger = self.bot.core.logger
		self.db = self.bot.core.db
		self.ai = self.bot.core.ai
		self.cog_loader = self.bot.core.cog_loader
		self.config = self.bot.core.config
		self.giphy = self.bot.core.giphy
		self.personality_manager = self.bot.core.personality_manager
		self.rag = self.bot.core.rag
		self.token = self.bot.core.token

	@commands.command(name='example')
	async def example(self, ctx: commands.Context):
		"""Example command demonstrating all utils."""

		return # we don't actually want to run this command.  it's an example.

		count = self.token.count_tokens("gpt-4", "Hello world")  # Count tokens in a sample text for a model
		cost = self.token.tokens_to_usd("gpt-4", "Hello world", "Hi there", 0.03, 0.06)  # Estimate cost for tokens

		self.rag.add_document("This is a sample document text.", doc_id="doc1")  # Add a document to RAG
		results = self.rag.query_top_documents("sample query", top_k=3)  # Query top relevant documents

		personality = self.personality_manager.get("friendly_assistant")  # Retrieve a personality by name
		gif_url = await self.giphy.get_react_gif_url("That's hilarious!")  # Get a relevant reaction GIF URL

		result = self.db.run_script("SELECT * FROM users WHERE id = %s", (123,))  # Run SQL query with parameters

		await self.cog_loader.enable_cog(self.bot, "example_cog")  # Enable a cog by name

		response = self.ai.openai_chat_completion("gpt-4", "System prompt here", "User prompt here")  # OpenAI chat completion
		context = [
			{"role": "system", "content": "You are helpful."},
			{"role": "user", "content": "Hello, who won the game?"}
		]
		response_ctx = self.ai.openai_chat_completion_with_context("gpt-4", context)  # OpenAI chat with context

		ollama_response = self.ai.ollama_chat_completion("ollama-model", "System prompt", "User prompt")  # Ollama chat completion
		ollama_response_ctx = self.ai.ollama_chat_completion_with_context("ollama-model", context)  # Ollama chat with context

		api_key = self.config.get_variable("GIPHY_API_KEY")  # Access a config variable
		self.config.set_variable("NEW_SETTING", "value")  # Set a config variable and save
		exists = self.config.variable_exists("NEW_SETTING")  # Check if config variable exists
		self.config.print_config()  # Print all config variables
		missing = self.config.get_missing_variables()  # Retrieve missing config variables

		self.logger.info("This is an info log message.")  # Log an info message

		self.rag.delete_document_by_id("doc1")  # Delete a document by ID
		self.rag.remove_duplicate_documents()  # Remove duplicate documents
		doc_text = self.rag.get_document_by_id("doc1")  # Get document text by ID

		await ctx.send("Example command executed. Check logs and variables for outputs.")  # Send confirmation message

	@commands.Cog.listener()
	async def on_ready(self):
		# we don't actually want to run this command.  it's an example.
		self.logger.info(f"{self.bot.user.name} is online.")
		await self.bot.change_presence(activity=discord.Game(name="Template Bot"))

	@commands.Cog.listener()
	async def on_command(self, ctx: commands.Context):
		return  # we don't actually want to run this command.  it's an example.
		self.logger.info(f"Command '{ctx.command}' invoked by {ctx.author} in {ctx.channel} in {ctx.guild} server.")

async def setup(bot: commands.Bot):
	cog = TemplateSimple(bot)
	await bot.add_cog(cog)
