#!/usr/bin/env python3

import glob
import json
import pathlib
import sys
import re
from decimal import *
import matplotlib.pyplot as plt

YEAR = "2017"

def read_judgments_jsons(files):
    for path in files:
        yield json.loads(pathlib.Path(path).read_text())


def items_from_judgments_jsons(judgments):
    for judgment in judgments:
        for item in judgment["items"]:
            yield item



def is_correct_judgment_year(year):
    return lambda item:item["judgmentDate"][:4] == year

def remove_xml_tags(text):
    return re.sub(r"<.*?>", " ", text)

def get_multiplier(text):
    return 1

def extract_money_amounts_from_text(text):

    text = remove_xml_tags(text)
    #for match in re.finditer(r"(\d[\d,\.\s]*)[^\d,\.;:!?]*?zł", text):
    for match in re.finditer(r"(\d[\d,\.\s]*?)[^\d,\.;:!?]*?zł", text):
        try:
            print(match.group(0), end="")
            number = match.group(1)

            # remove unecessary dots
            number = number.replace(".", "")

            # convert polish ',' decimal seperator to english
            number = number.replace(",", ".")

            # remove whitespaces between digits
            number = re.sub(r"\s", "", number)
            dec = Decimal(number)


            m = match.group(0)
            # remove 'in words' brackets
            m = re.sub("\(.*?\)?", "", m)
            money_amount = int(dec * get_multiplier(m))

            print("\t\t", int(dec))

            yield int(dec)
        except Exception as e:
            print("")
            print(e, file=sys.stderr)

# all jsons
if __name__ == "__main__":
    files = glob.glob("data/json/judgments*.json")

    judgments_jsons = read_judgments_jsons(files)
    items = items_from_judgments_jsons(judgments_jsons)

    money_amounts = []

    for item in filter(is_correct_judgment_year(YEAR), items):
        text_content = item["textContent"]
        money_amounts.extend(extract_money_amounts_from_text(text_content))

    print(len(money_amounts))

    #plt.hist(money_amounts, bins="auto", facecolor='g', alpha=0.75)
    #plt.title("Money amounts in judgments texts")
    #plt.grid(True)
    #plt.show()
