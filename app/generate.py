from transformers import AutoTokenizer, AutoModelForSeq2SeqLM #, AutoModelForCausalLM
import torch

model_name = "google/flan-t5-base"
tokenizer = AutoTokenizer.from_pretrained(model_name)
#model = AutoModelForCausalLM.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)


def generate_answer(query, retrieved_chunks, max_tokens=512):
    context = "\n---\n".join(chunk["content"] for chunk in retrieved_chunks)
    prompt = f"""You are an expert in machine learning and information retrieval.

    Here are excerpts from scientific papers:
    {context}

    Answer the following question clearly and concisely using only the documents above.

    Question: {query}
    """
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=1024).to(model.device)
    outputs = model.generate(**inputs, max_new_tokens=max_tokens)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)
