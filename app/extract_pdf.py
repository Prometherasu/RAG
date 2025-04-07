#from langchain_community.document_loaders import PyMuPDFLoader
import os
import json

import pymupdf4llm
import pathlib
from langchain.text_splitter import MarkdownTextSplitter

# faire la detection des nouveau pdf pour evite de tout refaire a cahque fois ?
def get_pdf_names(folder_path="data/pdf"):
    pdf_names = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            pdf_names.append(filename)
    return pdf_names

def get_pdf_paths(folder_path="data/pdf"):
    pdf_paths = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            pdf_paths.append(os.path.join(folder_path, filename))
    return pdf_paths
print(get_pdf_paths())




def to_markdown(pdf_paths, output_folder="data/markdown"):
    os.makedirs(output_folder, exist_ok=True)

    for pdf_path in pdf_paths:
        filename = os.path.basename(pdf_path)
        base_name = os.path.splitext(filename)[0]
        md_text = pymupdf4llm.to_markdown(pdf_path)

        output_path = os.path.join(output_folder, f"{base_name}.md")

        pathlib.Path(output_path).write_bytes(md_text.encode("utf-8"))
        print(f" Markdown sauvegardé : {output_path}")


#to_markdown(get_pdf_paths())