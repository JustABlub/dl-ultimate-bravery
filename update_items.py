#!/usr/bin/env python3

import json

import requests
from bs4 import BeautifulSoup

itempage = "https://deadlock.wiki/Items"

page = requests.get(itempage)
soup = BeautifulSoup(page.text, "html.parser")

table = soup.find("table", {"class": "navbox"})
trs = table.find_all("tr")[1:]

master_list = {}
for item_type_tr in trs:
    category_list = {}
    try:
        title_span = item_type_tr.find("span", {"class": "item-nav-category-text"})
        item_table = item_type_tr.find("table", {"class": "navbox-subgroup"})

        soul_categories = item_table.find_all("tr")[::2]
        for tr in soul_categories:
            try:
                item_soul_value = tr.find("b").get_text()
                unparsed_items = tr.find_all("span", {"class": "item-link-wrapper"})

                temp_arr = []
                for item in unparsed_items:
                    temp_arr.append(item.get_text()[1:])
                category_list[item_soul_value] = temp_arr
            except:
                pass
        master_list[title_span.get_text()] = category_list
    except:
        pass

with open("items.json", "w") as fp:
    json.dump(master_list, fp, sort_keys=False, indent=4)
