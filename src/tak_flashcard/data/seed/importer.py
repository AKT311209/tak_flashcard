"""CSV importer for vocabulary data."""

import csv
from pathlib import Path
from typing import List, Dict, Optional
from tak_flashcard.db import get_session, close_session, WordRepository
from tak_flashcard.config import VOCAB_SOURCE, MIN_WORDS_REQUIRED


class VocabularyImporter:
    """Imports vocabulary data from CSV files into the database."""

    def __init__(self, csv_path: Optional[Path] = None):
        """
        Initialize the importer.

        Args:
            csv_path: Path to CSV file (defaults to VOCAB_SOURCE)
        """
        self.csv_path = csv_path or VOCAB_SOURCE
        self.session = None
        self.repo = None

    def validate_csv(self) -> bool:
        """
        Validate that the CSV file exists and has required columns.

        Returns:
            True if valid, False otherwise
        """
        if not self.csv_path.exists():
            return False

        try:
            with open(self.csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                headers = reader.fieldnames
                required_cols = ['english', 'pronunciation',
                                 'vietnamese', 'part_of_speech']

                return all(col in headers for col in required_cols)
        except Exception:
            return False

    def parse_csv(self) -> List[Dict]:
        """
        Parse CSV file and extract vocabulary data.

        Returns:
            List of word dictionaries
        """
        words = []

        with open(self.csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)

            for row in reader:
                word_data = {
                    'english': row['english'].strip(),
                    'pronunciation': row['pronunciation'].strip(),
                    'vietnamese': row['vietnamese'].strip(),
                    'part_of_speech': row['part_of_speech'].strip(),
                    'display_count': 0,
                    'correct_count': 0,
                    'difficulty': 1.0
                }
                words.append(word_data)

        return words

    def import_data(self, progress_callback=None) -> tuple[bool, str]:
        """
        Import vocabulary data from CSV into database.

        Args:
            progress_callback: Optional callback function(current, total) for progress

        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            if not self.validate_csv():
                return False, "CSV file is missing or invalid format"

            self.session = get_session()
            self.repo = WordRepository(self.session)

            existing_count = self.repo.count()
            if existing_count >= MIN_WORDS_REQUIRED:
                close_session(self.session)
                return True, f"Database already has {existing_count} words"

            words = self.parse_csv()

            if len(words) < MIN_WORDS_REQUIRED:
                close_session(self.session)
                return False, f"CSV has only {len(words)} words (need at least {MIN_WORDS_REQUIRED})"

            batch_size = 100
            total = len(words)

            for i in range(0, total, batch_size):
                batch = words[i:i + batch_size]
                self.repo.bulk_insert(batch)

                if progress_callback:
                    progress_callback(min(i + batch_size, total), total)

            final_count = self.repo.count()
            close_session(self.session)

            return True, f"Successfully imported {final_count} words"

        except Exception as e:
            if self.session:
                close_session(self.session)
            return False, f"Import failed: {str(e)}"


def check_and_import_if_needed(progress_callback=None) -> tuple[bool, str]:
    """
    Check if database has enough words, import if needed.

    Args:
        progress_callback: Optional callback function(current, total) for progress

    Returns:
        Tuple of (success: bool, message: str)
    """
    session = get_session()
    repo = WordRepository(session)
    count = repo.count()
    close_session(session)

    if count >= MIN_WORDS_REQUIRED:
        return True, f"Database has {count} words"

    importer = VocabularyImporter()
    return importer.import_data(progress_callback)
