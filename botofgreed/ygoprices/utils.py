import difflib
import json

import requests

from botofgreed import config


def get_rarity(rarity):
    if not rarity:
        return None, False

    r = rarity
    for key, value in config.rarity_subs:
        r = r.replace(key, value)

    r = difflib.get_close_matches(r, config.rarities, n=1)

    if len(r) == 0:
        return None, True
    else:
        if r[0].casefold() == rarity.casefold():
            return r[0], False
        else:
            return r[0], True


def closest_name(name, lookup="card"):
    if lookup == "card":
        index_file = config.cards_path
    elif lookup == "set":
        index_file = config.sets_path
    else:
        return None

    with open(index_file, 'r') as f:
        index = json.load(f)

    r = difflib.get_close_matches(name, index, n=1, cutoff=config.similarity)

    if len(r) == 0:
        return name, True
    else:
        if r[0].casefold() == name.casefold():
            return r[0], False
        else:
            return r[0], True


def get_set_names():
    r = requests.get("http://yugiohprices.com/api/card_sets")
    if r.status_code != 200:
        print("not good")
        return

    j = r.json()
    with open(config.sets_path, "w") as f:
        json.dump(j, f)


def get_card_names():
    get_set_names()

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
