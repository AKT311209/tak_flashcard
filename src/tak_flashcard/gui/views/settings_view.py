"""Settings view for user preferences."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Callable

from tak_flashcard.core.settings import Settings, SettingsManager


class SettingsView(ttk.Frame):
    """UI to edit and save user settings."""

    def __init__(self, master: tk.Misc, manager: SettingsManager, on_back: Callable[[], None]):
        """Create settings view with settings manager."""

        super().__init__(master, padding=12)
        self.manager = manager
        self.settings: Settings = manager.settings

        ttk.Label(self, text="Appearance", font=(
            "Arial", 12, "bold")).pack(anchor=tk.W)
        appearance_frame = ttk.Frame(self)
        ttk.Label(appearance_frame, text="Theme (light/dark)").pack(anchor=tk.W)
        self.theme_var = tk.StringVar(value=self.settings.appearance.theme)
        ttk.Entry(appearance_frame, textvariable=self.theme_var).pack(fill="x")
        ttk.Label(appearance_frame,
                  text="Font size (small/medium/large)").pack(anchor=tk.W, pady=4)
        self.font_var = tk.StringVar(value=self.settings.appearance.font_size)
        ttk.Entry(appearance_frame, textvariable=self.font_var).pack(fill="x")
        appearance_frame.pack(fill="x", pady=6)

        ttk.Label(self, text="Defaults", font=(
            "Arial", 12, "bold")).pack(anchor=tk.W)
        defaults_frame = ttk.Frame(self)
        self.difficulty_var = tk.IntVar(
            value=self.settings.defaults.difficulty_level)
        ttk.Label(defaults_frame, text="Default difficulty 1-5").pack(anchor=tk.W)
        ttk.Scale(defaults_frame, from_=1, to=5,
                  variable=self.difficulty_var, orient=tk.HORIZONTAL).pack(fill="x")
        self.question_var = tk.IntVar(
            value=self.settings.defaults.question_count)
        ttk.Label(defaults_frame, text="Default question count").pack(
            anchor=tk.W, pady=4)
        ttk.Entry(defaults_frame, textvariable=self.question_var).pack(fill="x")
        defaults_frame.pack(fill="x", pady=6)

        btn_frame = ttk.Frame(self)
        ttk.Button(btn_frame, text="Save", command=self.save).pack(
            side=tk.LEFT, padx=4)
        ttk.Button(btn_frame, text="Back", command=on_back).pack(
            side=tk.LEFT, padx=4)
        btn_frame.pack(pady=8)

        self.status = tk.StringVar(value="")
        ttk.Label(self, textvariable=self.status,
                  foreground="green").pack(anchor=tk.W)

    def save(self) -> None:
        """Persist updated settings to disk."""

        self.settings.appearance.theme = self.theme_var.get() or "light"
        self.settings.appearance.font_size = self.font_var.get() or "medium"
        self.settings.defaults.difficulty_level = int(
            self.difficulty_var.get())
        self.settings.defaults.question_count = int(self.question_var.get())
        self.manager.save(self.settings)
        self.status.set("Saved settings")
