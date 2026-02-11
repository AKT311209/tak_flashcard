"""Main GUI application entry point using DearPyGui."""

import logging
import sys

import dearpygui.dearpygui as dpg

from tak_flashcard.db.db import init_db
from tak_flashcard.settings import get_settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def setup_gui():
    """Set up the main GUI window and components."""
    dpg.create_context()

    # Main window
    with dpg.window(label="Tak Flashcard", tag="main_window"):
        dpg.add_text("Welcome to Tak Flashcard!", tag="welcome_text")
        dpg.add_separator()

        # Navigation tabs
        with dpg.tab_bar():
            # Flashcard tab
            with dpg.tab(label="Flashcard"):
                dpg.add_text("Flashcard Mode")
                dpg.add_separator()

                dpg.add_text("Session Configuration:")
                dpg.add_combo(
                    label="Mode",
                    items=["Endless", "Speed", "Testing"],
                    default_value="Endless",
                    tag="mode_combo",
                )
                dpg.add_combo(
                    label="Direction",
                    items=["E->V", "V->E", "Mixed"],
                    default_value="E->V",
                    tag="direction_combo",
                )
                dpg.add_slider_int(
                    label="Difficulty",
                    default_value=1,
                    min_value=1,
                    max_value=5,
                    tag="difficulty_slider",
                )
                dpg.add_input_int(
                    label="Question Count",
                    default_value=10,
                    tag="question_count_input",
                )

                dpg.add_separator()
                dpg.add_button(label="Start Session", callback=lambda: dpg.add_text("Session starting... (not implemented)", parent="main_window"))

            # Dictionary tab
            with dpg.tab(label="Dictionary"):
                dpg.add_text("Dictionary Browser")
                dpg.add_separator()

                dpg.add_input_text(label="Search", tag="search_input")
                dpg.add_button(label="Search", callback=lambda: dpg.add_text("Search not implemented", parent="main_window"))

                dpg.add_separator()
                dpg.add_text("(Dictionary table will be displayed here)")

            # Import tab
            with dpg.tab(label="Import"):
                dpg.add_text("Import Vocabulary")
                dpg.add_separator()

                dpg.add_button(
                    label="Select CSV/XLSX File",
                    callback=lambda: dpg.add_text("File picker not implemented", parent="main_window"),
                )
                dpg.add_text("", tag="import_status")

            # Settings tab
            with dpg.tab(label="Settings"):
                dpg.add_text("Application Settings")
                dpg.add_separator()

                settings = get_settings()
                dpg.add_slider_int(
                    label="Text Size",
                    default_value=settings.get("text_size", 14),
                    min_value=10,
                    max_value=24,
                    tag="text_size_slider",
                )
                dpg.add_checkbox(
                    label="Enable Animations",
                    default_value=settings.get("enable_animations", True),
                    tag="animations_checkbox",
                )

                dpg.add_separator()
                dpg.add_button(
                    label="Save Settings",
                    callback=lambda: save_settings(),
                )

            # Guide tab
            with dpg.tab(label="Guide"):
                dpg.add_text("User Guide")
                dpg.add_separator()

                dpg.add_text(
                    """
Tak Flashcard - User Guide

MODES:
- Endless: Practice without time limits
- Speed: Race against the clock
- Testing: Test your knowledge with limited HP

DIRECTIONS:
- E->V: English to Vietnamese
- V->E: Vietnamese to English
- Mixed: Random direction for each question

CONTROLS:
- Type your answer and press Enter to submit
- Click Reveal to show the answer (penalty applied)
- Track your score and progress in real-time

IMPORT:
- Import vocabulary from CSV or XLSX files
- Required columns: word, english, vietnamese
- Optional columns: pos, pronunciation, difficulty

For more information, visit the project documentation.
                    """,
                    wrap=600,
                )

    dpg.create_viewport(title="Tak Flashcard", width=800, height=600)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("main_window", True)


def save_settings():
    """Save settings from GUI to persistent storage."""
    settings = get_settings()

    # Get values from GUI
    text_size = dpg.get_value("text_size_slider")
    animations = dpg.get_value("animations_checkbox")

    # Update settings
    settings.set("text_size", text_size)
    settings.set("enable_animations", animations)
    settings.save()

    logger.info("Settings saved")
    dpg.set_value("import_status", "Settings saved successfully!")


def main():
    """Main application entry point."""
    logger.info("Starting Tak Flashcard application")

    try:
        # Initialize database
        logger.info("Initializing database...")
        init_db()

        # Set up GUI
        logger.info("Setting up GUI...")
        setup_gui()

        # Start GUI event loop
        dpg.start_dearpygui()

    except Exception as e:
        logger.error(f"Application error: {e}", exc_info=True)
        sys.exit(1)

    finally:
        # Cleanup
        dpg.destroy_context()
        logger.info("Application closed")


if __name__ == "__main__":
    main()
