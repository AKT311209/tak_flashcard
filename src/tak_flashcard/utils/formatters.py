"""Data formatting utilities."""

import unicodedata


def normalize_unicode(text: str) -> str:
    """Normalize unicode text to NFC for consistent display and storage.

    Args:
        text: Input string

    Returns:
        NFC-normalized string (returns original if not a str)
    """
    if not isinstance(text, str):
        return text
    try:
        return unicodedata.normalize("NFC", text)
    except Exception:
        return text


def format_time(seconds: float) -> str:
    """
    Format seconds into MM:SS format.

    Args:
        seconds: Time in seconds

    Returns:
        Formatted time string
    """
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes}:{secs:02d}"


def format_difficulty(difficulty: float) -> str:
    """
    Format difficulty score for display.

    Args:
        difficulty: Difficulty score (0-1)

    Returns:
        Formatted difficulty string
    """
    return f"{difficulty:.2f}"


def format_percentage(value: float, total: float) -> str:
    """
    Format percentage for display.

    Args:
        value: Numerator value
        total: Denominator value

    Returns:
        Formatted percentage string
    """
    if total == 0:
        return "0.0%"
    percentage = (value / total) * 100
    return f"{percentage:.1f}%"
