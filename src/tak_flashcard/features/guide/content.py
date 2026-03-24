"""Static guide content for the application."""

from __future__ import annotations

GUIDE_TEXT = """
Welcome to Tak Flashcard!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GETTING STARTED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- Choose a mode: Endless, Speed, or Testing.
- Select translation direction: English→Vietnamese, Vietnamese→English, or Mixed.
- Adjust difficulty from 1 (easy) to 5 (hard).
- Every question is multiple choice with 4 options.
- Eng→Vn uses 1 correct Vietnamese answer plus 3 random Vietnamese distractors.
- Vn→Eng uses 1 correct English answer plus 3 random English distractors.
- Mixed mode applies the matching rule for whichever direction is selected on that turn.
- Use Show Answer sparingly; it applies a penalty.
- Track your score and accuracy in results.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEYBOARD SHORTCUTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Flashcard Configuration Screen
  Enter      Start Session
  Escape     Back to Home

Flashcard Session
  1 / 2 / 3 / 4   Select answer choice 1, 2, 3, or 4 (auto-submit)
  Space            Show Answer (before answering) / Next card (after answering)
  Enter            Next card (after answering)
  Escape           End session early

Dictionary
  Enter      Search
  Escape     Back to Home

Results Screen
  Enter      Play Again (return to configuration)
  Escape     Back to Home

Other Screens (Guide, Settings, Import)
  Escape     Back to Home
"""
