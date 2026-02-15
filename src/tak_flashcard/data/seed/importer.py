"""CSV importer and bootstrap seeding for vocabulary."""

from __future__ import annotations

import csv
import random
from pathlib import Path
from typing import Iterable, Sequence

from sqlalchemy.orm import Session

from tak_flashcard.config import MIN_WORDS_REQUIRED, VOCAB_PATH
from tak_flashcard.db.repo import bulk_insert_words, get_word_count

PARTS = ["noun", "verb", "adjective", "adverb", "phrase"]


def generate_placeholder_words(count: int = MIN_WORDS_REQUIRED) -> list[dict[str, object]]:
    """Generate placeholder vocabulary entries to satisfy minimum requirements."""

    words: list[dict[str, object]] = []
    for idx in range(count):
        base = f"word_{idx + 1}"
        words.append(
            {
                "english": base,
                "vietnamese": f"nghia_{idx + 1}",
                "part_of_speech": random.choice(PARTS),
                "display_count": 0,
                "correct_count": 0,
                "difficulty": 0.5,
            }
        )
    return words


def read_vocab_file(path: Path = VOCAB_PATH) -> Sequence[dict[str, object]]:
    """Read vocabulary rows from CSV if present; otherwise generate placeholder data."""

    if not path.exists():
        return generate_placeholder_words()
    with path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        rows: list[dict[str, object]] = []
        for row in reader:
            english = row.get("english", "").strip()
            vietnamese = row.get("vietnamese", "").strip()
            part_of_speech = row.get("part_of_speech", "").strip() or None
            if not english or not vietnamese:
                continue
            rows.append(
                {
                    "english": english,
                    "vietnamese": vietnamese,
                    "part_of_speech": part_of_speech,
                    "display_count": 0,
                    "correct_count": 0,
                    "difficulty": 0.5,
                }
            )
        if len(rows) < MIN_WORDS_REQUIRED:
            rows.extend(generate_placeholder_words(
                MIN_WORDS_REQUIRED - len(rows)))
        return rows


def ensure_seed_data(db: Session) -> None:
    """Ensure the database contains at least the minimum number of words."""

    current = get_word_count(db)
    if current >= MIN_WORDS_REQUIRED:
        return
    rows = read_vocab_file()
    bulk_insert_words(db, rows)
    db.commit()
