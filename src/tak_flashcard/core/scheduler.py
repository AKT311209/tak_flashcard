"""Timer and scheduler logic for Speed mode."""

import time
from typing import Optional, Callable


class Timer:
    """Countdown timer for Speed mode."""

    def __init__(self, duration: int):
        """
        Initialize timer.

        Args:
            duration: Timer duration in seconds
        """
        self.duration = duration
        self.remaining = duration
        self.start_time = None
        self.paused_time = None
        self.is_running = False
        self.is_paused = False

    def start(self):
        """Start the timer."""
        self.start_time = time.time()
        self.is_running = True
        self.is_paused = False

    def pause(self):
        """Pause the timer."""
        if self.is_running and not self.is_paused:
            self.paused_time = time.time()
            self.is_paused = True

    def resume(self):
        """Resume the timer after pause."""
        if self.is_running and self.is_paused:
            pause_duration = time.time() - self.paused_time
            self.start_time += pause_duration
            self.is_paused = False

    def get_remaining(self) -> float:
        """
        Get remaining time in seconds.

        Returns:
            Remaining time in seconds
        """
        if not self.is_running:
            return self.remaining

        if self.is_paused:
            elapsed = self.paused_time - self.start_time
        else:
            elapsed = time.time() - self.start_time

        self.remaining = max(0, self.duration - elapsed)
        return self.remaining

    def subtract_time(self, seconds: int):
        """
        Subtract time from the timer (for penalties).

        Args:
            seconds: Number of seconds to subtract
        """
        self.remaining = max(0, self.get_remaining() - seconds)
        self.duration = self.remaining
        self.start_time = time.time()

    def is_expired(self) -> bool:
        """
        Check if timer has expired.

        Returns:
            True if time is up
        """
        return self.get_remaining() <= 0

    def stop(self):
        """Stop the timer."""
        self.is_running = False
        self.get_remaining()

    def reset(self, duration: Optional[int] = None):
        """
        Reset the timer.

        Args:
            duration: New duration (uses original if None)
        """
        if duration is not None:
            self.duration = duration
        self.remaining = self.duration
        self.start_time = None
        self.paused_time = None
        self.is_running = False
        self.is_paused = False
