# Zadanie 4

## Jak uruchomić:

Budowa i uruchomienie dockera wraz z pluginem elasticsearch-analysis-morfologik:

```bash
docker build -t pjn4 . && docker run -p 9200:9200 pjn4
```

Utworzenie listy frekwencyjnej dla unigramów i bigramów:
```bash
./make_unigram_frequence_list.py  | tee unigram_frequence_list.json
``` 
```bash
./make_bigram_frequence_list.py  | tee bigram_frequence_list.json 
``` 

[Wyniki](main.ipynb)

