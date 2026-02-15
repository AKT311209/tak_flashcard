"""Reusable toolbar component."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Callable


class Toolbar(ttk.Frame):
    """Simple toolbar with navigation buttons."""

    def __init__(self, master: tk.Misc, on_home: Callable[[], None], on_back: Callable[[], None]):
        """Create toolbar with provided callbacks."""

        super().__init__(master, padding=(8, 4))
        ttk.Button(self, text="Home", command=on_home).pack(
            side=tk.LEFT, padx=4)
        ttk.Button(self, text="Back", command=on_back).pack(
            side=tk.LEFT, padx=4)
