#!/usr/bin/env python3
"""Initialize the database and create all tables."""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from tak_flashcard.db.db import init_db


def main():
    """Initialize the database."""
    print("Initializing database...")

    try:
        init_db()
        print("✓ Database initialized successfully")
        print("✓ All tables created")
    except Exception as e:
        print(f"✗ Error initializing database: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
