# Quick Start (Non-Technical)

This guide helps you open and use Tak Flashcard quickly.

## 1) Start the app

### Setup (one-time)

```bash
pip install -r requirements.txt
pip install -e .
```

### Run the app

```bash
python src/tak_flashcard/main.py
```

**Alternative** (without `pip install -e .`):

```bash
PYTHONPATH=src python src/tak_flashcard/main.py
```

## 2) First launch behavior

On first run, the app will:

1. Create the database file.
2. Check whether words exist.
3. If no words exist, open **Import Vocabulary** in forced mode.

Forced mode means:

- You must import a CSV first.
- Back button is hidden.
- After successful import, app goes to Home screen.

## 3) CSV import requirements

Your CSV must include these columns:

- `english`
- `vietnamese`
- `part_of_speech`

**A sample CSV** (`sample_vocab_source.csv`) is included in the project. You can use it directly or as a template for your own vocabulary list.

Import modes:

- **Append**: keep existing words, add/update from file.
- **Replace**: remove all existing words, then insert from file.

Before import, the app creates a backup copy in `src/tak_flashcard/data/vocab/`.

## 4) Basic learning flow

1. Home → **Flashcard**
2. Pick mode, direction, difficulty
3. Click **Start Session**
4. Answer cards
5. See **Session Summary**

Flashcard setup fields are validated in real time. If an input is invalid, an
error appears in the setup status row immediately and **Start Session** stays
disabled until the value is corrected.

## 5) Keyboard shortcuts

| Screen | Key | Action |
|---|---|---|
| Flashcard setup | `Enter` | Start session |
| Flashcard setup | `Escape` | Back to Home |
| Flashcard session | `1` / `2` / `3` / `4` | Choose answer |
| Flashcard session | `Space` | Show Answer or Next |
| Flashcard session | `Enter` | Next card (after answer) |
| Flashcard session | `Escape` | End session |
| Dictionary | `Enter` | Search |
| Dictionary | `Escape` | Back to Home |
| Results | `Enter` | Play Again |
| Results | `Escape` | Home |

## 6) If something goes wrong

- Check dependencies are installed from `requirements.txt`.
- Confirm CSV has required columns.
- If data seems broken, remove the local DB file and restart (the app recreates it).

## 7) Read more (simple docs)

- `docs/NON_TECH_OVERVIEW.md`
- `docs/CORE_LOGIC_SIMPLE.md`
- `docs/FUNCTION_ROLE_MAP.md`
