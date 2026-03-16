"""Word selection logic for flashcard sessions.

This module decides WHICH word to show the user next.
It uses weighted random sampling so that the user's chosen difficulty level
controls how often easy vs. hard words appear.

Calling order:
  features/flashcard/service.py
      → select_next_word()
          → _choose_weighted_word()
              → _clamp_difficulty()          (once per call)
              → _calculate_difficulty_weight()  (once per word in the list)
"""

from __future__ import annotations

import math
import random
from typing import Sequence

from tak_flashcard.config import Direction, DIFFICULTY_LEVELS
from tak_flashcard.db.models import Word


def select_next_word(
    words: Sequence[Word],
    difficulty_level: int,
    direction: Direction,
) -> Word | None:
    """Pick the next word to show in a flashcard session.

    This is the main entry point called by the flashcard service every time
    a new card is needed.  It delegates to the weighted random draw below.

    Parameters:
        words: The full list of vocabulary words to choose from.
        difficulty_level: The user's selected difficulty (1 = easiest, 5 = hardest).
        direction: Translation direction for this card (English→Vietnamese,
            Vietnamese→English, or Mixed).  Reserved for future filtering;
            the current draw is direction-agnostic.

    Returns:
        One :class:`Word` chosen by weighted random draw, or ``None`` if
        the word list is empty.
    """

    return _choose_weighted_word(words, difficulty_level, direction)


def _choose_weighted_word(
    words: Sequence[Word],
    difficulty_level: int,
    _direction: Direction,
) -> Word | None:
    """Run the weighted random draw to pick one word.

    Every word in the list gets a numeric weight based on its stored
    difficulty score and the user's chosen difficulty level.  Words with
    a higher weight are more likely to be drawn.  The built-in
    ``random.choices`` function performs the final selection.

    Parameters:
        words: Vocabulary words to choose from.
        difficulty_level: User-selected level (1–5); clamped to a valid range
            before use.
        _direction: Kept for signature consistency; not used by the draw.

    Returns:
        The selected :class:`Word`, or ``None`` if ``words`` is empty.
    """

    if not words:
        return None

    clamped = _clamp_difficulty(difficulty_level)
    weights: list[float] = []
    for word in words:
        raw = word.difficulty
        base = float(raw) if raw is not None else 0.5
        weight = _calculate_difficulty_weight(clamped, base)
        weights.append(max(weight, 0.01))   # floor prevents zero-weight words

    return random.choices(words, weights=weights, k=1)[0]


def _clamp_difficulty(level: int) -> int:
    """Keep a difficulty level inside the valid 1–5 range.

    If a value outside the configured range is passed in, this clips it to
    the nearest valid boundary so the weight formula always receives a safe
    input.

    Parameters:
        level: Raw difficulty number.

    Returns:
        The same number if already within [1, 5], otherwise the nearest bound.
    """

    min_level = min(DIFFICULTY_LEVELS)
    max_level = max(DIFFICULTY_LEVELS)
    return max(min(level, max_level), min_level)


def _calculate_difficulty_weight(level: int, base: float) -> float:
    """Return how likely a word is to be selected, given the difficulty setting.

    Uses an exponential curve (e^x) so that each step on the 1–5 slider
    noticeably shifts the probability gap between easy and hard words.

    How to read each level:
      Level 1 (easiest) — words the user already knows well (low ``base``)
                          get a HIGH weight; unfamiliar words get a LOW weight.
      Level 2            — mild bias toward easier words.
      Level 3 (balanced) — every word has weight 1.0; all equally likely.
      Level 4            — mild bias toward harder words.
      Level 5 (hardest)  — words the user struggles with (high ``base``)
                           get a HIGH weight; known words get a LOW weight.

    Parameters:
        level: Clamped difficulty level (1–5).
        base: The word's individual difficulty score (0.0 = easy, 1.0 = hard).

    Returns:
        A positive float that serves as the selection weight for this word.
    """

    if level == 1:
        return math.exp(-2.0 * base)   # strongly favours easy words
    if level == 2:
        return math.exp(-base)          # mildly favours easy words
    if level == 3:
        return 1.0                      # all words equally likely
    if level == 4:
        return math.exp(base)           # mildly favours hard words
    return math.exp(2.0 * base)         # strongly favours hard words
