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
        if argument == 'rock' or 'r':
            self.choice = RPS.rock
        elif argument == 'paper' or 'p':
            self.choice = RPS.paper
        elif argument == 'scissors' or 's':
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

        await ctx.send(f'{random.choice(['HEADS', 'TAILS'])}')

    @commands.group()
    async def random(self, ctx):
        """Random commands."""
        if ctx.invoked_subcommand is None:
            await ctx.send(f'Incorrect random subcommand passed. Try {ctx.prefix}help random')

    @random.command()
    async def choice(self, ctx, *choices):
        """Choose between some choices.
        Multiple choices must be denoted with double quotes."""

        if len(choices) < 2:
            return await ctx.send('Not enough choices.')

        await ctx.send(random.choice(choices))

    @random.command()
    async def number(self, ctx, minimum: int = 0, maximum: int = 1000):
        """Displays a random number within a range. Maximum default is 1000."""

        maximum = min(maximum, 1000)
        if minimum >= maximum:
            await ctx.send('Maximum is smaller than the minimum.')
            return
        await ctx.send(str(random.randint(minimum, maximum)))

    @random.command()
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

    @commands.group()
    async def roll(self, ctx):
        """Roll a die (or some dice) in NdN format."""
        if ctx.invoked_subcommand is None:
            await ctx.send(f'Incorrect roll command passed. Try {ctx.prefix}help roll.')


    @roll.command()
    async def dice(self, ctx, dice: str):
        """Basic dice rolls."""
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            await ctx.send('Format must be NdN!')
            return
        result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))

        await ctx.send(result)

    @roll.command()
    async def total(self, ctx, dice: str):
        """Totals the dice rolls you've made."""

        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            await ctx.send('Format must be NdN!')
            return
        
        dice_rolls = [str(random.randint(1, limit)) for r in range(rolls)]
        
        result = ', '.join(dice_rolls)

        for i in range(0, len(dice_rolls)):
            dice_rolls[i] = int(dice_rolls[i])
        

        await ctx.send(f'{result}\nTotal: {sum(dice_rolls)}')

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
            await ctx.send(f'{random.choice(responses)}')
        else:
            await ctx.send('Questions must end with a question mark.')

    @commands.command()
    async def rps(self, ctx, your_choice: RPSParser):
        """Play rock, paper, scissors."""

        player_choice = your_choice.choice

        if not player_choice:
            return await ctx.send('Not a valid option. Options: {r}, {p}, {s}'.format(r='rock', p='paper', s='scissors'))

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
