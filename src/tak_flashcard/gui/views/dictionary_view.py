"""Dictionary browsing view."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Callable, Iterable

from tak_flashcard.db.models import Word
from tak_flashcard.features.dictionary.service import DictionaryService

_COLUMNS: list[tuple[str, str]] = [
    ("english", "English"),
    ("vietnamese", "Vietnamese"),
    ("pos", "Part of Speech"),
    ("difficulty", "Difficulty"),
]

_NUMERIC_COLS: frozenset[str] = frozenset({"difficulty"})


class DictionaryView(ttk.Frame):
    """View to browse and search vocabulary."""

    def __init__(self, master: tk.Misc, service: DictionaryService, on_back: Callable[[], None]):
        """Initialize dictionary view with service and navigation."""

        super().__init__(master, padding=10)
        self.service = service

        self._sort_col: str | None = None
        self._sort_ascending: bool = True

        search_frame = ttk.Frame(self)
        ttk.Label(search_frame, text="Search").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        entry = ttk.Entry(search_frame, textvariable=self.search_var)
        entry.pack(side=tk.LEFT, fill="x", expand=True, padx=4)
        ttk.Button(search_frame, text="Go", command=self.perform_search).pack(
            side=tk.LEFT, padx=4)
        ttk.Button(search_frame, text="Back", command=on_back).pack(
            side=tk.LEFT, padx=4)
        search_frame.pack(fill="x", pady=6)

        self.tree = ttk.Treeview(
            self,
            columns=tuple(col for col, _ in _COLUMNS),
            show="headings",
        )
        for col, text in _COLUMNS:
            self.tree.heading(
                col, text=text, command=lambda c=col: self._on_heading_click(c))
            self.tree.column(col, width=150, anchor=tk.W)
        self.tree.pack(fill="both", expand=True)
        self.refresh()

    def _on_heading_click(self, col: str) -> None:
        """Handle a column heading click: toggle direction on the same column,
        or switch to ascending on a new column."""

        if self._sort_col == col:
            self._sort_ascending = not self._sort_ascending
        else:
            self._sort_col = col
            self._sort_ascending = True

        self._apply_sort()

    def _apply_sort(self) -> None:
        """Sort the current treeview rows by the active sort column and direction."""

        if self._sort_col is None:
            return

        rows = [
            (self.tree.set(item, self._sort_col), item)
            for item in self.tree.get_children("")
        ]

        numeric = self._sort_col in _NUMERIC_COLS
        rows.sort(
            key=lambda pair: float(pair[0]) if numeric else pair[0].lower(),
            reverse=not self._sort_ascending,
        )

        for index, (_, item) in enumerate(rows):
            self.tree.move(item, "", index)

        self._refresh_headings()

    def _refresh_headings(self) -> None:
        """Update all column heading labels to reflect the active sort state."""

        for col, label in _COLUMNS:
            if col == self._sort_col:
                indicator = " ▲" if self._sort_ascending else " ▼"
                self.tree.heading(col, text=label + indicator)
            else:
                self.tree.heading(col, text=label)

    def _populate(self, words: Iterable[Word]) -> None:
        """Clear the tree and insert the given word records, then re-apply any active sort."""

        for item in self.tree.get_children():
            self.tree.delete(item)
        for word in words:
            self.tree.insert("", tk.END, values=(
                word.english, word.vietnamese, word.part_of_speech, f"{word.difficulty:.2f}"))
        self._apply_sort()

    def refresh(self) -> None:
        """Load all words into the tree view."""

        self._populate(self.service.all_words())

    def perform_search(self) -> None:
        """Search and update the list."""

        query = self.search_var.get().strip()
        self._populate(self.service.search(query))
