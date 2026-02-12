"""Main entry point for the application."""

import sys
from tak_flashcard.db import init_db
from tak_flashcard.data.seed import check_and_import_if_needed
from tak_flashcard.gui.app import create_app


def main():
    """
    Main function to start the application.

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    try:
        print("Initializing database...")
        init_db()

        print("Checking vocabulary data...")
        success, message = check_and_import_if_needed()
        print(message)

        if not success:
            print("ERROR: Failed to initialize vocabulary data.")
            print("Please ensure vocab_source.csv exists in data/vocab/ directory.")
            return 1

        print("Starting application...")
        app = create_app()
        app.setup()
        app.run()

        return 0

    except Exception as e:
        print(f"ERROR: Application failed to start: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
