"""Repository layer for database queries."""

from typing import List, Optional
from sqlalchemy import func
from sqlalchemy.orm import Session
from tak_flashcard.db.models import Word, Session as SessionModel
from tak_flashcard.constants import EPSILON


class WordRepository:
    """Repository for Word model operations."""

    def __init__(self, session: Session):
        """
        Initialize repository with database session.

        Args:
            session: SQLAlchemy session
        """
        self.session = session

    def get_all(self) -> List[Word]:
        """
        Get all words from database.

        Returns:
            List of all Word objects
        """
        return self.session.query(Word).all()

    def get_by_id(self, word_id: int) -> Optional[Word]:
        """
        Get a word by ID.

        Args:
            word_id: Word ID

        Returns:
            Word object or None if not found
        """
        return self.session.query(Word).filter(Word.id == word_id).first()

    def get_by_difficulty_range(self, min_diff: float, max_diff: float) -> List[Word]:
        """
        Get words within a difficulty range.

        Args:
            min_diff: Minimum difficulty
            max_diff: Maximum difficulty

        Returns:
            List of Word objects
        """
        return self.session.query(Word).filter(
            Word.difficulty >= min_diff,
            Word.difficulty <= max_diff
        ).all()

    def get_by_part_of_speech(self, pos: str) -> List[Word]:
        """
        Get words by part of speech.

        Args:
            pos: Part of speech

        Returns:
            List of Word objects
        """
        return self.session.query(Word).filter(
            Word.part_of_speech == pos
        ).all()

    def search(self, query: str) -> List[Word]:
        """
        Search words by English or Vietnamese text.

        Args:
            query: Search query

        Returns:
            List of matching Word objects
        """
        search_pattern = f"%{query}%"
        return self.session.query(Word).filter(
            (Word.english.ilike(search_pattern)) |
            (Word.vietnamese.ilike(search_pattern))
        ).all()

    def update_stats(self, word: Word, is_correct: bool):
        """
        Update word statistics after an answer.

        Args:
            word: Word object to update
            is_correct: Whether the answer was correct
        """
        word.display_count += 1
        if is_correct:
            word.correct_count += 1

        word.difficulty = 1 - (word.correct_count /
                               (word.display_count + EPSILON))

        self.session.commit()

    def count(self) -> int:
        """
        Count total number of words in database.

        Returns:
            Total word count
        """
        return self.session.query(func.count(Word.id)).scalar()

    def bulk_insert(self, words: List[dict]):
        """
        Bulk insert words into database.

        Args:
            words: List of word dictionaries
        """
        word_objects = [Word(**word_data) for word_data in words]
        self.session.bulk_save_objects(word_objects)
        self.session.commit()

    def get_unique_parts_of_speech(self) -> List[str]:
        """
        Get all unique parts of speech in the database.

        Returns:
            List of unique part of speech strings
        """
        results = self.session.query(Word.part_of_speech).distinct().all()
        return [result[0] for result in results]


class SessionRepository:
    """Repository for Session model operations."""

    def __init__(self, session: Session):
        """
        Initialize repository with database session.

        Args:
            session: SQLAlchemy session
        """
        self.session = session

    def create(self, session_data: dict) -> SessionModel:
        """
        Create a new session record.

        Args:
            session_data: Dictionary with session data

        Returns:
            Created Session object
        """
        session_obj = SessionModel(**session_data)
        self.session.add(session_obj)
        self.session.commit()
        return session_obj

    def update(self, session_obj: SessionModel, update_data: dict):
        """
        Update an existing session record.

        Args:
            session_obj: Session object to update
            update_data: Dictionary with fields to update
        """
        for key, value in update_data.items():
            setattr(session_obj, key, value)
        self.session.commit()

    def get_recent_sessions(self, limit: int = 10) -> List[SessionModel]:
        """
        Get recent session records.

        Args:
            limit: Maximum number of sessions to return

        Returns:
            List of recent Session objects
        """
        return self.session.query(SessionModel).order_by(
            SessionModel.start_time.desc()
        ).limit(limit).all()
