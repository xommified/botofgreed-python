import sys
import os

sys.path.insert(0, os.path.abspath('.'))
from botofgreed import bot
from botofgreed import config
from botofgreed.ygoprices import utils
from botofgreed.ygoprices import cards
from botofgreed.ygoprices import sets


@bot.event
async def on_ready():
    print("Logged in as: {}. ID: {}".format(bot.user.name, bot.user.id))


@bot.command(pass_context=True)
async def pc(ctx, *, arg):
    """Retrieves the price of a card."""
    if "$" in arg:
        a = arg.split("$")
        name = a[0].strip()
        rarity = a[1].strip()
    else:
        name = arg.strip()
        rarity = "all"

    name = utils.closest_name(name)
    rarity = cards.get_card_rarity(rarity)

    data = cards.get_card_prices(name, rarity)

    text, em = cards.build_card_message(name, data, rarity)

    if any((text, em)):
        await bot.say(text, embed=em)
    else:
        await bot.add_reaction(ctx.message, "❓")


@bot.command(pass_context=True)
async def ps(ctx, *, arg):
    """Retrieves price info on a set."""

    name = utils.closest_name(arg.strip(), lookup="set")
    data = sets.get_set_prices(name)
    text, em = sets.build_set_message(name, data)

    if any((text, em)):
        await bot.say(text, embed=em)
    else:
        await bot.add_reaction(ctx.message, "❓")


@bot.command()
async def kill():
    await bot.logout()


def run():
    bot.run(config.token)


if __name__ == "__main__":
    run()
