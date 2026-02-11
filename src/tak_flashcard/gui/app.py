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

    # Get settings and apply colors
    settings = get_settings()
    text_size = settings.get("text_size", 18)

    # Set global font scale
    default_font_size = 18
    font_scale = text_size / default_font_size
    dpg.set_global_font_scale(font_scale)

    # Create and apply custom theme with colors
    text_color = settings.get("text_color", "#FFFFFF")
    primary_bg_color = settings.get("primary_bg_color", "#1E1E1E")
    secondary_color = settings.get("secondary_color", "#007ACC")

    # Create theme
    with dpg.theme(tag="custom_theme"):
        with dpg.theme_component(dpg.mvThemeCat_Core):
            dpg.add_theme_color(dpg.mvThemeCol_Text, text_color)
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, primary_bg_color)
            dpg.add_theme_color(dpg.mvThemeCol_Button, secondary_color)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, secondary_color)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, secondary_color)
            dpg.add_theme_color(dpg.mvThemeCol_Tab, secondary_color)
            dpg.add_theme_color(dpg.mvThemeCol_TabHovered, secondary_color)
            dpg.add_theme_color(dpg.mvThemeCol_TabActive, secondary_color)

    # Apply the theme
    dpg.bind_theme("custom_theme")

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
                    default_value=settings.get("text_size", 18),
                    min_value=1,
                    max_value=100,
                    tag="text_size_slider",
                )
                dpg.add_color_edit(
                    label="Text Color",
                    default_value=settings.get("text_color", "#FFFFFF"),
                    tag="text_color_picker",
                    no_alpha=True,
                )
                dpg.add_color_edit(
                    label="Primary Background Color",
                    default_value=settings.get("primary_bg_color", "#1E1E1E"),
                    tag="primary_bg_color_picker",
                    no_alpha=True,
                )
                dpg.add_color_edit(
                    label="Secondary Color (Buttons/Tabs)",
                    default_value=settings.get("secondary_color", "#007ACC"),
                    tag="secondary_color_picker",
                    no_alpha=True,
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
    text_color = dpg.get_value("text_color_picker")
    primary_bg_color = dpg.get_value("primary_bg_color_picker")
    secondary_color = dpg.get_value("secondary_color_picker")
    animations = dpg.get_value("animations_checkbox")

    # Convert colors to hex format
    text_color_hex = f"#{int(text_color[0]*255):02X}{int(text_color[1]*255):02X}{int(text_color[2]*255):02X}"
    primary_bg_color_hex = f"#{int(primary_bg_color[0]*255):02X}{int(primary_bg_color[1]*255):02X}{int(primary_bg_color[2]*255):02X}"
    secondary_color_hex = f"#{int(secondary_color[0]*255):02X}{int(secondary_color[1]*255):02X}{int(secondary_color[2]*255):02X}"

    # Update settings
    settings.set("text_size", text_size)
    settings.set("text_color", text_color_hex)
    settings.set("primary_bg_color", primary_bg_color_hex)
    settings.set("secondary_color", secondary_color_hex)
    settings.set("enable_animations", animations)
    settings.save()

    # Apply text size immediately
    font_scale = text_size / 18
    dpg.set_global_font_scale(font_scale)

    # Update theme colors immediately
    # Clear existing theme and create new one
    dpg.clear_theme("custom_theme")
    
    # Create new theme with updated colors
    with dpg.theme(tag="custom_theme"):
        with dpg.theme_component(dpg.mvThemeCat_Core):
            dpg.add_theme_color(dpg.mvThemeCol_Text, text_color)
            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, primary_bg_color)
            dpg.add_theme_color(dpg.mvThemeCol_Button, secondary_color)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, secondary_color)
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, secondary_color)
            dpg.add_theme_color(dpg.mvThemeCol_Tab, secondary_color)
            dpg.add_theme_color(dpg.mvThemeCol_TabHovered, secondary_color)
            dpg.add_theme_color(dpg.mvThemeCol_TabActive, secondary_color)

    # Rebind the theme
    dpg.bind_theme("custom_theme")

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
