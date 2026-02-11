"""CSV/XLSX importer for vocabulary words."""

import csv
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


def import_csv(
    file_path: str, db_session, batch_size: int = 500
) -> dict[str, int]:
    """
    Import vocabulary words from CSV or XLSX file.

    Expected columns (case-insensitive):
    - word (required): English word
    - meaning_vn (required): Vietnamese meaning
    - pos (optional): Part of speech
    - pronunciation (optional): Pronunciation guide
    - meaning_en (optional): English meaning/definition
    - example_en (optional): English example sentence
    - example_vn (optional): Vietnamese example sentence
    - audio_url (optional): URL to audio file
    - image_url (optional): URL to image file
    - difficulty (optional): Difficulty level (1-5)
    - tags (optional): Comma-separated tags
    - frequency_rank (optional): Frequency rank

    Args:
        file_path: Path to CSV or XLSX file
        db_session: SQLAlchemy database session
        batch_size: Number of rows to process in each batch

    Returns:
        Dictionary with counts: {added, skipped, errors}
    """
    from tak_flashcard.db.models import Word

    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    stats = {"added": 0, "skipped": 0, "errors": 0}

    try:
        # Try pandas first for better handling
        try:
            import pandas as pd

            if path.suffix.lower() in [".xlsx", ".xls"]:
                df = pd.read_excel(file_path)
            else:
                df = pd.read_csv(file_path)

            # Normalize column names to lowercase
            df.columns = df.columns.str.lower().str.strip()

            # Check required columns
            if "word" not in df.columns or "meaning_vn" not in df.columns:
                raise ValueError("Required columns 'word' and 'meaning_vn' not found")

            # Drop empty rows and duplicates
            df = df.dropna(subset=["word", "meaning_vn"])
            df = df.drop_duplicates(subset=["word"], keep="first")

            # Process in batches
            batch = []
            for _, row in df.iterrows():
                try:
                    # Check if word already exists
                    word_text = str(row["word"]).strip()
                    existing = (
                        db_session.query(Word)
                        .filter(Word.word == word_text)
                        .first()
                    )

                    if existing:
                        stats["skipped"] += 1
                        continue

                    # Create new word
                    word = Word(
                        word=word_text,
                        meaning_vn=str(row["meaning_vn"]).strip(),
                        pos=str(row.get("pos", "")).strip() or None,
                        pronunciation=str(row.get("pronunciation", "")).strip()
                        or None,
                        meaning_en=str(row.get("meaning_en", "")).strip() or None,
                        example_en=str(row.get("example_en", "")).strip() or None,
                        example_vn=str(row.get("example_vn", "")).strip() or None,
                        audio_url=str(row.get("audio_url", "")).strip() or None,
                        image_url=str(row.get("image_url", "")).strip() or None,
                        difficulty=int(row.get("difficulty", 1)),
                        tags=str(row.get("tags", "")).strip() or None,
                        frequency_rank=int(row.get("frequency_rank", 0))
                        if pd.notna(row.get("frequency_rank"))
                        else None,
                    )

                    batch.append(word)

                    if len(batch) >= batch_size:
                        db_session.add_all(batch)
                        db_session.commit()
                        stats["added"] += len(batch)
                        batch = []

                except Exception as e:
                    logger.error(f"Error processing row: {e}")
                    stats["errors"] += 1
                    continue

            # Add remaining batch
            if batch:
                db_session.add_all(batch)
                db_session.commit()
                stats["added"] += len(batch)

        except ImportError:
            # Fallback to built-in csv module
            logger.info("pandas not available, using built-in csv module")

            with open(file_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)

                # Normalize column names
                reader.fieldnames = [
                    name.lower().strip() for name in reader.fieldnames
                ]

                # Check required columns
                if "word" not in reader.fieldnames or "meaning_vn" not in reader.fieldnames:
                    raise ValueError("Required columns 'word' and 'meaning_vn' not found")

                batch = []
                for row in reader:
                    try:
                        word_text = row["word"].strip()
                        if not word_text:
                            continue

                        # Check if word already exists
                        existing = (
                            db_session.query(Word)
                            .filter(Word.word == word_text)
                            .first()
                        )

                        if existing:
                            stats["skipped"] += 1
                            continue

                        # Create new word
                        word = Word(
                            word=word_text,
                            meaning_vn=row["meaning_vn"].strip(),
                            pos=row.get("pos", "").strip() or None,
                            pronunciation=row.get("pronunciation", "").strip()
                            or None,
                            meaning_en=row.get("meaning_en", "").strip() or None,
                            example_en=row.get("example_en", "").strip() or None,
                            example_vn=row.get("example_vn", "").strip() or None,
                            audio_url=row.get("audio_url", "").strip() or None,
                            image_url=row.get("image_url", "").strip() or None,
                            difficulty=int(row.get("difficulty", 1)),
                            tags=row.get("tags", "").strip() or None,
                            frequency_rank=int(row.get("frequency_rank", 0))
                            if row.get("frequency_rank")
                            else None,
                        )

                        batch.append(word)

                        if len(batch) >= batch_size:
                            db_session.add_all(batch)
                            db_session.commit()
                            stats["added"] += len(batch)
                            batch = []

                    except Exception as e:
                        logger.error(f"Error processing row: {e}")
                        stats["errors"] += 1
                        continue

                # Add remaining batch
                if batch:
                    db_session.add_all(batch)
                    db_session.commit()
                    stats["added"] += len(batch)

    except Exception as e:
        logger.error(f"Import failed: {e}")
        raise

    logger.info(
        f"Import completed: {stats['added']} added, {stats['skipped']} skipped, {stats['errors']} errors"
    )

    return stats
