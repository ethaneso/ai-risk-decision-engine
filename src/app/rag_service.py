from src.app.retrieval.pipeline import RetrievalPipeline
from src.app.generation.prompt import build_context
from src.app.generation.generator import Generator


class RAGService:

    def __init__(self):

        self.retrieval = RetrievalPipeline()
        self.generator = Generator()

    def answer(
        self,
        question: str
    ):

        results = self.retrieval.retrieve(
            question,
            top_k=10,
            top_n=5
        )

        context = build_context(
            results
        )

        answer = self.generator.generate(
            question,
            context
        )

        sources = [
            {
                "page": r["page_number"],
                "document_id": r["document_id"],
                "similarity": r["similarity"],
                "rerank_score": r["rerank_score"]
            }
            for r in results
        ]

        return {
            "answer": answer,
            "sources": sources
        }