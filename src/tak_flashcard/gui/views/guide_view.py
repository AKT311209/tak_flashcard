"""Guide view displaying user manual."""

import dearpygui.dearpygui as dpg
from tak_flashcard.gui.components.toolbar import create_toolbar
from tak_flashcard.features.guide import GuideController


def show_guide_view():
    """Display the guide view."""
    # present the guide as a modal popup over the main window
    if dpg.does_item_exist("guide_window"):
        dpg.delete_item("guide_window")

    guide_controller = GuideController()
    content = guide_controller.get_content()

    viewport_width = dpg.get_viewport_width()
    viewport_height = dpg.get_viewport_height()

    dialog_width = min(800, viewport_width - 80)
    dialog_height = min(700, viewport_height - 80)
    pos_x = (viewport_width - dialog_width) // 2
    pos_y = (viewport_height - dialog_height) // 2

    with dpg.window(
        tag="guide_window",
        label="User Guide",
        width=dialog_width,
        height=dialog_height,
        pos=(pos_x, pos_y),
        modal=True,
        no_resize=True
    ):
        create_toolbar(on_back=None, on_home=_back_to_home, show_back=False)
        dpg.add_separator()
        dpg.add_spacer(height=10)

        with dpg.child_window(border=True, height=620):
            dpg.add_text(content, wrap=750)


def _back_to_home():
    """Return to home view."""
    if dpg.does_item_exist("guide_window"):
        dpg.delete_item("guide_window")

    from tak_flashcard.gui.views.home_view import show_home_view
    show_home_view()
