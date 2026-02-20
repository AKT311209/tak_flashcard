#!/bin/bash

# Build script for creating the Tak Flashcard Windows EXE
# This script can be run on Windows (Git Bash), Linux, or macOS with Wine

set -e

echo ""
echo "========================================"
echo "Tak Flashcard - Build EXE for Windows"
echo "========================================"
echo ""

# Check Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python3 is not installed or not in PATH"
    exit 1
fi

echo "[1/5] Checking Python version..."
python3 --version

echo ""
echo "[2/5] Installing dependencies..."
python3 -m pip install --upgrade pip
pip3 install -r requirements.txt
pip3 install pyinstaller

echo ""
echo "[3/5] Building EXE with PyInstaller..."
pyinstaller tak_flashcard.spec

if [ $? -ne 0 ]; then
    echo "Error: PyInstaller build failed"
    exit 1
fi

echo ""
echo "[4/5] Creating data directory structure..."
mkdir -p dist/tak_flashcard_data/vocab
mkdir -p dist/tak_flashcard_data/seed

echo ""
echo "[5/5] Build complete!"
echo ""
echo "========================================"
echo "Output location: dist/tak_flashcard.exe"
echo "========================================"
echo ""
echo "Next steps:"
echo "  1. Copy your vocabulary CSV files to: dist/tak_flashcard_data/vocab/"
echo "  2. Run on Windows: dist/tak_flashcard.exe"
echo ""
