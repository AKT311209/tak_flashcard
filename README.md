# Tak Flashcard - English-Vietnamese Vocabulary Learning App

A comprehensive desktop application for learning English-Vietnamese vocabulary through interactive flashcard sessions. Built with Python and Tkinter.

## Features

### 🎯 Three Flashcard Modes
- **Endless Mode**: Practice at your own pace without time limits
- **Speed Mode**: Race against the clock with time-based scoring
- **Testing Mode**: Take formal tests with a set number of questions

### 🔄 Multiple Translation Directions
- English → Vietnamese
- Vietnamese → English
- Mixed (random alternation)

### 📊 Adaptive Difficulty System
- 5 difficulty levels (1-5)
- Weighted word selection based on your performance
- Words you struggle with appear more frequently at higher difficulty levels

### 📚 Comprehensive Dictionary
- Browse over 1000 English-Vietnamese word pairs
- Search by English or Vietnamese words
- Filter by part of speech
- Sort by English, Vietnamese, or difficulty

### ⚙️ Customizable Settings
- Appearance customization (fonts, colors, window size)
- Default preferences for flashcard sessions

### 🎓 Learning Features
- Optional "Show Answer" with penalty system
- Score tracking and statistics
- Detailed results with accuracy percentages
- Visual feedback for correct/incorrect answers

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone the repository** (if using git):
   ```bash
   cd /path/to/tak_flashcard
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify vocabulary data**:
   - The application includes a vocabulary CSV file with 1000+ words
   - Located at: `src/tak_flashcard/data/vocab/vocab_source.csv`

## How to Run

Run the application (ensure `src` is on `PYTHONPATH`):

```bash
PYTHONPATH=src python -m tak_flashcard.main
```

Or from within the src directory:

```bash
cd src
python -m tak_flashcard.main
```

## Usage Guide

### Starting a Flashcard Session

1. Click **"Flashcard"** from the home screen
2. Configure your session:
   - **Mode**: Choose Endless, Speed, or Testing
   - **Direction**: Select translation direction
   - **Difficulty**: Adjust from 1 (easiest) to 5 (hardest)
  - **Additional options**: Set question count (Testing mode) and time limit (Speed mode), plus penalty type
3. Click **"Start Session"**
4. Answer questions by selecting one of four options (1 correct + 3 random distractors)
5. View your results at the end

### Using the Dictionary

1. Click **"Dictionary"** from the home screen
2. Browse all vocabulary words
3. Use the search bar to find specific words
4. Filter by part of speech (noun, verb, adjective, etc.)
5. Sort by English, Vietnamese, or difficulty level

### Reading the Guide

Click **"Guide"** from the home screen for comprehensive instructions on:
- Flashcard modes and their features
- Translation directions
- Difficulty levels
- Penalty system
- Scoring rules
- Tips for effective learning

### Adjusting Settings

1. Click **"Settings"** from the home screen
2. Customize appearance (font, pixel size, colors, window size)
3. Set default preferences for flashcard sessions
4. Enable/disable sound effects and animations
5. Click **"Save & Apply"** to save changes

## Difficulty System

The difficulty setting controls word selection probability:

- **Level 1**: Heavily favors words you know well
- **Level 2**: Slightly favors easier words
- **Level 3**: Equal probability for all words
- **Level 4**: Slightly favors challenging words
- **Level 5**: Heavily favors your most difficult words

Word difficulty is calculated dynamically based on:
- Number of times displayed
- Number of correct answers
- Formula: `difficulty = 1 - (correct_count / display_count)`

## Penalty System

When "Show Answer" is enabled:

- **Score Deduction**: -10 points per use (Endless/Speed)
- **Time Deduction**: -10 seconds per use (Speed only)
- **HP Limit**: Maximum 3 uses per session (Endless/Speed)

## Scoring

- **Correct Answer**: +10 base points
- **Speed Bonus**: Up to +10 points for quick answers (Speed mode)
- **Show Answer Penalty**: -10 points or -10 seconds
- **Final Results**: Total score, accuracy percentage, correct/incorrect breakdown

## Project Structure

```
tak_flashcard/
├── src/
│   └── tak_flashcard/
│       ├── main.py              # Application entry point
│       ├── config.py            # Configuration settings
│       ├── constants.py         # Enums and constants
│       ├── db/                  # Database layer
│       ├── data/                # Data storage and import
│       ├── core/                # Core business logic
│       ├── features/            # Feature modules
│       ├── gui/                 # GUI views and components
│       └── utils/               # Utility functions
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## Technology Stack

- **Python 3.8+**: Core programming language
- **Tkinter**: GUI framework for desktop interface (built-in with Python)
- **ttk**: Themed widget set for modern UI components
- **SQLAlchemy**: ORM for database management
- **SQLite**: Embedded database for storing vocabulary and statistics

## Database Schema

### Words Table
- `english`: English word
- `vietnamese`: Vietnamese translation
- `part_of_speech`: noun, verb, adjective, etc.
- `display_count`: Number of times shown
- `correct_count`: Number of correct answers
- `difficulty`: Calculated difficulty score (0-1)

### Sessions Table (Optional)
- Session metadata and statistics
- Mode, direction, difficulty settings
- Scores and performance metrics

