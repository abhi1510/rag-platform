import numpy as np

from app.core.logger import logger


class Retriever:
    def __init__(self, vector_store, embedder):
        self.vector_store = vector_store
        self.embedder = embedder

    def search(self, query, k=5):
        if self.vector_store.index is None:
            return []

        query_embedding = self.embedder.embed([query])

        distances, indices = self.vector_store.index.search(
            np.array(query_embedding), k
        )

        results = []
        for idx in indices[0]:
            results.append(
                {
                    "content": self.vector_store.texts[idx],
                    "metadata": self.vector_store.metadata[idx],
                }
            )

        return results
