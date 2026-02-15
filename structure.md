# Project Structure

## Directory Layout

```
tak_flashcard/
├── src/
│   └── tak_flashcard/
│       ├── __init__.py
│       ├── main.py                 # Entry point
│       ├── config.py               # Application configuration
│       ├── constants.py            # Enums/labels for modes, directions, difficulty
│       │
│       ├── data/                   # Data storage
│       │   ├── vocab/
│       │   │   └── vocab_source.csv    # Import source ≥1000 words
│       │   ├── seed/
│       │   │   └── importer.py         # CSV → DB loader
│       │   └── user_settings.json      # User configuration/preferences
│       │
│       ├── db/                     # Database layer
│       │   ├── models.py           # SQLAlchemy models
│       │   ├── session.py          # Engine + session management
│       │   ├── repo.py             # Repository/queries
│       │   └── migrations/         # Alembic migrations (optional)
│       │
│       ├── core/                   # Core business logic
│       │   ├── difficulty.py       # Difficulty calculation
│       │   ├── scheduler.py        # Timer/speed logic
│       │   ├── scoring.py          # Scoring, penalty system
│       │   ├── selectors.py        # Question selection by difficulty/direction
│       │   └── settings.py         # Settings management and persistence
│       │
│       ├── features/               # Feature modules
│       │   ├── flashcard/
│       │   │   ├── controller.py   # Flashcard mode controller
│       │   │   ├── service.py      # Business logic
│       │   │   └── states.py       # State machine
│       │   ├── dictionary/
│       │   │   ├── controller.py   # Dictionary controller
│       │   │   └── service.py      # Dictionary logic
│       │   └── guide/
│       │       ├── controller.py   # Guide controller
│       │       └── content.py      # Static guide content│       │   └── settings/
│       │       ├── controller.py   # Settings controller
│       │       └── service.py      # Settings logic│       │
│       ├── gui/                    # GUI layer (Tkinter)
│       │   ├── app.py              # Initialize Tkinter application
│       │   ├── views/              # Screen views (Frames)
│       │   │   ├── home_view.py
│       │   │   ├── flashcard_view.py      # Flashcard settings + separate session frame class
│       │   │   ├── dictionary_view.py
│       │   │   ├── guide_view.py
│       │   │   ├── settings_view.py
│       │   │   └── results_view.py
│       │   └── components/         # Reusable UI components
│       │       ├── toolbar.py
│       │       ├── option_panels.py
│       │       └── flashcard_card.py
│       │
│       └── utils/                  # Utilities
│           ├── io.py               # File I/O operations
│           ├── validators.py       # Input validation
│           └── formatters.py       # Data formatters
│
├── requirements.txt                # Python dependencies
├── structure.md                    # This file
├── plan.md                         # Implementation plan
├── flow.md                         # Application flows
└── README.md                       # Project documentation
```

## Data Model

### Word (Vocabulary)
Each word in the database contains:
1. **English Word** (string) - The English vocabulary word
2. **Vietnamese Word** (string) - Vietnamese translation
3. **Part of Speech** (string) - noun, verb, adjective, etc.
4. **Display Count** (integer) - Number of times word was displayed
5. **Correct Count** (integer) - Number of times answered correctly
6. **Difficulty** (float) - Calculated from display_count and correct_count

### Session (optional)
Store flashcard session history:
- Session ID
- Mode (Endless/Speed/Testing)
- Direction (Eng→Vn/Vn→Eng/Mixed)
- Settings (time limit, question count, difficulty filter)
- Start/End time
- Score
- Results

## Technology Stack

- **Language:** Python 3.8+
- **GUI Framework:** Tkinter (built-in with Python)
- **Themed Widgets:** ttk (tkinter.ttk)
- **Database:** SQLite
- **ORM:** SQLAlchemy
- **Import Format:** CSV/TSV

## Key Features Mapping

### 9 Study Modes (3×3)
| Mode \ Direction | Eng→Vn | Vn→Eng | Mixed |
|-----------------|--------|--------|-------|
| Endless         | ✅     | ✅     | ✅    |
| Speed/Timer     | ✅     | ✅     | ✅    |
| Testing/Exam    | ✅     | ✅     | ✅    |

### Required Mechanisms
1. **Flashcard** - 3 modes × 3 directions = 9 study types
	- Settings are configured first, then **START SESSION** opens a separate active-session view
	- Each question uses 4 multiple-choice options (1 correct + 3 random distractors from the same answer language)
2. **Dictionary** - Full vocabulary list with search
3. **Guide** - User manual for all features
4. **Settings** - User preferences and appearance configuration

### Configurable Options
- Difficulty level adjustment (Scale 1-5: controls proportion of high-difficulty words)
- Question count (Testing mode)
- Time limit (Speed mode)
- Show Answer feature with penalty system
- Penalty types: score deduction, timeout, HP limit

-### User Settings (Appearance & Preferences)
- Font selection and pixel size controls
- Color palette (background, text, secondary)
- Window size (default dimensions)
- Language preference (if multi-language support)
- Default flashcard mode and difficulty
- Sound effects (enable/disable)
- Animation speed (fast/normal/slow/off)
