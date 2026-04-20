import json
import os
import random

import httpx

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def generate_name():
    with open(os.path.join(BASE_DIR, "names.json")) as f:
        NAMES_DATA = json.load(f)
    return (
        f"{random.choice(NAMES_DATA['adjectives'])}{random.choice(NAMES_DATA['names'])}"
    )


def choose_surfer():
    with open(os.path.join(BASE_DIR, "surfers.json"), "r") as f:
        surfers = json.load(f).get("surfers", [])

    surfer = random.choice(surfers)
    dataTag = surfer["dataTag"]

    return dataTag


def choose_country():
    with open(os.path.join(BASE_DIR, "countries.json"), "r") as f:
        countries = json.load(f).get("countries", [])

    country = random.choice(countries)
    code = country["code"]

    return code


def get_countrys():
    with open(os.path.join(BASE_DIR, "countries.json"), "r") as f:
        countries = json.load(f).get("countries", [])

    return countries
