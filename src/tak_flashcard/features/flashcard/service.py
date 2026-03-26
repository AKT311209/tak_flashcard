"""The engine that runs a flashcard session.

This module does all the work:
  - Loading vocabulary words from the database into memory.
  - Picking the next word and building the four answer choices.
  - Checking whether the user's answer is correct.
  - Updating word difficulty statistics in the database.
  - Applying the scoring rules.
  - Knowing when the session is over and building the summary.

It is the only "brain" layer — the GUI calls it through a controller but
never talks to the database directly.

Calling order (typical session):
  FlashcardController  (features/flashcard/controller.py)
      → FlashcardService.start_session()   — set up a new session
      → FlashcardService.next_card()       — get the next word to display
          → _pick_word()
              → core/selectors.py :: select_next_word()
              → _build_choices()
      → FlashcardService.submit_answer()   — process the user's selection
          → db/repo.py :: update_word_stats()
          → core/scoring.py :: apply_scoring()
      → FlashcardService.get_summary()     — build end-of-session stats
"""

from __future__ import annotations

import random
from collections import deque
from dataclasses import dataclass
from datetime import datetime
from typing import Deque, Optional

from sqlalchemy.orm import Session

from tak_flashcard.config import Direction, Mode
from tak_flashcard.core.scoring import PENALTY_POINTS, apply_scoring
from tak_flashcard.core.selectors import select_next_word
from tak_flashcard.db import repo
from tak_flashcard.db.models import Word
from tak_flashcard.features.flashcard.states import (
    AnswerResult,
    FlashcardState,
    SessionConfig,
    SessionSummary,
    ShowAnswerOutcome,
)


@dataclass
class _PreparedCard:
    """Pre-rendered question payload used for fast card delivery.

    Attributes:
        word: The selected vocabulary record for this card.
        direction: The resolved direction for this specific question.
        choices: The shuffled answer options to render.
    """

    word: Word
    direction: Direction
    choices: list[str]


