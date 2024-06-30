import discord
from discord.ext import commands

class Admin(commands.Cog):
    """Admin-based bot commands."""
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, *, module: str):
        """Loads a module."""
        try:
            await self.bot.load_extension(module)
        except commands.ExtensionError as e:
            await ctx.send(f'An error occured: {e}')
        else:
            await ctx.send(f'Successfully loaded {module}')

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, *, module: str):
        """Unloads a module."""
        try:
            await self.bot.unload_extension(module)
        except commands.ExtensionError as e:
            await ctx.send(f'An error occured: {e}')
        else:
            await ctx.send(f'Successfully unloaded {module}')
    
    @commands.command(name='reload')
    @commands.is_owner()
    async def _reload(self, ctx, *, module: str):
        """Reloads a module."""
        try:
            await self.bot.unload_extension(module)
            await self.bot.load_extension(module)
        except commands.ExtensionError as e:
            await ctx.send(f'An error occured: {e}')
        else:
            await ctx.send(f'Successfully reloaded {module}')

    @commands.command()
    @commands.is_owner()
    async def echo(self, ctx, *, message: str):
        """A simple message to check if the person invoking it is the owner."""
        await ctx.send(message)

async def setup(bot):
    await bot.add_cog(Admin(bot))