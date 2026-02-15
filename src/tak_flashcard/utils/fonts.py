"""Font discovery and management utilities."""

from __future__ import annotations

import tkinter as tk
import tkinter.font as tk_font


def get_available_fonts() -> list[str]:
    """
    Discover all available fonts on the system.

    Returns:
        A sorted list of system font names.
    """
    root = tk.Tk()
    root.withdraw()
    try:
        fonts = sorted(tk_font.families())
    finally:
        root.destroy()
    return fonts
