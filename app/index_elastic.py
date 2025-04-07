from elasticsearch import Elasticsearch
import os

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


def cleanup_orphan_documents(orphans, json_folder="data/chunks_json", index_name="rag_chunks"):
    for md_path in orphans:
        base_name = os.path.splitext(os.path.basename(md_path))[0]
        print(f"Nettoyage : {base_name}")

        es.delete_by_query(index=index_name, query={
            "match": {
                "metadata.source": f"{base_name}.md"
            }
        })
        print(f"Index Elasticsearch supprimer : {base_name}")

        json_path = os.path.join(json_folder, base_name + ".json")
        if os.path.exists(json_path):
            os.remove(json_path)

        if os.path.exists(md_path):
            os.remove(md_path)


def delete_index(index_name="rag_chunks"):
    if es.indices.exists(index=index_name):
        es.indices.delete(index=index_name)
        print(f"Index '{index_name}' supprimé.")
    else:
        print(f"L'index '{index_name}' n'existe pas.")