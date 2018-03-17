# Zadanie 3

## Jak uruchomić:

Budowa i uruchomienie dockera wraz z pluginem elasticsearch-analysis-morfologik:

```bash
docker build -t pjn3 . && docker run -p 9200:9200 pjn3
```

Utworzenie listy frekwencyjnej słow:
```bash
./make_frequence_list.py  | tee frequence_list.json
```

[Wyniki](main.ipynb)

