"""Scoring and penalty system logic."""

from tak_flashcard.constants import (
    BASE_POINTS, PENALTY_POINTS, PENALTY_TIME, MAX_HP_USES, PenaltyType
)


class ScoreManager:
    """Manages scoring and penalties for flashcard sessions."""

    def __init__(self, penalty_type: PenaltyType = PenaltyType.SCORE):
        """
        Initialize score manager.

        Args:
            penalty_type: Type of penalty for Show Answer
        """
        self.score = 0
        self.correct_count = 0
        self.total_count = 0
        self.penalty_type = penalty_type
        self.show_answer_uses = 0

    def answer_correct(self, response_time: float = 0) -> int:
        """
        Process a correct answer.

        Args:
            response_time: Time taken to answer (for speed bonus)

        Returns:
            Points awarded
        """
        self.correct_count += 1
        self.total_count += 1

        points = BASE_POINTS

        if response_time > 0:
            time_bonus = max(0, int(10 - response_time))
            points += time_bonus

        self.score += points
        return points

    def answer_incorrect(self) -> int:
        """
        Process an incorrect answer.

        Returns:
            Points deducted (negative value)
        """
        self.total_count += 1
        return 0

    def apply_show_answer_penalty(self) -> dict:
        """
        Apply penalty for using Show Answer feature.

        Returns:
            Dictionary with penalty details
        """
        result = {
            'allowed': True,
            'score_penalty': 0,
            'time_penalty': 0,
            'hp_used': 0,
            'hp_remaining': MAX_HP_USES
        }

        if self.penalty_type == PenaltyType.SCORE:
            self.score = max(0, self.score - PENALTY_POINTS)
            result['score_penalty'] = PENALTY_POINTS

        elif self.penalty_type == PenaltyType.TIME:
            result['time_penalty'] = PENALTY_TIME

        elif self.penalty_type == PenaltyType.HP:
            self.show_answer_uses += 1
            result['hp_used'] = self.show_answer_uses
            result['hp_remaining'] = MAX_HP_USES - self.show_answer_uses

            if self.show_answer_uses >= MAX_HP_USES:
                result['allowed'] = False

        return result

    def can_use_show_answer(self) -> bool:
        """
        Check if Show Answer can still be used.

        Returns:
            True if Show Answer is still available
        """
        if self.penalty_type == PenaltyType.HP:
            return self.show_answer_uses < MAX_HP_USES
        return True

    def get_statistics(self) -> dict:
        """
        Get current session statistics.

        Returns:
            Dictionary with score and stats
        """
        accuracy = 0
        if self.total_count > 0:
            accuracy = (self.correct_count / self.total_count) * 100

        return {
            'score': self.score,
            'correct': self.correct_count,
            'total': self.total_count,
            'accuracy': accuracy
        }
