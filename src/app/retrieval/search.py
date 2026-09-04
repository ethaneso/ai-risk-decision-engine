from src.app.retrieval.database import get_connection
from src.app.retrieval.embedder import Embedder


class Retriever:

    def __init__(self):
        self.embedder = Embedder()

    def search(
        self,
        query: str,
        k: int = 10
    ):

        query_vector = self.embedder.embed_query(
            query
        )

        with get_connection() as conn:

            with conn.cursor() as cur:

                cur.execute(
                    """
                    SELECT
                        id,
                        document_id,
                        content,
                        page_number,
                        1 - (
                            embedding <=> %s::vector
                        ) AS similarity
                    FROM chunks
                    ORDER BY
                        embedding <=> %s::vector
                    LIMIT %s
                    """,
                    (
                        query_vector.tolist(),
                        query_vector.tolist(),
                        k
                    )
                )

                rows = cur.fetchall()

        return [
            {
                "id": str(row[0]),
                "document_id": str(row[1]),
                "content": row[2],
                "page_number": row[3],
                "similarity": float(row[4])
            }
            for row in rows
        ]