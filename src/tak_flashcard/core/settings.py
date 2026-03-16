"""User settings — storage, loading, and saving.

The app remembers the user's appearance preferences (font, colors, window
size) between sessions by writing them to a JSON file on disk.

On first run the file does not exist, so defaults are used and then saved.
On subsequent runs the file is read and the stored values are applied.

Calling order:
  gui/app.py :: FlashcardApp.__init__()
      → SettingsManager()           — loads settings from disk (or creates defaults)
      → gui/styles.py :: apply_appearance_settings()
                                    — applies them to the Tkinter style engine
  gui/views/settings_view.py
      → SettingsManager.save()      — writes updated settings back to disk
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from tak_flashcard.config import SETTINGS_PATH, ensure_data_dirs

ensure_data_dirs()


@dataclass
class AppearanceSettings:
    """Visual appearance preferences chosen by the user.

    Attributes:
        theme: Named colour theme, e.g. ``"light"`` or ``"dark"``.
        font_size: Named size category (legacy field, kept for compatibility).
        window_width: Preferred window width in pixels.
        window_height: Preferred window height in pixels.
        font_name: Name of the font family to use across the app.
        font_size_px: Font size in pixels (controls all text).
        background_color: Main background colour as a hex string (e.g. ``"#ffffff"``).
        text_color: Primary text colour as a hex string.
        secondary_color: Accent / secondary background colour as a hex string.
    """

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
class UserPreferences:
    """Miscellaneous user experience preferences.

    Attributes:
        sound_enabled: Whether to play sounds on correct/wrong answers.
        animation_speed: Speed of UI transitions (e.g. ``"normal"``, ``"fast"``).
    """

    sound_enabled: bool = False
    animation_speed: str = "normal"


@dataclass
class Settings:
    """Top-level container that groups all user settings together.

    Holds an :class:`AppearanceSettings` and a :class:`UserPreferences`
    instance.  Provides helpers to convert to/from a plain dict for
    JSON serialisation.
    """

    appearance: AppearanceSettings = field(default_factory=AppearanceSettings)
    preferences: UserPreferences = field(default_factory=UserPreferences)

    def to_dict(self) -> dict[str, Any]:
        """Convert settings to a plain dict so they can be saved as JSON.

        Returns:
            A dict with keys ``"appearance"`` and ``"preferences"``, each
            containing the fields of the respective dataclass.
        """

        return {
            "appearance": self.appearance.__dict__,
            "preferences": self.preferences.__dict__,
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "Settings":
        """Reconstruct a :class:`Settings` instance from a loaded JSON dict.

        Missing keys fall back to their defaults, so older settings files
        (that lack newer fields) still work without errors.

        Parameters:
            payload: The raw dict read from ``user_settings.json``.

        Returns:
            A fully populated :class:`Settings` instance.
        """

        appearance_payload = payload.get("appearance", {})
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
        preferences = UserPreferences(
            sound_enabled=bool(
                preferences_payload.get("sound_enabled", False)),
            animation_speed=preferences_payload.get(
                "animation_speed", "normal"),
        )
        return cls(appearance=appearance, preferences=preferences)


class SettingsManager:
    """Loads and saves user settings to/from a JSON file on disk.

    On construction the settings file is read automatically.  If it does
    not exist yet, defaults are used and immediately written to disk.
    The in-memory :class:`Settings` object is then available via the
    :attr:`settings` property for the rest of the app's lifetime.

    Calling order:
        gui/app.py → SettingsManager() → load()
        gui/views/settings_view.py → SettingsManager.save()
    """

    def __init__(self, path: Path = SETTINGS_PATH):
        """Initialise the manager and immediately load (or create) settings.

        Parameters:
            path: Path to the JSON file.  Defaults to the location defined
                in :mod:`config`.
        """

        self.path = path
        ensure_data_dirs()
        self._settings = self.load()

    def load(self) -> Settings:
        """Read settings from the JSON file, or create defaults if missing.

        Returns:
            The loaded or freshly-created :class:`Settings` instance.
        """

        if self.path.exists():
            data = json.loads(self.path.read_text(encoding="utf-8"))
            return Settings.from_dict(data)
        defaults = Settings()
        self.save(defaults)
        return defaults

    def save(self, settings: Settings | None = None) -> None:
        """Write the current settings to the JSON file on disk.

        If ``settings`` is provided it replaces the in-memory copy first.
        Creates the parent directory if it does not exist.

        Parameters:
            settings: New :class:`Settings` to store.  If ``None``, the
                existing in-memory settings are re-saved unchanged.
        """

        if settings:
            self._settings = settings
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(
            self._settings.to_dict(), indent=2), encoding="utf-8")

    @property
    def settings(self) -> Settings:
        """The currently loaded settings instance (read-only shortcut)."""

        return self._settings
