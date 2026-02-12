"""Guide controller managing guide display."""

from tak_flashcard.features.guide.content import get_guide_content


class GuideController:
    """Controller for guide functionality."""

    def __init__(self):
        """Initialize guide controller."""
        self.content = get_guide_content()

    def get_content(self) -> str:
        """
        Get guide content.

        Returns:
            Guide content string
        """
        return self.content
