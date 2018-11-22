import os
import sys

from discord.ext import commands

print("Starting BotofGreed...")
sys.path.insert(0, os.path.abspath('.'))
from botofgreed import config

bot = commands.Bot(command_prefix=config.prefix, description=config.description)
