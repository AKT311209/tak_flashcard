"""Tkinter application entry point."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from tak_flashcard.config import APP_NAME, WINDOW_HEIGHT, WINDOW_WIDTH, ensure_data_dirs
from tak_flashcard.core.settings import Settings, SettingsManager
from tak_flashcard.data.seed.importer import ensure_seed_data
from tak_flashcard.db.session import SessionLocal, init_db
from tak_flashcard.features.dictionary.service import DictionaryService
from tak_flashcard.features.flashcard.controller import FlashcardController
from tak_flashcard.gui.styles import apply_appearance_settings
from tak_flashcard.gui.views.dictionary_view import DictionaryView
from tak_flashcard.gui.views.flashcard_view import FlashcardView
from tak_flashcard.gui.views.guide_view import GuideView
from tak_flashcard.gui.views.home_view import HomeView
from tak_flashcard.gui.views.settings_view import SettingsView


class FlashcardApp(tk.Tk):
    """Main Tkinter application container."""

    def __init__(self):
        """Initialize the application window and views."""

        super().__init__()
        ensure_data_dirs()
        self.title(APP_NAME)
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.style = ttk.Style(self)
        self.style.theme_use("clam")

        init_db()
        self.db = SessionLocal()
        ensure_seed_data(self.db)
        self.settings_manager = SettingsManager()

        apply_appearance_settings(
            self.style, self.settings_manager.settings.appearance)

        self.controller = FlashcardController(self.db)
        self.dictionary_service = DictionaryService(self.db)

        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)
        self.frames = {}

        self.frames["home"] = HomeView(container, self.navigate)
        self.frames["flashcard"] = FlashcardView(
            container, self.controller, lambda: self.navigate("home"))
        self.frames["dictionary"] = DictionaryView(
            container, self.dictionary_service, lambda: self.navigate("home"))
        self.frames["guide"] = GuideView(
            container, lambda: self.navigate("home"))
        self.frames["settings"] = SettingsView(
            container, self.settings_manager, lambda: self.navigate("home"), self.apply_appearance)

        for frame in self.frames.values():
            frame.grid(row=0, column=0, sticky="nsew")

        self.navigate("home")

    def apply_appearance(self, settings: Settings) -> None:
        """Apply appearance settings to the application immediately."""
        apply_appearance_settings(self.style, settings.appearance)

    def navigate(self, key: str) -> None:
        """Show the requested frame or exit."""

        if key == "exit":
            self.destroy()
            return
        frame = self.frames.get(key)
        if frame:
            if key == "dictionary" and isinstance(frame, DictionaryView):
                frame.refresh()
            frame.tkraise()


def run() -> None:
    """Start the Tkinter main loop."""

    app = FlashcardApp()
    app.mainloop()


if __name__ == "__main__":
    run()
