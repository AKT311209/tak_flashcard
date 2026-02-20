# Building Tak Flashcard EXE

This document explains how to build the Tak Flashcard Windows executable.

## Automated Build with GitHub Actions

A GitHub Actions workflow automatically builds the Windows EXE when code is pushed to the `main` branch.

### Build Triggers

The workflow runs automatically when:
- Code is pushed to `main` branch (only if `src/`, `requirements.txt`, or `tak_flashcard.spec` changed)
- A pull request is created against `main`
- Manually triggered via the Actions tab

### Build Output

The workflow:
1. Sets up a Windows environment with Python 3.11
2. Installs dependencies from `requirements.txt`
3. Builds the EXE using PyInstaller with `tak_flashcard.spec`
4. Creates the `tak_flashcard_data` directory structure
5. Uploads artifacts for 30 days

**Artifacts are available** in the Actions tab after a successful build.

### Creating a Release

To create a GitHub release with the EXE attached:

1. Create a git tag: `git tag v1.0.0`
2. Push the tag: `git push origin v1.0.0`
3. The workflow will automatically create a release with the EXE file

## Manual Local Build

### Windows (Recommended for local testing)

**Using the batch script:**
```bash
build_exe.bat
```

**Or manually:**
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller
pyinstaller tak_flashcard.spec
mkdir dist\tak_flashcard_data\vocab
mkdir dist\tak_flashcard_data\seed
```

### Linux / macOS (with cross-compilation)

**Using the shell script:**
```bash
chmod +x build_exe.sh
./build_exe.sh
```

Note: The resulting EXE will be Windows-only and won't run directly on Linux/macOS.

## Using the Built EXE

### Directory Structure

After building, the output looks like:
```
dist/
├── tak_flashcard.exe          # Main application executable
└── tak_flashcard_data/        # Data directory (same location as exe)
    ├── vocab/                 # CSV vocabulary files go here
    │   └── vocab_source_*.csv
    ├── seed/                  # Import seed directory
    ├── flashcard.db           # SQLite database (auto-created)
    └── user_settings.json     # User preferences
```

### First Run Setup

1. **Prepare vocabulary files:**
   - Copy your CSV vocabulary files to `tak_flashcard_data/vocab/`
   - CSV format must have columns: `english`, `vietnamese`, `part_of_speech`

2. **Run the application:**
   ```bash
   tak_flashcard.exe
   ```

3. **Import vocabulary:**
   - On first run, you'll be prompted to import vocabulary
   - Select your CSV file and choose "Append" or "Replace"
   - The app will validate and load the data

### Data and Database

- **Vocabulary data:** Stored in `tak_flashcard_data/vocab/`
- **SQLite database:** Auto-created at `tak_flashcard_data/flashcard.db`
- **Settings:** Stored in `tak_flashcard_data/user_settings.json`

These directories are **separate from the EXE** and persist across app updates.

## PyInstaller Configuration

The build process uses `tak_flashcard.spec` which:
- Bundles the application into a single `tak_flashcard.exe`
- Excludes the `data/` and `db/` directories from the bundle
- Includes SQLAlchemy SQLite support
- Uses tkinter (built-in with Python)

The EXE runs with `sys.frozen = True`, which the application uses to redirect data paths to `tak_flashcard_data/`.

## Troubleshooting

### "PyInstaller not found"
```bash
pip install pyinstaller
```

### Build fails with module errors
Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### EXE doesn't find vocabulary files
Verify the structure:
```
C:\Users\YourName\Desktop\tak_flashcard.exe
C:\Users\YourName\Desktop\tak_flashcard_data\vocab\vocab_source.csv
```

The `tak_flashcard_data` folder must be in the same directory as the EXE.

## Design Rationale

### Why separate data from EXE?
- **Updates:** Updates don't affect user data
- **Portability:** Can move the exe without losing data
- **Smaller exe:** Excludes large CSV files
- **Flexibility:** Users can manage/backup data independently

### Path Detection
The application detects whether it's running from:
- **Source code:** Uses `src/tak_flashcard/data/` 
- **Built EXE:** Uses sibling folder `tak_flashcard_data/`

This is automatic via `sys.frozen` check in `config.py`.
