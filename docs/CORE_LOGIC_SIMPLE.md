# Core Logic (Simple)

This file explains the app core logic step by step.

## 1. Startup logic

1. Create required folders.
2. Initialize database tables.
3. Load user settings.
4. Build all screens.
5. Count words in DB.
6. If count is 0 → open Import screen in forced mode.
7. Else → open Home screen.

## 2. Flashcard setup to session

1. User opens Flashcard setup.
2. User selects:
   - mode,
   - direction,
   - difficulty,
   - penalties,
   - time or question limit (mode-dependent).
3. App validates all setup inputs through `core/safeguard.py`.
4. If invalid, app shows the error immediately in setup status and does not start.
5. App builds one safe `SessionConfig` object.
6. App starts Flashcard session view using that config.

## 3. Card generation logic

For each card:

1. Resolve direction (if Mixed, choose random direction).
2. Select one word by weighted difficulty.
3. Build 4 options:
   - 1 correct answer,
   - up to 3 distractors.
4. Show question and choices.

## 4. Answer handling logic

When user answers:

1. Compare user choice to correct answer (case-insensitive).
2. Update word stats in DB:
   - `display_count` always increases,
   - `correct_count` increases if correct.
3. Recalculate word difficulty.
4. Update score.
5. Move card to feedback state.

## 5. Show Answer logic

If Show Answer is used:

1. Check if feature is enabled.
2. Check usage limit (if any).
3. Apply configured penalty:
   - score loss and/or
   - time deduction.
4. Increase `show_used` counter.
5. Reveal answer and wait for next card.

## 6. End conditions

- **Endless**: ends only when user clicks End Session.
- **Speed**: ends when timer reaches 0 or user exits.
- **Testing**: ends when question limit reached or user exits.

## 7. Summary logic

At session end, app builds `SessionSummary`:

- correct answers,
- total asked/answered,
- percent correct,
- score,
- time used (Speed only),
- show-answer usage.

Then app opens Results screen.

## 8. Dictionary logic

- Loads all words from DB.
- Supports search by English/Vietnamese text.
- Allows one-column sorting:
  - string columns sort case-insensitively,
  - difficulty sorts numerically.

## 9. Settings logic

- Load settings from `user_settings.json`.
- If file does not exist, create defaults.
- On Save, write settings to JSON.
- Apply appearance changes immediately.

## 10. Import logic

1. User selects CSV.
2. App reads headers and maps required columns.
3. App validates rows.
4. App creates timestamped backup.
5. App imports using selected mode:
   - append or replace.
6. App shows success/failure details.
