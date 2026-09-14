from functools import lru_cache

from langchain.tools import tool

from src.app.retrieval.pipeline import RetrievalPipeline


@lru_cache(maxsize=1)
def get_retrieval_pipeline() -> RetrievalPipeline:
    return RetrievalPipeline()


@tool
def search_evidence(
    query: str,
    top_k: int = 5,
) -> dict:
    """
    Search indexed cybersecurity, governance, policy,
    compliance, and risk documents for relevant evidence.

    Use this tool when the user's question requires
    evidence from the document corpus.
    """

    results = get_retrieval_pipeline().retrieve(
        query=query,
        top_k=max(top_k, 10),
        top_n=top_k,
    )

    evidence = []

    for result in results:
        evidence.append(
            {
                "chunk_id": str(
                    result.get("id", "")
                ),
                "document_id": str(
                    result.get(
                        "document_id",
                        "",
                    )
                ),
                "content": result["content"],
                "source": result.get("source"),
                "similarity": result.get(
                    "similarity"
                ),
                "rerank_score": result.get(
                    "rerank_score"
                ),
                "page_number": result.get(
                    "page_number"
                ),
            }
        )

    return {
        "query": query,
        "result_count": len(evidence),
        "evidence": evidence,
    }
