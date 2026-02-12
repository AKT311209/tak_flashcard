"""Settings service managing settings persistence."""

from tak_flashcard.core.settings import SettingsManager


class SettingsService:
    """Service for settings management."""

    def __init__(self):
        """Initialize settings service."""
        self.manager = SettingsManager()

    def get_all_settings(self) -> dict:
        """
        Get all settings.

        Returns:
            Dictionary of all settings
        """
        return self.manager.get_all()

    def get_setting(self, category: str, key: str, default=None):
        """
        Get a specific setting value.

        Args:
            category: Settings category
            key: Setting key
            default: Default value if not found

        Returns:
            Setting value
        """
        return self.manager.get(category, key, default)

    def update_setting(self, category: str, key: str, value) -> bool:
        """
        Update a setting value with validation.

        Args:
            category: Settings category
            key: Setting key
            value: New value

        Returns:
            True if successful, False otherwise
        """
        return self.manager.validate_and_set(category, key, value)

    def save_settings(self) -> bool:
        """
        Save settings to file.

        Returns:
            True if successful, False otherwise
        """
        return self.manager.save_settings()

    def reset_to_defaults(self):
        """Reset all settings to defaults."""
        self.manager.reset_to_defaults()
