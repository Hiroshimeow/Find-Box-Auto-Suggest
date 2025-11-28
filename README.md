# Auto-Suggest

Auto-Suggest is a powerful and intuitive productivity tool designed to help you quickly find and launch applications, commands, or information directly from your desktop. Triggered by a simple hotkey, it provides instant, context-aware suggestions, streamlining your workflow and keeping you focused.

## Features

*   **Instant Search:** Quickly search for anything with a few keystrokes.
*   **Hotkey Activation:** Access the tool instantly from anywhere with a configurable global hotkey (default: `Ctrl+Alt+F`).
*   **Clean & Simple UI:** A minimal and unobtrusive interface that stays out of your way.
*   **Extensible via Plugins:** Easily add new search sources or functionalities through a plugin architecture.

## Screenshot

Here's a glimpse of Auto-Suggest in action:

![Auto-Suggest in action](src/image_sample.png)

## Installation

To get Auto-Suggest up and running, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/auto-suggest.git
    cd auto-suggest
    ```
    (Replace `https://github.com/your-username/auto-suggest.git` with the actual repository URL if it exists, or remove this line if it's a local project without a remote.)

2.  **Install dependencies:**
    Make sure you have Python 3.x and `pip` installed.
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Once installed, you can run Auto-Suggest:

```bash
python main.py
```

After launching, press the default hotkey (`Ctrl+Alt+F`) to bring up the search bar. Start typing, and Auto-Suggest will provide real-time suggestions. Select an option using the arrow keys and press `Enter` to execute or open it.
