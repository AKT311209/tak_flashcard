"""Input validation utilities."""

from typing import Any


def validate_int_range(value: Any, min_val: int, max_val: int) -> bool:
    """
    Validate that value is an integer within range.

    Args:
        value: Value to validate
        min_val: Minimum allowed value
        max_val: Maximum allowed value

    Returns:
        True if valid, False otherwise
    """
    try:
        int_val = int(value)
        return min_val <= int_val <= max_val
    except (TypeError, ValueError):
        return False


def validate_string_not_empty(value: Any) -> bool:
    """
    Validate that value is a non-empty string.

    Args:
        value: Value to validate

    Returns:
        True if valid, False otherwise
    """
    return isinstance(value, str) and len(value.strip()) > 0


def sanitize_string(value: str) -> str:
    """
    Sanitize string input by trimming whitespace.

    Args:
        value: String to sanitize

    Returns:
        Sanitized string
    """
    return value.strip() if isinstance(value, str) else ""
