import sys

from src.app.retrieval.search import Retriever


def main():

    query = " ".join(sys.argv[1:])

    retriever = Retriever()

    results = retriever.search(
        query,
        k=5
    )

    for i, result in enumerate(
        results,
        start=1
    ):

        print("=" * 60)

        print(f"Rank: {i}")
        print(
            f"Similarity: "
            f"{result['similarity']:.4f}"
        )

        print(
            f"Page: "
            f"{result['page_number']}"
        )

        print()

        print(result["content"])


if __name__ == "__main__":
    main()