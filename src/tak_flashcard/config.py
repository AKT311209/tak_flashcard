"""Central configuration — all shared constants, paths, and option types.

This is the single source of truth for values used across the whole app.
Any number that controls behaviour (default question count, window size,
penalty defaults, etc.) or any symbolic name (mode names, direction names)
lives here so it can be changed in one place and take effect everywhere.

Every other module imports from this file; nothing here imports from the
rest of the application (it has no internal dependencies).
"""

from __future__ import annotations

import sys
from enum import Enum
from pathlib import Path

APP_NAME = "Tak Flashcard"
PACKAGE_ROOT = Path(__file__).resolve().parent


def _get_data_dir() -> Path:
    """Find the folder where runtime data (database, settings) should live.

    When the app is packaged as a Windows EXE the data folder is placed
    next to the executable (``tak_flashcard_data/``).  When running from
    Python source it lives inside the package at ``src/tak_flashcard/data/``.

    Returns:
        Absolute path to the data directory (may not exist yet).
    """

    if getattr(sys, "frozen", False):
        exe_dir = Path(sys.executable).parent
        data_dir = exe_dir / "tak_flashcard_data"
    else:
        data_dir = PACKAGE_ROOT / "data"
    return data_dir


DATA_DIR = _get_data_dir()
DB_PATH = DATA_DIR / "flashcard.db"
SETTINGS_PATH = DATA_DIR / "user_settings.json"

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 750

STYLE_THEME = "clam"


class Mode(str, Enum):
    """The three flashcard study modes available to the user.

    Values:
        ENDLESS  — Practice indefinitely; no question limit or timer.
        SPEED    — Race against a countdown timer.
        TESTING  — Answer a fixed number of questions (exam style).
    """

    ENDLESS = "endless"
    SPEED = "speed"
    TESTING = "testing"


class Direction(str, Enum):
    """Which language is shown as the question and which as the answer.

    Values:
        ENG_TO_VN — English word shown; user picks the Vietnamese answer.
        VN_TO_ENG — Vietnamese word shown; user picks the English answer.
        MIXED     — Each card randomly picks one of the two directions above.
    """

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
    """Create the data folder hierarchy if it does not already exist.

    Safe to call multiple times — uses ``exist_ok=True`` so it does nothing
    if the directories are already present.  Called on import by modules
    that need to write data files (settings, database).
    """

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "vocab").mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "seed").mkdir(parents=True, exist_ok=True)


def ensure_executable_data_dirs() -> None:
    """Create data folders when running from the packaged EXE.

    Identical to :func:`ensure_data_dirs` but only runs when the app has
    been frozen by PyInstaller (i.e. ``sys.frozen`` is set).  Called once
    at the very start of :func:`main` before anything else is imported.
    """

    if not getattr(sys, "frozen", False):
        return

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "vocab").mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "seed").mkdir(parents=True, exist_ok=True)
