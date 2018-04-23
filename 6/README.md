# Zadanie 

## Jak uruchomić:

Budowa i uruchomienie dockera wraz z pluginem elasticsearch-analysis-morfologik:

```bash
docker build -t pjn6 . && docker run -p 9200:9200 pjn6
```

Utworzenie danych uczących i testowych dla obu przypadków:
```bash
./prepare_data.py && \
./prepare_data.py --lematization
``` 

[Wyniki](main.ipynb)

