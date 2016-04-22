import discord
from discord.ext import commands
from .utils.dataIO import fileIO
from .utils import checks
from time import ctime
import os
import random

"""-----------------------------------------------------------------------------------------------------------------------------------
                                                          ||Store Data||
-----------------------------------------------------------------------------------------------------------------------------------"""

DATA_FILE_PATH = "data/kantobot/"
PC_FILE = "pc.json"
POKEMON_FILE = "pokemon.json"
BASE_ROLE_NAME = "@Trainer"

"""-----------------------------------------------------------------------------------------------------------------------------------
                                              || Start Creating Commands for the Bot ||
-----------------------------------------------------------------------------------------------------------------------------------"""

class Kanto:
    """
    Lets you catch random pokemon utilizing the economy cog.
    Goal is to complete the PokeDex.
    You can purchase Pokeballs at the pokemart.
    """
  
    def __init__(self, bot):
        print("-- Starting kanto @ " + ctime() + " --")
        self.bot = bot
        self.dex = fileIO(DATA_FILE_PATH + PC_FILE, "load")
        self.pokemon = fileIO(DATA_FILE_PATH + POKEMON_FILE, "load")

    #Seeing if the bot is responding. Will be removed for release later.
    @commands.command(name="test", pass_context=True)
    async def isAlive(self):
        """Test bot is alive!"""
        print ("KantoBot is able to respond!")

    @commands.command(pass_context=True, no_pm=False) #When user checks pokedex, send PM, don't have it spam server chat.
    async def pokedex(self, ctx):
        """Pokedex"""
        user = ctx.message.author
        dex_user = get_dex_user(self, user)

        if dex_user is not None:
            str = ""
            for pokemon in dex_user["pokemon"]:
                str += get_pokemon(self, pokemon)["name"]
                str += "\n" #Bug purposes, see if this goes through.
            await self.bot.say(user.mention + " is travelling with: \n" + str)#Making it list style instead or long string of text.
            return

        print("No Pokedex found for " + user.name)
        await create_user(self, ctx)


"""-----------------------------------------------------------------------------------------------------------------------------------
                                                      || End of Commands ||
                                                || Start of Background Check ||
-----------------------------------------------------------------------------------------------------------------------------------"""

async def create_user(self, ctx):
    """
    Creates a user record in the user information, assigning them the base role.
    Also assigns this new user a starter pokemon
    :param ctx: Context of call
    :return:
    """
    server = ctx.message.server
    user = ctx.message.author

    print("Creating kantobot info for user " + user.name)

    # Create the base trainer role iff it doesn't exist
    if BASE_ROLE_NAME not in [role.name for role in server.roles]:
        print("No base role found. Creating channel wide role - " + BASE_ROLE_NAME)
        try:
            # Create role - No permissions required
            perms = discord.Permissions.none()
            await self.bot.create_role(server, name=BASE_ROLE_NAME, permissions=perms)
            print(BASE_ROLE_NAME + " role created")
        except discord.Forbidden as e:
            # This exception can occur when the bot account does not have the relevant permissions
            print("Bot could not create " + BASE_ROLE_NAME + " role - Have you checked bot permissions?")
            print(e)
            await self.bot.say("Something went wrong " + user.mention + " please seek admin help.")
            return

    # Gives user the Trainer role. Checks to see if they already have role.
    role = discord.utils.get(ctx.message.server.roles, name=BASE_ROLE_NAME)
    if BASE_ROLE_NAME not in [role.name for role in user.roles]:
        # Add role to user
        await self.bot.add_roles(user, role)
        print("Gave " + BASE_ROLE_NAME + " role to " + user.name)
        await self.bot.say("Prof. Oak: Hello! Welcome to the world of Pokemon! Here at " + server.name + ", there's about 151 pokemon out there! Let me assign you a PokeDex so you can head out and start your adventure!\n")
    else:
        # User already has role
        print(BASE_ROLE_NAME + " role is already assigned to " + user.name)
        await self.bot.say("Prof. Oak: Did you already finish your PokeDex?")#This will be assigned for !pokemon register if they have an account

    # Gives user random starter Pokemon
    starter = receive_starter(self, user)
    await self.bot.say("Your new journey starts here! " + user.mention +
                       " is now a Trainer with their first trusty partner " + starter + "!")

def get_pokemon(self, number):
    """
    Get pokemon by dex number string identifier
    :param number: String representing pokemon id e.g. "151"
    :return: Pokemon dict object
    """
    # Check if Pokemon exists in dex
    if number in self.pokemon:
        return self.pokemon[number]
    else:
        # Something went wrong - assign user a 'MissingNo.'
        print("ERROR: No Pokemon found for number: " + number)
        return self.pokemon["0"]

def receive_starter(self, user):
    """
    Assigns a user one of 4 starter Pokemon
    The Gen I default starters are ids 001, 004, 007 and 025
    :param user: The user to receive the starter
    :return: The starter's name
    """
    # Get random choice from the starters
    starter = random.choice(["1", "4", "7", "25"])
    pokemon = get_pokemon(self, starter)
    # Save starter to file
    self.dex.append({"id": user.name, "pokemon": [starter]})
    fileIO(DATA_FILE_PATH + PC_FILE, "save", self.dex)
    # Reload new dex to memory
    self.dex = fileIO(DATA_FILE_PATH + PC_FILE, "load")
    # Return the starter name for prompt
    name = pokemon["name"]
    print("Assigned " + name + " as " + user.name + "'s starter")
    return name

def get_dex_user(self, user):
    """
    Retrieves user information from info stored in memory
    :param user: User to get information on
    :return: The user's information if available, None otherwise
    """
    for dex_user in self.dex:
        if dex_user["id"] == user.name:
            return dex_user
    return None

def give_pokemon(self, user, number):
    """
    Adds a Pokemon to a user's party
    :param user: The user to add the Pokemon too
    :param number: The string dex identifier of the Pokemon to add
    :return:
    """
    # Get user info
    dex_user = get_dex_user(self, user)
    # Printing for debug purposes - TODO Remove
    print("Giving pokemon to " + user.name)
    print(get_pokemon(self, number))
    # Add Pokemon to user
    dex_user["pokemon"].append(number)
    # Save user information
    print("Saving pokemon to user")
    fileIO(DATA_FILE_PATH + PC_FILE, "save", self.dex)
    # Reload information to memory
    self.dex = fileIO(DATA_FILE_PATH + PC_FILE, "load")


def check_folders():
    """
    Checks if data folders are created.
    If not, the folder is created
    :return:
    """
    if not os.path.exists(DATA_FILE_PATH):
        print("Creating " + DATA_FILE_PATH + " folder...")
        os.makedirs(DATA_FILE_PATH)

def check_files():
    """
    Checks if data file are created.
    If not, the files are created and populated with relevant base data
    :return:
    """
    # Check User storage file
    f = DATA_FILE_PATH + PC_FILE
    if not fileIO(f, "check"):
        print("Creating empty " + PC_FILE)
        fileIO(f, "save", [])
    # Check Pokemon JSON
    f = DATA_FILE_PATH + POKEMON_FILE
    if not fileIO(f, "check"):
        print("WARNING: Empty " + f)
        print("WARNING: Please download a relevant Pokemon JSON file")
        fileIO(f, "save", [])

def setup(bot):
    """
    Set up of bot
    :param bot: Red Bot instance
    :return:
    """
    check_folders()
    check_files()
    bot.add_cog(Kanto(bot))
