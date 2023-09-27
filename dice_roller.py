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
CHECKTYPESET = {"athletics", "acrobatics", "sleightofhand",
                "stealth", "arcana", "history", "investigation",
                "nature", "religion", "animalhandling",
                "insight", "medicine", "perception", "survival",
                "deception",  "intimidation", "performance",
                "persuasion"}

# Bot event: When bot is ready send message
@diceRollerBot.event
async def on_ready():
    print(f'{diceRollerBot.user.name} ~Ready to perform checks ...')

# Ability Check processing to handle checks that have more than one string
# I.e. Ability Checks that are seperated with whitespace characters
async def processArgs(*args):
    temp: str = ""
    # Traverse through the arguments
    for i in args:
        temp = " ".join(*args)
        print(f'CONSOLE: Concatenated argument is: {temp}')
    return temp

# Bot command: Roll a d20 and check that value against a randomly generated number
@diceRollerBot.command()
async def roll(ctx, *args):
    # Process arguments passed into coroutine that handles ability checks with whitespaces
    processArgsResult = processArgs(*args)
    checkType = await processArgsResult
    print(f'CONSOLE: Final processed argument is: {checkType}')
    
    # Convert to lowercase and remove whitespaces
    temp: str = checkType
    checkTypeString = temp.replace(" ", "").lower()
    print(f'CONSOLE: String used for checking {checkTypeString}')
    
    # Simulate the roll of a 20 sided dice
    result: int = random.randint(1,20)
    # Setup random number to perform check against
    numberToPass: int = random.randint(2,20)
    validAbilityCheck: bool = op.countOf(CHECKTYPESET, checkTypeString)
    print(f'CONSOLE: Valid ability check result: {validAbilityCheck}')

    # Check that ability check type is valid
    if op.countOf(CHECKTYPESET, checkTypeString) == True:
        await ctx.send(f'Difficulty Class: {numberToPass}')
        print(f'CONSOLE: Difficulty Class: {numberToPass}')

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
        await ctx.send(f"Please enter a valid ability check")
        return

diceRollerBot.run('')