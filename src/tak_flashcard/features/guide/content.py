"""Guide content for the application."""

GUIDE_CONTENT = """
# Tak Flashcard - User Guide

## Introduction
Welcome to Tak Flashcard! This application helps you learn English-Vietnamese vocabulary through interactive flashcard sessions.

## Table of Contents
1. Flashcard Modes
2. Translation Directions
3. Difficulty Levels
4. Penalty System
5. Scoring
6. Tips for Effective Learning

---

## 1. Flashcard Modes

### Endless Mode
- **Description**: Practice vocabulary without time limits or question limits
- **Features**:
  - No automatic ending - study at your own pace
  - Optional "Show Answer" feature
  - Track your score and accuracy
- **Best for**: Casual learning and practice

### Speed Mode
- **Description**: Race against the clock to answer as many questions as possible
- **Features**:
  - Countdown timer (configurable)
  - Time bonus for quick answers
  - Optional "Show Answer" with time penalty
  - Session ends when timer reaches zero
- **Best for**: Quick practice sessions and improving response speed

### Testing Mode
- **Description**: Take a formal test with a set number of questions
- **Features**:
  - Fixed number of questions (configurable: 10-100)
  - No "Show Answer" option
  - Final results with detailed statistics
  - Review wrong answers
- **Best for**: Self-assessment and exam preparation

---

## 2. Translation Directions

### English → Vietnamese
- Question displays an English word
- Type the Vietnamese translation
- Example: "hello" → answer "xin chào"

### Vietnamese → English
- Question displays a Vietnamese word
- Type the English translation
- Example: "xin chào" → answer "hello"

### Mixed
- Randomly alternates between English → Vietnamese and Vietnamese → English
- Provides variety and tests both directions
- Best for comprehensive practice

---

## 3. Difficulty Levels

The difficulty setting (1-5) controls which words you'll see more often:

### Level 1 (Easiest)
- Mostly shows words you've answered correctly before
- Great for beginners and confidence building

### Level 2 (Easy)
- Slightly favors easier words
- Good for gradual progression

### Level 3 (Balanced)
- Equal mix of all difficulty levels
- Recommended for most users

### Level 4 (Hard)
- Slightly favors words you struggle with
- Helps target weak areas

### Level 5 (Hardest)
- Mostly shows your most difficult words
- Ideal for advanced learners and challenge seekers

**Note**: All words remain accessible at every difficulty level. The setting only adjusts the probability of seeing each word.

---

## 4. Penalty System

When "Show Answer" is enabled, you can peek at the answer, but with a penalty:

### Score Deduction (Endless/Speed)
- Lose 10 points each time you view the answer
- Your score cannot go below zero

### Time Deduction (Speed only)
- Lose 10 seconds from your remaining time
- Use carefully as time is limited!

### HP Limit (Endless/Speed)
- Maximum 3 uses of "Show Answer" per session
- Once used up, the feature is disabled
- Choose wisely when you really need help

---

## 5. Scoring

### Base Points
- Correct answer: +10 points
- Wrong answer: 0 points

### Speed Bonuses (Speed Mode only)
- Answer within 1 second: +9 bonus points
- Answer within 3 seconds: +7 bonus points
- Answer within 5 seconds: +5 bonus points
- Answer within 10 seconds: +1 bonus point

### Final Score (Testing Mode)
- Total score = Correct answers × 10
- Accuracy percentage displayed
- Breakdown by direction

---

## 6. Tips for Effective Learning

### 1. Start with Lower Difficulty
- Build confidence with Level 1 or 2
- Gradually increase as you improve

### 2. Practice Both Directions
- Use "Mixed" mode for balanced learning
- Strengthens bidirectional vocabulary

### 3. Use Speed Mode for Quick Reviews
- 5-minute sessions are effective
- Helps with retention and recall speed

### 4. Take Tests Regularly
- Weekly tests track your progress
- Identify areas needing improvement

### 5. Review the Dictionary
- Browse all words periodically
- Use search to find specific vocabulary
- Filter by part of speech to focus on specific word types

### 6. Limit Show Answer Usage
- Try to recall before showing the answer
- Active recall strengthens memory better than passive review

### 7. Consistent Practice
- Short daily sessions are better than long weekly cramming
- Aim for 10-15 minutes per day

---

## Dictionary Feature

Access the full vocabulary database:
- **Search**: Find words by English or Vietnamese text
- **Filter**: Filter by part of speech (noun, verb, adjective, etc.)
- **Sort**: Sort by English, Vietnamese, or difficulty
- **View Details**: See pronunciation and statistics for each word

---

## Settings

Customize your experience:
- **Theme**: Light or Dark mode
- **Font Size**: Adjust for comfortable reading
- **Default Values**: Set your preferred mode and difficulty
- **Window Size**: Customize application dimensions

---

Thank you for using Tak Flashcard! Happy learning! 📚✨
"""


def get_guide_content() -> str:
    """
    Get the complete guide content.

    Returns:
        Guide content as string
    """
    return GUIDE_CONTENT
