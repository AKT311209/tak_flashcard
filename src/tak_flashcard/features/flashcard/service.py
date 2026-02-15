"""Business logic for flashcard sessions."""

from __future__ import annotations

import random
from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from tak_flashcard.constants import Direction, Mode
from tak_flashcard.core.scoring import PENALTY_POINTS, apply_scoring
from tak_flashcard.core.selectors import select_next_word
from tak_flashcard.db import repo
from tak_flashcard.db.models import Word
from tak_flashcard.features.flashcard.states import (
    AnswerResult,
    FlashcardState,
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

        if not self.words:
            return None
        if self.state is None:
            return None
        if self.state.direction == Direction.MIXED:
            direction = random.choice(
                [Direction.ENG_TO_VN, Direction.VN_TO_ENG])
        else:
            direction = self.state.direction
        word = select_next_word(self.words, self.state.difficulty, direction)
        if word:
            self.state.current_word = word
            self.state.current_direction = direction
            self.state.current_choices = self._build_choices(word, direction)
        return word

    def _build_choices(self, word: Word, direction: Direction) -> list[str]:
        """Build shuffled multiple-choice options for the current question.

        Parameters:
            word: The selected vocabulary word for the question prompt.
            direction: Active translation direction for this card.

        Returns:
            A shuffled list containing the correct answer and up to three
            distinct distractors from other words in the dataset.
        """

        if direction == Direction.ENG_TO_VN:
            correct_answer = str(word.vietnamese)
            candidate_pool = {
                str(item.vietnamese)
                for item in self.words
                if str(item.vietnamese).strip()
            }
        else:
            correct_answer = str(word.english)
            candidate_pool = {
                str(item.english)
                for item in self.words
                if str(item.english).strip()
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

        if self.state is None or self.state.current_word is None:
            return None
        active_direction = self.state.current_direction or self.state.direction
        correct_answer = self.state.current_word.vietnamese if active_direction == Direction.ENG_TO_VN else self.state.current_word.english
        is_correct = answer.strip().lower() == correct_answer.strip().lower()
        repo.update_word_stats(self.db, self.state.current_word.id, is_correct)
        scoring = apply_scoring(
            self.state.score,
            is_correct,
            penalty_points=self.state.wrong_answer_penalty,
        )
        self.state.score = scoring.total
        if is_correct:
            self.state.correct += 1
        if self.state.question_limit and self.state.asked >= self.state.question_limit:
            self.state.finished = True
        self.db.commit()
        return AnswerResult(
            is_correct=is_correct,
            correct_answer=correct_answer,
            new_score=self.state.score,
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
