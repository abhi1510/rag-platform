from fastapi import APIRouter

from app.ingestion.pipeline import run_ingestion
from app.services.guardrails import sanitize_input
from app.services.rag_service import StaticRAG

router = APIRouter()
rag = StaticRAG()


@router.post("/ingest")
def ingest():
    return run_ingestion("data/")


@router.get("/query")
def query(q: str):
    clean_q = sanitize_input(q)

    if clean_q == "Malicious query detected.":
        return {"error": clean_q}

    return rag.query(clean_q)
