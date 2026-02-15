"""Settings management and persistence."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from tak_flashcard.config import SETTINGS_PATH, ensure_data_dirs
from tak_flashcard.constants import Direction, Mode

ensure_data_dirs()


@dataclass
class AppearanceSettings:
    """Appearance preferences for the application."""

    theme: str = "light"
    font_size: str = "medium"
    window_width: int = 960
    window_height: int = 640
    font_name: str = "Arial"
    font_size_px: int = 11
    background_color: str = "#ffffff"
    text_color: str = "#000000"
    secondary_color: str = "#f0f0f0"


@dataclass
class DefaultPreferences:
    """Default flashcard session settings."""

    flashcard_mode: Mode = Mode.ENDLESS
    difficulty_level: int = 3
    question_count: int = 20
    time_limit: int = 300
    direction: Direction = Direction.ENG_TO_VN


@dataclass
class UserPreferences:
    """User experience preferences."""

    sound_enabled: bool = False
    animation_speed: str = "normal"


@dataclass
class Settings:
    """Aggregate settings container."""

    appearance: AppearanceSettings = field(default_factory=AppearanceSettings)
    defaults: DefaultPreferences = field(default_factory=DefaultPreferences)
    preferences: UserPreferences = field(default_factory=UserPreferences)

    def to_dict(self) -> dict[str, Any]:
        """Convert settings to a JSON-serializable dictionary."""

        return {
            "appearance": self.appearance.__dict__,
            "defaults": {
                "flashcard_mode": self.defaults.flashcard_mode.value,
                "difficulty_level": self.defaults.difficulty_level,
                "question_count": self.defaults.question_count,
                "time_limit": self.defaults.time_limit,
                "direction": self.defaults.direction.value,
            },
            "preferences": self.preferences.__dict__,
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "Settings":
        """Create settings from a dictionary payload."""

        appearance_payload = payload.get("appearance", {})
        defaults_payload = payload.get("defaults", {})
        preferences_payload = payload.get("preferences", {})

        appearance = AppearanceSettings(
            theme=appearance_payload.get("theme", "light"),
            font_size=appearance_payload.get("font_size", "medium"),
            window_width=appearance_payload.get("window_width", 960),
            window_height=appearance_payload.get("window_height", 640),
            font_name=appearance_payload.get("font_name", "Arial"),
            font_size_px=int(appearance_payload.get("font_size_px", 11)),
            background_color=appearance_payload.get(
                "background_color", "#ffffff"),
            text_color=appearance_payload.get("text_color", "#000000"),
            secondary_color=appearance_payload.get(
                "secondary_color", "#f0f0f0"),
        )
        defaults = DefaultPreferences(
            flashcard_mode=Mode(defaults_payload.get(
                "flashcard_mode", Mode.ENDLESS)),
            difficulty_level=int(defaults_payload.get("difficulty_level", 3)),
            question_count=int(defaults_payload.get("question_count", 20)),
            time_limit=int(defaults_payload.get("time_limit", 300)),
            direction=Direction(defaults_payload.get(
                "direction", Direction.ENG_TO_VN)),
        )
        preferences = UserPreferences(
            sound_enabled=bool(
                preferences_payload.get("sound_enabled", False)),
            animation_speed=preferences_payload.get(
                "animation_speed", "normal"),
        )
        return cls(appearance=appearance, defaults=defaults, preferences=preferences)


class SettingsManager:
    """Load and save user settings."""

    def __init__(self, path: Path = SETTINGS_PATH):
        """Initialize settings manager with the target file path."""

        self.path = path
        ensure_data_dirs()
        self._settings = self.load()

    def load(self) -> Settings:
        """Load settings from disk or return defaults."""

        if self.path.exists():
            data = json.loads(self.path.read_text(encoding="utf-8"))
            return Settings.from_dict(data)
        defaults = Settings()
        self.save(defaults)
        return defaults

    def save(self, settings: Settings | None = None) -> None:
        """Persist settings to disk."""

        if settings:
            self._settings = settings
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(
            self._settings.to_dict(), indent=2), encoding="utf-8")

    @property
    def settings(self) -> Settings:
        """Return the current settings instance."""

        return self._settings
