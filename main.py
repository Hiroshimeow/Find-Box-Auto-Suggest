from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import QLockFile, QDir, QTimer
from src.ui import SearchOverlay
from src.search import SearchEngine
from src.hotkey import HotkeyListener
import os
import sys
import signal

def main():
    # Allow Ctrl+C to exit the app
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    
    app = QApplication(sys.argv)
    
    # This timer allows the Python interpreter to run every 500ms
    # to process signals like Ctrl+C
    timer = QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None) # No-op
    
    # Singleton Check
    lock_file = QLockFile(os.path.join(QDir.tempPath(), 'find_box_auto_suggest.lock'))
    if not lock_file.tryLock(100):
        # App is already running
        print("Application is already running.")
        sys.exit(1)
    
    # Initialize components
    search_engine = SearchEngine("keyword.txt")
    window = SearchOverlay(search_engine)
    
    # Initialize Hotkey Listener
    hotkey_listener = HotkeyListener()
    
    # Connect signal
    hotkey_listener.activated.connect(window.show_search)
    hotkey_listener.escape_pressed.connect(window.hide_if_visible)
    
    hotkey_listener.start()
    
    print("App is running. Press Ctrl+C to exit.")
    print("Press Ctrl+Alt+F to toggle search.")
    
    # Run the event loop
    try:
        sys.exit(app.exec())
    finally:
        hotkey_listener.stop()

if __name__ == "__main__":
    main()
