"""Tkinter application entry point."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import cast

from tak_flashcard.config import APP_NAME, WINDOW_HEIGHT, WINDOW_WIDTH, ensure_data_dirs
from tak_flashcard.core.settings import Settings, SettingsManager
from tak_flashcard.db.repo import get_word_count
from tak_flashcard.db.session import SessionLocal, init_db
from tak_flashcard.features.dictionary.service import DictionaryService
from tak_flashcard.features.flashcard.controller import FlashcardController
from tak_flashcard.features.flashcard.states import SessionConfig
from tak_flashcard.gui.styles import apply_appearance_settings
from tak_flashcard.gui.views.dictionary_view import DictionaryView
from tak_flashcard.gui.views.flashcard_view import FlashcardSessionView, FlashcardView
from tak_flashcard.gui.views.guide_view import GuideView
from tak_flashcard.gui.views.home_view import HomeView
from tak_flashcard.gui.views.import_view import ImportView
from tak_flashcard.gui.views.results_view import ResultsView
from tak_flashcard.gui.views.settings_view import SettingsView


class FlashcardApp(tk.Tk):
    """Main Tkinter application container."""

    def __init__(self):
        """Initialize the application window and views."""

        super().__init__()
        ensure_data_dirs()
        self.title(APP_NAME)
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.style = ttk.Style(self)
        self.style.theme_use("clam")

        init_db()
        self.db = SessionLocal()
        self.settings_manager = SettingsManager()

        apply_appearance_settings(
            self.style, self.settings_manager.settings.appearance)

        self.controller = FlashcardController(self.db)
        self.dictionary_service = DictionaryService(self.db)
        self._current_view: str = ""

        outer = ttk.Frame(self)
        outer.pack(fill="both", expand=True)

        self._canvas = tk.Canvas(outer, highlightthickness=0)
        self._scrollbar = ttk.Scrollbar(
            outer, orient="vertical", command=self._canvas.yview)
        self._canvas.configure(yscrollcommand=self._scrollbar.set)

        self._scrollbar.pack(side="right", fill="y")
        self._canvas.pack(side="left", fill="both", expand=True)

        container = ttk.Frame(self._canvas)
        self._canvas_window = self._canvas.create_window(
            (0, 0), window=container, anchor="nw")

        container.bind("<Configure>", self._on_inner_configure)
        self._canvas.bind("<Configure>", self._on_canvas_configure)
        self._canvas.bind("<Enter>", self._bind_mousewheel)
        self._canvas.bind("<Leave>", self._unbind_mousewheel)

        self.frames: dict[str, ttk.Frame] = {}

        self.frames["home"] = HomeView(container, self.navigate)
        self.frames["flashcard"] = FlashcardView(
            container,
            self.start_flashcard_session,
            lambda: self.navigate("home"),
        )
        self.frames["flashcard_session"] = FlashcardSessionView(
            container, self.controller, self._on_session_end
        )
        self.frames["dictionary"] = DictionaryView(
            container, self.dictionary_service, lambda: self.navigate("home"))
        self.frames["guide"] = GuideView(
            container, lambda: self.navigate("home"))
        self.frames["settings"] = SettingsView(
            container, self.settings_manager, lambda: self.navigate("home"), self.apply_appearance)
        self.frames["import"] = ImportView(
            container, self.db, lambda: self.navigate("home"),
            on_success=lambda: self.navigate("home"),
        )
        self.frames["results"] = ResultsView(
            container,
            on_back=lambda: self.navigate("flashcard"),
            on_home=lambda: self.navigate("home"),
        )

        for frame in self.frames.values():
            frame.grid(row=0, column=0, sticky="nsew")

        if get_word_count(self.db) == 0:
            self.navigate("import")
        else:
            self.navigate("home")

    def apply_appearance(self, settings: Settings) -> None:
        """Apply appearance settings to the application immediately."""
        apply_appearance_settings(self.style, settings.appearance)

    def _on_session_end(self, summary) -> None:
        """Populate the results view with the session summary and navigate to it.

        Parameters:
            summary: A :class:`SessionSummary` produced at end of session.
        """

        results_frame = self.frames.get("results")
        if isinstance(results_frame, ResultsView):
            results_frame.update_summary(summary)
        self.navigate("results")

    def start_flashcard_session(self, config: SessionConfig) -> None:
        """Start a flashcard session and navigate to the dedicated session view.

        Parameters:
            config: Session settings collected from the flashcard configuration view.
        """

        session_frame = self.frames.get("flashcard_session")
        if isinstance(session_frame, FlashcardSessionView):
            session_frame.begin_session(config)
            self.navigate("flashcard_session")

    def navigate(self, key: str) -> None:
        """Show the requested frame or exit."""

        if key == "exit":
            self.destroy()
            return
        frame = self.frames.get(key)
        if frame:
            if key == "dictionary" and isinstance(frame, DictionaryView):
                frame.refresh()
            elif key == "import" and isinstance(frame, ImportView):
                frame._set_status("")
                frame.configure_mode(get_word_count(self.db) == 0)
            frame.tkraise()
            self._current_view = key
            self._update_global_shortcuts()

    def _update_global_shortcuts(self) -> None:
        """Rebind root-level keyboard shortcuts for the currently active view.

        All previously registered shortcuts are cleared before applying the new
        set so there is no cross-view interference.
        """

        _events = ("<Return>", "<Escape>", "<space>",
                   "<Key-1>", "<Key-2>", "<Key-3>", "<Key-4>")
        for event in _events:
            self.unbind(event)

        key = self._current_view

        if key == "flashcard":
            fc = cast(FlashcardView, self.frames["flashcard"])
            self.bind("<Return>", lambda _e: fc.start_session())
            self.bind("<Escape>", lambda _e: self.navigate("home"))

        elif key == "flashcard_session":
            session = cast(FlashcardSessionView, self.frames["flashcard_session"])
            self.bind("<Return>", lambda _e: session.on_enter_key())
            self.bind("<space>", lambda _e: session.on_space_key())
            self.bind("<Escape>", lambda _e: session._handle_exit_session())
            for _i in range(1, 5):
                self.bind(f"<Key-{_i}>", lambda _e,
                          n=_i: session.on_number_key(n))

        elif key == "dictionary":
            dv = cast(DictionaryView, self.frames["dictionary"])
            self.bind("<Return>", lambda _e: dv.perform_search())
            self.bind("<Escape>", lambda _e: self.navigate("home"))

        elif key == "guide":
            self.bind("<Escape>", lambda _e: self.navigate("home"))

        elif key == "settings":
            self.bind("<Escape>", lambda _e: self.navigate("home"))

        elif key == "results":
            self.bind("<Return>", lambda _e: self.navigate("flashcard"))
            self.bind("<Escape>", lambda _e: self.navigate("home"))

        elif key == "import":
            import_frame = cast(ImportView, self.frames["import"])
            self.bind(
                "<Escape>",
                lambda _e: (
                    None if import_frame._forced else self.navigate("home")),
            )

    def _on_inner_configure(self, event: tk.Event) -> None:
        """Update the canvas scroll region when the inner frame resizes."""
        self._canvas.configure(scrollregion=self._canvas.bbox("all"))

    def _on_canvas_configure(self, event: tk.Event) -> None:
        """Stretch the inner frame to always fill the canvas width."""
        self._canvas.itemconfigure(self._canvas_window, width=event.width)

    def _bind_mousewheel(self, event: tk.Event) -> None:
        """Attach mousewheel scrolling when the pointer enters the canvas."""
        self._canvas.bind_all(
            "<Button-4>", lambda e: self._canvas.yview_scroll(-1, "units"))
        self._canvas.bind_all(
            "<Button-5>", lambda e: self._canvas.yview_scroll(1, "units"))

    def _unbind_mousewheel(self, event: tk.Event) -> None:
        """Detach mousewheel scrolling when the pointer leaves the canvas."""
        self._canvas.unbind_all("<Button-4>")
        self._canvas.unbind_all("<Button-5>")


def run() -> None:
    """Start the Tkinter main loop."""

    app = FlashcardApp()
    app.mainloop()


if __name__ == "__main__":
    run()
