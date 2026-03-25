"""Reusable option panels for flashcard configuration."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional

from tak_flashcard.config import (
    DEFAULT_QUESTION_COUNT,
    DEFAULT_SHOW_LIMIT,
    DEFAULT_SHOW_SCORE_PENALTY,
    DEFAULT_SHOW_TIME_PENALTY,
    DEFAULT_TIME_LIMIT,
    DEFAULT_WRONG_ANSWER_PENALTY,
    DIFFICULTY_LEVELS,
    Direction,
    Mode,
)
from tak_flashcard.core.safeguard import SessionConfigValidation, build_safe_session_config
from tak_flashcard.features.flashcard.states import SessionConfig


class FlashcardOptions(ttk.Frame):
    """Options panel for configuring a flashcard session."""

    def __init__(
        self,
        master: tk.Misc,
        default_question_count: int = DEFAULT_QUESTION_COUNT,
        default_time_limit: int = DEFAULT_TIME_LIMIT,
        on_validation_change: Optional[Callable[[
            SessionConfigValidation], None]] = None,
    ):
        """Initialize the options panel widgets."""

        super().__init__(master, padding=10, style="Glass.TFrame")
        self.mode = tk.StringVar(value=Mode.ENDLESS.value)
        self.direction = tk.StringVar(value=Direction.ENG_TO_VN.value)
        self.difficulty = tk.IntVar(value=3)
        self.question_count = tk.StringVar(value=str(default_question_count))
        self.time_limit = tk.StringVar(value=str(default_time_limit))
        self.show_score_penalty = tk.StringVar(
            value=str(DEFAULT_SHOW_SCORE_PENALTY)
        )
        self.show_limit = tk.StringVar(value=str(DEFAULT_SHOW_LIMIT))
        self.show_time_penalty = tk.StringVar(
            value=str(DEFAULT_SHOW_TIME_PENALTY))
        self.endless_penalty_choice = tk.StringVar(value="score")
        self.speed_penalty_choice = tk.StringVar(value="score")
        self.wrong_answer_penalty = tk.StringVar(
            value=str(DEFAULT_WRONG_ANSWER_PENALTY)
        )
        self._on_validation_change = on_validation_change
        self._last_validation = SessionConfigValidation(config=None, issues=[])

        self._build_widgets()
        self._setup_validation_traces()
        self._emit_validation_state()

    def _build_widgets(self) -> None:
        """Construct the option controls."""

        mode_frame = ttk.LabelFrame(
            self, text="Mode", style="Glass.TLabelframe")
        for m in Mode:
            ttk.Radiobutton(
                mode_frame,
                text=m.name.title(),
                variable=self.mode,
                value=m.value,
            ).pack(anchor=tk.W, pady=1)
        mode_frame.grid(row=0, column=0, sticky="nsew", padx=6, pady=4)

        dir_frame = ttk.LabelFrame(
            self, text="Direction", style="Glass.TLabelframe")
        for d in Direction:
            label = {
                Direction.ENG_TO_VN: "English → Vietnamese",
                Direction.VN_TO_ENG: "Vietnamese → English",
                Direction.MIXED: "Mixed",
            }[d]
            ttk.Radiobutton(
                dir_frame, text=label, variable=self.direction, value=d.value).pack(anchor=tk.W)
        dir_frame.grid(row=0, column=1, sticky="nsew", padx=6, pady=4)

        diff_frame = ttk.LabelFrame(
            self, text="Difficulty", style="Glass.TLabelframe")
        self.difficulty_scale = tk.Scale(
            diff_frame,
            from_=min(DIFFICULTY_LEVELS),
            to=max(DIFFICULTY_LEVELS),
            variable=self.difficulty,
            orient=tk.HORIZONTAL,
            resolution=1,
            tickinterval=1,
            showvalue=False,
        )
        self._apply_difficulty_scale_style()
        self.difficulty_scale.pack(fill="x", padx=6, pady=6)
        ttk.Label(diff_frame, textvariable=self.difficulty,
                  style="Muted.TLabel").pack()
        diff_frame.grid(row=1, column=0, sticky="nsew", padx=6, pady=4)

        mode_opts = ttk.LabelFrame(
            self, text="Mode Options", style="Glass.TLabelframe")
        self.question_frame = ttk.Frame(mode_opts)
        ttk.Label(self.question_frame,
                  text="Question Count (Testing)").pack(anchor=tk.W)
        ttk.Entry(self.question_frame, textvariable=self.question_count).pack(
            fill="x", padx=4, pady=2)

        self.endless_choice_frame = ttk.Frame(mode_opts)
        ttk.Label(self.endless_choice_frame, text="Endless show penalty type").pack(
            anchor=tk.W)
        ttk.Radiobutton(
            self.endless_choice_frame,
            text="Score deduction",
            variable=self.endless_penalty_choice,
            value="score",
        ).pack(anchor=tk.W)
        ttk.Radiobutton(
            self.endless_choice_frame,
            text="Limit uses",
            variable=self.endless_penalty_choice,
            value="limit",
        ).pack(anchor=tk.W)

        self.speed_choice_frame = ttk.Frame(mode_opts)
        ttk.Label(self.speed_choice_frame, text="Speed show penalty type").pack(
            anchor=tk.W)
        ttk.Radiobutton(
            self.speed_choice_frame,
            text="Score deduction",
            variable=self.speed_penalty_choice,
            value="score",
        ).pack(anchor=tk.W)
        ttk.Radiobutton(
            self.speed_choice_frame,
            text="Limit uses",
            variable=self.speed_penalty_choice,
            value="limit",
        ).pack(anchor=tk.W)
        ttk.Radiobutton(
            self.speed_choice_frame,
            text="Time deduction",
            variable=self.speed_penalty_choice,
            value="time",
        ).pack(anchor=tk.W)

        self.penalty_score_frame = ttk.Frame(mode_opts)
        ttk.Label(self.penalty_score_frame, text="Show penalty points").pack(
            anchor=tk.W)
        self.penalty_score_entry = ttk.Entry(
            self.penalty_score_frame, textvariable=self.show_score_penalty
        )
        self.penalty_score_entry.pack(fill="x", padx=4, pady=2)

        self.limit_question_frame = ttk.Frame(mode_opts)
        ttk.Label(self.limit_question_frame, text="Limit show uses (0 = unlimited)").pack(
            anchor=tk.W)
        self.limit_spinbox = ttk.Spinbox(
            self.limit_question_frame, from_=0, to=99, textvariable=self.show_limit
        )
        self.limit_spinbox.pack(fill="x", padx=4, pady=2)

        self.penalty_time_frame = ttk.Frame(mode_opts)
        ttk.Label(self.penalty_time_frame, text="Time penalty sec (Speed)").pack(
            anchor=tk.W)
        self.penalty_time_entry = ttk.Entry(
            self.penalty_time_frame, textvariable=self.show_time_penalty
        )
        self.penalty_time_entry.pack(fill="x", padx=4, pady=2)

        self.time_frame = ttk.Frame(mode_opts)
        ttk.Label(self.time_frame, text="Time Limit sec (Speed)").pack(
            anchor=tk.W)
        ttk.Entry(self.time_frame, textvariable=self.time_limit).pack(
            fill="x", padx=4, pady=2)
        self.wrong_penalty_frame = ttk.Frame(mode_opts)
        ttk.Label(
            self.wrong_penalty_frame, text="Wrong answer penalty points"
        ).pack(anchor=tk.W)
        self.wrong_penalty_entry = ttk.Entry(
            self.wrong_penalty_frame, textvariable=self.wrong_answer_penalty
        )
        self.wrong_penalty_entry.pack(fill="x", padx=4, pady=2)
        mode_opts.grid(row=1, column=1, sticky="nsew", padx=6, pady=4)

        self.mode.trace_add("write", self._update_mode_specific_controls)
        self.endless_penalty_choice.trace_add(
            "write", lambda *_: self._sync_endless_penalty_state()
        )
        self.speed_penalty_choice.trace_add(
            "write", lambda *_: self._sync_speed_penalty_state()
        )
        self._update_mode_specific_controls()

        for i in range(2):
            self.columnconfigure(i, weight=1)
        for i in range(2):
            self.rowconfigure(i, weight=1)

    def session_config(self) -> SessionConfig:
        """Build a normalized :class:`SessionConfig` from widget values.

        Raises:
            ValueError: If one or more inputs are invalid.
        """

        validation = self.validation_result()
        if validation.config is None:
            first_error = validation.issues[0].message if validation.issues else "Invalid session configuration."
            raise ValueError(first_error)
        return validation.config

    def validation_result(self) -> SessionConfigValidation:
        """Return the current safeguard validation result for all inputs."""

        return build_safe_session_config(
            mode_value=self.mode.get(),
            direction_value=self.direction.get(),
            difficulty_value=self.difficulty.get(),
            question_count_value=self.question_count.get(),
            time_limit_value=self.time_limit.get(),
            show_score_penalty_value=self.show_score_penalty.get(),
            show_limit_value=self.show_limit.get(),
            show_time_penalty_value=self.show_time_penalty.get(),
            wrong_answer_penalty_value=self.wrong_answer_penalty.get(),
            endless_penalty_choice=self.endless_penalty_choice.get(),
            speed_penalty_choice=self.speed_penalty_choice.get(),
        )

    def _update_mode_specific_controls(self, *_: str) -> None:
        """Show or hide mode-specific fields based on the selected mode."""

        selected = Mode(self.mode.get())
        # Reset all mode-specific frames
        self.question_frame.pack_forget()
        self.endless_choice_frame.pack_forget()
        self.speed_choice_frame.pack_forget()
        self.penalty_score_frame.pack_forget()
        self.limit_question_frame.pack_forget()
        self.penalty_time_frame.pack_forget()
        self.time_frame.pack_forget()
        self._disable_all_penalty_entries()
        self._configure_wrong_penalty_field(False)

        if selected == Mode.TESTING:
            self.question_frame.pack(fill="x", padx=4, pady=2)

        if selected == Mode.ENDLESS:
            self.endless_choice_frame.pack(fill="x", padx=4, pady=2)
            self._sync_endless_penalty_state()
            self._configure_wrong_penalty_field(True)
        elif selected == Mode.SPEED:
            self.speed_choice_frame.pack(fill="x", padx=4, pady=2)
            self._sync_speed_penalty_state()
            self.time_frame.pack(fill="x", padx=4, pady=2)
            self._configure_wrong_penalty_field(True)

        self._emit_validation_state()

    def _sync_endless_penalty_state(self) -> None:
        """Show the correct endless penalty field and disable the rest."""

        if Mode(self.mode.get()) != Mode.ENDLESS:
            return
        choice = self.endless_penalty_choice.get()
        self._disable_entry(self.penalty_time_entry, self.show_time_penalty)
        self.penalty_score_frame.pack_forget()
        self.limit_question_frame.pack_forget()
        if choice == "score":
            self._enable_entry(
                self.penalty_score_entry,
                self.show_score_penalty,
                DEFAULT_SHOW_SCORE_PENALTY,
            )
            self._disable_entry(self.limit_spinbox, self.show_limit)
            self.penalty_score_frame.pack(fill="x", padx=4, pady=2)
        else:
            self._disable_entry(self.penalty_score_entry,
                                self.show_score_penalty)
            self._enable_entry(
                self.limit_spinbox,
                self.show_limit,
                DEFAULT_SHOW_LIMIT,
            )
            self.limit_question_frame.pack(fill="x", padx=4, pady=2)

        self._emit_validation_state()

    def _sync_speed_penalty_state(self) -> None:
        """Show the selected speed penalty field and disable the others."""

        if Mode(self.mode.get()) != Mode.SPEED:
            return
        choice = self.speed_penalty_choice.get()
        self.penalty_score_frame.pack_forget()
        self.limit_question_frame.pack_forget()
        self.penalty_time_frame.pack_forget()
        if choice == "score":
            self._enable_entry(
                self.penalty_score_entry,
                self.show_score_penalty,
                DEFAULT_SHOW_SCORE_PENALTY,
            )
            self._disable_entry(self.limit_spinbox, self.show_limit)
            self._disable_entry(self.penalty_time_entry,
                                self.show_time_penalty)
            self.penalty_score_frame.pack(fill="x", padx=4, pady=2)
        elif choice == "limit":
            self._disable_entry(self.penalty_score_entry,
                                self.show_score_penalty)
            self._enable_entry(
                self.limit_spinbox,
                self.show_limit,
                DEFAULT_SHOW_LIMIT,
            )
            self._disable_entry(self.penalty_time_entry,
                                self.show_time_penalty)
            self.limit_question_frame.pack(fill="x", padx=4, pady=2)
        else:
            self._disable_entry(self.penalty_score_entry,
                                self.show_score_penalty)
            self._disable_entry(self.limit_spinbox, self.show_limit)
            self._enable_entry(
                self.penalty_time_entry,
                self.show_time_penalty,
                DEFAULT_SHOW_TIME_PENALTY,
            )
            self.penalty_time_frame.pack(fill="x", padx=4, pady=2)

        self._emit_validation_state()

    def _disable_all_penalty_entries(self) -> None:
        """Disable every penalty input field."""

        self._disable_entry(self.penalty_score_entry, self.show_score_penalty)
        self._disable_entry(self.limit_spinbox, self.show_limit)
        self._disable_entry(self.penalty_time_entry, self.show_time_penalty)

    def _apply_difficulty_scale_style(self) -> None:
        """Apply glassmorphism-aligned colors to the difficulty slider."""

        style = ttk.Style(self)
        background = (
            style.lookup("Glass.TLabelframe", "background")
            or style.lookup("TLabelframe", "background")
            or "#e8eef7"
        )
        slider_bg = (
            style.lookup("Glass.TFrame", "background")
            or style.lookup("TButton", "background")
            or "#f2f6fc"
        )
        trough = (
            style.lookup("Horizontal.TScale", "troughcolor")
            or style.lookup("TLabelframe", "bordercolor")
            or "#c7d3e3"
        )
        text = style.lookup("TLabel", "foreground") or "#1a1a2e"
        accent = style.lookup("Primary.TButton", "background") or "#7bbad6"
        border = style.lookup("TLabelframe", "bordercolor") or "#c7d3e3"

        self.difficulty_scale.configure(
            bg=background,
            fg=text,
            troughcolor=trough,
            sliderlength=28,
            width=14,
            cursor="hand2",
            bd=1,
            background=slider_bg,
            activebackground=accent,
            highlightthickness=0,
            relief=tk.GROOVE,
            sliderrelief=tk.RAISED,
        )

    def _configure_wrong_penalty_field(self, visible: bool) -> None:
        """Show or hide the wrong-answer penalty field."""

        if visible:
            self.wrong_penalty_frame.pack(fill="x", padx=4, pady=2)
            self._set_entry_state(self.wrong_penalty_entry, True)
        else:
            self.wrong_penalty_frame.pack_forget()
            self._set_entry_state(self.wrong_penalty_entry, False)

    def _setup_validation_traces(self) -> None:
        """Attach traces so validation updates immediately on any input change."""

        variables: list[tk.Variable] = [
            self.mode,
            self.direction,
            self.difficulty,
            self.question_count,
            self.time_limit,
            self.show_score_penalty,
            self.show_limit,
            self.show_time_penalty,
            self.wrong_answer_penalty,
            self.endless_penalty_choice,
            self.speed_penalty_choice,
        ]
        for variable in variables:
            variable.trace_add("write", self._handle_value_change)

    def _handle_value_change(self, *_: str) -> None:
        """React to variable changes by emitting a fresh validation state."""

        self._emit_validation_state()

    def _emit_validation_state(self) -> None:
        """Compute and publish the latest safeguard validation result."""

        self._last_validation = self.validation_result()
        if self._on_validation_change:
            self._on_validation_change(self._last_validation)

    @staticmethod
    def _set_entry_state(entry: ttk.Entry, enabled: bool) -> None:
        """Configure the entry widget state without mutating its value."""

        entry.config(state="normal" if enabled else "disabled")

    @staticmethod
    def _enable_entry(entry: ttk.Entry, var: tk.Variable, default_value: int) -> None:
        """Enable the entry and ensure it has a default value."""

        entry.config(state="normal")
        text = str(var.get()).strip()
        if text == "" or text == "0":
            var.set(str(default_value))

    @staticmethod
    def _disable_entry(entry: ttk.Entry, var: tk.Variable) -> None:
        """Disable the entry and reset its value to zero."""

        entry.config(state="disabled")
        var.set("0")
