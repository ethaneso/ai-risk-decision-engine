import argparse
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from src.app.ingestion.indexer import Indexer


SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".md",
    ".txt",
}


def parse_args():
    parser = argparse.ArgumentParser(
        description="Ingest documents into the AI Risk Decision Engine RAG index."
    )

    parser.add_argument(
        "path",
        type=Path,
        help="Document or directory to ingest.",
    )

    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Recursively scan directories for supported documents.",
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-index documents even if their content has not changed.",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Parse and inspect documents without writing to the database.",
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print detailed ingestion information.",
    )

    return parser.parse_args()


def collect_documents(
    path: Path,
    recursive: bool,
) -> list[Path]:

    if not path.exists():
        raise FileNotFoundError(
            f"Path does not exist: {path}"
        )

    if path.is_file():
        if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Unsupported file type: {path.suffix}"
            )

        return [path]

    iterator = (
        path.rglob("*")
        if recursive
        else path.glob("*")
    )

    return sorted(
        file
        for file in iterator
        if file.is_file()
        and file.suffix.lower() in SUPPORTED_EXTENSIONS
    )


def main():
    args = parse_args()

    documents = collect_documents(
        args.path,
        args.recursive,
    )

    if not documents:
        print("No supported documents found.")
        return

    indexer = Indexer()

    print(
        f"Found {len(documents)} document(s)."
    )

    succeeded = 0
    rebuilt = 0
    skipped = 0
    failed = 0

    for path in documents:

        try:
            result = indexer.index_document(
                path=path,
                force=args.force,
                dry_run=args.dry_run,
            )

            status = result.get(
                "status",
                "unknown",
            )

            if status == "indexed":
                succeeded += 1

            elif status == "rebuilt":
                rebuilt += 1

            elif status == "skipped":
                skipped += 1

            if args.verbose or status != "indexed":
                print(
                    f"[{status.upper()}] "
                    f"{path}: {result}"
                )
            else:
                print(
                    f"[INDEXED] {path}"
                )

        except Exception as exc:
            failed += 1

            print(
                f"[FAILED] {path}: {exc}"
            )

    print()
    print("Ingestion summary")
    print("-----------------")
    print(f"Indexed : {succeeded}")
    print(f"Rebuilt : {rebuilt}")
    print(f"Skipped : {skipped}")
    print(f"Failed  : {failed}")


if __name__ == "__main__":
    main()
