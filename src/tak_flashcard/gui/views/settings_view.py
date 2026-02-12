"""Settings view for configuring application preferences."""

import dearpygui.dearpygui as dpg
from tak_flashcard.gui.components.toolbar import create_toolbar
from tak_flashcard.features.settings import SettingsController
from tak_flashcard.config import (
    DEFAULT_DIFFICULTY, DEFAULT_QUESTION_COUNT, DEFAULT_TIME_LIMIT,
    DEFAULT_WINDOW_HEIGHT, DEFAULT_WINDOW_WIDTH
)
from tak_flashcard.constants import Theme, FontSize, FlashcardMode, AnimationSpeed
from tak_flashcard.gui.fonts import (
    apply_font_from_appearance,
    bind_font_from_metadata,
    discover_system_fonts,
)


settings_controller = None


def _safe_int(value, fallback):
    """Return the integer value or fallback when conversion fails."""
    if value is None:
        return fallback
    try:
        return int(value)
    except (TypeError, ValueError):
        return fallback


def _get_settings_controller() -> SettingsController:
    """Ensure a settings controller instance is available."""
    global settings_controller
    if settings_controller is None:
        settings_controller = SettingsController()
    return settings_controller


def show_settings_view():
    """Display the settings view."""
    global settings_controller

    # show settings as a modal popup rather than replacing the main window
    if dpg.does_item_exist("settings_window"):
        dpg.delete_item("settings_window")

    settings_controller = SettingsController()

    viewport_width = dpg.get_viewport_width()
    viewport_height = dpg.get_viewport_height()

    dialog_width = min(900, viewport_width - 80)
    dialog_height = min(800, viewport_height - 80)
    pos_x = (viewport_width - dialog_width) // 2
    pos_y = (viewport_height - dialog_height) // 2

    with dpg.window(
        tag="settings_window",
        label="Settings",
        width=dialog_width,
        height=dialog_height,
        pos=(pos_x, pos_y),
        modal=True,
        no_resize=True
    ):
        create_toolbar(on_back=None, on_home=_back_to_home, show_back=False)
        dpg.add_separator()
        dpg.add_spacer(height=10)

        with dpg.child_window(border=True, height=580):
            _create_appearance_section()
            dpg.add_spacer(height=20)
            dpg.add_separator()
            dpg.add_spacer(height=20)

            _create_defaults_section()
            dpg.add_spacer(height=20)
            dpg.add_separator()
            dpg.add_spacer(height=20)

            _create_preferences_section()

        dpg.add_spacer(height=10)

        with dpg.group(horizontal=True):
            dpg.add_spacer(width=100)
            dpg.add_button(
                label="Save & Apply",
                width=150,
                height=40,
                callback=_save_settings
            )
            dpg.add_spacer(width=20)
            dpg.add_button(
                label="Reset to Default",
                width=150,
                height=40,
                callback=_reset_settings
            )
            dpg.add_spacer(width=20)
            dpg.add_button(
                label="Cancel",
                width=150,
                height=40,
                callback=_back_to_home
            )


