"""Repository layer for database operations.

This module is the ONLY place in the codebase that reads from or writes to
the database.  Every function here takes an active SQLAlchemy session (``db``)
as its first argument and performs exactly one logical database task.

No business logic lives here — just raw queries and writes.

Calling order (typical):
  db/session.py creates the session
      → gui/app.py holds it open for the lifetime of the app
          → features/ and gui/ call these functions via services/controllers
"""

from __future__ import annotations

from collections.abc import Iterable

from sqlalchemy import func, insert, select
from sqlalchemy.orm import Session

from tak_flashcard.core.difficulty import difficulty_score
from tak_flashcard.db.models import Word


def get_word_count(db: Session) -> int:
    """Count how many vocabulary words are currently in the database.

    Used at startup to decide whether to show the Import screen first.

    Parameters:
        db: The open database connection.

    Returns:
        Total number of words stored (0 if the table is empty).
    """

    return db.scalar(select(func.count()).select_from(Word)) or 0


def bulk_insert_words(db: Session, words: Iterable[dict[str, object]]) -> None:
    """Write a large batch of new words to the database in one go.

    More efficient than inserting words one at a time; used during CSV import.

    Parameters:
        db: The open database connection.
        words: Each item is a dict with keys ``english``, ``vietnamese``, and
               optionally ``part_of_speech``.
    """

    db.execute(insert(Word), list(words))


def find_word_by_english(db: Session, english: str) -> Word | None:
    """Look up a word by its English text (case-insensitive).

    Used during import to check whether a word already exists before
    deciding to insert or update it.

    Parameters:
        db: The open database connection.
        english: The English word to search for (e.g. ``"apple"``).

    Returns:
        The matching :class:`Word` record, or ``None`` if not found.
    """

    return db.scalars(
        select(Word).where(func.lower(Word.english) == english.lower())
    ).first()


def upsert_words_append(
    db: Session,
    rows: list[dict[str, object]],
    overwrite_duplicates: bool,
    reset_difficulty: bool,
) -> tuple[int, int, int]:
    """Add new words while leaving existing ones alone (Append import mode).

    Goes through each row from the CSV one by one:
    - If the English word is not yet in the database → insert it as new.
    - If it already exists and ``overwrite_duplicates`` is True → update
      its Vietnamese translation and part of speech.
    - If it already exists and ``overwrite_duplicates`` is False → skip it.

    Parameters:
        db: The open database connection.
        rows: Parsed CSV rows, each a dict with ``english``, ``vietnamese``,
              and optionally ``part_of_speech``.
        overwrite_duplicates: Whether to update existing words with new data
            from the CSV.
        reset_difficulty: When ``True`` (and ``overwrite_duplicates`` is also
            ``True``), wipe the word's progress stats back to zero.

    Returns:
        A three-item tuple: ``(added, updated, skipped)`` — how many words
        fell into each category.
    """

    added = updated = skipped = 0
    to_insert: list[dict[str, object]] = []

    for row in rows:
        english = str(row.get("english", ""))
        existing = find_word_by_english(db, english)

        if existing is None:
            to_insert.append(row)
            added += 1
        elif overwrite_duplicates:
            existing.vietnamese = str(row.get("vietnamese", ""))
            existing.part_of_speech = row.get(
                "part_of_speech")  # type: ignore[assignment]
            if reset_difficulty:
                existing.difficulty = 0.5
                existing.display_count = 0
                existing.correct_count = 0
            db.add(existing)
            updated += 1
        else:
            skipped += 1

    if to_insert:
        db.execute(insert(Word), to_insert)

    return added, updated, skipped


def clear_all_words(db: Session) -> int:
    """Delete every word from the database (Replace import mode).

    Called before a fresh import when the user chooses "Replace" mode,
    which wipes the existing vocabulary and replaces it entirely.

    Parameters:
        db: The open database connection.

    Returns:
        The number of words that were deleted.
    """

    count = get_word_count(db)
    db.query(Word).delete()
    return count


def list_words(db: Session) -> list[Word]:
    """Fetch every word from the database, sorted A→Z by English text.

    Used by the Dictionary view to show the full vocabulary list and by
    the flashcard service to load all words into memory at session start.

    Parameters:
        db: The open database connection.

    Returns:
        All :class:`Word` records, ordered alphabetically by English word.
    """

    return list(db.scalars(select(Word).order_by(Word.english)).all())


def search_words(db: Session, query: str) -> list[Word]:
    """Find words whose English or Vietnamese text contains the search query.

    Called by the Dictionary view's search bar.  Matching is
    case-insensitive and uses a "contains" check (not exact match).

    Parameters:
        db: The open database connection.
        query: Text typed by the user in the search bar.

    Returns:
        All matching :class:`Word` records, sorted A→Z by English text.
    """

    pattern = f"%{query.lower()}%"
    stmt = select(Word).where(
        func.lower(Word.english).like(pattern) | func.lower(
            Word.vietnamese).like(pattern)
    ).order_by(Word.english)
    return list(db.scalars(stmt).all())


def filter_by_part_of_speech(db: Session, part: str) -> list[Word]:
    """Fetch only words that match a specific part of speech.

    Parameters:
        db: The open database connection.
        part: The part of speech to filter by (e.g. ``"noun"``, ``"verb"``).
              Matching is case-insensitive.

    Returns:
        Matching :class:`Word` records, sorted A→Z by English text.
    """

    stmt = select(Word).where(func.lower(Word.part_of_speech)
                              == part.lower()).order_by(Word.english)
    return list(db.scalars(stmt).all())


def update_word_stats(db: Session, word_id: int, is_correct: bool) -> None:
    """Record the result of one answer attempt and refresh the word's difficulty.

    Called after every answer submitted during a flashcard session.
    Increments the word's display count each time, and its correct count
    only when the user answered correctly.  Then recalculates difficulty
    so future word selection reflects the latest performance.

    Parameters:
        db: The open database connection.
        word_id: The database ID of the word that was just answered.
        is_correct: ``True`` if the user chose the right answer.
    """

    word = db.get(Word, word_id)
    if word is None:
        return
    word.display_count += 1
    if is_correct:
        word.correct_count += 1
    word.difficulty = difficulty_score(
        word.display_count, word.correct_count)
    db.add(word)


