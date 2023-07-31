from elasticsearch import Elasticsearch

es = Elasticsearch(hosts="localhost:9200")

es.indices.delete(index='song')
