#!/usr/bin/env python3

import glob
import os
import requests
import json
import pathlib
import collections
import re
import sys
import math
import pickle
import numpy as np
import gc
from tqdm import tqdm

from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from scipy import sparse

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
    most_common = {"na", "do", "nie", "że", "art", "się", "dnia", "przez", "od",
                   "sąd", "za", "jest", "zł", "oraz", "roku", "tym", "co", "sądu", "po", "pracy"}
    return (word not in most_common) and re.match(r"^[aąbcćdeęfghijklłmnńoóprsśtuwyzźż-]{2,}$", word)


def determine_group(item):
    groups = [r"A?C.*", r"A?U.*", r"A?K.*",
              r"G.*", r"A?P.*", r"R.*", r"W.*", r"Am.*"]
    court_case = item["courtCases"][0]["caseNumber"]

    for group in groups:
        if re.search(group, court_case):
            return group


@dataclass
class BagOfWord:
    group: str
    counter: collections.Counter


def extract_bags_of_words(items, perform_lemmatisation):
    bagOfWords = []

    i = 0
    for item in tqdm(filter(lambda x: x["courtType"] == "COMMON", items)):
        text_content = item["textContent"]

        i += 1
        if i == 1000:
            break


        group = determine_group(item)
        if not group:
            continue

        try:
            text_content = re.search(
                r"^[\s\S]*?UZASADNIENIE([\s\S]*)$", text_content, re.IGNORECASE).group(1)
        except (AttributeError, IndexError):
            continue

        url = "http://localhost:9200/_analyze"

        filters = ["lowercase", "stop"]
        if perform_lemmatisation:
            filters.append("morfologik_stem")

        request = {
            "char_filter":  ["html_strip"],
            "filter": filters,
            "tokenizer": "standard",
            "text": text_content,
        }
        response = requests.post(url, json=request)
        words = [token["token"] for token in response.json()["tokens"]]
        words = filter(is_correct_word, words)

        bagOfWords.append(BagOfWord(determine_group(item),
                                    collections.Counter(words)))

    return bagOfWords


if __name__ == "__main__":
    perform_lemmatisation = False
    if len(sys.argv) == 2:
        perform_lemmatisation = True if sys.argv[1] == "--lemmatisation" else False

    files = glob.glob("data/json/judgments*.json")

    bags_of_words = extract_bags_of_words(
        items_in_given_year(files),
        perform_lemmatisation
    )
    print(f"bags_of_words len == {len(bags_of_words)}")

    all_words_counter = collections.Counter()

    for bow in bags_of_words:
        all_words_counter.update(bow.counter)

    for w in list(all_words_counter):
        if sum(1 for bow in bags_of_words if w in bow.counter) < 10:
            del all_words_counter[w]

    words_sequence = sorted([w for w in all_words_counter])
    print(f"words_sequence len == {len(words_sequence)}")

    bags_of_words_len = float(len(bags_of_words))
    idfs = {
        w: math.log(
            bags_of_words_len /
            sum(1 for bow in bags_of_words if w in bow.counter)
        )
        for w in words_sequence
    }

    train_data = []
    test_data = []

    for group in tqdm(set([bow.group for bow in bags_of_words])):
        group_bow = [bow for bow in bags_of_words if bow.group == group]
        train, test = train_test_split(group_bow, test_size=0.25)
        train_data.extend(train)
        test_data.extend(test)

    print(f"train_data len == {len(train_data)}")
    print(f"test_data len == {len(test_data)}")

    directory = "lemmatised" if perform_lemmatisation else "normal"
    if not os.path.exists(directory):
        os.makedirs(directory)

    del bags_of_words
    del all_words_counter

    for name, data in tqdm((("test", test_data), ("train", train_data))):
        gc.collect()
        shape = (len(data), len(words_sequence))
        print(f"{name}: {shape}")

        m = sparse.lil_matrix(shape, dtype=float)
        for i, bow in enumerate(data):
            bc_sum =  float(sum(bow.counter.values()))
            for j, w in enumerate(words_sequence):
                tf = float(bow.counter[w]) / bc_sum
                m[i, j] = tf * idfs[w]

        m = m.tocsr()
        gc.collect()
        with open(f"{directory}/{name}.pkl", "wb") as f:
            pickle.dump(m.tocsr(), f, pickle.HIGHEST_PROTOCOL)

        with open(f"{directory}/{name}_groups.json", "w") as f:
            json.dump([bow.group for bow in data], f)

