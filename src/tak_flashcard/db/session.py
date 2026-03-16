"""Database connection setup.

This module opens the connection to the SQLite database file and provides
``SessionLocal`` — a factory for creating database sessions.

A "session" is like a temporary workspace: you read and write data inside
it, and when you're ready the changes are committed (saved) to disk.

The application creates ONE session at startup (in ``gui/app.py``) and
reuses it for the entire lifetime of the app.

Module-level side effects:
    - Calls ``ensure_data_dirs()`` so the ``data/`` folder exists before
      SQLite tries to create the ``.db`` file inside it.
"""

from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from tak_flashcard.config import DB_PATH, ensure_data_dirs
from tak_flashcard.db.models import Base

ensure_data_dirs()

ENGINE = create_engine(f"sqlite:///{DB_PATH}", echo=False, future=True)
SessionLocal = sessionmaker(
    bind=ENGINE, autoflush=False, autocommit=False, future=True)


def init_db() -> None:
    """Create the database tables on first run (safe to call every startup).

    Checks whether the ``words`` table exists and creates it if not.
    If the table is already there, nothing changes — no data is lost.
    Called once during app startup before any data is read or written.
    """

    Base.metadata.create_all(bind=ENGINE)
