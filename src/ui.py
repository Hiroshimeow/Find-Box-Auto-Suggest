from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, 
    QListWidget, QApplication, QPushButton
)
from PyQt6.QtCore import Qt, QSize, pyqtSignal, QTimer
from PyQt6.QtGui import QColor, QFont, QKeyEvent, QCursor
import os

class SearchOverlay(QMainWindow):
    def __init__(self, search_engine):
        super().__init__()
        self.search_engine = search_engine
        self.init_ui()
        
        # Connect data reload signal
        if hasattr(self.search_engine, 'data_changed'):
            self.search_engine.data_changed.connect(self.on_data_changed)

    def init_ui(self):
        # Window flags
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.WindowStaysOnTopHint | 
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Central widget
        self.central_widget = QWidget()
        self.central_widget.setObjectName("CentralWidget")
        self.setCentralWidget(self.central_widget)
        
        # Layout
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Container for border and background
        # We use a container to draw the border/background manually via stylesheet
        # This avoids the UpdateLayeredWindowIndirect issues with complex effects
        self.container = QWidget()
        self.container.setObjectName("Container")
        self.layout.addWidget(self.container)

        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setContentsMargins(10, 10, 10, 10)
        self.container_layout.setSpacing(5)

        # Input Row (Input field + Add button)
        self.input_row = QWidget()
        self.input_row_layout = QHBoxLayout(self.input_row)
        self.input_row_layout.setContentsMargins(0, 0, 0, 0)
        self.input_row_layout.setSpacing(5)

        # Input Field
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Type to search...")
        self.input_field.setFixedHeight(40)
        # Use textEdited instead of textChanged to avoid issues during programmatic updates
        self.input_field.textEdited.connect(self.on_text_changed)
        self.input_field.returnPressed.connect(self.on_enter_pressed)
        
        # Add Button
        self.add_button = QPushButton("+")
        self.add_button.setFixedSize(40, 40)
        self.add_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.add_button.clicked.connect(self.on_add_keyword)
        self.add_button.setToolTip("Add current text to keywords")
        
        self.input_row_layout.addWidget(self.input_field)
        self.input_row_layout.addWidget(self.add_button)
        
        # Suggestions List
        self.list_widget = QListWidget()
        self.list_widget.setVisible(False)
        self.list_widget.itemClicked.connect(self.on_item_clicked)
        self.list_widget.itemSelectionChanged.connect(self.on_selection_changed)
        # Prevent focus stealing by the list widget
        self.list_widget.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.container_layout.addWidget(self.input_row)
        self.container_layout.addWidget(self.list_widget)

        # Styles
        self.apply_styles()

        # Initial size - wider for Vietnamese and long text
        self.resize(700, 60)
        
        # Track if we should hide on focus loss
        self.should_hide_on_focus_loss = True
        
        # Track if current selection is from user keyboard navigation
        self.user_navigating = False
        
        # Install event filter on application to catch clicks outside
        QApplication.instance().installEventFilter(self)

    def apply_styles(self):
        # Dark theme with high contrast
        self.setStyleSheet("""
            #Container {
                background-color: #1e1e1e;
                border: 1px solid #454545;
                border-radius: 8px;
            }
            QLineEdit {
                background-color: #2d2d2d;
                color: #e0e0e0;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                padding: 4px 8px;
                font-family: 'Segoe UI', sans-serif;
                font-size: 12px; /* Smaller font for input */
                selection-background-color: #0078d4;
            }
            QLineEdit:focus {
                border: 1px solid #0078d4;
            }
            QListWidget {
                background-color: #2d2d2d;
                color: #e0e0e0;
                border: none;
                border-radius: 4px;
                outline: none;
                margin-top: 5px;
                font-size: 14px; /* Normal font for list */
            }
            QListWidget::item {
                padding: 6px 8px;
                min-height: 20px;
                border-radius: 4px;
            }
            QListWidget::item:selected {
                background-color: #0078d4;
                color: white;
            }
            QListWidget::item:hover {
                background-color: #3d3d3d;
            }
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                border-radius: 4px;
                font-size: 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #005a9e;
            }
            QPushButton:pressed {
                background-color: #004578;
            }
        """)

    def position_at_cursor(self):
        cursor_pos = QCursor.pos()
        screen = QApplication.screenAt(cursor_pos)
        if not screen:
            screen = QApplication.primaryScreen()
        
        screen_geo = screen.availableGeometry()
        
        # Determine direction
        # If cursor is in the bottom half/third of the screen, go UP
        # Or better: check if there is enough space for max height (approx 350px)
        max_needed_height = 350
        space_below = screen_geo.bottom() - cursor_pos.y()
        
        if space_below < max_needed_height:
            self.search_direction = 'up'
        else:
            self.search_direction = 'down'

        # Update Layout Order
        if self.search_direction == 'up':
            # List on top, Input on bottom
            self.container_layout.removeWidget(self.input_row)
            self.container_layout.removeWidget(self.list_widget)
            self.container_layout.addWidget(self.list_widget)
            self.container_layout.addWidget(self.input_row)
        else:
            # Input on top, List on bottom
            self.container_layout.removeWidget(self.input_row)
            self.container_layout.removeWidget(self.list_widget)
            self.container_layout.addWidget(self.input_row)
            self.container_layout.addWidget(self.list_widget)

        # Calculate X
        x = cursor_pos.x()
        if x + self.width() > screen_geo.right():
            x = screen_geo.right() - self.width() - 10
            
        # Calculate Y
        if self.search_direction == 'up':
            # Position bottom of window near cursor
            # We need to know current height. 
            # If we are just showing, height might be small (just input).
            # adjust_size will handle the growth, but initial Y must be set.
            y = cursor_pos.y() - self.height() - 10
        else:
            y = cursor_pos.y() + 20

        self.move(x, y)

    def on_data_changed(self):
        # Refresh current search if visible
        if self.isVisible() and self.input_field.text():
            self.on_text_changed(self.input_field.text())

    def on_text_changed(self, text):
        if not text:
            self.list_widget.clear()
            self.list_widget.setVisible(False)
            self.adjust_size()
            return

        results = self.search_engine.search(text)
        
        # Temporarily disconnect to prevent auto-fill when populating list
        self.list_widget.itemSelectionChanged.disconnect(self.on_selection_changed)
        
        self.list_widget.clear()
        
        if results:
            self.list_widget.addItems(results)
            # Auto-select first item for visual highlight (but don't auto-fill)
            self.user_navigating = False
            self.list_widget.setCurrentRow(0)
            self.list_widget.setVisible(True)
            
            item_height = 28 # Adjusted for new padding/font
            count = min(len(results), 10)
            # Add a small buffer to prevent scrollbar if exactly 10
            list_height = count * item_height + 4 
            self.list_widget.setFixedHeight(list_height)
        else:
            self.list_widget.setVisible(False)
        
        # Reconnect signal
        self.list_widget.itemSelectionChanged.connect(self.on_selection_changed)
        
        self.adjust_size()

    def adjust_size(self):
        # Calculate required height
        # Input height (40) + Margins (10+10) + Spacing (5 if list visible)
        base_height = 60 
        if self.list_widget.isVisible():
            base_height += self.list_widget.height() + 5
        
        old_height = self.height()
        new_height = base_height
        
        # Force resize immediately
        self.setFixedSize(self.width(), new_height)
        
        # If growing UP, we need to move the window up by the difference
        if hasattr(self, 'search_direction') and self.search_direction == 'up':
            diff = new_height - old_height
            if diff != 0:
                self.move(self.x(), self.y() - diff)

    def on_add_keyword(self):
        """Add current input text to keyword.txt at the top."""
        text = self.input_field.text().strip()
        if not text:
            return
        
        try:
            # Read existing keywords
            existing = []
            if os.path.exists(self.search_engine.data_file):
                with open(self.search_engine.data_file, 'r', encoding='utf-8') as f:
                    existing = [line.strip() for line in f.readlines() if line.strip()]
            
            # Check if keyword already exists
            if text in existing:
                print(f"Keyword '{text}' already exists.")
                return
            
            # Write new keyword at the top
            with open(self.search_engine.data_file, 'w', encoding='utf-8') as f:
                f.write(text + '\n')
                for line in existing:
                    f.write(line + '\n')
            
            print(f"Added keyword: {text}")
            # The file watcher will auto-reload
            
            # Clear input and hide
            self.input_field.clear()
            self.hide()
        except Exception as e:
            print(f"Error adding keyword: {e}")

    def hide_if_visible(self):
        if self.isVisible():
            self.hide()
            # Do NOT clear input, preserve state
            # self.input_field.clear()

    def on_enter_pressed(self):
        # If there's a selected item in the list, copy it
        current_item = self.list_widget.currentItem()
        if current_item and self.list_widget.isVisible():
            self.select_item(current_item.text())
        elif self.input_field.text():
            # No selection but has text - copy the typed text
            self.select_item(self.input_field.text())
        else:
            # Nothing to copy, just hide
            self.hide()

    def on_item_clicked(self, item):
        self.select_item(item.text())

    def on_selection_changed(self):
        """When user navigates with arrow keys, fill input with selected item."""
        # Only fill input if this is from user keyboard navigation
        if not self.user_navigating:
            return
            
        current_item = self.list_widget.currentItem()
        if current_item:
            # Fill input field with selected keyword without triggering search
            self.input_field.blockSignals(True)
            self.input_field.setText(current_item.text())
            self.input_field.blockSignals(False)

    def select_item(self, text):
        clipboard = QApplication.clipboard()
        clipboard.setText(text)
        # Clear after selection as action is complete
        self.input_field.clear()
        self.hide()

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Escape:
            self.hide()
            # Do NOT clear input on ESC
        elif event.key() == Qt.Key.Key_Down:
            if self.list_widget.isVisible() and self.list_widget.count() > 0:
                self.user_navigating = True  # User is navigating
                curr = self.list_widget.currentRow()
                if curr < self.list_widget.count() - 1:
                    self.list_widget.setCurrentRow(curr + 1)
                else:
                    # Wrap to first item
                    self.list_widget.setCurrentRow(0)
        elif event.key() == Qt.Key.Key_Up:
            if self.list_widget.isVisible() and self.list_widget.count() > 0:
                self.user_navigating = True  # User is navigating
                curr = self.list_widget.currentRow()
                if curr > 0:
                    self.list_widget.setCurrentRow(curr - 1)
                else:
                    # Wrap to last item
                    self.list_widget.setCurrentRow(self.list_widget.count() - 1)
        else:
            super().keyPressEvent(event)

    def eventFilter(self, obj, event):
        """Filter app events to detect clicks outside the window."""
        if event.type() == event.Type.MouseButtonPress:
            # Check if click is outside our window
            if self.isVisible():
                click_pos = event.globalPosition().toPoint()
                window_rect = self.geometry()
                if not window_rect.contains(click_pos):
                    # Click outside - hide
                    self.hide()
                    return False  # Don't consume the event
        return super().eventFilter(obj, event)

    def event(self, event):
        """Override event to catch window deactivation."""
        if event.type() == event.Type.WindowDeactivate:
            # Window lost focus - hide after small delay
            QTimer.singleShot(150, self._check_and_hide)
        elif event.type() == event.Type.Show:
            # When window is shown, ensure it's activated
            QTimer.singleShot(10, self.activateWindow)
        return super().event(event)

    def _check_and_hide(self):
        """Check if we should hide after losing focus."""
        if self.should_hide_on_focus_loss and not self.isActiveWindow():
            self.hide()

    def show_search(self):
        # Always reposition at cursor (remove the "if not visible" check)
        self.position_at_cursor()
        self.adjust_size() # Ensure correct size based on current state
        
        # Always show
        self.show()
        self.setWindowState(self.windowState() & ~Qt.WindowState.WindowMinimized | Qt.WindowState.WindowActive)
        self.raise_()
        self.activateWindow()
        
        # Robust Focus Stealing for Windows
        try:
            import ctypes
            from ctypes import wintypes
            
            hwnd = int(self.winId())
            user32 = ctypes.windll.user32
            
            # Get current foreground window and threads
            foreground_hwnd = user32.GetForegroundWindow()
            if foreground_hwnd != hwnd:
                foreground_thread_id = user32.GetWindowThreadProcessId(foreground_hwnd, None)
                app_thread_id = user32.GetWindowThreadProcessId(hwnd, None)
                
                # Attach thread input if different
                if foreground_thread_id != app_thread_id:
                    user32.AttachThreadInput(foreground_thread_id, app_thread_id, True)
                    user32.SetForegroundWindow(hwnd)
                    user32.SetFocus(hwnd)
                    user32.AttachThreadInput(foreground_thread_id, app_thread_id, False)
                else:
                    user32.SetForegroundWindow(hwnd)
        except Exception as e:
            print(f"Focus error: {e}")

        # Qt Focus - immediate and delayed
        self.input_field.setFocus()
        self.input_field.end(False)
        
        # Delayed focus as backup (Qt events need to process)
        QTimer.singleShot(50, self._delayed_focus)
        QTimer.singleShot(100, self._delayed_focus)
        
        # Clear stray 'F' from hotkey if it appears
        QTimer.singleShot(50, self._clean_hotkey_artifact)

    def _delayed_focus(self):
        """Delayed focus helper."""
        if self.isVisible():
            self.input_field.setFocus()
            self.input_field.end(False)
    
    def _clean_hotkey_artifact(self):
        """Remove stray 'F' character from Ctrl+Alt+F hotkey."""
        if self.isVisible():
            current_text = self.input_field.text()
            # If text is just "F" or "f", clear it (it's from the hotkey)
            if current_text.lower() in ['f', 'F']:
                self.input_field.clear()
