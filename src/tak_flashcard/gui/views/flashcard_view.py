"""Flashcard view - configuration and session."""

import dearpygui.dearpygui as dpg
import threading
from tak_flashcard.gui.components.toolbar import create_toolbar
from tak_flashcard.gui.components.option_panels import FlashcardOptionsPanel
from tak_flashcard.gui.views.results_view import show_results_view
from tak_flashcard.features.flashcard import FlashcardController, FlashcardState
from tak_flashcard.constants import FlashcardMode


current_controller = None
timer_thread = None
stop_timer = False


def show_flashcard_config_view():
    """Display flashcard configuration view."""
    # present flashcard configuration as a modal popup over the main window
    if dpg.does_item_exist("flashcard_config_window"):
        dpg.delete_item("flashcard_config_window")

    def _go_home():
        from tak_flashcard.gui.views.home_view import show_home_view
        if dpg.does_item_exist("flashcard_config_window"):
            dpg.delete_item("flashcard_config_window")
        show_home_view()

    viewport_width = dpg.get_viewport_width()
    viewport_height = dpg.get_viewport_height()

    dialog_width = min(800, viewport_width - 100)
    dialog_height = min(640, viewport_height - 120)
    pos_x = (viewport_width - dialog_width) // 2
    pos_y = (viewport_height - dialog_height) // 2

    with dpg.window(
        tag="flashcard_config_window",
        label="Flashcard Configuration",
        width=dialog_width,
        height=dialog_height,
        pos=(pos_x, pos_y),
        modal=True,
        no_resize=True
    ):
        create_toolbar(on_back=None, on_home=_go_home, show_back=False)
        dpg.add_separator()
        dpg.add_spacer(height=10)

        options_panel = FlashcardOptionsPanel("flashcard_config_window")
        options_panel.create()

        dpg.add_spacer(height=20)

        with dpg.group(horizontal=True):
            dpg.add_spacer(width=200)
            dpg.add_button(
                label="Start Session",
                width=200,
                height=40,
                callback=lambda: _start_flashcard_session(
                    options_panel.get_config())
            )


def _start_flashcard_session(config: dict):
    """Start a flashcard session with the given configuration."""
    global current_controller

    current_controller = FlashcardController(
        mode=config['mode'],
        direction=config['direction'],
        difficulty=config['difficulty'],
        question_count=config['question_count'],
        time_limit=config['time_limit'],
        enable_show_answer=config['enable_show_answer'],
        penalty_type=config['penalty_type']
    )

    current_controller.start_session()
    show_flashcard_session_view()


def show_flashcard_session_view():
    """Display the active flashcard session view."""
    global stop_timer, timer_thread

    if dpg.does_item_exist("flashcard_config_window"):
        dpg.delete_item("flashcard_config_window")

    if dpg.does_item_exist("flashcard_session_window"):
        dpg.delete_item("flashcard_session_window")

    viewport_width = dpg.get_viewport_width()
    viewport_height = dpg.get_viewport_height()

    dialog_width = min(900, viewport_width - 80)
    dialog_height = min(700, viewport_height - 80)
    pos_x = (viewport_width - dialog_width) // 2
    pos_y = (viewport_height - dialog_height) // 2

    with dpg.window(
        tag="flashcard_session_window",
        label="Flashcard Session",
        width=dialog_width,
        height=dialog_height,
        pos=(pos_x, pos_y),
        modal=False,
        no_resize=True
    ):
        create_toolbar(
            on_back=lambda: _end_session_early(),
            on_home=None,
            show_home=False
        )
        dpg.add_separator()
        dpg.add_spacer(height=10)

        state = current_controller.get_current_state()

        with dpg.group(horizontal=True):
            dpg.add_text("Score: ", color=(100, 200, 255))
            dpg.add_text("0", tag="score_text")
            dpg.add_spacer(width=30)

            if state['mode'] == FlashcardMode.TESTING:
                dpg.add_text("Progress: ", color=(100, 200, 255))
                dpg.add_text("0/0", tag="progress_text")
            elif state['mode'] == FlashcardMode.SPEED:
                dpg.add_text("Time: ", color=(255, 100, 100))
                dpg.add_text("0:00", tag="timer_text")

        dpg.add_spacer(height=30)

        with dpg.child_window(height=200, border=True):
            dpg.add_spacer(height=40)
            dpg.add_text("", tag="question_text", wrap=600)
            dpg.add_spacer(height=10)
            dpg.add_text("", tag="pronunciation_text", color=(150, 150, 150))
            dpg.add_text("", tag="pos_text", color=(150, 150, 150))

        dpg.add_spacer(height=20)

        dpg.add_text("Your Answer:")
        dpg.add_input_text(
            tag="answer_input",
            width=600,
            on_enter=True,
            callback=lambda s, a: _submit_answer()
        )

        dpg.add_spacer(height=20)

        with dpg.group(horizontal=True):
            dpg.add_spacer(width=100)
            dpg.add_button(
                label="Submit Answer",
                width=150,
                height=40,
                tag="submit_button",
                callback=lambda: _submit_answer()
            )
            dpg.add_spacer(width=20)
            dpg.add_button(
                label="Show Answer",
                width=150,
                height=40,
                tag="show_answer_button",
                callback=lambda: _show_answer()
            )
            dpg.add_spacer(width=20)
            dpg.add_button(
                label="Next Question",
                width=150,
                height=40,
                tag="next_button",
                show=False,
                callback=lambda: _next_question()
            )

        dpg.add_spacer(height=20)
        dpg.add_text("", tag="result_text", wrap=600)

    _update_question_display()

    if current_controller.mode == FlashcardMode.SPEED:
        stop_timer = False
        timer_thread = threading.Thread(target=_update_timer, daemon=True)
        timer_thread.start()


