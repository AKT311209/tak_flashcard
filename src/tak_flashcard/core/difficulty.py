"""Formula for calculating how hard a word is for the user.

A word's difficulty is a number between 0 and 1:
  - 0.0  → the user always gets it right (easy)
  - 1.0  → the user never gets it right (hard)
  - 0.5  → the user gets it right about half the time

This score is stored in the database after every answer and feeds the
word-selection logic in ``core/selectors.py``.

Calling order:
  db/repo.py :: update_word_stats() → difficulty_score()
"""

from __future__ import annotations


def difficulty_score(display_count: int, correct_count: int) -> float:
    """Calculate how hard a word is, based on the user's answer history.

    The more often the user gets a word wrong, the closer the result is
    to 1.0 (hard).  The more they get it right, the closer it is to 0.0
    (easy).

    A tiny value (epsilon) is added to ``display_count`` to avoid
    dividing by zero when a word has never been shown before.

    Parameters:
        display_count: How many times this word has appeared as a question.
        correct_count: How many times the user answered it correctly.

    Returns:
        A float between 0.0 (always correct) and ~1.0 (never correct).

    Examples:
        10 shown, 9 correct  →  1 - 9/10  = 0.1  (easy word)
        10 shown, 1 correct  →  1 - 1/10  = 0.9  (hard word)
        0 shown              →  1 - 0/0   ≈ 1.0  (unknown, treated as hard)
    """

    epsilon = 1e-6
    return 1.0 - (correct_count / (display_count + epsilon))
