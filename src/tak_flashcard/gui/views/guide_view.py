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

        super().__init__(master, padding=20, style="Page.TFrame")

        header = ttk.Frame(self, padding=16, style="Glass.TFrame")
        header.pack(fill="x", pady=(0, 12))
        ttk.Label(header, text="Guide", style="Title.TLabel").pack(anchor=tk.W)
        ttk.Label(
            header,
            text="Everything you need for modes, scoring, and smart practice flow.",
            style="Subtitle.TLabel",
        ).pack(anchor=tk.W, pady=(4, 0))

        content = ttk.Frame(self, padding=12, style="Glass.TFrame")
        content.pack(fill="both", expand=True)

        text = tk.Text(
            content,
            wrap="word",
            height=20,
            bg="#f8fdff",
            fg="#164e63",
            relief=tk.FLAT,
            bd=0,
            padx=12,
            pady=12,
        )
        text.insert("1.0", GUIDE_TEXT)
        text.configure(state="disabled")
        text.pack(fill="both", expand=True)

        controls = ttk.Frame(self, style="Page.TFrame")
        controls.pack(fill="x", pady=(10, 0))
        ttk.Button(controls, text="Back", command=on_back).pack(anchor=tk.W)
