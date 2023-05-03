# https://discordapi.com/permissions.html#395137058816
import os
import asyncio

import nextcord
from nextcord.ext import commands
from dotenv import load_dotenv
import openai
import tiktoken
from loguru import logger as log

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

intents = nextcord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True

bot = commands.Bot(intents=intents, help_command=None)

MAX_TOKENS = {
    "gpt-4": 8192,
    "gpt-3.5-turbo": 4096,
}

allowed_models = MAX_TOKENS.keys()

enc = tiktoken.get_encoding("cl100k_base")


def count_tokens(text: str):
    return len(enc.encode(text))


def req(messages: list[dict]) -> str | list[str]:
    resp = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=messages)
    if len(resp.choices) == 0:
        return "No response"
    return resp.choices[0]['message']['content']


@bot.event
async def on_ready():
    log.info(f"Logged in as {bot.user}")


@bot.event
async def on_message(message: nextcord.Message):
    if message.author == bot.user:
        return

    if message.channel.type == nextcord.ChannelType.public_thread or message.channel.type == nextcord.ChannelType.private_thread:
        # check if the bot is the one who started the thread
        if message.channel.owner != bot.user:
            return
        log.info(
            f'Received message in thread on {message.guild.name} ({message.guild.id})')
        await message.channel.trigger_typing()
        # get the name and remove the "Chat-" part
        model = message.channel.name[5:]
        # check if the model is allowed
        if model not in allowed_models:
            model = "gpt-3.5-turbo"
        # get the prompt from the user. Its the just sent message
        prompt = message.content
        tokens = count_tokens(prompt)
        # check if the prompt is too long
        if tokens > MAX_TOKENS[model]:
            await message.channel.send(f"Prompt is too long. Max tokens: {MAX_TOKENS[model]}")
            return
        thread_messages = []
        # get previous messages in the thread
        # if it was a user, add { 'role': 'user', 'content': message.content }
        # if it was the bot, add { 'role': 'assistant', 'content': message.content }
        # count the tokens first and check if it is too long
        async for msg in message.channel.history():
            if msg.author == bot.user:
                thread_messages.append(
                    {'role': 'assistant', 'content': msg.content})
            else:
                thread_messages.append(
                    {'role': 'user', 'content': msg.content})
        thread_messages.reverse()
        messages = [{"role": "user", "content": prompt}]
        for msg in thread_messages:
            msg_tokens = count_tokens(msg['content'])
            if msg_tokens + tokens > MAX_TOKENS[model]:
                break
            messages.append(msg)
            tokens += msg_tokens
        messages.reverse()
        response = req(messages)
        if len(response) > 2000:
            # split until the message is less than 2000 characters
            split = response.split("\n")
            responses = []
            current = ""
            for line in split:
                if len(current) + len(line) > 2000:
                    responses.append(current)
                    current = ""
                current += line + "\n"
            responses.append(current)
            for response in responses:
                await message.channel.send(response)
        else:
            await message.channel.send(response)


@bot.slash_command(
    name="chat",
    description="Chat with the AI model",
)
async def _chat(ctx: nextcord.Interaction, model: str | None = nextcord.SlashOption(name="model", description="The model to use", required=False, choices=allowed_models)):
    if model is None or model not in allowed_models:
        model = "gpt-3.5-turbo"

    log.info(
        f"Creating new thread for on {ctx.guild.name} ({ctx.guild.id})")
    # needs to make the initial request to chatgpt
    thread_name = f"Chat-{model}"
    await ctx.response.defer()
    thread = await ctx.channel.create_thread(name=thread_name, type=nextcord.ChannelType.public_thread)
    await thread.trigger_typing()
    await asyncio.sleep(1)
    await thread.send("Hello! I am Otto, your helpful ChatGPT assistant. How can I help you today?")
    await ctx.send(f"Chatting in {thread.mention}")


@bot.slash_command(
    name="delete",
    description="Delete the thread. Does nothing if the bot is not the owner or if not in a thread.",
)
async def _delete(ctx: nextcord.Interaction):
    if ctx.channel.type == nextcord.ChannelType.public_thread or ctx.channel.type == nextcord.ChannelType.private_thread:
        if ctx.channel.owner != bot.user:
            return
        await ctx.channel.delete()

bot.run(os.getenv("TOKEN"))
