"""Constants and enumerations for the application."""

from enum import Enum


class FlashcardMode(Enum):
    """Flashcard study modes."""
    ENDLESS = "endless"
    SPEED = "speed"
    TESTING = "testing"


class Direction(Enum):
    """Translation direction for flashcards."""
    ENG_TO_VN = "eng_to_vn"
    VN_TO_ENG = "vn_to_eng"
    MIXED = "mixed"


class PenaltyType(Enum):
    """Penalty types for Show Answer feature."""
    SCORE = "score"
    TIME = "time"
    HP = "hp"


class Theme(Enum):
    """UI theme options."""
    LIGHT = "light"
    DARK = "dark"


class FontSize(Enum):
    """Font size options."""
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"


class AnimationSpeed(Enum):
    """Animation speed options."""
    FAST = "fast"
    NORMAL = "normal"
    SLOW = "slow"
    OFF = "off"


MODE_LABELS = {
    FlashcardMode.ENDLESS: "Endless",
    FlashcardMode.SPEED: "Speed",
    FlashcardMode.TESTING: "Testing"
}

DIRECTION_LABELS = {
    Direction.ENG_TO_VN: "English → Vietnamese",
    Direction.VN_TO_ENG: "Vietnamese → English",
    Direction.MIXED: "Mixed"
}

PENALTY_LABELS = {
    PenaltyType.SCORE: "Score Deduction (-10 points)",
    PenaltyType.TIME: "Time Deduction (-10 seconds)",
    PenaltyType.HP: "HP Limit (max 3 uses)"
}

BASE_POINTS = 10
PENALTY_POINTS = 10
PENALTY_TIME = 10
MAX_HP_USES = 3
EPSILON = 0.001
