"""Repository layer for database operations."""

from __future__ import annotations

import random
import math
from collections.abc import Iterable
from typing import Sequence, cast

from sqlalchemy import func, insert, select
from sqlalchemy.orm import Session

from tak_flashcard.config import Direction, DIFFICULTY_LEVELS
from tak_flashcard.core.difficulty import difficulty_score
from tak_flashcard.db.models import Word


def get_word_count(db: Session) -> int:
    """Return the total count of words in the database."""

    return db.scalar(select(func.count()).select_from(Word)) or 0


def bulk_insert_words(db: Session, words: Iterable[dict[str, object]]) -> None:
    """Insert multiple words into the database."""

    db.execute(insert(Word), list(words))


def clear_all_words(db: Session) -> int:
    """Delete every word from the database and return the count removed.

    Parameters:
        db: Active SQLAlchemy session.

    Returns:
        The number of rows that were deleted.
    """

    count = get_word_count(db)
    db.query(Word).delete()
    return count


def list_words(db: Session) -> list[Word]:
    """Return all words ordered by English word."""

    return list(db.scalars(select(Word).order_by(Word.english)).all())


def search_words(db: Session, query: str) -> list[Word]:
    """Search words by English or Vietnamese fields."""

    pattern = f"%{query.lower()}%"
    stmt = select(Word).where(
        func.lower(Word.english).like(pattern) | func.lower(
            Word.vietnamese).like(pattern)
    ).order_by(Word.english)
    return list(db.scalars(stmt).all())


def filter_by_part_of_speech(db: Session, part: str) -> list[Word]:
    """Filter words by part of speech."""

    stmt = select(Word).where(func.lower(Word.part_of_speech)
                              == part.lower()).order_by(Word.english)
    return list(db.scalars(stmt).all())


def update_word_stats(db: Session, word_id: int, is_correct: bool) -> None:
    """Update display and correct counts, and recalculate difficulty for a word."""

    word = db.get(Word, word_id)
    if word is None:
        return
    word.display_count += 1
    if is_correct:
        word.correct_count += 1
    word.difficulty = difficulty_score(
        word.display_count, word.correct_count)
    db.add(word)


def choose_weighted_word(words: Sequence[Word], difficulty_level: int, _direction: Direction) -> Word | None:
    """Select a word weighted by difficulty preference and direction."""

    if not words:
        return None

    clamped = _clamp_difficulty(difficulty_level)
    weights: list[float] = []
    for word in words:
        base_value = cast(float | None, word.difficulty)
        base = base_value if base_value is not None else 0.5
        weight = _calculate_difficulty_weight(clamped, base)
        weights.append(max(weight, 0.01))

    chosen = random.choices(words, weights=weights, k=1)[0]
    return chosen


def _clamp_difficulty(level: int) -> int:
    """Clamp user-selected difficulty to valid configured bounds."""

    min_level = min(DIFFICULTY_LEVELS)
    max_level = max(DIFFICULTY_LEVELS)
    return max(min(level, max_level), min_level)


def _calculate_difficulty_weight(level: int, base: float) -> float:
    """Return the selection weight for a word given the difficulty level.

    Uses an exponential multiplier so that each successive level increases
    the hard-to-easy probability ratio rather than simply shifting all weights
    up by a constant.

    Level 1 (easiest): strongly favours low-difficulty words via 1/e^(2*base).
    Level 2 (easy):    gently favours low-difficulty words via 1/e^(base).
    Level 3 (neutral): flat weight; all words equally likely.
    Level 4 (hard):    gently favours high-difficulty words via e^base.
    Level 5 (hardest): strongly favours high-difficulty words via e^(2*base).
    """

    if level == 1:
        return math.exp(-2.0 * base)
    if level == 2:
        return math.exp(-base)
    if level == 3:
        return 1.0
    if level == 4:
        return math.exp(base)
    return math.exp(2.0 * base)
