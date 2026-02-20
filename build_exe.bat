@echo off
REM Build script for creating the Tak Flashcard Windows EXE

setlocal enabledelayedexpansion

echo.
echo ========================================
echo Tak Flashcard - Build EXE for Windows
echo ========================================
echo.

REM Check Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    goto error
)

echo [1/5] Checking Python version...
python --version

echo.
echo [2/5] Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller

if errorlevel 1 (
    echo Error: Failed to install dependencies
    goto error
)

echo.
echo [3/5] Building EXE with PyInstaller...
pyinstaller --onefile tak_flashcard.spec

if errorlevel 1 (
    echo Error: PyInstaller build failed
    goto error
)

echo.
echo [4/5] Creating data directory structure...
mkdir dist\tak_flashcard_data\vocab 2>nul
mkdir dist\tak_flashcard_data\seed 2>nul

echo.
echo [5/5] Build complete!
echo.
echo ========================================
echo Output location: dist\tak_flashcard.exe
echo ========================================
echo.
echo Next steps:
echo   1. Copy your vocabulary CSV files to: dist\tak_flashcard_data\vocab\
echo   2. Run: dist\tak_flashcard.exe
echo.

goto end

:error
echo.
echo Build failed. See errors above.
exit /b 1

:end
