"""Data containers that describe the state of a flashcard session.

These are plain Python dataclasses — essentially labelled bundles of data
with no logic of their own.  They are passed between the service layer and
the GUI so each layer only needs to know the data, not each other's internals.

Contents at a glance:
  ShowAnswerConfig  — Settings for how the "Show Answer" button works.
  FlashcardState    — Full live state of an in-progress session
                      (current word, score, counters, timer settings, etc.).
  SessionSummary    — End-of-session statistics snapshot.
  AnswerResult      — Result of one submitted answer.
  ShowAnswerOutcome — Result of one "Show Answer" reveal request.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from tak_flashcard.config import Direction, Mode
from tak_flashcard.core.scoring import PENALTY_POINTS
from tak_flashcard.db.models import Word


@dataclass
class ShowAnswerConfig:
    """Controls how the "Show Answer" button behaves during a session.

    The user can configure whether revealing the answer is allowed and
    what penalty it carries.  This config is built from the options panel
    before the session starts and stays unchanged for the whole session.

    Attributes:
        enabled: ``True`` if the Show Answer button is active in this session.
        score_penalty: Points deducted from the score each time the user
            reveals an answer (0 means no score penalty).
        max_uses: Maximum number of times the user may reveal an answer
            in the whole session.  ``None`` means unlimited.
        time_penalty: Seconds removed from the timer each reveal
            (Speed mode only; 0 means no time penalty).
    """

    enabled: bool = True
    score_penalty: int = 0
    max_uses: Optional[int] = None
    time_penalty: int = 0


@dataclass
class SessionConfig:
    """Configuration used to start and run a flashcard session.

    Attributes:
        mode: Selected study mode.
        direction: Selected translation direction.
        difficulty: Difficulty level from 1 to 5.
        show_config: Rules used when Show Answer is available.
        question_limit: Number of questions for Testing mode, otherwise None.
        time_limit: Time budget in seconds for Speed mode, otherwise None.
        wrong_penalty: Points deducted for wrong answers.
    """

    mode: Mode
    direction: Direction
    difficulty: int
    show_config: ShowAnswerConfig
    question_limit: Optional[int]
    time_limit: Optional[int]
    wrong_penalty: int = PENALTY_POINTS


@dataclass
class FlashcardState:
    """Live snapshot of everything happening in an active flashcard session.

    Created by :meth:`FlashcardService.start_session` and mutated by the
    service as the session progresses.  The GUI reads it (via the controller)
    to know what to display.

    Attributes:
        mode: Which study mode is running (Endless, Speed, or Testing).
        direction: Translation direction chosen for this session.
        difficulty: Difficulty level (1–5) chosen by the user.
        question_limit: Max questions before the session auto-ends.
            ``None`` means unlimited (Endless/Speed modes).
        time_limit: Starting time in seconds (Speed mode only; ``None`` otherwise).
        show_config: Settings for the Show Answer penalty system.
        current_word: The vocabulary word currently on the card (``None`` before
            the first card is drawn).
        current_direction: Resolved direction for the current card — for Mixed
            mode this is either ENG_TO_VN or VN_TO_ENG, chosen randomly.
        current_choices: The four answer options shown on the current card.
        score: Running total of points earned this session.
        asked: Number of cards drawn so far (includes cards the user chose
            to reveal rather than answer).
        answered: Number of answers actually submitted or revealed by the user.
        correct: Number of correctly answered questions.
        started_at: UTC timestamp when the session began.
        finished: ``True`` once the session has reached an end condition.
        show_used: How many times the user has clicked Show Answer.
        wrong_answer_penalty: Points deducted per wrong answer (configurable).
        time_used: Seconds of active play elapsed (Speed mode only; set when
            the session ends).
    """

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
        difficulty: Difficulty level that drove the session.
        show_limit_total: Maximum Show Answer uses enforced by the "limit uses"
            penalty (None if unlimited or not applicable).
    """

    mode: Mode
    correct: int
    asked: int
    percent_correct: float
    score: int
    time_used: Optional[int]
    show_used: int
    difficulty: int
    direction: Direction
    show_score_penalty: int = 0
    show_time_penalty: int = 0
    wrong_penalty: int = PENALTY_POINTS
    show_limit_total: Optional[int] = None


@dataclass
class AnswerResult:
    """What happened immediately after the user submitted an answer.

    Attributes:
        is_correct: ``True`` if the user chose the right answer.
        correct_answer: The text of the correct answer (shown as feedback).
        new_score: The player's updated total score after this answer.
        delta: How many points were gained (+) or lost (−) by this answer.
    """

    is_correct: bool
    correct_answer: str
    new_score: int
    delta: int


@dataclass
class ShowAnswerOutcome:
    """What happened when the user asked to reveal the current answer.

    Attributes:
        allowed: ``True`` if the reveal was permitted (Show Answer is
            enabled and uses haven't been exhausted).
        score_delta: How many points were deducted (negative number, or 0).
        remaining_uses: How many more reveals are allowed this session, or
            ``None`` if there is no cap.
        time_penalty: Seconds that were removed from the timer (Speed mode).
    """

    allowed: bool
    score_delta: int
    remaining_uses: Optional[int]
    time_penalty: int
