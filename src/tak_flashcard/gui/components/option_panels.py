"""Reusable option panels for flashcard configuration."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from tak_flashcard.constants import (
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


class FlashcardOptions(ttk.Frame):
    """Options panel for configuring a flashcard session."""

    def __init__(
        self,
        master: tk.Misc,
        default_question_count: int = DEFAULT_QUESTION_COUNT,
        default_time_limit: int = DEFAULT_TIME_LIMIT,
    ):
        """Initialize the options panel widgets."""

        super().__init__(master, padding=8)
        self.mode = tk.StringVar(value=Mode.ENDLESS.value)
        self.direction = tk.StringVar(value=Direction.ENG_TO_VN.value)
        self.difficulty = tk.IntVar(value=3)
        self.question_count = tk.IntVar(value=default_question_count)
        self.time_limit = tk.IntVar(value=default_time_limit)
        self.show_score_penalty = tk.IntVar(value=DEFAULT_SHOW_SCORE_PENALTY)
        self.show_limit = tk.IntVar(value=DEFAULT_SHOW_LIMIT)
        self.show_time_penalty = tk.IntVar(value=DEFAULT_SHOW_TIME_PENALTY)
        self.endless_penalty_choice = tk.StringVar(value="score")
        self.speed_penalty_choice = tk.StringVar(value="score")
        self.wrong_answer_penalty = tk.IntVar(
            value=DEFAULT_WRONG_ANSWER_PENALTY)

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

    def values(self) -> tuple[Mode, Direction, int, int, int, int, int, int, int]:
        """Return the selected configuration values."""

        return (
            Mode(self.mode.get()),
            Direction(self.direction.get()),
            int(self.difficulty.get()),
            int(self.question_count.get()),
            int(self.time_limit.get()),
            int(self.show_score_penalty.get()),
            int(self.show_limit.get()),
            int(self.show_time_penalty.get()),
            int(self.wrong_answer_penalty.get()),
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

    def _disable_all_penalty_entries(self) -> None:
        """Disable every penalty input field."""

        self._disable_entry(self.penalty_score_entry, self.show_score_penalty)
        self._disable_entry(self.limit_spinbox, self.show_limit)
        self._disable_entry(self.penalty_time_entry, self.show_time_penalty)

    def _configure_wrong_penalty_field(self, visible: bool) -> None:
        """Show or hide the wrong-answer penalty field."""

        if visible:
            self.wrong_penalty_frame.pack(fill="x", padx=4, pady=2)
            self._set_entry_state(self.wrong_penalty_entry, True)
        else:
            self.wrong_penalty_frame.pack_forget()
            self._set_entry_state(self.wrong_penalty_entry, False)

    @staticmethod
    def _set_entry_state(entry: ttk.Entry, enabled: bool) -> None:
        """Configure the entry widget state without mutating its value."""

        entry.config(state="normal" if enabled else "disabled")

    @staticmethod
    def _enable_entry(entry: ttk.Entry, var: tk.IntVar, default_value: int) -> None:
        """Enable the entry and ensure it has a default value."""

        entry.config(state="normal")
        if var.get() <= 0:
            var.set(default_value)

    @staticmethod
    def _disable_entry(entry: ttk.Entry, var: tk.IntVar) -> None:
        """Disable the entry and reset its value to zero."""

        entry.config(state="disabled")
        var.set(0)
