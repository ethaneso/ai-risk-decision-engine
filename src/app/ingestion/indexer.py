import uuid

from src.app.ingestion.parser import parse_pdf
from src.app.ingestion.cleaner import clean_text
from src.app.ingestion.chunker import chunk_text
from src.app.retrieval.embedder import Embedder
from src.app.retrieval.database import get_connection


class Indexer:

    def __init__(self):
        self.embedder = Embedder()

    def index_pdf(self, path: str):

        document_id = uuid.uuid4()

        pages = parse_pdf(path)

        all_chunks = []

        for page in pages:

            cleaned = clean_text(
                page["text"]
            )

            chunks = chunk_text(cleaned)

            for index, chunk in enumerate(chunks):

                all_chunks.append({
                    "content": chunk,
                    "page_number": page["page_number"],
                    "chunk_index": index
                })

        texts = [
            chunk["content"]
            for chunk in all_chunks
        ]

        embeddings = self.embedder.embed_documents(
            texts
        )

        with get_connection() as conn:

            with conn.cursor() as cur:

                cur.execute(
                    """
                    INSERT INTO documents
                    (id, filename)
                    VALUES (%s, %s)
                    """,
                    (
                        document_id,
                        path
                    )
                )

                for chunk, embedding in zip(
                    all_chunks,
                    embeddings
                ):

                    chunk_id = uuid.uuid4()

                    cur.execute(
                        """
                        INSERT INTO chunks
                        (
                            id,
                            document_id,
                            chunk_index,
                            content,
                            page_number,
                            embedding
                        )
                        VALUES
                        (
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            %s
                        )
                        """,
                        (
                            chunk_id,
                            document_id,
                            chunk["chunk_index"],
                            chunk["content"],
                            chunk["page_number"],
                            embedding.tolist()
                        )
                    )

            conn.commit()

        return {
            "document_id": str(document_id),
            "chunks": len(all_chunks)
        }