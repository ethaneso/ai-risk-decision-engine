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
                        chunks.id,
                        chunks.document_id,
                        chunks.content,
                        chunks.page_number,
                        documents.filename,
                        1 - (
                            chunks.embedding <=> %s::vector
                        ) AS similarity
                    FROM chunks
                    JOIN documents
                      ON documents.id = chunks.document_id
                    ORDER BY
                        chunks.embedding <=> %s::vector
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
                "source": row[4],
                "similarity": float(row[5])
            }
            for row in rows
        ]
