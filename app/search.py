from .index_elastic import es

def search_chunks(query, model=None, index_name="rag_chunks", top_k=3):# top_k c'est le nombre de chunk pertinent a retourner
    if model!= None:
        return hybrid_query(query, model)
    else:
        res = es.search(index=index_name, size=top_k, query={
            "match": {
                "content": query
            }
        })

        return [hit["_source"] for hit in res["hits"]["hits"]]


def hybrid_query(query, model, index_name="rag_chunks", k=5):
    query_embedding = model.encode(query, normalize_embeddings=True).tolist()

    query_body = {
        "size": k,
        "query": {
            "script_score": {
                "query": {
                    "match": {
                        "content": query
                    }
                },
                "script": {
                    "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
                    "params": {
                        "query_vector": query_embedding
                    }
                }
            }
        }
    }

    response = es.search(index=index_name, body=query_body)
    return [hit["_source"] for hit in response["hits"]["hits"]]
