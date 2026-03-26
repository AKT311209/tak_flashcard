# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Essential Reading Before Writing Code

**ALWAYS read these files first** before making any code changes:
- `docs/plan.md` - Implementation plan and requirements
- `docs/flow.md` - Application flows and logic
- `docs/structure.md` - Project structure and architecture

These contain critical context that guides implementation decisions.

## Running the Application

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python src/tak_flashcard/main.py
```

The main entry point is `src/tak_flashcard/main.py`.

## Building the EXE

```bash
# Windows (automated)
build_exe.bat

# Linux/macOS (cross-compile to Windows)
chmod +x build_exe.sh
./build_exe.sh

# Manual PyInstaller
pip install pyinstaller
pyinstaller tak_flashcard.spec
```

The `.spec` file includes SQLAlchemy SQLite support and embeds the app icon.

## Code Standards

### Comments
- **ONLY** add comments to explain code logic
- **NEVER** add comments describing what you have done, are doing, or have changed (per [`.github/copilot-instructions.md`](.github/copilot-instructions.md))

### Docstrings
- All functions and classes **must** have docstrings explaining purpose, parameters, and return values

### Production Code
- **DO NOT** include test code, debugging statements, or temporary code
- Code must be clean and production-ready

## Architecture Overview

### Layer Structure
```
├── core/          # Business logic (difficulty, scoring, selectors, safeguard, etc.)
├── db/            # Database layer (models, session, repo)
├── features/      # Feature modules (flashcard, dictionary, guide, settings)
├── gui/           # Tkinter UI layer (views, components)
└── data/          # Data storage and CSV import
```

### Key Design Patterns

**Feature Modules**: Each feature follows Controller → Service → State pattern
- Controller: UI interactions and navigation
- Service: Business logic implementation
- States: State machine for session management (flashcard)

**Performance Optimization**: Card pre-rendering
- Testing mode: All cards pre-rendered upfront
- Endless/Speed modes: Batch pre-rendering with queue refill
- Implemented in `FlashcardService._prepare_next_card()` using `collections.deque`

**Input Validation**: All flashcard setup inputs validated via `core/safeguard.py`
- Real-time validation on input change
- Session start blocked when invalid

### Data Flow
```
CSV Import → SQLite DB → Repository Layer → Services → Controllers → GUI Views
                    ↑                                          ↓
                    └────────── Stats Update (display_count, correct_count, difficulty)
```

## Important Behaviors

### Startup Behavior
1. Check if database has words
2. If empty → Force Import Vocabulary mode (Back button hidden, warning banner shown)
3. If has words → Show Home screen

### Flashcard Modes (9 total: 3 modes × 3 directions)
- **Modes**: Endless (no timer), Speed (countdown), Testing (fixed questions)
- **Directions**: Eng→Vn, Vn→Eng, Mixed (random per card)
- Configuration view → Separate session frame → Results summary

### Difficulty System
Word difficulty calculated as: `difficulty = 1 - (correct_count / (display_count + ε))`

User setting (1-5) controls weighted random selection probability, not filtering.

### Import Vocabulary
- CSV requires columns: `english`, `vietnamese`, `part_of_speech`
- **Append mode**: Insert new words without touching existing ones
- **Replace mode**: Clear word table, then insert new words
- Timestamped backup created before any DB change in `data/vocab/`

### Settings Persistence
- Stored in `data/user_settings.json`
- Includes appearance (font, colors, window size), defaults (mode, difficulty), and preferences
- Applied immediately on save

## Data Paths

The app detects running mode and adjusts paths automatically:

| Mode | Data Location |
|------|---------------|
| Source code | `src/tak_flashcard/data/` |
| Built EXE | Sibling folder `tak_flashcard_data/` |

Detection via `sys.frozen` check in `config.py`.

## CSV Import Format

Required columns:
- `english` - English vocabulary word
- `vietnamese` - Vietnamese translation
- `part_of_speech` - noun, verb, adjective, etc.

See `sample_vocab_source.csv` for reference.

## Session State Machine

Flashcard session states: `INIT` → `QUESTION` → `ANSWERING` → `VALIDATE` → `RESULT` → (loop) → `FINISH` → `SUMMARY`

See `features/flashcard/states.py` for implementation.
