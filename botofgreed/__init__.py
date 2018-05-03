import sys
import os

import discord
from discord.ext import commands

print("heyo")
sys.path.insert(0, os.path.abspath('.'))
from botofgreed import config
from botofgreed import ygoprices

bot = commands.Bot(command_prefix=config.prefix, description=config.description)
