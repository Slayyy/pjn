#!/usr/bin/env python3

import glob
import requests
import json
import pathlib
import re


YEAR = "2017"

def read_judgments_jsons(files):
    for path in files:
        yield json.loads(pathlib.Path(path).read_text())


def items_from_judgments_jsons(judgments):
    for judgment in judgments:
        for item in judgment["items"]:
            yield item


def is_correct_judgment_year(year):
    return lambda item: item["judgmentDate"][:4] == year


def items_in_given_year(files):
    judgments_jsons = read_judgments_jsons(files)
    items = items_from_judgments_jsons(judgments_jsons)
    for item in filter(is_correct_judgment_year(YEAR), items):
        yield item


def is_correct_word(word):
    return re.match(r"^[aąbcćdeęfghijklłmnńoóprsśtuwyzźż-]+$", word)


if __name__ == "__main__":
    files = glob.glob("data/json/judgments*.json")
    items = items_in_given_year(files)

    frequence_list = {}
    for i, item in enumerate(items):
        text_content = item["textContent"]
        text_content = re.sub('<[^<]+>', "", text_content)
        with open("{}_items/{}.txt".format(YEAR, i), "w") as f:
            f.write(text_content)

