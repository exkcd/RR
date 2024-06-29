import discord
from discord.ext import commands


class Meta(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        """Pings the bot."""
        await ctx.send('Pong.')
    
    @commands.command(name='quit', hidden=True)
    @commands.is_owner()
    async def _quit(self, ctx):
        """Quits the bot."""
        await ctx.send('Goodbye.')
        await self.bot.close()

async def setup(bot):
    await bot.add_cog(Meta(bot))