"""Session summary view shown after every flashcard session."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Callable

from tak_flashcard.config import Mode
from tak_flashcard.features.flashcard.states import SessionSummary


def _format_seconds(total: int) -> str:
    """Convert a number of seconds to a human-readable ``Xm Ys`` string.

    Parameters:
        total: Duration in whole seconds.

    Returns:
        A string like ``"2m 5s"`` for values ≥ 60 seconds, or ``"42s"``
        for shorter durations.
    """

    mins, secs = divmod(total, 60)
    if mins:
        return f"{mins}m {secs}s"
    return f"{secs}s"


class ResultsView(ttk.Frame):
    """Display an aggregated summary of the most recent flashcard session.

    This view is raised after every session ends, whether through a natural
    completion (timer expiry, question limit reached) or a user-initiated
    exit.  It shows correct-answer rate, final score, time used (Speed mode
    only), and show-answer usage (non-Testing modes only).
    """

    def __init__(
        self,
        master: tk.Misc,
        on_back: Callable[[], None],
        on_home: Callable[[], None],
    ):
        """Create the results view with navigation callbacks.

        Parameters:
            master: Parent Tkinter widget.
            on_back: Callback to return to the flashcard settings view.
            on_home: Callback to return to the application home screen.
        """

        super().__init__(master, padding=24)

        ttk.Label(
            self,
            text="Session Summary",
            font=("Arial", 18, "bold"),
        ).pack(pady=(0, 18))

        stats_frame = ttk.LabelFrame(self, text="Results", padding=16)
        stats_frame.pack(fill="x", padx=20, pady=8)

        self._correct_var = tk.StringVar(value="")
        self._score_var = tk.StringVar(value="")
        self._difficulty_var = tk.StringVar(value="")
        self._time_var = tk.StringVar(value="")
        self._show_var = tk.StringVar(value="")
        self._show_limit_var = tk.StringVar(value="")

        self._correct_label = ttk.Label(
            stats_frame,
            textvariable=self._correct_var,
            font=("Arial", 13),
        )
        self._correct_label.pack(anchor=tk.W, pady=4)

        score_row = ttk.Frame(stats_frame)
        self._score_label = ttk.Label(
            score_row,
            textvariable=self._score_var,
            font=("Arial", 13),
        )
        self._score_label.pack(side=tk.LEFT)
        self._show_limit_label = ttk.Label(
            score_row,
            textvariable=self._show_limit_var,
            font=("Arial", 12),
        )
        score_row.pack(anchor=tk.W, pady=4)

        self._difficulty_label = ttk.Label(
            stats_frame,
            textvariable=self._difficulty_var,
            font=("Arial", 13),
        )
        self._difficulty_label.pack(anchor=tk.W, pady=4)

        self._time_label = ttk.Label(
            stats_frame,
            textvariable=self._time_var,
            font=("Arial", 13),
        )

        self._show_label = ttk.Label(
            stats_frame,
            textvariable=self._show_var,
            font=("Arial", 13),
        )

        btn_frame = ttk.Frame(self)
        ttk.Button(
            btn_frame,
            text="Play Again",
            command=on_back,
        ).pack(side=tk.LEFT, padx=8)
        ttk.Button(
            btn_frame,
            text="Home",
            command=on_home,
        ).pack(side=tk.LEFT, padx=8)
        btn_frame.pack(pady=20)

    def update_summary(self, summary: SessionSummary) -> None:
        """Refresh all displayed statistics from the provided session summary.

        Parameters:
            summary: Completed-session data produced by
                :meth:`FlashcardController.get_summary`.
        """

        pct = f"{summary.percent_correct:.1f}%"
        self._correct_var.set(
            f"Correct:          {summary.correct} / {summary.asked}  ({pct})"
        )
        self._score_var.set(f"Score:            {summary.score}")
        self._difficulty_var.set(f"Difficulty:       {summary.difficulty}")
        limit_active = (
            summary.show_limit_total is not None
            and summary.mode in (Mode.ENDLESS, Mode.SPEED)
        )
        if limit_active:
            self._show_limit_var.set(
                f"Show uses: {summary.show_used}/{summary.show_limit_total}"
            )
            if not self._show_limit_label.winfo_ismapped():
                self._show_limit_label.pack(side=tk.LEFT, padx=(12, 0))
        else:
            self._show_limit_var.set("")
            self._show_limit_label.pack_forget()

        if summary.mode == Mode.SPEED and summary.time_used is not None:
            self._time_var.set(
                f"Time Used:        {_format_seconds(summary.time_used)}"
            )
            self._time_label.pack(anchor=tk.W, pady=4)
        else:
            self._time_label.pack_forget()

        if summary.mode != Mode.TESTING and not limit_active:
            self._show_var.set(
                f"Show Answer Uses: {summary.show_used}"
            )
            self._show_label.pack(anchor=tk.W, pady=4)
        else:
            self._show_label.pack_forget()
