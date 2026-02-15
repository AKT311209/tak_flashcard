"""Repository layer for database operations."""

from __future__ import annotations

import random
from collections.abc import Iterable
from typing import Sequence

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from tak_flashcard.constants import Direction, DIFFICULTY_LEVELS
from tak_flashcard.db.models import Word


def get_word_count(db: Session) -> int:
    """Return the total count of words in the database."""

    return db.scalar(select(func.count()).select_from(Word)) or 0


def bulk_insert_words(db: Session, words: Iterable[dict[str, object]]) -> None:
    """Insert multiple words into the database."""

    db.bulk_insert_mappings(Word, list(words))


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
    word.difficulty = calculate_difficulty(
        word.display_count, word.correct_count)
    db.add(word)


def calculate_difficulty(display_count: int, correct_count: int) -> float:
    """Compute difficulty score based on counts."""

    epsilon = 1e-6
    return 1.0 - (correct_count / (display_count + epsilon))


def choose_weighted_word(words: Sequence[Word], difficulty_level: int, direction: Direction) -> Word | None:
    """Select a word weighted by difficulty preference and direction."""

    if not words:
        return None

    clamped = max(min(difficulty_level, max(DIFFICULTY_LEVELS)),
                  min(DIFFICULTY_LEVELS))
    weights: list[float] = []
    for word in words:
        base = word.difficulty or 0.5
        if clamped <= 2:
            weight = 1.0 - base
        elif clamped == 3:
            weight = 1.0
        elif clamped == 4:
            weight = 0.5 + base
        else:
            weight = 1.0 + base
        weights.append(max(weight, 0.01))

    chosen = random.choices(words, weights=weights, k=1)[0]
    return chosen
