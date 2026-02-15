"""Flashcard display component."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Callable


class FlashcardCard(ttk.Frame):
    """Widget to display the current flashcard question and collect input."""

    def __init__(
        self,
        master: tk.Misc,
        on_submit: Callable[[str], None],
        on_show_answer: Callable[[], None],
        on_next: Callable[[], None],
    ):
        """Create card with callbacks for answer submission, show answer, and next actions."""

        super().__init__(master, padding=12)
        self._on_submit = on_submit
        self._on_show_answer = on_show_answer
        self._on_next = on_next
        self._awaiting_next = False
        self._show_enabled = True
        self.prompt_var = tk.StringVar(value="Press Start to begin")
        self.choice_var = tk.StringVar(value="")
        self._default_feedback_color = "black"
        ttk.Label(self, textvariable=self.prompt_var,
                  font=("Arial", 14)).pack(fill="x", pady=8)
        self.choice_buttons: list[ttk.Radiobutton] = []
        self.choices_frame = ttk.Frame(self)
        self.choices_frame.pack(fill="x", pady=4)
        self.show_button = ttk.Button(
            self,
            text="Show Answer",
            command=self._handle_show_or_next,
            takefocus=0,
        )
        self.show_button.pack(pady=6)
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
        self.choice_var.set("")

        for index, choice in enumerate(choices):
            button = ttk.Radiobutton(
                self.choices_frame,
                text=choice,
                variable=self.choice_var,
                value=choice,
                command=self._handle_choice_selected,
            )
            button.grid(row=index, column=0, sticky="w", pady=2)
            self.choice_buttons.append(button)

    def set_feedback(self, message: str, color: str | None = None) -> None:
        """Show feedback text with an optional color highlight."""

        self.feedback.set(message)
        if color:
            self.feedback_label.config(fg=color)

    def reset_after_show(self) -> None:
        """Return choice controls to their default state and show button to Show Answer."""

        self._awaiting_next = False
        self.choice_var.set("")
        for button in self.choice_buttons:
            button.config(state="normal")
        self.feedback.set("")
        self.feedback_label.config(fg=self._default_feedback_color)
        self.show_button.config(text="Show Answer")
        self._apply_show_state()

    def prepare_for_next(self) -> None:
        """Prepare the card for the next question after a submit or show-answer event."""

        self._awaiting_next = True
        self.show_button.config(text="Next")
        for button in self.choice_buttons:
            button.config(state="disabled")
        self._apply_show_state()

    def set_show_enabled(self, enabled: bool) -> None:
        """Enable or disable the show-answer control."""

        self._show_enabled = enabled
        self._apply_show_state()

    def disable_all(self) -> None:
        """Disable choice selection and show-answer actions."""

        for button in self.choice_buttons:
            button.config(state="disabled")
        self.set_show_enabled(False)

    def _handle_show_or_next(self) -> None:
        """Route the show-answer button between reveal and next actions."""

        if self._awaiting_next:
            self._on_next()
            return
        self._on_show_answer()

    def _handle_choice_selected(self) -> None:
        """Submit the currently selected choice automatically."""

        if self._awaiting_next:
            return
        selection = self.choice_var.get()
        if not selection.strip():
            return
        self._on_submit(selection)

    def _apply_show_state(self) -> None:
        """Apply the stored show-answer enabled flag while respecting await state."""

        if self._awaiting_next:
            self.show_button.config(state="normal")
            return
        state = "normal" if self._show_enabled else "disabled"
        self.show_button.config(state=state)
