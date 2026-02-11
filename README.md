# Tak Flashcard

A Vietnamese-English vocabulary learning application built with Python and DearPyGui.

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
│       ├── gui/              # DearPyGui views and widgets
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

4. (Optional) Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

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

You can import vocabulary from CSV or XLSX files. The file should have the following columns:

**Required columns:**
- `word`: English word
- `meaning_vn`: Vietnamese meaning

**Optional columns:**
- `pos`: Part of speech (noun, verb, adjective, etc.)
- `pronunciation`: Pronunciation guide (IPA)
- `meaning_en`: English definition
- `example_en`: English example sentence
- `example_vn`: Vietnamese example sentence
- `audio_url`: URL to audio file
- `image_url`: URL to image file
- `difficulty`: Difficulty level (1-5)
- `tags`: Comma-separated tags
- `frequency_rank`: Word frequency rank

Example CSV:
```csv
word,meaning_vn,pos,difficulty
hello,xin chào,interjection,1
goodbye,tạm biệt,interjection,1
friend,bạn bè,noun,1
```

Import via script:
```bash
python scripts/import_csv.py path/to/your/words.csv
```

Or use the Import tab in the GUI.

### Starting a Session

1. Launch the application
2. Go to the **Flashcard** tab
3. Configure your session:
   - Choose a mode (Endless, Speed, Testing)
   - Select direction (E→V, V→E, Mixed)
   - Set difficulty level (1-5)
   - Set number of questions
4. Click **Start Session**
5. Answer questions by typing your response
6. Use **Reveal** button if you need help (penalty applied)
7. Review your results at the end

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=tak_flashcard --cov-report=html

# Run specific test file
pytest tests/test_models.py

# Run specific test
pytest tests/test_models.py::test_create_word
```

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
- **GUI** (`gui/`): DearPyGui interface
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
- [DearPyGui](https://github.com/hoffstadt/DearPyGui) - GUI framework
- [SQLAlchemy](https://www.sqlalchemy.org/) - Database ORM
- [Pandas](https://pandas.pydata.org/) - Data processing