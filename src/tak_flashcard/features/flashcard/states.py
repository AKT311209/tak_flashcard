"""Flashcard session state definitions."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from tak_flashcard.constants import Direction, Mode
from tak_flashcard.db.models import Word


@dataclass
class FlashcardState:
    """Represents the current session state."""

    mode: Mode
    direction: Direction
    difficulty: int
    question_limit: Optional[int]
    time_limit: Optional[int]
    current_word: Optional[Word] = None
    current_direction: Optional[Direction] = None
    score: int = 0
    asked: int = 0
    correct: int = 0
    started_at: Optional[datetime] = None
    finished: bool = False


@dataclass
class AnswerResult:
    """Result of an answer validation."""

    is_correct: bool
    correct_answer: str
    new_score: int
    delta: int
