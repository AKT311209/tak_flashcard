# Function Role Map (What each function does, and when it runs)

This document is written for non-technical readers and reviewers.

- **Role** = why this function exists.
- **Called when** = what user/system action triggers it.

---

## Entry and configuration

### `src/tak_flashcard/main.py`

- `main()`
  - **Role**: application start pipeline.
  - **Called when**: user launches app module.

### `src/tak_flashcard/config.py`

- `_get_data_dir()`
  - **Role**: decide where app data should be stored.
  - **Called when**: config constants are initialized.
- `ensure_data_dirs()`
  - **Role**: create required data folders.
  - **Called when**: app startup.
- `ensure_executable_data_dirs()`
  - **Role**: ensure data folders exist when running packaged executable.
  - **Called when**: pre-start checks in entry flow.

---

## Database layer

### `src/tak_flashcard/db/session.py`

- `init_db()`
  - **Role**: create database tables if missing.
  - **Called when**: app startup.

### `src/tak_flashcard/db/models.py`

- `Word.to_dict()`
  - **Role**: convert a `Word` row into dictionary-like data.
  - **Called when**: data needs display/export-ready structure.

### `src/tak_flashcard/db/repo.py`

- `get_word_count(db)`
  - **Role**: count words in database.
  - **Called when**: startup routing and import forced-mode checks.
- `bulk_insert_words(db, words)`
  - **Role**: insert many rows efficiently.
  - **Called when**: replace import workflow.
- `find_word_by_english(db, english)`
  - **Role**: find existing word by english key.
  - **Called when**: append import deduplication.
- `upsert_words_append(db, rows, overwrite_duplicates, reset_difficulty)`
  - **Role**: append/update import behavior.
  - **Called when**: append import workflow.
- `clear_all_words(db)`
  - **Role**: remove all word rows.
  - **Called when**: replace import workflow.
- `list_words(db)`
  - **Role**: fetch all words.
  - **Called when**: flashcard service load + dictionary refresh.
- `search_words(db, query)`
  - **Role**: text search across english/vietnamese.
  - **Called when**: user searches in dictionary.
- `filter_by_part_of_speech(db, part)`
  - **Role**: filter rows by part of speech.
  - **Called when**: dictionary filtering.
- `update_word_stats(db, word_id, is_correct)`
  - **Role**: increment counters and recalculate difficulty for a word.
  - **Called when**: user selects an answer choice (auto-submitted).

---

## Core logic layer

### `src/tak_flashcard/core/difficulty.py`

- `difficulty_score(display_count, correct_count)`
  - **Role**: calculate difficulty metric from performance.
  - **Called when**: word stats are updated.

### `src/tak_flashcard/core/scoring.py`

- `apply_scoring(current_score, correct, penalty_points)`
  - **Role**: return new score and delta.
  - **Called when**: an answer choice is auto-submitted.

### `src/tak_flashcard/core/selectors.py`

- `select_next_word(words, difficulty_level, direction)`
  - **Role**: wrapper entry for weighted next-word selection.
  - **Called when**: flashcard service asks for a new card.
- `_choose_weighted_word(words, difficulty_level, _direction)`
  - **Role**: run weighted random draw.
  - **Called when**: `select_next_word` is executed.
- `_clamp_difficulty(level)`
  - **Role**: keep difficulty within valid range.
  - **Called when**: weighted draw begins.
- `_calculate_difficulty_weight(level, base)`
  - **Role**: compute per-word selection weight.
  - **Called when**: each word is scored during weighted draw.

### `src/tak_flashcard/core/scheduler.py` (`CountdownTimer` methods)

- `start()`
  - **Role**: begin countdown.
  - **Called when**: Speed session starts.
- `stop()`
  - **Role**: stop timer and callbacks.
  - **Called when**: session ends/exits.
- `pause()`
  - **Role**: pause countdown.
  - **Called when**: feedback shown between questions.
- `resume()`
  - **Role**: continue countdown.
  - **Called when**: next question starts.
- `tick()`
  - **Role**: update remaining seconds.
  - **Called when**: periodic UI timer callback runs.
- `deduct(seconds)`
  - **Role**: subtract penalty time.
  - **Called when**: show-answer time penalty applies.

### `src/tak_flashcard/core/settings.py`

- `Settings.to_dict()`
  - **Role**: convert settings object to JSON-serializable dict.
  - **Called when**: saving settings.
- `Settings.from_dict(data)`
  - **Role**: build settings object from JSON data.
  - **Called when**: loading settings.