def _update_timer():
    """Update timer display in a separate thread."""
    global stop_timer

    import time
    while not stop_timer and current_controller.timer:
        remaining = current_controller.timer.get_remaining()

        if remaining <= 0:
            dpg.set_value("timer_text", "0:00")
            _end_session()
            break

        minutes = int(remaining // 60)
        seconds = int(remaining % 60)
        dpg.set_value("timer_text", f"{minutes}:{seconds:02d}")

        time.sleep(0.1)


def _update_question_display():
    """Update the question display."""
    state = current_controller.get_current_state()

    if state['state'] == FlashcardState.COMPLETED:
        _end_session()
        return

    dpg.set_value("question_text", f"     {state['question']}")

    if 'word_info' in state:
        dpg.set_value("pronunciation_text",
                      f"     /{state['word_info']['pronunciation']}/")
        dpg.set_value(
            "pos_text", f"     ({state['word_info']['part_of_speech']})")

    stats = state['statistics']
    dpg.set_value("score_text", str(stats['score']))

    if state['mode'] == FlashcardMode.TESTING:
        progress = state.get('question_progress', '0/0')
        dpg.set_value("progress_text", progress)

    can_show = state.get('can_show_answer', False)
    dpg.configure_item("show_answer_button", show=can_show)

    dpg.set_value("answer_input", "")
    dpg.set_value("result_text", "")
    dpg.configure_item("next_button", show=False)
    dpg.configure_item("submit_button", show=True)
    dpg.configure_item("answer_input", enabled=True)


def _submit_answer():
    """Submit the user's answer."""
    answer = dpg.get_value("answer_input")

    if not answer or answer.strip() == "":
        dpg.set_value("result_text", "Please enter an answer!")
        return

    result = current_controller.submit_answer(answer)

    if result['is_correct']:
        dpg.set_value(
            "result_text", f"✓ Correct! (+{result['points']} points)")
        dpg.configure_item("result_text", color=(100, 255, 100))
    else:
        dpg.set_value(
            "result_text", f"✗ Incorrect. The correct answer is: {result['correct_answer']}")
        dpg.configure_item("result_text", color=(255, 100, 100))

    stats = result['statistics']
    dpg.set_value("score_text", str(stats['score']))

    dpg.configure_item("submit_button", show=False)
    dpg.configure_item("next_button", show=True)
    dpg.configure_item("answer_input", enabled=False)
    dpg.configure_item("show_answer_button", show=False)


def _show_answer():
    """Show the answer with penalty."""
    result = current_controller.show_answer()

    if result:
        dpg.set_value("result_text", f"Answer: {result['answer']}")
        dpg.configure_item("result_text", color=(255, 200, 100))

        stats = result['statistics']
        dpg.set_value("score_text", str(stats['score']))

        dpg.configure_item("show_answer_button",
                           show=result['penalty']['allowed'])


def _next_question():
    """Move to the next question."""
    if current_controller.is_session_complete():
        _end_session()
    else:
        current_controller.next_question()
        _update_question_display()


def _end_session_early():
    """End the session early."""
    global stop_timer
    stop_timer = True
    _end_session()


def _end_session():
    """End the session and show results."""
    global stop_timer, current_controller

    stop_timer = True

    if current_controller:
        stats = current_controller.end_session()

        if dpg.does_item_exist("flashcard_session_window"):
            dpg.delete_item("flashcard_session_window")

        show_results_view(stats, current_controller.mode)
        current_controller = None
