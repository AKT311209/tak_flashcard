"""Settings controller managing settings view."""

from tak_flashcard.features.settings.service import SettingsService


class SettingsController:
    """Controller for settings functionality."""

    def __init__(self):
        """Initialize settings controller."""
        self.service = SettingsService()
        self.pending_changes = {}

    def load_settings(self) -> dict:
        """
        Load current settings.

        Returns:
            Dictionary of all settings
        """
        return self.service.get_all_settings()

    def get_appearance_settings(self) -> dict:
        """
        Get appearance settings.

        Returns:
            Dictionary of appearance settings
        """
        all_settings = self.service.get_all_settings()
        return all_settings.get('appearance', {})

    def get_default_settings(self) -> dict:
        """
        Get default flashcard settings.

        Returns:
            Dictionary of default settings
        """
        all_settings = self.service.get_all_settings()
        return all_settings.get('defaults', {})

    def get_preferences(self) -> dict:
        """
        Get user preferences.

        Returns:
            Dictionary of preferences
        """
        all_settings = self.service.get_all_settings()
        return all_settings.get('preferences', {})

    def update_setting(self, category: str, key: str, value) -> tuple[bool, str]:
        """
        Update a setting (stores in pending changes).

        Args:
            category: Settings category
            key: Setting key
            value: New value

        Returns:
            Tuple of (success, message)
        """
        if category not in self.pending_changes:
            self.pending_changes[category] = {}

        self.pending_changes[category][key] = value
        return True, "Setting updated (not saved yet)"

    def apply_changes(self) -> tuple[bool, str]:
        """
        Apply and save all pending changes.

        Returns:
            Tuple of (success, message)
        """
        for category, settings in self.pending_changes.items():
            for key, value in settings.items():
                if not self.service.update_setting(category, key, value):
                    return False, f"Invalid value for {category}.{key}"

        if self.service.save_settings():
            self.pending_changes.clear()
            return True, "Settings saved successfully"
        else:
            return False, "Failed to save settings"

    def discard_changes(self):
        """Discard all pending changes."""
        self.pending_changes.clear()

    def reset_to_defaults(self) -> tuple[bool, str]:
        """
        Reset all settings to defaults.

        Returns:
            Tuple of (success, message)
        """
        self.service.reset_to_defaults()
        if self.service.save_settings():
            self.pending_changes.clear()
            return True, "Settings reset to defaults"
        else:
            return False, "Failed to reset settings"
