"""Styling utilities for theming the application."""

from __future__ import annotations

from tkinter import ttk

from tak_flashcard.core.settings import AppearanceSettings


def _hex_to_rgb(value: str) -> tuple[int, int, int]:
    """Parse a ``#RRGGBB`` color into an RGB tuple.

    Parameters:
        value: Hex color string.

    Returns:
        A 3-tuple of ``(red, green, blue)`` values.
    """

    hex_value = value.strip().lstrip("#")
    if len(hex_value) != 6:
        return (255, 255, 255)
    return (
        int(hex_value[0:2], 16),
        int(hex_value[2:4], 16),
        int(hex_value[4:6], 16),
    )


def _rgb_to_hex(rgb: tuple[int, int, int]) -> str:
    """Convert an RGB tuple into ``#RRGGBB`` format."""

    r, g, b = rgb
    return f"#{max(0, min(255, r)):02x}{max(0, min(255, g)):02x}{max(0, min(255, b)):02x}"


def _mix(a: tuple[int, int, int], b: tuple[int, int, int], ratio: float) -> tuple[int, int, int]:
    """Blend two RGB colors by ratio.

    Parameters:
        a: Base RGB tuple.
        b: Target RGB tuple.
        ratio: Blend amount in range ``0.0`` to ``1.0``.

    Returns:
        Mixed RGB tuple.
    """

    mix_ratio = max(0.0, min(1.0, ratio))
    return (
        int(a[0] + (b[0] - a[0]) * mix_ratio),
        int(a[1] + (b[1] - a[1]) * mix_ratio),
        int(a[2] + (b[2] - a[2]) * mix_ratio),
    )


def _luminance(rgb: tuple[int, int, int]) -> float:
    """Calculate perceived luminance for simple contrast decisions."""

    r, g, b = rgb
    return (0.299 * r + 0.587 * g + 0.114 * b) / 255


def _build_palette(settings: AppearanceSettings) -> dict[str, str]:
    """Build a glassmorphism-oriented color palette with shadow system aligned to CSS design tokens.

    Implements Tailwind CSS shadow system equivalent:
    - shadow-sm:  0 1px 2px rgba(0,0,0,0.05) → 5% opacity
    - shadow-md:  0 4px 6px rgba(0,0,0,0.1) → 10% opacity (cards, buttons)
    - shadow-lg:  0 10px 15px rgba(0,0,0,0.1) → 10% opacity (modals)
    - shadow-xl:  0 20px 25px rgba(0,0,0,0.15) → 15% opacity (hero elements)

    Parameters:
        settings: Current appearance settings.

    Returns:
        A dictionary of named design tokens used by ttk styles.
    """

    base_rgb = _hex_to_rgb(settings.background_color)
    accent_rgb = _hex_to_rgb(settings.secondary_color)
    text_rgb = _hex_to_rgb(settings.text_color)

    dark_mode = _luminance(base_rgb) < 0.45
    white = (255, 255, 255)
    black = (15, 23, 42)

    if dark_mode:
        bg = _rgb_to_hex(_mix(base_rgb, black, 0.35))
        surface = _rgb_to_hex(_mix(base_rgb, white, 0.08))
        surface_alt = _rgb_to_hex(_mix(base_rgb, white, 0.14))
        border = _rgb_to_hex(_mix(base_rgb, white, 0.28))
        text = _rgb_to_hex(_mix(text_rgb, white, 0.18))
        muted = _rgb_to_hex(_mix(text_rgb, white, 0.45))
        input_bg = _rgb_to_hex(_mix(base_rgb, white, 0.12))

        neumorphic_shadow = _rgb_to_hex(_mix(black, base_rgb, 0.6))
        neumorphic_highlight = _rgb_to_hex(_mix(white, base_rgb, 0.25))
        button_shadow = _rgb_to_hex(_mix(black, base_rgb, 0.7))
        button_highlight = _rgb_to_hex(_mix(white, base_rgb, 0.2))

        shadow_sm = _rgb_to_hex(_mix(black, base_rgb, 0.05))
        shadow_md = _rgb_to_hex(_mix(black, base_rgb, 0.1))
        shadow_lg = _rgb_to_hex(_mix(black, base_rgb, 0.15))
        shadow_xl = _rgb_to_hex(_mix(black, base_rgb, 0.2))
    else:
        bg = _rgb_to_hex(_mix(base_rgb, (242, 245, 250), 0.3))
        surface = _rgb_to_hex(_mix(base_rgb, (255, 255, 255), 0.5))
        surface_alt = _rgb_to_hex(_mix(base_rgb, (255, 255, 255), 0.7))
        border = _rgb_to_hex(_mix(base_rgb, (180, 195, 215), 0.45))
        text = _rgb_to_hex(_mix(text_rgb, (20, 20, 35), 0.15))
        muted = _rgb_to_hex(_mix(text_rgb, (80, 90, 110), 0.4))
        input_bg = _rgb_to_hex(_mix(base_rgb, (255, 255, 255), 0.85))

        neumorphic_shadow = _rgb_to_hex(_mix((60, 80, 110), base_rgb, 0.5))
        neumorphic_highlight = _rgb_to_hex(_mix(white, base_rgb, 0.7))
        button_shadow = _rgb_to_hex(_mix((50, 75, 110), base_rgb, 0.55))
        button_highlight = _rgb_to_hex(_mix(white, base_rgb, 0.75))

        shadow_sm = _rgb_to_hex(_mix((100, 120, 150), base_rgb, 0.16))
        shadow_md = _rgb_to_hex(_mix((80, 110, 140), base_rgb, 0.28))
        shadow_lg = _rgb_to_hex(_mix((60, 90, 130), base_rgb, 0.32))
        shadow_xl = _rgb_to_hex(_mix((40, 70, 120), base_rgb, 0.35))

    accent = _rgb_to_hex(_mix(accent_rgb, (8, 145, 178), 0.3))
    accent_hover = _rgb_to_hex(_mix(_hex_to_rgb(accent), (5, 150, 105), 0.12))
    warning = _rgb_to_hex(_mix((220, 38, 38), base_rgb,
                          0.35 if dark_mode else 0.45))
    warning_hover = _rgb_to_hex(
        _mix(_hex_to_rgb(warning), (185, 28, 28), 0.12))
    focus = _rgb_to_hex(
        _mix(_hex_to_rgb(accent), white if dark_mode else black, 0.2))

    return {
        "bg": bg,
        "surface": surface,
        "surface_alt": surface_alt,
        "border": border,
        "text": text,
        "muted": muted,
        "accent": accent,
        "accent_hover": accent_hover,
        "warning": warning,
        "warning_hover": warning_hover,
        "focus": focus,
        "input_bg": input_bg,
        "tree_bg": surface_alt,
        "neumorphic_shadow": neumorphic_shadow,
        "neumorphic_highlight": neumorphic_highlight,
        "button_shadow": button_shadow,
        "button_highlight": button_highlight,
        "shadow_sm": shadow_sm,
        "shadow_md": shadow_md,
        "shadow_lg": shadow_lg,
        "shadow_xl": shadow_xl,
    }


