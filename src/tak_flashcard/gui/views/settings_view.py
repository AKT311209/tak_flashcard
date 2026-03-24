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

        super().__init__(master, padding=20, style="Page.TFrame")
        self.manager = manager
        self.settings: Settings = manager.settings
        self.on_apply = on_apply

        header = ttk.Frame(self, padding=16, style="Glass.TFrame")
        header.pack(fill="x", pady=(0, 12))
        ttk.Label(header, text="Settings",
                  style="Title.TLabel").pack(anchor=tk.W)
        ttk.Label(
            header,
            text="Tune typography and palette preferences for your ideal learning environment.",
            style="Subtitle.TLabel",
        ).pack(anchor=tk.W, pady=(4, 0))

        appearance_frame = ttk.LabelFrame(
            self, text="Appearance", padding=12, style="Glass.TLabelframe")
        appearance_frame.pack(fill="x", pady=(0, 10))

        # Font selector
        ttk.Label(appearance_frame, text="Font", style="Section.TLabel").pack(
            anchor=tk.W, pady=(4, 0))
        self.font_var = tk.StringVar(value=self.settings.appearance.font_name)
        available_fonts = get_available_fonts()
        font_combo = ttk.Combobox(
            appearance_frame, textvariable=self.font_var, values=available_fonts, state="readonly")
        font_combo.pack(fill="x")

        # Font size selector (in pixels)
        ttk.Label(appearance_frame, text="Font Size (pixels)", style="Section.TLabel").pack(
            anchor=tk.W, pady=(4, 0))
        self.font_size_px_var = tk.IntVar(
            value=self.settings.appearance.font_size_px)
        ttk.Spinbox(appearance_frame, from_=8, to=32,
                    textvariable=self.font_size_px_var).pack(fill="x")

        # Background color
        ttk.Label(appearance_frame, text="Background Color (hex)", style="Section.TLabel").pack(
            anchor=tk.W, pady=(4, 0))
        self.bg_color_var = tk.StringVar(
            value=self.settings.appearance.background_color)
        ttk.Entry(appearance_frame,
                  textvariable=self.bg_color_var).pack(fill="x")

        # Text color
        ttk.Label(appearance_frame, text="Text Color (hex)", style="Section.TLabel").pack(
            anchor=tk.W, pady=(4, 0))
        self.text_color_var = tk.StringVar(
            value=self.settings.appearance.text_color)
        ttk.Entry(appearance_frame,
                  textvariable=self.text_color_var).pack(fill="x")

        # Secondary color
        ttk.Label(appearance_frame, text="Secondary Color (hex)", style="Section.TLabel").pack(
            anchor=tk.W, pady=(4, 0))
        self.secondary_color_var = tk.StringVar(
            value=self.settings.appearance.secondary_color)
        ttk.Entry(appearance_frame,
                  textvariable=self.secondary_color_var).pack(fill="x")

        tip_frame = ttk.Frame(self, padding=12, style="Glass.TFrame")
        tip_frame.pack(fill="x", pady=(0, 10))
        ttk.Label(
            tip_frame,
            text="Tip: use high-contrast colors for readability (target at least 4.5:1).",
            style="Muted.TLabel",
        ).pack(anchor=tk.W)

        btn_frame = ttk.Frame(self, style="Page.TFrame")
        ttk.Button(btn_frame, text="Save", style="Primary.TButton", command=self.save).pack(
            side=tk.LEFT, padx=4)
        ttk.Button(btn_frame, text="Back", command=on_back).pack(
            side=tk.LEFT, padx=4)
        btn_frame.pack(pady=8)

        self.status = tk.StringVar(value="")
        status_row = ttk.Frame(self, padding=10, style="Glass.TFrame")
        status_row.pack(fill="x")
        ttk.Label(status_row, textvariable=self.status,
                  style="Status.TLabel").pack(anchor=tk.W)

    def save(self) -> None:
        """Persist updated settings to disk and apply immediately."""

        self.settings.appearance.font_name = self.font_var.get() or "Arial"
        self.settings.appearance.font_size_px = int(
            self.font_size_px_var.get() or 11)
        self.settings.appearance.background_color = self.bg_color_var.get() or "#ffffff"
        self.settings.appearance.text_color = self.text_color_var.get() or "#000000"
        self.settings.appearance.secondary_color = self.secondary_color_var.get() or "#f0f0f0"
        self.manager.save(self.settings)
        self.status.set("Saved settings")

        if self.on_apply:
            self.on_apply(self.settings)
