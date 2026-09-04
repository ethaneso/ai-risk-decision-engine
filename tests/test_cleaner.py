from src.app.ingestion.cleaner import clean_text


def test_clean_text():
    text = "Hello    world\n\nthis is   a test."

    result = clean_text(text)

    assert result == "Hello world this is a test."