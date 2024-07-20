import discord
from discord.ext import commands

import aiohttp


class Fun(commands.Cog, name="Fun"):
    """Some fun commands."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def cat(self, ctx):
        """Gives a random cat."""
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.thecatapi.com/v1/images/search') as resp:
                if resp.status != 200:
                    await ctx.send('No cat found :(')

                js = await resp.json()
                await ctx.send(embed=discord.Embed(colour=discord.Colour.blurple()).set_image(url=js[0]['url']))

    @commands.command()
    async def dog(self, ctx):
        """Gives a random dog."""
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.thedogapi.com/v1/images/search') as resp:
                if resp.status != 200:
                    await ctx.send('No cat found :(')

                js = await resp.json()
                await ctx.send(embed=discord.Embed(colour=discord.Colour.blurple()).set_image(url=js[0]['url']))


async def setup(bot):
    await bot.add_cog(Fun(bot))
