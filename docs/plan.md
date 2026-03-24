# Implementation Plan

## Phase 1: Data Layer & Import

### 1.1 Database Setup
- [ ] Create SQLAlchemy models (`db/models.py`)
  - Word model with all 7 fields
  - Session model (optional, for history tracking)
- [ ] Setup database session management (`db/session.py`)
- [ ] Create repository layer for queries (`db/repo.py`)
  - Get words by difficulty
  - Get words by part of speech
  - Update display/correct counts
  - Search words

### 1.2 Data Import
- [x] Implement importer (`data/seed/importer.py`)
  - Parse CSV files
  - Validate column structure (`english`, `vietnamese`, `part_of_speech`)
  - Bulk insert to database
  - Manual import via GUI (Import Vocabulary view) with Replace / Append modes
  - Timestamped backup written to `data/vocab/` before every import
- [x] Add startup validation
  - Check if DB has any words on launch
  - If empty: redirect to Import View in forced mode (Back button hidden, warning banner shown)
  - After a successful forced import: auto-navigate to Home

### 1.3 Testing
- [ ] Verify database schema
- [ ] Test import with sample CSV
- [ ] Confirm ≥1000 words loaded correctly

---

## Phase 2: Core Logic

### 2.1 Difficulty Calculation
- [ ] Implement difficulty formula (`core/difficulty.py`)
  ```python
  difficulty = 1 - (correct_count / (display_count + epsilon))
  ```
- [ ] Normalize difficulty to 0-1 scale for each word
- [ ] No filtering - all words remain available

### 2.2 Question Selection
- [ ] Implement card selector (`core/selectors.py`)
  - Weighted selection based on difficulty setting (1-5)
  - Higher setting → higher probability of high-difficulty words
  - Select by direction (Eng→Vn, Vn→Eng, Mixed)
  - Randomization with weighted probabilities
  - Avoid immediate repetition

### 2.3 Scoring & Penalty System
- [ ] Implement scoring logic (`core/scoring.py`)
  - Base points for correct answer
  - Bonus points for speed (Speed mode)
  - Penalty for wrong answer
- [ ] Implement penalty mechanisms
  - Score deduction
  - Time penalty (reduce remaining time)
  - HP/show answer limit
- [ ] Track session statistics

### 2.4 Timer Logic
- [ ] Implement countdown timer (`core/scheduler.py`)
  - For Speed mode
  - Timer callbacks
  - Pause/resume functionality

---

## Phase 3: GUI Foundation (Week 3)

### 3.1 Tkinter Setup
- [ ] Initialize Tkinter application (`gui/app.py`)
- [ ] Setup main window with ttk theming
- [ ] Create navigation system between frames/views
- [ ] Define window layout (header, content, footer)
- [ ] Configure grid/pack layout managers

### 3.2 Home View
- [ ] Create home view (`gui/views/home_view.py`)
- [ ] Add navigation buttons:
  - Flashcard
  - Dictionary
  - Guide
  - Settings
  - Exit
- [ ] Display app title and brief instructions
- [ ] Implement frame switching logic

### 3.3 Reusable Components
- [ ] Toolbar component (`gui/components/toolbar.py`)
  - Back button
  - Home button
  - Settings button (optional)
- [ ] Create consistent styling with ttk.Style
- [ ] Base frame class for common functionality

---

## Phase 4: Flashcard Feature

### 4.1 Configuration Panel
- [ ] Create option panel (`gui/components/option_panels.py`)
- [ ] Keep flashcard settings in dedicated configuration view (`gui/views/flashcard_view.py`)
- [ ] Mode selection: Endless / Speed / Testing
- [ ] Direction selection: Eng→Vn / Vn→Eng / Mixed
- [ ] Difficulty slider: 1 (easiest) to 5 (hardest)
- [ ] Additional settings:
  - Question count (Testing mode; visible only when Testing selected)
  - Time limit (Speed mode; visible only when Speed selected)
  - Enable Show Answer (Endless/Speed)
  - Penalty type (if Show Answer enabled)
- [ ] Add **START SESSION** action to navigate from settings view to a separate session view

### 4.2 Endless Mode
- [ ] Implement Endless controller (`features/flashcard/controller.py`)
- [ ] Create dedicated flashcard session view (`gui/views/flashcard_view.py` → `FlashcardSessionView`)
  - Display question
  - Multiple-choice options (4 choices: 1 correct + 3 random distractors)
  - Auto-submit on choice selection (no separate Submit button)
  - Next button
  - Show Answer button (optional)
