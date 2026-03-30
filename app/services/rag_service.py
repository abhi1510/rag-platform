from app.core.logger import logger
from app.retrieval.embedder import Embedder
from app.retrieval.retriever import Retriever
from app.retrieval.vector_store import VectorStore
from app.services.llm import LLM
from app.services.prompt import build_prompt


class StaticRAG:
    def __init__(self):
        self.embedder = Embedder()
        self.vector_store = VectorStore()
        self._load_vector_store()
        self.retriever = Retriever(self.vector_store, self.embedder)
        self.llm = LLM()

    def _load_vector_store(self):
        try:
            self.vector_store.load()
        except FileNotFoundError:
            logger.warning("Vector store not found. Run ingestion first.")
            self.vector_store.index = None

    def query(self, question: str):
        logger.info(f"Query: {question}")

        docs = self.retriever.search(question, k=5)
        if not docs:
            return {
                "question": question,
                "answer": "Knowledge base is empty. Please run ingestion first.",
                "sources": [],
            }

        context = "\n\n".join(
            [f"[Source: {d['metadata']['source']}]\n{d['content']}" for d in docs]
        )

        prompt = build_prompt(question, context)

        answer = self.llm.generate(prompt)

        return {
            "question": question,
            "answer": answer,
            "sources": [d["metadata"] for d in docs],
        }
