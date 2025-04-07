from elasticsearch import Elasticsearch

es = Elasticsearch("http://localhost:9200")

def create_index(index_name):
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name)
        print(f" Index '{index_name}' créé")
    else:
        print(f" Index '{index_name}' déjà existant")

def index_chunks(index_name, chunks):
    for chunk in chunks:
        es.index(index=index_name, body=chunk)
