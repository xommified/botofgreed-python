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


def check_for_new_sets():
    r = requests.get("http://yugiohprices.com/api/card_sets")
    if r.status_code != 200:
        print("not good")
        return

    new = set(r.json())

    try:
        with open(config.sets_path, "r") as f:
            old = set(json.load(f))
    except IOError:
        old = set()

    new_sets = sorted(new-old)
    starting, ending = get_card_names(all_sets=False, sets=new_sets)

    with open(config.sets_path, "w") as f:
        json.dump(list(new), f)

    new_sets = new_sets if new_sets else None

    return new_sets, starting, ending


def get_set_names():
    r = requests.get("http://yugiohprices.com/api/card_sets")
    if r.status_code != 200:
        print("not good")
        return

    j = r.json()
    with open(config.sets_path, "w") as f:
        json.dump(j, f)


def get_card_names(all_sets=True, sets=None):

    if all_sets:
        try:
            with open(config.sets_path, "r") as f:
                sets = json.load(f)
        except IOError:
            get_set_names()
            with open(config.sets_path, "r") as f:
                sets = json.load(f)

        all_cards = set()
    else:
        try:
            with open(config.cards_path, "r") as f:
                all_cards = set(json.load(f))
        except IOError:
            all_cards = set()

    starting = len(all_cards)
    print("Starting with {} cards.".format(starting))

    for i, set_name in enumerate(sets):
        print("{}/{}: Getting {}".format(i, len(sets), set_name))
        r = requests.get("http://yugiohprices.com/api/set_data/{}".format(set_name))
        if r.status_code != 200:
            print("Error: {}".format(r))
            continue
        j = r.json()
        print([x["name"] for x in j["data"]["cards"]])
        for card in j["data"]["cards"]:
            all_cards.add(card["name"])

        # print(all_cards)

    ending = len(all_cards)
    print("Finished with {} cards.".format(ending))

    with open(config.cards_path, "w") as f:
        json.dump(list(all_cards), f)

    return starting, ending
