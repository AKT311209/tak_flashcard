"""Flashcard configuration view implementation."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional

from tak_flashcard.constants import Direction, Mode
from tak_flashcard.core.scheduler import CountdownTimer
from tak_flashcard.core.settings import DefaultPreferences
from tak_flashcard.features.flashcard.controller import FlashcardController
from tak_flashcard.features.flashcard.states import ShowAnswerConfig, ShowAnswerOutcome
from tak_flashcard.gui.components.flashcard_card import FlashcardCard
from tak_flashcard.gui.components.option_panels import FlashcardOptions


class FlashcardView(ttk.Frame):
    """View for configuring flashcard sessions before starting."""

    def __init__(
        self,
        master: tk.Misc,
        on_start_session: Callable[
            [Mode, Direction, int, int, int, ShowAnswerConfig, int], None
        ],
        defaults: DefaultPreferences,
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
        self.options = FlashcardOptions(
            self,
            default_question_count=defaults.question_count,
            default_time_limit=defaults.time_limit,
        )
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

        (
            mode,
            direction,
            difficulty,
            question_count,
            time_limit,
            score_penalty,
            show_limit,
            time_penalty,
            wrong_answer_penalty,
        ) = self.options.values()
        self.status_var.set(
            f"Starting {mode.name.title()} | {direction.name} | Difficulty {difficulty}"
        )
        show_config = ShowAnswerConfig(
            enabled=mode != Mode.TESTING,
            score_penalty=max(score_penalty, 0),
            time_penalty=time_penalty if mode == Mode.SPEED else 0,
        )
        if mode == Mode.TESTING:
            show_config.max_uses = 0
        elif show_limit > 0:
            show_config.max_uses = show_limit
        wrong_penalty = (
            wrong_answer_penalty
            if mode in (Mode.ENDLESS, Mode.SPEED)
            else 0
        )
        self.on_start_session(
            mode,
            direction,
            difficulty,
            question_count,
            time_limit,
            show_config,
            wrong_penalty,
        )


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
        self.timer_var = tk.StringVar(value="")
        self.timer_label = ttk.Label(self, textvariable=self.timer_var,
                                     font=("Arial", 11, "bold"))
        self.timer: CountdownTimer | None = None
        self._timer_after_id: Optional[str] = None

        self.card = FlashcardCard(self, self.submit_answer,
                                  self.show_answer, self.next_card)
        self.card.pack(fill="both", expand=True, pady=6)

        controls = ttk.Frame(self)
        ttk.Button(
            controls,
            text="Back to Settings",
            command=self._handle_back_to_settings,
        ).pack(side=tk.LEFT, padx=4)
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
        show_config: ShowAnswerConfig,
        wrong_penalty: int,
    ) -> None:
        """Start a new session and render the first card.

        Parameters:
            mode: Selected study mode.
            direction: Selected translation direction.
            difficulty: Selected difficulty from 1-5.
            question_count: User-entered question count for testing mode.
            time_limit: User-entered time limit for speed mode.
            show_config: Settings for show-answer penalties.
            wrong_penalty: Configured score deduction for incorrect answers.
        """

        self._stop_timer()
        q_limit: Optional[int] = question_count if mode == Mode.TESTING else None
        t_limit: Optional[int] = time_limit if mode == Mode.SPEED else None
        self.controller.start(
            mode,
            direction,
            difficulty,
            show_config,
            q_limit,
            t_limit,
            wrong_penalty,
        )
        self.status_var.set(
            f"Mode: {mode.name.title()} | Direction: {direction.name} | Score: 0"
        )
        if mode == Mode.SPEED and t_limit is not None:
            self._start_timer(t_limit)
        else:
            self._hide_timer_label()
        self.next_card()

    def next_card(self) -> None:
        """Fetch and display the next card for the current session."""

        card = self.controller.next_card()
        if card is None:
            self.card.set_question("Session finished or no cards available")
            self.card.set_choices([])
            self.card.disable_all()
            self.card.set_show_enabled(False)
            self._stop_timer()
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
        self.card.set_choices(state.current_choices if state else [])
        self._update_show_button_state()

    def submit_answer(self, answer: str) -> None:
        """Submit answer and update feedback panel.

        Parameters:
            answer: Selected answer option.
        """

        if not answer.strip():
            self.card.set_feedback(
                "Please select one option before submitting.")
            return
        result = self.controller.submit(answer)
        if result is None:
            return
        if result.is_correct:
            feedback = f"Correct! ({result.delta:+d})"
            color = "green"
        else:
            feedback = (
                f"Incorrect. Correct answer: {str(result.correct_answer)} ({result.delta:+d})"
            )
            color = "red"
        self.card.set_feedback(feedback, color=color)
        self.card.prepare_for_next()
        self.card.set_show_enabled(False)
        self.status_var.set(f"Score: {result.new_score}")

    def show_answer(self) -> None:
        """Reveal the current answer and apply configured penalty."""

        state = self.controller.service.state
        if state is None or state.current_word is None:
            return
        direction = state.current_direction or state.direction
        prompt = (
            str(state.current_word.english)
            if direction == Direction.ENG_TO_VN
            else str(state.current_word.vietnamese)
        )
        answer = (
            str(state.current_word.vietnamese)
            if direction == Direction.ENG_TO_VN
            else str(state.current_word.english)
        )
        outcome: ShowAnswerOutcome = self.controller.reveal()
        if not outcome.allowed:
            message = "Show answer unavailable"
            if state.show_config.max_uses is not None:
                message = "Show limit reached"
            self.card.set_feedback(message)
            self._update_show_button_state()
            return
        details: list[str] = []
        if outcome.score_delta:
            details.append(f"{outcome.score_delta} pts")
        if outcome.time_penalty:
            details.append(f"-{outcome.time_penalty}s")
        info = f" ({', '.join(details)})" if details else ""
        self.card.set_feedback(
            f"Question: {prompt} | Answer: {answer}{info}", color="orange"
        )
        if outcome.time_penalty:
            self._apply_time_penalty(outcome.time_penalty)
        self.status_var.set(f"Score: {state.score}")
        self.card.prepare_for_next()
        self._update_show_button_state()

    def _handle_back_to_settings(self) -> None:
        """Stop the timer and return to the settings view."""

        self._stop_timer()
        self.on_back_to_settings()

    def _update_show_button_state(self) -> None:
        """Enable or disable the show-answer button based on the state."""

        self.card.set_show_enabled(self._is_show_allowed())

    def _is_show_allowed(self) -> bool:
        """Determine whether the show-answer control can currently be used."""

        state = self.controller.service.state
        if state is None:
            return False
        config = state.show_config
        if not config.enabled:
            return False
        if config.max_uses is None:
            return True
        if config.max_uses <= 0:
            return False
        return state.show_used < config.max_uses

    def _start_timer(self, seconds: int) -> None:
        """Create and begin the countdown timer for Speed mode."""

        self._stop_timer()
        self._show_timer_label()
        self.timer = CountdownTimer(seconds, self._update_timer_label,
                                    self._handle_timer_finish)
        self.timer.start()
        self._schedule_timer_tick()

    def _schedule_timer_tick(self) -> None:
        """Arrange the next timer tick callback."""

        if self.timer and self.timer.is_running:
            self._timer_after_id = self.after(250, self._tick_timer)

    def _tick_timer(self) -> None:
        """Advance the timer and continue scheduling ticks."""

        if not self.timer:
            return
        self.timer.tick()
        if self.timer.is_running:
            self._timer_after_id = self.after(250, self._tick_timer)
        else:
            self._timer_after_id = None

    def _update_timer_label(self, remaining: int) -> None:
        """Refresh the displayed timer text."""

        self.timer_var.set(f"Time Remaining: {remaining}s")

    def _apply_time_penalty(self, seconds: int) -> None:
        """Deduct time from the running timer."""

        if self.timer:
            self.timer.deduct(seconds)

    def _handle_timer_finish(self) -> None:
        """Respond to the timer reaching zero seconds."""

        state = self.controller.service.state
        if state:
            state.finished = True
            self.status_var.set(f"Time's up! Score: {state.score}")
        self.card.set_question("Time's up! Session ended.")
        self.card.disable_all()
        self.card.set_show_enabled(False)
        self._stop_timer()

    def _stop_timer(self) -> None:
        """Halt any active timer and remove scheduled callbacks."""

        if self.timer:
            self.timer.stop()
            self.timer = None
        if self._timer_after_id:
            self.after_cancel(self._timer_after_id)
            self._timer_after_id = None
        self._hide_timer_label()

    def _show_timer_label(self) -> None:
        """Display the timer label above the flashcard."""

        if not self.timer_label.winfo_ismapped():
            self.timer_label.pack(before=self.card, anchor=tk.N, pady=(0, 6))

    def _hide_timer_label(self) -> None:
        """Hide the timer label when Speed mode is not active."""

        self.timer_label.pack_forget()
