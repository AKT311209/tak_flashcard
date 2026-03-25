"""Input safeguard utilities for flashcard session configuration.

This module provides one centralized validation layer for all setup inputs
coming from the flashcard options UI.  It accepts raw widget values (strings
or numbers), validates them, and either returns a safe ``SessionConfig`` or a
list of user-friendly validation issues.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

from tak_flashcard.config import DIFFICULTY_LEVELS, Direction, Mode
from tak_flashcard.features.flashcard.states import SessionConfig, ShowAnswerConfig


@dataclass
class SafeguardIssue:
    """Represents one validation issue for a specific input field.

    Attributes:
        field: Internal field key (for example ``"time_limit"``).
        message: Human-friendly validation message.
    """

    field: str
    message: str


@dataclass
class SessionConfigValidation:
    """Validation result for raw flashcard setup input.

    Attributes:
        config: A sanitized ``SessionConfig`` when validation succeeds,
            otherwise ``None``.
        issues: A list of detected validation issues. Empty when valid.
    """

    config: Optional[SessionConfig]
    issues: list[SafeguardIssue]

    @property
    def is_valid(self) -> bool:
        """Return ``True`` when no validation issue exists."""

        return not self.issues


def build_safe_session_config(
    *,
    mode_value: Any,
    direction_value: Any,
    difficulty_value: Any,
    question_count_value: Any,
    time_limit_value: Any,
    show_score_penalty_value: Any,
    show_limit_value: Any,
    show_time_penalty_value: Any,
    wrong_answer_penalty_value: Any,
    endless_penalty_choice: Any,
    speed_penalty_choice: Any,
) -> SessionConfigValidation:
    """Validate raw setup values and return a safe ``SessionConfig``.

    Parameters:
        mode_value: Raw mode value from UI state.
        direction_value: Raw direction value from UI state.
        difficulty_value: Raw difficulty value.
        question_count_value: Raw testing question count value.
        time_limit_value: Raw speed-mode time limit value.
        show_score_penalty_value: Raw score penalty value for Show Answer.
        show_limit_value: Raw maximum Show Answer uses.
        show_time_penalty_value: Raw time penalty value for Show Answer.
        wrong_answer_penalty_value: Raw wrong-answer penalty value.
        endless_penalty_choice: Raw endless mode penalty choice.
        speed_penalty_choice: Raw speed mode penalty choice.

    Returns:
        A ``SessionConfigValidation`` containing a safe session config when all
        checks pass, otherwise a list of validation issues.
    """

    issues: list[SafeguardIssue] = []

    mode = _parse_enum(mode_value, Mode, "mode", issues)
    direction = _parse_enum(direction_value, Direction, "direction", issues)

    difficulty = _parse_int(
        difficulty_value,
        field="difficulty",
        issues=issues,
        minimum=min(DIFFICULTY_LEVELS),
        maximum=max(DIFFICULTY_LEVELS),
        label="Difficulty",
    )

    question_count: Optional[int] = None
    time_limit: Optional[int] = None
    show_score_penalty: Optional[int] = None
    show_limit: Optional[int] = None
    show_time_penalty: Optional[int] = None
    wrong_answer_penalty: Optional[int] = None

    endless_choice = str(endless_penalty_choice or "score").strip().lower()
    if endless_choice not in {"score", "limit"}:
        issues.append(
            SafeguardIssue(
                field="endless_penalty_choice",
                message="Endless show penalty type must be score deduction or limit uses.",
            )
        )

    speed_choice = str(speed_penalty_choice or "score").strip().lower()
    if speed_choice not in {"score", "limit", "time"}:
        issues.append(
            SafeguardIssue(
                field="speed_penalty_choice",
                message="Speed show penalty type must be score deduction, limit uses, or time deduction.",
            )
        )

    if issues or mode is None or direction is None:
        return SessionConfigValidation(config=None, issues=issues)

    score_penalty = 0
    max_uses: Optional[int] = None
    time_penalty = 0

    if mode == Mode.TESTING:
        question_count = _parse_int(
            question_count_value,
            field="question_count",
            issues=issues,
            minimum=1,
            maximum=1000,
            label="Question count",
        )
    elif mode == Mode.ENDLESS:
        wrong_answer_penalty = _parse_int(
            wrong_answer_penalty_value,
            field="wrong_answer_penalty",
            issues=issues,
            minimum=0,
            maximum=10000,
            label="Wrong answer penalty",
        )
        if endless_choice == "score":
            show_score_penalty = _parse_int(
                show_score_penalty_value,
                field="show_score_penalty",
                issues=issues,
                minimum=0,
                maximum=10000,
                label="Show penalty points",
            )
            score_penalty = show_score_penalty or 0
        else:
            show_limit = _parse_int(
                show_limit_value,
                field="show_limit",
                issues=issues,
                minimum=0,
                maximum=10000,
                label="Show limit uses",
            )
            max_uses = show_limit if (show_limit or 0) > 0 else None
    elif mode == Mode.SPEED:
        time_limit = _parse_int(
            time_limit_value,
            field="time_limit",
            issues=issues,
            minimum=1,
            maximum=36000,
            label="Time limit",
        )
        wrong_answer_penalty = _parse_int(
            wrong_answer_penalty_value,
            field="wrong_answer_penalty",
            issues=issues,
            minimum=0,
            maximum=10000,
            label="Wrong answer penalty",
        )
        if speed_choice == "score":
            show_score_penalty = _parse_int(
                show_score_penalty_value,
                field="show_score_penalty",
                issues=issues,
                minimum=0,
                maximum=10000,
                label="Show penalty points",
            )
            score_penalty = show_score_penalty or 0
        elif speed_choice == "limit":
            show_limit = _parse_int(
                show_limit_value,
                field="show_limit",
                issues=issues,
                minimum=0,
                maximum=10000,
                label="Show limit uses",
            )
            max_uses = show_limit if (show_limit or 0) > 0 else None
        elif speed_choice == "time":
            show_time_penalty = _parse_int(
                show_time_penalty_value,
                field="show_time_penalty",
                issues=issues,
                minimum=0,
                maximum=36000,
                label="Show time penalty",
            )
            time_penalty = show_time_penalty or 0

    if issues:
        return SessionConfigValidation(config=None, issues=issues)

    show_config = ShowAnswerConfig(
        enabled=mode != Mode.TESTING,
        score_penalty=score_penalty,
        time_penalty=time_penalty if mode == Mode.SPEED else 0,
        max_uses=0 if mode == Mode.TESTING else max_uses,
    )
    safe_config = SessionConfig(
        mode=mode,
        direction=direction,
        difficulty=difficulty or min(DIFFICULTY_LEVELS),
        show_config=show_config,
        question_limit=question_count if mode == Mode.TESTING else None,
        time_limit=time_limit if mode == Mode.SPEED else None,
        wrong_penalty=(wrong_answer_penalty or 0)
        if mode in (Mode.ENDLESS, Mode.SPEED)
        else 0,
    )
    return SessionConfigValidation(config=safe_config, issues=[])


def _parse_enum(value: Any, enum_type: type[Mode] | type[Direction], field: str, issues: list[SafeguardIssue]) -> Any:
    """Convert a raw enum value and report validation issues when invalid.

    Parameters:
        value: Raw value from UI.
        enum_type: The target enum class.
        field: Field name used in validation output.
        issues: Mutable list where validation issues are appended.

    Returns:
        A parsed enum value, or ``None`` when parsing fails.
    """

    try:
        return enum_type(value)
    except (TypeError, ValueError):
        readable = " / ".join(item.value for item in enum_type)
        issues.append(
            SafeguardIssue(
                field=field,
                message=f"{field.replace('_', ' ').title()} must be one of: {readable}.",
            )
        )
        return None


def _parse_int(
    value: Any,
    *,
    field: str,
    issues: list[SafeguardIssue],
    minimum: int,
    maximum: int,
    label: str,
) -> Optional[int]:
    """Parse and range-check a raw integer input value.

    Parameters:
        value: Raw value from UI widgets.
        field: Internal field key.
        issues: Mutable list where validation issues are appended.
        minimum: Minimum accepted integer value.
        maximum: Maximum accepted integer value.
        label: User-facing field label for error messages.

    Returns:
        Parsed integer when valid, otherwise ``None``.
    """

    text = str(value).strip()
    if text == "":
        issues.append(SafeguardIssue(
            field=field, message=f"{label} is required."))
        return None
    try:
        parsed = int(text)
    except (TypeError, ValueError):
        issues.append(SafeguardIssue(
            field=field, message=f"{label} must be an integer."))
        return None

    if parsed < minimum or parsed > maximum:
        issues.append(
            SafeguardIssue(
                field=field,
                message=f"{label} must be between {minimum} and {maximum}.",
            )
        )
        return None
    return parsed
