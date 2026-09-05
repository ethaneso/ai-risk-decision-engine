def build_context(results: list[dict]) -> str:

    sections = []

    for index, result in enumerate(
        results,
        start=1
    ):

        sections.append(
            f"""
SOURCE {index}

Document:
{result['document_id']}

Page:
{result['page_number']}

Content:
{result['content']}
"""
        )

    return "\n".join(sections)