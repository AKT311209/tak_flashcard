"""Application configuration values and paths."""

from __future__ import annotations

from pathlib import Path

APP_NAME = "Tak Flashcard"
PACKAGE_ROOT = Path(__file__).resolve().parent
DATA_DIR = PACKAGE_ROOT / "data"
VOCAB_PATH = DATA_DIR / "vocab" / "vocab_source.csv"
DB_PATH = DATA_DIR / "flashcard.db"
SETTINGS_PATH = DATA_DIR / "user_settings.json"
MIN_WORDS_REQUIRED = 1000

WINDOW_WIDTH = 960
WINDOW_HEIGHT = 640

STYLE_THEME = "clam"


def ensure_data_dirs() -> None:
    """Create required data directories if they are missing."""

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "vocab").mkdir(parents=True, exist_ok=True)
    (DATA_DIR / "seed").mkdir(parents=True, exist_ok=True)
