"""Results view placeholder."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Callable


class ResultsView(ttk.Frame):
    """Show summary of a completed session."""

    def __init__(self, master: tk.Misc, summary: str, on_back: Callable[[], None]):
        """Create results view with provided summary text."""

        super().__init__(master, padding=12)
        ttk.Label(self, text="Results", font=(
            "Arial", 16, "bold")).pack(pady=8)
        text = tk.Text(self, wrap="word", height=12)
        text.insert("1.0", summary)
        text.configure(state="disabled")
        text.pack(fill="both", expand=True)
        ttk.Button(self, text="Back", command=on_back).pack(pady=6)
