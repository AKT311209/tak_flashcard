"""Dictionary service for browsing vocabulary."""

from __future__ import annotations

from typing import Iterable

from sqlalchemy.orm import Session

from tak_flashcard.db import repo
from tak_flashcard.db.models import Word


class DictionaryService:
    """Provide search, filter, and list capabilities for words."""

    def __init__(self, db: Session):
        """Create service with the provided database session."""

        self.db = db

    def all_words(self) -> Iterable[Word]:
        """Return all words sorted by English text."""

        return repo.list_words(self.db)

    def search(self, query: str) -> Iterable[Word]:
        """Search for words containing the query in English or Vietnamese."""

        if not query:
            return self.all_words()
        return repo.search_words(self.db, query)

    def filter_part(self, part: str) -> Iterable[Word]:
        """Filter words by part of speech."""

        return repo.filter_by_part_of_speech(self.db, part)
