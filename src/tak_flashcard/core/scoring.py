"""Scoring rules for flashcard sessions.

Every correct answer gives the user points; wrong answers may deduct
points (depending on configuration).  This module calculates the new
score and the delta (change) after each answer.

Constants:
    BASE_POINTS   — points awarded for a correct answer (+10).
    PENALTY_POINTS — default points deducted for a wrong answer (−10).

Calling order:
  features/flashcard/service.py :: submit_answer() → apply_scoring()
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ScoreResult:
    """The outcome of one scoring calculation.

    Attributes:
        total: The player's new cumulative score after this answer.
        delta: How many points were added (positive) or removed (negative).
        correct: Whether the answer was right.
    """

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
    """Update the player's score after one answer and return the result.

    Correct answer  → adds ``BASE_POINTS`` (+10) to the score.
    Wrong answer    → subtracts ``penalty_points`` (default −10).
    Negative penalties are ignored (treated as 0) to prevent unexpected
    score increases from misconfiguration.

    Parameters:
        current_score: The player's score before this answer.
        correct: ``True`` if the player chose the right answer.
        penalty_points: Points to deduct for a wrong answer.
            Defaults to :data:`PENALTY_POINTS` (10).

    Returns:
        A :class:`ScoreResult` with the new total, the change, and
        whether the answer was correct.
    """

    penalty = max(penalty_points, 0)
    delta = BASE_POINTS if correct else -penalty
    return ScoreResult(total=current_score + delta, delta=delta, correct=correct)
