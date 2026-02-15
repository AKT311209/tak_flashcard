"""Home view with navigation buttons."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Callable


class HomeView(ttk.Frame):
    """Home screen with navigation shortcuts."""

    def __init__(self, master: tk.Misc, on_nav: Callable[[str], None]):
        """Create the home view with navigation callback."""

        super().__init__(master, padding=16)
        ttk.Label(self, text="Tak Flashcard", font=(
            "Arial", 18, "bold")).pack(pady=10)
        ttk.Label(self, text="Choose an action to begin").pack(pady=4)
        for name, key in [
            ("Flashcard", "flashcard"),
            ("Dictionary", "dictionary"),
            ("Guide", "guide"),
            ("Settings", "settings"),
            ("Exit", "exit"),
        ]:
            ttk.Button(self, text=name, command=lambda k=key: on_nav(
                k), width=24).pack(pady=4)
