"""Scoring and penalties."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ScoreResult:
    """Represents a scoring outcome."""

    total: int
    delta: int
    correct: bool


BASE_POINTS = 10
PENALTY_POINTS = 10


def apply_scoring(
    current_score: int,
    correct: bool,
    penalty_points: int = PENALTY_POINTS,
) -> ScoreResult:
    """Apply scoring rules and return updated totals."""

    penalty = max(penalty_points, 0)
    delta = BASE_POINTS if correct else -penalty
    return ScoreResult(total=current_score + delta, delta=delta, correct=correct)
