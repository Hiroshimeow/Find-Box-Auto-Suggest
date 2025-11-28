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
        Searches for all query words in the data.
        Returns a list of matching strings, case-insensitive.
        Words can appear in any order.
        
        Format support: "shortcut||content"
        - Search both shortcut and content parts
        - Prioritize matches in the shortcut part (before ||)
        """
        if not query:
            return []

        query_words = query.lower().split()
        if not query_words:
            return []

        matches = []
        
        # Parse data into structured format
        parsed_items = []
        for item in self.data:
            if '||' in item:
                parts = item.split('||', 1)
                shortcut = parts[0].strip()
                content = parts[1].strip() if len(parts) > 1 else ''
                parsed_items.append({
                    'display': item,
                    'shortcut_lower': shortcut.lower(),
                    'content_lower': content.lower()
                })
            else:
                # No separator, treat whole line as both shortcut and content
                parsed_items.append({
                    'display': item,
                    'shortcut_lower': item.lower(),
                    'content_lower': item.lower()
                })

        def all_words_in(text, words):
            return all(word in text for word in words)

        # Priority 1: All words in shortcut
        for item in parsed_items:
            if all_words_in(item['shortcut_lower'], query_words):
                if item['display'] not in matches:
                    matches.append(item['display'])
                    if len(matches) >= limit:
                        return matches
        
        # Priority 2: All words in content
        for item in parsed_items:
            if all_words_in(item['content_lower'], query_words):
                if item['display'] not in matches:
                    matches.append(item['display'])
                    if len(matches) >= limit:
                        return matches
                    
        return matches
