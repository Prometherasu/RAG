

# a finir en connectant a une ia

def generate_answer(question, retrieved_chunks):
    context = "\n---\n".join(chunk["content"] for chunk in retrieved_chunks)

    prompt = f"""Tu es un expert. Voici des extraits de documents pertinents :
        {context}
        
        Question : {question}
        Réponds de manière claire et concise, uniquement à partir des documents ci-dessus."""