import requests
from prettytable import PrettyTable
import json
import difflib
from urllib.parse import quote
import datetime

from botofgreed import config
from botofgreed import discord


def closest_name(name, lookup="card"):
    if lookup == "card":
        index_file = config.cards_path
    elif lookup == "set":
        index_file = config.sets_path
    else:
        return None

    with open(index_file, 'r') as f:
        index = json.load(f)

    r = difflib.get_close_matches(name, index, n=1)

    if len(r) == 0:
        return None
    else:
        return r[0]


def price_table_from_name(name):
    r = requests.get("http://yugiohprices.com/api/get_card_prices/{}".format(name))
    if r.status_code != 200:
        print("not good")
        return

    j = r.json()
    if j["status"] == "success":
        pt = PrettyTable()
        pt.field_names = ["Set", "Rarity", "Low-Avg"]
        pt.align = "l"
        for row in j["data"]:
            card_set = row["print_tag"].split("-")[0]
            rarity = row["rarity"].replace(" Rare", "")
            price = "${0:.2f}-${1:.2f}".format(row["price_data"]["data"]["prices"]["low"],
                                               row["price_data"]["data"]["prices"]["average"])
            print(price, row["price_data"]["data"]["prices"]["low"], row["price_data"]["data"]["prices"]["average"])
            pt.add_row([card_set, rarity, price])

        human_url = "https://yugiohprices.com/card_price?name={}".format(quote(name, safe=''))
        icon, color, image = get_properties(name)
        em = discord.Embed(type="rich",
                           description="```{}```".format(pt),
                           color=int(color, 0))
        em.set_author(name=name, icon_url=icon)
        # em.set_thumbnail(url=image)
        return em
    else:
        return j


def get_properties(name):
    r = requests.get("http://yugiohprices.com/api/card_data/{}".format(name))

    if r.status_code != 200:
        print("not good")
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



def retrieve_sets():
    r = requests.get("http://yugiohprices.com/api/card_sets")
    if r.status_code != 200:
        print("not good")
        return

    j = r.json()
    with open(config.sets_path, "w") as f:
        json.dump(j, f)


def retrieve_card_names():
    with open(config.sets_path, "r") as f:
        sets = json.load(f)

    all_cards = set()
    for set_name in sets:
        print("Getting {}".format(set_name))
        r = requests.get("http://yugiohprices.com/api/set_data/{}".format(set_name))
        if r.status_code != 200:
            print("not good")
            return
        j = r.json()
        for card in j["data"]["cards"]:
            all_cards.add(card["name"])

        print(all_cards)

    with open(config.cards_path, "w") as f:
        json.dump(list(all_cards), f)
