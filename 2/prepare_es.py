#!/usr/bin/env python3

import glob
import json
import pathlib

from elasticsearch import Elasticsearch
from elasticsearch.exceptions import TransportError
from elasticsearch.helpers import bulk, streaming_bulk

YEAR = "2017"

def read_judgments_jsons(files):
    for path in files:
        yield json.loads(pathlib.Path(path).read_text())

def items_from_judgments_jsons(judgments):
    for judgment in judgments:
        for item in judgment["items"]:
            yield item

def is_correct_judgment_year(year):
    return lambda item:item["judgmentDate"][:4] == year

def items_in_given_year(files):
    judgments_jsons = read_judgments_jsons(files)
    items = items_from_judgments_jsons(judgments_jsons)
    for item in filter(is_correct_judgment_year(YEAR), items):
        yield item

def create_judgment_index(client):
    create_index_body = {
      "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 0,

        "analysis": {
          "analyzer": {
            "polish_analyzer": {
              "type": "custom",
              "tokenizer": "standard",
              "filter": ["morfologik_stem"]
            }
          }
        }
      },
      "mappings": {
        "doc": {
          "properties": {
            "id": {"type": "keyword"},
            "date": {"type": "date"},
            "text_content": {"type": "text"},
            "judges": {"type": "text"}
          }
        }
      }
    }
    client.indices.create(
        index="judgment",
        body=create_index_body
    )

def items_to_es_doc(items):
    for item in items:
        yield {
            "text_content": item["textContent"],
            "date": item["judgmentDate"],
            "id": item["id"],
            "judges": [judge["name"] for judge in item["judges"]]
        }
        
def push_judgments_to_es(client, items_in_es_format):
    for ok, result in streaming_bulk(
            client,
            items_in_es_format,
            index="judgment",
            doc_type="doc",
        ):
        action, result = result.popitem()
        doc_id = "/{}/doc/{}".format("judgment", result['_id'])

        if not ok:
            print("Failed to {} document {}: {}".format(action, doc_id, result))
        else:
            print(doc_id)


if __name__ == "__main__":
    es = Elasticsearch("localhost:9200")
    try:
        create_judgment_index(es)
    except Exception as e:
        print(e)

    files = glob.glob("data/json/judgments*.json")
    judgments_jsons = read_judgments_jsons(files)
    items = items_from_judgments_jsons(judgments_jsons)
    push_judgments_to_es(es, items_to_es_doc(items))

    es.indices.refresh(index="judgment")
