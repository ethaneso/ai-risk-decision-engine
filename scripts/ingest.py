import sys
from pathlib import Path


# Allow this file to be executed directly (``python scripts/ingest.py``).
# In that mode Python adds ``scripts/`` to sys.path, but not the project root
# that contains the top-level ``src`` package.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

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
