import os
import pickle

import faiss
import numpy as np

from app.core.config import settings


class VectorStore:
    def __init__(self):
        self.index = None
        self.texts = []
        self.metadata = []

    def build(self, embeddings, documents):
        dim = len(embeddings[0])
        self.index = faiss.IndexFlatL2(dim)

        self.index.add(np.array(embeddings))
        self.texts = [doc.page_content for doc in documents]
        self.metadata = [doc.metadata for doc in documents]

    def save(self):
        os.makedirs(settings.VECTOR_DB_PATH, exist_ok=True)
        faiss.write_index(self.index, f"{settings.VECTOR_DB_PATH}/index.faiss")

        with open(f"{settings.VECTOR_DB_PATH}/store.pkl", "wb") as f:
            pickle.dump((self.texts, self.metadata), f)

    def load(self):
        index_path = f"{settings.VECTOR_DB_PATH}/index.faiss"
        store_path = f"{settings.VECTOR_DB_PATH}/store.pkl"

        if not os.path.exists(index_path) or not os.path.exists(store_path):
            raise FileNotFoundError(
                "Vector store not found. Please run ingestion first."
            )

        self.index = faiss.read_index(index_path)

        with open(store_path, "rb") as f:
            self.texts, self.metadata = pickle.load(f)
