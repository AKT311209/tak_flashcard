"""Results view for flashcard sessions."""

import dearpygui.dearpygui as dpg
from tak_flashcard.gui.components.toolbar import create_toolbar
from tak_flashcard.constants import FlashcardMode


def show_results_view(stats: dict, mode: FlashcardMode):
    """
    Display session results.

    Args:
        stats: Statistics dictionary
        mode: Flashcard mode that was used
    """
    if dpg.does_item_exist("results_window"):
        dpg.delete_item("results_window")

    def _go_home():
        from tak_flashcard.gui.views.home_view import show_home_view
        if dpg.does_item_exist("results_window"):
            dpg.delete_item("results_window")
        show_home_view()

    # center the popup on the viewport and make it a modal window
    viewport_width = dpg.get_viewport_width()
    viewport_height = dpg.get_viewport_height()
    dialog_width = 600
    dialog_height = 420
    pos_x = (viewport_width - dialog_width) // 2
    pos_y = (viewport_height - dialog_height) // 2

    with dpg.window(
        tag="results_window",
        label="Session Results",
        width=dialog_width,
        height=dialog_height,
        pos=(pos_x, pos_y),
        modal=True,
        no_resize=True
    ):
        create_toolbar(on_back=None, on_home=_go_home, show_back=False)
        dpg.add_separator()
        dpg.add_spacer(height=30)

        dpg.add_text("Session Complete!", color=(100, 255, 100))
        dpg.add_spacer(height=30)

        with dpg.child_window(height=250, border=True):
            dpg.add_spacer(height=20)

            dpg.add_text(f"Final Score: {stats['score']}", indent=100)
            dpg.add_spacer(height=15)

            dpg.add_text(f"Questions Answered: {stats['total']}", indent=100)
            dpg.add_spacer(height=15)

            dpg.add_text(
                f"Correct Answers: {stats['correct']}", indent=100, color=(100, 255, 100))
            dpg.add_spacer(height=15)

            incorrect = stats['total'] - stats['correct']
            dpg.add_text(
                f"Incorrect Answers: {incorrect}", indent=100, color=(255, 100, 100))
            dpg.add_spacer(height=15)

            dpg.add_text(
                f"Accuracy: {stats['accuracy']:.1f}%", indent=100, color=(100, 200, 255))
            dpg.add_spacer(height=20)

            if stats['accuracy'] >= 90:
                message = "Excellent work!"
            elif stats['accuracy'] >= 70:
                message = "Great job!"
            elif stats['accuracy'] >= 50:
                message = "Good effort! Keep practicing!"
            else:
                message = "Keep learning! You'll improve!"

            dpg.add_text(message, indent=150, color=(255, 200, 100))

        dpg.add_spacer(height=30)

        def _click_home():
            from tak_flashcard.gui.views.home_view import show_home_view
            if dpg.does_item_exist("results_window"):
                dpg.delete_item("results_window")
            show_home_view()

        with dpg.group(horizontal=True):
            dpg.add_spacer(width=150)
            dpg.add_button(
                label="Back to Home",
                width=150,
                height=40,
                callback=_click_home
            )
