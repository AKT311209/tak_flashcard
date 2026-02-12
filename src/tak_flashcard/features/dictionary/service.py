"""Dictionary service providing search and filter functionality."""

from typing import List, Optional
from tak_flashcard.db import get_session, close_session, WordRepository
from tak_flashcard.db.models import Word


class DictionaryService:
    """Service for dictionary functionality."""

    def __init__(self):
        """Initialize dictionary service."""
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
        Get all words in the dictionary.

        Returns:
            List of all Word objects
        """
        if not self.repo:
            self.initialize()
        return self.repo.get_all()

    def search_words(self, query: str) -> List[Word]:
        """
        Search for words matching the query.

        Args:
            query: Search query string

        Returns:
            List of matching Word objects
        """
        if not self.repo:
            self.initialize()
        return self.repo.search(query)

    def filter_by_part_of_speech(self, pos: str) -> List[Word]:
        """
        Filter words by part of speech.

        Args:
            pos: Part of speech to filter by

        Returns:
            List of Word objects with matching part of speech
        """
        if not self.repo:
            self.initialize()
        return self.repo.get_by_part_of_speech(pos)

    def filter_by_difficulty(self, min_diff: float, max_diff: float) -> List[Word]:
        """
        Filter words by difficulty range.

        Args:
            min_diff: Minimum difficulty
            max_diff: Maximum difficulty

        Returns:
            List of Word objects within difficulty range
        """
        if not self.repo:
            self.initialize()
        return self.repo.get_by_difficulty_range(min_diff, max_diff)

    def get_parts_of_speech(self) -> List[str]:
        """
        Get all unique parts of speech.

        Returns:
            List of unique part of speech strings
        """
        if not self.repo:
            self.initialize()
        return self.repo.get_unique_parts_of_speech()

    def sort_words(self, words: List[Word], sort_by: str = 'english', ascending: bool = True) -> List[Word]:
        """
        Sort words by specified field.

        Args:
            words: List of words to sort
            sort_by: Field to sort by ('english', 'vietnamese', 'difficulty')
            ascending: Sort in ascending order if True

        Returns:
            Sorted list of Word objects
        """
        reverse = not ascending

        if sort_by == 'english':
            return sorted(words, key=lambda w: w.english.lower(), reverse=reverse)
        elif sort_by == 'vietnamese':
            return sorted(words, key=lambda w: w.vietnamese.lower(), reverse=reverse)
        elif sort_by == 'difficulty':
            return sorted(words, key=lambda w: w.difficulty, reverse=reverse)
        else:
            return words
