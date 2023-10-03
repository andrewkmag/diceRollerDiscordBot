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

# Remove provided help command
diceRollerBot.remove_command('help')

# Define set to contain valid types of checks for command parameter
CHECKTYPESET = {"athletics", "acrobatics", "sleight of hand",
                "stealth", "arcana", "history", "investigation",
                "nature", "religion", "animal handling",
                "insight", "medicine", "perception", "survival",
                "deception",  "intimidation", "performance",
                "persuasion", "strength", "wisdom", "intelligence", 
                "dexterity", "charisma", "constitution"}

# Bot event: When bot is ready send message
@diceRollerBot.event
async def on_ready():
    print(f'{diceRollerBot.user.name} ~Ready to perform checks ...')

# Bot command: /roll <ability_check>
# Roll a d20 (randomly generated number between 1 and 20) 
# and check that value against the Difficulty Class number
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

# Bot command: /help roll
# When no arguments are specified list the possible commands to provide documentation about
# If valid argument is specified detail the usage of said command
@diceRollerBot.command()
async def help(ctx, *args):
    # Handle case of empty arguments
    if len(args) == 0:
        await ctx.send(f'```Documentation available for commands:\n- roll```')
        return
    
    # Check which command to display documentation for
    processCommandString: str = args[0].lower()
    match processCommandString:
        case "roll":
            rollDocumentationString: str = '```Usage: /roll <ability_check>\nExample: /roll sleight of hand\nList of Valid Ability Checks:\n'
            for x in CHECKTYPESET:
                rollDocumentationString = rollDocumentationString + "-> " + x + "\n"
            await ctx.send(f'{rollDocumentationString}```')
        case _:
            await ctx.send(f'No documentation provided for the command / non-existant command input')

diceRollerBot.run('')