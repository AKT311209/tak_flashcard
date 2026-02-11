"""Database connection and initialization module."""

import logging
import os
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import Base

logger = logging.getLogger(__name__)

# Database file location
DB_DIR = Path.home() / ".tak_flashcard"
DB_FILE = DB_DIR / "tak_flashcard.db"

# SQLAlchemy engine and session
engine = None
SessionLocal = None


def get_db_path() -> Path:
    """Get the database file path, ensuring the directory exists."""
    DB_DIR.mkdir(parents=True, exist_ok=True)
    return DB_FILE


def init_db(db_path: str = None) -> None:
    """
    Initialize the database connection and create all tables.

    Args:
        db_path: Optional path to database file. If None, uses default location.
    """
    global engine, SessionLocal

    if db_path is None:
        db_path = get_db_path()

    # Create engine with SQLite-specific settings
    database_url = f"sqlite:///{db_path}"
    engine = create_engine(
        database_url,
        connect_args={"check_same_thread": False},
        echo=False,  # Set to True for SQL logging during development
    )

    # Create session factory
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Create all tables
    Base.metadata.create_all(bind=engine)

    logger.info(f"Database initialized at {db_path}")


def get_session():
    """
    Create and return a new database session.

    Usage:
        with get_session() as session:
            # use session
            pass
    """
    if SessionLocal is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_db():
    """
    Get a database session (for direct use, not as context manager).

    Note: Caller is responsible for closing the session.
    """
    if SessionLocal is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")

    return SessionLocal()
