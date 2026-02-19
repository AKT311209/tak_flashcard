"""Business logic for flashcard sessions."""

from __future__ import annotations

import random
from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from tak_flashcard.config import Direction, Mode
from tak_flashcard.core.scoring import PENALTY_POINTS, apply_scoring
from tak_flashcard.core.selectors import select_next_word
from tak_flashcard.db import repo
from tak_flashcard.db.models import Word
from tak_flashcard.features.flashcard.states import (
    AnswerResult,
    FlashcardState,
    SessionSummary,
    ShowAnswerConfig,
    ShowAnswerOutcome,
)


class FlashcardService:
    """Manage flashcard session lifecycle and logic."""

    def __init__(self, db: Session):
        """Create service bound to a database session."""

        self.db = db
        self.words: list[Word] = []
        self.state: Optional[FlashcardState] = None

    def load_words(self) -> None:
        """Load all words into memory."""

        self.words = repo.list_words(self.db)

    def start_session(
        self,
        mode: Mode,
        direction: Direction,
        difficulty: int,
        show_config: ShowAnswerConfig,
        question_limit: Optional[int] = None,
        time_limit: Optional[int] = None,
        wrong_penalty: int = PENALTY_POINTS,
    ) -> FlashcardState:
        """Initialize a new session and return its state."""

        self.load_words()
        self.state = FlashcardState(
            mode=mode,
            direction=direction,
            difficulty=difficulty,
            question_limit=question_limit,
            time_limit=time_limit,
            show_config=show_config,
            current_word=None,
            score=0,
            asked=0,
            correct=0,
            started_at=datetime.utcnow(),
            finished=False,
            wrong_answer_penalty=wrong_penalty,
        )
        return self.state

    def _pick_word(self) -> Optional[Word]:
        """Select the next word respecting direction and difficulty."""

        state = self.state
        if state is None or not self.words:
            return None
        direction = self._resolve_direction(state.direction)
        word = select_next_word(self.words, state.difficulty, direction)
        if word is not None:
            state.current_word = word
            state.current_direction = direction
            state.current_choices = self._build_choices(word, direction)
        return word

    @staticmethod
    def _resolve_direction(direction: Direction) -> Direction:
        """Resolve mixed direction into a concrete direction for a card."""

        if direction == Direction.MIXED:
            return random.choice([Direction.ENG_TO_VN, Direction.VN_TO_ENG])
        return direction

    @staticmethod
    def _answer_for(word: Word, direction: Direction) -> str:
        """Return the expected answer text for a word and direction."""

        return (
            str(word.vietnamese)
            if direction == Direction.ENG_TO_VN
            else str(word.english)
        )

    def _build_choices(self, word: Word, direction: Direction) -> list[str]:
        """Build shuffled multiple-choice options for the current question.

        Parameters:
            word: The selected vocabulary word for the question prompt.
            direction: Active translation direction for this card.

        Returns:
            A shuffled list containing the correct answer and up to three
            distinct distractors from other words in the dataset.
        """

        correct_answer = self._answer_for(word, direction)
        candidate_pool = {
            value
            for item in self.words
            if (value := self._answer_for(item, direction)).strip()
        }

        candidate_pool.discard(correct_answer)
        candidate_list = list(candidate_pool)
        distractor_count = min(3, len(candidate_list))
        distractors = random.sample(candidate_list, distractor_count)

        choices = [correct_answer, *distractors]
        random.shuffle(choices)
        return choices

    def next_card(self) -> Optional[Word]:
        """Advance to the next card and update asked counter."""

        if self.state is None:
            return None
        if self.state.question_limit and self.state.asked >= self.state.question_limit:
            self.state.finished = True
            return None
        word = self._pick_word()
        if word:
            self.state.asked += 1
        return word

    def submit_answer(self, answer: str) -> Optional[AnswerResult]:
        """Validate an answer, update stats, and return result."""

        state = self.state
        if state is None or state.current_word is None:
            return None
        active_direction = state.current_direction or state.direction
        correct_answer = self._answer_for(state.current_word, active_direction)
        is_correct = answer.strip().lower() == correct_answer.strip().lower()
        repo.update_word_stats(self.db, state.current_word.id, is_correct)
        scoring = apply_scoring(
            state.score,
            is_correct,
            penalty_points=state.wrong_answer_penalty,
        )
        state.score = scoring.total
        state.answered += 1
        if is_correct:
            state.correct += 1
        if state.question_limit and state.asked >= state.question_limit:
            state.finished = True
        self.db.commit()
        return AnswerResult(
            is_correct=is_correct,
            correct_answer=correct_answer,
            new_score=state.score,
            delta=scoring.delta,
        )

    def show_answer_penalty(self) -> ShowAnswerOutcome:
        """Apply a penalty for revealing an answer and report the outcome."""

        if self.state is None:
            return ShowAnswerOutcome(False, 0, None, 0)
        config = self.state.show_config
        if not config.enabled:
            return ShowAnswerOutcome(False, 0, None, 0)
        if config.max_uses is not None and self.state.show_used >= config.max_uses:
            return ShowAnswerOutcome(False, 0, 0, 0)
        penalty = config.score_penalty
        self.state.score -= penalty
        self.state.answered += 1
        self.state.show_used += 1
        remaining_uses = None
        if config.max_uses is not None:
            remaining_uses = max(config.max_uses - self.state.show_used, 0)
        time_penalty = max(config.time_penalty, 0)
        return ShowAnswerOutcome(
            allowed=True,
            score_delta=-penalty,
            remaining_uses=remaining_uses,
            time_penalty=time_penalty,
        )

    def is_finished(self) -> bool:
        """Return whether the session has reached an end condition."""

        if self.state is None:
            return True
        return bool(self.state.finished)

    def get_summary(self) -> Optional[SessionSummary]:
        """Build and return a summary of the current or completed session.

        Returns:
            A :class:`SessionSummary` populated from the current state, or
            ``None`` if no session has been started.
        """

        if self.state is None:
            return None
        s = self.state
        percent = round(s.correct / s.answered * 100, 1) if s.answered > 0 else 0.0
        show_limit_total: Optional[int] = None
        if (
            s.mode in (Mode.ENDLESS, Mode.SPEED)
            and s.show_config.max_uses is not None
            and s.show_config.max_uses > 0
        ):
            show_limit_total = s.show_config.max_uses
        return SessionSummary(
            mode=s.mode,
            correct=s.correct,
            asked=s.answered,
            percent_correct=percent,
            score=s.score,
            time_used=s.time_used,
            show_used=s.show_used,
            difficulty=s.difficulty,
            show_limit_total=show_limit_total,
        )
