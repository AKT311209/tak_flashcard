"""Core session engine for flashcard study sessions."""

import logging
import random
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional

logger = logging.getLogger(__name__)


@dataclass
class Question:
    """Represents a single flashcard question."""

    word_id: int
    prompt: str  # The text shown to the user
    expected_answer: str  # The correct answer
    choices: list[str] = field(default_factory=list)  # For MCQ mode
    revealed: bool = False
    answered: bool = False
    correct: bool = False
    given_answer: Optional[str] = None


@dataclass
class SessionOptions:
    """Configuration options for a study session."""

    mode: str = "Endless"  # Endless, Speed, Testing
    direction: str = "E->V"  # E->V, V->E, Mixed
    difficulty: int = 1  # 1-5 scale
    question_count: int = 10
    time_per_question: int = 30  # seconds
    total_time: int = 300  # seconds (for Speed mode)
    reveal_enabled: bool = True
    reveal_penalty_points: int = 5
    reveal_penalty_time: int = 10  # seconds
    initial_hp: int = 3


class Session:
    """
    In-memory session object managing a flashcard study session.

    This class handles the lifecycle of a study session including:
    - Building the question queue
    - Managing current question state
    - Tracking score and HP
    - Recording results
    """

    def __init__(self, session_id: int, options: SessionOptions):
        """
        Initialize a new session.

        Args:
            session_id: Database session ID
            options: Session configuration options
        """
        self.id = session_id
        self.options = options
        self.queue: list[Question] = []
        self.current_index = 0
        self.score = 0
        self.hp = options.initial_hp
        self.started_at = datetime.now()
        self.ended_at: Optional[datetime] = None
        self.results: list[dict[str, Any]] = []

    def add_question(self, question: Question) -> None:
        """Add a question to the session queue."""
        self.queue.append(question)

    def get_current_question(self) -> Optional[Question]:
        """Get the current question."""
        if self.current_index < len(self.queue):
            return self.queue[self.current_index]
        return None

    def next_question(self) -> Optional[Question]:
        """Move to the next question and return it."""
        self.current_index += 1
        return self.get_current_question()

    def has_more_questions(self) -> bool:
        """Check if there are more questions in the queue."""
        return self.current_index < len(self.queue)

    def submit_answer(self, answer: str) -> bool:
        """
        Submit an answer for the current question.

        Args:
            answer: The user's answer

        Returns:
            True if correct, False otherwise
        """
        question = self.get_current_question()
        if question is None:
            return False

        # Normalize answers for comparison
        normalized_answer = answer.strip().lower()
        normalized_expected = question.expected_answer.strip().lower()

        is_correct = normalized_answer == normalized_expected
        question.answered = True
        question.correct = is_correct
        question.given_answer = answer

        if is_correct:
            self.score += 10  # Base points for correct answer
            if question.revealed:
                self.score -= self.options.reveal_penalty_points
        else:
            self.hp -= 1  # Lose HP for wrong answer

        # Record result
        self._record_result(question)

        return is_correct

    def reveal_answer(self) -> str:
        """
        Reveal the answer for the current question.

        Returns:
            The correct answer
        """
        question = self.get_current_question()
        if question is None:
            return ""

        question.revealed = True
        self.hp -= 1  # Lose HP for revealing
        self.score -= self.options.reveal_penalty_points

        return question.expected_answer

    def _record_result(self, question: Question) -> None:
        """Record a question result."""
        result = {
            "word_id": question.word_id,
            "asked_text": question.prompt,
            "expected_answer": question.expected_answer,
            "given_answer": question.given_answer,
            "correct": 1 if question.correct else 0,
            "revealed": 1 if question.revealed else 0,
            "penalty": self.options.reveal_penalty_points if question.revealed else 0,
        }
        self.results.append(result)

    def end_session(self) -> dict[str, Any]:
        """
        End the session and return summary.

        Returns:
            Session summary dictionary
        """
        self.ended_at = datetime.now()

        summary = {
            "session_id": self.id,
            "mode": self.options.mode,
            "direction": self.options.direction,
            "score": self.score,
            "total_questions": len(self.queue),
            "correct_count": sum(1 for q in self.queue if q.correct),
            "revealed_count": sum(1 for q in self.queue if q.revealed),
            "started_at": self.started_at.isoformat(),
            "ended_at": self.ended_at.isoformat() if self.ended_at else None,
            "results": self.results,
        }

        logger.info(
            f"Session {self.id} ended: {summary['correct_count']}/{summary['total_questions']} correct"
        )

        return summary


def create_session(db_session, options: SessionOptions) -> Session:
    """
    Create a new study session with questions from the database.

    Args:
        db_session: SQLAlchemy database session
        options: Session configuration options

    Returns:
        Initialized Session object
    """
    from tak_flashcard.db.models import Session as DBSession
    from tak_flashcard.db.models import Word

    # Create database session record
    db_session_obj = DBSession(
        mode=options.mode,
        direction=options.direction,
        start_ts=datetime.now().isoformat(),
        score=0,
        total_questions=options.question_count,
    )
    db_session.add(db_session_obj)
    db_session.commit()
    db_session.refresh(db_session_obj)

    # Create in-memory session
    session = Session(session_id=db_session_obj.id, options=options)

    # Build question queue from database
    # Query words based on difficulty
    query = db_session.query(Word).filter(Word.difficulty <= options.difficulty)

    # Limit and randomize
    words = query.limit(options.question_count * 2).all()  # Get extra for randomness
    random.shuffle(words)
    words = words[: options.question_count]

    # Create questions based on direction
    for word in words:
        if options.direction == "E->V":
            prompt = word.word
            answer = word.vietnamese
        elif options.direction == "V->E":
            prompt = word.vietnamese
            answer = word.word
        else:  # Mixed
            if random.choice([True, False]):
                prompt = word.word
                answer = word.vietnamese
            else:
                prompt = word.vietnamese
                answer = word.word

        question = Question(
            word_id=word.id, prompt=prompt, expected_answer=answer, choices=[]
        )
        session.add_question(question)

    logger.info(
        f"Created session {session.id} with {len(session.queue)} questions"
    )

    return session


def save_session_results(db_session, session: Session) -> None:
    """
    Save session results to the database.

    Args:
        db_session: SQLAlchemy database session
        session: The completed Session object
    """
    from tak_flashcard.db.models import Session as DBSession
    from tak_flashcard.db.models import SessionResult

    # Update session record
    db_session_obj = (
        db_session.query(DBSession).filter(DBSession.id == session.id).first()
    )
    if db_session_obj:
        db_session_obj.score = session.score
        db_session_obj.end_ts = (
            session.ended_at.isoformat() if session.ended_at else None
        )

    # Save individual results
    for result in session.results:
        result_obj = SessionResult(
            session_id=session.id,
            word_id=result["word_id"],
            asked_text=result["asked_text"],
            expected_answer=result["expected_answer"],
            given_answer=result["given_answer"],
            correct=result["correct"],
            revealed=result["revealed"],
            penalty=result["penalty"],
        )
        db_session.add(result_obj)

    db_session.commit()
    logger.info(f"Saved results for session {session.id}")