def apply_appearance_settings(style: ttk.Style, settings: AppearanceSettings) -> dict[str, str]:
    """Apply a glassmorphism-inspired style system to ttk widgets.

    Parameters:
        style: Active ttk style object.
        settings: Appearance settings selected by the user.

    Returns:
        The resolved palette tokens so root windows can apply matching colors.
    """

    palette = _build_palette(settings)

    font_name = settings.font_name if settings.font_name != "Arial" else "Segoe UI"
    font = (font_name, settings.font_size_px)
    heading_font = (font_name, settings.font_size_px + 8, "bold")
    subheading_font = (font_name, settings.font_size_px + 3, "bold")

    style.configure(".", font=font)

    style.configure("TFrame", background=palette["bg"])
    style.configure("App.TFrame", background=palette["bg"])
    style.configure("Page.TFrame", background=palette["bg"])
    style.configure(
        "Glass.TFrame",
        background=palette["surface"],
        bordercolor=palette["border"],
        relief="solid",
        borderwidth=1,
    )
    style.configure("Card.TFrame", background=palette["surface_alt"])
    style.configure("Surface.TFrame", background=palette["surface"])

    style.configure(
        "TLabel", background=palette["bg"], foreground=palette["text"], font=font)
    style.configure(
        "Title.TLabel", background=palette["bg"], foreground=palette["text"], font=heading_font)
    style.configure("Subtitle.TLabel",
                    background=palette["bg"], foreground=palette["muted"], font=font)
    style.configure(
        "Section.TLabel", background=palette["surface"], foreground=palette["text"], font=subheading_font)
    style.configure(
        "Muted.TLabel", background=palette["surface"], foreground=palette["muted"], font=font)
    style.configure(
        "Status.TLabel", background=palette["surface"], foreground=palette["text"], font=font)

    style.configure(
        "TLabelframe",
        background=palette["surface"],
        bordercolor=palette["border"],
        relief="solid",
        borderwidth=1,
    )
    style.configure(
        "TLabelframe.Label",
        background=palette["surface"],
        foreground=palette["text"],
        font=subheading_font,
    )
    style.configure(
        "Glass.TLabelframe",
        background=palette["surface_alt"],
        bordercolor=palette["border"],
        relief="solid",
        borderwidth=1,
    )
    style.configure(
        "Glass.TLabelframe.Label",
        background=palette["surface_alt"],
        foreground=palette["text"],
        font=subheading_font,
    )

    style.configure(
        "TButton",
        background=palette["surface_alt"],
        foreground=palette["text"],
        bordercolor=palette["border"],
        focusthickness=0,
        focuscolor=palette["focus"],
        padding=(16, 12),
        relief="solid",
        borderwidth=1,
    )
    style.map(
        "TButton",
        background=[("active", palette["surface"]),
                    ("pressed", palette["surface"])],
        foreground=[("active", palette["text"]),
                    ("disabled", palette["muted"])],
        bordercolor=[("focus", palette["focus"]),
                     ("active", palette["border"])],
    )
    style.configure(
        "Glass.TButton",
        background=palette["surface_alt"],
        foreground=palette["text"],
        bordercolor=palette["border"],
        focusthickness=0,
        focuscolor=palette["focus"],
        padding=(16, 12),
        relief="solid",
        borderwidth=2,
    )
    style.map(
        "Glass.TButton",
        background=[("active", palette["surface"]),
                    ("pressed", palette["surface"])],
        foreground=[("active", palette["text"]),
                    ("disabled", palette["muted"])],
        bordercolor=[("focus", palette["focus"]),
                     ("active", palette["border"])],
    )
    style.configure(
        "Primary.TButton",
        background=palette["accent"],
        foreground="#ffffff",
        bordercolor=palette["accent"],
        padding=(18, 13),
        relief="flat",
        borderwidth=1,
    )
    style.map(
        "Primary.TButton",
        background=[("active", palette["accent_hover"]),
                    ("pressed", palette["accent_hover"]),
                    ("disabled", palette["muted"])],
        foreground=[("disabled", palette["focus"])],
    )
    style.configure(
        "Warning.TButton",
        background=palette["warning"],
        foreground="#ffffff",
        bordercolor=palette["warning"],
        padding=(18, 13),
        relief="flat",
        borderwidth=1,
    )
    style.map(
        "Warning.TButton",
        background=[("active", palette["warning_hover"]),
                    ("pressed", palette["warning_hover"]),
                    ("disabled", palette["muted"])],
        foreground=[("disabled", palette["focus"])],
    )

    style.configure(
        "TRadiobutton",
        background=palette["surface"],
        foreground=palette["text"],
        indicatorcolor=palette["accent"],
        indicatormargin=4,
    )
    style.map("TRadiobutton", foreground=[("disabled", palette["muted"])])
    style.configure(
        "TCheckbutton",
        background=palette["surface"],
        foreground=palette["text"],
        indicatorcolor=palette["accent"],
    )

    style.configure(
        "TEntry",
        fieldbackground=palette["input_bg"],
        background=palette["input_bg"],
        foreground=palette["text"],
        bordercolor=palette["border"],
        insertcolor=palette["text"],
        lightcolor=palette["focus"],
        darkcolor=palette["border"],
        padding=(10, 8),
    )
    style.configure(
        "TCombobox",
        fieldbackground=palette["input_bg"],
        background=palette["input_bg"],
        foreground=palette["text"],
        bordercolor=palette["border"],
        arrowcolor=palette["text"],
        lightcolor=palette["focus"],
        darkcolor=palette["border"],
        padding=(8, 6),
    )
    style.map("TCombobox", fieldbackground=[("readonly", palette["input_bg"])])
    style.configure(
        "TSpinbox", fieldbackground=palette["input_bg"], foreground=palette["text"])

    style.configure(
        "Horizontal.TScale",
        background=palette["surface"],
        troughcolor=palette["surface_alt"],
    )

    style.configure(
        "Treeview",
        background=palette["tree_bg"],
        fieldbackground=palette["tree_bg"],
        foreground=palette["text"],
        bordercolor=palette["border"],
        rowheight=max(24, settings.font_size_px + 16),
    )
    style.map(
        "Treeview",
        background=[("selected", palette["accent"])],
        foreground=[("selected", "#ffffff")],
    )
    style.configure(
        "Treeview.Heading",
        background=palette["surface"],
        foreground=palette["text"],
        bordercolor=palette["border"],
        relief="flat",
        font=(settings.font_name, settings.font_size_px, "bold"),
    )
    style.map("Treeview.Heading", background=[
              ("active", palette["surface_alt"])])

    style.configure(
        "Neumorphic.TFrame",
        background=palette["surface"],
        relief="flat",
    )
    style.configure(
        "Timer.TLabel",
        background=palette["surface"],
        foreground=palette["text"],
        font=(settings.font_name, settings.font_size_px + 8, "bold"),
    )
    style.configure(
        "Neumorphic.TLabel",
        background=palette["surface"],
        foreground=palette["text"],
        font=font,
    )

    return palette
