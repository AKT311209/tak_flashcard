"""Controller to bridge flashcard service and GUI."""

from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from tak_flashcard.constants import Direction, Mode
from tak_flashcard.core.scoring import PENALTY_POINTS
from tak_flashcard.features.flashcard.service import FlashcardService
from tak_flashcard.features.flashcard.states import (
    AnswerResult,
    FlashcardState,
    ShowAnswerConfig,
    ShowAnswerOutcome,
)


class FlashcardController:
    """High-level controller for flashcard interactions."""

    def __init__(self, db: Session):
        """Create controller with provided database session."""

        self.service = FlashcardService(db)

    def start(
        self,
        mode: Mode,
        direction: Direction,
        difficulty: int,
        show_config: ShowAnswerConfig,
        question_limit: Optional[int],
        time_limit: Optional[int],
        wrong_penalty: int = PENALTY_POINTS,
    ) -> FlashcardState:
        """Start a new session with given parameters."""

        return self.service.start_session(
            mode,
            direction,
            difficulty,
            show_config,
            question_limit,
            time_limit,
            wrong_penalty,
        )

    def next_card(self):
        """Move to the next card and return it."""

        return self.service.next_card()

    def submit(self, answer: str) -> Optional[AnswerResult]:
        """Submit an answer for validation."""

        return self.service.submit_answer(answer)

    def reveal(self) -> ShowAnswerOutcome:
        """Reveal the answer and apply penalty."""

        return self.service.show_answer_penalty()

    def finished(self) -> bool:
        """Return whether the session has ended."""

        return self.service.is_finished()
