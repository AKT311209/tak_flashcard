"""Formatting helpers."""

from __future__ import annotations

from tak_flashcard.config import Direction, Mode

def format_direction(direction: Direction | str) -> str:
    """Pretty-print translation direction labels."""

    value = direction.value if isinstance(direction, Direction) else direction
    normalized = str(value).strip().lower()
    mapping = {
        Direction.ENG_TO_VN.value: "English → Vietnamese",
        Direction.VN_TO_ENG.value: "Vietnamese → English",
        Direction.MIXED.value: "Mixed",
    }
    return mapping.get(normalized, str(direction))


def format_mode(mode: Mode | str) -> str:
    """Pretty-print flashcard mode labels."""

    value = mode.value if isinstance(mode, Mode) else mode
    normalized = str(value).strip().lower()
    mapping = {
        Mode.ENDLESS.value: "Endless",
        Mode.SPEED.value: "Speed",
        Mode.TESTING.value: "Testing",
    }
    return mapping.get(normalized, str(mode).replace("_", " ").title())


def format_seconds(total: int) -> str:
    """Convert seconds to a human-readable ``Xm Ys`` string."""

    mins, secs = divmod(max(int(total), 0), 60)
    if mins:
        return f"{mins}m {secs}s"
    return f"{secs}s"
