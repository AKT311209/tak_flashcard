"""Utility script to normalize unicode fields stored in the SQLite database.

Run with:
  PYTHONPATH=src python scripts/normalize_db_unicode.py

This will normalize text fields to NFC in-place for words to fix display issues
caused by decomposed Unicode sequences.
"""
from tak_flashcard.db import get_session, close_session
from tak_flashcard.db.models import Word
import unicodedata


def normalize_word_fields(word: Word) -> bool:
    changed = False
    for field in ('english', 'vietnamese', 'part_of_speech'):
        val = getattr(word, field, None)
        if isinstance(val, str):
            norm = unicodedata.normalize('NFC', val)
            if norm != val:
                setattr(word, field, norm)
                changed = True
    return changed


def main():
    session = get_session()
    try:
        words = session.query(Word).all()
        total = len(words)
        print(f"Normalizing {total} words...")
        updated = 0
        batch = []
        for i, w in enumerate(words, 1):
            if normalize_word_fields(w):
                updated += 1
                batch.append(w)

            # commit in batches
            if i % 200 == 0:
                if batch:
                    session.commit()
                    batch = []

        if batch:
            session.commit()

        print(f"Normalization complete. Updated {updated} / {total} rows.")
    except Exception as e:
        print("Error during normalization:", e)
    finally:
        close_session(session)


if __name__ == '__main__':
    main()
