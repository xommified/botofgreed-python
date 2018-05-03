import sys
import os

sys.path.insert(0, os.path.abspath('.'))
from botofgreed import *


@bot.event
async def on_ready():
    print("Logged in as: {}. ID: {}".format(bot.user.name, bot.user.id))


@bot.command()
async def add(name: str):
    """Retrieves the price of a card."""
    fuzzy = ygoprices.closest_name(name)
    if fuzzy is None:
        fuzzy = name

    r = ygoprices.price_table_from_name(fuzzy)
    await bot.say(embed=r)


def run():
    bot.run(config.token)


if __name__ == "__main__":
    run()
