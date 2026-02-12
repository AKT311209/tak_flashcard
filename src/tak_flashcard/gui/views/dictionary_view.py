"""Dictionary view for browsing and searching words."""

import dearpygui.dearpygui as dpg
from tak_flashcard.gui.components.toolbar import create_toolbar
from tak_flashcard.features.dictionary import DictionaryController


dictionary_controller = None


def show_dictionary_view():
    """Display the dictionary view."""
    global dictionary_controller

    # show as a centered modal popup instead of replacing the main window
    if dpg.does_item_exist("dictionary_window"):
        dpg.delete_item("dictionary_window")

    dictionary_controller = DictionaryController()

    viewport_width = dpg.get_viewport_width()
    viewport_height = dpg.get_viewport_height()

    dialog_width = min(900, viewport_width - 80)
    dialog_height = min(700, viewport_height - 80)
    pos_x = (viewport_width - dialog_width) // 2
    pos_y = (viewport_height - dialog_height) // 2

    with dpg.window(
        tag="dictionary_window",
        label="Dictionary",
        width=dialog_width,
        height=dialog_height,
        pos=(pos_x, pos_y),
        modal=True,
        no_resize=True
    ):
        create_toolbar(on_back=None, on_home=_cleanup_and_home,
                       show_back=False)
        dpg.add_separator()
        dpg.add_spacer(height=10)

        with dpg.group(horizontal=True):
            dpg.add_text("Search:")
            dpg.add_input_text(
                tag="search_input",
                width=300,
                callback=lambda s, a: _search_words(a)
            )
            dpg.add_spacer(width=20)

            dpg.add_text("Filter by POS:")
            parts_of_speech = ["All"] + \
                dictionary_controller.get_parts_of_speech()
            dpg.add_combo(
                tag="pos_filter",
                items=parts_of_speech,
                default_value="All",
                width=150,
                callback=lambda s, a: _filter_by_pos(a)
            )
            dpg.add_spacer(width=20)

            dpg.add_text("Sort:")
            dpg.add_combo(
                tag="sort_combo",
                items=["English", "Vietnamese", "Difficulty"],
                default_value="English",
                width=120,
                callback=lambda s, a: _change_sort(a)
            )

        dpg.add_spacer(height=15)
        dpg.add_separator()

        with dpg.table(
            tag="word_table",
            header_row=True,
            borders_innerH=True,
            borders_outerH=True,
            borders_innerV=True,
            borders_outerV=True,
            scrollY=True,
            height=550
        ):
            dpg.add_table_column(label="English", width=150)
            dpg.add_table_column(label="Pronunciation", width=150)
            dpg.add_table_column(label="Vietnamese", width=200)
            dpg.add_table_column(label="Part of Speech", width=120)
            dpg.add_table_column(label="Difficulty", width=80)

    _load_words()


def _load_words():
    """Load and display all words."""
    words = dictionary_controller.load_all_words()
    _update_table(words)


def _search_words(query: str):
    """Search for words matching the query."""
    words = dictionary_controller.search(query)
    _update_table(words)


def _filter_by_pos(pos: str):
    """Filter words by part of speech."""
    words = dictionary_controller.filter_by_part_of_speech(
        None if pos == "All" else pos)
    _update_table(words)


def _change_sort(sort_by: str):
    """Change sort order."""
    sort_map = {
        "English": "english",
        "Vietnamese": "vietnamese",
        "Difficulty": "difficulty"
    }
    dictionary_controller.set_sort(sort_map[sort_by])
    _update_table(dictionary_controller.current_words)


def _update_table(words):
    """Update the word table with new data."""
    if not dpg.does_item_exist("word_table"):
        return

    for child in dpg.get_item_children("word_table", 1):
        dpg.delete_item(child)

    for word in words:
        with dpg.table_row(parent="word_table"):
            dpg.add_text(word.english)
            dpg.add_text(word.pronunciation)
            dpg.add_text(word.vietnamese)
            dpg.add_text(word.part_of_speech)
            dpg.add_text(f"{word.difficulty:.2f}")


def _cleanup_and_home():
    """Clean up and return to home."""
    global dictionary_controller

    if dictionary_controller:
        dictionary_controller.cleanup()
        dictionary_controller = None

    if dpg.does_item_exist("dictionary_window"):
        dpg.delete_item("dictionary_window")

    from tak_flashcard.gui.views.home_view import show_home_view
    show_home_view()
