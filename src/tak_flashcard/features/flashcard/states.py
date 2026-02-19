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
    answered: int = 0
    correct: int = 0
    started_at: Optional[datetime] = None
    finished: bool = False
    show_used: int = 0
    wrong_answer_penalty: int = PENALTY_POINTS
    time_used: Optional[int] = None


@dataclass
class SessionSummary:
    """Aggregated statistics for a completed flashcard session.

    Attributes:
        mode: Study mode that was used.
        correct: Number of correctly answered questions.
        asked: Total number of questions actually resolved by the user
            (submitted or revealed); excludes any card displayed but not yet
            acted upon when the session ended.
        percent_correct: Correct answers as a percentage of total asked.
        score: Final session score.
        time_used: Seconds of active play time (Speed mode only; None otherwise).
        show_used: Number of times Show Answer was used.
    """

    mode: Mode
    correct: int
    asked: int
    percent_correct: float
    score: int
    time_used: Optional[int]
    show_used: int


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
