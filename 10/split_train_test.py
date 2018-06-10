#!/usr/bin/env python3

import sys

input_file = open(sys.argv[1], "r").readlines()
ratio = int(sys.argv[2].replace("%", "")) / 100

categories = {}
for row in input_file:
    category = row.split(" ")[0]
    if category not in categories:
        categories[category] = []
    categories[category].append(row)


test_rows = []
train_rows = []
for _, rows in categories.items():
    bound = int(len(rows) * ratio)
    test_rows.extend(rows[:bound])
    train_rows.extend(rows[bound:])

open("test.txt", "w").write("".join(test_rows))
open("train.txt", "w").write("".join(train_rows))
