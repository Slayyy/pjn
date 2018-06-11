# Zadanie 10

## Jak uruchomić:


```bash
./collect.py Informatyka Muzyka Polacy
./split_train_test.py input.txt 30%

fasttext supervised -input train.txt -output model -epoch 100  -thread 4
fasttext predict model.bin test.txt > pred.txt
```

[Wyniki](main.ipynb)