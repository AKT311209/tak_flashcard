"""Flashcard controller managing flashcard sessions."""

from typing import Optional, Dict, Any
from datetime import datetime
from tak_flashcard.constants import FlashcardMode, Direction, PenaltyType
from tak_flashcard.core import CardSelector, ScoreManager, Timer
from tak_flashcard.features.flashcard.service import FlashcardService
from tak_flashcard.features.flashcard.states import FlashcardState
from tak_flashcard.db import get_session, close_session, SessionRepository
from tak_flashcard.db.models import Word


class FlashcardController:
    """Controller for flashcard sessions."""

    def __init__(
        self,
        mode: FlashcardMode,
        direction: Direction,
        difficulty: int,
        question_count: Optional[int] = None,
        time_limit: Optional[int] = None,
        enable_show_answer: bool = True,
        penalty_type: PenaltyType = PenaltyType.SCORE
    ):
        """
        Initialize flashcard controller.

        Args:
            mode: Flashcard mode
            direction: Translation direction
            difficulty: Difficulty level (1-5)
            question_count: Number of questions for Testing mode
            time_limit: Time limit in seconds for Speed mode
            enable_show_answer: Whether Show Answer is enabled
            penalty_type: Penalty type for Show Answer
        """
        self.mode = mode
        self.direction = direction
        self.difficulty = difficulty
        self.question_count = question_count
        self.time_limit = time_limit
        self.enable_show_answer = enable_show_answer
        self.penalty_type = penalty_type

        self.service = FlashcardService()
        self.service.initialize()

        words = self.service.get_all_words()
        self.selector = CardSelector(words, difficulty)
        self.score_manager = ScoreManager(penalty_type)
        self.timer = Timer(time_limit) if time_limit else None

        self.state = FlashcardState.QUESTION
        self.current_word = None
        self.current_direction = None
        self.current_question = None
        self.current_answer = None
        self.questions_answered = 0
        self.session_start_time = datetime.utcnow()
        self.session_id = None
        self.answer_shown = False

    def start_session(self):
        """Start the flashcard session."""
        if self.timer:
            self.timer.start()

        session_data = {
            'mode': self.mode.value,
            'direction': self.direction.value,
            'difficulty_setting': self.difficulty,
            'question_count': self.question_count,
            'time_limit': self.time_limit,
            'start_time': self.session_start_time
        }

        db_session = get_session()
        session_repo = SessionRepository(db_session)
        session_obj = session_repo.create(session_data)
        self.session_id = session_obj.id
        close_session(db_session)

        self.next_question()

    def next_question(self):
        """Load the next question."""
        if self.is_session_complete():
            self.state = FlashcardState.COMPLETED
            return

        card_data = self.selector.select_card(self.direction)
        if not card_data:
            self.state = FlashcardState.COMPLETED
            return

        self.current_word, self.current_direction = card_data
        self.current_question, self.current_answer = self.service.get_question_and_answer(
            self.current_word, self.current_direction
        )
        self.state = FlashcardState.QUESTION
        self.answer_shown = False

    def submit_answer(self, user_answer: str) -> Dict[str, Any]:
        """
        Submit and validate an answer.

        Args:
            user_answer: User's answer text

        Returns:
            Dictionary with result information
        """
        is_correct = self.service.validate_answer(
            user_answer, self.current_answer)

        response_time = 0
        if self.timer and self.timer.is_running:
            response_time = self.time_limit - self.timer.get_remaining()

        if is_correct:
            points = self.score_manager.answer_correct(response_time)
        else:
            points = self.score_manager.answer_incorrect()

        self.service.update_word_stats(self.current_word, is_correct)
        self.questions_answered += 1
        self.state = FlashcardState.RESULT

        return {
            'is_correct': is_correct,
            'correct_answer': self.current_answer,
            'points': points,
            'word': self.current_word,
            'statistics': self.score_manager.get_statistics()
        }

    def show_answer(self) -> Optional[Dict[str, Any]]:
        """
        Show the answer (applies penalty).

        Returns:
            Dictionary with answer and penalty details, or None if not allowed
        """
        if not self.enable_show_answer or not self.score_manager.can_use_show_answer():
            return None

        penalty_result = self.score_manager.apply_show_answer_penalty()

        if self.timer and self.penalty_type == PenaltyType.TIME:
            self.timer.subtract_time(penalty_result['time_penalty'])

        self.answer_shown = True

        return {
            'answer': self.current_answer,
            'penalty': penalty_result,
            'statistics': self.score_manager.get_statistics()
        }

    def is_session_complete(self) -> bool:
        """
        Check if the session is complete.

        Returns:
            True if session should end
        """
        if self.mode == FlashcardMode.TESTING:
            return self.questions_answered >= self.question_count

        if self.mode == FlashcardMode.SPEED:
            return self.timer and self.timer.is_expired()

        return False

    def end_session(self) -> Dict[str, Any]:
        """
        End the session and save results.

        Returns:
            Dictionary with final statistics
        """
        if self.timer:
            self.timer.stop()

        stats = self.score_manager.get_statistics()

        if self.session_id:
            db_session = get_session()
            session_repo = SessionRepository(db_session)
            session_obj = db_session.query(
                "Session").filter_by(id=self.session_id).first()

            if session_obj:
                session_repo.update(session_obj, {
                    'end_time': datetime.utcnow(),
                    'score': stats['score'],
                    'correct_count': stats['correct'],
                    'total_count': stats['total']
                })

            close_session(db_session)

        self.service.cleanup()
        self.state = FlashcardState.COMPLETED

        return stats

    def get_current_state(self) -> Dict[str, Any]:
        """
        Get current session state.

        Returns:
            Dictionary with current state information
        """
        state_info = {
            'state': self.state,
            'mode': self.mode,
            'direction': self.current_direction,
            'question': self.current_question,
            'questions_answered': self.questions_answered,
            'statistics': self.score_manager.get_statistics(),
            'can_show_answer': self.enable_show_answer and self.score_manager.can_use_show_answer(),
            'answer_shown': self.answer_shown
        }

        if self.mode == FlashcardMode.TESTING and self.question_count:
            state_info['question_progress'] = f"{self.questions_answered}/{self.question_count}"

        if self.timer:
            state_info['time_remaining'] = self.timer.get_remaining()

        if self.current_word:
            state_info['word_info'] = {
                'pronunciation': self.current_word.pronunciation,
                'part_of_speech': self.current_word.part_of_speech
            }

        return state_info
