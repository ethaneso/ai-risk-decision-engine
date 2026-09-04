from src.app.ingestion.chunker import chunk_text


def test_chunker():
    text = "A" * 5000

    chunks = chunk_text(
        text,
        chunk_size=1000,
        overlap=100
    )

    assert len(chunks) > 1

    for chunk in chunks:
        assert len(chunk) <= 1000