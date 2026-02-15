"""Flashcard display component."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk


class FlashcardCard(ttk.Frame):
    """Widget to display the current flashcard question and collect input."""

    def __init__(self, master: tk.Misc, on_submit, on_show_answer):
        """Create card with callbacks for submit and show answer."""

        super().__init__(master, padding=12)
        self.prompt_var = tk.StringVar(value="Press Start to begin")
        self.answer_var = tk.StringVar()
        ttk.Label(self, textvariable=self.prompt_var,
                  font=("Arial", 14)).pack(fill="x", pady=8)
        ttk.Entry(self, textvariable=self.answer_var).pack(fill="x", pady=4)
        btn_frame = ttk.Frame(self)
        ttk.Button(btn_frame, text="Submit", command=lambda: on_submit(
            self.answer_var.get())).pack(side=tk.LEFT, padx=4)
        ttk.Button(btn_frame, text="Show Answer",
                   command=on_show_answer).pack(side=tk.LEFT, padx=4)
        btn_frame.pack(pady=6)
        self.feedback = tk.StringVar(value="")
        ttk.Label(self, textvariable=self.feedback, foreground="blue").pack()

    def set_question(self, text: str) -> None:
        """Update the displayed question text and clear answer box."""

        self.prompt_var.set(text)
        self.answer_var.set("")
        self.feedback.set("")

    def set_feedback(self, message: str) -> None:
        """Show feedback text."""

        self.feedback.set(message)
