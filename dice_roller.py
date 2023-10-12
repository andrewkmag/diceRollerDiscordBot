import discord
from discord.ext import commands
import yaml
import random
import operator as op
import time
from table2ascii import table2ascii as t2a, PresetStyle
from table2ascii import Alignment

intents = discord.Intents.default()
intents.message_content = True
intents.presences = True

# Invite Link: https://discord.com/oauth2/authorize?client_id=1147014445474787409&permissions=68164851858518&scope=bot

# Setup bot with command prefix '/'
diceRollerBot = commands.Bot(command_prefix='/', intents=intents)

# Load ability and skill proficiency class data from YAML file
with open("class_modifier_spec.yaml", "r") as file:
    ability_data = yaml.safe_load(file)

# Remove provided help command
diceRollerBot.remove_command('help')

# Bot event: Log on the server terminal when bot is active and ready to send messages
@diceRollerBot.event
async def on_ready():
    print(f'{diceRollerBot.user.name} ~Ready to perform checks ...')

# Define player class
class PlayerClass:
    def __init__(self, name: str, className: str):
        self.name = name
        self.className = className

# Define set to contain valid types of checks for command parameter
CHECKTYPESET = {"athletics", "acrobatics", "sleight of hand",
                "stealth", "arcana", "history", "investigation",
                "nature", "religion", "animal handling",
                "insight", "medicine", "perception", "survival",
                "deception",  "intimidation", "performance",
                "persuasion", "strength", "wisdom", "intelligence", 
                "dexterity", "charisma", "constitution"}

# Define set of valid classes users can select from
CHECKCLASSSET = {"barbarian", "bard", "cleric", 
                 "druid", "fighter", "monk", 
                 "paladin", "ranger", "rogue", 
                 "sorcerer", "warlock", "wizard"}

# Define dictionary of users that have selected their starting class
userClassSelectionDict = {}

# Bot command: /selectClass <class_name>
# Sets the starting class for discord user
@diceRollerBot.command()
async def selectClass(ctx, userChoice: str):
    # Check if the user has already chosen a class
    # and send inform-message that states users can only select
    # a class once with the selectClass command 
    if op.countOf(userClassSelectionDict,ctx.author.id) == True:
        await ctx.send(f"```ERROR: Class not selected ...\nERROR: You can only select your starting class once.```")
        return
    else:
        userChoiceStr: str = userChoice.lower()
        # Create a PlayerClass object and Add that player to dictionary
        if op.countOf(CHECKCLASSSET, userChoiceStr) == True:
            startingPlayerClass = PlayerClass(ctx.author.name, userChoiceStr)
            userClassSelectionDict[ctx.author.id] = startingPlayerClass
            await ctx.send(f'***{ctx.author.name.upper()}*** has chosen the __**{userChoiceStr.upper()}**__ class as their starting class!')
            return
        else:
            await ctx.send(f"```ERROR: Invalid/Unknown class ...```")
            await ctx.send(f"```ERROR: Please enter a valid class to select from.```")
            return
        
# Bot command: /displayClass
# Displays the discord user's current class if set
@diceRollerBot.command()
async def displayClass(ctx):
    # Check if player has even set their class
    # and display class if found and inform if not found
    userHasClass = userClassSelectionDict.get(ctx.author.id)
    if userHasClass:
        await ctx.send(f'***{ctx.author.name.upper()}\'s*** current class is: __**{userHasClass.className.upper()}**__')
        return
    else:
        await ctx.send(f'***{ctx.author.name.upper()}\'s*** has not selected a class!')
        return

