"""SQLAlchemy database models for Tak Flashcard application."""

from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Word(Base):
    """Word model representing vocabulary entries."""

    __tablename__ = "words"

    id = Column(Integer, primary_key=True, index=True)
    word = Column(String(255), nullable=False, index=True)
    pos = Column(String(50))  # part of speech (noun, verb, adjective, etc.)
    pronunciation = Column(String(255))  # pronunciation guide (IPA)
    vietnamese = Column(Text, nullable=False)  # Vietnamese translation
    english = Column(Text, nullable=False)  # English definition
    difficulty = Column(Integer, default=1, index=True)  # 1-5 scale

    # Relationship
    session_results = relationship("SessionResult", back_populates="word")

    def __repr__(self):
        return f"<Word(id={self.id}, word='{self.word}')>"


class Session(Base):
    """Session model representing a flashcard study session."""

    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    mode = Column(String(50), nullable=False)  # Endless, Speed, Testing
    direction = Column(String(50), nullable=False)  # E->V, V->E, Mixed
    start_ts = Column(String(50))  # ISO timestamp
    end_ts = Column(String(50))  # ISO timestamp
    score = Column(Integer, default=0)
    total_questions = Column(Integer, default=0)

    # Relationship
    results = relationship("SessionResult", back_populates="session")

    def __repr__(self):
        return f"<Session(id={self.id}, mode='{self.mode}', score={self.score})>"


class SessionResult(Base):
    """SessionResult model representing individual question results."""

    __tablename__ = "session_results"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)
    word_id = Column(Integer, ForeignKey("words.id"), nullable=False)
    asked_text = Column(Text, nullable=False)
    expected_answer = Column(Text, nullable=False)
    given_answer = Column(Text)
    correct = Column(Integer, default=0)  # 0 or 1
    revealed = Column(Integer, default=0)  # 0 or 1
    penalty = Column(Integer, default=0)

    # Relationships
    session = relationship("Session", back_populates="results")
    word = relationship("Word", back_populates="session_results")

    def __repr__(self):
        return f"<SessionResult(id={self.id}, correct={self.correct})>"


class Setting(Base):
    """Setting model for persistent application settings."""

    __tablename__ = "settings"

    key = Column(String(100), primary_key=True)
    value = Column(Text)

    def __repr__(self):
        return f"<Setting(key='{self.key}', value='{self.value}')>"
