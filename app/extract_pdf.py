import os
import pymupdf4llm
import pathlib

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
#print(get_pdf_paths())


# on cree les markdown qui ne sont pas deja cree et onr etourne tout les markdown qui n'on plus de source pdf pour les retirer des chunk
def extract_missing_markdown(pdf_folder="data/pdf", md_folder="data/markdown"):
    os.makedirs(md_folder, exist_ok=True)

    pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith(".pdf")]
    md_basenames = {os.path.splitext(f)[0] for f in os.listdir(md_folder) if f.endswith(".md")}

    for pdf_file in pdf_files:
        base_name = os.path.splitext(pdf_file)[0]

        if base_name not in md_basenames:
            pdf_path = os.path.join(pdf_folder, pdf_file)
            #md_text = pymupdf4llm.to_markdown(pdf_path)
            md_text = to_clean_markdown(pdf_path)

            md_path = os.path.join(md_folder, base_name + ".md")
            pathlib.Path(md_path).write_bytes(md_text.encode("utf-8"))
            print(f"Markdown créé : {md_path}")
        else:
            print(f"Markdown deja crée : {pdf_file}")
        md_basenames.discard(base_name)

    orphans = [os.path.join(md_folder, name + ".md") for name in md_basenames]
    return orphans


def to_clean_markdown(pdf_path):# pas ouf
    md_text = pymupdf4llm.to_markdown(pdf_path)

    cleaned_lines = []
    for line in md_text.splitlines():
        line = line.strip()
        if line.startswith("![") or line.startswith("|") or line.endswith("|"):
            continue
        cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


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