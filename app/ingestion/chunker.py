from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.core.config import settings


def chunk_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE, chunk_overlap=settings.CHUNK_OVERLAP
    )

    texts = [doc["content"] for doc in documents]
    metadatas = [doc["metadata"] for doc in documents]

    return splitter.create_documents(texts, metadatas)
