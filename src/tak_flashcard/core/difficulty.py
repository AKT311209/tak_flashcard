"""Difficulty calculation utilities."""

from __future__ import annotations


def difficulty_score(display_count: int, correct_count: int) -> float:
    """Calculate difficulty based on correct ratio."""

    epsilon = 1e-6
    return 1.0 - (correct_count / (display_count + epsilon))
