"""Neumorphic UI components with soft shadows, transparency, and glassmorphism styling."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Any, Callable


class ShadowedFrame(tk.Frame):
    """Frame with multi-layer shadow effects for elevation and depth.

    Simulates CSS shadow system:
    - shadow-sm: 0 1px 2px rgba(0,0,0,0.05) → Subtle lift
    - shadow-md: 0 4px 6px rgba(0,0,0,0.1) → Cards, buttons
    - shadow-lg: 0 10px 15px rgba(0,0,0,0.1) → Modals, dropdowns
    - shadow-xl: 0 20px 25px rgba(0,0,0,0.15) → Hero elements
    """

    def __init__(
        self,
        master: tk.Misc,
        bg_color: str = "#f8f9fa",
        shadow_color: str = "#d0d0d0",
        elevation: str = "md",
        **kwargs: Any,
    ):
        """Initialize shadowed frame with elevation level.

        Parameters:
            master: Parent widget.
            bg_color: Frame background color.
            shadow_color: Shadow color for depth effect.
            elevation: Shadow elevation level ('sm', 'md', 'lg', 'xl').
        """

        super().__init__(master, bg=bg_color, **kwargs)  # type: ignore
        self.bg_color = bg_color
        self.shadow_color = shadow_color
        self.elevation = elevation
        self._shadow_canvas: tk.Canvas | None = None
        self._content_frame: tk.Frame | None = None

    def add_content(self, creator: Callable[[tk.Frame], None]) -> tk.Frame:
        """Add shadowed content to the frame.

        Parameters:
            creator: Callable that populates a frame with widgets.

        Returns:
            The frame containing the content (for further customization).
        """

        if not self._shadow_canvas:
            self._create_shadow()

        if not self._content_frame:
            self._content_frame = tk.Frame(self, bg=self.bg_color)
            self._content_frame.pack(fill="both", expand=True, padx=2, pady=2)

        creator(self._content_frame)
        return self._content_frame

    def _create_shadow(self) -> None:
        """Create multi-layer shadow based on elevation."""

        shadow_offsets = {
            "sm": [(1, 1, 1)],
            "md": [(2, 2, 2), (4, 4, 3)],
            "lg": [(4, 4, 3), (8, 8, 5)],
            "xl": [(6, 6, 4), (12, 12, 8)],
        }

        offsets = shadow_offsets.get(self.elevation, shadow_offsets["md"])

        for offset_x, offset_y, blur in offsets:
            shadow_frame = tk.Frame(self, bg=self.shadow_color)
            shadow_frame.place(
                x=offset_x,
                y=offset_y,
                relwidth=1.0,
                relheight=1.0,
            )
            shadow_frame.lower()


class NeumorphicTimer(tk.Canvas):
    """Neumorphic timer display with professional depth and glassmorphism styling."""

    def __init__(
        self,
        master: tk.Misc,
        width: int = 280,
        height: int = 140,
        bg_color: str = "#f0f0f0",
        shadow_color: str = "#d0d0d0",
        highlight_color: str = "#ffffff",
        text_color: str = "#333333",
        **kwargs: object,
    ):
        """Initialize neumorphic timer with dimensions and colors.

        Parameters:
            master: Parent widget.
            width: Canvas width.
            height: Canvas height.
            bg_color: Background color matching theme.
            shadow_color: Shadow color for neumorphic effect.
            highlight_color: Highlight color for neumorphic effect.
            text_color: Text color for time display.
        """

        super().__init__(
            master,
            width=width,
            height=height,
            bg=bg_color,
            highlightthickness=0,
            relief="flat",
            **kwargs,
        )
        self.bg_color = bg_color
        self.shadow_color = shadow_color
        self.highlight_color = highlight_color
        self.text_color = text_color

        self._draw_glassmorphic_border()

        self._time_text = self.create_text(
            width // 2,
            int(height * 0.63),
            text=self._format_time_label(0),
            font=("Segoe UI", 50, "bold"),
            fill=text_color,
            tags="time",
        )
        self._label_text = self.create_text(
            width // 2,
            int(height * 0.22),
            text="Time Remaining",
            font=("Segoe UI", 13, "bold"),
            fill=text_color,
            tags="label",
        )

    def _draw_glassmorphic_border(self) -> None:
        """Draw multi-layer shadows with glassmorphism aesthetic for depth."""

        canvas_width = int(self.cget("width"))
        canvas_height = int(self.cget("height"))

        shadow_soft = self._mix_colors(self.shadow_color, "#000000", 0.22)
        shadow_faint = self._mix_colors(self.shadow_color, "#000000", 0.08)
        highlight_edge = self._mix_colors(
            self.highlight_color, "#ffffff", 0.62)
        glass_fill = self._mix_colors(self.bg_color, "#ffffff", 0.30)
        glass_gloss = self._mix_colors(glass_fill, "#ffffff", 0.55)
        inner_line = self._mix_colors(glass_fill, self.highlight_color, 0.28)

        self.create_rectangle(
            8,
            10,
            canvas_width - 8,
            canvas_height - 6,
            fill="",
            outline=shadow_soft,
            width=3,
            tags="shadow_lg",
        )
        self.create_rectangle(
            6,
            8,
            canvas_width - 10,
            canvas_height - 8,
            fill="",
            outline=shadow_faint,
            width=1,
            tags="shadow_sm",
        )
        self.create_rectangle(
            4,
            4,
            canvas_width - 12,
            canvas_height - 12,
            fill=glass_fill,
            outline=highlight_edge,
            width=1,
            tags="glass_panel",
        )
        self.create_rectangle(
            8,
            8,
            canvas_width - 16,
            int(canvas_height * 0.36),
            fill=glass_gloss,
            outline="",
            tags="glass_gloss",
        )
        self.create_rectangle(
            7,
            7,
            canvas_width - 15,
            canvas_height - 15,
            fill="",
            outline=inner_line,
            width=1,
            tags="border",
        )

        self.tag_lower("shadow_lg")
        self.tag_lower("shadow_sm")
        self.tag_lower("glass_panel")
        self.tag_lower("glass_gloss")
        self.tag_raise("label")
        self.tag_raise("time")

    def update_time(self, seconds: int) -> None:
        """Update the displayed time value.

        Parameters:
            seconds: Remaining time in seconds.
        """

        self.itemconfig(self._time_text, text=self._format_time_label(seconds))

    @staticmethod
    def _format_time_label(seconds: int) -> str:
        """Format a remaining-second value as ``MM:SS``.

        Parameters:
            seconds: Remaining time in whole seconds.

        Returns:
            Formatted timer text in ``MM:SS`` style.
        """

        safe_seconds = max(0, int(seconds))
        mins, secs = divmod(safe_seconds, 60)
        return f"{mins:02d}:{secs:02d}"

    def _mix_colors(self, color1: str, color2: str, ratio: float) -> str:
        """Blend two hex colors for subtle effects."""

        def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
            hex_color = hex_color.lstrip("#")
            # type: ignore
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

        def rgb_to_hex(rgb: tuple[int, int, int]) -> str:
            return "#{:02x}{:02x}{:02x}".format(
                max(0, min(255, int(rgb[0]))),
                max(0, min(255, int(rgb[1]))),
                max(0, min(255, int(rgb[2]))),
            )

        ratio = max(0.0, min(1.0, ratio))
        rgb1 = hex_to_rgb(color1)
        rgb2 = hex_to_rgb(color2)
        blended = tuple(rgb1[i] + (rgb2[i] - rgb1[i])
                        * ratio for i in range(3))
        return rgb_to_hex(blended)  # type: ignore


class NeumorphicRadioButton(tk.Frame):
    """Neumorphic radio button with professional depth, transparency, and smooth interactions."""

    def __init__(
        self,
        master: tk.Misc,
        text: str = "",
        variable: tk.StringVar | None = None,
        value: str = "",
        command: Callable[[], None] | None = None,
        bg_color: str = "#f0f0f0",
        shadow_color: str = "#d0d0d0",
        highlight_color: str = "#ffffff",
        text_color: str = "#333333",
        accent_color: str = "#0891b2",
        state: str = "normal",
        **kwargs: Any,
    ):
        """Initialize neumorphic radio button.

        Parameters:
            master: Parent widget.
            text: Label text for the radio.
            variable: StringVar to bind to (for value tracking).
            value: Value to set in variable when selected.
            command: Callback when radio is selected.
            bg_color: Background color matching parent theme.
            shadow_color: Shadow color for neumorphic depth effect.
            highlight_color: Highlight color for inset effect.
            text_color: Text label color.
            accent_color: Accent color when selected.
            state: Widget state ('normal' or 'disabled').
        """

        super().__init__(master, bg=bg_color, **kwargs)  # type: ignore
        self.text = text
        self.variable = variable
        self.value = value
        self.command = command
        self.bg_color = bg_color
        self.shadow_color = shadow_color
        self.highlight_color = highlight_color
        self.text_color = text_color
        self.accent_color = accent_color
        self._current_state = state
        self._is_hovered = False
        self._animation_id: str | None = None

        self._radio_canvas = tk.Canvas(
            self,
            width=26,
            height=26,
            bg=bg_color,
            highlightthickness=0,
            relief="flat",
        )
        self._radio_canvas.pack(side=tk.LEFT, padx=(0, 12))

        self._label = tk.Label(
            self,
            text=text,
            bg=bg_color,
            fg=text_color,
            font=("Segoe UI", 11),
        )
        self._label.pack(side=tk.LEFT, fill="x", expand=True, pady=4)

        self._shadow_layer = None
        self._highlight_layer = None
        self._radio_circle = None

        self._radio_canvas.bind("<Button-1>", self._on_click)
        self._radio_canvas.bind("<Enter>", self._on_enter)
        self._radio_canvas.bind("<Leave>", self._on_leave)
        self._label.bind("<Button-1>", self._on_click)
        self._label.bind("<Enter>", self._on_enter)
        self._label.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_click)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

        self._update_appearance()

    def _on_enter(self, event: tk.Event | None = None) -> None:
        """Handle mouse enter for hover effect with smooth transition."""

        if self._current_state == "normal":
            self._is_hovered = True
            self._update_appearance()
            self.config(cursor="hand2")

    def _on_leave(self, event: tk.Event | None = None) -> None:
        """Handle mouse leave."""

        self._is_hovered = False
        self._update_appearance()
        self.config(cursor="")

    def _on_click(self, event: tk.Event | None = None) -> None:
        """Handle click event."""

        if self._current_state == "disabled":
            return
        self.select()

    def select(self) -> None:
        """Select this radio button and invoke callback."""

        if self.variable:
            self.variable.set(self.value)
        self._update_appearance()
        if self.command:
            self.command()

    def _update_appearance(self) -> None:
        """Update visual appearance with neumorphic depth and glassmorphism effects."""

        is_selected = self.variable and self.variable.get() == self.value

        self._radio_canvas.delete("all")

        if self._current_state == "disabled":
            self._draw_disabled(is_selected)
        elif is_selected:
            self._draw_selected()
        elif self._is_hovered:
            self._draw_hovered()
        else:
            self._draw_normal()

        if is_selected and self._current_state != "disabled":
            text_color = self.highlight_color
        elif self._current_state == "disabled":
            text_color = self.shadow_color
        else:
            text_color = self.text_color

        self._label.config(fg=text_color)

    def _draw_normal(self) -> None:
        """Draw unselected button with subtle neumorphic shadows."""

        self._draw_neumorphic_button(
            outer_fill=self.bg_color,
            outer_stroke=self.shadow_color,
            inner_fill=self.bg_color,
            is_pressed=False,
        )

    def _draw_hovered(self) -> None:
        """Draw hovered button with enhanced depth and lifted appearance."""

        self._draw_neumorphic_button(
            outer_fill=self._lighten_color(self.bg_color, 0.12),
            outer_stroke=self._darken_color(self.shadow_color, 0.3),
            inner_fill=self._lighten_color(self.bg_color, 0.12),
            is_pressed=False,
        )

    def _draw_selected(self) -> None:
        """Draw selected button with accent color and inset shadow effect."""

        self._draw_neumorphic_button(
            outer_fill=self.accent_color,
            outer_stroke=self._darken_color(self.accent_color, 0.25),
            inner_fill=self.accent_color,
            is_pressed=True,
        )

    def _draw_disabled(self, is_selected: bool) -> None:
        """Draw disabled button with muted colors and reduced contrast."""

        fill = self._mix_colors(
            self.accent_color, self.bg_color, 0.35) if is_selected else self.bg_color
        stroke = self._mix_colors(self.shadow_color, self.bg_color, 0.5)

        self._draw_neumorphic_button(
            outer_fill=fill,
            outer_stroke=stroke,
            inner_fill=fill,
            is_pressed=False,
        )

    def _draw_neumorphic_button(
        self,
        outer_fill: str,
        outer_stroke: str,
        inner_fill: str,
        is_pressed: bool,
    ) -> None:
        """Draw button with multi-layer shadows and glassmorphism effects.

        Parameters:
            outer_fill: Outer circle fill color.
            outer_stroke: Outer circle stroke color.
            inner_fill: Inner area fill color.
            is_pressed: Whether button appears pressed (inset) or raised.
        """

        if is_pressed:
            self._draw_inset_button(outer_fill, outer_stroke, inner_fill)
        else:
            self._draw_raised_button(outer_fill, outer_stroke, inner_fill)

    def _draw_raised_button(self, fill: str, stroke: str, inner_fill: str) -> None:
        """Draw raised button with multi-layer outset shadows for elevation."""

        self._shadow_layer = self._radio_canvas.create_oval(
            3, 5, 23, 23,
            fill=self._darken_color(self.bg_color, 0.25),
            outline="",
            tags="shadow",
        )
        self._highlight_layer = self._radio_canvas.create_oval(
            1, 2, 25, 20,
            fill=self._lighten_color(self.bg_color, 0.35),
            outline="",
            tags="highlight",
        )

        self._radio_circle = self._radio_canvas.create_oval(
            2, 2, 24, 24,
            fill=fill,
            outline=stroke,
            width=2,
            tags="circle",
        )

        self._radio_canvas.tag_lower("shadow")
        self._radio_canvas.tag_lower("highlight")

    def _draw_inset_button(self, fill: str, stroke: str, inner_fill: str) -> None:
        """Draw pressed/selected button with inset shadows for depth."""

        self._highlight_layer = self._radio_canvas.create_oval(
            2, 2, 12, 12,
            fill=self._lighten_color(fill, 0.4),
            outline="",
            tags="highlight",
        )

        self._radio_circle = self._radio_canvas.create_oval(
            2, 2, 24, 24,
            fill=fill,
            outline=stroke,
            width=2,
            tags="circle",
        )

        self._shadow_layer = self._radio_canvas.create_oval(
            14, 14, 22, 22,
            fill=self._darken_color(fill, 0.25),
            outline="",
            tags="shadow",
        )

        self._radio_canvas.tag_lower("shadow")

    def _lighten_color(self, color: str, amount: float) -> str:
        """Lighten a hex color by blending towards white.

        Parameters:
            color: Hex color string.
            amount: Blend amount (0.0-1.0).

        Returns:
            Lightened hex color.
        """

        return self._mix_colors(color, "#ffffff", amount)

    def _darken_color(self, color: str, amount: float) -> str:
        """Darken a hex color by blending towards black.

        Parameters:
            color: Hex color string.
            amount: Blend amount (0.0-1.0).

        Returns:
            Darkened hex color.
        """

        return self._mix_colors(color, "#000000", amount)

    def _mix_colors(self, color1: str, color2: str, ratio: float) -> str:
        """Blend two hex colors.

        Parameters:
            color1: First hex color.
            color2: Second hex color.
            ratio: Blend amount (0.0 = color1, 1.0 = color2).

        Returns:
            Blended hex color.
        """

        def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
            hex_color = hex_color.lstrip("#")
            # type: ignore
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

        def rgb_to_hex(rgb: tuple[int, int, int]) -> str:
            return "#{:02x}{:02x}{:02x}".format(
                max(0, min(255, int(rgb[0]))),
                max(0, min(255, int(rgb[1]))),
                max(0, min(255, int(rgb[2]))),
            )

        ratio = max(0.0, min(1.0, ratio))
        rgb1 = hex_to_rgb(color1)
        rgb2 = hex_to_rgb(color2)
        blended = tuple(rgb1[i] + (rgb2[i] - rgb1[i])
                        * ratio for i in range(3))
        return rgb_to_hex(blended)  # type: ignore

    def config(self, **kwargs: object) -> None:
        """Configure widget options.

        Parameters:
            state: 'normal' or 'disabled'.
            Other options are passed to parent Frame.
        """

        if "state" in kwargs:
            self._current_state = str(kwargs.pop("state"))
            self._update_appearance()

        if kwargs:
            super().config(**kwargs)

    def cget(self, option: str) -> object:
        """Get widget option value."""

        if option == "state":
            return self._current_state
        return super().cget(option)

    def invoke(self) -> None:
        """Invoke the radio button (same as clicking it)."""

        self.select()
    """Neumorphic timer display with soft shadows and rounded appearance."""

    def __init__(
        self,
        master: tk.Misc,
        width: int = 200,
        height: int = 120,
        bg_color: str = "#f0f0f0",
        shadow_color: str = "#d0d0d0",
        highlight_color: str = "#ffffff",
        text_color: str = "#333333",
        **kwargs: object,
    ):
        """Initialize neumorphic timer with dimensions and colors.

        Parameters:
            master: Parent widget.
            width: Canvas width.
            height: Canvas height.
            bg_color: Background color matching theme.
            shadow_color: Shadow color for neumorphic effect.
            highlight_color: Highlight color for neumorphic effect.
            text_color: Text color for time display.
        """

        super().__init__(
            master,
            width=width,
            height=height,
            bg=bg_color,
            highlightthickness=0,
            relief="flat",
            **kwargs,
        )
        self.bg_color = bg_color
        self.shadow_color = shadow_color
        self.highlight_color = highlight_color
        self.text_color = text_color
        self._time_text = self.create_text(
            width // 2,
            height // 2,
            text="0s",
            font=("Arial", 48, "bold"),
            fill=text_color,
            tags="time",
        )
        self._label_text = self.create_text(
            width // 2,
            height * 0.15,
            text="Time Remaining",
            font=("Arial", 11),
            fill=text_color,
            tags="label",
        )
        self._draw_neumorphic_border()

    def _draw_neumorphic_border(self) -> None:
        """Draw soft shadow and highlight borders for neumorphic effect."""

        canvas_width = int(self.cget("width"))
        canvas_height = int(self.cget("height"))
        radius = 16

        self.create_rectangle(
            4,
            4,
            canvas_width - 2,
            canvas_height - 2,
            fill=self.highlight_color,
            outline="",
            tags="highlight_border",
        )
        self.create_rectangle(
            6,
            6,
            canvas_width - 4,
            canvas_height - 4,
            fill=self.shadow_color,
            outline="",
            tags="shadow_border",
        )
        self.tag_lower("highlight_border")
        self.tag_lower("shadow_border")

    def update_time(self, seconds: int) -> None:
        """Update the displayed time value.

        Parameters:
            seconds: Remaining time in seconds.
        """

        self.itemconfig(self._time_text, text=f"{seconds}s")


class NeumorphicRadioButton(tk.Frame):
    """Neumorphic radio button widget with soft shadows and glassmorphism styling."""

    def __init__(
        self,
        master: tk.Misc,
        text: str = "",
        variable: tk.StringVar | None = None,
        value: str = "",
        command: Callable[[], None] | None = None,
        bg_color: str = "#f0f0f0",
        shadow_color: str = "#d0d0d0",
        highlight_color: str = "#ffffff",
        text_color: str = "#333333",
        accent_color: str = "#0891b2",
        state: str = "normal",
        **kwargs: str,
    ):
        """Initialize neumorphic radio button with enhanced styling.

        Parameters:
            master: Parent widget.
            text: Label text for the radio.
            variable: StringVar to bind to (for value tracking).
            value: Value to set in variable when selected.
            command: Callback when radio is selected.
            bg_color: Background color matching parent theme.
            shadow_color: Shadow color for neumorphic depth effect.
            highlight_color: Highlight color for inset effect.
            text_color: Text label color.
            accent_color: Accent color when selected.
            state: Widget state ('normal' or 'disabled').
        """

        super().__init__(master, bg=bg_color, **kwargs)  # type: ignore
        self.text = text
        self.variable = variable
        self.value = value
        self.command = command
        self.bg_color = bg_color
        self.shadow_color = shadow_color
        self.highlight_color = highlight_color
        self.text_color = text_color
        self.accent_color = accent_color
        self._current_state = state
        self._is_hovered = False

        self._radio_canvas = tk.Canvas(
            self,
            width=24,
            height=24,
            bg=bg_color,
            highlightthickness=0,
            relief="flat",
        )
        self._radio_canvas.pack(side=tk.LEFT, padx=(0, 12))

        self._label = tk.Label(
            self,
            text=text,
            bg=bg_color,
            fg=text_color,
            font=("Arial", 11),
            anchor="w",
            justify="left",
        )
        self._label.pack(side=tk.LEFT, fill="x", expand=True)

        self._shadow_layer = None
        self._highlight_layer = None
        self._radio_circle = None

        self._radio_canvas.bind("<Button-1>", self._on_click)
        self._radio_canvas.bind("<Enter>", self._on_enter)
        self._radio_canvas.bind("<Leave>", self._on_leave)
        self._label.bind("<Button-1>", self._on_click)
        self._label.bind("<Enter>", self._on_enter)
        self._label.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_click)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

        self._update_appearance()

    def _on_enter(self, event: tk.Event | None = None) -> None:
        """Handle mouse enter for hover effect."""

        if self._current_state == "normal":
            self._is_hovered = True
            self._update_appearance()

    def _on_leave(self, event: tk.Event | None = None) -> None:
        """Handle mouse leave."""

        self._is_hovered = False
        self._update_appearance()

    def _on_click(self, event: tk.Event | None = None) -> None:
        """Handle click event."""

        if self._current_state == "disabled":
            return
        self.select()

    def select(self) -> None:
        """Select this radio button and invoke callback."""

        if self.variable:
            self.variable.set(self.value)
        self._update_appearance()
        if self.command:
            self.command()

    def _update_appearance(self) -> None:
        """Update visual appearance with neumorphic and glassmorphism effects."""

        is_selected = self.variable and self.variable.get() == self.value

        self._radio_canvas.delete("all")

        if self._current_state == "disabled":
            self._draw_disabled(is_selected)
        elif is_selected:
            self._draw_selected()
        elif self._is_hovered:
            self._draw_hovered()
        else:
            self._draw_normal()

        if is_selected and self._current_state != "disabled":
            text_color = self.highlight_color
        elif self._current_state == "disabled":
            text_color = self.shadow_color
        else:
            text_color = self.text_color

        self._label.config(fg=text_color)

    def _draw_normal(self) -> None:
        """Draw unselected button with soft neumorphic shadows."""

        self._draw_neumorphic_button(
            outer_fill=self.bg_color,
            outer_stroke=self.shadow_color,
            inner_fill=self.bg_color,
            is_pressed=False,
        )

    def _draw_hovered(self) -> None:
        """Draw hovered button with enhanced depth."""

        self._draw_neumorphic_button(
            outer_fill=self._lighten_color(self.bg_color, 0.05),
            outer_stroke=self._darken_color(self.shadow_color, 0.15),
            inner_fill=self._lighten_color(self.bg_color, 0.05),
            is_pressed=False,
        )

    def _draw_selected(self) -> None:
        """Draw selected button with accent color and inset shadow effect."""

        self._draw_neumorphic_button(
            outer_fill=self.accent_color,
            outer_stroke=self._darken_color(self.accent_color, 0.2),
            inner_fill=self.accent_color,
            is_pressed=True,
        )

    def _draw_disabled(self, is_selected: bool) -> None:
        """Draw disabled button with muted colors."""

        fill = self._mix_colors(
            self.accent_color, self.bg_color, 0.3) if is_selected else self.bg_color
        stroke = self._mix_colors(self.shadow_color, self.bg_color, 0.4)

        self._draw_neumorphic_button(
            outer_fill=fill,
            outer_stroke=stroke,
            inner_fill=fill,
            is_pressed=False,
        )

    def _draw_neumorphic_button(
        self,
        outer_fill: str,
        outer_stroke: str,
        inner_fill: str,
        is_pressed: bool,
    ) -> None:
        """Draw button with neumorphic shadows and glassmorphism effects.

        Parameters:
            outer_fill: Outer circle fill color.
            outer_stroke: Outer circle stroke color.
            inner_fill: Inner area fill color.
            is_pressed: Whether button appears pressed (inset) or raised.
        """

        if is_pressed:
            self._draw_inset_button(outer_fill, outer_stroke, inner_fill)
        else:
            self._draw_raised_button(outer_fill, outer_stroke, inner_fill)

    def _draw_raised_button(self, fill: str, stroke: str, inner_fill: str) -> None:
        """Draw raised button with outset shadows."""

        self._shadow_layer = self._radio_canvas.create_oval(
            2, 4, 22, 22,
            fill=self._darken_color(self.bg_color, 0.12),
            outline="",
            tags="shadow",
        )
        self._highlight_layer = self._radio_canvas.create_oval(
            1, 2, 23, 20,
            fill=self._lighten_color(self.bg_color, 0.18),
            outline="",
            tags="highlight",
        )

        self._radio_circle = self._radio_canvas.create_oval(
            3, 3, 21, 21,
            fill=fill,
            outline=stroke,
            width=1.5,
            tags="circle",
        )

        self._radio_canvas.tag_lower("shadow")
        self._radio_canvas.tag_lower("highlight")

    def _draw_inset_button(self, fill: str, stroke: str, inner_fill: str) -> None:
        """Draw pressed/selected button with inset shadows."""

        self._highlight_layer = self._radio_canvas.create_oval(
            2, 2, 10, 10,
            fill=self._lighten_color(fill, 0.25),
            outline="",
            tags="highlight",
        )

        self._radio_circle = self._radio_canvas.create_oval(
            3, 3, 21, 21,
            fill=fill,
            outline=stroke,
            width=1.5,
            tags="circle",
        )

        self._shadow_layer = self._radio_canvas.create_oval(
            12, 12, 20, 20,
            fill=self._darken_color(fill, 0.15),
            outline="",
            tags="shadow",
        )

        self._radio_canvas.tag_lower("shadow")

    def _lighten_color(self, color: str, amount: float) -> str:
        """Lighten a hex color by blending towards white.

        Parameters:
            color: Hex color string.
            amount: Blend amount (0.0-1.0).

        Returns:
            Lightened hex color.
        """

        return self._mix_colors(color, "#ffffff", amount)

    def _darken_color(self, color: str, amount: float) -> str:
        """Darken a hex color by blending towards black.

        Parameters:
            color: Hex color string.
            amount: Blend amount (0.0-1.0).

        Returns:
            Darkened hex color.
        """

        return self._mix_colors(color, "#000000", amount)

    def _mix_colors(self, color1: str, color2: str, ratio: float) -> str:
        """Blend two hex colors.

        Parameters:
            color1: First hex color.
            color2: Second hex color.
            ratio: Blend amount (0.0 = color1, 1.0 = color2).

        Returns:
            Blended hex color.
        """

        def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
            hex_color = hex_color.lstrip("#")
            # type: ignore
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

        def rgb_to_hex(rgb: tuple[int, int, int]) -> str:
            return "#{:02x}{:02x}{:02x}".format(max(0, min(255, int(rgb[0]))), max(0, min(255, int(rgb[1]))), max(0, min(255, int(rgb[2]))))

        ratio = max(0.0, min(1.0, ratio))
        rgb1 = hex_to_rgb(color1)
        rgb2 = hex_to_rgb(color2)
        blended = tuple(rgb1[i] + (rgb2[i] - rgb1[i])
                        * ratio for i in range(3))
        return rgb_to_hex(blended)  # type: ignore

    def config(self, **kwargs: object) -> None:
        """Configure widget options.

        Parameters:
            state: 'normal' or 'disabled'.
            Other options are passed to parent Frame.
        """

        if "state" in kwargs:
            self._current_state = str(kwargs.pop("state"))
            self._update_appearance()

        if kwargs:
            super().config(**kwargs)

    def cget(self, option: str) -> object:
        """Get widget option value."""

        if option == "state":
            return self._current_state
        return super().cget(option)

    def invoke(self) -> None:
        """Invoke the radio button (same as clicking it)."""

        self.select()


class NeumorphicRadio(tk.Canvas):
    """Neumorphic radio button with soft appearance and smooth interaction."""

    def __init__(
        self,
        master: tk.Misc,
        text: str = "",
        command: Callable[[], None] | None = None,
        bg_color: str = "#f0f0f0",
        shadow_color: str = "#d0d0d0",
        highlight_color: str = "#ffffff",
        text_color: str = "#333333",
        accent_color: str = "#0891b2",
        **kwargs: object,
    ):
        """Initialize neumorphic radio button.

        Parameters:
            master: Parent widget.
            text: Label text for the radio.
            command: Callback when radio is selected.
            bg_color: Background color.
            shadow_color: Shadow color for neumorphic effect.
            highlight_color: Highlight color for neumorphic effect.
            text_color: Text color.
            accent_color: Accent color when selected.
        """

        super().__init__(
            master,
            width=20,
            height=20,
            bg=bg_color,
            highlightthickness=0,
            relief="flat",
            **kwargs,
        )
        self.text = text
        self.command = command
        self.bg_color = bg_color
        self.shadow_color = shadow_color
        self.highlight_color = highlight_color
        self.text_color = text_color
        self.accent_color = accent_color
        self._selected = False
        self._radio_circle = self.create_oval(
            4, 4, 16, 16, fill=bg_color, outline=shadow_color, width=2
        )
        self.bind("<Button-1>", self._on_click)
        self._draw_neumorphic()

    def _draw_neumorphic(self) -> None:
        """Redraw the neumorphic effect based on selection state."""

        if self._selected:
            self.itemconfig(self._radio_circle,
                            fill=self.accent_color, outline=self.accent_color)
            self.create_oval(
                8, 8, 12, 12, fill=self.highlight_color, tags="inner_dot"
            )
        else:
            self.itemconfig(self._radio_circle,
                            fill=self.bg_color, outline=self.shadow_color)
            self.delete("inner_dot")

    def _on_click(self, event: tk.Event) -> None:
        """Handle click event."""

        self.select()

    def select(self) -> None:
        """Select this radio button."""

        self._selected = True
        self._draw_neumorphic()
        if self.command:
            self.command()

    def deselect(self) -> None:
        """Deselect this radio button."""

        self._selected = False
        self._draw_neumorphic()

    def is_selected(self) -> bool:
        """Return whether this radio button is selected."""

        return self._selected


class NeumorphicRadioGroup(ttk.Frame):
    """Group of neumorphic radio buttons with mutual exclusivity."""

    def __init__(
        self,
        master: tk.Misc,
        options: list[str],
        command: Callable[[str], None] | None = None,
        bg_color: str = "#f0f0f0",
        shadow_color: str = "#d0d0d0",
        highlight_color: str = "#ffffff",
        text_color: str = "#333333",
        accent_color: str = "#0891b2",
        **kwargs: object,
    ):
        """Initialize neumorphic radio group.

        Parameters:
            master: Parent widget.
            options: List of radio button labels.
            command: Callback when selection changes, receives the selected value.
            bg_color: Background color.
            shadow_color: Shadow color for neumorphic effect.
            highlight_color: Highlight color for neumorphic effect.
            text_color: Text color.
            accent_color: Accent color when selected.
        """

        super().__init__(master, **kwargs)
        self.options = options
        self.command = command
        self.bg_color = bg_color
        self._radios: list[NeumorphicRadio] = []
        self._selected_value: str | None = None

        for option in options:
            radio_frame = ttk.Frame(self)
            radio_frame.pack(fill="x", pady=4)

            radio_canvas = NeumorphicRadio(
                radio_frame,
                text=option,
                bg_color=bg_color,
                shadow_color=shadow_color,
                highlight_color=highlight_color,
                text_color=text_color,
                accent_color=accent_color,
                command=lambda opt=option: self._on_radio_select(opt),
            )
            radio_canvas.pack(side=tk.LEFT, padx=(0, 8))

            label = ttk.Label(
                radio_frame,
                text=option,
                foreground=text_color,
            )
            label.pack(side=tk.LEFT, fill="x", expand=True)
            label.bind("<Button-1>", lambda e,
                       opt=option: self._on_radio_select(opt))

            self._radios.append((option, radio_canvas))

    def _on_radio_select(self, value: str) -> None:
        """Handle radio selection change.

        Parameters:
            value: The selected option value.
        """

        for opt, radio in self._radios:
            if opt == value:
                radio.select()
                self._selected_value = value
            else:
                radio.deselect()

        if self.command:
            self.command(value)

    def get(self) -> str | None:
        """Return the currently selected value."""

        return self._selected_value

    def set(self, value: str) -> None:
        """Set the selected value.

        Parameters:
            value: The option value to select.
        """

        if value in self.options:
            self._on_radio_select(value)
