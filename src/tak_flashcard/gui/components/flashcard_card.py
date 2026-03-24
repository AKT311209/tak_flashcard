"""Flashcard display component."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Callable

from tak_flashcard.gui.components.neumorphic import NeumorphicRadioButton


class FlashcardCard(ttk.Frame):
    """Widget to display the current flashcard question and collect input."""

    def __init__(
        self,
        master: tk.Misc,
        on_submit: Callable[[str], None],
        on_show_answer: Callable[[], None],
        on_next: Callable[[], None],
        on_end_session: Callable[[], None],
    ):
        """Create card with callbacks for answer submission, reveal, next, and end-session actions.

        Parameters:
            master: Parent Tkinter widget.
            on_submit: Callback for submitted selected answer text.
            on_show_answer: Callback to reveal the answer.
            on_next: Callback to move to the next card.
            on_end_session: Callback to end the active session immediately.
        """

        super().__init__(master, padding=(16, 12), style="Glass.TFrame")
        self._on_submit = on_submit
        self._on_show_answer = on_show_answer
        self._on_next = on_next
        self._on_end_session = on_end_session
        self._awaiting_next = False
        self._show_enabled = True
        self.prompt_var = tk.StringVar(value="Press Start to begin")
        self.choice_var = tk.StringVar(value="")
        self._default_feedback_color = "#334155"

        ttk.Label(
            self,
            textvariable=self.prompt_var,
            style="Section.TLabel",
            wraplength=900,
        ).pack(fill="x", pady=(4, 10))

        self.choice_buttons: list[NeumorphicRadioButton] = []
        self.choices_frame = ttk.Frame(self, style="Glass.TFrame")
        self.choices_frame.pack(fill="x", pady=(0, 8))

        controls_frame = ttk.Frame(self, style="Glass.TFrame")
        controls_frame.pack(fill="x", pady=(8, 4), expand=False)

        buttons_container = ttk.Frame(controls_frame, style="Glass.TFrame")
        buttons_container.pack(anchor="center")

        self.show_button = ttk.Button(
            buttons_container,
            text="Show Answer",
            command=self._handle_show_or_next,
            takefocus=0,
        )
        self.show_button.pack(side=tk.LEFT, padx=(0, 8))

        self.end_session_button = ttk.Button(
            buttons_container,
            text="End Session",
            style="Warning.TButton",
            command=self._on_end_session,
            takefocus=0,
        )
        self.end_session_button.pack(side=tk.LEFT, padx=(12, 0))

        self.feedback = tk.StringVar(value="")
        style = ttk.Style(self)
        feedback_bg = style.lookup(
            "Glass.TFrame", "background") or style.lookup("TFrame", "background")
        self.feedback_label = tk.Label(
            self,
            textvariable=self.feedback,
            fg=self._default_feedback_color,
            bg=feedback_bg,
        )
        self.feedback_label.pack(pady=(4, 0))

    def set_question(self, text: str) -> None:
        """Update the displayed question text and prepare inputs for a new answer."""

        self.reset_after_show()
        self.prompt_var.set(text)

    def set_choices(self, choices: list[str]) -> None:
        """Render multiple-choice options with enhanced neumorphic shadow system.

        Parameters:
            choices: A list of answer options to display.
        """

        for button in self.choice_buttons:
            button.destroy()
        self.choice_buttons = []
        self.choice_var.set("")
        self.choices_frame.columnconfigure(0, weight=1)

        style = ttk.Style(self)
        bg_color = style.lookup("Glass.TFrame", "background") or "#f8f9fa"
        shadow_color = style.lookup(
            "button_shadow", "background") or "#6b7280"
        highlight_color = style.lookup(
            "button_highlight", "background") or "#ffffff"
        text_color = style.lookup("Section.TLabel", "foreground") or "#1a1a2e"
        accent_color = style.lookup(
            "Primary.TButton", "background") or "#0891b2"

        for index, choice in enumerate(choices):
            button = NeumorphicRadioButton(
                self.choices_frame,
                text=choice,
                variable=self.choice_var,
                value=choice,
                command=self._handle_choice_selected,
                bg_color=bg_color,
                shadow_color=shadow_color,
                highlight_color=highlight_color,
                text_color=text_color,
                accent_color=accent_color,
            )
            button.grid(row=index, column=0, sticky="ew", pady=6, padx=2)
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

    # ── keyboard helpers ──────────────────────────────────────────────────────

    @property
    def awaiting_next(self) -> bool:
        """Return whether the card is waiting for the user to advance to the next question."""

        return self._awaiting_next

    def select_choice(self, index: int) -> None:
        """Programmatically select and submit the answer choice at a 1-based index.

        Parameters:
            index: 1-based position of the choice to select (1–4).
        """

        if self._awaiting_next:
            return
        if index < 1 or index > len(self.choice_buttons):
            return
        button = self.choice_buttons[index - 1]
        if str(button.cget("state")) == "disabled":
            return
        button.invoke()

    def trigger_show_or_next(self) -> None:
        """Trigger the Show Answer / Next button if it is currently enabled."""

        if str(self.show_button.cget("state")) == "disabled":
            return
        self._handle_show_or_next()
