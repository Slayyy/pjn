#!/usr/bin/env python3

from gensim.models import Word2Vec

import logging

from tqdm import tqdm
from glob import glob


logging.basicConfig(
    format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


if __name__ == "__main__":

    class TextsIterator(object):
        def __iter__(self):
            for f in tqdm(glob("trigrams/*.txt")):
                yield open(f, "r").read().split(" ")

    wv = Word2Vec(
        TextsIterator(),
        sg=0,  # CBOW
        window=5,
        size=300,
        min_count=3,
        workers=4
    ).wv

    wv.save("wv")
