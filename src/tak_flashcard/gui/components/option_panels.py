"""Reusable option panels for flashcard configuration."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from tak_flashcard.constants import DIFFICULTY_LEVELS, Direction, Mode


class FlashcardOptions(ttk.Frame):
    """Options panel for configuring a flashcard session."""

    def __init__(self, master: tk.Misc):
        """Initialize the options panel widgets."""

        super().__init__(master, padding=8)
        self.mode = tk.StringVar(value=Mode.ENDLESS.value)
        self.direction = tk.StringVar(value=Direction.ENG_TO_VN.value)
        self.difficulty = tk.IntVar(value=3)
        self.question_count = tk.IntVar(value=20)
        self.time_limit = tk.IntVar(value=300)

        self._build_widgets()

    def _build_widgets(self) -> None:
        """Construct the option controls."""

        mode_frame = ttk.LabelFrame(self, text="Mode")
        for m in Mode:
            ttk.Radiobutton(mode_frame, text=m.name.title(),
                            variable=self.mode, value=m.value).pack(anchor=tk.W)
        mode_frame.grid(row=0, column=0, sticky="nsew", padx=6, pady=4)

        dir_frame = ttk.LabelFrame(self, text="Direction")
        for d in Direction:
            label = {
                Direction.ENG_TO_VN: "English → Vietnamese",
                Direction.VN_TO_ENG: "Vietnamese → English",
                Direction.MIXED: "Mixed",
            }[d]
            ttk.Radiobutton(
                dir_frame, text=label, variable=self.direction, value=d.value).pack(anchor=tk.W)
        dir_frame.grid(row=0, column=1, sticky="nsew", padx=6, pady=4)

        diff_frame = ttk.LabelFrame(self, text="Difficulty")
        ttk.Scale(diff_frame, from_=min(DIFFICULTY_LEVELS), to=max(DIFFICULTY_LEVELS),
                  variable=self.difficulty, orient=tk.HORIZONTAL).pack(fill="x", padx=6, pady=6)
        ttk.Label(diff_frame, textvariable=self.difficulty).pack()
        diff_frame.grid(row=1, column=0, sticky="nsew", padx=6, pady=4)

        mode_opts = ttk.LabelFrame(self, text="Mode Options")
        ttk.Label(mode_opts, text="Question Count (Testing)").pack(anchor=tk.W)
        ttk.Entry(mode_opts, textvariable=self.question_count).pack(
            fill="x", padx=4, pady=2)
        ttk.Label(mode_opts, text="Time Limit sec (Speed)").pack(anchor=tk.W)
        ttk.Entry(mode_opts, textvariable=self.time_limit).pack(
            fill="x", padx=4, pady=2)
        mode_opts.grid(row=1, column=1, sticky="nsew", padx=6, pady=4)

        for i in range(2):
            self.columnconfigure(i, weight=1)
        for i in range(2):
            self.rowconfigure(i, weight=1)

    def values(self) -> tuple[Mode, Direction, int, int, int]:
        """Return the selected configuration values."""

        return (
            Mode(self.mode.get()),
            Direction(self.direction.get()),
            int(self.difficulty.get()),
            int(self.question_count.get()),
            int(self.time_limit.get()),
        )
