import os
import json

description = "A bot that retrieves prices of Yu-Gi-Oh! cards from YugiohPrices.com"
prefix = "$"

here_path = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(here_path, "data")
config_path = os.path.join(data_path, "config.json")
sets_path = os.path.join(data_path, "set_names.json")
cards_path = os.path.join(data_path, "card_names.json")

with open(config_path, 'r') as f:
    j = json.load(f)
    token = j["token"]
    owner_id = j["owner_id"]

max_results = 3
trunc_len = 20

icons = {
    "dark": "http://i.imgur.com/slNEyVk.png",
    "wind": "http://i.imgur.com/iecrLfT.png",
    "water": "http://i.imgur.com/OAhQgUw.png",
    "light": "http://i.imgur.com/EZbrrQ5.png",
    "fire": "http://i.imgur.com/6nGb4rf.png",
    "earth": "http://i.imgur.com/r3jFsid.png",
    "divine": "http://i.imgur.com/GGInB3U.png",
    "Continuous": "http://i.imgur.com/0s3LFUC.png",
    "Normal": "http://i.imgur.com/Q8a9IZN.png",
    "Equip": "http://i.imgur.com/M4CsBYb.png",
    "Quick-Play": "http://i.imgur.com/bv6OTZg.png",
    "Field": "http://i.imgur.com/aUFrtm1.png",
    "Ritual": "http://i.imgur.com/MYquQVC.png",
    "Counter": "http://i.imgur.com/hVGUA9L.png"
}

colors = {
    "Effect": "0xFF8B53",
    "Fusion": "0xA086B7",
    "Xyz": "0x111111",
    "Synchro": "0xFFFFFF",
    "Ritual": "0x9DB5CC",
    "Link": "0x00008B",
    "Normal": "0xFDE68A",
    "spell": "0x1D9E74",
    "trap": "0xBC5A84"
}

rarity_subs = [
    (" Rare", ""),
    ("Duel Terminal", "DT"),
    ("DT Normal Parallel", "DT Normal"),
    ("DT Super Parallel", "DT Super"),
    ("DT Ultra Parallel", "DT Ultra"),
    ("Unknown Rarity", "Unknown")
]

rarities = [
    "Super Short Print",
    "Short Print",
    "Common",
    "Rare",
    "Super",
    "Ultra",
    "Secret",
    "Ghost",
    "Ultimate",
    "Ghost/Gold",
    "Gold",
    "Gold Secret",
    "Platinum",
    "Platinum Secret",
    "Prismatic Secret",
    "Extra Secret",
    "DT Normal",
    "DT Super",
    "DT Ultra",
    "Normal Parallel",
    "Super Parallel",
    "Ultra Parallel",
    "Shatterfoil",
    "Starfoil",
    "Mosaic",
    "Unknown"
]
