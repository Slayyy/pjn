#!/usr/bin/env python3

import glob
import json
import pathlib
import os
import os.path
import re
import errno

from datetime import datetime


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


def get_date(item):
    return datetime.strptime(item["judgmentDate"], "%Y-%m-%d")


def create_dir_if_not_exits(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


if __name__ == "__main__":
    N = 100
    DIR_NAME = f"first_{N}"
    files = glob.glob("data/json/judgments*.json")

    items_ids_to_dates = [
        (item["id"], get_date(item))
        for item in items_in_given_year(files)
    ]

    items_ids_to_dates = sorted(items_ids_to_dates, key=lambda x: x[1])
    items_ids = [x[0] for x in items_ids_to_dates]
    items_ids = items_ids[:N]

    create_dir_if_not_exits(DIR_NAME)
    for i, item in enumerate(
        filter(
            lambda item: item["id"] in items_ids,
            items_in_given_year(files)
        )
    ):
        with open(os.path.join(DIR_NAME, f"{i}.txt"), "w") as f:
            without_xml_tags = re.sub('<[^<]+>', "", item["textContent"])
            f.write(without_xml_tags)
