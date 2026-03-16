"""Thin bridge between the GUI and the flashcard session engine.

The GUI should never call :class:`FlashcardService` directly.  Instead it
uses this controller, which delegates every call one-to-one to the service.

Why a separate controller? It keeps the GUI independent of the service's
internal structure — if the service changes internally, only this file
needs to adapt, not every GUI view.

Calling order:
  gui/views/flashcard_view.py :: FlashcardSessionView
      → FlashcardController.start()        — begin a new session
      → FlashcardController.next_card()    — get the next word
      → FlashcardController.submit()       — submit an answer
      → FlashcardController.reveal()       — reveal the answer (with penalty)
      → FlashcardController.finished()     — check if session is over
      → FlashcardController.get_summary()  — get end-of-session stats
"""

from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from tak_flashcard.features.flashcard.service import FlashcardService
from tak_flashcard.features.flashcard.states import (
    AnswerResult,
    FlashcardState,
    SessionConfig,
    SessionSummary,
    ShowAnswerOutcome,
)


class FlashcardController:
    """Gateway that the GUI uses to run a flashcard session.

    Every public method here is a thin wrapper around the same method on
    :class:`FlashcardService`.  The GUI imports this class and calls these
    methods; it never touches the service or the database directly.
    """

    def __init__(self, db: Session):
        """Create the controller, which in turn creates the session service.

        Parameters:
            db: The shared database session opened by the application.
        """

        self.service = FlashcardService(db)

    def start(self, config: SessionConfig) -> FlashcardState:
        """Start a new flashcard session with the given configuration.

        Parameters:
            config: All session settings (mode, direction, difficulty,
                time limit, question limit, penalty rules).

        Returns:
            The initial :class:`FlashcardState` for the new session.
        """

        return self.service.start_session(config)

    def next_card(self):
        """Ask the service to pick the next word and advance the card counter.

        Returns:
            The selected :class:`Word`, or ``None`` if the session is over.
        """

        return self.service.next_card()

    def submit(self, answer: str) -> Optional[AnswerResult]:
        """Send the user's chosen answer to the service for validation.

        Parameters:
            answer: The text of the option the user selected.

        Returns:
            An :class:`AnswerResult` with correctness, new score, and
            delta, or ``None`` if there is no active question.
        """

        return self.service.submit_answer(answer)

    def reveal(self) -> ShowAnswerOutcome:
        """Ask the service to reveal the current answer (with any penalty).

        Returns:
            A :class:`ShowAnswerOutcome` describing whether the reveal was
            allowed and what penalties were applied.
        """

        return self.service.show_answer_penalty()

    def finished(self) -> bool:
        """Check whether the session has ended.

        Returns:
            ``True`` if the session is over (question limit reached, timer
            expired, or manually ended).
        """

        return self.service.is_finished()

    def get_summary(self) -> Optional[SessionSummary]:
        """Retrieve the end-of-session statistics.

        Returns:
            A :class:`SessionSummary` populated from the session state, or
            ``None`` if no session has been started.
        """

        return self.service.get_summary()
