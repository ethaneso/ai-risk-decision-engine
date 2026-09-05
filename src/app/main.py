from fastapi import FastAPI
from pydantic import BaseModel

from src.app.rag_service import RAGService

app = FastAPI(
    title="AI Risk Decision Engine",
    version="0.1.0",
)


rag = RAGService()


class QueryRequest(BaseModel):
    question: str


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


@app.post("/query")
def query(
    request: QueryRequest
):

    return rag.answer(
        request.question
    )