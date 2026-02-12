"""Toolbar component with navigation buttons."""

import dearpygui.dearpygui as dpg
from typing import Callable, Optional


def create_toolbar(
    on_back: Optional[Callable] = None,
    on_home: Optional[Callable] = None,
    show_back: bool = True,
    show_home: bool = True
):
    """
    Create a toolbar with navigation buttons.

    Args:
        on_back: Callback for back button
        on_home: Callback for home button
        show_back: Whether to show back button
        show_home: Whether to show home button
    """
    with dpg.group(horizontal=True):
        if show_back and on_back:
            dpg.add_button(label="← Back", callback=on_back, width=100)

        if show_home and on_home:
            dpg.add_button(label="Home", callback=on_home, width=100)

        dpg.add_spacer(width=10)
