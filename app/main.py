from fastapi import FastAPI

from app.api.routes import router

app = FastAPI(title="ContextStream - Static RAG")

app.include_router(router)
