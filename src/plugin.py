import sys
import threading
from PyQt6.QtWidgets import QApplication
from src.ui import SearchOverlay
from src.search import SearchEngine
from src.hotkey import HotkeyListener

class FindBoxPlugin:
    def __init__(self, data_file="keyword.txt"):
        self.data_file = data_file
        self.app = None
        self.window = None
        self.listener = None
        self._thread = None

    def start(self):
        """Starts the plugin in a separate thread (if needed) or prepares it."""
        # PyQt needs to run in the main thread usually. 
        # If integrating into an existing PyQt app, we just need to init the window.
        # If integrating into a non-PyQt app, we need to start a QApplication.
        
        if not QApplication.instance():
            self.app = QApplication(sys.argv)
        else:
            self.app = QApplication.instance()

        self.search_engine = SearchEngine(self.data_file)
        self.window = SearchOverlay(self.search_engine)
        
        self.listener = HotkeyListener()
        self.listener.activated.connect(self.window.show_search)
        self.listener.start()
        
        print("Find Box Plugin Started. Press Ctrl+Alt+F.")

    def run_blocking(self):
        """Runs the application event loop (blocking)."""
        if self.app:
            self.app.exec()

    def stop(self):
        if self.listener:
            self.listener.stop()

# Example usage:
# plugin = FindBoxPlugin()
# plugin.start()
# plugin.run_blocking()
