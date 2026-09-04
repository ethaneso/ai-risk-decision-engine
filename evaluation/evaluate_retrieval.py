import json

from src.app.retrieval.search import Retriever


def evaluate():

    with open(
        "evaluation/questions.json",
        "r"
    ) as f:
        questions = json.load(f)

    retriever = Retriever()

    hits = 0

    for item in questions:

        results = retriever.search(
            item["question"],
            k=5
        )

        found = any(
            r["page_number"]
            == item["expected_page"]
            for r in results
        )

        if found:
            hits += 1

        print(
            item["question"],
            "→",
            "PASS" if found else "FAIL"
        )

    recall_at_5 = hits / len(questions)

    print(
        f"\nRecall@5: "
        f"{recall_at_5:.2%}"
    )


if __name__ == "__main__":
    evaluate()