"""Shared constants and enumerations for Tak Flashcard."""

from enum import Enum


class Mode(str, Enum):
    """Flashcard study modes."""

    ENDLESS = "endless"
    SPEED = "speed"
    TESTING = "testing"


class Direction(str, Enum):
    """Translation direction options."""

    ENG_TO_VN = "eng_to_vn"
    VN_TO_ENG = "vn_to_eng"
    MIXED = "mixed"


DIFFICULTY_LEVELS = [1, 2, 3, 4, 5]

DEFAULT_QUESTION_COUNT = 20
DEFAULT_TIME_LIMIT = 300
DEFAULT_DIFFICULTY_LEVEL = 3
DEFAULT_FLASHCARD_MODE = Mode.ENDLESS
DEFAULT_DIRECTION = Direction.ENG_TO_VN
DEFAULT_WINDOW_SIZE = (960, 640)
DEFAULT_SHOW_SCORE_PENALTY = 10
DEFAULT_SHOW_LIMIT = 0
DEFAULT_SHOW_TIME_PENALTY = 10
DEFAULT_WRONG_ANSWER_PENALTY = 10
