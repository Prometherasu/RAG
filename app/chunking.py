import os
import json
from langchain.text_splitter import MarkdownTextSplitter


def chunk_markdown_file(md_path, chunk_size=300, chunk_overlap=50):
    with open(md_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    splitter = MarkdownTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    documents = splitter.create_documents([md_text])

    chunks = []
    for i, doc in enumerate(documents):
        chunks.append({
            "chunk_id": i,
            "content": doc.page_content,
            "metadata": {
                "source": os.path.basename(md_path)
            }
        })

    return chunks


def process_all_markdown(input_folder="data/markdown", output_folder="data/chunks_json"):
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if filename.endswith(".md"):
            md_path = os.path.join(input_folder, filename)
            chunks = chunk_markdown_file(md_path)

            json_path = os.path.join(output_folder, filename.replace(".md", ".json"))
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(chunks, f, ensure_ascii=False, indent=2)

            print(f" Chunks enregistrés : {json_path}")

process_all_markdown()
