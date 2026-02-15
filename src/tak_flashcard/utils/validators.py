"""Input validation helpers."""

from __future__ import annotations


def is_positive_int(value: str) -> bool:
    """Return True if the string represents a positive integer."""

    return value.isdigit() and int(value) > 0
