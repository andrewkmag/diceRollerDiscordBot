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
dice_roller_bot = commands.Bot(command_prefix='/', intents=intents)

# Load ability and skill proficiency class data from YAML file
with open("class_modifier_spec.yaml", "r") as file:
    class_proficiency_data = yaml.safe_load(file)

# Remove provided help command
dice_roller_bot.remove_command('help')

# Bot event: Log on the server terminal when bot is active and ready to send messages
@dice_roller_bot.event
async def on_ready():
    print(f'{dice_roller_bot.user.name} ~Ready to perform checks ...')

# Define player class
class player_class:
    def __init__(self, name: str, class_name: str):
        self.name = name
        self.class_name = class_name

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
user_class_selection_dict = {}

# Bot command: /select_class <class_name>
# Sets the starting class for discord user
@dice_roller_bot.command()
async def select_class(ctx, user_class_choice: str):
    # Check if the user has already chosen a class
    # and send inform-message that states users can only select
    # a class once with the select_class command 
    if op.countOf(user_class_selection_dict,ctx.author.id) == True:
        await ctx.send(f"```ERROR: Class not selected ...\nERROR: You can only select your starting class once.```")
        return
    else:
        user_class_choice_str: str = user_class_choice.lower()
        # Create a player_class object and Add that player to dictionary
        if op.countOf(CHECKCLASSSET, user_class_choice_str) == True:
            starting_player_class = player_class(ctx.author.name, user_class_choice_str)
            user_class_selection_dict[ctx.author.id] = starting_player_class
            await ctx.send(f'***{ctx.author.name.upper()}*** has chosen the __**{user_class_choice_str.upper()}**__ class as their starting class!')
            return
        else:
            await ctx.send(f"```ERROR: Invalid/Unknown class ...```")
            await ctx.send(f"```ERROR: Please enter a valid class to select from.```")
            return
        
# Bot command: /display_class
# Displays the discord user's current class if set
@dice_roller_bot.command()
async def display_class(ctx):
    # Check if player has even set their class
    # and display class if found and inform if not found
    user_has_class = user_class_selection_dict.get(ctx.author.id)
    if user_has_class:
        await ctx.send(f'***{ctx.author.name.upper()}\'s*** current class is: __**{user_has_class.class_name.upper()}**__')
        return
    else:
        await ctx.send(f'***{ctx.author.name.upper()}\'s*** has not selected a class!')
        return

# TODO: Bot command: /remove_class
# Removes the discord user's current class if set

# Bot command: /roll <ability_check>
# Roll a d20 (randomly generated number between 1 and 20) 
# and check that value against the Difficulty Class number
@dice_roller_bot.command()
async def roll(ctx, *args):
    # Use join to handle checks with more than one string
    skill_check_type = " ".join(args).lower()

    # Check that ability check type is valid
    if op.countOf(CHECKTYPESET, skill_check_type) == True:

        # Setup random number to perform check against
        difficulty_class_num: int = random.randint(2,20)
        await ctx.send(f'# __Difficulty Class: {difficulty_class_num}__')
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
        user_class = user_class_selection_dict.get(ctx.author.id)
        if user_class:
                modifier: int = random.randint(1,3)
                # Check if the user's class is proficient in that ability
                if skill_check_type in class_proficiency_data[user_class.class_name]:
                    await ctx.send(f'## +{modifier} Modifier: __**{user_class.class_name.upper()}**__ Proficiency in __**{skill_check_type.upper()}**__ ')
                    result += modifier
                    await ctx.send(f'## Rolled a {result}')
                # Else apply negative modifer if user's class has no proficiency
                else:
                    await ctx.send(f'## -{modifier} Modifier: __**{user_class.class_name.upper()}**__ Not Proficient in __**{skill_check_type.upper()}**__ ')
                    result -= modifier
                    await ctx.send(f'## Rolled a {result}')

        # Check if roll passed or failed against the generated number to beat
        if result >= difficulty_class_num:
            await ctx.send(f'## SUCCESS')
            return
        elif result < difficulty_class_num:
            await ctx.send(f'## FAILURE')
            return
    else:
        await ctx.send(f"Invalid/Unknown ability check ...")
        await ctx.send(f"Please enter a valid ability check")
        return

# Bot command: /help roll
# When no arguments are specified list the possible commands to provide documentation about
# If valid argument is specified detail the usage of said command
@dice_roller_bot.command()
async def help(ctx, *args):
    # Handle case of empty arguments
    if len(args) == 0:
        SETOFCOMMANDS = {'- roll', '- select_class', '- display_class'}
        commands_list: str = "\n".join(SETOFCOMMANDS)
        await ctx.send(f'__**Documentation available for commands:**__\n{commands_list}')
        return
    
    # Check which command to display documentation for
    process_command: str = args[0].lower()
    match process_command:
        case "roll":
            roll_documentation_message: str = 'Usage: /roll <ability_check>\n\nExample: /roll sleight of hand\n\nTable of Valid Ability Checks:\n'
            skill_check_table = t2a(header=["Strength", "Dexterity", "Wisdom", "Intelligence", "Charisma"],
                                        body=[['Athletics', 'Acrobatics', 'Animal Handling', 'Arcana', 'Deception'], 
                                                [' ', 'Sleight of Hand', 'Insight', 'History', 'Intimidation'], 
                                                [' ', ' ', 'Medicine', 'Investigation', 'Performance'],
                                                [' ', ' ', 'Perception', 'Nature', 'Persuasion'],
                                                [' ', ' ', 'Survival', 'Religion', ' ']],
                                        alignments=Alignment.LEFT,
                        )
            skill_check_note: str = '\n\nNote: *Constitution* is a valid ability check but since there are no other checks that fall into that category it is excluded from the above table.'
            await ctx.send(f'```{roll_documentation_message}{skill_check_table}{skill_check_note}```')
        case "select_class":
            select_class_documentation_message: str = 'Usage: /select_class <class_name>\n\nExample: /select_class Barbarian\n\nTable of Valid Classes:\n'
            class_table = t2a(header=["Class Names"],
                                 body=[['Barbarian'], ['Bard'], ['Cleric'], ['Druid'], ['Fighter'], ['Monk'], 
                                 ['Paladin'],['Ranger'], ['Rogue'], ['Sorcerer'], ['Warlock'], ['Wizard']],
                                 alignments=Alignment.LEFT,)
            await ctx.send(f'```{select_class_documentation_message}{class_table}```')
        case "display_class":
            display_class_documentation_message: str = 'Usage: /display_class\n\nDisplays the current class of the user if set and informs the user if they have not selected a valid class.'
            await ctx.send(f'```{display_class_documentation_message}```')
        case _:
            await ctx.send(f'No documentation provided for the command / non-existant command input.')

dice_roller_bot.run('')