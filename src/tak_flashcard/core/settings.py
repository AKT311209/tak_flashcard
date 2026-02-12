"""Settings management and persistence."""

import json
from pathlib import Path
from typing import Any, Dict
from tak_flashcard.config import (
    SETTINGS_PATH, DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT,
    DEFAULT_QUESTION_COUNT, DEFAULT_TIME_LIMIT, DEFAULT_DIFFICULTY,
    MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT, MAX_WINDOW_WIDTH, MAX_WINDOW_HEIGHT,
    MIN_QUESTION_COUNT, MAX_QUESTION_COUNT, MIN_TIME_LIMIT, MAX_TIME_LIMIT,
    MIN_DIFFICULTY, MAX_DIFFICULTY
)
from tak_flashcard.constants import FlashcardMode, Theme, FontSize, AnimationSpeed


DEFAULT_SETTINGS = {
    "appearance": {
        "theme": Theme.LIGHT.value,
        "font_size": FontSize.MEDIUM.value,
        "window_width": DEFAULT_WINDOW_WIDTH,
        "window_height": DEFAULT_WINDOW_HEIGHT
    },
    "defaults": {
        "flashcard_mode": FlashcardMode.ENDLESS.value,
        "difficulty_level": DEFAULT_DIFFICULTY,
        "question_count": DEFAULT_QUESTION_COUNT,
        "time_limit": DEFAULT_TIME_LIMIT
    },
    "preferences": {
        "sound_enabled": False,
        "animation_speed": AnimationSpeed.NORMAL.value
    }
}


class SettingsManager:
    """Manages application settings and persistence."""

    def __init__(self, settings_path: Path = SETTINGS_PATH):
        """
        Initialize settings manager.

        Args:
            settings_path: Path to settings JSON file
        """
        self.settings_path = settings_path
        self.settings = self._load_settings()

    def _load_settings(self) -> Dict:
        """
        Load settings from file or return defaults.

        Returns:
            Settings dictionary
        """
        if self.settings_path.exists():
            try:
                with open(self.settings_path, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    return self._merge_with_defaults(loaded)
            except Exception:
                return DEFAULT_SETTINGS.copy()
        return DEFAULT_SETTINGS.copy()

    def _merge_with_defaults(self, loaded: Dict) -> Dict:
        """
        Merge loaded settings with defaults to ensure all keys exist.

        Args:
            loaded: Loaded settings dictionary

        Returns:
            Merged settings dictionary
        """
        merged = DEFAULT_SETTINGS.copy()
        for category, values in loaded.items():
            if category in merged and isinstance(values, dict):
                merged[category].update(values)
        return merged

    def save_settings(self) -> bool:
        """
        Save current settings to file.

        Returns:
            True if successful, False otherwise
        """
        try:
            self.settings_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.settings_path, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2)
            return True
        except Exception:
            return False

    def get(self, category: str, key: str, default: Any = None) -> Any:
        """
        Get a setting value.

        Args:
            category: Settings category
            key: Setting key
            default: Default value if not found

        Returns:
            Setting value
        """
        return self.settings.get(category, {}).get(key, default)

    def set(self, category: str, key: str, value: Any):
        """
        Set a setting value.

        Args:
            category: Settings category
            key: Setting key
            value: New value
        """
        if category not in self.settings:
            self.settings[category] = {}
        self.settings[category][key] = value

    def validate_and_set(self, category: str, key: str, value: Any) -> bool:
        """
        Validate and set a setting value.

        Args:
            category: Settings category
            key: Setting key
            value: New value

        Returns:
            True if valid and set, False otherwise
        """
        if not self._validate_setting(category, key, value):
            return False
        self.set(category, key, value)
        return True

    def _validate_setting(self, category: str, key: str, value: Any) -> bool:
        """
        Validate a setting value.

        Args:
            category: Settings category
            key: Setting key
            value: Value to validate

        Returns:
            True if valid, False otherwise
        """
        if category == "appearance":
            if key == "window_width":
                return MIN_WINDOW_WIDTH <= value <= MAX_WINDOW_WIDTH
            elif key == "window_height":
                return MIN_WINDOW_HEIGHT <= value <= MAX_WINDOW_HEIGHT
            elif key == "theme":
                return value in [t.value for t in Theme]
            elif key == "font_size":
                return value in [f.value for f in FontSize]

        elif category == "defaults":
            if key == "difficulty_level":
                return MIN_DIFFICULTY <= value <= MAX_DIFFICULTY
            elif key == "question_count":
                return MIN_QUESTION_COUNT <= value <= MAX_QUESTION_COUNT
            elif key == "time_limit":
                return MIN_TIME_LIMIT <= value <= MAX_TIME_LIMIT
            elif key == "flashcard_mode":
                return value in [m.value for m in FlashcardMode]

        elif category == "preferences":
            if key == "sound_enabled":
                return isinstance(value, bool)
            elif key == "animation_speed":
                return value in [a.value for a in AnimationSpeed]

        return True

    def reset_to_defaults(self):
        """Reset all settings to defaults."""
        self.settings = DEFAULT_SETTINGS.copy()

    def get_all(self) -> Dict:
        """
        Get all settings.

        Returns:
            Complete settings dictionary
        """
        return self.settings.copy()
