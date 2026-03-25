# Tak Flashcard

Tak Flashcard is a desktop app to help people practice English–Vietnamese vocabulary.

It is made for learners first: pick a mode, answer quick multiple-choice cards, and track your progress.

## What this app does

- Practice vocabulary with flashcards
- Adjust difficulty from easy to hard
- Use three learning modes:
  - **Endless** (no timer)
  - **Speed** (countdown timer)
  - **Testing** (fixed number of questions)
- Browse all words in a built-in dictionary
- Import your own CSV vocabulary file
- Save UI preferences (font/colors/window size)

## Run in 3 steps

1. Install dependencies
2. Start the app
3. Import vocabulary if prompted

For exact commands and troubleshooting, see `docs/QUICKSTART.md`.

## How the app behaves (simple)

1. App starts
2. App checks if the database has words
3. If empty, app opens **Import Vocabulary** and requires import first
4. User reaches Home screen
5. User chooses Flashcard / Dictionary / Guide / Settings

## Learning logic (simple)

- Every word stores:
  - how many times it was shown
  - how many times it was answered correctly
- Word difficulty is recalculated after answers using:

$$
difficulty = 1 - \frac{correct\_count}{display\_count + \epsilon}
$$

- The selected difficulty level (1–5) changes the chance of selecting easier vs harder words.

## Input safeguards

- Flashcard setup input values are validated through `src/tak_flashcard/core/safeguard.py`.
- Invalid values are rejected before a session starts.
- Validation errors are shown immediately in the setup status area as soon as input becomes invalid.

## Non-technical documentation

If you want plain-language documentation for operations and internals:

- `docs/NON_TECH_OVERVIEW.md` — app behavior explained in simple language
- `docs/CORE_LOGIC_SIMPLE.md` — end-to-end core flows
- `docs/FUNCTION_ROLE_MAP.md` — each function/class method, its role, and when it is called

## Tech stack

- Python
- Tkinter (desktop UI)
- SQLite + SQLAlchemy

## Project entry point

- Main module: `src/tak_flashcard/main.py`
