from urllib.parse import quote

import discord
import requests
from prettytable import PrettyTable

from botofgreed import config
from botofgreed.ygoprices import utils


def get_card_prices(name, rarity):
    r = requests.get(config.card_price_endpoint.format(name))
    if r.status_code not in (200, 404):
        return r.status_code

    if r.status_code == 404:
        return None

    j = r.json()
    if j["status"] == "success":
        if rarity:
            j["data"] = [row for row in j["data"] if utils.get_rarity(row["rarity"])[0] == rarity]
        return j
    else:
        return None


def build_card_message(name, resp, req_rarity, rarity_guess):
    post = ""

    if isinstance(resp, int):
        em = discord.Embed(type="rich",
                           description="HTTP status code {} from YugiohPrices.".format(resp),
                           color=int("0xFF0000", 0),
                           title="View on YugiohPrices.com",
                           url=config.card_price_url.format(quote(name)))
        em.set_author(name="Error", icon_url=config.icons["Error"])
        em.set_footer(text="Check if YugiohPrices.com is down. If not, contact xomm.",
                      icon_url=config.icons["YGOP"])
        return em, False
    elif not resp:
        return None, False

    pt = PrettyTable()
    pt.field_names = ["Set", "Rarity", "Low-Avg"]
    pt.align = "l"

    seen = {}
    extra = {}
    if req_rarity:
        max_results = config.max_with_rarity
    else:
        max_results = config.max_results

    for i, row in enumerate(resp["data"]):

        card_set = row["print_tag"]  # .split("-")[0]
        rarity = utils.get_rarity(row["rarity"])[0]

        if rarity not in seen:
            seen[rarity] = 0
        seen[rarity] += 1

        if seen[rarity] > max_results:
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
        pt = "No prints of '{}' found for rarity '{}'.".format(name, req_rarity)

    if rarity_guess:
        post += "Unknown rarity, best guess: `{}`. Valid rarities are: \n```{}```\n".format(req_rarity, config.rarities)

    if extra:
        post += "Showing {} cheapest prints of each rarity.\nOmitted ".format(max_results)
        for key, value in extra.items():
            post += "{} {}, ".format(value, key)
        post = post[:-2] + " print(s)"

    icon, color, image = get_card_properties(name)
    em = discord.Embed(type="rich",
                       description="```{}```\n{}\n".format(pt, post),
                       color=int(color, 0),
                       title="View on YugiohPrices.com",
                       url=config.card_price_url.format(quote(name)))
    em.set_author(name=name, icon_url=icon)
    em.set_footer(text="Data from YugiohPrices.com. May not be 100% accurate, use only as an estimate.",
                  icon_url=config.icons["YGOP"])
    # em.set_thumbnail(url=image)
    return em, True


def get_card_properties(name):
    r = requests.get(config.card_data_endpoint.format(name))

    if r.status_code not in (200, 404):
        return r.status_code

    if r.status_code == 404:
        return None

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

        image = requests.get(config.card_image_endpoint.format(name)).url

        return icon, color, image

    else:
        return
