# source env/bin/activate

import discord
from discord.ext import commands

import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')

intents = discord.Intents(
    guilds=True,
    messages=True,
    message_content=True,
    reactions=True
)

description = 'A personal discord bot.'
prefix = commands.when_mentioned_or('?')

initial_extensions = (
    'cogs.admin',
    'cogs.fun',
    'cogs.meta',
    'cogs.rng'
)

bot = commands.Bot(command_prefix=prefix,
                   description=description, intents=intents)


async def load_extensions():
    for extension in initial_extensions:
        try:
            await bot.load_extension(extension)
            print(f'Loaded {extension}')
        except Exception as e:
            print(f'Could not load {extension}\nError: {e}')


@bot.event
async def on_ready():
    await load_extensions()
    print(f'Logged in as: {bot.user} (ID: {bot.user.id})')
    print('-------')

bot.run(TOKEN)
