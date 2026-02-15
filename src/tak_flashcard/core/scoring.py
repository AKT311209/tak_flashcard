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
SPEED_BONUS_MAX = 10
PENALTY_POINTS = 10


def speed_bonus(response_seconds: float, time_limit: int) -> int:
    """Calculate speed bonus inversely proportional to response time."""

    if response_seconds <= 0:
        return SPEED_BONUS_MAX
    ratio = max(min(response_seconds / max(time_limit, 1), 1.0), 0.0)
    return int(SPEED_BONUS_MAX * (1 - ratio))


def apply_scoring(current_score: int, correct: bool, response_seconds: float | None = None, time_limit: int | None = None) -> ScoreResult:
    """Apply scoring rules and return updated totals."""

    delta = BASE_POINTS if correct else -PENALTY_POINTS
    if correct and response_seconds is not None and time_limit:
        delta += speed_bonus(response_seconds, time_limit)
    return ScoreResult(total=current_score + delta, delta=delta, correct=correct)
