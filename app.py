from flask import Flask, render_template
import random
import json

with open('./resources/characters.json') as f:
    characters = json.load(f)
with open("./resources/items.json") as f:
    item_page = json.load(f)

ITEM_TYPE = ["Spirit", "Vitality", "Weapon"]

def generate_draft():
    return random.sample(population=characters, k=4)

def generate_items(build_type, game_phase, k, used=None):
    if used is None:
        used = set()
    if build_type == "Spirit":
        item_bias = [60, 20, 20]
    elif build_type == "Vitality":
        item_bias = [20, 60, 20]
    elif build_type == "Weapon":
        item_bias = [20, 20, 60]

    if game_phase == "early":
        soul_bias = [30, 60, 7, 3, 0]
    elif game_phase == "mid":
        soul_bias = [0, 15, 55, 30, 0]
    elif game_phase == "late":
        soul_bias = [0, 0, 0, 1, 0]

    types = list(item_page.keys())
    build_page = []
    for _ in range(k):
        while True:
            item_type = random.choices(types, weights=item_bias, k=1)[0]
            tiers = list(item_page[item_type].keys())
            soul = random.choices(tiers, weights=soul_bias, k=1)[0]
            pool = [i for i in item_page[item_type][soul] if i not in used]
            if pool:
                item = random.choice(pool)
                break
        used.add(item)
        build_page.append(item)
    return build_page

app = Flask(__name__)

@app.route("/")
def index():
    build_bias = random.choice(ITEM_TYPE)
    used = set()
    return render_template(
        'index.html',
        draft=generate_draft(),
        early=generate_items(build_bias, "early", 4, used),
        mid=generate_items(build_bias, "mid", 4, used),
        late=generate_items(build_bias, "late", 4, used),
    )
