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
    return re.match(r"^[aąbcćdeęfghijklłmnńoóprsśtuwyzźż]{2,}$", word)


if __name__ == "__main__":
    files = glob.glob("data/json/judgments*.json")
    items = items_in_given_year(files)

    frequence_list = {}
    for item in items:
        text_content = item["textContent"]
        text_content = text_content.replace("-", "")
        text_content = text_content.replace("\n", "")

        url = "http://localhost:9200/_analyze"
        request = {
           "char_filter":  ["html_strip"],
           "tokenizer": "standard",
           "filter": ["lowercase", "stop"],
           "text": item["textContent"],
        }
        response = requests.post(url, json=request)

        words = [token["token"] for token in response.json()["tokens"]]
        for word in filter(is_correct_word, words):
            if word not in frequence_list:
                frequence_list[word] = 0
            frequence_list[word] += 1
        
    frequence_list = [(k, v) for k, v in frequence_list.items()]
    frequence_list = sorted(frequence_list, key=lambda x: x[1], reverse=True)
    print(json.dumps(frequence_list))
    

