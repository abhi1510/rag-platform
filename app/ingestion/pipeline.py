from app.core.logger import logger
from app.ingestion.chunker import chunk_documents
from app.ingestion.loader import load_files
from app.retrieval.embedder import Embedder
from app.retrieval.vector_store import VectorStore


def run_ingestion(data_dir: str):
    docs = load_files(data_dir)
    chunks = chunk_documents(docs)

    logger.info("Loaded docs: %s", len(docs))
    logger.info("Loaded chunks: %s", len(chunks))

    embedder = Embedder()
    embeddings = embedder.embed([doc.page_content for doc in chunks])

    logger.info("Loaded embeddings: %s", len(embeddings))

    store = VectorStore()
    store.build(embeddings, chunks)
    store.save()

    return {"status": "Ingestion complete"}
