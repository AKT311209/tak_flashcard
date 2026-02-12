"""Flashcard service providing business logic."""

from typing import List, Optional
from tak_flashcard.db import get_session, close_session, WordRepository
from tak_flashcard.db.models import Word
from tak_flashcard.constants import Direction


class FlashcardService:
    """Service for flashcard business logic."""

    def __init__(self):
        """Initialize flashcard service."""
        self.session = None
        self.repo = None

    def initialize(self):
        """Initialize database session and repository."""
        self.session = get_session()
        self.repo = WordRepository(self.session)

    def cleanup(self):
        """Clean up database session."""
        if self.session:
            close_session(self.session)
            self.session = None
            self.repo = None

    def get_all_words(self) -> List[Word]:
        """
        Get all words from database.

        Returns:
            List of all Word objects
        """
        if not self.repo:
            self.initialize()
        return self.repo.get_all()

    def validate_answer(self, user_answer: str, correct_answer: str) -> bool:
        """
        Validate user's answer against correct answer.

        Args:
            user_answer: User's input
            correct_answer: Correct answer

        Returns:
            True if correct, False otherwise
        """
        user_clean = user_answer.strip().lower()
        correct_clean = correct_answer.strip().lower()
        return user_clean == correct_clean

    def update_word_stats(self, word: Word, is_correct: bool):
        """
        Update word statistics after answering.

        Args:
            word: Word object to update
            is_correct: Whether answer was correct
        """
        if not self.repo:
            self.initialize()
        self.repo.update_stats(word, is_correct)

    def get_question_and_answer(self, word: Word, direction: Direction) -> tuple[str, str]:
        """
        Get question and answer text based on direction.

        Args:
            word: Word object
            direction: Translation direction

        Returns:
            Tuple of (question, answer)
        """
        if direction == Direction.ENG_TO_VN:
            return word.english, word.vietnamese
        else:
            return word.vietnamese, word.english
