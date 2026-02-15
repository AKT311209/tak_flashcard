"""Flashcard display component."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Callable


class FlashcardCard(ttk.Frame):
    """Widget to display the current flashcard question and collect input."""

    def __init__(self, master: tk.Misc, on_submit: Callable[[str], None], on_show_answer: Callable[[], None], on_next: Callable[[], None]):
        """Create card with callbacks for submit, show answer, and next actions."""

        super().__init__(master, padding=12)
        self._on_submit = on_submit
        self._on_show_answer = on_show_answer
        self._on_next = on_next
        self._awaiting_next = False
        self.prompt_var = tk.StringVar(value="Press Start to begin")
        self.choice_var = tk.StringVar(value="")
        self._default_feedback_color = "black"
        ttk.Label(self, textvariable=self.prompt_var,
                  font=("Arial", 14)).pack(fill="x", pady=8)
        self.choice_buttons: list[ttk.Radiobutton] = []
        self.choices_frame = ttk.Frame(self)
        self.choices_frame.pack(fill="x", pady=4)
        btn_frame = ttk.Frame(self)
        self.submit_button = ttk.Button(
            btn_frame, text="Submit", command=self._handle_submit_or_next)
        self.submit_button.pack(side=tk.LEFT, padx=4)
        self.show_button = ttk.Button(btn_frame, text="Show Answer",
                                      command=self._handle_show_answer)
        self.show_button.pack(side=tk.LEFT, padx=4)
        btn_frame.pack(pady=6)
        self.feedback = tk.StringVar(value="")
        self.feedback_label = tk.Label(self, textvariable=self.feedback,
                                       fg=self._default_feedback_color)
        self.feedback_label.pack()

    def set_question(self, text: str) -> None:
        """Update the displayed question text and prepare inputs for a new answer."""

        self.reset_after_show()
        self.prompt_var.set(text)

    def set_choices(self, choices: list[str]) -> None:
        """Render multiple-choice options for the current question.

        Parameters:
            choices: A list of answer options to display.
        """

        for button in self.choice_buttons:
            button.destroy()
        self.choice_buttons = []
        self.choice_var.set(choices[0] if len(choices) == 1 else "")

        for index, choice in enumerate(choices):
            button = ttk.Radiobutton(
                self.choices_frame,
                text=choice,
                variable=self.choice_var,
                value=choice,
            )
            button.grid(row=index, column=0, sticky="w", pady=2)
            self.choice_buttons.append(button)

    def set_feedback(self, message: str, color: str | None = None) -> None:
        """Show feedback text with an optional color highlight."""

        self.feedback.set(message)
        if color:
            self.feedback_label.config(fg=color)

    def reset_after_show(self) -> None:
        """Return submit and choice controls to their default state."""

        self._awaiting_next = False
        self.submit_button.config(text="Submit")
        self.submit_button.config(state="normal")
        self.choice_var.set("")
        for button in self.choice_buttons:
            button.config(state="normal")
        self.feedback.set("")
        self.feedback_label.config(fg=self._default_feedback_color)

    def prepare_for_next(self) -> None:
        """Prepare the card for the next question after a submit or show-answer event."""

        self._awaiting_next = True
        self.submit_button.config(text="Next")
        for button in self.choice_buttons:
            button.config(state="disabled")

    def set_show_enabled(self, enabled: bool) -> None:
        """Enable or disable the show-answer control."""

        state = "normal" if enabled else "disabled"
        self.show_button.config(state=state)

    def disable_all(self) -> None:
        """Disable submit, choice selection, and show-answer actions."""

        self.submit_button.config(state="disabled")
        for button in self.choice_buttons:
            button.config(state="disabled")
        self.set_show_enabled(False)

    def _handle_submit_or_next(self) -> None:
        """Route the submit button action based on the current interaction state."""

        if self._awaiting_next:
            self._on_next()
            return
        self._on_submit(self.choice_var.get())

    def _handle_show_answer(self) -> None:
        """Invoke the parent-provided show-answer callback."""

        self._on_show_answer()
