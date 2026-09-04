import sys

from src.app.ingestion.indexer import Indexer


def main():

    if len(sys.argv) != 2:
        print(
            "Usage: python scripts/ingest.py <pdf>"
        )
        sys.exit(1)

    path = sys.argv[1]

    indexer = Indexer()

    result = indexer.index_pdf(path)

    print(result)


if __name__ == "__main__":
    main()