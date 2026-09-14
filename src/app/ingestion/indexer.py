import hashlib
import uuid
from pathlib import Path

from src.app.ingestion.parser import parse_pdf
from src.app.ingestion.cleaner import clean_text
from src.app.ingestion.chunker import chunk_text
from src.app.retrieval.embedder import Embedder
from src.app.retrieval.database import get_connection


SUPPORTED_EXTENSIONS = {
    ".pdf",
}


def calculate_sha256(
    path: Path,
    buffer_size: int = 1024 * 1024,
) -> str:
    """
    Calculate SHA-256 checksum for a source document.

    The checksum identifies document content rather than
    relying only on the filename.
    """

    digest = hashlib.sha256()

    with path.open("rb") as file:

        while data := file.read(buffer_size):
            digest.update(data)

    return digest.hexdigest()


class Indexer:

    def __init__(self):
        self.embedder = Embedder()

    def index_document(
        self,
        path: str | Path,
        force: bool = False,
        dry_run: bool = False,
    ) -> dict:

        path = Path(path)

        # --------------------------------------------------
        # 1. Validate input
        # --------------------------------------------------

        if not path.exists():
            raise FileNotFoundError(
                f"Document does not exist: {path}"
            )

        if not path.is_file():
            raise ValueError(
                f"Expected a file, got: {path}"
            )

        suffix = path.suffix.lower()

        if suffix not in SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Unsupported document type: {suffix}"
            )

        # --------------------------------------------------
        # 2. Calculate document checksum
        # --------------------------------------------------

        checksum = calculate_sha256(path)

        # --------------------------------------------------
        # 3. Check whether identical content already exists
        # --------------------------------------------------

        existing_document = self._find_by_sha256(
            checksum
        )

        if existing_document and not force:

            return {
                "status": "skipped",
                "reason": "content_already_indexed",
                "sha256": checksum,
                "document_id": str(
                    existing_document["id"]
                ),
                "path": str(path),
            }

        # A checksum identifies identical bytes. The filename is the stable
        # logical identity used to detect a revised version of a document.
        existing_source = self._find_by_filename(
            path.name
        )

        # --------------------------------------------------
        # 4. Parse document
        # --------------------------------------------------

        pages = self._parse_document(path)

        # --------------------------------------------------
        # 5. Clean and chunk
        # --------------------------------------------------

        all_chunks = []

        global_chunk_index = 0

        for page in pages:

            cleaned = clean_text(
                page["text"]
            )

            chunks = chunk_text(
                cleaned
            )

            for chunk in chunks:

                all_chunks.append(
                    {
                        "content": chunk,
                        "page_number": page[
                            "page_number"
                        ],
                        "chunk_index":
                            global_chunk_index,
                    }
                )

                global_chunk_index += 1

        # --------------------------------------------------
        # 6. Dry-run stops before embeddings / DB writes
        # --------------------------------------------------

        if dry_run:

            return {
                "status": "dry_run",
                "path": str(path),
                "filename": path.name,
                "sha256": checksum,
                "pages": len(pages),
                "chunks": len(all_chunks),
            }

        if not all_chunks:

            raise ValueError(
                f"No chunks were produced for {path}"
            )

        # --------------------------------------------------
        # 7. Batch embedding
        # --------------------------------------------------

        texts = [
            chunk["content"]
            for chunk in all_chunks
        ]

        embeddings = (
            self.embedder.embed_documents(
                texts
            )
        )

        if len(embeddings) != len(all_chunks):

            raise RuntimeError(
                "Embedding count does not match "
                "chunk count."
            )

        # --------------------------------------------------
        # 8. Write atomically to PostgreSQL
        # --------------------------------------------------

        with get_connection() as conn:

            try:

                with conn.cursor() as cur:

                    # Delete the prior logical document in the same
                    # transaction. ON DELETE CASCADE removes its old chunks,
                    # so stale vectors are never left in the index.
                    document_to_replace = (
                        existing_document
                        if existing_document and force
                        else existing_source
                    )

                    if document_to_replace:

                        cur.execute(
                            """
                            DELETE FROM documents
                            WHERE id = %s
                            """,
                            (
                                document_to_replace[
                                    "id"
                                ],
                            ),
                        )

                    document_id = uuid.uuid4()

                    cur.execute(
                        """
                        INSERT INTO documents
                        (
                            id,
                            filename,
                            source_path,
                            sha256,
                            status,
                            indexed_at
                        )
                        VALUES
                        (
                            %s,
                            %s,
                            %s,
                            %s,
                            %s,
                            NOW()
                        )
                        """,
                        (
                            document_id,
                            path.name,
                            str(path),
                            checksum,
                            "indexing",
                        ),
                    )

                    # --------------------------------------
                    # 9. Insert chunks + embeddings
                    # --------------------------------------

                    for chunk, embedding in zip(
                        all_chunks,
                        embeddings,
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
                                chunk[
                                    "chunk_index"
                                ],
                                chunk["content"],
                                chunk[
                                    "page_number"
                                ],
                                embedding.tolist(),
                            ),
                        )

                    # --------------------------------------
                    # 10. Mark document indexed
                    # --------------------------------------

                    cur.execute(
                        """
                        UPDATE documents
                        SET
                            status = 'indexed',
                            indexed_at = NOW()
                        WHERE id = %s
                        """,
                        (
                            document_id,
                        ),
                    )

                conn.commit()

            except Exception:

                conn.rollback()

                raise

        rebuilt = bool(
            (existing_document and force)
            or existing_source
        )

        return {
            "status": (
                "rebuilt"
                if rebuilt
                else "indexed"
            ),
            "document_id": str(
                document_id
            ),
            "filename": path.name,
            "path": str(path),
            "pages": len(pages),
            "chunks": len(all_chunks),
            "sha256": checksum,
        }

    def _parse_document(
        self,
        path: Path,
    ):

        suffix = path.suffix.lower()

        if suffix == ".pdf":

            return parse_pdf(
                str(path)
            )

        raise ValueError(
            f"No parser implemented for {suffix}"
        )

    def _find_by_sha256(
        self,
        checksum: str,
    ):

        with get_connection() as conn:

            with conn.cursor() as cur:

                cur.execute(
                    """
                    SELECT
                        id,
                        filename,
                        source_path,
                        sha256,
                        status
                    FROM documents
                    WHERE sha256 = %s
                    LIMIT 1
                    """,
                    (
                        checksum,
                    ),
                )

                row = cur.fetchone()

        if row is None:
            return None

        return {
            "id": row[0],
            "filename": row[1],
            "source_path": row[2],
            "sha256": row[3],
            "status": row[4],
        }

    def _find_by_filename(
        self,
        filename: str,
    ):

        with get_connection() as conn:

            with conn.cursor() as cur:

                cur.execute(
                    """
                    SELECT
                        id,
                        filename,
                        source_path,
                        sha256,
                        status
                    FROM documents
                    WHERE
                        filename = %s
                        OR regexp_replace(
                            filename,
                            '^.*/',
                            ''
                        ) = %s
                    ORDER BY
                        CASE
                            WHEN filename = %s THEN 0
                            ELSE 1
                        END
                    LIMIT 1
                    """,
                    (
                        filename,
                        filename,
                        filename,
                    ),
                )

                row = cur.fetchone()

        if row is None:
            return None

        return {
            "id": row[0],
            "filename": row[1],
            "source_path": row[2],
            "sha256": row[3],
            "status": row[4],
        }

    # Temporary backward compatibility
    def index_pdf(
        self,
        path: str | Path,
    ) -> dict:

        return self.index_document(
            path=path
        )
