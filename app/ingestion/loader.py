# app/ingestion/loader.py

import os

import fitz  # PyMuPDF


def load_text_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def load_pdf_file(path):
    doc = fitz.open(path)
    text = ""

    for page in doc:
        text += page.get_text()

    return text


def load_files(data_dir: str):
    documents = []

    for root, _, files in os.walk(data_dir):
        for file in files:
            path = os.path.join(root, file)

            try:
                if file.endswith(".txt"):
                    content = load_text_file(path)

                elif file.endswith(".pdf"):
                    content = load_pdf_file(path)

                else:
                    continue  # skip unsupported files

                documents.append({"content": content, "metadata": {"source": path}})

            except Exception as e:
                print(f"Error processing {path}: {e}")

    return documents
