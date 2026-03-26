"""Flashcard configuration view implementation."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional

from tak_flashcard.config import (
    DEFAULT_QUESTION_COUNT,
    DEFAULT_TIME_LIMIT,
    Direction,
    Mode,
)
from tak_flashcard.core.safeguard import SessionConfigValidation
from tak_flashcard.core.scheduler import CountdownTimer
from tak_flashcard.features.flashcard.controller import FlashcardController
from tak_flashcard.features.flashcard.states import (
    SessionConfig,
    SessionSummary,
    ShowAnswerOutcome,
)
from tak_flashcard.gui.components.flashcard_card import FlashcardCard
from tak_flashcard.gui.components.neumorphic import NeumorphicTimer
from tak_flashcard.gui.components.option_panels import FlashcardOptions


class FlashcardView(ttk.Frame):
    """View for configuring flashcard sessions before starting."""

    def __init__(
        self,
        master: tk.Misc,
        on_start_session: Callable[[SessionConfig], None],
        on_back: Callable[[], None],
    ):
        """Initialize the flashcard settings view and navigation callbacks.

        Parameters:
            master: Parent Tkinter widget.
            on_start_session: Callback invoked with selected session options.
            on_back: Callback used to return to home.
        """

        super().__init__(master, padding=20, style="Page.TFrame")
        self.on_start_session = on_start_session
        self.on_back = on_back
        self.status_var = tk.StringVar(value="Ready to start")
        self._start_button: Optional[ttk.Button] = None
        self._status_label: Optional[ttk.Label] = None
        self._pending_validation: Optional[SessionConfigValidation] = None

        header = ttk.Frame(self, padding=16, style="Glass.TFrame")
        header.pack(fill="x", pady=(0, 12))
        ttk.Label(header, text="Flashcard Setup",
                  style="Title.TLabel").pack(anchor=tk.W)
        ttk.Label(
            header,
            text="Choose mode, direction, and penalties. Your learning logic stays exactly the same.",
            style="Subtitle.TLabel",
        ).pack(anchor=tk.W, pady=(4, 0))

        self.options = FlashcardOptions(
            self,
            default_question_count=DEFAULT_QUESTION_COUNT,
            default_time_limit=DEFAULT_TIME_LIMIT,
            on_validation_change=self._handle_validation_change,
        )
        self.options.pack(fill="x", pady=(0, 10))

        info = ttk.LabelFrame(self, text="Session Setup",
                              padding=10, style="Glass.TLabelframe")
        ttk.Label(
            info,
            text="Adjust settings above, then click START SESSION to open the session screen.",
            style="Muted.TLabel",
        ).pack(anchor=tk.W)
        info.pack(fill="x", pady=(0, 10))

        controls = ttk.Frame(self, style="Page.TFrame")
        self._start_button = ttk.Button(
            controls,
            text="Start Session",
            style="Primary.TButton",
            command=self.start_session,
        )
        self._start_button.pack(side=tk.LEFT, padx=4)
        ttk.Button(controls, text="Back", command=self.on_back).pack(
            side=tk.LEFT, padx=4
        )
        controls.pack(pady=6)

        status = ttk.Frame(self, padding=10, style="Glass.TFrame")
        status.pack(fill="x", pady=(4, 0))
        self._status_label = ttk.Label(
            status,
            textvariable=self.status_var,
            style="Status.TLabel",
        )
        self._status_label.pack(anchor=tk.W)

        if self._pending_validation is not None:
            self._handle_validation_change(self._pending_validation)
        else:
            self._handle_validation_change(self.options.validation_result())

    def _handle_validation_change(self, validation: SessionConfigValidation) -> None:
        """Update setup status and button state when input validity changes."""

        if self._status_label is None or self._start_button is None:
            self._pending_validation = validation
            return

        self._pending_validation = None

        if validation.is_valid:
            self.status_var.set("Ready to start")
            self._status_label.config(foreground="black")
            self._start_button.config(state="normal")
            return

        self.status_var.set(validation.issues[0].message)
        self._status_label.config(foreground="red")
        self._start_button.config(state="disabled")

    def start_session(self) -> None:
        """Start a new flashcard session using the configured options."""

        validation = self.options.validation_result()
        if not validation.is_valid or validation.config is None:
            message = validation.issues[0].message if validation.issues else "Invalid session configuration."
            self.status_var.set(message)
            if self._status_label is not None:
                self._status_label.config(foreground="red")
            if self._start_button is not None:
                self._start_button.config(state="disabled")
            return
        if self._status_label is not None:
            self._status_label.config(foreground="black")
        if self._start_button is not None:
            self._start_button.config(state="normal")
        self.on_start_session(validation.config)


class FlashcardSessionView(ttk.Frame):
    """View for running an active flashcard session."""

    def __init__(
        self,
        master: tk.Misc,
        controller: FlashcardController,
        on_session_end: Callable[[SessionSummary], None],
    ):
        """Initialize session widgets and callbacks.

        Parameters:
            master: Parent Tkinter widget.
            controller: Flashcard session controller.
            on_session_end: Callback invoked with the session summary when the
                session ends (natural completion or user exit).
        """

        super().__init__(master, padding=20, style="Page.TFrame")
        self.controller = controller
        self.on_session_end = on_session_end
        self.timer_var = tk.StringVar(value="")

        header = ttk.Frame(self, padding=14, style="Glass.TFrame")
        header.pack(fill="x", pady=(0, 10))
        ttk.Label(header, text="Active Session",
                  style="Section.TLabel").pack(anchor=tk.W)

        timer_container = ttk.Frame(self, style="Glass.TFrame")

        self.timer_display: NeumorphicTimer | None = None
        self.timer: CountdownTimer | None = None
        self._timer_after_id: str | None = None

        self.card = FlashcardCard(
            self,
            self.submit_answer,
            self.show_answer,
            self.next_card,
            self._handle_exit_session,
        )
        self.card.pack(fill="x", pady=(6, 4))

        self._loading_var = tk.StringVar(value="")
        self._loading_label = ttk.Label(
            self, textvariable=self._loading_var, style="Muted.TLabel"
        )
        self._loading_label.pack(anchor=tk.W, padx=14)

        self.status_var = tk.StringVar(value="Session not started")
        status_card = ttk.Frame(self, padding=12, style="Glass.TFrame")
        status_card.pack(fill="x", pady=(8, 6))
        ttk.Label(
            status_card,
            textvariable=self.status_var,
            style="Status.TLabel",
        ).pack(anchor=tk.W)

        self._timer_container = timer_container

    def begin_session(
        self,
        config: SessionConfig,
    ) -> None:
        """Start a new session and render the first card."""

        self._stop_timer()
        self._loading_var.set("Preparing questions…")
        self.status_var.set("Preparing session...")
        self.update_idletasks()
        self.controller.start(config)
        self._loading_var.set("")
        self.status_var.set(
            f"Mode: {config.mode.name.title()} | Direction: {config.direction.name} | Score: 0"
        )
        if config.mode == Mode.SPEED and config.time_limit is not None:
            self._start_timer(config.time_limit)
        else:
            self._hide_timer_label()
        self.next_card()

    def next_card(self) -> None:
        """Fetch and display the next card for the current session."""

        self._loading_var.set("Loading…")
        self.update_idletasks()
        card = self.controller.next_card()
        if card is None:
            self._loading_var.set("")
            state = self.controller.service.state
            self._stop_timer()
            if state and state.finished:
                self._display_terminal_card("Session complete!")
                self._capture_time_used()
                self.after(1500, self._emit_session_end)
            else:
                self._display_terminal_card("No cards available.")
            return
        state = self.controller.service.state
        direction = self._active_direction()
        prompt = self._prompt_for(card.english, card.vietnamese, direction)
        self.card.set_question(prompt)
        self.card.set_choices(state.current_choices if state else [])
        self._loading_var.set("")
        self._update_show_button_state()
        self._resume_timer()

    def submit_answer(self, answer: str) -> None:
        """Submit answer and update feedback panel."""

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
        self._pause_timer()
        self.status_var.set(f"Score: {result.new_score}")

    def show_answer(self) -> None:
        """Reveal the current answer and apply configured penalty."""

        state = self.controller.service.state
        if state is None or state.current_word is None:
            return
        direction = self._active_direction()
        prompt = self._prompt_for(
            state.current_word.english,
            state.current_word.vietnamese,
            direction,
        )
        answer = self._answer_for(
            state.current_word.english,
            state.current_word.vietnamese,
            direction,
        )
        outcome: ShowAnswerOutcome = self.controller.reveal()
        if not outcome.allowed:
            message = "Show limit reached" if state.show_config.max_uses is not None else "Show answer unavailable"
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
        self._pause_timer()

    def _handle_exit_session(self) -> None:
        """Capture remaining time, stop the timer, and emit the session summary."""

        self._capture_time_used()
        self._stop_timer()
        self._emit_session_end()

    def _capture_time_used(self) -> None:
        """Store the elapsed play time on the state for Speed mode sessions."""

        state = self.controller.service.state
        if state is None:
            return
        if state.mode == Mode.SPEED:
            if self.timer is not None:
                state.time_used = (state.time_limit or 0) - \
                    int(self.timer.remaining)
            elif state.time_limit is not None and state.finished:
                state.time_used = state.time_limit

    def _emit_session_end(self) -> None:
        """Build the session summary and invoke the end-of-session callback."""

        summary = self.controller.get_summary()
        if summary is not None:
            self.on_session_end(summary)

    def _update_show_button_state(self) -> None:
        """Enable or disable the show-answer button based on the state."""

        self.card.set_show_enabled(self._is_show_allowed())

    def _is_show_allowed(self) -> bool:
        """Determine whether the show-answer control can currently be used."""

        state = self.controller.service.state
        if state is None or not state.show_config.enabled:
            return False
        config = state.show_config
        return config.max_uses is None or (config.max_uses > 0 and state.show_used < config.max_uses)

    def _active_direction(self) -> Direction:
        """Return the current card direction or a sensible default."""

        state = self.controller.service.state
        if state is None:
            return Direction.ENG_TO_VN
        return state.current_direction or state.direction

    @staticmethod
    def _prompt_for(english: object, vietnamese: object, direction: Direction) -> str:
        """Return the prompt text for the provided direction."""

        return str(english) if direction == Direction.ENG_TO_VN else str(vietnamese)

    @staticmethod
    def _answer_for(english: object, vietnamese: object, direction: Direction) -> str:
        """Return the answer text for the provided direction."""

        return str(vietnamese) if direction == Direction.ENG_TO_VN else str(english)

    def _display_terminal_card(self, message: str) -> None:
        """Render a disabled terminal card state with a message."""

        self.card.set_question(message)
        self.card.set_choices([])
        self.card.disable_all()
        self.card.set_show_enabled(False)

    def _start_timer(self, seconds: int) -> None:
        """Create and begin the countdown timer for Speed mode."""

        self._stop_timer()
        self._show_timer_label()
        self.timer = CountdownTimer(
            seconds, self._update_timer_label, self._handle_timer_finish)
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
        timer = self.timer
        timer.tick()
        if timer.is_running:
            self._timer_after_id = self.after(250, self._tick_timer)
        else:
            self._timer_after_id = None

    def _update_timer_label(self, remaining: int) -> None:
        """Refresh the displayed timer text."""

        if self.timer_display is not None:
            self.timer_display.update_time(remaining)

    def _apply_time_penalty(self, seconds: int) -> None:
        """Deduct time from the running timer."""

        if self.timer:
            self.timer.deduct(seconds)

    def _pause_timer(self) -> None:
        """Pause timer updates while the flashcard is in feedback mode."""

        if not self.timer:
            return
        self.timer.pause()
        if self._timer_after_id:
            self.after_cancel(self._timer_after_id)
            self._timer_after_id = None

    def _resume_timer(self) -> None:
        """Resume the timer when a new question becomes active."""

        if not self.timer or self.timer.is_running:
            return
        if self.timer.remaining <= 0:
            return
        self.timer.resume()
        self._schedule_timer_tick()

    def _handle_timer_finish(self) -> None:
        """Respond to the timer reaching zero seconds."""

        state = self.controller.service.state
        if state:
            state.finished = True
            state.time_used = state.time_limit
            self.status_var.set(f"Time's up! Score: {state.score}")
        self._display_terminal_card("Time's up! Session ended.")
        self._stop_timer()
        self.after(1500, self._emit_session_end)

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

        if not self._timer_container.winfo_manager():
            self._timer_container.pack(fill="x", pady=(0, 8), before=self.card)

        if self.timer_display is None:
            style = ttk.Style(self)
            bg_color = style.lookup("Glass.TFrame", "background") or "#f0f0f0"
            shadow_color = style.lookup(
                "Neumorphic.TFrame", "background") or "#e0e0e0"
            highlight_color = "#ffffff"
            text_color = style.lookup(
                "Section.TLabel", "foreground") or "#333333"

            self.timer_display = NeumorphicTimer(
                self._timer_container,
                width=300,
                height=140,
                bg_color=bg_color,
                shadow_color=shadow_color,
                highlight_color=highlight_color,
                text_color=text_color,
            )

        if not self.timer_display.winfo_manager():
            self.timer_display.pack(anchor=tk.CENTER, pady=8)

    def _hide_timer_label(self) -> None:
        """Hide the timer label when Speed mode is not active."""

        if self.timer_display is not None:
            self.timer_display.pack_forget()
        if self._timer_container.winfo_manager():
            self._timer_container.pack_forget()

    # ── keyboard handlers ─────────────────────────────────────────────────────

    def on_enter_key(self) -> None:
        """Advance to the next card when Enter is pressed and the card is awaiting next."""

        if self.card.awaiting_next:
            self.next_card()

    def on_space_key(self) -> None:
        """Trigger the Show Answer or Next button when Space is pressed."""

        self.card.trigger_show_or_next()

    def on_number_key(self, index: int) -> None:
        """Select and submit the answer choice at the given 1-based position.

        Parameters:
            index: 1-based index of the answer to select (1–4).
        """

        self.card.select_choice(index)
