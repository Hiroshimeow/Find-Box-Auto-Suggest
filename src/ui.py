from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, 
    QListWidget, QApplication, QPushButton
)
from PyQt6.QtCore import Qt, QSize, pyqtSignal, QTimer, QEvent
from PyQt6.QtGui import QColor, QFont, QKeyEvent, QCursor
import os
import ctypes
import sys

class SearchOverlay(QMainWindow):
    def __init__(self, search_engine):
        super().__init__()
        self.search_engine = search_engine
        self._text_before_show = ""
        self.last_active_window_handle = None
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

        # Connect to the application's state change signal for robust hiding
        QApplication.instance().applicationStateChanged.connect(self.on_app_state_changed)

        # Central widget
        self.central_widget = QWidget()
        self.central_widget.setObjectName("CentralWidget")
        self.setCentralWidget(self.central_widget)
        
        # Layout
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Container for border and background
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
        self.list_widget.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.container_layout.addWidget(self.input_row)
        self.container_layout.addWidget(self.list_widget)

        # Styles
        self.apply_styles()

        # Initial size
        self.resize(700, 60)
        
        # Track if current selection is from user keyboard navigation
        self.user_navigating = False

    def on_app_state_changed(self, state):
        """Hides the overlay when the entire application becomes inactive."""
        if self.isVisible() and state == Qt.ApplicationState.ApplicationInactive:
            self.hide()

    def apply_styles(self):
        # Styles content remains the same
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
                font-size: 12px;
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
                font-size: 14px;
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
        
        max_needed_height = 350
        space_below = screen_geo.bottom() - cursor_pos.y()
        
        self.search_direction = 'down'
        if space_below < max_needed_height:
            self.search_direction = 'up'

        if self.search_direction == 'up':
            self.container_layout.removeWidget(self.input_row)
            self.container_layout.removeWidget(self.list_widget)
            self.container_layout.addWidget(self.list_widget)
            self.container_layout.addWidget(self.input_row)
        else:
            self.container_layout.removeWidget(self.input_row)
            self.container_layout.removeWidget(self.list_widget)
            self.container_layout.addWidget(self.input_row)
            self.container_layout.addWidget(self.list_widget)

        x = cursor_pos.x()
        if x + self.width() > screen_geo.right():
            x = screen_geo.right() - self.width() - 10
            
        y = cursor_pos.y() + 20
        if self.search_direction == 'up':
            y = cursor_pos.y() - self.height() - 10

        self.move(x, y)

    def on_data_changed(self):
        if self.isVisible() and self.input_field.text():
            self.on_text_changed(self.input_field.text())

    def on_text_changed(self, text):
        if not text:
            self.list_widget.clear()
            self.list_widget.setVisible(False)
            self.adjust_size()
            return

        results = self.search_engine.search(text)
        
        self.list_widget.itemSelectionChanged.disconnect(self.on_selection_changed)
        
        self.list_widget.clear()
        
        if results:
            self.list_widget.addItems(results)
            self.user_navigating = False
            self.list_widget.setCurrentRow(0)
            self.list_widget.setVisible(True)
            
            # Dynamic height calculation
            count = min(len(results), 6)
            list_height = 0
            if count > 0:
                for i in range(count):
                    # Use sizeHintForRow for an accurate height, with a fallback
                    h = self.list_widget.sizeHintForRow(i)
                    list_height += h if h > 0 else 32
            
            list_height += 4 # Padding
            self.list_widget.setFixedHeight(list_height)
        else:
            self.list_widget.setVisible(False)
        
        self.list_widget.itemSelectionChanged.connect(self.on_selection_changed)
        
        self.adjust_size()

    def adjust_size(self):
        base_height = 60 
        if self.list_widget.isVisible():
            base_height += self.list_widget.height() + 5
        
        old_height = self.height()
        new_height = base_height
        
        self.setFixedSize(self.width(), new_height)
        
        if hasattr(self, 'search_direction') and self.search_direction == 'up':
            diff = new_height - old_height
            if diff != 0:
                self.move(self.x(), self.y() - diff)

    def on_add_keyword(self):
        text = self.input_field.text().strip()
        if not text:
            return
        
        try:
            existing = []
            if os.path.exists(self.search_engine.data_file):
                with open(self.search_engine.data_file, 'r', encoding='utf-8') as f:
                    existing = [line.strip() for line in f.readlines() if line.strip()]
            
            if text in existing:
                print(f"Keyword '{text}' already exists.")
                return
            
            with open(self.search_engine.data_file, 'w', encoding='utf-8') as f:
                f.write(text + '\n')
                for line in existing:
                    f.write(line + '\n')
            
            print(f"Added keyword: {text}")
            
            self.input_field.clear()
            self.hide()
        except Exception as e:
            print(f"Error adding keyword: {e}")

    def hide_if_visible(self):
        if self.isVisible():
            self.hide()

    def on_enter_pressed(self):
        current_item = self.list_widget.currentItem()
        if current_item and self.list_widget.isVisible():
            self.select_item(current_item.text())
        elif self.input_field.text():
            self.select_item(self.input_field.text())
        else:
            self.hide()

    def on_item_clicked(self, item):
        self.select_item(item.text())

    def on_selection_changed(self):
        if not self.user_navigating:
            return
            
        current_item = self.list_widget.currentItem()
        if current_item:
            self.input_field.blockSignals(True)
            self.input_field.setText(current_item.text())
            self.input_field.blockSignals(False)

    def select_item(self, text):
        clipboard = QApplication.clipboard()
        
        if '||' in text:
            parts = text.split('||', 1)
            content = parts[1].strip() if len(parts) > 1 else text
            clipboard.setText(content)
            print(f"Copied: {content}")
        else:
            clipboard.setText(text)
            print(f"Copied: {text}")
        
        self.hide()

        # Try to restore focus to the last active window (Windows specific)
        if self.last_active_window_handle and sys.platform == "win32":
            try:
                user32 = ctypes.windll.user32
                user32.SetForegroundWindow(self.last_active_window_handle)
            except Exception as e:
                print(f"Could not restore focus: {e}")

        self.input_field.clear()

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Escape:
            self.hide()
        elif event.key() == Qt.Key.Key_Down:
            if self.list_widget.isVisible() and self.list_widget.count() > 0:
                self.user_navigating = True
                curr = self.list_widget.currentRow()
                if curr < self.list_widget.count() - 1:
                    self.list_widget.setCurrentRow(curr + 1)
                else:
                    self.list_widget.setCurrentRow(0)
        elif event.key() == Qt.Key.Key_Up:
            if self.list_widget.isVisible() and self.list_widget.count() > 0:
                self.user_navigating = True
                curr = self.list_widget.currentRow()
                if curr > 0:
                    self.list_widget.setCurrentRow(curr - 1)
                else:
                    self.list_widget.setCurrentRow(self.list_widget.count() - 1)
        else:
            super().keyPressEvent(event)

    def changeEvent(self, event: QEvent):
        """Hides the window when it loses focus (is deactivated)."""
        super().changeEvent(event)
        if event.type() == QEvent.Type.ActivationChange:
            if not self.isActiveWindow():
                self.hide()

    def show_search(self):
        # Store previous active window to restore focus later
        if sys.platform == "win32":
            try:
                user32 = ctypes.windll.user32
                self.last_active_window_handle = user32.GetForegroundWindow()
            except Exception as e:
                print(f"Could not get foreground window: {e}")
                self.last_active_window_handle = None

        # Store text before showing to handle hotkey artifact
        self._text_before_show = self.input_field.text()

        self.position_at_cursor()
        self.adjust_size()
        
        self.show()
        self.setWindowState(self.windowState() & ~Qt.WindowState.WindowMinimized | Qt.WindowState.WindowActive)
        self.raise_()
        self.activateWindow()
        
        # Robust Focus Stealing for Windows
        if sys.platform == "win32":
            try:
                our_hwnd = int(self.winId())
                user32 = ctypes.windll.user32
                
                foreground_hwnd = user32.GetForegroundWindow()
                if foreground_hwnd != our_hwnd:
                    foreground_thread_id = user32.GetWindowThreadProcessId(foreground_hwnd, None)
                    app_thread_id = user32.GetWindowThreadProcessId(our_hwnd, None)
                    
                    if foreground_thread_id != app_thread_id:
                        user32.AttachThreadInput(foreground_thread_id, app_thread_id, True)
                        user32.SetForegroundWindow(our_hwnd)
                        user32.SetFocus(our_hwnd)
                        user32.AttachThreadInput(foreground_thread_id, app_thread_id, False)
                    else:
                        user32.SetForegroundWindow(our_hwnd)
            except Exception as e:
                print(f"Focus error: {e}")

        self.input_field.setFocus()
        self.input_field.end(False)
        
        QTimer.singleShot(50, self._delayed_focus)
        QTimer.singleShot(100, self._delayed_focus)
        QTimer.singleShot(50, self._clean_hotkey_artifact)

        # Trigger search for any pre-existing text when shown
        QTimer.singleShot(110, lambda: self.on_text_changed(self.input_field.text()))

    def _delayed_focus(self):
        if self.isVisible():
            self.input_field.setFocus()
            self.input_field.end(False)
    
    def _clean_hotkey_artifact(self):
        if self.isVisible():
            current_text = self.input_field.text()
            if current_text.lower() == (self._text_before_show + 'f').lower():
                self.input_field.setText(self._text_before_show)
