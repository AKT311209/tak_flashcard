"""Styling utilities for theming the application."""

from __future__ import annotations

from tkinter import ttk

from tak_flashcard.core.settings import AppearanceSettings


def apply_appearance_settings(style: ttk.Style, settings: AppearanceSettings) -> None:
    """
    Apply appearance settings to the ttk style.

    Args:
        style: The ttk.Style object to configure.
        settings: The appearance settings to apply.
    """
    # Configure colors for various ttk elements
    style.configure(
        "TFrame",
        background=settings.background_color,
    )
    style.configure(
        "TLabel",
        background=settings.background_color,
        foreground=settings.text_color,
        font=(settings.font_name, settings.font_size_px),
    )
    style.configure(
        "TButton",
        background=settings.secondary_color,
        foreground=settings.text_color,
        font=(settings.font_name, settings.font_size_px),
    )
    style.configure(
        "TEntry",
        fieldbackground=settings.background_color,
        background=settings.secondary_color,
        foreground=settings.text_color,
        font=(settings.font_name, settings.font_size_px),
    )
    style.configure(
        "TScale",
        background=settings.background_color,
        foreground=settings.text_color,
    )
    style.configure(
        "TCombobox",
        fieldbackground=settings.background_color,
        background=settings.secondary_color,
        foreground=settings.text_color,
    )