def _create_appearance_section():
    """Create appearance settings section."""
    dpg.add_text("APPEARANCE", color=(100, 200, 255))
    dpg.add_spacer(height=10)

    controller = _get_settings_controller()
    appearance = controller.get_appearance_settings() or {}

    with dpg.group(horizontal=True):
        dpg.add_text("Theme:")
        dpg.add_spacer(width=80)
        dpg.add_combo(
            tag="theme_combo",
            items=[t.value.title() for t in Theme],
            default_value=appearance.get('theme', 'light').title(),
            width=200
        )
    dpg.add_spacer(height=10)

    with dpg.group(horizontal=True):
        dpg.add_text("Font Size:")
        dpg.add_spacer(width=65)
        dpg.add_combo(
            tag="font_size_combo",
            items=[f.value.title() for f in FontSize],
            default_value=appearance.get('font_size', 'medium').title(),
            width=200
        )
    dpg.add_spacer(height=10)

    # Font selection (font file) and pixel size
    fonts = discover_system_fonts()
    font_items = list(fonts.keys())
    default_font_display = None
    if appearance.get('font_path'):
        # find matching display name if available
        for disp, path in fonts.items():
            if path == appearance.get('font_path'):
                default_font_display = disp
                break

    with dpg.group(horizontal=True):
        dpg.add_text("Font:")
        dpg.add_spacer(width=115)
        dpg.add_combo(
            tag="font_combo",
            items=font_items if font_items else ["(system default)"],
            default_value=default_font_display or (
                font_items[0] if font_items else "(system default)"),
            width=400
        )
    dpg.add_spacer(height=10)

    with dpg.group(horizontal=True):
        dpg.add_text("Font Pixel Size:")
        dpg.add_spacer(width=25)
        dpg.add_input_int(
            tag="font_pixel_size_input",
            default_value=_safe_int(appearance.get('font_pixel_size'), 16),
            min_value=8,
            max_value=72,
            min_clamped=True,
            max_clamped=True,
            width=100
        )

    with dpg.group(horizontal=True):
        dpg.add_text("Window Width:")
        dpg.add_spacer(width=35)
        dpg.add_input_int(
            tag="window_width_input",
            default_value=_safe_int(appearance.get('window_width'),
                                    DEFAULT_WINDOW_WIDTH),
            min_value=640,
            max_value=1920,
            min_clamped=True,
            max_clamped=True,
            width=200
        )
    dpg.add_spacer(height=10)

    with dpg.group(horizontal=True):
        dpg.add_text("Window Height:")
        dpg.add_spacer(width=30)
        dpg.add_input_int(
            tag="window_height_input",
            default_value=_safe_int(appearance.get('window_height'),
                                    DEFAULT_WINDOW_HEIGHT),
            min_value=480,
            max_value=1080,
            min_clamped=True,
            max_clamped=True,
            width=200
        )


def _create_defaults_section():
    """Create default settings section."""
    dpg.add_text("DEFAULT SETTINGS", color=(100, 200, 255))
    dpg.add_spacer(height=10)

    controller = _get_settings_controller()
    defaults = controller.get_default_settings() or {}

    difficulty_default = _safe_int(
        defaults.get('difficulty_level'), DEFAULT_DIFFICULTY)

    question_count_default = _safe_int(
        defaults.get('question_count'), DEFAULT_QUESTION_COUNT)

    time_limit_default = _safe_int(
        defaults.get('time_limit'), DEFAULT_TIME_LIMIT)

    with dpg.group(horizontal=True):
        dpg.add_text("Default Mode:")
        dpg.add_spacer(width=35)
        dpg.add_combo(
            tag="default_mode_combo",
            items=[m.value.title() for m in FlashcardMode],
            default_value=defaults.get('flashcard_mode', 'endless').title(),
            width=200
        )
    dpg.add_spacer(height=10)

    with dpg.group(horizontal=True):
        dpg.add_text("Default Difficulty:")
        dpg.add_spacer(width=5)
        dpg.add_slider_int(
            tag="default_difficulty_slider",
            default_value=difficulty_default,
            min_value=1,
            max_value=5,
            width=200
        )
    dpg.add_spacer(height=10)

    with dpg.group(horizontal=True):
        dpg.add_text("Question Count:")
        dpg.add_spacer(width=25)
        dpg.add_input_int(
            tag="question_count_input",
            default_value=question_count_default,
            min_value=10,
            max_value=100,
            min_clamped=True,
            max_clamped=True,
            width=200
        )
    dpg.add_spacer(height=10)

    with dpg.group(horizontal=True):
        dpg.add_text("Time Limit (seconds):")
        dpg.add_spacer(width=5)
        dpg.add_input_int(
            tag="time_limit_input",
            default_value=time_limit_default,
            min_value=60,
            max_value=600,
            min_clamped=True,
            max_clamped=True,
            width=200
        )


