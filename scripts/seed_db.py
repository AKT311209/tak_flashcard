#!/usr/bin/env python3
"""Seed the database with sample vocabulary data."""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from tak_flashcard.db.db import get_db, init_db
from tak_flashcard.db.models import Word


def main():
    """Seed database with sample words."""
    print("Seeding database with sample vocabulary...")

    # Initialize database
    init_db()

    # Sample vocabulary words
    sample_words = [
        {
            "word": "hello",
            "pos": "interjection",
            "pronunciation": "həˈləʊ",
            "english": "a greeting",
            "vietnamese": "xin chào",
            "difficulty": 1,
        },
        {
            "word": "goodbye",
            "pos": "interjection",
            "pronunciation": "ɡʊdˈbaɪ",
            "english": "a parting phrase",
            "vietnamese": "tạm biệt",
            "difficulty": 1,
        },
        {
            "word": "thank",
            "pos": "verb",
            "pronunciation": "θæŋk",
            "english": "to express gratitude",
            "vietnamese": "cảm ơn",
            "difficulty": 1,
        },
        {
            "word": "beautiful",
            "pos": "adjective",
            "pronunciation": "ˈbjuːtɪfl",
            "english": "pleasing to the senses",
            "vietnamese": "đẹp",
            "difficulty": 2,
        },
        {
            "word": "friend",
            "pos": "noun",
            "pronunciation": "frend",
            "english": "a person you know well and like",
            "vietnamese": "bạn bè",
            "difficulty": 1,
        },
        {
            "word": "love",
            "pos": "verb",
            "pronunciation": "lʌv",
            "english": "to have deep affection for",
            "vietnamese": "yêu",
            "difficulty": 1,
        },
        {
            "word": "happy",
            "pos": "adjective",
            "pronunciation": "ˈhæpi",
            "english": "feeling pleasure or contentment",
            "vietnamese": "hạnh phúc",
            "difficulty": 1,
        },
        {
            "word": "learn",
            "pos": "verb",
            "pronunciation": "lɜːn",
            "english": "to acquire knowledge or skill",
            "vietnamese": "học",
            "difficulty": 2,
        },
        {
            "word": "understand",
            "pos": "verb",
            "pronunciation": "ʌndəˈstænd",
            "english": "to comprehend",
            "vietnamese": "hiểu",
            "difficulty": 2,
        },
        {
            "word": "important",
            "pos": "adjective",
            "pronunciation": "ɪmˈpɔːtnt",
            "english": "of great significance",
            "vietnamese": "quan trọng",
            "difficulty": 2,
        },
    ]

    try:
        db = get_db()

        added = 0
        skipped = 0

        for word_data in sample_words:
            # Check if word already exists
            existing = (
                db.query(Word).filter(Word.word == word_data["word"]).first()
            )

            if existing:
                skipped += 1
                continue

            # Create new word
            word = Word(**word_data)
            db.add(word)
            added += 1

        db.commit()

        print("-" * 50)
        print(f"✓ Seeding completed!")
        print(f"  - Added: {added}")
        print(f"  - Skipped: {skipped}")

    except Exception as e:
        print(f"✗ Error seeding database: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
