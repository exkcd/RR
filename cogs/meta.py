import discord
from discord.ext import commands, menus

import inspect
import contextlib

from collections import Counter
from typing import Union


class HelpEmbed(discord.Embed):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        footer = "Use help [command] or help [category] for more information."
        self.set_footer(text=footer)
        self.colour = discord.Colour.blurple()


class FrontPageSource(HelpEmbed):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Welcome to the help page!"
        self.add_field(
            name="About me",
            value=(
                "I am a bot made by Rey (exkcd). I am a pretty basic bot used mainly for fun and "
                " to hone the skills of the Python programming language.\n"
                "You can view my code on [GitHub](https://github.com/exkcd/winston)"
            ),
            inline=True
        )
        self.add_field(
            name="Usage",
            value=inspect.cleandoc(
                f"""
            '<argument>' means the argument is __**required**__.
            '[argument]' means the argument is __**optional**__.
            '[A|B]' means it can __**either be A or B**__.
            '[argument...]' means you can have __**multiple arguments**__.
            """
            ),
            inline=True
        )


class HelpMenu(commands.HelpCommand):
    def __init__(self):
        super().__init__(
            command_attrs={
                "help": "The help command for the bot",
                "cooldown": commands.CooldownMapping.from_cooldown(1, 3.0, commands.BucketType.user),
            }
        )

    async def send(self, **kwargs):
        """shortcut to sending get_destination."""
        await self.get_destination().send(**kwargs)

    async def send_help_embed(self, title, description, commands):
        embed = HelpEmbed(
            title=title, description=description or "No help found...")

        if filtered_commands := await self.filter_commands(commands, sort=True):
            for command in filtered_commands:
                embed.add_field(name=self.get_command_signature(
                    command), value=command.help or "No help found...", inline=False)

        await self.send(embed=embed)

    def get_command_signature(self, command: commands.Command) -> str:
        parent = command.full_parent_name
        if len(command.aliases) > 0:
            fmt = f'{command.name}'
            if parent:
                fmt = f'{parent} {fmt}'
            alias = fmt
        else:
            alias = command.name if not parent else f'{parent} {command.name}'
        return f'{alias} {command.signature}'

    async def send_bot_help(self, mapping):
        """called with <prefix>help"""

        embed = FrontPageSource()

        for cog, commands in mapping.items():
            if filtered_commands := await self.filter_commands(commands, sort=True):
                amount_commands = len(filtered_commands)
                if cog:
                    name = cog.qualified_name
                    description = cog.description or "No description"
                else:
                    name = "No"
                    description = "Commands with no category"

                embed.add_field(
                    name=f'{name} Category ({amount_commands})', value=description, inline=False)

        await self.send(embed=embed)

    async def send_command_help(self, command):
        """called with <prefix>help [command]"""
        signature = self.get_command_signature(command)
        embed = HelpEmbed(
            title=signature, description=command.help or "No help found...")

        alias = command.aliases

        if alias:
            embed.description = f'**Aliases**: [{('|').join(alias)}]'
        if cog := command.cog:
            embed.add_field(name="Category", value=cog.qualified_name)

        can_run = "No"
        with contextlib.suppress(commands.CommandError):
            if await command.can_run(self.context):
                can_run = "Yes"
        embed.add_field(name="Usable", value=can_run)

        if command._buckets and (
                cooldown := command._buckets._cooldown):
            embed.add_field(
                name="Cooldown",
                value=f"{cooldown.rate} per {cooldown.per:.0f} seconds",
            )
        await self.send(embed=embed)

    async def send_cog_help(self, cog):
        """called with <prefix>help [cog]"""
        title = cog.qualified_name or "No"
        await self.send_help_embed(f'{title} Category', cog.description, cog.get_commands())

    async def send_group_help(self, group):
        """called with <prefix>help [group]"""
        title = self.get_command_signature(group)
        await self.send_help_embed(title, group.help, group.commands)


class Meta(commands.Cog, name="Meta"):
    """Utility type commands."""

    def __init__(self, bot):
        self.bot = bot
        help_command = HelpMenu()
        help_command.cog = self
        bot.help_command = help_command

    @commands.command()
    async def hello(self, ctx):
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
        e = discord.Embed(colour=discord.Colour.blurple())

        e.set_author(name=str(user))

        e.add_field(name='ID', value=user.id, inline=False)

        created_at = user.created_at.strftime('%s')
        joined_at = user.joined_at.strftime('%s')

        if ctx.guild is not None and isinstance(user, discord.Member):
            e.add_field(
                name='Joined', value=f'<t:{joined_at}:F> (<t:{joined_at}:R>)', inline=False)

        if ctx.guild is not None and isinstance(user, discord.Member):
            e.add_field(
                name='Created', value=f'<t:{created_at}:F> (<t:{created_at}:R>)', inline=False)

        if ctx.guild is not None and isinstance(user, discord.Member):
            roles = [role.name for role in user.roles]
        else:
            roles = []

        e.add_field(name='Roles', value=', '.join(roles), inline=False)

        e.set_thumbnail(url=user.display_avatar.url)

        await ctx.send(embed=e)

    @commands.command(aliases=['server', 'guildinfo'])
    async def serverinfo(self, ctx, *, guild_id: int = None):
        """Shows info about this server."""

        guild = ctx.guild

        e = discord.Embed(colour=discord.Colour.blurple())

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
            perms = discord.Permissions(
                (everyone_perms & ~deny.value) | allow.value)
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
                channel_info.append(
                    f'{match_channel}: {total} ({secrets} locked)')
            else:
                channel_info.append(f'{match_channel}: {total}')

        e.add_field(name='Channels', value='\n'.join(
            channel_info), inline=False)

        if len(guild.roles) > 2:
            e.add_field(
                name='Roles', value=f'{len(guild.roles)} roles', inline=False)

        else:
            roles = [role.name for role in guild.roles]
            e.add_field(name=f'Roles ({len(guild.roles)})',
                        value=', '.join(roles), inline=False)

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
