# GitHub Actions Windows EXE Build - Setup Summary

## ✅ Completed Setup

I've configured your Tak Flashcard project to automatically build a Windows EXE with GitHub Actions. Here's what was set up:

### 1. **Path Configuration** (`src/tak_flashcard/config.py`)
- Modified to detect when running from a built EXE using `sys.frozen` check
- When running from EXE: data/db stored in `tak_flashcard_data/` folder (sibling to exe)
- When running from source: uses `src/tak_flashcard/data/` as before

### 2. **PyInstaller Configuration** (`tak_flashcard.spec`)
- Builds a single-file EXE: `tak_flashcard.exe`
- Excludes `data/` and `db/` directories from the bundle (keeps EXE small)
- Includes SQLAlchemy SQLite dialect and Tkinter support
- Runs as windowed app (no console window)

### 3. **GitHub Actions Workflow** (`.github/workflows/build-exe.yml`)
- **Runs on:** Windows (windows-latest) - FREE for public repos
- **Triggers:** 
  - Automatic on push to `main` (when src/, requirements.txt, or spec changes)
  - Manual trigger via GitHub Actions tab
  - Tag-based releases (e.g., `git tag v1.0.0`)
- **Build steps:**
  1. Checkout code
  2. Setup Python 3.11
  3. Install dependencies + PyInstaller
  4. Build EXE
  5. Create `tak_flashcard_data/vocab` and `tak_flashcard_data/seed` directories
  6. Upload artifact (30-day retention)
  7. Create GitHub release (if tag is pushed)

### 4. **Local Build Scripts**
- **`build_exe.bat`** - Windows batch script for local builds
- **`build_exe.sh`** - Shell script for Linux/macOS (produces Windows EXE)

### 5. **Documentation** (`BUILD.md`)
- Complete guide to using GitHub Actions workflow
- Instructions for local builds
- Setup and troubleshooting guide

## 📁 Resulting Directory Structure

When the EXE is built and run:
```
dist/
├── tak_flashcard.exe              # Main application
└── tak_flashcard_data/
    ├── vocab/                     # Put CSV files here
    │   └── vocab_source_*.csv
    ├── seed/                      # Import staging area
    ├── flashcard.db               # Auto-created SQLite DB
    └── user_settings.json         # Auto-created user prefs
```

The `tak_flashcard_data` folder is **NOT bundled in the EXE**, so it survives app updates and can be easily backed up.

## 🚀 Next Steps

### 1. **Test the Workflow**
- Push your changes to GitHub
- Go to Actions tab → Watch "Build Windows EXE" workflow
- Download artifact from completed run

### 2. **Create a Release**
```bash
git tag v1.0.0
git push origin v1.0.0
```
The workflow will automatically create a GitHub release with the EXE.

### 3. **Distribute the EXE**
Users can:
- Download from GitHub releases page
- Extract files to a folder
- Run `tak_flashcard.exe`
- Add CSV vocabulary files to `tak_flashcard_data/vocab/`

## 🔧 Customization

### Change Python version
Edit `.github/workflows/build-exe.yml`, line 27:
```yaml
python-version: '3.12'  # Change to any version
```

### Add more hidden imports
If you add new Python packages, edit `tak_flashcard.spec`:
```python
hiddenimports=[
    'sqlalchemy.dialects.sqlite',
    'tkinter',
    'your_new_package',  # Add here
],
```

### Change output filename
Edit `tak_flashcard.spec`, line 19:
```python
name='your_name',  # Changes exe name
```

## 📊 GitHub Actions Costs

For **public repositories**: 
- ✅ **COMPLETELY FREE** - unlimited minutes and storage

For **private repositories**:
- 2,000 free minutes/month (should be enough for multiple builds)
- Each Windows build takes ~5-10 minutes

## ⚠️ Important Notes

1. **EXE must find data folder:** Users must place `tak_flashcard_data/` in the same directory as the EXE
2. **No console window:** EXE runs silently - add `console=True` in spec if you need debug output
3. **Antivirus:** Some antivirus software may flag PyInstaller exes - this is normal and harmless
4. **First run:** On first run, app will prompt user to import vocabulary from CSV

## 📝 Files Changed/Created

```
Modified:
  ✓ src/tak_flashcard/config.py       (Path detection logic)

Created:
  ✓ tak_flashcard.spec                (PyInstaller configuration)
  ✓ .github/workflows/build-exe.yml    (GitHub Actions workflow)
  ✓ build_exe.bat                     (Local build script - Windows)
  ✓ build_exe.sh                      (Local build script - Unix)
  ✓ BUILD.md                          (Build documentation)
```

## 🎯 Summary

Your project is now fully configured for automated Windows EXE builds on GitHub Actions. The workflow is:

1. **You push code** → GitHub Actions automatically builds the EXE
2. **You create a tag** → GitHub Actions creates a release with the EXE attached
3. **Users download** → They get a standalone EXE that just works

The data folders are separate from the EXE, so updates don't affect user data!