- [ ] Implement state machine (`features/flashcard/states.py`)
  - Question → Answer → Result → Next Question
- [ ] Track statistics (no time limit)
- [ ] No automatic ending

### 4.3 Speed/Timer Mode
- [ ] Extend controller for Speed mode
- [ ] Add countdown timer display
- [ ] Implement time penalties for Show Answer
- [ ] Auto-end when time runs out
- [ ] Display score during session
- [ ] Record `time_used` (time_limit − remaining) for the session summary

### 4.4 Testing/Exam Mode
- [ ] Extend controller for Testing mode
- [ ] Display question counter (e.g., "5/20")
- [ ] No Show Answer option
- [ ] Implement scoring system
- [ ] Navigate to Session Summary after final question

### 4.5 Session Summary View
- [ ] Create `SessionSummary` dataclass (`features/flashcard/states.py`)
  - `correct`, `asked`, `percent_correct`
  - `score`
  - `time_used` (Speed mode only)
  - `show_used` (Endless/Speed only)
- [ ] Add `get_summary()` to `FlashcardService` and `FlashcardController`
- [ ] Implement `ResultsView` (`gui/views/results_view.py`)
  - Always show: Correct / Total (%), Score
  - Speed mode only: Time Used (formatted as Xm Ys)
  - Non-Testing only: Show Answer Uses
  - **Play Again** button → Flashcard Settings view
  - **Home** button → Home screen
- [ ] Auto-navigate to summary:
  - After 1.5 s delay when session ends naturally (timer expires / question limit reached)
  - Immediately when user clicks "Back to Settings" (early exit)

### 4.6 Answer Validation
- [ ] Implement answer checking logic
  - Case-insensitive comparison
  - Trim whitespace
  - Partial match (optional, for Vietnamese diacritics)
- [ ] Update word statistics (display_count, correct_count)

---

## Phase 5: Dictionary Feature

### 5.1 Dictionary View
- [ ] Create dictionary view (`gui/views/dictionary_view.py`)
- [ ] Display all words in table/list
  - Columns: English, Vietnamese, Part of Speech
- [ ] Implement search functionality
  - Search by English word
  - Search by Vietnamese word
- [ ] Add filters
  - Filter by Part of Speech
  - Filter by difficulty level (optional)
- [x] Add column-header sorting
  - Click a column heading to sort ascending (▲); click again to sort descending (▼)
  - Only one column is active at a time; selecting a new column resets to ascending
  - `difficulty` column sorts numerically; all other columns sort case-insensitively
  - Sort state is preserved after a search or full refresh

### 5.2 Dictionary Service
- [ ] Implement dictionary service (`features/dictionary/service.py`)
  - Fetch all words
  - Search words
  - Filter/sort logic

---

## Phase 6: Guide Feature

### 6.1 Guide View
- [ ] Create guide view (`gui/views/guide_view.py`)
- [ ] Display static guide content

### 6.2 Guide Content
- [ ] Write comprehensive guide (`features/guide/content.py`)
  - Introduction to app
  - Flashcard modes explanation
    - Endless mode
    - Speed/Timer mode
    - Testing/Exam mode
  - Direction types (Eng→Vn, Vn→Eng, Mixed)
  - Difficulty levels
  - Penalty system
  - Scoring rules
  - Tips for effective learning

---

## Phase 6.5: Settings Feature (Week 6)

### 6.5.1 Settings Data Management
- [ ] Create settings manager (`core/settings.py`)
  - Load settings from JSON file
  - Save settings to JSON file
  - Provide default settings
  - Validate setting values
- [ ] Define settings schema in `data/user_settings.json`
  ```json
  {
    "appearance": {
      "font_name": "Arial",
      "font_size_px": 11,
      "background_color": "#ffffff",
      "text_color": "#000000",
      "secondary_color": "#f0f0f0",
      "window_width": 960,
      "window_height": 640
    },
    "defaults": {
      "flashcard_mode": "endless",
      "difficulty_level": 3,
      "question_count": 20,
      "time_limit": 300
    },
    "preferences": {
      "sound_enabled": false,
      "animation_speed": "normal"
    }
  }
  ```

### 6.5.2 Settings View
- [ ] Create settings view (`gui/views/settings_view.py`)
- [ ] Implement appearance settings section
  - Font selector (choose font family)
  - Font size input (pixels)
  - Color inputs for background/text/secondary elements
  - Window size inputs
