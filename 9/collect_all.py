#!/usr/bin/env python3

import glob
import json
import pathlib
import re
import os

from tqdm import tqdm


def read_judgments_jsons(files):
    for path in files:
        yield json.loads(pathlib.Path(path).read_text())


def items_from_judgments_jsons(judgments):
    for judgment in judgments:
        for item in judgment["items"]:
            yield item


def texts(files):
    judgments_jsons = read_judgments_jsons(files)
    items = items_from_judgments_jsons(judgments_jsons)
    for item in items:
        yield item["textContent"]


def create_dir_if_not_exits(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)


if __name__ == "__main__":
    DIR = "all_items"
    create_dir_if_not_exits(DIR)
    files = glob.glob("data/json/judgments*.json")

    for i, text in tqdm(enumerate(texts(files))):
        text = re.sub('<[^<]+>', "", text)
        text = text.replace("-\n", "")
        text = re.sub("[^\w]", " ", text)
        text = text.lower()

        open(f"{DIR}/{i}.txt", "w").write(text)
