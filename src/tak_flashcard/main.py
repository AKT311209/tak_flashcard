"""Application entry point wrapper."""

from __future__ import annotations

from tak_flashcard.config import ensure_executable_data_dirs
from tak_flashcard.gui.app import run


def main() -> None:
    """Launch the GUI application."""

    ensure_executable_data_dirs()

    run()


if __name__ == "__main__":
    main()
