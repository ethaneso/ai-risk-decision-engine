from typing import Literal
from functools import lru_cache

from fastapi import FastAPI
from pydantic import BaseModel

from src.app.rag_service import RAGService
from src.app.api.routers.risk import (
    router as risk_router,
)

app = FastAPI(
    title="AI Risk Decision Engine",
    version="0.1.0",
)

app.include_router(
    risk_router
)

@lru_cache(maxsize=1)
def get_rag_service() -> RAGService:
    return RAGService()


class QueryRequest(BaseModel):
    question: str
    mode: Literal["offline", "online"] | None = None
    model: str | None = None


@app.get("/")
def root():
    return {
        "name": app.title,
        "version": app.version,
        "status": "running",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/query")
def query(
    request: QueryRequest
):

    return get_rag_service().answer(
        request.question,
        mode=request.mode,
        model=request.model,
    )
