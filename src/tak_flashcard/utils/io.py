"""I/O utility functions."""

import json
from pathlib import Path
from typing import Any, Dict, Optional


def read_json(file_path: Path) -> Optional[Dict]:
    """
    Read JSON data from file.

    Args:
        file_path: Path to JSON file

    Returns:
        Dictionary with JSON data or None if error
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return None


def write_json(file_path: Path, data: Dict) -> bool:
    """
    Write JSON data to file.

    Args:
        file_path: Path to JSON file
        data: Dictionary to write

    Returns:
        True if successful, False otherwise
    """
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception:
        return False


def ensure_dir(dir_path: Path) -> bool:
    """
    Ensure directory exists, create if it doesn't.

    Args:
        dir_path: Path to directory

    Returns:
        True if successful, False otherwise
    """
    try:
        dir_path.mkdir(parents=True, exist_ok=True)
        return True
    except Exception:
        return False
