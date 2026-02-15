"""Guide view showing static instructions."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Callable

from tak_flashcard.features.guide.content import GUIDE_TEXT


class GuideView(ttk.Frame):
    """Display guide content."""

    def __init__(self, master: tk.Misc, on_back: Callable[[], None]):
        """Create guide view with back navigation."""

        super().__init__(master, padding=12)
        ttk.Label(self, text="Guide", font=("Arial", 16, "bold")).pack(pady=8)
        text = tk.Text(self, wrap="word", height=20)
        text.insert("1.0", GUIDE_TEXT)
        text.configure(state="disabled")
        text.pack(fill="both", expand=True)
        ttk.Button(self, text="Back", command=on_back).pack(pady=6)
