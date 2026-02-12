"""Font discovery and binding utilities for DearPyGui.

Provides functions to discover system fonts and bind a unicode-capable
font based on the application's appearance settings.
"""

from pathlib import Path
import shutil
import subprocess
import dearpygui.dearpygui as dpg
from typing import Dict, List, Optional


def discover_system_fonts() -> Dict[str, str]:
    """Discover fonts on the system and return a mapping display->path.

    Returns:
        dict where keys are human-readable display names and values are
        absolute file paths to font files.
    """
    fonts: Dict[str, str] = {}

    # try common locations first
    common = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
    ]
    for p in common:
        if Path(p).exists():
            fonts[f"{Path(p).stem} ({Path(p).name})"] = str(Path(p).absolute())

    # use fontconfig if available to enumerate installed fonts (Linux)
    try:
        if shutil.which("fc-list"):
            proc = subprocess.run(
                ["fc-list", ":file:family"], capture_output=True, text=True)
            out = proc.stdout
            for line in out.splitlines():
                if not line.strip():
                    continue
                # format: /path/to/font.ttf: Family Name, Other
                parts = line.split(":", 1)
                if len(parts) != 2:
                    continue
                path = parts[0].strip()
                fam = parts[1].strip().split(",")[0]
                if Path(path).exists():
                    display = f"{fam} ({Path(path).name})"
                    if display not in fonts:
                        fonts[display] = path
    except Exception:
        pass

    # deduplicate and return
    return fonts


def apply_font_from_appearance(appearance: dict) -> Optional[dict]:
    """Load and bind a font based on appearance settings.

    Appearance may include keys:
      - font_path: path to TTF font file
      - font_pixel_size: desired pixel size (int)

    If font_path is not provided or invalid, the function will attempt to
    locate a common unicode-capable font using system discovery.

    Returns:
        Path to bound font file on success, or None on failure.
    """
    size = appearance.get("font_pixel_size", 16)
    font_path = appearance.get("font_path")

    candidates: List[str] = []
    if font_path:
        candidates.append(str(Path(font_path).expanduser()))

    # add discovered fonts
    fonts = discover_system_fonts()
    candidates.extend(list(fonts.values()))

    found = None
    for p in candidates:
        try:
            if Path(p).exists():
                found = str(Path(p).absolute())
                break
        except Exception:
            continue

    if not found:
        print("[tak_flashcard] No suitable font found; using DearPyGui default")
        return None

    try:
        with dpg.font_registry():
            font = dpg.add_font(found, int(size))
            if font:
                # ensure Vietnamese glyphs are loaded so diacritics render
                try:
                    dpg.add_font_range_hint(
                        dpg.mvFontRangeHint_Vietnamese,
                        parent=font
                    )
                except Exception:
                    pass
                try:
                    dpg.add_font_range_hint(
                        dpg.mvFontRangeHint_Default,
                        parent=font
                    )
                except Exception:
                    pass
                try:
                    dpg.add_font_range(0x0000, 0x10FFFF, parent=font)
                except Exception:
                    for start, end in [
                        (0x0000, 0x00FF),    # Basic Latin
                        (0x0100, 0x024F),    # Latin Extended-A/B
                        (0x0250, 0x02AF),    # IPA Extensions
                        (0x0300, 0x036F),    # Combining Diacritical Marks
                        (0x1E00, 0x1EFF),    # Latin Extended Additional
                        (0x1F00, 0x1FFF),    # Greek Extended
                        (0x1F300, 0x1F5FF),  # Misc Symbols and Pictographs
                        (0x1F600, 0x1F64F),  # Emoticons
                        (0x1F680, 0x1F6FF),  # Transport & Map Symbols
                        (0x2600, 0x26FF),    # Misc symbols
                        (0x2700, 0x27BF),    # Dingbats
                    ]:
                        try:
                            dpg.add_font_range(start, end, parent=font)
                        except Exception:
                            continue
                # return font metadata; do not bind here because binding
                # should happen after DearPyGui setup to affect rendering.
                print(
                    f"[tak_flashcard] Registered font: {found} @ size {size}")
                return {"font_id": font, "path": found, "size": int(size)}
    except Exception as e:
        print("[tak_flashcard] Failed to register font:", e)
    return None


def bind_font_from_metadata(meta: Optional[dict]) -> bool:
    """Bind a previously registered font using its metadata.

    This should be called after dpg.setup_dearpygui() to ensure binding takes effect.
    """
    if not meta:
        return False
    try:
        font_id = meta.get("font_id")
        # font_id may be valid; bind it
        if font_id:
            dpg.bind_font(font_id)
            print(
                f"[tak_flashcard] Bound font: {meta.get('path')} @ size {meta.get('size')}")
            # also attempt to bind this font to existing text items so the
            # change is visible immediately for already-created widgets.
            try:
                bind_font_to_all_text_items(font_id)
            except Exception:
                pass
            return True
    except Exception as e:
        print("[tak_flashcard] Failed to bind font from metadata:", e)
    return False


def bind_font_to_all_text_items(font_id: int):
    """Bind the given font to all text-like items currently in the DearPyGui context.

    This forces existing labels, table cells, and other text widgets to use the new
    font immediately.
    """
    try:
        all_items = dpg.get_all_items()
        for item in all_items:
            try:
                itype = dpg.get_item_type(item)
                # bind to common text item types
                if itype in ("mvText", "text", "mvTableCell"):
                    dpg.bind_item_font(item, font_id)
            except Exception:
                continue
    except Exception as e:
        print("[tak_flashcard] Failed to bind font to all items:", e)
