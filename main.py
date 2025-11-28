from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import QLockFile, QDir
from src.ui import SearchOverlay
from src.search import SearchEngine
from src.hotkey import HotkeyListener
import os
import sys

def main():
    app = QApplication(sys.argv)
    
    # Singleton Check
    lock_file = QLockFile(os.path.join(QDir.tempPath(), 'find_box_auto_suggest.lock'))
    if not lock_file.tryLock(100):
        # App is already running
        print("Application is already running.")
        # Optional: Could try to activate the existing window here if we had IPC
        sys.exit(1)
    
    # Initialize components
    search_engine = SearchEngine("keyword.txt")
    window = SearchOverlay(search_engine)
    
    # Initialize Hotkey Listener
    hotkey_listener = HotkeyListener()
    
    # Connect signal
    # Note: The signal comes from a different thread, but PyQt handles this safely 
    # via queued connection by default for signals between threads.
    hotkey_listener.activated.connect(window.show_search)
    hotkey_listener.escape_pressed.connect(window.hide_if_visible)
    
    hotkey_listener.start()
    
    print("App is running. Press Ctrl+Alt+F to toggle search.")
    
    # Run the event loop
    try:
        sys.exit(app.exec())
    finally:
        hotkey_listener.stop()

if __name__ == "__main__":
    main()
