import os
import urllib
import requests
import discord
from prettytable import PrettyTable
import pandas as pd
from colorthief import ColorThief
from io import BytesIO

from botofgreed import config
from botofgreed.ygoprices import utils


def dominant_color_from_url(url, tmp_file='tmp.jpg'):
    '''Downloads ths image file and analyzes the dominant color'''
    urllib.urlretrieve(url, tmp_file)
    color_thief = ColorThief(tmp_file)
    dominant_color = color_thief.get_color(quality=1)
    os.remove(tmp_file)
    return dominant_color


def get_set_prices(name):

    r = requests.get("http://yugiohprices.com/api/set_data/{}".format(name))
    if r.status_code != 200:
        return None, None
    j = r.json()
    if j["status"] == "success" and len(j["data"]["cards"]) > 0:
        for card in j["data"]["cards"]:
            card["low"] = card["numbers"][0]["price_data"]["data"]["prices"]["low"]
            card["average"] = card["numbers"][0]["price_data"]["data"]["prices"]["average"]
            card["rarity"] = card["numbers"][0]["rarity"]
        p = pd.DataFrame(j["data"]["cards"], columns=["name", "rarity", "low", "average"])
        p = p.sort_values(by=["low", "average"], ascending=False)
        d = p.head(10).to_dict('records')

        return d
    else:
        return None


def build_set_message(set_name, resp):

    post = ""

    if resp is None:
        return None, None

    pt = PrettyTable()
    pt.field_names = ["Set", "Rarity", "Low-Avg"]
    pt.align = "l"

    for row in resp:
        card_name = row["name"]
        if len(card_name) > config.trunc_len:
            card_name = card_name[:config.trunc_len-1] + "…"

        rarity = utils.get_rarity(row["rarity"])
        price = "${0:.2f}-${1:.2f}".format(row["low"], row["average"])
        pt.add_row([card_name, rarity, price])

    # icon, color, image = get_card_properties(name)

    r2 = requests.get("http://yugiohprices.com/api/set_image/{}".format(set_name))
    b = BytesIO(r2.content)
    ct = ColorThief(b)
    co = ct.get_color(quality=10)
    color = '0x%02x%02x%02x' % co

    em = discord.Embed(type="rich",
                       description="```{}```\n{}\n".format(pt, post),
                       color=int(color, 0))
    em.set_author(name=set_name, icon_url=r2.url)
    em.set_footer(text="Data from YugiohPrices.com. May not be 100% accurate, use only as an estimate.",
                  icon_url="http://i.imgur.com/kLsxdAd.png")
    # em.set_thumbnail(url=image)
    return None, em

