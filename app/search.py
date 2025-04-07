from .index_elastic import es

def search_chunks(query, index_name="rag_chunks", top_k=3):# top_k c'est le nombre de chunk pertinent a retourner
    res = es.search(index=index_name, size=top_k, query={
        "match": {
            "content": query
        }
    })
    print("="*100)
    print(res)
    print("=" * 100)
    return [hit["_source"] for hit in res["hits"]["hits"]]
