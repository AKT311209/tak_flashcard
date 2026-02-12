"""Dictionary controller managing dictionary view."""

from typing import List, Optional
from tak_flashcard.features.dictionary.service import DictionaryService
from tak_flashcard.db.models import Word


class DictionaryController:
    """Controller for dictionary functionality."""

    def __init__(self):
        """Initialize dictionary controller."""
        self.service = DictionaryService()
        self.service.initialize()
        self.current_words = []
        self.current_filter_pos = None
        self.current_sort = 'english'
        self.sort_ascending = True

    def load_all_words(self) -> List[Word]:
        """
        Load all words from dictionary.

        Returns:
            List of all Word objects
        """
        self.current_words = self.service.get_all_words()
        self._apply_sort()
        return self.current_words

    def search(self, query: str) -> List[Word]:
        """
        Search for words matching query.

        Args:
            query: Search query

        Returns:
            List of matching Word objects
        """
        if not query or query.strip() == "":
            return self.load_all_words()

        self.current_words = self.service.search_words(query)
        self._apply_sort()
        return self.current_words

    def filter_by_part_of_speech(self, pos: Optional[str]) -> List[Word]:
        """
        Filter words by part of speech.

        Args:
            pos: Part of speech (None to clear filter)

        Returns:
            List of filtered Word objects
        """
        self.current_filter_pos = pos

        if pos is None or pos == "All":
            self.current_words = self.service.get_all_words()
        else:
            self.current_words = self.service.filter_by_part_of_speech(pos)

        self._apply_sort()
        return self.current_words

    def set_sort(self, sort_by: str, ascending: bool = True):
        """
        Set sort order for displayed words.

        Args:
            sort_by: Field to sort by
            ascending: Sort ascending if True
        """
        self.current_sort = sort_by
        self.sort_ascending = ascending
        self._apply_sort()

    def _apply_sort(self):
        """Apply current sort settings to word list."""
        self.current_words = self.service.sort_words(
            self.current_words,
            self.current_sort,
            self.sort_ascending
        )

    def get_parts_of_speech(self) -> List[str]:
        """
        Get all available parts of speech.

        Returns:
            List of part of speech strings
        """
        return self.service.get_parts_of_speech()

    def cleanup(self):
        """Clean up resources."""
        self.service.cleanup()
