"""Card selection logic."""

from __future__ import annotations

from typing import Sequence

from tak_flashcard.constants import Direction
from tak_flashcard.db.models import Word
from tak_flashcard.db.repo import choose_weighted_word


def select_next_word(words: Sequence[Word], difficulty_level: int, direction: Direction) -> Word | None:
    """Select the next word for a session with weighted difficulty."""

    return choose_weighted_word(words, difficulty_level, direction)
