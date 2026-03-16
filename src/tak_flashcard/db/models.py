"""Database table definitions.

This module describes the shape of the data stored on disk.
There is one table: ``words``, holding every vocabulary entry.
SQLAlchemy reads this description and creates/manages the actual
SQLite table automatically.
"""

from __future__ import annotations

from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Declarative base class for all ORM models."""


class Word(Base):
    """One row in the ``words`` table — a single vocabulary word and its stats.

    Each word tracks how often it has been shown and how often the user
    answered it correctly.  These counts feed the difficulty formula so
    the app learns which words to show more or less often.

    Attributes:
        id: Auto-assigned unique number for each word.
        english: The English word (e.g. ``"apple"``).
        vietnamese: The Vietnamese translation (e.g. ``"quả táo"``).
        part_of_speech: Grammar category — noun, verb, adjective, etc.
            Can be empty/missing for older imported data.
        display_count: Total times this word has appeared as a question.
        correct_count: Times the user selected the right answer.
        difficulty: Calculated score from 0.0 (always correct) to ~1.0
            (never correct).  Updated after every answer.
    """

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
        """Return all fields of this word as a plain Python dictionary.

        Useful when the GUI needs to display the data without holding a
        direct reference to the database object.

        Returns:
            A dict with keys: ``id``, ``english``, ``vietnamese``,
            ``part_of_speech``, ``display_count``, ``correct_count``,
            ``difficulty``.
        """

        return {
            "id": self.id,
            "english": self.english,
            "vietnamese": self.vietnamese,
            "part_of_speech": self.part_of_speech,
            "display_count": self.display_count,
            "correct_count": self.correct_count,
            "difficulty": self.difficulty,
        }
