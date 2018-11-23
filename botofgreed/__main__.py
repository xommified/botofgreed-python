import os
import sys

sys.path.insert(0, os.path.abspath('.'))
from botofgreed import config
from botofgreed.ygoprices import utils
from botofgreed.ygoprices import cards
from botofgreed.ygoprices import sets

from discord.ext import commands
from discord import Embed
from discord import Game

print("Starting BotofGreed...")
sys.path.insert(0, os.path.abspath('.'))
from botofgreed import config

bot = commands.Bot(command_prefix=config.prefix, description=config.description)
bot.remove_command('help')


@bot.event
async def on_ready():
    print("Logged in as: {}. ID: {}".format(bot.user.name, bot.user.id))
    await bot.change_presence(game=Game(name="$help for info",
                                        url="https://github.com/xommified/botofgreed-python",
                                        type=1),
                              status="$help for info")


@bot.event
async def on_message(message):
    print("got message: {}".format(message.content))
    if not message.author.bot:
        if message.content.startswith("$$"):
            await bot.send_message(message.channel, ("<@{}>: $$ has been deprecated, use `$pc` instead. "
                                                     "Type `$help` for more info.").format(message.author.id))
        elif message.content.startswith("##"):
            await bot.send_message(message.channel, ("<@{}>: ## has been deprecated, use `$ps` instead. "
                                                     "Type `$help` for more info.").format(message.author.id))

    await bot.process_commands(message)


@bot.command(pass_context=True)
async def pc(ctx, *, arg):
    """Retrieves the price of a card, ex: $pc Raigeki. Can specify rarity like: $pc Raigeki $Secret"""

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
    """Retrieves cards costing more than $5 USD or otherwise top 8 cards from a set, ex: $ps Starstrike Blast"""

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


@bot.command(pass_context=True)
async def help(ctx):
    em = Embed(type="rich",
               color=int("0x50C878", 0),
               title="View source on Github",
               url="https://github.com/xommified/botofgreed-python")
    em.add_field(name="`$pc Card Name`", value="Retrieve price listings for a card. "
                                               "Displays up to **{}** copies per rarity.\n—".format(config.max_results))
    em.add_field(name="`$pc Card Name $Rarity`", value=("Retrieve price listings for a card with a specific rarity. "
                                                        "Displays up to **{}** copies.\n\n"
                                                        "Valid rarities are: \n"
                                                        "Super Short Print, Short Print, Common, Rare, Super, Ultra, "
                                                        "Secret, Ghost, Ultimate, Ghost/Gold, Gold, Gold Secret, "
                                                        "Platinum, Platinum Secret, Prismatic Secret, Extra Secret, "
                                                        "DT Normal, DT Super, DT Ultra, Normal Parallel, "
                                                        "Super Parallel, Ultra Parallel, Shatterfoil, Starfoil, "
                                                        "Mosaic, Unknown\n—").format(config.max_with_rarity))
    em.add_field(name="`$ps Set Name`", value="Retrieve cards costing more than **$5 USD** from a set, "
                                              "or if there are none, the top **8** cards from the set.\n—")

    em.add_field(name="`Reactions`", value=("💭: Request has been received and has started processing.\n"
                                            "🤔: No exact match found in database, guessing with up to {} similarity.\n"
                                            "✅: Request completed successfully.\n"
                                            "❌: Request was not completed successfully.\n—").format(config.similarity))
    em.set_author(name="Help:")
    em.set_footer(text="Data from YugiohPrices.com. May not be 100% accurate, use only as an estimate.",
                  icon_url=config.icons["YGOP"])
    await bot.say(None, embed=em)


def run():
    bot.run(config.token)


if __name__ == "__main__":
    run()