- `SettingsManager.load()`
  - **Role**: read settings file from disk.
  - **Called when**: app startup and manager initialization.
- `SettingsManager.save(settings)`
  - **Role**: persist settings to disk.
  - **Called when**: user clicks Save in Settings screen.

---

## Data import layer

### `src/tak_flashcard/data/seed/importer.py`

- `read_csv_headers(path)`
  - **Role**: read CSV header list.
  - **Called when**: user chooses CSV file.
- `_parse_csv_rows(path, column_map)`
  - **Role**: parse normalized rows from mapped columns.
  - **Called when**: import starts.
- `_backup_vocab(source)`
  - **Role**: make timestamped backup copy of source file.
  - **Called when**: before database-changing import.
- `import_vocab_file(db, source, column_map, replace, overwrite_duplicates, reset_difficulty)`
  - **Role**: main import pipeline.
  - **Called when**: user clicks Import.

---

## Flashcard feature

### `src/tak_flashcard/features/flashcard/service.py` (`FlashcardService`)

- `load_words()`
  - **Role**: cache all words in memory for session.
  - **Called when**: new session starts.
- `start_session(config)`
  - **Role**: initialize session state from one config object.
  - **Called when**: user starts session from setup screen.
- `_pick_word()`
  - **Role**: choose and prepare next word + choices.
  - **Called when**: next card requested.
- `_resolve_direction(direction)`
  - **Role**: turn Mixed into one concrete direction.
  - **Called when**: preparing next card.
- `_answer_for(word, direction)`
  - **Role**: return expected answer text.
  - **Called when**: building choices and validating answers.
- `_build_choices(word, direction)`
  - **Role**: build shuffled options (1 correct + distractors).
  - **Called when**: preparing next card.
- `next_card()`
  - **Role**: enforce limits and return next word.
  - **Called when**: session view asks for new card.
- `submit_answer(answer)`
  - **Role**: validate answer, update DB stats, update score.
  - **Called when**: user chooses an answer option (auto-submit).
- `show_answer_penalty()`
  - **Role**: apply show-answer limits and penalties.
  - **Called when**: user presses Show Answer.
- `is_finished()`
  - **Role**: report whether session has ended.
  - **Called when**: controller/view checks end state.
- `get_summary()`
  - **Role**: build final stats object.
  - **Called when**: session ends.

### `src/tak_flashcard/features/flashcard/controller.py` (`FlashcardController`)

- `start(config)`
  - **Role**: pass session config into service.
  - **Called when**: session view begins session.
- `next_card()`
  - **Role**: request next card from service.
  - **Called when**: session view advances.
- `submit(answer)`
  - **Role**: submit answer through service.
  - **Called when**: session UI auto-submits the selected choice.
- `reveal()`
  - **Role**: request show-answer outcome.
  - **Called when**: Show Answer button used.
- `finished()`
  - **Role**: check finish status.
  - **Called when**: session flow checks completion.
- `get_summary()`
  - **Role**: retrieve completed summary.
  - **Called when**: session finishes.

---

## Dictionary feature

### `src/tak_flashcard/features/dictionary/service.py`

- `all_words()`
  - **Role**: provide full list for dictionary table.
  - **Called when**: dictionary view opens/refreshes.
- `search(query)`
  - **Role**: provide filtered list by text.
  - **Called when**: dictionary search triggered.
- `filter_part(part)`
  - **Role**: provide list filtered by part of speech.
  - **Called when**: dictionary filters are used.

---

## Guide feature

### `src/tak_flashcard/features/guide/content.py`

- `GUIDE_TEXT` (constant)
  - **Role**: static guide content.
  - **Called when**: guide view renders.

---

## GUI application shell

### `src/tak_flashcard/gui/app.py` (`FlashcardApp`)

- `__init__()`
  - **Role**: boot app, create all views, route first screen.
  - **Called when**: app launches.
- `apply_appearance(settings)`
  - **Role**: apply style updates immediately.
  - **Called when**: settings saved.
- `_on_session_end(summary)`
  - **Role**: push summary to results view and navigate there.
  - **Called when**: flashcard session finishes.
- `start_flashcard_session(config)`
  - **Role**: start active session screen from setup.
  - **Called when**: user presses Start Session.
- `navigate(key)`
  - **Role**: switch current screen.
  - **Called when**: any menu/back action occurs.
