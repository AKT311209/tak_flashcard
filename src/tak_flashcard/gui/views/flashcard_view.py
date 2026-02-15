"""Flashcard configuration view implementation."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional

from tak_flashcard.constants import Direction, Mode
from tak_flashcard.features.flashcard.controller import FlashcardController
from tak_flashcard.gui.components.flashcard_card import FlashcardCard
from tak_flashcard.gui.components.option_panels import FlashcardOptions


class FlashcardView(ttk.Frame):
    """View for configuring flashcard sessions before starting."""

    def __init__(
        self,
        master: tk.Misc,
        on_start_session: Callable[[Mode, Direction, int, int, int], None],
        on_back: Callable[[], None],
    ):
        """Initialize the flashcard settings view and navigation callbacks.

        Parameters:
            master: Parent Tkinter widget.
            on_start_session: Callback invoked with selected session options.
            on_back: Callback used to return to home.
        """

        super().__init__(master, padding=10)
        self.on_start_session = on_start_session
        self.on_back = on_back
        self.options = FlashcardOptions(self)
        self.options.pack(fill="x", pady=6)

        info = ttk.LabelFrame(self, text="Session Setup", padding=8)
        ttk.Label(
            info,
            text="Adjust settings above, then click START SESSION to open the session screen.",
        ).pack(anchor=tk.W)
        info.pack(fill="x", pady=6)

        controls = ttk.Frame(self)
        ttk.Button(controls, text="Start Session", command=self.start_session).pack(
            side=tk.LEFT, padx=4
        )
        ttk.Button(controls, text="Back", command=self.on_back).pack(
            side=tk.LEFT, padx=4)
        controls.pack(pady=6)

        self.status_var = tk.StringVar(value="Ready to start")
        ttk.Label(self, textvariable=self.status_var).pack(anchor=tk.W)

    def start_session(self) -> None:
        """Start a new flashcard session using current options."""

        mode, direction, difficulty, question_count, time_limit = self.options.values()
        self.status_var.set(
            f"Starting {mode.name.title()} | {direction.name} | Difficulty {difficulty}"
        )
        self.on_start_session(mode, direction, difficulty,
                              question_count, time_limit)


class FlashcardSessionView(ttk.Frame):
    """View for running an active flashcard session."""

    def __init__(
        self,
        master: tk.Misc,
        controller: FlashcardController,
        on_back_to_settings: Callable[[], None],
    ):
        """Initialize session widgets and callbacks.

        Parameters:
            master: Parent Tkinter widget.
            controller: Flashcard session controller.
            on_back_to_settings: Callback used to return to settings view.
        """

        super().__init__(master, padding=10)
        self.controller = controller
        self.on_back_to_settings = on_back_to_settings

        self.card = FlashcardCard(self, self.submit_answer, self.show_answer)
        self.card.pack(fill="both", expand=True, pady=6)

        controls = ttk.Frame(self)
        ttk.Button(controls, text="Back to Settings", command=self.on_back_to_settings).pack(
            side=tk.LEFT, padx=4
        )
        controls.pack(pady=6)

        self.status_var = tk.StringVar(value="Session not started")
        ttk.Label(self, textvariable=self.status_var).pack(anchor=tk.W)

    def begin_session(
        self,
        mode: Mode,
        direction: Direction,
        difficulty: int,
        question_count: int,
        time_limit: int,
    ) -> None:
        """Start a new session and render the first card.

        Parameters:
            mode: Selected study mode.
            direction: Selected translation direction.
            difficulty: Selected difficulty from 1-5.
            question_count: User-entered question count for testing mode.
            time_limit: User-entered time limit for speed mode.
        """

        q_limit: Optional[int] = question_count if mode == Mode.TESTING else None
        t_limit: Optional[int] = time_limit if mode == Mode.SPEED else None
        self.controller.start(mode, direction, difficulty, q_limit, t_limit)
        self.status_var.set(
            f"Mode: {mode.name.title()} | Direction: {direction.name} | Score: 0"
        )
        self.next_card()

    def next_card(self) -> None:
        """Fetch and display the next card for the current session."""

        card = self.controller.next_card()
        if card is None:
            self.card.set_question("Session finished or no cards available")
            return
        state = self.controller.service.state
        direction = (
            state.current_direction
            if state and state.current_direction
            else (state.direction if state else Direction.ENG_TO_VN)
        )
        prompt = str(card.english) if direction == Direction.ENG_TO_VN else str(
            card.vietnamese)
        self.card.set_question(prompt)

    def submit_answer(self, answer: str) -> None:
        """Submit answer and update feedback panel.

        Parameters:
            answer: Raw answer entered by the user.
        """

        result = self.controller.submit(answer)
        if result is None:
            return
        if result.is_correct:
            self.card.set_feedback(f"Correct! (+{result.delta})")
        else:
            self.card.set_feedback(
                f"Incorrect. Correct answer: {str(result.correct_answer)} ({result.delta})"
            )
        self.status_var.set(f"Score: {result.new_score}")
        self.next_card()

    def show_answer(self) -> None:
        """Reveal the current answer and apply configured penalty."""

        state = self.controller.service.state
        if state is None or state.current_word is None:
            return
        direction = state.current_direction or state.direction
        answer = (
            str(state.current_word.vietnamese)
            if direction == Direction.ENG_TO_VN
            else str(state.current_word.english)
        )
        self.card.set_feedback(f"Answer: {answer} (-10)")
        self.controller.reveal()
        self.status_var.set(f"Score: {state.score}")
