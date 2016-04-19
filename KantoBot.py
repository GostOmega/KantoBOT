import discord
from discord.ext import commands
from .utils.dataIO import fileIO
from random import randint
from copy import deepcopy
from .utils import checks
from __main__ import send_cmd_help
from operator import settings as bot_settings
import os
import time
#import logging

#-------------------------------------------------------------------------------------------------------------------------------------
#                                                          ||Store Data||
#-------------------------------------------------------------------------------------------------------------------------------------

ECON_DIR = "data/economy/bank.json"
#SPRITES = http://randompokemon.com/ (NEED TO CONTACT)

#-------------------------------------------------------------------------------------------------------------------------------------
#                                              || Start Creating Commands for the Bot ||
#-------------------------------------------------------------------------------------------------------------------------------------

class Kanto:
  """
  Lets you catch random pokemon utilizing the economy cog.
  Goal is to complete the PokeDex
  You can purchase Pokeballs
  """
  
  def __int__(self, bot):
    self.bot = bot
    self.bal = fileIO(ECON_DIR, "load")
    self.pc = fileIO("data/kantobot/pc/users.json", "load")
    self.pokedex = {}
    pokemon = {"Bulbasaure" : 1, "Squirtle" : 2, "Charmander" : 3} #Finish off list
  
  @commands.group(name="pokemon", pass_context=True, no_pm=True)
  async def _pokemon(self, ctx):
    """ Shows all pokemon commands """
    if ctx.invoked_subcommand is None:
      msg = "```"
      for z, y in self.settings.items():
        msg += str(z) + ": " + str(y) + "\n"
      msg += "\nType {}help pokemon to see the list of commands."
      await self.bot.say(msg)
      #await send_cmd_help(ctx)
  
  @_pokemon.command(pass_contex=True)
  async def register(self, ctx, user: discord.Member):
    """ Registers the user to become a pokemon trainer """
    server = ctx.message.server
    #Builders the @Trainer role.
    if '@Trainer' not in [role.name for role in server.roles]:
      await self.bot.say("\nThis is my first time running! Creating the Trainer Role! One second {}...").format(user.mention)
      try:
        perms = discord.Permissions.none()
        #Just a simple tag being created, doesn't need special permission. This is to see who are using KantoBot!
        await self.bot.create_role(server, name="@Trainer", permissions=perms)
      except discord.Forbidden:
        await self.bot.say("```diff\n- I cannot create a role. Please assign Manger Roles to me!\n```")
    
    #Gives user the @trainer role. Checks to see if they already have role.
    role = discord.utils.get(ctx.message.server.roles, name="@Trainer")
    if '@Trainer' not in [role.name for role in user.roles]:
      await self.bot.add_roles(user, role)
    else
      await self.bot.say("The @Trainer role is already assigned to {}.").format(user.name)
    
    #Creates storage for the user to start capturing pokemon.
    if user.id not in self.pc:
      self.pc[user.id] = {"Name" : user.name, "Pokemon" : self.pokedex}
      fileIO("data/kantobot/pc/users.json", "save", self.pc)
      await self.bot.say("Your new journey starts here! {} is now a Trainer!").format(user.name)
    else:
      await self.bot.say("\nYou already have caught {} Pokemon!").format(int(self.pokedex))

#-------------------------------------------------------------------------------------------------------------------------------------
#                                                      || End of Commands ||
#                                                || Start of Background Check ||
#-------------------------------------------------------------------------------------------------------------------------------------

def check_folders():
  """ Check to see if all the directories are present
  
  Add folders here if needed for a new directory """
  folders = ("data/kantobot/", "data/kantobot/pc/")
  for folder in folders:
    if not os.path.exsist(folder):
      print("Building the directory " + folder + " ...")
      os.makedir(folder)

def check_files():
  """ Check to see if all the needed files are downloaded
  
  Add files here if needed for new file """
  file = "data/kantobot/pc/users.json"
  if not fileIO(file, "check"):
    print("Adding in empty users.json ...")
    fileIO(file, "save", [])

def setup(bot):
  game = Kanto(bot)
  bot.add_cog(game)
