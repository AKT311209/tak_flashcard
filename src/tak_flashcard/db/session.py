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

    try:
        engine = create_engine(
            f"sqlite:///{DB_PATH}",
            connect_args={"check_same_thread": False},
            echo=False,
            future=True,
        )

        # create tables if they don't exist
        Base.metadata.create_all(bind=engine)

        SessionLocal = scoped_session(
            sessionmaker(autocommit=False, autoflush=False,
                         bind=engine, expire_on_commit=False, future=True)
        )

        return engine
    except Exception as e:
        print(f"[tak_flashcard] Failed to initialize database engine: {e}")
        raise


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
