"""Dictionary browsing view."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Callable

from tak_flashcard.features.dictionary.service import DictionaryService


class DictionaryView(ttk.Frame):
    """View to browse and search vocabulary."""

    def __init__(self, master: tk.Misc, service: DictionaryService, on_back: Callable[[], None]):
        """Initialize dictionary view with service and navigation."""

        super().__init__(master, padding=10)
        self.service = service
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

        self.tree = ttk.Treeview(self, columns=(
            "english", "vietnamese", "pos", "difficulty"), show="headings")
        for col, text in [
            ("english", "English"),
            ("vietnamese", "Vietnamese"),
            ("pos", "Part of Speech"),
            ("difficulty", "Difficulty"),
        ]:
            self.tree.heading(col, text=text)
            self.tree.column(col, width=150, anchor=tk.W)
        self.tree.pack(fill="both", expand=True)
        self.refresh()

    def refresh(self) -> None:
        """Load all words into the tree view."""

        for item in self.tree.get_children():
            self.tree.delete(item)
        for word in self.service.all_words():
            self.tree.insert("", tk.END, values=(
                word.english, word.vietnamese, word.part_of_speech, f"{word.difficulty:.2f}"))

    def perform_search(self) -> None:
        """Search and update the list."""

        query = self.search_var.get().strip()
        for item in self.tree.get_children():
            self.tree.delete(item)
        for word in self.service.search(query):
            self.tree.insert("", tk.END, values=(
                word.english, word.vietnamese, word.part_of_speech, f"{word.difficulty:.2f}"))
