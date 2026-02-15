"""Database session management."""

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
    """Create database tables if they do not exist."""

    Base.metadata.create_all(bind=ENGINE)