# Bot command: /roll <ability_check>
# Roll a d20 (randomly generated number between 1 and 20) 
# and check that value against the Difficulty Class number
@diceRollerBot.command()
async def roll(ctx, *args):
    # Use join to handle checks with more than one string
    checkType = " ".join(args).lower()

    # Check that ability check type is valid
    if op.countOf(CHECKTYPESET, checkType) == True:

        # Setup random number to perform check against
        numberToPass: int = random.randint(2,20)
        await ctx.send(f'# __Difficulty Class: {numberToPass}__')
        time.sleep(1)
        
        # Simulate the roll of a 20 sided dice
        result: int = random.randint(1,20)
        
        # Handle special cases for rolls that are 1 or 20
        if result == 20:
            await ctx.send(f"## Rolled a {result}: CRITICAL SUCCESS")
            return
        elif result == 1: 
            await ctx.send(f"## Rolled a {result}: CRITICAL FAILURE")       
            return
        
        await ctx.send(f'## Rolled a {result}')
        # Check if the user's class is set. If not continue the roll as normal
        userClass = userClassSelectionDict.get(ctx.author.id)
        if userClass:
                modifier: int = random.randint(1,3)
                # Check if the user's class is proficient in that ability
                if checkType in ability_data[userClass.className]:
                    await ctx.send(f'## +{modifier} Modifier: __**{userClass.className.upper()}**__ Proficiency in __**{checkType.upper()}**__ ')
                    result += modifier
                    await ctx.send(f'## Rolled a {result}')
                # Else apply negative modifer if user's class has no proficiency
                else:
                    await ctx.send(f'## -{modifier} Modifier: __**{userClass.className.upper()}**__ Not Proficient in __**{checkType.upper()}**__ ')
                    result -= modifier
                    await ctx.send(f'## Rolled a {result}')

        # Check if roll passed or failed against the generated number to beat
        if result >= numberToPass:
            await ctx.send(f'## SUCCESS')
            return
        elif result < numberToPass:
            await ctx.send(f'## FAILURE')
            return
    else:
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
        SETOFCOMMANDS = {'- roll', '- selectClass', '- displayClass'}
        listOfCommandsString: str = "\n".join(SETOFCOMMANDS)
        await ctx.send(f'__**Documentation available for commands:**__\n{listOfCommandsString}')
        return
    
    # Check which command to display documentation for
    processCommandString: str = args[0].lower()
    match processCommandString:
        case "roll":
            rollDocumentationString: str = 'Usage: /roll <ability_check>\n\nExample: /roll sleight of hand\n\nTable of Valid Ability Checks:\n'
            tableOfAbilityChecks = t2a(header=["Strength", "Dexterity", "Wisdom", "Intelligence", "Charisma"],
                                        body=[['Athletics', 'Acrobatics', 'Animal Handling', 'Arcana', 'Deception'], 
                                                [' ', 'Sleight of Hand', 'Insight', 'History', 'Intimidation'], 
                                                [' ', ' ', 'Medicine', 'Investigation', 'Performance'],
                                                [' ', ' ', 'Perception', 'Nature', 'Persuasion'],
                                                [' ', ' ', 'Survival', 'Religion', ' ']],
                                        alignments=Alignment.LEFT,
                        )
            noteAbilityChecks: str = '\n\nNote: *Constitution* is a valid ability check but since there are no other checks that fall into that category it is excluded from the above table.'
            await ctx.send(f'```{rollDocumentationString}{tableOfAbilityChecks}{noteAbilityChecks}```')
        case "selectclass":
            selectClassDocumentationString: str = 'Usage: /selectClass <class_name>\n\nExample: /selectClass Barbarian\n\nTable of Valid Classes:\n'
            tableOfClasses = t2a(header=["Class Names"],
                                 body=[['Barbarian'], ['Bard'], ['Cleric'], ['Druid'], ['Fighter'], ['Monk'], 
                                 ['Paladin'],['Ranger'], ['Rogue'], ['Sorcerer'], ['Warlock'], ['Wizard']],
                                 alignments=Alignment.LEFT,)
            await ctx.send(f'```{selectClassDocumentationString}{tableOfClasses}```')
        case "displayclass":
            displayClassDocumentationString: str = 'Usage: /displayClass\n\nDisplays the current class of the user if set and informs the user if they have not selected a valid class.'
            await ctx.send(f'```{displayClassDocumentationString}```')
        case _:
            await ctx.send(f'No documentation provided for the command / non-existant command input.')

diceRollerBot.run('')