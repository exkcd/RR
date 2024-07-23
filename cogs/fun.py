import discord
from discord.ext import commands

import aiohttp
import random


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
                await ctx.send(embed=discord.Embed().set_image(url=js[0]['url']))

    @commands.command()
    async def dog(self, ctx):
        """Gives a random dog."""
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.thedogapi.com/v1/images/search') as resp:
                if resp.status != 200:
                    await ctx.send('No cat found :(')

                js = await resp.json()
                await ctx.send(embed=discord.Embed().set_image(url=js[0]['url']))

    @commands.command()
    async def quote(self, ctx):
        """Grabs a random quote. Source: monkeytype.com"""

        async with aiohttp.ClientSession() as session:
            async with session.get('https://raw.githubusercontent.com/monkeytypegame/monkeytype/master/frontend/static/quotes/english.json') as resp:
                if resp.status != 200:
                    await print('No quote found :(')

                js = await resp.json(content_type='text/plain')

                async def format_quote():
                    
                    quote_source = f' - {js['quotes'][rq]['source']}'

                    quote_text = f'{js['quotes'][rq]['text']}'

                    embed = discord.Embed()

                    embed.add_field(name=quote_text, value=quote_source)

                    await ctx.send(embed=embed)

                rq = random.randint(0, len(js['quotes']))

                if js['quotes'][rq]['length'] < 256:
                    pass

                else:
                    rq = random.randint(0, len(js['quotes']))

                await format_quote()



    @commands.command()
    async def love(self, ctx):
        """what is love?"""

        responses = [
            'a symphony of deeply felt affection towards another self-aware being',
            'something we don\'t have',
            'https://www.youtube.com/watch?v=HEXWRTEbj1I',
            'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
        ]

        await ctx.send(random.choice(responses))

    @commands.command(hidden=True)
    async def bored(self, ctx):
        """boredom looms"""

        await ctx.send('http://i.imgur.com/BuTKSzf.png')

    @commands.command()
    async def feelsbad(self, ctx):
        """feelsbadman"""

        await ctx.send('https://tenor.com/view/lilo-and-stitch-stitch-rain-no-sad-gif-4029226')

    @commands.command()
    async def feelsgood(self, ctx):
        """feelsgoodman"""
        
        await ctx.send('https://media1.tenor.com/m/BvIvARKLrkQAAAAC/tobey-maguire-spiderman.gif')
async def setup(bot):
    await bot.add_cog(Fun(bot))
