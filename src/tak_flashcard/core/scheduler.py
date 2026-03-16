"""Countdown timer for Speed mode sessions.

In Speed mode the player races against a clock.  This module provides
``CountdownTimer``, which counts down from a given number of seconds and
fires callbacks so the GUI can update the display and end the session
when time runs out.

The timer measures real wall-clock time (via ``time.time()``) rather than
trusting the Tkinter ``after()`` interval, so it stays accurate even if
the UI is briefly delayed.

Calling order:
  gui/views/flashcard_view.py :: FlashcardSessionView
      → _start_timer()   — creates and starts the timer
      → _tick_timer()    — called every 250 ms by Tkinter's after() loop
          → CountdownTimer.tick()
              → tick_callback(seconds_left)   — updates the display label
              → finish_callback()             — called when time reaches 0
"""

from __future__ import annotations

import time
from typing import Callable


class CountdownTimer:
    """A countdown timer that integrates with Tkinter's event loop.

    The GUI polls this object every 250 ms by calling :meth:`tick`.
    On each tick the elapsed wall-clock time is subtracted from the
    remaining seconds, then the ``tick_callback`` is called with the
    updated value.  When time reaches zero, ``finish_callback`` is called
    once to signal session end.

    The timer can be paused and resumed (e.g. while feedback is shown),
    and seconds can be deducted as a penalty when the user reveals an answer.
    """

    def __init__(
        self,
        seconds: int,
        tick_callback: Callable[[int], None],
        finish_callback: Callable[[], None],
    ):
        """Set up the timer before starting it.

        Parameters:
            seconds: Total number of seconds to count down from.
            tick_callback: Called with the remaining seconds (as an int)
                on every tick and immediately after start/resume/deduct.
                Used to update the on-screen timer label.
            finish_callback: Called once when remaining time reaches zero.
                Used to trigger end-of-session logic.
        """

        self.total_seconds = float(seconds)
        self.remaining = float(seconds)
        self._running = False
        self._tick_callback = tick_callback
        self._finish_callback = finish_callback
        self._last_tick = time.time()

    def start(self) -> None:
        """Begin the countdown and fire the first tick callback immediately."""

        self._running = True
        self._last_tick = time.time()
        self._tick_callback(int(self.remaining))

    def stop(self) -> None:
        """Stop the countdown completely (cannot be resumed after this)."""

        self._running = False

    def pause(self) -> None:
        """Freeze the timer without resetting the remaining time.

        Typically called when the session is waiting for the user to read
        feedback between cards.
        """

        if not self._running:
            return
        self._running = False

    def resume(self) -> None:
        """Continue counting down from where it was paused.

        Does nothing if already running or if time has already expired.
        """

        if self._running or self.remaining <= 0:
            return
        self._running = True
        self._last_tick = time.time()
        self._tick_callback(int(self.remaining))

    def tick(self) -> None:
        """Advance the timer by however much real time has passed since the last call.

        Called repeatedly by the GUI every 250 ms.  Measures actual elapsed
        wall-clock time rather than assuming exactly 250 ms, so the countdown
        stays accurate even when the UI is briefly busy.

        If remaining time reaches zero, ``finish_callback`` is fired and the
        timer stops itself automatically.
        """

        if not self._running:
            return
        now = time.time()
        elapsed = now - self._last_tick
        self._last_tick = now
        self.remaining = max(self.remaining - elapsed, 0.0)
        self._tick_callback(int(self.remaining))
        if self.remaining <= 0:
            self._running = False
            self._finish_callback()

    def deduct(self, seconds: int) -> None:
        """Subtract seconds from the remaining time as a Show Answer penalty.

        If the deduction brings time to zero or below, the finish callback
        is triggered immediately.

        Parameters:
            seconds: Number of seconds to remove.  Non-positive values
                are ignored.
        """

        if seconds <= 0:
            return
        self.remaining = max(self.remaining - seconds, 0.0)
        self._tick_callback(int(self.remaining))
        if self.remaining <= 0 and self._running:
            self._running = False
            self._finish_callback()

    @property
    def is_running(self) -> bool:
        """``True`` if the timer is currently counting down."""

        return self._running
