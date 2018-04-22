#!/usr/bin/env python3

from tqdm import tqdm

from multiprocessing import Pool
from pathlib import Path

import requests
import glob
import os
import re

def tag_file(file_path):
    tagged_file_path = re.sub(r"^(.*?)/(.*?)$", r"\1_tagged/\2", file_path)
    if Path(tagged_file_path).is_file():
        return

    text = Path(file_path).read_text()
    text = text.encode("utf-8")
    tagged_text = requests.post("http://localhost:9200", data=text).content

    os.makedirs(os.path.dirname(tagged_file_path), exist_ok=True)
    with open(tagged_file_path, "wb") as f:
        f.write(tagged_text)

def mycallback(x):
     print('mycallback is called with {}'.format(x))

if __name__ == "__main__":
    file_paths = sorted(glob.glob("2017_items/*.txt"))
    
    with Pool(processes=4) as p:
        with tqdm(total=len(file_paths)) as pbar:
            for i, _ in tqdm(enumerate(p.imap_unordered(tag_file, file_paths))):
                pbar.update()

