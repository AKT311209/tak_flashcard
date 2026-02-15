"""Flashcard session state definitions."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from tak_flashcard.constants import Direction, Mode
from tak_flashcard.core.scoring import PENALTY_POINTS
from tak_flashcard.db.models import Word


@dataclass
class ShowAnswerConfig:
    """Configuration for how show-answer penalties operate."""

    enabled: bool = True
    score_penalty: int = 0
    max_uses: Optional[int] = None
    time_penalty: int = 0


@dataclass
class FlashcardState:
    """Represents the current session state."""

    mode: Mode
    direction: Direction
    difficulty: int
    question_limit: Optional[int]
    time_limit: Optional[int]
    show_config: ShowAnswerConfig = field(default_factory=ShowAnswerConfig)
    current_word: Optional[Word] = None
    current_direction: Optional[Direction] = None
    current_choices: list[str] = field(default_factory=list)
    score: int = 0
    asked: int = 0
    correct: int = 0
    started_at: Optional[datetime] = None
    finished: bool = False
    show_used: int = 0
    wrong_answer_penalty: int = PENALTY_POINTS


@dataclass
class AnswerResult:
    """Result of an answer validation."""

    is_correct: bool
    correct_answer: str
    new_score: int
    delta: int


@dataclass
class ShowAnswerOutcome:
    """Outcome of a show-answer request."""

    allowed: bool
    score_delta: int
    remaining_uses: Optional[int]
    time_penalty: int
