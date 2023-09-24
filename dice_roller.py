import discord
from discord.ext import commands
import random
import operator as op
import time

intents = discord.Intents.default()
intents.message_content = True
intents.presences = True

# Permissions Integer 68164851711094

# Setup bot with command prefix '/'
diceRollerBot = commands.Bot(command_prefix='!', intents=intents)

# define set to contain valid types of checks for command parameter
CHECKTYPESET = {"athletics", "acrobatics", "sleight of hand",
                "stealth", "arcana", "history", "investigation",
                "nature", "religion", "animal handling",
                "insight", "medicine", "perception", "survival",
                "deception",  "intimidation", "performance",
                "persuasion"}

# Bot event: When bot is ready send message
@diceRollerBot.event
async def on_ready():
    print(f'{diceRollerBot.user.name} ~Ready to perform checks ...')

#Bot command: Roll a d20 and check that value against a randomly generated number
@diceRollerBot.command()
async def roll(ctx, checkType: str):
    # Check that ability check type is valid
    if op.countOf(CHECKTYPESET, checkType.lower()) == True:
        # Setup random number to perform check against
        numberToPass = random.randint(2,20)
        await ctx.send(f'Difficulty Class: {numberToPass}')
        print(f'CONSOLE: Difficulty Class: {numberToPass}')

        # Define number and simulate roll
        result = random.randint(1,20)

        # Handle special cases for rolls that are 1 or 20
        if result == 20:
            time.sleep(1) 
            await ctx.send(f"Rolled a {result}: CRITICAL SUCCESS")
            print(f"CONSOLE: Rolled a {result}: CRITICAL SUCCESS")
            return
        elif result == 1:
            time.sleep(1) 
            await ctx.send(f"Rolled a {result}: CRITICAL FAILURE")
            print(f"CONSOLE: Rolled a {result}: CRITICAL FAILURE")
            return
        # Check if roll passed or failed against the generated number to beat
        elif result >= numberToPass:
            time.sleep(1) 
            await ctx.send(f'Rolled a {result}: SUCCESS')
            print(f'CONSOLE: Rolled a {result}: SUCCESS')
            return
        elif result < numberToPass:
            time.sleep(1) 
            await ctx.send(f'Rolled a {result}: FAILURE')
            print(f'CONSOLE: Rolled a {result}: FAILURE')
            return
    else:
        time.sleep(1) 
        await ctx.send(f"Invalid/Unknown ability check ...")
        print(f'CONSOLE: Rolled a {result}: FAILURE')
        await ctx.send(f"Please enter a valid ability check")
        print(f'CONSOLE: Rolled a {result}: FAILURE')
        return
    


diceRollerBot.run('MTE0NzAxNDQ0NTQ3NDc4NzQwOQ.Gsk4p_.wz1N-gKDDM8FS299N3i33X96WdByLBBG7DHquM')