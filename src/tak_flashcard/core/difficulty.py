"""Difficulty calculation and word selection weight calculation."""

from tak_flashcard.constants import EPSILON


def calculate_word_difficulty(correct_count: int, display_count: int) -> float:
    """
    Calculate difficulty score for a word based on user performance.

    Args:
        correct_count: Number of times answered correctly
        display_count: Number of times word was displayed

    Returns:
        Difficulty score between 0 (easy) and 1 (hard)
    """
    return 1 - (correct_count / (display_count + EPSILON))


def calculate_selection_weight(word_difficulty: float, user_setting: int) -> float:
    """
    Calculate selection weight for a word based on difficulty and user setting.

    Higher user settings favor harder words, lower settings favor easier words.

    Args:
        word_difficulty: Word's difficulty score (0-1)
        user_setting: User's difficulty setting (1-5)

    Returns:
        Selection weight (higher = more likely to be selected)
    """
    bias = user_setting - 3

    if bias < 0:
        weight = (1 - word_difficulty) ** abs(bias)
    elif bias > 0:
        weight = word_difficulty ** bias
    else:
        weight = 1.0

    return max(weight, EPSILON)
