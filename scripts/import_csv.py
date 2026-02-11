#!/usr/bin/env python3
"""Import vocabulary words from CSV or XLSX file."""

import argparse
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from tak_flashcard.db.db import get_db, init_db
from tak_flashcard.importers.csv_importer import import_csv


def main():
    """Import vocabulary from file."""
    parser = argparse.ArgumentParser(
        description="Import vocabulary words from CSV or XLSX file"
    )
    parser.add_argument("file", help="Path to CSV or XLSX file")
    parser.add_argument(
        "--batch-size",
        type=int,
        default=500,
        help="Batch size for database inserts (default: 500)",
    )

    args = parser.parse_args()

    # Initialize database if needed
    init_db()

    print(f"Importing from: {args.file}")
    print(f"Batch size: {args.batch_size}")
    print("-" * 50)

    try:
        db = get_db()
        stats = import_csv(args.file, db, batch_size=args.batch_size)

        print("-" * 50)
        print(f"✓ Import completed!")
        print(f"  - Added: {stats['added']}")
        print(f"  - Skipped: {stats['skipped']}")
        print(f"  - Errors: {stats['errors']}")

    except FileNotFoundError:
        print(f"✗ Error: File not found: {args.file}")
        sys.exit(1)
    except ValueError as e:
        print(f"✗ Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error importing file: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
