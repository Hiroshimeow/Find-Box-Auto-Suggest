import os
from typing import List
from PyQt6.QtCore import QFileSystemWatcher, QObject, pyqtSignal

class SearchEngine(QObject):
    data_changed = pyqtSignal()

    def __init__(self, data_file: str = "keyword.txt"):
        super().__init__()
        self.data_file = os.path.abspath(data_file)
        self.data: List[str] = []
        self.load_data()
        
        # Watch for file changes
        self.watcher = QFileSystemWatcher()
        if os.path.exists(self.data_file):
            self.watcher.addPath(self.data_file)
        self.watcher.fileChanged.connect(self.on_file_changed)

    def on_file_changed(self, path):
        print(f"File changed: {path}")
        self.load_data()
        self.data_changed.emit()

    def load_data(self):
        """Loads data from the TXT file (one phrase per line)."""
        if not os.path.exists(self.data_file):
            print(f"Warning: {self.data_file} not found.")
            self.data = []
            return

        try:
            # Add a small delay or retry mechanism might be needed if file is being written to
            # But for now, direct read.
            with open(self.data_file, 'r', encoding='utf-8') as f:
                # Read lines and strip whitespace
                lines = [line.strip() for line in f.readlines()]
                # Filter out empty lines
                self.data = [line for line in lines if line]
            print(f"Loaded {len(self.data)} keywords.")
        except Exception as e:
            print(f"Error loading data: {e}")
            self.data = []

    def search(self, query: str, limit: int = 10) -> List[str]:
        """
        Searches for the query in the data.
        Returns a list of matching strings, case-insensitive.
        """
        if not query:
            return []

        query = query.lower()
        # Simple containment search. Can be improved with fuzzy search if needed.
        # Prioritize starts_with for better UX?
        # For now, just simple 'in' check.
        
        matches = []
        count = 0
        
        # First pass: starts with
        for item in self.data:
            if item.lower().startswith(query):
                matches.append(item)
                count += 1
                if count >= limit:
                    return matches

        # Second pass: contains (but not starts with)
        for item in self.data:
            if query in item.lower() and item not in matches:
                matches.append(item)
                count += 1
                if count >= limit:
                    return matches
                    
        return matches
