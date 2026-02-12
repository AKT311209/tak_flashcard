"""Question selection logic based on difficulty and direction."""

import random
from typing import List, Optional
from tak_flashcard.db.models import Word
from tak_flashcard.constants import Direction
from tak_flashcard.core.difficulty import calculate_selection_weight


class CardSelector:
    """Selects flashcards based on difficulty setting and direction."""

    def __init__(self, words: List[Word], difficulty_setting: int):
        """
        Initialize card selector.

        Args:
            words: List of available words
            difficulty_setting: User's difficulty setting (1-5)
        """
        self.words = words
        self.difficulty_setting = difficulty_setting
        self.recent_words = []
        self.max_recent = min(10, len(words) // 10)

    def select_card(self, direction: Direction) -> Optional[tuple[Word, Direction]]:
        """
        Select a card based on difficulty and direction settings.

        Args:
            direction: Translation direction setting

        Returns:
            Tuple of (word, actual_direction) or None if no words available
        """
        if not self.words:
            return None

        available_words = [w for w in self.words if w not in self.recent_words]
        if not available_words:
            available_words = self.words
            self.recent_words.clear()

        weights = [
            calculate_selection_weight(
                word.difficulty, self.difficulty_setting)
            for word in available_words
        ]

        selected_word = random.choices(
            available_words, weights=weights, k=1)[0]

        self.recent_words.append(selected_word)
        if len(self.recent_words) > self.max_recent:
            self.recent_words.pop(0)

        actual_direction = self._determine_direction(direction)

        return selected_word, actual_direction

    def _determine_direction(self, direction: Direction) -> Direction:
        """
        Determine actual direction for the question.

        Args:
            direction: Direction setting

        Returns:
            Actual direction to use (ENG_TO_VN or VN_TO_ENG)
        """
        if direction == Direction.MIXED:
            return random.choice([Direction.ENG_TO_VN, Direction.VN_TO_ENG])
        return direction

    def select_multiple(self, count: int, direction: Direction) -> List[tuple[Word, Direction]]:
        """
        Select multiple cards for testing mode.

        Args:
            count: Number of cards to select
            direction: Translation direction setting

        Returns:
            List of (word, actual_direction) tuples
        """
        selected = []
        for _ in range(min(count, len(self.words))):
            card = self.select_card(direction)
            if card:
                selected.append(card)
        return selected
