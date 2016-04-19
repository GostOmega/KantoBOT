import discord
from discord.ext import commands
from .utils.dataIO import fileIO
from time import ctime
import os
import random

"""-----------------------------------------------------------------------------------------------------------------------------------
                                                          ||Store Data||
-----------------------------------------------------------------------------------------------------------------------------------"""

DATA_FILE_PATH = "data/kantobot/"
PC_FILE = "pc.json"
POKEMON_FILE = "pokemon.json"

"""-----------------------------------------------------------------------------------------------------------------------------------
                                              || Start Creating Commands for the Bot ||
-----------------------------------------------------------------------------------------------------------------------------------"""

class Kanto:
    """
    Lets you catch random pokemon utilizing the economy cog.
    Goal is to complete the PokeDex
    You can purchase Pokeballs
    """
  
    def __init__(self, bot):
        print("-- Starting bot @ " + ctime() + " --")
        self.bot = bot
        self.dex = fileIO(DATA_FILE_PATH + PC_FILE, "load")
        self.pokemon = fileIO(DATA_FILE_PATH + POKEMON_FILE, "load")

    @commands.command()
    async def isAlive(self):
        """Test bot is alive!"""
        await self.bot.say("Hello World!")

    @commands.command(pass_context=True, no_pm=True)
    async def pokedex(self, ctx):
        """Pokedex"""
        user = ctx.message.author

        for result in self.dex:
            if result["id"] == user.name:
                print("Pokedex found for " + user.name)
                dex_user = get_dex_user(self, user)
                str = ""
                for pokemon in dex_user["pokemon"]:
                    str += get_pokemon(self, pokemon)["name"]
                    str += " "
                await self.bot.say(user.mention + " already has Pokemon: " + str)
                return

        print("No Pokedex found for " + user.name)
        await create_user(self, ctx)


"""-----------------------------------------------------------------------------------------------------------------------------------
                                                      || End of Commands ||
                                                || Start of Background Check ||
-----------------------------------------------------------------------------------------------------------------------------------"""

async def create_user(self, ctx):
    print("create user")
    server = ctx.message.server
    user = ctx.message.author

    print("user " + user.name)

    # Builders the @Trainer role.
    if 'Trainer' not in [role.name for role in server.roles]:
        print("Creating channel wide role - Trainer")
        try:
            perms = discord.Permissions.none()
            await self.bot.create_role(server, name="Trainer", permissions=perms)
            print("Role created")
        except discord.Forbidden as e:
            print("Bot could not create Trainer role - Have you checked bot permissions?")
            print(e)
            await self.bot.say("Something went wrong " + user.mention + " please seek admin help.")
            return

    # Gives user the trainer role. Checks to see if they already have role.
    role = discord.utils.get(ctx.message.server.roles, name="Trainer")
    if 'Trainer' not in [role.name for role in user.roles]:
        await self.bot.add_roles(user, role)
        print("Gave Trainer role to " + user.name)
    else:
        print("Trainer role is already assigned to " + user.name)

    # replace with give starter
    starter = recieve_starter(self, user)
    await self.bot.say("Your new journey starts here! " + user.mention +
                       " is now a Trainer with their trusty partner " + starter + "!")

def get_pokemon(self, number):
    if number in self.pokemon:
        return self.pokemon[number]
    else:
        # Something went wrong - assign user MissingNo.
        print("ERROR: No Pokemon found for number: " + number)
        return self.pokemon["0"]

def recieve_starter(self, user):
    # Default starters are 001, 004, 007, 025
    starter = random.choice(["1","4","7","25"])
    pokemon = get_pokemon(self, starter)
    # Save starter to file
    self.dex.append({"id": user.name, "pokemon": [starter]})
    fileIO(DATA_FILE_PATH + PC_FILE, "save", self.dex)
    self.dex = fileIO(DATA_FILE_PATH + PC_FILE, "load")
    return pokemon["name"]

def get_dex_user(self, user):
    for dex_user in self.dex:
        if dex_user["id"] == user.name:
            return dex_user
        break
    return None

def give_pokemon(self, user, number):
    dex_user = get_dex_user(self, user)
    # Debug purposes
    print("Giving pokemon to " + user.name)
    print(get_pokemon(self, number))
    dex_user["pokemon"].append(number)

    print("Saving pokemon to user")
    fileIO(DATA_FILE_PATH + PC_FILE, "save", self.dex)
    self.dex = fileIO(DATA_FILE_PATH + PC_FILE, "load")

def check_folders():
    if not os.path.exists(DATA_FILE_PATH):
        print("Creating " + DATA_FILE_PATH + " folder...")
        os.makedirs(DATA_FILE_PATH)

def check_files():
    f = DATA_FILE_PATH + PC_FILE
    if not fileIO(f, "check"):
        print("Creating empty " + PC_FILE + "...")
        fileIO(f, "save", [])
    f = DATA_FILE_PATH + POKEMON_FILE
    if not fileIO(f, "check"):
        print("WARNING: Empty " + f)
        fileIO(f, "save", [])

def setup(bot):
    check_folders()
    check_files()
    bot.add_cog(Kanto(bot))
