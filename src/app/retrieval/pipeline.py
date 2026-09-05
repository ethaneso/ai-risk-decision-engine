from src.app.retrieval.search import Retriever
from src.app.retrieval.reranker import Reranker


class RetrievalPipeline:

    def __init__(self):

        self.retriever = Retriever()
        self.reranker = Reranker()

    def retrieve(
        self,
        query: str,
        top_k: int = 10,
        top_n: int = 5
    ):

        candidates = self.retriever.search(
            query,
            k=top_k
        )

        results = self.reranker.rerank(
            query,
            candidates,
            top_n=top_n
        )

        return results