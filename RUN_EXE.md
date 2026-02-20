# Running Tak Flashcard EXE

Quick start guide for using the built Windows executable.

## Before First Run

1. **Let the EXE prepare its data folder**
     - The first time you run `tak_flashcard.exe`, it automatically creates
         `tak_flashcard_data` (along with `vocab/` and `seed/`) in the same folder
         as the executable.
     - You do not need to create anything manually—just launch the EXE and it
         will set up the data directories before showing the GUI.


## Running the Application

**Double-click** `tak_flashcard.exe`

On first run with no vocabulary data:
- App will prompt you to import vocabulary
- Click "Import Vocabulary" and select your CSV file
- Choose "Append" to add words or "Replace" to replace existing data

## Folder Structure

After first run, you'll see:
```
├── tak_flashcard.exe              # The app - run this
└── tak_flashcard_data/
    ├── vocab/                     # Your CSV files go here
    │   └── vocab_source_*.csv
    ├── flashcard.db               # Database (auto-created)
    └── user_settings.json         # Settings (auto-created)
```

## Features

Once vocabulary is imported, you can:
- **Flashcard Mode** - Study with timed or untimed sessions
- **Dictionary** - Browse and search all vocabulary
- **Settings** - Customize appearance and preferences
- **Import** - Add more vocabulary from additional CSV files

## Troubleshooting

**"Cannot find tak_flashcard_data folder"**
- Run `tak_flashcard.exe` once so it can create the folder automatically
- If that still fails, you can manually create `tak_flashcard_data` next to the EXE

**"No vocabulary found"**
- You need to import vocabulary (select CSV file in Import view)
- Or add CSV files to `tak_flashcard_data/vocab/`

**App closes immediately**
- Check that `tak_flashcard_data` folder exists
- Make sure you have write permissions in that folder

**CSV import fails**
- Check CSV column names: `english`, `vietnamese`, `part_of_speech`
- Make sure there are no spaces in column names
- Try opening the CSV in Excel to verify format

## Support

For issues or questions:
- Check the CSV format matches requirements
- Ensure `tak_flashcard_data` folder is in the same directory as exe
- Try removing `flashcard.db` to reset the database (you'll need to re-import vocabulary)

## Updates

When you upgrade to a new version:
1. Keep your `tak_flashcard_data` folder
2. Replace only `tak_flashcard.exe`
3. All your vocabulary and settings will be preserved!
