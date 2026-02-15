"""Flashcard view implementation."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Callable

from tak_flashcard.constants import Direction, Mode
from tak_flashcard.gui.components.flashcard_card import FlashcardCard
from tak_flashcard.gui.components.option_panels import FlashcardOptions
from tak_flashcard.features.flashcard.controller import FlashcardController


class FlashcardView(ttk.Frame):
    """View for configuring and running flashcard sessions."""

    def __init__(self, master: tk.Misc, controller: FlashcardController, on_back: Callable[[], None]):
        """Initialize the flashcard view with controller and navigation."""

        super().__init__(master, padding=10)
        self.controller = controller
        self.on_back = on_back
        self.options = FlashcardOptions(self)
        self.options.pack(fill="x", pady=6)

        self.card = FlashcardCard(self, self.submit_answer, self.show_answer)
        self.card.pack(fill="both", expand=True, pady=6)

        controls = ttk.Frame(self)
        ttk.Button(controls, text="Start Session",
                   command=self.start_session).pack(side=tk.LEFT, padx=4)
        ttk.Button(controls, text="Back", command=self.on_back).pack(
            side=tk.LEFT, padx=4)
        controls.pack(pady=6)

        self.status_var = tk.StringVar(value="Not started")
        ttk.Label(self, textvariable=self.status_var).pack(anchor=tk.W)

    def start_session(self) -> None:
        """Start a new flashcard session using current options."""

        mode, direction, difficulty, question_count, time_limit = self.options.values()
        q_limit = question_count if mode == Mode.TESTING else None
        t_limit = time_limit if mode == Mode.SPEED else None
        self.controller.start(mode, direction, difficulty, q_limit, t_limit)
        self.next_card()
        self.status_var.set(
            f"Mode: {mode.name.title()} | Direction: {direction.name} | Score: 0")

    def next_card(self) -> None:
        """Fetch and display the next card."""

        card = self.controller.next_card()
        if card is None:
            self.card.set_question("Session finished or no cards available")
            return
        state = self.controller.service.state
        direction = state.current_direction if state and state.current_direction else (
            state.direction if state else Direction.ENG_TO_VN)
        prompt = card.english if direction == Direction.ENG_TO_VN else card.vietnamese
        self.card.set_question(prompt)

    def submit_answer(self, answer: str) -> None:
        """Submit answer and update feedback."""

        result = self.controller.submit(answer)
        if result is None:
            return
        if result.is_correct:
            self.card.set_feedback(f"Correct! (+{result.delta})")
        else:
            self.card.set_feedback(
                f"Incorrect. Correct answer: {result.correct_answer} ({result.delta})")
        self.status_var.set(f"Score: {result.new_score}")
        self.next_card()

    def show_answer(self) -> None:
        """Reveal answer and apply penalty."""

        state = self.controller.service.state
        if state is None or state.current_word is None:
            return
        direction = state.current_direction or state.direction
        answer = state.current_word.vietnamese if direction == Direction.ENG_TO_VN else state.current_word.english
        self.card.set_feedback(f"Answer: {answer} (-10)")
        self.controller.reveal()
        self.status_var.set(f"Score: {state.score}")