def _create_preferences_section():
    """Create preferences section."""
    dpg.add_text("PREFERENCES", color=(100, 200, 255))
    dpg.add_spacer(height=10)

    controller = _get_settings_controller()
    preferences = controller.get_preferences() or {}

    with dpg.group(horizontal=True):
        dpg.add_text("Sound Effects:")
        dpg.add_spacer(width=40)
        dpg.add_checkbox(
            tag="sound_enabled_checkbox",
            default_value=preferences.get('sound_enabled', False)
        )
    dpg.add_spacer(height=10)

    with dpg.group(horizontal=True):
        dpg.add_text("Animation Speed:")
        dpg.add_spacer(width=15)
        dpg.add_combo(
            tag="animation_speed_combo",
            items=[a.value.title() for a in AnimationSpeed],
            default_value=preferences.get('animation_speed', 'normal').title(),
            width=200
        )


def _apply_appearance_settings():
    """Apply appearance settings immediately."""
    try:
        controller = _get_settings_controller()
        appearance = controller.get_appearance_settings() or {}

        theme = appearance.get('theme', 'light')
        if theme == 'dark':
            _apply_dark_theme()
        else:
            _apply_light_theme()

        window_width = appearance.get('window_width', 800)
        window_height = appearance.get('window_height', 600)
        dpg.configure_viewport("__dearpygui_viewport",
                               width=window_width,
                               height=window_height)
    except Exception:
        pass


