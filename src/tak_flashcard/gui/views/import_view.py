"""Import vocabulary view for loading CSV files into the database."""

from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import filedialog, ttk
from typing import Callable

from sqlalchemy.orm import Session

from tak_flashcard.data.seed.importer import ImportResult, import_vocab_file, read_csv_headers


_GUIDE_TEXT = (
    "Import a CSV file to update the vocabulary database.\n\n"
    "Steps:\n"
    "  1. Browse to a CSV file — the first row is treated as the header.\n"
    "  2. Use the Column Mapping dropdowns to tell the app which columns\n"
    "     contain the English word, Vietnamese translation, and (optionally)\n"
    "     the part of speech.\n"
    "  3. Choose an import mode and click Import.\n\n"
    "Modes:\n"
    "  • Replace — deletes all existing words, then inserts the new ones.\n"
    "  • Append  — keeps existing words and adds the new ones alongside them.\n"
    "               Duplicate options (words whose English text already exists):\n"
    "               - Overwrite: replaces the translation and part-of-speech.\n"
    "               - Keep original: leaves the existing record untouched.\n"
    "               - Reset difficulty: resets score history when overwriting.\n\n"
)


class ImportView(ttk.Frame):
    """View that lets the user pick a CSV file and import it into the database."""

    def __init__(
        self,
        master: tk.Misc,
        db: Session,
        on_back: Callable[[], None],
        on_success: Callable[[], None] | None = None,
    ):
        """Initialise all import-view widgets and state.

        Parameters:
            master: Parent Tkinter widget.
            db: Active SQLAlchemy session used to write imported words.
            on_back: Callback to return to the previous screen.
            on_success: Optional callback invoked automatically after a
                successful import when the view is in forced mode.
        """

        super().__init__(master, padding=16)
        self.db = db
        self.on_back = on_back
        self._on_success = on_success
        self._forced = False
        self._selected_path: Path | None = None

        self._build_header()
        self._build_forced_banner()
        self._build_guide()
        self._build_file_row()
        self._build_column_map_row()
        self._build_mode_row()
        self._build_action_row()
        self._build_status_area()

    # ── layout helpers ────────────────────────────────────────────────────────

    def _build_header(self) -> None:
        """Render the section title."""

        ttk.Label(self, text="Import Vocabulary", font=("Arial", 15, "bold")).pack(
            anchor=tk.W, pady=(0, 6)
        )

    def _build_forced_banner(self) -> None:
        """Render the notice shown when the database is empty and import is required."""

        self._forced_banner = ttk.Label(
            self,
            text="",
            foreground="#b85c00",
            font=("Arial", 11),
            justify=tk.LEFT,
        )
        self._forced_banner.pack(anchor=tk.W, pady=(0, 8))

    def _build_guide(self) -> None:
        """Render the collapsible user guide panel."""

        guide_frame = ttk.LabelFrame(self, text="Guide", padding=8)
        ttk.Label(guide_frame, text=_GUIDE_TEXT, justify=tk.LEFT).pack(
            anchor=tk.W
        )
        guide_frame.pack(fill="x", pady=(0, 10))

    def _build_file_row(self) -> None:
        """Render the file-picker row."""

        row = ttk.LabelFrame(self, text="CSV File", padding=8)
        self._path_var = tk.StringVar(value="No file selected")
        ttk.Label(row, textvariable=self._path_var, foreground="gray").pack(
            side=tk.LEFT, fill="x", expand=True
        )
        ttk.Button(row, text="Browse…", command=self._browse_file).pack(
            side=tk.RIGHT, padx=(8, 0)
        )
        row.pack(fill="x", pady=(0, 8))

    def _build_column_map_row(self) -> None:
        """Render the column-mapping dropdowns.

        The frame is created but kept hidden until a file is selected. Once
        :meth:`_load_columns` populates it with the CSV headers the frame is
        packed into the layout.
        """

        self._col_map_frame = ttk.LabelFrame(
            self, text="Column Mapping", padding=8)

        eng_row = ttk.Frame(self._col_map_frame)
        ttk.Label(eng_row, text="English *", width=18,
                  anchor=tk.W).pack(side=tk.LEFT)
        self._english_var = tk.StringVar()
        self._english_combo = ttk.Combobox(
            eng_row, textvariable=self._english_var, state="readonly", width=30
        )
        self._english_combo.pack(side=tk.LEFT, padx=(8, 0))
        self._english_combo.bind(
            "<<ComboboxSelected>>", self._on_column_selected)
        eng_row.pack(anchor=tk.W, pady=4)

        vn_row = ttk.Frame(self._col_map_frame)
        ttk.Label(vn_row, text="Vietnamese *", width=18,
                  anchor=tk.W).pack(side=tk.LEFT)
        self._vietnamese_var = tk.StringVar()
        self._vietnamese_combo = ttk.Combobox(
            vn_row, textvariable=self._vietnamese_var, state="readonly", width=30
        )
        self._vietnamese_combo.pack(side=tk.LEFT, padx=(8, 0))
        self._vietnamese_combo.bind(
            "<<ComboboxSelected>>", self._on_column_selected)
        vn_row.pack(anchor=tk.W, pady=4)

        pos_row = ttk.Frame(self._col_map_frame)
        ttk.Label(pos_row, text="Part of Speech",
                  width=18, anchor=tk.W).pack(side=tk.LEFT)
        self._pos_var = tk.StringVar()
        self._pos_combo = ttk.Combobox(
            pos_row, textvariable=self._pos_var, state="readonly", width=30
        )
        self._pos_combo.pack(side=tk.LEFT, padx=(8, 0))
        pos_row.pack(anchor=tk.W, pady=4)

        ttk.Label(
            self._col_map_frame,
            text="* Required",
            foreground="gray",
            font=("Arial", 9),
        ).pack(anchor=tk.W, pady=(4, 0))

    def _build_mode_row(self) -> None:
        """Render import-mode radio buttons and Append-specific duplicate options."""

        row = ttk.LabelFrame(self, text="Import Mode", padding=8)
        self._mode_frame = row
        self._mode_var = tk.StringVar(value="append")
        ttk.Radiobutton(
            row,
            text="Append  (keep existing words, add new ones)",
            variable=self._mode_var,
            value="append",
            command=self._on_mode_changed,
        ).pack(anchor=tk.W, pady=2)
        ttk.Radiobutton(
            row,
            text="Replace  (delete ALL existing words, then insert new ones)",
            variable=self._mode_var,
            value="replace",
            command=self._on_mode_changed,
        ).pack(anchor=tk.W, pady=2)

        self._append_options_frame = ttk.Frame(row)
        ttk.Label(
            self._append_options_frame,
            text="Duplicate words (same English):",
            font=("Arial", 9),
        ).pack(anchor=tk.W, pady=(6, 2))

        self._overwrite_var = tk.BooleanVar(value=False)
        self._overwrite_check = ttk.Checkbutton(
            self._append_options_frame,
            text="Overwrite duplicate words (update translation & part-of-speech)",
            variable=self._overwrite_var,
            command=self._on_overwrite_changed,
        )
        self._overwrite_check.pack(anchor=tk.W, padx=(16, 0))

        self._reset_difficulty_var = tk.BooleanVar(value=False)
        self._reset_difficulty_check = ttk.Checkbutton(
            self._append_options_frame,
            text="Reset difficulty for overwritten words",
            variable=self._reset_difficulty_var,
        )
        self._reset_difficulty_check.pack(anchor=tk.W, padx=(32, 0))
        self._reset_difficulty_check.state(["disabled"])

        self._append_options_frame.pack(anchor=tk.W, fill="x", pady=(4, 0))
        row.pack(fill="x", pady=(0, 10))

    def _build_action_row(self) -> None:
        """Render the Import and Back buttons."""

        row = ttk.Frame(self)
        self._import_btn = ttk.Button(
            row, text="Import", command=self._run_import, state="disabled"
        )
        self._import_btn.pack(side=tk.LEFT, padx=(0, 8))
        self._back_btn = ttk.Button(row, text="Back", command=self.on_back)
        self._back_btn.pack(side=tk.LEFT)
        row.pack(anchor=tk.W, pady=(0, 10))

    def _build_status_area(self) -> None:
        """Render the result / status label."""

        self._status_var = tk.StringVar(value="")
        self._status_label = ttk.Label(
            self, textvariable=self._status_var, wraplength=700, justify=tk.LEFT
        )
        self._status_label.pack(anchor=tk.W)

    # ── event handlers ────────────────────────────────────────────────────────

    def _on_mode_changed(self) -> None:
        """Show or hide Append-specific options based on the selected mode."""

        if self._mode_var.get() == "append":
            self._append_options_frame.pack(anchor=tk.W, fill="x", pady=(4, 0))
        else:
            self._append_options_frame.pack_forget()

    def _on_overwrite_changed(self) -> None:
        """Enable or disable the reset-difficulty checkbox based on overwrite state."""

        if self._overwrite_var.get():
            self._reset_difficulty_check.state(["!disabled"])
        else:
            self._reset_difficulty_var.set(False)
            self._reset_difficulty_check.state(["disabled"])

    def _browse_file(self) -> None:
        """Open a file-picker dialog, update the displayed path, and load column headers."""

        chosen = filedialog.askopenfilename(
            title="Select vocabulary CSV",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        )
        if not chosen:
            return
        self._selected_path = Path(chosen)
        self._path_var.set(str(self._selected_path))
        self._import_btn.config(state="disabled")
        self._set_status("")
        self._load_columns()

    def _load_columns(self) -> None:
        """Read the CSV header row and populate the column-mapping dropdowns.

        Attempts to auto-select columns whose names contain common keywords.
        Shows the column-mapping frame and updates the Import button state.
        """

        if self._selected_path is None:
            return
        headers = read_csv_headers(self._selected_path)
        if not headers:
            self._set_status(
                "Could not read column headers from the selected file.", error=True
            )
            return

        self._english_var.set("")
        self._vietnamese_var.set("")
        self._pos_var.set("(none)")

        self._english_combo["values"] = headers
        self._vietnamese_combo["values"] = headers
        self._pos_combo["values"] = ["(none)"] + headers

        lower = [h.lower() for h in headers]
        for i, h in enumerate(lower):
            if not self._english_var.get() and ("english" in h or h in ("en", "word")):
                self._english_var.set(headers[i])
            if not self._vietnamese_var.get() and ("viet" in h or h in ("vn", "vi")):
                self._vietnamese_var.set(headers[i])
            if self._pos_var.get() == "(none)" and ("part" in h or "pos" in h or "speech" in h):
                self._pos_var.set(headers[i])

        self._col_map_frame.pack(fill="x", pady=(
            0, 10), before=self._mode_frame)
        self._on_column_selected()

    def _on_column_selected(self, _event: object = None) -> None:
        """Enable the Import button when both required columns are mapped.

        Parameters:
            _event: Unused Tkinter event argument passed by ComboboxSelected.
        """

        if self._english_var.get() and self._vietnamese_var.get():
            self._import_btn.config(state="normal")
        else:
            self._import_btn.config(state="disabled")

    def _run_import(self) -> None:
        """Build the column mapping and perform the import operation."""

        if self._selected_path is None:
            self._set_status("Please select a CSV file first.", error=True)
            return

        column_map: dict[str, str] = {
            "english": self._english_var.get(),
            "vietnamese": self._vietnamese_var.get(),
        }
        pos = self._pos_var.get()
        if pos and pos != "(none)":
            column_map["part_of_speech"] = pos

        replace = self._mode_var.get() == "replace"
        overwrite_duplicates = (not replace) and self._overwrite_var.get()
        reset_difficulty = overwrite_duplicates and self._reset_difficulty_var.get()
        self._set_status("Importing…")
        self.update_idletasks()

        result: ImportResult = import_vocab_file(
            self.db, self._selected_path, column_map,
            replace=replace,
            overwrite_duplicates=overwrite_duplicates,
            reset_difficulty=reset_difficulty,
        )

        if result.errors:
            self._set_status(
                "Import failed — validation errors:\n" +
                "\n".join(f"  • {e}" for e in result.errors),
                error=True,
            )
            return

        self._set_status(self._format_success(result), success=True)
        if self._forced and self._on_success is not None:
            self.after(800, self._on_success)

    # ── helpers ────────────────────────────────────────────────────────────────

    def configure_mode(self, forced: bool) -> None:
        """Switch the view between forced-import and normal modes.

        In forced mode the Back button is hidden and a notice banner is shown
        prompting the user to import before the application can be used. In
        normal mode the banner is hidden and the Back button is visible.

        Parameters:
            forced: ``True`` to enable forced-import mode, ``False`` for normal.
        """

        self._forced = forced
        if forced:
            self._forced_banner.config(
                text=(
                    "No vocabulary found in the database.\n"
                    "Please import a CSV file to continue using the application."
                )
            )
            self._back_btn.pack_forget()
        else:
            self._forced_banner.config(text="")
            self._back_btn.pack(side=tk.LEFT)

    @staticmethod
    def _format_success(result: ImportResult) -> str:
        """Build a success message from an :class:`ImportResult`."""

        parts: list[str] = [
            f"✓ Import complete — {result.added} word(s) added."]
        if result.removed:
            parts.append(
                f"  {result.removed} existing word(s) were removed (Replace mode).")
        if result.updated:
            parts.append(
                f"  {result.updated} duplicate word(s) were overwritten.")
        if result.skipped:
            parts.append(
                f"  {result.skipped} duplicate word(s) were kept unchanged.")
        if result.backup_path:
            parts.append(f"  Backup saved to: {result.backup_path}")
        return "\n".join(parts)

    def _set_status(
        self,
        message: str,
        *,
        error: bool = False,
        success: bool = False,
    ) -> None:
        """Update the status label text and colour.

        Parameters:
            message: Text to display.
            error: Show in red to indicate a failure.
            success: Show in green to indicate success.
        """

        self._status_var.set(message)
        if error:
            self._status_label.config(foreground="red")
        elif success:
            self._status_label.config(foreground="green")
        else:
            self._status_label.config(foreground="black")
