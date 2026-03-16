# Tak Flashcard — Non-Technical Overview

This document explains the app in plain language.

## What this app is

Tak Flashcard is a vocabulary practice app.

You choose a study style, answer multiple-choice cards, and the app tracks your progress.

## Main screens

- **Home**: main menu
- **Flashcard setup**: choose mode, direction, difficulty
- **Flashcard session**: active quiz screen
- **Results**: session summary
- **Dictionary**: browse/search all words
- **Import Vocabulary**: load words from CSV
- **Guide**: help page
- **Settings**: visual preferences

## Flashcard modes

- **Endless**: no timer, keep practicing
- **Speed**: timer counts down
- **Testing**: fixed number of questions

## Direction options

- English → Vietnamese
- Vietnamese → English
- Mixed (random direction each card)

## Difficulty behavior

- Difficulty range is 1 to 5
- Level 1 prefers easier words
- Level 5 prefers harder words
- Word difficulty updates after each answer

## What happens when app opens

1. App checks local database.
2. If database has no words, app opens Import screen in forced mode.
3. After successful import, app goes to Home.

## How import works

CSV must include:

- `english`
- `vietnamese`
- `part_of_speech`

Before changing database, app saves a backup CSV copy in `data/vocab/`.

Import modes:

- **Append**: keeps old words
- **Replace**: clears old words first

## Session scoring and penalties

- Correct answers increase score.
- Wrong answers can reduce score (depending on mode config).
- Show Answer can apply one penalty:
  - score deduction,
  - time deduction,
  - usage limit.

## Where to read deeper

- Core flow: `docs/CORE_LOGIC_SIMPLE.md`
- Function roles and call timing: `docs/FUNCTION_ROLE_MAP.md`