class FlashcardService:
    """Manages the full lifecycle of a flashcard session.

    On :meth:`start_session` all vocabulary words are loaded into memory
    and a fresh :class:`FlashcardState` is created.  Subsequent calls to
    :meth:`next_card`, :meth:`submit_answer`, and :meth:`show_answer_penalty`
    advance the session, update stats, and keep state in sync.

    One instance is created at app startup and reused across sessions
    (it reloads words and resets state on each :meth:`start_session` call).
    """

    def __init__(self, db: Session):
        """Bind the service to a database session.

        Parameters:
            db: The shared database session opened once by the application.
        """

        self.db = db
        self.words: list[Word] = []
        self.state: Optional[FlashcardState] = None
        self._pre_rendered_cards: Deque[_PreparedCard] = deque()

    def load_words(self) -> None:
        """Fetch all vocabulary from the database into memory.

        Storing words in memory (``self.words``) avoids repeated DB queries
        during a session.  Called automatically by :meth:`start_session`.
        """

        self.words = repo.list_words(self.db)

    def start_session(self, config: SessionConfig) -> FlashcardState:
        """Set up a brand-new session from the provided configuration.

        Loads all words from the database into memory, then creates a fresh
        :class:`FlashcardState` using the settings in ``config``.  Any
        previous session data is discarded.

        Parameters:
            config: Session settings (mode, direction, difficulty, limits,
                penalty rules).

        Returns:
            The newly created :class:`FlashcardState`.
        """

        self.load_words()
        self.state = FlashcardState(
            mode=config.mode,
            direction=config.direction,
            difficulty=config.difficulty,
            question_limit=config.question_limit,
            time_limit=config.time_limit,
            show_config=config.show_config,
            current_word=None,
            score=0,
            asked=0,
            correct=0,
            started_at=datetime.utcnow(),
            finished=False,
            wrong_answer_penalty=config.wrong_penalty,
        )
        self._pre_rendered_cards = deque()
        self._prime_pre_rendered_cards()
        return self.state

    def _target_pre_render_count(self) -> int:
        """Return how many cards should be pre-rendered for the active session.

        Testing sessions pre-render all questions upfront. Endless and Speed
        sessions pre-render a fixed batch and refill as the queue shrinks.

        Returns:
            Number of card payloads to keep prepared in memory.
        """

        state = self.state
        if state is None:
            return 0
        if state.mode == Mode.TESTING:
            return max(state.question_limit or 0, 0)
        return 30

    def _prime_pre_rendered_cards(self) -> None:
        """Build the initial pre-rendered card queue before session play starts.

        This method is called during session startup so the first set of
        questions can be shown immediately without per-card preparation delay.
        """

        target = self._target_pre_render_count()
        if target <= 0:
            return
        while len(self._pre_rendered_cards) < target:
            prepared = self._prepare_next_card()
            if prepared is None:
                break
            self._pre_rendered_cards.append(prepared)

    def _maybe_refill_pre_rendered_cards(self) -> None:
        """Top up pre-rendered cards for non-testing modes during a session.

        Endless and Speed sessions can be long-running, so this keeps a small
        queue warm by refilling it when capacity drops.
        """

        state = self.state
        if state is None or state.mode == Mode.TESTING:
            return
        if len(self._pre_rendered_cards) >= 10:
            return
        self._prime_pre_rendered_cards()

    def _prepare_next_card(self) -> Optional[_PreparedCard]:
        """Create one fully prepared card payload from current word inventory.

        Returns:
            A prepared card payload, or ``None`` when no words are available.
        """

        state = self.state
        if state is None or not self.words:
            return None
        direction = self._resolve_direction(state.direction)
        word = select_next_word(self.words, state.difficulty, direction)
        if word is None:
            return None
        choices = self._build_choices(word, direction)
        return _PreparedCard(word=word, direction=direction, choices=choices)

    def _pick_word(self) -> Optional[Word]:
        """Choose the next word to put on the card.

        Uses the word-selection logic in :mod:`core.selectors` (weighted
        random draw based on difficulty) and then immediately builds the
        four answer choices for the chosen word.

        Returns:
            The selected :class:`Word`, or ``None`` if the word list is
            empty or no session is active.
        """

        state = self.state
        if state is None or not self.words:
            return None

        if not self._pre_rendered_cards:
            prepared = self._prepare_next_card()
            if prepared is not None:
                self._pre_rendered_cards.append(prepared)

        if not self._pre_rendered_cards:
            return None

        prepared = self._pre_rendered_cards.popleft()
        state.current_word = prepared.word
        state.current_direction = prepared.direction
        state.current_choices = prepared.choices
        self._maybe_refill_pre_rendered_cards()
        return prepared.word

    @staticmethod
    def _resolve_direction(direction: Direction) -> Direction:
        """Turn a MIXED direction into a concrete ENG_TO_VN or VN_TO_ENG.

        For any non-Mixed direction the input is returned unchanged.
        For Mixed, one of the two concrete directions is selected at random
        (50/50) so each card can go in either direction independently.

        Parameters:
            direction: The session's configured direction (may be MIXED).

        Returns:
            A concrete :class:`Direction` (never MIXED).
        """

        if direction == Direction.MIXED:
            return random.choice([Direction.ENG_TO_VN, Direction.VN_TO_ENG])
        return direction

    @staticmethod
    def _answer_for(word: Word, direction: Direction) -> str:
        """Return the text the user must select to answer correctly.

        For English→Vietnamese the correct answer is the Vietnamese text.
        For Vietnamese→English the correct answer is the English text.

        Parameters:
            word: The vocabulary word being quizzed.
            direction: Which direction this card is going.

        Returns:
            The correct answer string.
        """

        return (
            str(word.vietnamese)
            if direction == Direction.ENG_TO_VN
            else str(word.english)
        )

    def _build_choices(self, word: Word, direction: Direction) -> list[str]:
        """Build the four answer options shown on the current card.

        Always produces exactly:
          1 correct answer (from the card's word in the given direction), plus
          up to 3 wrong distractors (random answers from other words).

        The four options are shuffled before returning so the correct answer
        is not always in the same position.

        Parameters:
            word: The vocabulary word for the current question.
            direction: Which direction this card is going (determines whether
                the correct answer is English or Vietnamese text).

        Returns:
            A shuffled list of strings — the four answer choices.
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
        """Pick the next word and increment the asked counter.

        Checks the question limit before drawing; marks the session finished
        and returns ``None`` if the limit has been reached.

        Returns:
            The newly chosen :class:`Word`, or ``None`` if the session is
            over or no words are available.
        """

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
        """Check the user's answer, update stats, and return the result.

        Steps performed:
          1. Compare the submitted text to the correct answer
             (case-insensitive, stripped of leading/trailing spaces).
          2. Update ``display_count``, ``correct_count``, and ``difficulty``
             in the database for the current word.
          3. Apply the scoring rule (add or deduct points).
          4. Commit the database changes.
          5. Mark the session finished if the question limit is now reached.

        Parameters:
            answer: The text of the option the user selected.

        Returns:
            An :class:`AnswerResult` describing correctness, new score, and
            point delta.  Returns ``None`` if no question is active.
        """

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
        """Handle a "Show Answer" request: apply penalties and report the outcome.

        Checks whether revealing is permitted (feature enabled, uses not
        exhausted).  If allowed, deducts the configured score penalty,
        increments ``show_used``, and calculates any time penalty for Speed
        mode.

        Returns:
            A :class:`ShowAnswerOutcome` with whether the reveal was allowed,
            the score change, remaining uses, and any time penalty.
        """

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
        """Check whether the session has ended.

        A session is considered finished when ``state.finished`` has been
        set to ``True`` (by the question-limit check, a timer expiry, or an
        explicit end triggered by the GUI).

        Returns:
            ``True`` if the session is over, ``False`` if it is still active.
            Also returns ``True`` if no session has been started.
        """

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
        percent = round(s.correct / s.answered * 100,
                        1) if s.answered > 0 else 0.0
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
            direction=s.direction,
            show_score_penalty=s.show_config.score_penalty,
            show_time_penalty=s.show_config.time_penalty,
            wrong_penalty=s.wrong_answer_penalty,
            show_limit_total=show_limit_total,
        )
