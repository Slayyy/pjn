# Zadanie 2

## Jak uruchomić:

Budowa i uruchomienie dockera wraz z pluginem elasticsearch-analysis-morfologik:

```bash
docker build -t pjn2 . && docker run -p 9200:9200 pjn2
```

Stworzenie indeksu + ładowanie danych z danego roku do elasticsearch:

```bash
./prepare_es.py
```

Wyniki zapytań dostępne [tutaj](pjn2.ipynb)

