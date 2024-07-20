import discord
from discord.ext import commands

import random
from enum import Enum


class RPS(Enum):
    rock = '\N{MOYAI}'
    paper = '\N{PAGE FACING UP}'
    scissors = '\N{BLACK SCISSORS}'


class RPSParser:
    def __init__(self, argument):
        argument = argument.lower()
        if argument == 'rock':
            self.choice = RPS.rock
        elif argument == 'paper':
            self.choice = RPS.paper
        elif argument == 'scissors':
            self.choice = RPS.scissors
        else:
            self.choice = None


class RNG(commands.Cog, name="RNG"):
    """Some pseudo-random commands."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def flip(self, ctx):
        """Flip a coin."""

        await ctx.send(f'`{random.choice(['HEADS', 'TAILS'])}`')

    @commands.command()
    async def choose(self, ctx, *choices):
        """Choose between some choices.
        Multiple choices must be denoted with double quotes."""

        if len(choices) < 2:
            return await ctx.send('Not enough choices.')

        await ctx.send(random.choice(choices))

    @commands.command()
    async def number(self, ctx, minimum: int = 0, maximum: int = 1000):
        """Displays a random number within a range. Maximum default is 1000."""

        maximum = min(maximum, 1000)
        if minimum >= maximum:
            await ctx.send('Maximum is smaller than the minimum.')
            return
        await ctx.send(str(random.randint(minimum, maximum)))

    @commands.command()
    async def lenny(self, ctx):
        """Displays a random lenny face."""

        lenny = random.choice(
            [
                "( ͡° ͜ʖ ͡°)",
                "( ͠° ͟ʖ ͡°)",
                "ᕦ( ͡° ͜ʖ ͡°)ᕤ",
                "( ͡~ ͜ʖ ͡°)",
                "( ͡o ͜ʖ ͡o)",
                "͡(° ͜ʖ ͡ -)",
                "( ͡͡ ° ͜ ʖ ͡ °)﻿",
                "(ง ͠° ͟ل͜ ͡°)ง",
                "ヽ༼ຈل͜ຈ༽ﾉ",
            ]
        )

        await ctx.send(lenny)

    @commands.command()
    async def hug(self, ctx, user: discord.Member, intensity: int = 1):
        """Hug a user. Up to 10 intensity levels."""
        name = f'*{user.display_name}*'

        if intensity <= 0:
            msg = "(っ˘̩╭╮˘̩)っ" + name
        elif intensity <= 3:
            msg = "(っ´▽｀)っ" + name
        elif intensity <= 6:
            msg = "(っ´▽｀)っ" + name
        elif intensity <= 9:
            msg = "(つ≧▽≦)つ" + name
        elif intensity >= 10:
            msg = "(づ￣ ³￣)づ{} ⊂(´・ω・｀⊂)".format(name)
        else:
            raise RuntimeError

        await ctx.send(msg)

    @commands.command(name='8ball', aliases=['8'])
    async def _8ball(self, ctx, *, question: str):
        """Ask the 8 ball a question. Queries must be denoted with a '?'."""

        responses = [
            ("As I see it, yes"),
            ("It is certain"),
            ("It is decidedly so"),
            ("Most likely"),
            ("Outlook good"),
            ("Signs point to yes"),
            ("Without a doubt"),
            ("Yes"),
            ("Yes, definitely"),
            ("You may rely on it"),
            ("Reply hazy, try again"),
            ("Ask again later"),
            ("Better not tell you now"),
            ("Cannot predict now"),
            ("Concentrate and ask again"),
            ("Don't count on it"),
            ("My reply is no"),
            ("My sources say no"),
            ("Outlook not so good"),
            ("Very doubtful"),
        ]

        if question.endswith('?') and question != '?':
            await ctx.send(f'`{random.choice(responses)}`')
        else:
            await ctx.send('Questions must end with a question mark.')

    @commands.command()
    async def rps(self, ctx, your_choice: RPSParser):
        """Play rock, paper, scissors."""

        player_choice = your_choice.choice

        if not player_choice:
            return ctx.send('Not a valid option. Options: {r}, {p}, {s}'.format(r='rock', p='paper', s='scissors'))

        bot_choice = random.choice((RPS.rock, RPS.paper, RPS.scissors))

        cond = {
            (RPS.rock, RPS.paper): False,
            (RPS.rock, RPS.scissors): True,
            (RPS.paper, RPS.rock): True,
            (RPS.paper, RPS.scissors): False,
            (RPS.scissors, RPS.paper): False,
            (RPS.scissors, RPS.rock): True,
        }

        if bot_choice == player_choice:
            outcome = None
        else:
            outcome = cond[(player_choice, bot_choice)]

        if outcome is True:
            await ctx.send(f'{bot_choice.value} You win!')

        elif outcome is False:
            await ctx.send(f'{bot_choice.value} You lose!')

        else:
            await ctx.send(f'{bot_choice.value} We\'re square!')


async def setup(bot):
    await bot.add_cog(RNG(bot))
