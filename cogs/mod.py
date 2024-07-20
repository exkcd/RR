import discord
from discord.ext import commands
from typing import Any, List, Dict, Union, Callable
import asyncio



class Mod(commands.Cog, name="Mod"):
    """Moderation like commands for managing a server."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['delete', 'clear'])
    @commands.guild_only()
    @commands.has_guild_permissions(manage_messages=True, read_message_history=True)
    async def purge(self, ctx, search: commands.Range[int, 1, 2000] = None):
        """Removes a number of messages."""

        predicates: list[Callable[[discord.Message], Any]] = []

        op = all

        def predicate(m: discord.Message) -> bool:
            r = op(p(m) for p in predicates)
            return r
        
        if search is None:
            search = 5
            
        await ctx.defer()

        try:
            deleted = await ctx.channel.purge(limit=search, check=predicate)
        except discord.Forbidden as e:
            return await ctx.send('I do not have permissions to delete messages.')
        except discord.HTTPException as e:
            return await ctx.send(f'Erorr: {e} (try a smaller search?)')

        
        deleted = len(deleted)
        messages = [f'{deleted} message{" was" if deleted == 1 else "s were"} removed.']
        if deleted:
            messages.append('')

        to_send = '\n'.join(messages)

        if len(to_send) > 2000:
            await ctx.send(f'Successfully removed {deleted} messages.', delete_after=10)
        else:
            await ctx.send(to_send, delete_after=10)

async def setup(bot):
    await bot.add_cog(Mod(bot))