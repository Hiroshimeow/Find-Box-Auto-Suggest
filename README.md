# Find Box Auto-Suggest - Quick Start

## Installation
```powershell
pip install -r requirements.txt
```

## Usage
```powershell
python main.py
```

Press `Ctrl + Alt + F` to open the search box at your mouse cursor.

## Adding Keywords
Edit `keyword.txt` - one phrase per line:
```
your first phrase
another phrase
search term example
```

## Features
- **Global Hotkey**: `Ctrl + Alt + F`
- **Mouse Positioning**: Box appears at cursor
- **Clipboard Copy**: Click/Enter to copy selected item
- **ESC to Close**: Hide anytime with ESC
- **Plugin Ready**: Import via `from src.plugin import FindBoxPlugin`