def _apply_light_theme():
    """Apply light theme colors."""
    with dpg.theme() as light_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_style(
                dpg.mvStyleVar_FrameRounding, 5, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(
                dpg.mvStyleVar_WindowRounding, 5, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(
                dpg.mvStyleVar_ChildRounding, 5, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding,
                                8, 6, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing,
                                8, 8, category=dpg.mvThemeCat_Core)

            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (240, 240, 240, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (250, 250, 250, 255))
            dpg.add_theme_color(dpg.mvThemeCol_Text, (0, 0, 0, 255))
            dpg.add_theme_color(dpg.mvThemeCol_Button, (100, 150, 255, 255))
            dpg.add_theme_color(
                dpg.mvThemeCol_ButtonHovered, (120, 170, 255, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive,
                                (80, 130, 235, 255))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (255, 255, 255, 255))
            dpg.add_theme_color(
                dpg.mvThemeCol_FrameBgHovered, (245, 245, 245, 255))
            dpg.add_theme_color(
                dpg.mvThemeCol_FrameBgActive, (235, 235, 235, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TitleBg, (220, 220, 220, 255))
            dpg.add_theme_color(
                dpg.mvThemeCol_TitleBgActive, (200, 200, 200, 255))
            dpg.add_theme_color(dpg.mvThemeCol_Header, (100, 150, 255, 80))
            dpg.add_theme_color(
                dpg.mvThemeCol_HeaderHovered, (100, 150, 255, 120))
            dpg.add_theme_color(dpg.mvThemeCol_HeaderActive,
                                (100, 150, 255, 160))
    dpg.bind_theme(light_theme)


def _apply_dark_theme():
    """Apply dark theme colors."""
    with dpg.theme() as dark_theme:
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_style(
                dpg.mvStyleVar_FrameRounding, 5, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(
                dpg.mvStyleVar_WindowRounding, 5, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(
                dpg.mvStyleVar_ChildRounding, 5, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding,
                                8, 6, category=dpg.mvThemeCat_Core)
            dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing,
                                8, 8, category=dpg.mvThemeCat_Core)

            dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (25, 25, 35, 255))
            dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (35, 35, 45, 255))
            dpg.add_theme_color(dpg.mvThemeCol_Text, (255, 255, 255, 255))
            dpg.add_theme_color(dpg.mvThemeCol_Button, (60, 100, 180, 255))
            dpg.add_theme_color(
                dpg.mvThemeCol_ButtonHovered, (80, 120, 200, 255))
            dpg.add_theme_color(
                dpg.mvThemeCol_ButtonActive, (50, 90, 160, 255))
            dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (45, 45, 55, 255))
            dpg.add_theme_color(
                dpg.mvThemeCol_FrameBgHovered, (55, 55, 65, 255))
            dpg.add_theme_color(
                dpg.mvThemeCol_FrameBgActive, (65, 65, 75, 255))
            dpg.add_theme_color(dpg.mvThemeCol_TitleBg, (40, 40, 50, 255))
            dpg.add_theme_color(
                dpg.mvThemeCol_TitleBgActive, (50, 50, 60, 255))
            dpg.add_theme_color(dpg.mvThemeCol_Header, (60, 100, 180, 80))
            dpg.add_theme_color(
                dpg.mvThemeCol_HeaderHovered, (60, 100, 180, 120))
            dpg.add_theme_color(dpg.mvThemeCol_HeaderActive,
                                (60, 100, 180, 160))
    dpg.bind_theme(dark_theme)


def _save_settings():
    """Save all settings."""
    controller = _get_settings_controller()
    controller.update_setting(
        'appearance', 'theme', dpg.get_value("theme_combo").lower())
    controller.update_setting(
        'appearance', 'font_size', dpg.get_value("font_size_combo").lower())
    # resolve font selection display -> path
    fonts = discover_system_fonts()
    selected_font_display = dpg.get_value("font_combo")
    font_path = None
    if selected_font_display and selected_font_display in fonts:
        font_path = fonts[selected_font_display]
    controller.update_setting(
        'appearance', 'font_path', font_path)
    controller.update_setting(
        'appearance', 'font_pixel_size', dpg.get_value("font_pixel_size_input"))
    controller.update_setting(
        'appearance', 'window_width', dpg.get_value("window_width_input"))
    controller.update_setting(
        'appearance', 'window_height', dpg.get_value("window_height_input"))

    controller.update_setting(
        'defaults', 'flashcard_mode', dpg.get_value("default_mode_combo").lower())
    controller.update_setting(
        'defaults', 'difficulty_level', dpg.get_value("default_difficulty_slider"))
    controller.update_setting(
        'defaults', 'question_count', dpg.get_value("question_count_input"))
    controller.update_setting(
        'defaults', 'time_limit', dpg.get_value("time_limit_input"))

    controller.update_setting(
        'preferences', 'sound_enabled', dpg.get_value("sound_enabled_checkbox"))
    controller.update_setting(
        'preferences', 'animation_speed', dpg.get_value("animation_speed_combo").lower())

    success, message = controller.apply_changes()

    if success:
        _apply_appearance_settings()
        # apply font immediately as well
        try:
            font_meta = apply_font_from_appearance(
                controller.get_appearance_settings())
            if font_meta:
                bind_font_from_metadata(font_meta)
        except Exception:
            pass
        _show_message(
            "Settings saved and applied successfully!")
    else:
        _show_message(f"Failed to save settings: {message}")


def _reset_settings():
    """Reset settings to defaults."""
    controller = _get_settings_controller()
    success, message = controller.reset_to_defaults()

    if success:
        _show_message("Settings reset to defaults!")
        if dpg.does_item_exist("settings_window"):
            dpg.delete_item("settings_window")
        show_settings_view()
    else:
        _show_message(f"Failed to reset settings: {message}")


def _show_message(message: str):
    """Show a message dialog."""
    if dpg.does_item_exist("message_window"):
        dpg.delete_item("message_window")

    viewport_width = dpg.get_viewport_width()
    viewport_height = dpg.get_viewport_height()

    dialog_width = 400
    dialog_height = 150
    pos_x = (viewport_width - dialog_width) // 2
    pos_y = (viewport_height - dialog_height) // 2

    with dpg.window(
        tag="message_window",
        label="Message",
        width=dialog_width,
        height=dialog_height,
        pos=(pos_x, pos_y),
        modal=True,
        no_move=True,
        no_resize=True
    ):
        dpg.add_spacer(height=20)
        dpg.add_text(message, wrap=350, indent=20)
        dpg.add_spacer(height=20)
        try:
            controller = _get_settings_controller()
            meta = apply_font_from_appearance(
                controller.get_appearance_settings())
            if meta:
                bind_font_from_metadata(meta)
        except Exception:
            pass
        with dpg.group(horizontal=True):
            dpg.add_spacer(width=150)
            dpg.add_button(
                label="OK",
                width=100,
                callback=lambda: dpg.delete_item("message_window")
            )


def _back_to_home():
    """Return to home view."""
    global settings_controller

    settings_controller = None

    if dpg.does_item_exist("settings_window"):
        dpg.delete_item("settings_window")

    from tak_flashcard.gui.views.home_view import show_home_view
    show_home_view()
