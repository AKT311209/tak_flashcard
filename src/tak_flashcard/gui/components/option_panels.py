"""Option panels for flashcard configuration."""

import dearpygui.dearpygui as dpg
from tak_flashcard.constants import (
    FlashcardMode, Direction, PenaltyType,
    MODE_LABELS, DIRECTION_LABELS, PENALTY_LABELS
)
from tak_flashcard.config import (
    DEFAULT_DIFFICULTY, DEFAULT_QUESTION_COUNT, DEFAULT_TIME_LIMIT,
    MIN_QUESTION_COUNT, MAX_QUESTION_COUNT, MIN_TIME_LIMIT, MAX_TIME_LIMIT
)


class FlashcardOptionsPanel:
    """Panel for configuring flashcard session options."""

    def __init__(self, parent):
        """
        Initialize options panel.

        Args:
            parent: Parent DearPyGui container
        """
        self.parent = parent
        self.mode = FlashcardMode.ENDLESS
        self.direction = Direction.ENG_TO_VN
        self.difficulty = DEFAULT_DIFFICULTY
        self.question_count = DEFAULT_QUESTION_COUNT
        self.time_limit = DEFAULT_TIME_LIMIT
        self.enable_show_answer = True
        self.penalty_type = PenaltyType.SCORE

        self.mode_group = None
        self.direction_group = None
        self.penalty_group = None

    def create(self):
        """Create the options panel UI."""
        with dpg.child_window(parent=self.parent, height=500, border=True):
            dpg.add_text("Flashcard Configuration", color=(100, 200, 255))
            dpg.add_separator()
            dpg.add_spacer(height=10)

            dpg.add_text("Select Mode:")
            self.mode_group = dpg.add_radio_button(
                items=[MODE_LABELS[m] for m in FlashcardMode],
                default_value=MODE_LABELS[FlashcardMode.ENDLESS],
                callback=self._on_mode_change
            )
            dpg.add_spacer(height=15)

            dpg.add_text("Select Direction:")
            self.direction_group = dpg.add_radio_button(
                items=[DIRECTION_LABELS[d] for d in Direction],
                default_value=DIRECTION_LABELS[Direction.ENG_TO_VN],
                callback=self._on_direction_change
            )
            dpg.add_spacer(height=15)

            dpg.add_text("Difficulty Level:")
            dpg.add_slider_int(
                tag="difficulty_slider",
                default_value=DEFAULT_DIFFICULTY,
                min_value=1,
                max_value=5,
                width=200,
                callback=self._on_difficulty_change
            )
            dpg.add_text("(1 = Easiest, 5 = Hardest)")
            dpg.add_spacer(height=15)

            dpg.add_text("Mode-Specific Options:", color=(255, 200, 100))
            dpg.add_separator()

            with dpg.group(tag="testing_options", show=False):
                dpg.add_text("Question Count:")
                dpg.add_input_int(
                    tag="question_count_input",
                    default_value=DEFAULT_QUESTION_COUNT,
                    min_value=MIN_QUESTION_COUNT,
                    max_value=MAX_QUESTION_COUNT,
                    min_clamped=True,
                    max_clamped=True,
                    width=150,
                    callback=self._on_question_count_change
                )

            with dpg.group(tag="speed_options", show=False):
                dpg.add_text("Time Limit (seconds):")
                dpg.add_input_int(
                    tag="time_limit_input",
                    default_value=DEFAULT_TIME_LIMIT,
                    min_value=MIN_TIME_LIMIT,
                    max_value=MAX_TIME_LIMIT,
                    min_clamped=True,
                    max_clamped=True,
                    width=150,
                    callback=self._on_time_limit_change
                )
                dpg.add_spacer(height=10)
                dpg.add_checkbox(
                    tag="show_answer_checkbox",
                    label="Enable Show Answer",
                    default_value=True,
                    callback=self._on_show_answer_change
                )
                with dpg.group(tag="penalty_options"):
                    dpg.add_text("Penalty Type:")
                    self.penalty_group = dpg.add_radio_button(
                        items=[PENALTY_LABELS[p] for p in PenaltyType],
                        default_value=PENALTY_LABELS[PenaltyType.SCORE],
                        callback=self._on_penalty_change
                    )

            with dpg.group(tag="endless_options", show=True):
                dpg.add_checkbox(
                    tag="endless_show_answer_checkbox",
                    label="Enable Show Answer",
                    default_value=True,
                    callback=self._on_show_answer_change
                )
                with dpg.group(tag="endless_penalty_options"):
                    dpg.add_text("Penalty Type:")
                    dpg.add_radio_button(
                        tag="endless_penalty_radio",
                        items=[PENALTY_LABELS[PenaltyType.SCORE],
                               PENALTY_LABELS[PenaltyType.HP]],
                        default_value=PENALTY_LABELS[PenaltyType.SCORE],
                        callback=self._on_penalty_change
                    )

    def _on_mode_change(self, sender, app_data):
        """Handle mode selection change."""
        selected_label = app_data
        for mode, label in MODE_LABELS.items():
            if label == selected_label:
                self.mode = mode
                break

        dpg.configure_item("testing_options", show=(
            self.mode == FlashcardMode.TESTING))
        dpg.configure_item("speed_options", show=(
            self.mode == FlashcardMode.SPEED))
        dpg.configure_item("endless_options", show=(
            self.mode == FlashcardMode.ENDLESS))

    def _on_direction_change(self, sender, app_data):
        """Handle direction selection change."""
        selected_label = app_data
        for direction, label in DIRECTION_LABELS.items():
            if label == selected_label:
                self.direction = direction
                break

    def _on_difficulty_change(self, sender, app_data):
        """Handle difficulty level change."""
        self.difficulty = app_data

    def _on_question_count_change(self, sender, app_data):
        """Handle question count change."""
        self.question_count = app_data

    def _on_time_limit_change(self, sender, app_data):
        """Handle time limit change."""
        self.time_limit = app_data

    def _on_show_answer_change(self, sender, app_data):
        """Handle show answer checkbox change."""
        self.enable_show_answer = app_data

        if dpg.does_item_exist("penalty_options"):
            dpg.configure_item("penalty_options", show=app_data)
        if dpg.does_item_exist("endless_penalty_options"):
            dpg.configure_item("endless_penalty_options", show=app_data)

    def _on_penalty_change(self, sender, app_data):
        """Handle penalty type change."""
        selected_label = app_data
        for penalty, label in PENALTY_LABELS.items():
            if label == selected_label:
                self.penalty_type = penalty
                break

    def get_config(self) -> dict:
        """
        Get the current configuration.

        Returns:
            Dictionary with configuration values
        """
        return {
            'mode': self.mode,
            'direction': self.direction,
            'difficulty': self.difficulty,
            'question_count': self.question_count if self.mode == FlashcardMode.TESTING else None,
            'time_limit': self.time_limit if self.mode == FlashcardMode.SPEED else None,
            'enable_show_answer': self.enable_show_answer if self.mode != FlashcardMode.TESTING else False,
            'penalty_type': self.penalty_type
        }