## Troubleshooting

### Application won't start
- Ensure Python 3.8+ is installed
- Install all dependencies: `pip install -r requirements.txt`
- Check that the vocabulary CSV file exists

### Database errors
- Delete the `flashcard.db` file to reset the database
- The application will recreate it on next startup

### Import errors
- Ensure the vocabulary CSV file is in the correct location
- Format: `english,vietnamese,part_of_speech`
- At least 1000 words required

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## License

This project is available for educational purposes.

## Author

AKT311209

## Version

1.0.0

---

**Happy Learning! 📚✨**

## Features

- **Multiple Study Modes**
  - Endless: Practice without time limits
  - Speed: Race against the clock
  - Testing: Test your knowledge with limited HP

- **Flexible Learning Directions**
  - English → Vietnamese
  - Vietnamese → English
  - Mixed (random direction)

- **Dictionary Browser**
  - Search and browse vocabulary
  - View word details with examples
  - Edit and manage words

- **Import/Export**
  - Import vocabulary from CSV/XLSX files
  - Export your progress and results

- **Session Tracking**
  - Track your learning progress
  - Review past sessions and results
  - See your accuracy and improvement

## Project Structure

```
tak_flashcard/
├── src/
│   └── tak_flashcard/
│       ├── gui/              # Tkinter views and widgets
│       ├── core/             # Session engine, scoring, session models
│       ├── db/               # Database models and access layer
│       ├── importers/        # CSV/JSON/XLSX import helpers
│       ├── assets/           # Images, sounds, intro.mp4
│       └── settings.py       # Persistent settings
├── data/                     # Sample import files
├── tests/                    # Test suite
├── scripts/                  # Helper scripts
├── requirements.txt          # Runtime dependencies
└── requirements-dev.txt      # Development dependencies
```

## Installation

### Prerequisites

- Python 3.10 or higher
- pip or poetry for package management

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd tak_flashcard
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate  # On Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. (Optional) Install development dependencies: (this repository does not include a dev requirements file)

5. Initialize the database:
```bash
python scripts/init_db.py
```

6. (Optional) Seed with sample data:
```bash
python scripts/seed_db.py
# or import from CSV
python scripts/import_csv.py data/sample_words.csv
```

## Running the Application

From the project root directory with `src` in your PYTHONPATH:

```bash
# Run as module (recommended)
python -m tak_flashcard.gui.app

# Or set PYTHONPATH explicitly
PYTHONPATH=src python -m tak_flashcard.gui.app
```

## Usage

### Importing Vocabulary

The built-in vocabulary dataset lives at `src/tak_flashcard/data/vocab/vocab_source.csv`. If you need to refresh or replace the data, provide a CSV with the following required columns:

- `english`: English word
- `vietnamese`: Vietnamese translation
- `part_of_speech`: noun, verb, adjective, etc.

The importer expects at least 1000 rows, each normalized to NFC. When the application starts, it checks whether the database has enough words and automatically imports the CSV if needed.

You can edit the CSV manually or regenerate it from another source as long as the column order stays the same. After replacing the file, delete `src/tak_flashcard/data/flashcard.db` (if present) so the next run rebuilds the schema and data.

### Starting a Session

1. Launch the application
2. Go to the **Flashcard** tab
3. Configure your session:
   - Choose a mode (Endless, Speed, Testing)
   - Select direction (E→V, V→E, Mixed)
   - Set difficulty level (1-5)
   - Set number of questions
4. Click **Start Session**
5. Answer questions by selecting one of four options (1 correct + 3 random distractors)
6. Use **Reveal** button if you need help (penalty applied)
7. Review your results at the end

## Development

### Running Tests

This project does not include a test suite. Test files and related configuration were removed from the repository.

### Code Formatting and Linting

```bash
# Format code
black src tests

# Sort imports
isort src tests

# Lint
ruff check src tests

# Type check
mypy src
```

### Database Scripts

```bash
# Initialize database
python scripts/init_db.py

# Import CSV/XLSX
python scripts/import_csv.py data/sample_words.csv

# Seed with sample data
python scripts/seed_db.py
```

## Architecture

### Database

- **Engine**: SQLite with SQLAlchemy ORM
- **Location**: `~/.tak_flashcard/tak_flashcard.db`
- **Tables**:
  - `words`: Vocabulary entries
  - `sessions`: Study session records
  - `session_results`: Individual question results
  - `settings`: Application settings

### Core Components

- **Session Engine** (`core/session_engine.py`): Manages study sessions, scoring, and question flow
- **Database Layer** (`db/`): SQLAlchemy models and database access
- **Importers** (`importers/`): CSV/XLSX import functionality
- **GUI** (`gui/`): Tkinter interface with ttk themed widgets
- **Settings** (`settings.py`): Persistent application settings

## Contributing

1. Follow the coding style in `AGENTS.md`
2. Add tests for new features
3. Run linters and tests before committing
4. Keep commits focused and descriptive

## License

[Add your license here]

## Credits

Built with:
- [Tkinter](https://docs.python.org/3/library/tkinter.html) - GUI framework (Python standard library)
- [SQLAlchemy](https://www.sqlalchemy.org/) - Database ORM
- [Pandas](https://pandas.pydata.org/) - Data processing
