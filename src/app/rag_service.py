from src.app.retrieval.pipeline import RetrievalPipeline
from src.app.generation.prompt import build_context
from src.app.generation.generator import Generator
from src.app.config import settings


class RAGService:

    def __init__(self):

        self.retrieval = RetrievalPipeline()
        self.generator = Generator()

    def answer(
        self,
        question: str,
        mode: str | None = None,
        model: str | None = None,
    ):
        if mode is None:
            provider_modes = {
                "ollama": "offline",
                "openai": "online",
            }
            try:
                mode = provider_modes[settings.llm_provider.lower()]
            except KeyError as exc:
                raise ValueError(
                    "LLM_PROVIDER must be either 'ollama' or 'openai'"
                ) from exc

        results = self.retrieval.retrieve(
            question,
            top_k=10,
            top_n=5
        )

        context = build_context(
            results
        )

        generation = self.generator.generate(
            question,
            context,
            mode=mode,
            model=model,
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
            "answer": generation["answer"],
            "mode": mode,
            "provider": generation["provider"],
            "model": generation["model"],
            "sources": sources,
        }
