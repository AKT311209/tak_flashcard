"""Simple countdown scheduler for Speed mode."""

from __future__ import annotations

import time
from typing import Callable


class CountdownTimer:
    """Countdown timer using a Tkinter-compatible callback."""

    def __init__(self, seconds: int, tick_callback: Callable[[int], None], finish_callback: Callable[[], None]):
        """Initialize the timer with callbacks for tick and completion."""

        self.total_seconds = float(seconds)
        self.remaining = float(seconds)
        self._running = False
        self._tick_callback = tick_callback
        self._finish_callback = finish_callback
        self._last_tick = time.time()

    def start(self) -> None:
        """Start the countdown."""

        self._running = True
        self._last_tick = time.time()
        self._tick_callback(int(self.remaining))

    def stop(self) -> None:
        """Stop the countdown."""

        self._running = False

    def tick(self) -> None:
        """Advance the timer; intended to be called by the UI loop."""

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
        """Subtract the specified number of seconds from the timer."""

        if seconds <= 0:
            return
        self.remaining = max(self.remaining - seconds, 0.0)
        self._tick_callback(int(self.remaining))
        if self.remaining <= 0 and self._running:
            self._running = False
            self._finish_callback()

    @property
    def is_running(self) -> bool:
        """Return whether the timer is currently running."""

        return self._running
