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

"""-----------------------------------------------------------------------------------------------------------------------------------
                                                          ||Store Data||
-----------------------------------------------------------------------------------------------------------------------------------"""

ECON_DIR = "data/economy/bank.json"
#SPRITES = http://randompokemon.com/ (NEED TO CONTACT)

"""-----------------------------------------------------------------------------------------------------------------------------------
                                              || Start Creating Commands for the Bot ||
-----------------------------------------------------------------------------------------------------------------------------------"""

class Kanto:
  """
  Lets you catch random pokemon utilizing the economy cog.
  Goal is to complete the PokeDex
  You can purchase Pokeballs
  """
  
  def __int__(self,bot):
    self.bot = bot
    self.bal = fileIO(ECON_DIR, "load")
    #self.pc = fileIO("data/KantoBot/pc/users.json", "load")  USE FOR FUTURE GOAL.
  
  @commands.group(name="pokemon", pass_context=True, no_pm=False)
  async def _pokemon(self, ctx):
    """ Shows all pokemon commands """
    if ctx.invoked_subcommand is None:
      await send_cmd_help(ctx)
  
  @_pokemon.command(pass_contex=True):
  async def register():
    """ Registers the user to become a pokemon trainer """
    

"""-----------------------------------------------------------------------------------------------------------------------------------
                                                      || End of Commands ||
                                                || Start of Background Check ||
-----------------------------------------------------------------------------------------------------------------------------------"""

def check_folders():
  """ Check to see if all the directories are present
  
  Add folders here if needed for a new directory """
  folders = ("data/KantoBot/", "data/KantoBot/pc/")
  for folder in folders:
    if not os.path.exsist(folder):
      print("Building the directory " + folder + " ...")
      os.makedir(folder)

def check_files():
  """ Check to see if all the needed files are downloaded
  
  Add files here if needed for new file """
  file = "data/KantoBot/pc/users.json"
  if not fileIO(file, "check"):
    print("Adding in empty users.json ...")
    fileIO(file, "save", [])

def setup(bot):
  game = Kanto(bot)
  bot.add_cog(game)
