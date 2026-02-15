"""Database models for Tak Flashcard."""

from __future__ import annotations

from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Word(Base):
    """Represents a vocabulary word with performance metrics."""

    __tablename__ = "words"

    id = Column(Integer, primary_key=True, autoincrement=True)
    english = Column(String, nullable=False, index=True)
    vietnamese = Column(String, nullable=False, index=True)
    part_of_speech = Column(String, nullable=True, index=True)
    display_count = Column(Integer, default=0, nullable=False)
    correct_count = Column(Integer, default=0, nullable=False)
    difficulty = Column(Float, default=0.0, nullable=False)

    def to_dict(self) -> dict[str, str | int | float | None]:
        """Convert the word record to a dictionary for UI display."""

        return {
            "id": self.id,
            "english": self.english,
            "vietnamese": self.vietnamese,
            "part_of_speech": self.part_of_speech,
            "display_count": self.display_count,
            "correct_count": self.correct_count,
            "difficulty": self.difficulty,
        }
