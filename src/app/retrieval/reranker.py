from sentence_transformers import CrossEncoder


class Reranker:

    def __init__(
        self,
        model_name: str = ("./models/" "ms-marco-MiniLM-L-6-v2")
    ):

        self.model = CrossEncoder(
            model_name
        )

    def rerank(
        self,
        query: str,
        documents: list[dict],
        top_n: int = 5
    ):

        pairs = [
            (
                query,
                document["content"]
            )
            for document in documents
        ]

        scores = self.model.predict(
            pairs
        )

        ranked = sorted(
            zip(documents, scores),
            key=lambda x: x[1],
            reverse=True
        )

        results = []

        for document, score in ranked[:top_n]:

            item = document.copy()

            item["rerank_score"] = float(
                score
            )

            results.append(item)

        return results