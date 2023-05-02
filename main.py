import os
import asyncio

import nextcord
from nextcord.ext import commands
from dotenv import load_dotenv

load_dotenv()

intents = nextcord.Intents.default()
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

allowed_models = ['gpt-4', 'gpt-3.5-turbo']


@bot.slash_command(
    name="chat",
    description="Chat with the AI model",
)
async def _chat(ctx: nextcord.Interaction, model: str | None = nextcord.SlashOption(name="model", description="The model to use", required=False, choices=allowed_models)):
    if model is None or model not in allowed_models:
        model = "gpt-3.5-turbo"

    thread_name = f"Chat-{model}"
    thread = await ctx.channel.create_thread(name=thread_name)
    await ctx.send(f"Created a new thread: {thread_name}")
    await thread.trigger_typing()
    await asyncio.sleep(1)
    await thread.send(f"Chatting with {model}")

bot.run(os.getenv("TOKEN"))
