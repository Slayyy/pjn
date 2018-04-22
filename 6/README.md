# Zadanie 4

## Jak uruchomić:

Budowa i uruchomienie dockera wraz z pluginem elasticsearch-analysis-morfologik:

```bash
docker build -t pjn6 . && docker run -p 9200:9200 pjn6
```

Utworzenie statystyk występowania słow w dokumentach:
```bash
./make_frequence_stats.py
``` 

[Wyniki](main.ipynb)

