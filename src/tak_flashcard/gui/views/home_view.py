"""Home view - main menu."""

import dearpygui.dearpygui as dpg


def show_home_view():
    """Display the home view."""
    if dpg.does_item_exist("home_window"):
        dpg.delete_item("home_window")

    with dpg.window(
        tag="home_window",
        label="Tak Flashcard - Home",
        no_close=True,
        no_collapse=True,
        no_title_bar=True,
        no_move=True,
        no_resize=True,
        pos=(0, 0)
    ):
        dpg.set_primary_window("home_window", True)

        viewport_width = dpg.get_viewport_width()
        viewport_height = dpg.get_viewport_height()

        dpg.add_spacer(height=viewport_height // 4)

        with dpg.group(horizontal=True):
            dpg.add_spacer(width=max(50, (viewport_width - 600) // 2))
            with dpg.group():
                dpg.add_text(
                    "TAK FLASHCARD",
                    color=(100, 150, 255)
                )

        dpg.add_spacer(height=10)

        with dpg.group(horizontal=True):
            dpg.add_spacer(width=max(50, (viewport_width - 600) // 2))
            with dpg.group():
                dpg.add_text(
                    "English-Vietnamese Vocabulary Learning",
                    color=(150, 150, 150)
                )

        dpg.add_spacer(height=40)

        def _show_flashcard():
            from tak_flashcard.gui.views.flashcard_view import show_flashcard_config_view
            show_flashcard_config_view()

        def _show_dictionary():
            from tak_flashcard.gui.views.dictionary_view import show_dictionary_view
            show_dictionary_view()

        def _show_guide():
            from tak_flashcard.gui.views.guide_view import show_guide_view
            show_guide_view()

        def _show_settings():
            from tak_flashcard.gui.views.settings_view import show_settings_view
            show_settings_view()

        with dpg.group(horizontal=True):
            dpg.add_spacer(width=max(50, (viewport_width - 400) // 2))
            with dpg.group():
                dpg.add_button(
                    label="Flashcard",
                    width=300,
                    height=50,
                    callback=_show_flashcard
                )
                dpg.add_spacer(height=15)

                dpg.add_button(
                    label="Dictionary",
                    width=300,
                    height=50,
                    callback=_show_dictionary
                )
                dpg.add_spacer(height=15)

                dpg.add_button(
                    label="Guide",
                    width=300,
                    height=50,
                    callback=_show_guide
                )
                dpg.add_spacer(height=15)

                dpg.add_button(
                    label="Settings",
                    width=300,
                    height=50,
                    callback=_show_settings
                )
                dpg.add_spacer(height=15)

                dpg.add_button(
                    label="Exit",
                    width=300,
                    height=50,
                    callback=lambda: dpg.stop_dearpygui()
                )

        dpg.add_spacer(height=30)

        with dpg.group(horizontal=True):
            dpg.add_spacer(width=max(50, (viewport_width - 100) // 2))
            dpg.add_text(
                "v1.0.0",
                color=(100, 100, 100)
            )