- `_update_global_shortcuts()`
  - **Role**: bind keyboard shortcuts by active screen.
  - **Called when**: navigation changes view.
- `_on_inner_configure(event)` / `_on_canvas_configure(event)`
  - **Role**: keep scroll layout correct.
  - **Called when**: UI size changes.
- `_bind_mousewheel(event)` / `_unbind_mousewheel(event)`
  - **Role**: enable/disable mouse wheel scrolling.
  - **Called when**: mouse enters/leaves app canvas.
- `run()`
  - **Role**: open main GUI loop.
  - **Called when**: app startup script executes.

---

## GUI views and components

### `gui/views/home_view.py` (`HomeView.__init__`)

- **Role**: create main menu buttons.
- **Called when**: app initializes screens.

### `gui/views/flashcard_view.py` (`FlashcardView`)

- `start_session()`
  - **Role**: read setup options and build `SessionConfig`.
  - **Called when**: Start Session button/Enter key.

### `gui/views/flashcard_view.py` (`FlashcardSessionView`)

- `begin_session(config)`
  - **Role**: initialize active run and first card.
  - **Called when**: app starts session screen.
- `next_card()`
  - **Role**: request and display next question.
  - **Called when**: session starts or user goes next.
- `submit_answer(answer)`
  - **Role**: process selected answer.
  - **Called when**: user selects a choice (auto-submit).
- `show_answer()`
  - **Role**: reveal answer with penalty logic.
  - **Called when**: user clicks Show Answer.
- `_handle_exit_session()`
  - **Role**: end session manually.
  - **Called when**: user clicks End Session or presses Escape.
- `_capture_time_used()`
  - **Role**: compute elapsed time for Speed mode.
  - **Called when**: session is ending.
- `_emit_session_end()`
  - **Role**: send final summary back to app shell.
  - **Called when**: session end pipeline completes.
- `_update_show_button_state()` / `_is_show_allowed()`
  - **Role**: manage Show Answer button availability.
  - **Called when**: card state changes.
- `_active_direction()`
  - **Role**: return effective direction for current card.
  - **Called when**: building prompt/answer.
- `_prompt_for(...)` / `_answer_for(...)`
  - **Role**: choose display text by direction.
  - **Called when**: rendering question and feedback.
- `_display_terminal_card(message)`
  - **Role**: show final non-interactive card state.
  - **Called when**: no cards remain or timer finished.
- `_start_timer(seconds)` / `_schedule_timer_tick()` / `_tick_timer()`
  - **Role**: timer lifecycle control.
  - **Called when**: Speed mode is active.
- `_update_timer_label(remaining)`
  - **Role**: update time text in UI.
  - **Called when**: timer ticks.
- `_apply_time_penalty(seconds)`
  - **Role**: deduct remaining time.
  - **Called when**: show-answer time penalty used.
- `_pause_timer()` / `_resume_timer()` / `_stop_timer()`
  - **Role**: timer state transitions.
  - **Called when**: card state/session state changes.
- `_handle_timer_finish()`
  - **Role**: auto-finish session when time reaches 0.
  - **Called when**: timer callback reports completion.
- `_show_timer_label()` / `_hide_timer_label()`
  - **Role**: show/hide timer UI.
  - **Called when**: mode changes and timer starts/stops.
- `on_enter_key()` / `on_space_key()` / `on_number_key(index)`
  - **Role**: keyboard handlers for session controls.
  - **Called when**: bound keys are pressed.

### `gui/views/dictionary_view.py` (`DictionaryView`)

- `_on_heading_click(col)`
  - **Role**: toggle sorting column/order.
  - **Called when**: user clicks a table header.
- `_apply_sort()`
  - **Role**: apply current sort to rows.
  - **Called when**: sort state changes.
- `_refresh_headings()`
  - **Role**: display ▲/▼ indicators.
  - **Called when**: sort state changes.
- `_populate(words)`
  - **Role**: render table rows.
  - **Called when**: refresh/search results update.
- `refresh()`
  - **Role**: load complete dictionary list.
  - **Called when**: view opened.
- `perform_search()`
  - **Role**: load search results.
  - **Called when**: user searches.

### `gui/views/results_view.py` (`ResultsView`)

- `update_summary(summary)`
  - **Role**: render final score/stat labels.
  - **Called when**: session ends.

### `gui/views/import_view.py` (`ImportView`)

- `_browse_file()`
  - **Role**: open file picker.
  - **Called when**: user clicks Browse.
