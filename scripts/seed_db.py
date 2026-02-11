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
            "meaning_vn": "xin chào",
            "meaning_en": "a greeting",
            "example_en": "Hello! How are you?",
            "example_vn": "Xin chào! Bạn khỏe không?",
            "difficulty": 1,
            "tags": "greeting,common",
            "frequency_rank": 100,
        },
        {
            "word": "goodbye",
            "pos": "interjection",
            "pronunciation": "ɡʊdˈbaɪ",
            "meaning_vn": "tạm biệt",
            "meaning_en": "a parting phrase",
            "example_en": "Goodbye! See you later.",
            "example_vn": "Tạm biệt! Hẹn gặp lại.",
            "difficulty": 1,
            "tags": "greeting,common",
            "frequency_rank": 150,
        },
        {
            "word": "thank",
            "pos": "verb",
            "pronunciation": "θæŋk",
            "meaning_vn": "cảm ơn",
            "meaning_en": "to express gratitude",
            "example_en": "Thank you for your help.",
            "example_vn": "Cảm ơn bạn đã giúp đỡ.",
            "difficulty": 1,
            "tags": "politeness,common",
            "frequency_rank": 200,
        },
        {
            "word": "beautiful",
            "pos": "adjective",
            "pronunciation": "ˈbjuːtɪfl",
            "meaning_vn": "đẹp",
            "meaning_en": "pleasing to the senses",
            "example_en": "She has a beautiful smile.",
            "example_vn": "Cô ấy có nụ cười đẹp.",
            "difficulty": 2,
            "tags": "adjective,common",
            "frequency_rank": 500,
        },
        {
            "word": "friend",
            "pos": "noun",
            "pronunciation": "frend",
            "meaning_vn": "bạn bè",
            "meaning_en": "a person you know well and like",
            "example_en": "She is my best friend.",
            "example_vn": "Cô ấy là bạn thân nhất của tôi.",
            "difficulty": 1,
            "tags": "relationship,common",
            "frequency_rank": 300,
        },
        {
            "word": "love",
            "pos": "verb",
            "pronunciation": "lʌv",
            "meaning_vn": "yêu",
            "meaning_en": "to have deep affection for",
            "example_en": "I love my family.",
            "example_vn": "Tôi yêu gia đình tôi.",
            "difficulty": 1,
            "tags": "emotion,common",
            "frequency_rank": 250,
        },
        {
            "word": "happy",
            "pos": "adjective",
            "pronunciation": "ˈhæpi",
            "meaning_vn": "hạnh phúc",
            "meaning_en": "feeling pleasure or contentment",
            "example_en": "I am happy to see you.",
            "example_vn": "Tôi rất vui được gặp bạn.",
            "difficulty": 1,
            "tags": "emotion,common",
            "frequency_rank": 400,
        },
        {
            "word": "learn",
            "pos": "verb",
            "pronunciation": "lɜːn",
            "meaning_vn": "học",
            "meaning_en": "to acquire knowledge or skill",
            "example_en": "I want to learn Vietnamese.",
            "example_vn": "Tôi muốn học tiếng Việt.",
            "difficulty": 2,
            "tags": "education,common",
            "frequency_rank": 600,
        },
        {
            "word": "understand",
            "pos": "verb",
            "pronunciation": "ʌndəˈstænd",
            "meaning_vn": "hiểu",
            "meaning_en": "to comprehend",
            "example_en": "Do you understand me?",
            "example_vn": "Bạn có hiểu tôi không?",
            "difficulty": 2,
            "tags": "communication,common",
            "frequency_rank": 700,
        },
        {
            "word": "important",
            "pos": "adjective",
            "pronunciation": "ɪmˈpɔːtnt",
            "meaning_vn": "quan trọng",
            "meaning_en": "of great significance",
            "example_en": "This is very important.",
            "example_vn": "Điều này rất quan trọng.",
            "difficulty": 2,
            "tags": "adjective,common",
            "frequency_rank": 800,
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
