**Agents Guide**

- Purpose: provide build / lint / test commands and repository coding conventions for automated coding agents working in this repository.
- Location notes: project layout is described in `plan.md`; source lives under `src/`, tests under `tests/`, and runtime deps in `requirements.txt`.

---

**Build & Environment**
- Use a virtual environment (recommended `venv` or `poetry`). Typical setup:

```bash
# create and activate venv (Unix)
python -m venv .venv
source .venv/bin/activate
# install runtime deps
python -m pip install -r requirements.txt
# install dev tools for lint/test/type-check
python -m pip install -r requirements-dev.txt  # optional if present
```

- Run the app (GUI entry point is expected under `src/tak_flashcard/gui/app.py` per `plan.md`):

```bash
python -m tak_flashcard.gui.app
```

If the repository uses a different entrypoint, check `src/` for a suitable `__main__` or CLI script.

---

**Tests**
- The project uses `pytest` (see `plan.md`). Basic commands:

```bash
# run full test suite
pytest

# run a single test file
pytest tests/test_foo.py

# run a single test case inside a file
pytest tests/test_foo.py::test_bar

# run tests matching keyword
pytest -k "keyword"

# verbose and show print output
pytest -q -s
```

- Use an in-memory SQLite DB for unit tests that touch the DB: configure fixtures to use `sqlite:///:memory:`.
- Keep tests deterministic and isolated: use `tmp_path` or `tmp_path_factory` for filesystem side-effects.

---

**Linting & Formatting**
- Recommended toolchain (try to mirror the project's current setup or add these dev-deps):

- `black` — code formatter (stable, zero-config)
- `isort` — sort imports (use `profile = black` in `pyproject.toml` for compatibility)
- `ruff` or `flake8` — lightweight linting (ruff can replace many linters)
- `mypy` — optional static type checking

Common commands:

```bash
# format everything
black src tests
# sort imports
isort src tests
# lint
ruff check src tests || flake8 src tests
# type-check (if used)
```

- Pre-commit: if `pre-commit` is used, run `pre-commit run --all-files` before commits.

---

**Packaging / Build**
- For distribution (desktop bundle): use PyInstaller or similar as suggested in `plan.md` (e.g. `scripts/build_windows.sh` or `build_windows.bat`). Keep packaging scripts under `scripts/`.

---

**Repository files to check**
- `requirements.txt` — runtime deps
- `plan.md` — design & expected layout
- `src/` — source packages
- `tests/` — test suite
- `scripts/` — helper scripts

---

**Code Style Guidelines**
- Purpose: keep code readable, predictable, and safe for agentic edits. Follow these rules strictly.

- Formatting
  - Use `black` formatting rules: 88-char line length by default. Let `black` make formatting decisions.
  - Use `isort` to order imports (sections: stdlib, third-party, local). Use `profile = black` for compatible formatting.
  - Prefer simple, short functions (single responsibility). When a function exceeds ~120 lines, consider splitting.

- Imports
  - Group imports in three sections separated by a blank line: standard library, third-party, local application.
  - Use explicit imports (from X import Y) for commonly used names; avoid `from module import *`.
  - Keep import order alphabetical within sections; let `isort` enforce this.

- Typing & Annotations
  - Add type hints for public functions, methods, and module-level APIs.
  - Use `typing` types (e.g., `list[str]`, `dict[str, Any]`) — prefer modern annotations (PEP 585) where supported.
  - Avoid `Any` in public interfaces; if used temporarily, add a `# TODO: narrow type` comment.
  - Run `mypy` for candidate modules and keep `--strict` for critical core modules (DB layer, core session engine).

- Naming Conventions
  - Modules & packages: lowercase_with_underscores (e.g., `importers`, `session_engine.py`).
  - Functions & variables: `snake_case`.
  - Classes: `PascalCase` (CamelCase without underscores).
  - Constants: `UPPER_SNAKE_CASE`.
  - Tests: file `test_*.py`, test functions `test_*`.

- Project Structure & Modules
  - `src/` is the application root package. Prefer absolute imports from `tak_flashcard` (e.g., `from tak_flashcard.db import db`), or use explicit relative imports inside packages.
  - Keep database models in `db/models.py`, DB logic in `db/db.py`, core session logic in `core/`, GUI code in `gui/`, and importers in `importers/` as described in `plan.md`.

- Error Handling
  - Use the `logging` module for non-fatal messages; don't use `print()` in production code (tests may assert on stdout sometimes — prefer `capfd` fixtures).
  - Prefer explicit exception types. Create custom exceptions for domain errors (e.g., `ImportError`, `ValidationError`, `SessionError`) under `src/tak_flashcard/errors.py` or similar.
  - Avoid broad `except:` blocks. Catch specific exceptions and either handle or re-raise with context using `raise ... from exc`.
  - Clean up resources with `with` context managers (DB sessions, file handles).

- Logging
  - Use module-level logger: `logger = logging.getLogger(__name__)`.
  - Log at appropriate levels: `debug` for development details, `info` for user-level events, `warning` for recoverable issues, `error` for failures.

- Database & Persistence
  - Use SQLAlchemy session-per-thread pattern. Do not share sessions between threads.
  - Use transactions for multi-row writes and batch operations; commit as late as possible.
  - For tests use `sqlite:///:memory:` and explicit schema creation via `Base.metadata.create_all(bind=engine)` or fixtures.

- Concurrency
  - Long-running or blocking work (importer, heavy IO) should run in worker threads/processes; communicate with GUI via thread-safe queues or callbacks.

- Security & Secrets
  - Do not commit secrets. Use environment variables or `.env` files read by `python-dotenv` if necessary; keep `.env` out of git.

---

**Testing Conventions**
- Unit tests: small, fast, no network or file system side effects unless explicit.
- Integration tests: explicit markers (e.g., `@pytest.mark.integration`) and run separately.
- Fixtures: use pytest fixtures for DB setup/teardown; prefer `scope='function'` for isolation unless expensive.
- Mocking: prefer `monkeypatch` or `pytest-mock` over heavy mocking frameworks.

---

**Commit & PR hygiene**
- Keep commits small and focused. Include a short descriptive message (1 sentence) and a longer body if needed.
- Add tests for any behavioral changes. Run `pytest` and linters locally before creating a PR.

---

**Agent Interaction Rules**
- When an agent edits files:
  1. Make a single logical change per commit.
  2. Do not revert unrelated working-tree changes; only modify files required for the task.
  3. Do not amend commits unless explicitly requested.
  4. If creating commits, show the user the commands you ran and the commit message.

- Cursor & Copilot rules:
  - This repository does not contain `.cursor/rules/` or `.cursorrules` files and does not include `.github/copilot-instructions.md` at the time of writing. If such files are added later, agents must read them and obey any additional rules contained there.

---

**Where to look for more context**
- `plan.md` — project design and expected file locations.
- `requirements.txt` — runtime dependencies.
- `tests/` — existing tests and test patterns to mimic.
