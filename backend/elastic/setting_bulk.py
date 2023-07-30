# search_app/setting_bulk.py
from elasticsearch import Elasticsearch


es = Elasticsearch()

es.indices.create(
    index='song',
    body={
        "settings": {
            "index": {
                "analysis": {
                    "analyzer": {
                        "my_analyzer": {
                            "type": "custom",
                            "tokenizer": "nori_tokenizer"
                        }
                    }
                }
            }
        },
        "mappings": {
            "properties": {
                "id": {
                    "type": "long"
                },
                "title": {
                    "type": "text",
                    "analyzer": "my_analyzer"
                },
                "artist": {
                    "type": "text",
                    "analyzer": "my_analyzer"
                },
                "ky_song_num_id": {
                    "type": "integer"
                },
                "tj_song_num_id": {
                    "type": "integer"
                },
                "master_number": {
                    "type": "integer"
                }
            }
        }
    }
)

import json

with open("./total-song2.json", encoding='utf-8') as json_file:
    json_data = json.loads(json_file.read())

songs = json_data['rows']

body = ""
for song in songs:
    title = song.get("title")
    artist = song.get("artist")
    
    body += json.dumps({"index": {"_index": "song"}}) + "\n"
    body += json.dumps(song, ensure_ascii=False) + "\n"

es.bulk(body)
