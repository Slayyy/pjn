#!/usr/bin/env python3

from gensim.models import Phrases

import logging

from tqdm import tqdm
from glob import glob
import os


logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


def items_stream_from_disk(all_files):
    for f in tqdm(all_files[:5 * 10**4]):
        yield open(f, "r").read().split(" ")


def create_dir_if_not_exits(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)


if __name__ == "__main__":
    DIR = "trigrams"

    all_files = glob("all_items/*.txt")

    bigram_transformer = Phrases(
        items_stream_from_disk(all_files), min_count=3)
    trigram_transformer = Phrases(
        bigram_transformer[items_stream_from_disk(all_files)], min_count=3)
    del bigram_transformer

    create_dir_if_not_exits(DIR)
    for i, text in enumerate(
        trigram_transformer[items_stream_from_disk(all_files)]
    ):
        open(f"{DIR}/{i}.txt", "w").write(" ".join(text))
