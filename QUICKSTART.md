# Quick Start Guide

## Running the Application

### From Project Root

```bash
cd /mnt/Data/Bi/Coding/Projects/tak_flashcard
python -m src.tak_flashcard.main
```

### From src Directory

```bash
cd /mnt/Data/Bi/Coding/Projects/tak_flashcard/src
python -m tak_flashcard.main
```

## First-Time Setup

When you run the application for the first time:

1. **Database Initialization**: The application will create a SQLite database at `src/tak_flashcard/data/flashcard.db`

2. **Vocabulary Import**: The application will automatically import 1037 words from `src/tak_flashcard/data/vocab/vocab_source.csv`

3. **Settings File**: A default settings file will be created at `src/tak_flashcard/data/user_settings.json`

## Testing the Features

### 1. Test Flashcard Feature
- Click "Flashcard" on home screen
- Select "Endless" mode
- Choose "English → Vietnamese"
- Set difficulty to 3
- Click "Start Session"
- Answer a few questions to test functionality

### 2. Test Dictionary Feature
- Click "Dictionary" on home screen
- Search for "hello"
- Filter by "verb"
- Sort by "Difficulty"

-### 3. Test Settings Feature
- Click "Settings" on home screen
- Adjust font or font size (pixels)
- Click "Save & Apply"

### 4. Test Guide Feature
- Click "Guide" on home screen
- Scroll through the user manual

## Expected Console Output

```
Initializing database...
Checking vocabulary data...
Successfully imported 1037 words
Starting application...
```

## Common Issues and Solutions

### Issue: ModuleNotFoundError
**Solution**: Make sure you're running from the correct directory and PYTHONPATH is set

```bash
# Option 1: Run from project root
cd /mnt/Data/Bi/Coding/Projects/tak_flashcard
PYTHONPATH=src python -m tak_flashcard.main

# Option 2: Run from src directory
cd /mnt/Data/Bi/Coding/Projects/tak_flashcard/src
python -m tak_flashcard.main
```

### Issue: Package import errors
**Solution**: Install all dependencies

```bash
pip install -r requirements.txt
```

### Issue: CSV file not found
**Solution**: Ensure the vocabulary CSV exists at the correct location

```bash
ls -la src/tak_flashcard/data/vocab/vocab_source.csv
```

### Issue: Database errors
**Solution**: Delete and recreate the database

```bash
rm src/tak_flashcard/data/flashcard.db
# Then restart the application
```

## Features Checklist

- ✅ **Database Layer**: SQLAlchemy models, session management, repositories
- ✅ **Data Import**: CSV importer with 1037+ words
- ✅ **Core Logic**: Difficulty calculation, card selection, scoring, timer
- ✅ **Settings**: JSON-based settings persistence
- ✅ **Flashcard Modes**: Endless, Speed, Testing
- ✅ **Directions**: Eng→Vn, Vn→Eng, Mixed
- ✅ **Difficulty Levels**: 1-5 with weighted selection
- ✅ **Penalty System**: Score deduction, time deduction, HP limit
- ✅ **Dictionary**: Search, filter, sort functionality
- ✅ **Guide**: Comprehensive user manual
- ✅ **Settings**: Appearance (font/colors), defaults, preferences
- ✅ **GUI**: Tkinter interface with all views

## File Structure Verification

```bash
# Check core files exist
ls -la src/tak_flashcard/main.py
ls -la src/tak_flashcard/config.py
ls -la src/tak_flashcard/constants.py

# Check database layer
ls -la src/tak_flashcard/db/models.py
ls -la src/tak_flashcard/db/session.py
ls -la src/tak_flashcard/db/repo.py

# Check features
ls -la src/tak_flashcard/features/flashcard/controller.py
ls -la src/tak_flashcard/features/dictionary/service.py
ls -la src/tak_flashcard/features/guide/content.py
ls -la src/tak_flashcard/features/settings/controller.py

# Check GUI
ls -la src/tak_flashcard/gui/app.py
ls -la src/tak_flashcard/gui/views/home_view.py
ls -la src/tak_flashcard/gui/views/flashcard_view.py

# Check data
ls -la src/tak_flashcard/data/vocab/vocab_source.csv
```

## Development Notes

### Type Checking Warnings
The Pylance type checker may show some warnings related to:
- SQLAlchemy Column types
- Optional type handling

These are false positives and won't affect runtime execution. The application has been designed to handle these cases properly.

### Database Schema
The database schema is automatically created on first run. You can inspect it using SQLite:

```bash
sqlite3 src/tak_flashcard/data/flashcard.db
.schema
SELECT COUNT(*) FROM words;
.quit
```

### Adding More Words
To add more vocabulary words:
1. Edit `src/tak_flashcard/data/vocab/vocab_source.csv`
2. Add entries in format: `english,vietnamese,part_of_speech`
3. Delete the database file
4. Restart the application to reimport

## Next Steps

After confirming the application works:

1. **Test all modes**: Try Endless, Speed, and Testing modes
2. **Test all directions**: Eng→Vn, Vn→Eng, Mixed
3. **Test difficulty levels**: Try levels 1-5 and observe word selection
4. **Test Show Answer**: See penalty system in action
5. **Complete a full session**: Get statistics and results
6. **Browse dictionary**: Search and filter words
7. **Customize settings**: Adjust font, colors, defaults
8. **Read the guide**: Review all features and tips

## Success Criteria

✅ Application starts without errors  
✅ Database auto-created with 1000+ words  
✅ All 3 flashcard modes work  
✅ All 3 directions functional  
✅ Difficulty system adapts to performance  
✅ Dictionary search/filter/sort works  
✅ Settings save and load correctly  
✅ Guide displays complete documentation  
✅ Session results shown correctly  
✅ Application stable on Windows/Linux

## Contact

For issues or questions, refer to the main README.md or the in-app Guide.
