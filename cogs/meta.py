import discord
from discord.ext import commands

import time
import datetime

from collections import Counter
from typing import Any, Optional, Union, TYPE_CHECKING


class Meta(commands.Cog):
    """Utility type commands."""
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello (self, ctx):
        """Shows my welcome message."""
        await ctx.send('Hello! I am a robot.')

    @commands.command()
    async def ping(self, ctx):
        """Pong."""
        await ctx.send('Pong.')
    
    @commands.command()
    async def pong(self, ctx):
        """Ping."""

        await ctx.send(f'Ping: `{int(self.bot.latency*1000)} ms`')
    
    @commands.command(name='quit', hidden=True)
    @commands.is_owner()
    async def _quit(self, ctx):
        """Quits the bot."""
        await ctx.send('Goodbye.')
        await self.bot.close()

    @commands.command()
    async def avatar(self, ctx, *, user: Union[discord.Member, discord.User] = None):
        """Shows a user's avatar but large."""
        embed = discord.Embed()
        user = user or ctx.author
        avatar = user.display_avatar.with_static_format('png')
        embed.set_author(name=str(user), url=avatar)
        embed.set_image(url=avatar)
        await ctx.send(embed=embed)

    @commands.command(aliases=['info'])
    async def userinfo(self, ctx, *, user: Union[discord.Member, discord.User] = None):
        """Shows information about a specific user."""

        user = user or ctx.author
        e = discord.Embed()

        e.set_author(name=str(user))

        e.add_field(name='ID', value=user.id, inline=False)

        created_at = user.created_at.strftime('%s')
        joined_at = user.joined_at.strftime('%s')

        if ctx.guild is not None and isinstance(user, discord.Member):
            e.add_field(name='Joined', value=f'<t:{joined_at}:F> (<t:{joined_at}:R>)', inline=False)

        if ctx.guild is not None and isinstance(user, discord.Member):
            e.add_field(name='Created', value=f'<t:{created_at}:F> (<t:{created_at}:R>)', inline=False)

        if ctx.guild is not None and isinstance(user, discord.Member):
            roles = [role.name for role in user.roles]
        else: 
            roles = []
        
        e.add_field(name='Roles', value=', '.join(roles), inline=False)

        colour = user.colour
        if colour.value:
            e.colour = colour

        e.set_thumbnail(url=user.display_avatar.url)

        await ctx.send(embed=e)

    @commands.command(aliases=['server','guildinfo'])
    async def serverinfo(self, ctx, *, guild_id: int = None):
        """Shows info about this server."""

        guild = ctx.guild

        e = discord.Embed()

        e.title = guild.name


        if guild.icon:
            e.set_thumbnail(url=guild.icon.url)
            
        if await self.bot.is_owner(ctx.author):
            e.description = f'**ID**: {guild.id}\n**Owner**: yourself'
        else:
            e.description = f'**ID**: {guild.id}\n**Owner**: {guild.owner}'


        everyone = guild.default_role
        everyone_perms = everyone.permissions.value

        totals = Counter()
        secret = Counter()

        key_to_channel = {
            discord.TextChannel: 'text'.capitalize(),
            discord.VoiceChannel: 'voice'.capitalize()
        }

        for channel in guild.channels:
            allow, deny = channel.overwrites_for(everyone).pair()
            perms = discord.Permissions((everyone_perms & ~deny.value) | allow.value)
            channel_type = type(channel)
            totals[channel_type] += 1

            if not perms.read_messages:
                secret[channel_type] += 1
            elif isinstance(channel, discord.VoiceChannel) and (not perms.connect or not perms.speak):
                secret[channel_type] += 1

        channel_info = []

        for key, total in totals.items():
            secrets = secret[key]
            try:
                match_channel = key_to_channel[key]
            except KeyError:
                continue
            if secrets:
                channel_info.append(f'{match_channel}: {total} ({secrets} locked)')
            else:
                channel_info.append(f'{match_channel}: {total}')
    

        e.add_field(name='Channels', value='\n'.join(channel_info), inline=False)

        if len(guild.roles) > 2:
            e.add_field(name='Roles', value=f'{len(guild.roles)} roles', inline=False)

        else:
            roles = [role.name for role in guild.roles]
            e.add_field(name=f'Roles ({len(guild.roles)})', value=', '.join(roles), inline=False)

        bots = sum(m.bot for m in guild.members)

        if bots < 1:
            total_members = f'Total: {guild.member_count} people ({bots} bots)'
        else:
            total_members = f'Total: {guild.member_count} people ({bots} bot)'


        e.add_field(name='Members', value=total_members, inline=False)

        e.set_footer(text='Created').timestamp = guild.created_at

        await ctx.send(embed=e)

async def setup(bot):
    await bot.add_cog(Meta(bot))