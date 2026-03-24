"""Home view with navigation buttons."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Callable


class HomeView(ttk.Frame):
    """Home screen with navigation shortcuts."""

    def __init__(self, master: tk.Misc, on_nav: Callable[[str], None]):
        """Create the home view with navigation callback."""

        super().__init__(master, padding=0, style="Page.TFrame")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)

        inner_frame = ttk.Frame(self, style="Page.TFrame")
        inner_frame.grid(row=0, column=0, sticky="ew", padx=40, pady=(40, 20))

        hero = ttk.Frame(inner_frame, padding=24, style="Glass.TFrame")
        hero.pack(fill="x", pady=(0, 32))

        ttk.Label(hero, text="Tak Flashcard",
                  style="Title.TLabel").pack(anchor=tk.W, pady=(0, 8))
        ttk.Label(
            hero,
            text="A sleek study workspace for flashcards, dictionary lookup, and guided learning.",
            style="Subtitle.TLabel",
            wraplength=600,
        ).pack(anchor=tk.W, pady=(0, 0))

        grid = ttk.Frame(inner_frame, style="Page.TFrame")
        grid.pack(fill="both", expand=False)

        actions: list[tuple[str, str, str]] = [
            ("Start Flashcards", "flashcard",
             "Launch a practice session with your selected mode."),
            ("Open Dictionary", "dictionary",
             "Search and sort your full vocabulary list."),
            ("Read Guide", "guide", "Review mode rules, scoring, and learning tips."),
            ("Import Vocabulary", "import",
             "Load a CSV and refresh your learning dataset."),
            ("Personalize Settings", "settings",
             "Tune font and color preferences instantly."),
            ("Exit App", "exit", "Close Tak Flashcard safely."),
        ]

        for index, (label, key, description) in enumerate(actions):
            row = index // 2
            col = index % 2
            card = ttk.Frame(grid, padding=20, style="Glass.TFrame")
            card.grid(row=row, column=col, sticky="ewns", padx=12, pady=12)

            ttk.Label(card, text=label, style="Section.TLabel").pack(
                anchor=tk.W, pady=(0, 8))
            ttk.Label(card, text=description, style="Muted.TLabel", wraplength=320).pack(
                anchor=tk.W, pady=(0, 14)
            )

            spacer = ttk.Frame(card)
            spacer.pack(fill="both", expand=True)

            btn_style = "Primary.TButton" if key == "flashcard" else "Glass.TButton"
            ttk.Button(
                card,
                text=label,
                style=btn_style,
                command=lambda k=key: on_nav(k),
            ).pack(anchor=tk.W, pady=(4, 0))

        grid.columnconfigure(0, weight=1, minsize=365)
        grid.columnconfigure(1, weight=1, minsize=365)
        grid.rowconfigure(0, weight=1)
        grid.rowconfigure(1, weight=1)
        grid.rowconfigure(2, weight=1)
