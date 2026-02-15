"""Application entry point wrapper."""

from __future__ import annotations

from tak_flashcard.gui.app import run


def main() -> None:
    """Launch the GUI application."""

    run()


if __name__ == "__main__":
    main()