- `_load_columns()`
  - **Role**: load CSV headers into mapping controls.
  - **Called when**: file selected.
- `_on_column_selected(_event)`
  - **Role**: update column mapping state.
  - **Called when**: dropdown values change.
- `_run_import()`
  - **Role**: execute full import process.
  - **Called when**: user clicks Import.
- `configure_mode(forced)`
  - **Role**: show forced/non-forced UI state.
  - **Called when**: import view opens.
- `_format_success(result)`
  - **Role**: user-friendly success summary text.
  - **Called when**: import succeeds.
- `_set_status(text, error)`
  - **Role**: status message output.
  - **Called when**: import events occur.
- `_build_header()` / `_build_forced_banner()` / `_build_guide()` / `_build_file_row()` / `_build_column_map_row()` / `_build_mode_row()` / `_build_action_row()` / `_build_status_area()`
  - **Role**: build sections of the import screen UI.
  - **Called when**: Import view is created.
- `_on_mode_changed()` / `_on_overwrite_changed()`
  - **Role**: adapt import options UI.
  - **Called when**: user changes import mode options.

### `gui/views/settings_view.py` (`SettingsView`)

- `save()`
  - **Role**: validate and persist settings.
  - **Called when**: user clicks Save.

### `gui/views/guide_view.py` (`GuideView.__init__`)

- **Role**: render static help text.
- **Called when**: guide view is created.

### `gui/components/flashcard_card.py` (`FlashcardCard`)

- `set_question(text)` / `set_choices(choices)` / `set_feedback(message, color)`
  - **Role**: update card UI content.
  - **Called when**: new question or feedback is shown.
- `reset_after_show()` / `prepare_for_next()` / `disable_all()`
  - **Role**: control interaction lifecycle.
  - **Called when**: card moves between states.
- `set_show_enabled(enabled)`
  - **Role**: enable/disable Show button.
  - **Called when**: penalties/limits change.
- `_handle_show_or_next()` / `_handle_choice_selected()` / `_apply_show_state()`
  - **Role**: internal UI event handling.
  - **Called when**: user interacts with card controls.
- `select_choice(index)` / `trigger_show_or_next()`
  - **Role**: keyboard-driven interaction support.
  - **Called when**: numeric/space key is used.

### `gui/components/option_panels.py` (`FlashcardOptions`)

- `values()`
  - **Role**: return raw selected option values.
  - **Called when**: setup screen reads options.
- `session_config()`
  - **Role**: convert options into normalized session config object.
  - **Called when**: Start Session is pressed.
- `_update_mode_specific_controls(*)`
  - **Role**: show/hide fields by selected mode.
  - **Called when**: mode value changes.
- `_sync_endless_penalty_state()` / `_sync_speed_penalty_state()`
  - **Role**: show proper penalty inputs.
  - **Called when**: penalty type radio changes.
- `_disable_all_penalty_entries()` / `_configure_wrong_penalty_field(visible)`
  - **Role**: enable/disable penalty controls.
  - **Called when**: mode/penalty state updates.
- `_set_entry_state(...)` / `_enable_entry(...)` / `_disable_entry(...)`
  - **Role**: shared entry-state helpers.
  - **Called when**: UI state transitions occur.

### `gui/components/toolbar.py` (`Toolbar.__init__`)

- **Role**: top navigation actions (Home/Back).
- **Called when**: toolbar is constructed.

---

## Utility functions

### `src/tak_flashcard/utils/formatters.py`

- `format_direction(direction)`
  - **Role**: convert direction enum/code into user-facing label.
  - **Called when**: results and labels are rendered.
- `format_mode(mode)`
  - **Role**: convert mode enum/code into user-facing label.
  - **Called when**: results and labels are rendered.
- `format_seconds(total)`
  - **Role**: convert raw seconds to readable time string.
  - **Called when**: results show Speed time used.

### `src/tak_flashcard/utils/validators.py`

- `is_positive_int(value)`
  - **Role**: simple input validation helper.
  - **Called when**: integer-only fields are validated.

### `src/tak_flashcard/utils/io.py`

- `read_json(path)`
  - **Role**: read JSON file safely.
  - **Called when**: loading structured file settings/data.
- `write_json(path, payload)`
  - **Role**: write JSON file safely.
  - **Called when**: storing structured file settings/data.

### `src/tak_flashcard/utils/fonts.py`

- `get_available_fonts()`
  - **Role**: discover system fonts for Settings UI.
  - **Called when**: settings screen needs available font list.
