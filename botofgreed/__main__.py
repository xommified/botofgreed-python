import os
import sys

sys.path.insert(0, os.path.abspath('.'))
from botofgreed import config
from botofgreed.ygoprices import utils
from botofgreed.ygoprices import cards
from botofgreed.ygoprices import sets

from discord.ext import commands

print("Starting BotofGreed...")
sys.path.insert(0, os.path.abspath('.'))
from botofgreed import config

bot = commands.Bot(command_prefix=config.prefix, description=config.description)


@bot.event
async def on_ready():
    print("Logged in as: {}. ID: {}".format(bot.user.name, bot.user.id))


@bot.command(pass_context=True)
async def pc(ctx, *, arg):
    """Retrieves the price of a card."""

    await bot.add_reaction(ctx.message, "💭")

    if "$" in arg:
        a = arg.split("$")
        name = a[0].strip()
        rarity = a[1].strip()
    else:
        name = arg.strip()
        rarity = None

    name, name_guess = utils.closest_name(name)
    rarity, rarity_guess = utils.get_rarity(rarity)

    if name_guess or rarity_guess:
        await bot.add_reaction(ctx.message, "🤔")

    data = cards.get_card_prices(name, rarity)
    em, success = cards.build_card_message(name, data, rarity, rarity_guess)

    if em:
        await bot.say(None, embed=em)

    if success:
        await bot.add_reaction(ctx.message, "✅")
    else:
        await bot.add_reaction(ctx.message, "❌")


@bot.command(pass_context=True)
async def ps(ctx, *, arg):
    """Retrieves price info on a set."""

    await bot.add_reaction(ctx.message, "💭")

    name, guess = utils.closest_name(arg.strip(), lookup="set")

    if guess:
        await bot.add_reaction(ctx.message, "🤔")

    data = sets.get_set_prices(name)
    em, success = sets.build_set_message(name, data)

    if em:
        await bot.say(None, embed=em)

    if success:
        await bot.add_reaction(ctx.message, "✅")
    else:
        await bot.add_reaction(ctx.message, "❌")


@bot.command(pass_context=True)
async def snap(ctx):
    if ctx.message.author.id == config.owner_id:
        await bot.say("I don't feel so good mister xomm...")
        await bot.logout()


@bot.command(pass_context=True)
async def update(ctx):
    if ctx.message.author.id == config.owner_id:
        await bot.say("Updating names database.")
        r, s, e = utils.check_for_new_sets()
        await bot.say("Finished updating names database. New sets: {}, {} -> {} cards.".format(r, s, e))


def run():
    bot.run(config.token)


if __name__ == "__main__":
    run()
