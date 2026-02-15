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
- [ ] Find/prepare CSV with ≥1000 English-Vietnamese words
  - Required columns: `english`, `vietnamese`, `part_of_speech`
  - Source: GitHub vocabulary lists, public datasets
- [ ] Implement importer (`data/seed/importer.py`)
  - Parse CSV/TSV files
  - Validate data format
  - Bulk insert to database
  - Show import progress
- [ ] Add startup validation
  - Check if DB has ≥1000 words
  - Trigger import if needed
  - Display error if import fails

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
- [ ] Mode selection: Endless / Speed / Testing
- [ ] Direction selection: Eng→Vn / Vn→Eng / Mixed
- [ ] Difficulty slider: 1 (easiest) to 5 (hardest)
- [ ] Additional settings:
  - Question count (Testing mode)
  - Time limit (Speed mode)
  - Enable Show Answer (Endless/Speed)
  - Penalty type (if Show Answer enabled)

### 4.2 Endless Mode
- [ ] Implement Endless controller (`features/flashcard/controller.py`)
- [ ] Create flashcard view (`gui/views/flashcard_view.py`)
  - Display question
  - Input area or multiple choice
  - Submit button
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

### 4.4 Testing/Exam Mode
- [ ] Extend controller for Testing mode
- [ ] Display question counter (e.g., "5/20")
- [ ] No Show Answer option
- [ ] Implement scoring system
- [ ] Create results view (`gui/views/results_view.py`)
  - Total score
  - Correct/Wrong count
  - Breakdown by direction
  - Review wrong answers (optional)
  - Retry button
  - Back to home button

### 4.5 Answer Validation
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
- [ ] Add sorting
  - Sort by English alphabetically
  - Sort by difficulty

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
      "theme": "light",
      "font_size": "medium",
      "window_width": 800,
      "window_height": 600
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
  - Theme selector (Light/Dark/Custom)
  - Font size slider/dropdown
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
- [ ] Apply theme settings to all views
- [ ] Apply font size to all text elements
- [ ] Load default values in Flashcard configuration
- [ ] Persist settings on app close
- [ ] Load settings on app start

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
✅ Scoring and results display for Testing mode  
✅ Persistent user settings (appearance and preferences)
✅ Stable operation on Windows OS  
✅ Video intro ≤5 minutes demonstrating all features
