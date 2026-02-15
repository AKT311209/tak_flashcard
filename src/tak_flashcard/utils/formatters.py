"""Formatting helpers."""

from __future__ import annotations


def format_direction(direction: str) -> str:
    """Pretty-print direction labels."""

    mapping = {
        "eng_to_vn": "English → Vietnamese",
        "vn_to_eng": "Vietnamese → English",
        "mixed": "Mixed",
    }
    return mapping.get(direction, direction)
