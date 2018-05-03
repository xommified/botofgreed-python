import difflib
from urllib.parse import quote
import requests
import discord
from prettytable import PrettyTable

from botofgreed import config
from botofgreed.ygoprices import utils


def get_card_prices(name, rarity):

    r = requests.get("http://yugiohprices.com/api/get_card_prices/{}".format(name))
    if r.status_code != 200:
        return None, None
    j = r.json()
    if j["status"] == "success":
        if rarity != "all":
            j["data"] = [row for row in j["data"] if utils.get_rarity(row["rarity"]) == rarity]
        return j
    else:
        return None


def build_card_message(name, resp, rarity):

    post = ""

    if resp is None:
        return None, None

    pt = PrettyTable()
    pt.field_names = ["Set", "Rarity", "Low-Avg"]
    pt.align = "l"

    seen = {}
    extra = {}

    for i, row in enumerate(resp["data"]):

        card_set = row["print_tag"]  # .split("-")[0]
        rarity = utils.get_rarity(row["rarity"])

        if rarity not in seen:
            seen[rarity] = 0
        seen[rarity] += 1

        if seen[rarity] > config.max_results:
            if rarity not in extra:
                extra[rarity] = 0
            extra[rarity] += 1
            continue

        if row["price_data"]["status"] != "success":
            price = "Unknown"
        else:
            price = "${0:.2f}-${1:.2f}".format(row["price_data"]["data"]["prices"]["low"],
                                               row["price_data"]["data"]["prices"]["average"])
        pt.add_row([card_set, rarity, price])

    if len(resp["data"]) == 0:
        pt = "No prints of '{}' found for rarity '{}'.".format(name, rarity)

    if extra:
        post += "Omitted "
        for key, value in extra.items():
            post += "{} {}, ".format(value, key)
        post = post[:-2] + " print(s)"

    # human_url = "https://yugiohprices.com/card_price?name={}".format(quote(name, safe=''))
    icon, color, image = get_card_properties(name)
    em = discord.Embed(type="rich",
                       description="```{}```\n{}\n".format(pt, post),
                       color=int(color, 0))
    em.set_author(name=name, icon_url=icon)
    em.set_footer(text="Data from YugiohPrices.com. May not be 100% accurate, use only as an estimate.",
                  icon_url="http://i.imgur.com/kLsxdAd.png")
    # em.set_thumbnail(url=image)
    return None, em


def get_card_properties(name):
    r = requests.get("http://yugiohprices.com/api/card_data/{}".format(name))

    if r.status_code != 200:
        return

    j = r.json()
    if j["status"] == "success":
        if j["data"]["card_type"] in ("spell", "trap"):
            icon = config.icons[j["data"]["property"]]
            color = config.colors[j["data"]["card_type"]]
        else:
            icon = config.icons[j["data"]["family"]]
            color = config.colors["Normal"]
            for key in config.colors:
                if key in j["data"]["type"]:
                    color = config.colors[key]
                    break

        image = requests.get("http://yugiohprices.com/api/card_image/{}".format(name)).url

        return icon, color, image

    else:
        return
