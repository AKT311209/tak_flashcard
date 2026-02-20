"""Application configuration values, paths, and shared constants."""

from __future__ import annotations

import sys
from enum import Enum
from pathlib import Path

APP_NAME = "Tak Flashcard"
PACKAGE_ROOT = Path(__file__).resolve().parent


def _get_data_dir() -> Path:
    """Determine data directory based on whether running from exe or source."""
    if getattr(sys, "frozen", False):
        exe_dir = Path(sys.executable).parent
        data_dir = exe_dir / "tak_flashcard_data"
    else:
        data_dir = PACKAGE_ROOT / "data"
    return data_dir


DATA_DIR = _get_data_dir()
DB_PATH = DATA_DIR / "flashcard.db"
SETTINGS_PATH = DATA_DIR / "user_settings.json"

WINDOW_WIDTH = 960
WINDOW_HEIGHT = 700

STYLE_THEME = "clam"


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
DEFAULT_WINDOW_SIZE = (960, 700)
DEFAULT_SHOW_SCORE_PENALTY = 10
DEFAULT_SHOW_LIMIT = 0
DEFAULT_SHOW_TIME_PENALTY = 10
DEFAULT_WRONG_ANSWER_PENALTY = 10


def ensure_data_dirs() -> None:
    """Create required data directories if they are missing."""

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "vocab").mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "seed").mkdir(parents=True, exist_ok=True)


def ensure_executable_data_dirs() -> None:
    """Ensure data directories exist when running from the built executable."""

    if not getattr(sys, "frozen", False):
        return

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "vocab").mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "seed").mkdir(parents=True, exist_ok=True)
