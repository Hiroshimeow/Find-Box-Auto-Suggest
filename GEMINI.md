# GEMINI.md - Project Context for `auto-suggest`

## Project Overview

This project is a desktop utility for Windows that provides a quick-search "find box" overlay. It allows users to press a global hotkey to summon a search input at their mouse cursor. As the user types, the application displays auto-suggested keywords from a local file. Selecting an item copies it to the clipboard.

The application is built with Python and uses the following main technologies:
-   **GUI Framework**: `PyQt6` is used to create the frameless, transparent search overlay and manage UI elements.
-   **Global Hotkeys**: The `pynput` library is used to listen for global keyboard events (e.g., the hotkey to trigger the search box and the 'ESC' key to close it) without needing the application window to be in focus.

The architecture is modular:
-   `main.py` serves as the entry point, initializing all components and the application event loop. It includes a singleton pattern to ensure only one instance of the app can run at a time.
-   `src/ui.py` (`SearchOverlay`): Manages the entire visual component, including rendering the input field and the suggestions list.
-   `src/search.py` (`SearchEngine`): Handles loading keywords from `keyword.txt`, performing the search logic, and watching the keyword file for changes to reload automatically.
-   `src/hotkey.py` (`HotkeyListener`): Runs in a separate thread to listen for global hotkeys without blocking the main application.
-   `src/plugin.py` (`FindBoxPlugin`): Exposes the core functionality in a class structure, suggesting it's designed to be potentially integrated into other tools.

## Building and Running

### 1. Installation

To install the required dependencies, run the following command in your terminal:

```sh
pip install -r requirements.txt
```

### 2. Running the Application

To start the application, run:

```sh
python main.py
```

The application will run in the background. To open the search box, press the global hotkey `Ctrl + Alt + F`.

### 3. Testing

There are no automated tests included in this project. Manual testing is required to verify functionality.

## Development Conventions

-   **Code Style**: The code follows general PEP 8 conventions for Python. It is written in a procedural style with classes encapsulating major components (UI, Search, Hotkeys).
-   **Dependencies**: Project dependencies are managed in `requirements.txt`.
-   **Configuration**: The primary data source for the search is the `keyword.txt` file, which is expected to be in the root directory. Each line in this file is treated as a separate keyword.
-   **Concurrency**: A `threading.Thread` is used in the `HotkeyListener` to monitor for keyboard input globally without blocking the PyQt event loop. Communication back to the main UI thread is handled safely via PyQt's signal/slot mechanism.
-   **Extensibility**: The presence of `src/plugin.py` indicates an intention for the project to be extensible or embeddable in other applications.