- [ ] Implement default preferences section
  - Default flashcard mode
  - Default difficulty level
  - Default question count
  - Default time limit
- [ ] Implement UI preferences section
  - Sound effects toggle
  - Animation speed selector
- [ ] Add Save/Apply/Reset buttons
- [ ] Add Back button to return to home

### 6.5.3 Settings Integration
- [ ] Apply appearance fonts and colors to all views
- [ ] Load default values in Flashcard configuration
- [ ] Persist settings on app close
- [ ] Load settings on app start

---

## Phase 6.7: Import Vocabulary Feature

### 6.7.1 Importer Logic (`data/seed/importer.py`)
- [x] `validate_csv_file(path)` — checks file existence, encoding, required columns, and non-empty rows; returns a list of error messages
- [x] `import_vocab_file(db, source, replace)` — orchestrates validate → backup → (optional clear) → bulk insert → commit
- [x] `ImportResult` dataclass — carries `added`, `removed`, `backup_path`, `errors`
- [x] `_backup_vocab(source)` — copies user CSV to `data/vocab/vocab_source_<YYYYMMDD_HHMMSS>.csv`

### 6.7.2 Repository (`db/repo.py`)
- [x] `clear_all_words(db)` — deletes every word row and returns the count removed (used by Replace mode)

### 6.7.3 Import View (`gui/views/import_view.py`)
- [x] Header and collapsible Guide panel explaining required columns and modes
- [x] File picker row (Browse… opens native file dialog, filters to `*.csv`)
- [x] Import Mode selector: **Append** (default) / **Replace**
- [x] Import button (disabled until a file is selected)
- [x] Status area: green on success, red on validation failure
  - Success message shows: words added, words removed (Replace only), backup path
- [x] Back button returns to Home (hidden in forced mode)
- [x] Forced mode: triggered on startup when DB is empty
  - Warning banner prompts user to import before proceeding
  - Back button hidden; user cannot leave without importing
  - Auto-navigates to Home after a successful import

### 6.7.4 Home Screen Integration
- [x] **Import Vocabulary** button added to `HomeView` between Guide and Settings

---

## Phase 7: Polish & Testing (Week 7)

### 7.1 Windows Compatibility
- [ ] Test on Windows OS
- [ ] Verify all file paths work on Windows
- [ ] Check Tkinter rendering on Windows
- [ ] Test ttk themed widgets on Windows
- [ ] Bundle dependencies with `requirements.txt`

### 7.2 Error Handling
- [ ] Add try-catch blocks for file operations
- [ ] Validate user inputs
- [ ] Handle edge cases:
  - No words in database
  - Invalid CSV format
  - Database connection errors

### 7.3 User Experience
- [ ] Ensure readable text in all views
- [ ] Test navigation flows
- [ ] Add loading indicators for long operations
- [ ] Optimize performance for large datasets

### 7.4 Code Quality
- [ ] Add docstrings to all functions
- [ ] Clean up unused code
- [ ] Consistent naming conventions
- [ ] Code review

---

## Phase 8: Documentation & Video (Week 8)

### 8.1 README
- [ ] Write comprehensive README.md
  - Project description
  - Installation instructions
  - How to run
  - Feature list
  - Screenshots (optional)

### 8.2 Video Intro (≤5 minutes)
- [ ] Script preparation
  - 30s: Introduction and tech stack
  - 2 min: Demo Flashcard modes (Endless + Speed)
  - 1 min: Testing mode + results
  - 30s: Dictionary + Guide
  - 30s: Conclusion and highlights
- [ ] Record on Windows OS
- [ ] Edit video
- [ ] Add captions (optional)

---

## Dependencies (requirements.txt)

```
sqlalchemy>=2.0.0
pandas>=1.5.0
```

**Note:** Tkinter is included with Python standard library, no separate installation required.

---

## Success Criteria

✅ Database contains ≥1000 words imported from external file  
✅ Three main features: Flashcard, Dictionary, Guide  
✅ Settings feature for user customization
✅ 9 study modes (3 flashcard modes × 3 directions)  
✅ Configurable difficulty, question count, time limit  
✅ Penalty system for Show Answer feature  
✅ Scoring and session summary for all three modes (correct %, score, time, show-answer uses)  
✅ Persistent user settings (appearance and preferences)
✅ Stable operation on Windows OS  
✅ Video intro ≤5 minutes demonstrating all features
