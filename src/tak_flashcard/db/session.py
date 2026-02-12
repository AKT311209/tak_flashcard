"""Database session management."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from tak_flashcard.config import DB_PATH
from tak_flashcard.db.models import Base


engine = None
SessionLocal = None


def init_db():
    """
    Initialize the database engine and create all tables.

    Returns:
        Engine: SQLAlchemy engine instance
    """
    global engine, SessionLocal

    engine = create_engine(
        f"sqlite:///{DB_PATH}",
        connect_args={"check_same_thread": False},
        echo=False
    )

    Base.metadata.create_all(bind=engine)

    SessionLocal = scoped_session(
        sessionmaker(autocommit=False, autoflush=False,
                     bind=engine, expire_on_commit=False)
    )

    return engine


def get_session():
    """
    Get a database session.

    Returns:
        Session: SQLAlchemy session instance
    """
    if SessionLocal is None:
        init_db()
    return SessionLocal()


def close_session(session):
    """
    Close a database session.

    Args:
        session: SQLAlchemy session to close
    """
    if session:
        session.close()
