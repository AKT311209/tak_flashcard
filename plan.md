Project structure

```
tak_flashcard/
├─ src/
│     ├─ gui/               # DearPyGui views and widgets
│     ├─ core/              # session engine, scoring, session models
│     ├─ db/                # db.py, models.py (SQLAlchemy), migrations
│     ├─ importers/         # CSV/JSON/XLSX import helpers (pandas)
│     ├─ assets/            # images, sounds, intro.mp4
│     └─ settings.py        # persistent settings (JSON)
├─ data/                    # sample import files
│  └─ sample_words.csv
├─ tests/
├─ scripts/                 # seed, build, packaging helpers
├─ requirements.txt
└─ README.md
```

Implementation steps (very detailed)

1) Scaffold project
- Create virtualenv or use `poetry` and add `requirements.txt` with `dearpygui, pandas, SQLAlchemy, python-dotenv`.
- Create folder structure and `__init__.py` files for packages.
- Add simple entry point `src/tak_flashcard/gui/app.py` that starts DearPyGui.

2) Database layer
- Design models in `src/tak_flashcard/db/models.py`: `words`, `sessions`, `session_results`, `settings`.
- Implement `src/tak_flashcard/db/db.py` with `create_engine`, `SessionLocal`, `init_db()` and `connect_args={'check_same_thread': False}`.
- Add `scripts/init_db.py` to call `init_db()` and create necessary indexes.

3) Importer
- Implement `src/tak_flashcard/importers/csv_importer.py`:
  - Read CSV/XLSX with `pandas.read_csv/read_excel`; fallback to builtin `csv`.
  - Normalize column names to lowercase; require `word` and `meaning_vn`.
  - Trim whitespace, drop empty rows, drop duplicates (by normalized word).
  - Batch-insert to DB with SQLAlchemy in chunks (e.g., 500 rows) inside transactions.
  - Return `{added, skipped, errors}` and log summary.
  - Provide CLI `scripts/import_csv.py` to run import from command line.

4) Core session engine (`src/tak_flashcard/core/`)
- Implement `Session` class (in-memory) with fields: `id, mode, direction, question_count, time_per_question, total_time, reveal_hp, score, queue, current_index, started_at, results`.
- Functions to implement:
  - `create_session(opts)` — build queue from DB filters (difficulty, tags), randomize if needed.
  - `session_next(session)` — return next Question (word, prompt, choices if MCQ).
  - `session_submit(session, answer)` — evaluate correctness (normalize & fuzzy options), update score, record result.
  - `session_reveal(session)` — return answer and apply configured penalty (points/time/HP).
  - `end_session(session)` — persist session summary and per-question results to DB.
- Implement scoring rules and penalty behavior configurable by session options.
- Ensure long operations run in worker threads; communicate with GUI via thread-safe queues or DearPyGui callbacks.

5) GUI implementation (DearPyGui)
- Main shell: top nav (Flashcard / Dictionary / Guide), Import button, Settings.
- Import UI: file picker, start import in background, progress bar, final stats display.
- Dictionary UI: searchable/paginated table (add_table) with filters; open WordDetail modal for details and edit.
- Flashcard UI:
  - Config panel: mode, direction, difficulty, question count, time settings, reveal options, penalty settings.
  - Session view: card area (prompt), input or choices, Reveal button, Submit/Next, Timer bar (for Speed), Score/Hp display.
  - Result modal: final score, accuracy, wrong list, buttons to review/export.
- Guide view: load and render `assets/guide.md` (plain text or rendered HTML).
- Settings modal: volume, animation toggle, default penalty presets; persist to `settings` table or JSON.

6) Multimedia & assets
- Integrate audio playback via `python-vlc` or OS audio APIs; expose volume control in Settings.
- Load images and ensure card text sits on semi-opaque background to maintain readability.

7) Persistence & utilities
- Save session summaries to `sessions` and detailed rows to `session_results`.
- Add utility scripts: `scripts/export_words.py`, `scripts/backup_db.py`.

8) Tests & packaging
- Unit tests (`pytest`) for importer, session engine, DB functions; use SQLite in-memory for tests.
- Create `scripts/build_windows.bat` or `build_windows.sh` using PyInstaller to bundle app and assets into a Windows exe.

Application flow

- Launch: app opens main shell with Mode selector, Import, Settings.
- Import flow: user picks CSV/XLSX -> clicks Import -> importer runs in background -> progress shown -> final stats shown.
- Dictionary flow: user searches/filters -> selects word -> WordDetail modal (audio, image, edit/save).
- Guide flow: user reads usage guide explaining modes and controls.
- Flashcard flow (detailed):
  1. Pre-config: user selects Mode (Endless/Speed/Testing), Direction (E->V/V->E/Mixed), Difficulty, Question count, Time settings, Reveal/penalty options.
  2. Create session: app builds question queue from DB (worker thread), then starts session and timer if applicable.
  3. Per question: show prompt; user answers (text or choose). If Reveal used, `session_reveal` applies penalty and decrements HP. On Submit, `session_submit` evaluates and updates score.
  4. Progress: UI shows timer (Speed), score, remaining reveal HP, and question index.
  5. End: when questions exhausted or time runs out, `end_session` persists results; UI shows summary with review/export options.

Database system

- Engine: SQLite file `tak_flashcard.db` stored in app folder or user data directory.
- Access layer: SQLAlchemy ORM (`create_engine('sqlite:///path', connect_args={'check_same_thread': False})`, `SessionLocal = sessionmaker(bind=engine)`).
- Tables (concise schema):

```
words(id PK, word TEXT, pos TEXT, pronunciation TEXT, meaning_vn TEXT, meaning_en TEXT, example_en TEXT, example_vn TEXT, audio_url TEXT, image_url TEXT, difficulty INT, tags TEXT, frequency_rank INT)
sessions(id PK, mode TEXT, direction TEXT, start_ts TEXT, end_ts TEXT, score INT, total_questions INT)
session_results(id PK, session_id FK, word_id FK, asked_text TEXT, expected_answer TEXT, given_answer TEXT, correct INT, revealed INT, penalty INT)
settings(key PK, value TEXT)
```

- Indexes: create indexes on `words.word`, `words.difficulty`, and `words.tags`.
- Concurrency: use one SQLAlchemy Session per thread; avoid sharing sessions across threads. Use `connect_args={'check_same_thread': False}` for SQLite.
- Import/seed scripts: `scripts/import_csv.py` and `scripts/seed_db.py` to populate `words` from `data/sample_words.csv`.
- Backup & export: `scripts/backup_db.py` and `scripts/export_csv.py` for safe copies and exports.
