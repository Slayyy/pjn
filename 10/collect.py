#!/usr/bin/env python3

import wikipedia
import sys
import re
from tqdm import tqdm

wikipedia.set_lang("pl")

result_file = open("input.txt", "w")
for category in sys.argv[1:]:
    file_content = open(category+".json", "r").read()
    ids = re.findall(r'"id":(\d+)', file_content)

    for id in tqdm(ids[:100]):
        try:
            page = wikipedia.page(pageid=id)
        except Exception as e:
            print(e)
            continue

        page = re.sub(r"==[^=]==", "", page.content)
        page = re.sub(r"[^\w\s]", " ", page)
        page = re.sub(r"[0-9]", " ", page)
        page = re.sub(r"\s+", " ", page)
        page = page.lower()

        result_file.write(f"__label__{category} ")
        result_file.write(page.replace("\n", " "))
        result_file.write("\n")
