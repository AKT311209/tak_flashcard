"""Flashcard state management."""

from enum import Enum


class FlashcardState(Enum):
    """States in the flashcard workflow."""
    QUESTION = "question"
    ANSWER = "answer"
    RESULT = "result"
    COMPLETED = "completed"
