"""Database models for the flashcard application."""

from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Word(Base):
    """
    Model representing a vocabulary word.

    Attributes:
        id: Primary key
        english: English word
        pronunciation: IPA pronunciation guide
        vietnamese: Vietnamese translation
        part_of_speech: Part of speech (noun, verb, etc.)
        display_count: Number of times word was displayed
        correct_count: Number of times answered correctly
        difficulty: Calculated difficulty score (0-1)
    """
    __tablename__ = "words"

    id = Column(Integer, primary_key=True, autoincrement=True)
    english = Column(String, nullable=False, index=True)
    pronunciation = Column(String, nullable=False)
    vietnamese = Column(String, nullable=False, index=True)
    part_of_speech = Column(String, nullable=False, index=True)
    display_count = Column(Integer, default=0, nullable=False)
    correct_count = Column(Integer, default=0, nullable=False)
    difficulty = Column(Float, default=1.0, nullable=False)

    def __repr__(self):
        return f"<Word(english='{self.english}', vietnamese='{self.vietnamese}')>"


class Session(Base):
    """
    Model representing a flashcard session (optional, for history tracking).

    Attributes:
        id: Primary key
        mode: Flashcard mode (endless/speed/testing)
        direction: Translation direction
        difficulty_setting: Difficulty level (1-5)
        question_count: Total questions (for testing mode)
        time_limit: Time limit in seconds (for speed mode)
        start_time: Session start timestamp
        end_time: Session end timestamp
        score: Final score
        correct_count: Number of correct answers
        total_count: Total questions answered
    """
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    mode = Column(String, nullable=False)
    direction = Column(String, nullable=False)
    difficulty_setting = Column(Integer, nullable=False)
    question_count = Column(Integer, nullable=True)
    time_limit = Column(Integer, nullable=True)
    start_time = Column(DateTime, default=datetime.utcnow, nullable=False)
    end_time = Column(DateTime, nullable=True)
    score = Column(Integer, default=0, nullable=False)
    correct_count = Column(Integer, default=0, nullable=False)
    total_count = Column(Integer, default=0, nullable=False)

    def __repr__(self):
        return f"<Session(mode='{self.mode}', score={self.score})>"
