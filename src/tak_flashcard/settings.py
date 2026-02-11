"""Settings module for persistent application settings."""

import json
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

# Settings file location
SETTINGS_DIR = Path.home() / ".tak_flashcard"
SETTINGS_FILE = SETTINGS_DIR / "settings.json"

# Default settings
DEFAULT_SETTINGS = {
    "volume": 0.7,
    "enable_animations": True,
    "default_mode": "Endless",
    "default_direction": "E->V",
    "default_difficulty": 1,
    "default_question_count": 10,
    "default_time_per_question": 30,
    "reveal_penalty_points": 5,
    "reveal_penalty_time": 10,
    "initial_hp": 3,
}


class Settings:
    """Settings manager for persistent application configuration."""

    def __init__(self):
        """Initialize settings manager."""
        self._settings = DEFAULT_SETTINGS.copy()
        self._ensure_settings_dir()
        self.load()

    def _ensure_settings_dir(self) -> None:
        """Ensure the settings directory exists."""
        SETTINGS_DIR.mkdir(parents=True, exist_ok=True)

    def load(self) -> None:
        """Load settings from file."""
        if not SETTINGS_FILE.exists():
            logger.info("Settings file not found, using defaults")
            self.save()  # Create default settings file
            return

        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                loaded_settings = json.load(f)
                self._settings.update(loaded_settings)
            logger.info("Settings loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load settings: {e}")
            logger.info("Using default settings")

    def save(self) -> None:
        """Save settings to file."""
        try:
            with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
                json.dump(self._settings, f, indent=2)
            logger.info("Settings saved successfully")
        except Exception as e:
            logger.error(f"Failed to save settings: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a setting value.

        Args:
            key: Setting key
            default: Default value if key not found

        Returns:
            Setting value or default
        """
        return self._settings.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """
        Set a setting value.

        Args:
            key: Setting key
            value: Setting value
        """
        self._settings[key] = value

    def get_all(self) -> dict:
        """Get all settings as a dictionary."""
        return self._settings.copy()

    def reset_to_defaults(self) -> None:
        """Reset all settings to default values."""
        self._settings = DEFAULT_SETTINGS.copy()
        self.save()
        logger.info("Settings reset to defaults")


# Global settings instance
_settings_instance = None


def get_settings() -> Settings:
    """Get the global settings instance."""
    global _settings_instance
    if _settings_instance is None:
        _settings_instance = Settings()
    return _settings_instance
