"""Settings view for user preferences."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional

from tak_flashcard.core.settings import Settings, SettingsManager
from tak_flashcard.utils.fonts import get_available_fonts


class SettingsView(ttk.Frame):
    """UI to edit and save user settings."""

    def __init__(self, master: tk.Misc, manager: SettingsManager, on_back: Callable[[], None], on_apply: Optional[Callable[[Settings], None]] = None):
        """Create settings view with settings manager."""

        super().__init__(master, padding=12)
        self.manager = manager
        self.settings: Settings = manager.settings
        self.on_apply = on_apply

        ttk.Label(self, text="Appearance", font=(
            "Arial", 12, "bold")).pack(anchor=tk.W)
        appearance_frame = ttk.Frame(self)

        # Theme selector
        ttk.Label(appearance_frame, text="Theme (light/dark)").pack(anchor=tk.W)
        self.theme_var = tk.StringVar(value=self.settings.appearance.theme)
        ttk.Entry(appearance_frame, textvariable=self.theme_var).pack(fill="x")

        # Font selector
        ttk.Label(appearance_frame, text="Font").pack(anchor=tk.W, pady=(4, 0))
        self.font_var = tk.StringVar(value=self.settings.appearance.font_name)
        available_fonts = get_available_fonts()
        font_combo = ttk.Combobox(
            appearance_frame, textvariable=self.font_var, values=available_fonts, state="readonly")
        font_combo.pack(fill="x")

        # Font size selector (in pixels)
        ttk.Label(appearance_frame, text="Font Size (pixels)").pack(
            anchor=tk.W, pady=(4, 0))
        self.font_size_px_var = tk.IntVar(
            value=self.settings.appearance.font_size_px)
        ttk.Spinbox(appearance_frame, from_=8, to=32,
                    textvariable=self.font_size_px_var).pack(fill="x")

        # Background color
        ttk.Label(appearance_frame, text="Background Color (hex)").pack(
            anchor=tk.W, pady=(4, 0))
        self.bg_color_var = tk.StringVar(
            value=self.settings.appearance.background_color)
        ttk.Entry(appearance_frame,
                  textvariable=self.bg_color_var).pack(fill="x")

        # Text color
        ttk.Label(appearance_frame, text="Text Color (hex)").pack(
            anchor=tk.W, pady=(4, 0))
        self.text_color_var = tk.StringVar(
            value=self.settings.appearance.text_color)
        ttk.Entry(appearance_frame,
                  textvariable=self.text_color_var).pack(fill="x")

        # Secondary color
        ttk.Label(appearance_frame, text="Secondary Color (hex)").pack(
            anchor=tk.W, pady=(4, 0))
        self.secondary_color_var = tk.StringVar(
            value=self.settings.appearance.secondary_color)
        ttk.Entry(appearance_frame,
                  textvariable=self.secondary_color_var).pack(fill="x")

        # Legacy font size selector
        ttk.Label(appearance_frame,
                  text="Font size (small/medium/large)").pack(anchor=tk.W, pady=4)
        self.font_legacy_var = tk.StringVar(
            value=self.settings.appearance.font_size)
        ttk.Entry(appearance_frame,
                  textvariable=self.font_legacy_var).pack(fill="x")
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
        """Persist updated settings to disk and apply immediately."""

        self.settings.appearance.theme = self.theme_var.get() or "light"
        self.settings.appearance.font_name = self.font_var.get() or "Arial"
        self.settings.appearance.font_size_px = int(
            self.font_size_px_var.get() or 11)
        self.settings.appearance.background_color = self.bg_color_var.get() or "#ffffff"
        self.settings.appearance.text_color = self.text_color_var.get() or "#000000"
        self.settings.appearance.secondary_color = self.secondary_color_var.get() or "#f0f0f0"
        self.settings.appearance.font_size = self.font_legacy_var.get() or "medium"
        self.settings.defaults.difficulty_level = int(
            self.difficulty_var.get())
        self.settings.defaults.question_count = int(self.question_var.get())
        self.manager.save(self.settings)
        self.status.set("Saved settings")

        if self.on_apply:
            self.on_apply(self.settings)
