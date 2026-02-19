"""CSV importer for vocabulary."""

from __future__ import annotations

import csv
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from sqlalchemy.orm import Session

from tak_flashcard.config import DATA_DIR
from tak_flashcard.db.repo import bulk_insert_words, clear_all_words, upsert_words_append


VOCAB_BACKUP_DIR = DATA_DIR / "vocab"


@dataclass
class ImportResult:
    """Result of a user-initiated CSV import operation.

    Attributes:
        added: Number of new words inserted into the database.
        removed: Number of words deleted (only non-zero for Replace mode).
        updated: Number of duplicate words overwritten (Append mode only).
        skipped: Number of duplicate words left unchanged (Append mode only).
        backup_path: Path to the timestamped backup CSV that was written.
        errors: Validation error messages; non-empty means import was aborted.
    """

    added: int
    removed: int
    updated: int
    skipped: int
    backup_path: Path | None
    errors: list[str]


def read_csv_headers(path: Path) -> list[str]:
    """Read and return the header row from a CSV file.

    The first row of the file is treated as the header. Returns an empty list
    if the file cannot be opened or contains no header row.

    Parameters:
        path: Path to the CSV file.

    Returns:
        A list of column header strings in their original order.
    """

    try:
        with path.open("r", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            return list(reader.fieldnames or [])
    except Exception:
        return []


def _parse_csv_rows(
    path: Path,
    column_map: dict[str, str],
) -> list[dict[str, object]]:
    """Parse vocabulary rows from a CSV file using a caller-supplied column mapping.

    Rows where either the English or Vietnamese value is blank are silently
    skipped.

    Parameters:
        path: Path to the CSV file.
        column_map: Mapping from logical field names (``english``,
            ``vietnamese``, ``part_of_speech``) to the actual column header
            names present in the CSV. ``part_of_speech`` is optional and may
            be omitted or set to an empty string.

    Returns:
        A list of word dicts ready for bulk insertion.
    """

    english_col = column_map.get("english", "")
    vietnamese_col = column_map.get("vietnamese", "")
    pos_col = column_map.get("part_of_speech", "")

    rows: list[dict[str, object]] = []
    with path.open("r", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            english = row.get(english_col, "").strip() if english_col else ""
            vietnamese = row.get(
                vietnamese_col, "").strip() if vietnamese_col else ""
            if not english or not vietnamese:
                continue
            rows.append(
                {
                    "english": english,
                    "vietnamese": vietnamese,
                    "part_of_speech": (row.get(pos_col, "").strip() or None)
                    if pos_col
                    else None,
                    "display_count": 0,
                    "correct_count": 0,
                    "difficulty": 0.5,
                }
            )
    return rows


def _backup_vocab(source: Path) -> Path:
    """Copy source CSV to a timestamped backup file in the vocab directory.

    Parameters:
        source: Path to the CSV file being imported.

    Returns:
        The path of the created backup file.
    """

    VOCAB_BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dest = VOCAB_BACKUP_DIR / f"vocab_source_{timestamp}.csv"
    shutil.copy2(source, dest)
    return dest


def import_vocab_file(
    db: Session,
    source: Path,
    column_map: dict[str, str],
    replace: bool = False,
    overwrite_duplicates: bool = False,
    reset_difficulty: bool = False,
) -> ImportResult:
    """Import vocabulary words from a CSV file into the database.

    Uses the caller-supplied ``column_map`` to locate the English, Vietnamese,
    and optional Part-of-Speech columns inside the file. A timestamped backup
    of the source file is written to ``data/vocab/`` before any database
    changes are made.

    Parameters:
        db: Active SQLAlchemy session.
        source: Path to the CSV file selected by the user.
        column_map: Mapping from logical field names (``english``,
            ``vietnamese``, ``part_of_speech``) to actual CSV column headers.
            ``english`` and ``vietnamese`` are required; ``part_of_speech`` is
            optional.
        replace: When ``True`` all existing words are deleted before inserting
                 the new ones (Replace mode). When ``False`` new words are
                 appended to the existing data (Append mode).
        overwrite_duplicates: Append mode only. When ``True``, existing words
            that match an imported English word are updated with the new
            translation and part-of-speech. When ``False`` they are skipped.
        reset_difficulty: Append mode only. When ``True`` (and
            ``overwrite_duplicates`` is also ``True``), the difficulty,
            display count, and correct count are reset to defaults for any
            overwritten word.

    Returns:
        An :class:`ImportResult` with counts and backup location, or a
        non-empty ``errors`` list when the import was aborted.
    """

    if not source.exists():
        return ImportResult(
            added=0, removed=0, updated=0, skipped=0, backup_path=None,
            errors=[f"File not found: {source}"],
        )

    if not column_map.get("english") or not column_map.get("vietnamese"):
        return ImportResult(
            added=0, removed=0, updated=0, skipped=0, backup_path=None,
            errors=[
                "Both the English and Vietnamese columns must be mapped before importing."],
        )

    backup_path = _backup_vocab(source)
    rows = _parse_csv_rows(source, column_map)

    if not rows:
        return ImportResult(
            added=0, removed=0, updated=0, skipped=0, backup_path=backup_path,
            errors=[
                "No valid rows were found in the CSV file after applying the column mapping."],
        )

    removed = 0
    updated = 0
    skipped = 0

    if replace:
        removed = clear_all_words(db)
        bulk_insert_words(db, rows)
        added = len(rows)
    else:
        added, updated, skipped = upsert_words_append(
            db, rows, overwrite_duplicates, reset_difficulty
        )

    db.commit()

    return ImportResult(
        added=added,
        removed=removed,
        updated=updated,
        skipped=skipped,
        backup_path=backup_path,
        errors=[],
    )
