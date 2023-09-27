import discord
from discord.ext import commands
import random
import operator as op
import time

intents = discord.Intents.default()
intents.message_content = True
intents.presences = True

# Invite Link: https://discord.com/oauth2/authorize?client_id=1147014445474787409&permissions=68164851858518&scope=bot

# Setup bot with command prefix '/'
diceRollerBot = commands.Bot(command_prefix='/', intents=intents)

# Define set to contain valid types of checks for command parameter
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

# Bot command: Roll a d20 and check that value against a randomly generated number
@diceRollerBot.command()
async def roll(ctx, *args):
    # Use join to handle checks with more than one string
    checkType = " ".join(args).lower()

    # Check that ability check type is valid
    if op.countOf(CHECKTYPESET, checkType) == True:
            
        # Simulate the roll of a 20 sided dice
        result: int = random.randint(1,20)
        # Setup random number to perform check against
        numberToPass: int = random.randint(2,20)
        
        await ctx.send(f'Difficulty Class: {numberToPass}')
        time.sleep(1)
        # Handle special cases for rolls that are 1 or 20
        if result == 20:
            await ctx.send(f"Rolled a {result}: CRITICAL SUCCESS")
            return
        elif result == 1: 
            await ctx.send(f"Rolled a {result}: CRITICAL FAILURE")       
            return
        # Check if roll passed or failed against the generated number to beat
        elif result >= numberToPass:
            await ctx.send(f'Rolled a {result}: SUCCESS')
            return
        elif result < numberToPass:
            await ctx.send(f'Rolled a {result}: FAILURE')
            return
    else:
        time.sleep(1) 
        await ctx.send(f"Invalid/Unknown ability check ...")
        await ctx.send(f"Please enter a valid ability check")
        return

diceRollerBot.run('')