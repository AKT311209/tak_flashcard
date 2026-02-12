"""Main DearPyGui application."""

import dearpygui.dearpygui as dpg
from tak_flashcard.config import DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT
from tak_flashcard.features.settings import SettingsController
from tak_flashcard.gui.fonts import apply_font_from_appearance, bind_font_from_metadata
from tak_flashcard.gui.views.home_view import show_home_view


class Application:
    """Main application class managing DearPyGui windows and navigation."""

    def __init__(self):
        """Initialize the application."""
        self.settings_controller = SettingsController()
        self.current_view = None
        self.window_width = DEFAULT_WINDOW_WIDTH
        self.window_height = DEFAULT_WINDOW_HEIGHT

    def setup(self):
        """Set up DearPyGui context and configuration."""
        dpg.create_context()

        appearance = self.settings_controller.get_appearance_settings()
        self.window_width = appearance.get(
            'window_width', DEFAULT_WINDOW_WIDTH)
        self.window_height = appearance.get(
            'window_height', DEFAULT_WINDOW_HEIGHT)

        self._setup_theme()

        # load and bind a font that supports unicode characters (Vietnamese/IPA)
        # so vocabulary text renders correctly.
        try:
            # register font so it's present in the font atlas; bind after setup
            self._registered_font = apply_font_from_appearance(appearance)
        except Exception:
            # don't block startup if font loading fails; default font will be used
            pass

        dpg.create_viewport(
            title="Tak Flashcard",
            width=self.window_width,
            height=self.window_height,
            min_width=640,
            min_height=480,
            resizable=True
        )

    def _setup_theme(self):
        """Set up application theme."""
        appearance = self.settings_controller.get_appearance_settings()
        theme_name = appearance.get('theme', 'light')

        if theme_name == 'dark':
            self._apply_dark_theme()
        else:
            self._apply_light_theme()

    def _apply_light_theme(self):
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

                dpg.add_theme_color(dpg.mvThemeCol_WindowBg,
                                    (240, 240, 240, 255))
                dpg.add_theme_color(dpg.mvThemeCol_ChildBg,
                                    (250, 250, 250, 255))
                dpg.add_theme_color(dpg.mvThemeCol_Text, (0, 0, 0, 255))
                dpg.add_theme_color(dpg.mvThemeCol_Button,
                                    (100, 150, 255, 255))
                dpg.add_theme_color(
                    dpg.mvThemeCol_ButtonHovered, (120, 170, 255, 255))
                dpg.add_theme_color(
                    dpg.mvThemeCol_ButtonActive, (80, 130, 235, 255))
                dpg.add_theme_color(dpg.mvThemeCol_FrameBg,
                                    (255, 255, 255, 255))
                dpg.add_theme_color(
                    dpg.mvThemeCol_FrameBgHovered, (245, 245, 245, 255))
                dpg.add_theme_color(
                    dpg.mvThemeCol_FrameBgActive, (235, 235, 235, 255))
                dpg.add_theme_color(dpg.mvThemeCol_TitleBg,
                                    (220, 220, 220, 255))
                dpg.add_theme_color(
                    dpg.mvThemeCol_TitleBgActive, (200, 200, 200, 255))
                dpg.add_theme_color(dpg.mvThemeCol_Header, (100, 150, 255, 80))
                dpg.add_theme_color(
                    dpg.mvThemeCol_HeaderHovered, (100, 150, 255, 120))
                dpg.add_theme_color(
                    dpg.mvThemeCol_HeaderActive, (100, 150, 255, 160))
        dpg.bind_theme(light_theme)

    def _apply_dark_theme(self):
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
                dpg.add_theme_color(
                    dpg.mvThemeCol_HeaderActive, (60, 100, 180, 160))
        dpg.bind_theme(dark_theme)

    # font loading is handled by tak_flashcard.gui.fonts.apply_font_from_appearance

    def run(self):
        """Run the application."""
        dpg.setup_dearpygui()
        # bind registered font after DearPyGui setup so it takes effect
        try:
            if getattr(self, "_registered_font", None):
                bind_font_from_metadata(self._registered_font)
        except Exception:
            pass
        dpg.show_viewport()

        show_home_view()

        dpg.start_dearpygui()
        dpg.destroy_context()


def create_app() -> Application:
    """
    Create and return application instance.

    Returns:
        Application instance
    """
    return Application()
