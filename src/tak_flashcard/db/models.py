"""Database models for Tak Flashcard."""

from __future__ import annotations

from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Declarative base class for all ORM models."""


class Word(Base):
    """Represents a vocabulary word with performance metrics."""

    __tablename__ = "words"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    english: Mapped[str] = mapped_column(String, nullable=False, index=True)
    vietnamese: Mapped[str] = mapped_column(String, nullable=False, index=True)
    part_of_speech: Mapped[str | None] = mapped_column(
        String, nullable=True, index=True)
    display_count: Mapped[int] = mapped_column(
        Integer, default=0, nullable=False)
    correct_count: Mapped[int] = mapped_column(
        Integer, default=0, nullable=False)
    difficulty: Mapped[float] = mapped_column(
        Float, default=0.0, nullable=False)

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
