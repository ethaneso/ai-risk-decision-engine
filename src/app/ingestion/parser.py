import pymupdf


def parse_pdf(path: str) -> list[dict]:
    document = pymupdf.open(path)

    pages = []

    for page_number, page in enumerate(document, start=1):
        text = page.get_text("text")

        pages.append({
            "page_number": page_number,
            "text": text
        })

    document.close()

    return pages